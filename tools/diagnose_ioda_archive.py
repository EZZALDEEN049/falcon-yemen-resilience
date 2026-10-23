#!/usr/bin/env python3
"""Evidence-safe IODA API availability audit.

Distinguishes a successful HTTP response containing no archived signal samples
from transport failure, parsing failure, and genuine numeric time-series data.
Never substitutes values from published figures or a different time period.
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://api.ioda.inetintel.cc.gatech.edu/v2/signals/raw"
USER_AGENT = "FALCON-Yemen-Research-Archive-Audit/1.0"
CASES = [
    ("2020_AS30873", "asn", "30873", "2020-01-08T00:00:00Z", "2020-01-12T00:00:00Z", None),
    ("2020_AS12486", "asn", "12486", "2020-01-08T00:00:00Z", "2020-01-12T00:00:00Z", None),
    ("2020_YE", "country", "YE", "2020-01-08T00:00:00Z", "2020-01-12T00:00:00Z", None),
    ("2020_AS30873_BGP", "asn", "30873", "2020-01-08T00:00:00Z", "2020-01-12T00:00:00Z", "bgp"),
    ("2020_AS30873_PING", "asn", "30873", "2020-01-08T00:00:00Z", "2020-01-12T00:00:00Z", "ping-slash24"),
    ("2023_AS30873", "asn", "30873", "2023-11-09T00:00:00Z", "2023-11-11T12:00:00Z", None),
    ("2026_AS30873_CONTROL", "asn", "30873", "2026-10-15T00:00:00Z", "2026-10-16T00:00:00Z", None),
    ("2026_YE_CONTROL", "country", "YE", "2026-10-15T00:00:00Z", "2026-10-16T00:00:00Z", None),
]


def unix(s):
    return int(dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp())


def count_native_points(obj):
    """Count native numeric series only; do not count envelope metadata/perf metrics."""
    if isinstance(obj, dict):
        values = obj.get("values")
        if isinstance(values, list) and isinstance(obj.get("datasource"), str):
            return sum(isinstance(v, (int, float)) and not isinstance(v, bool) for v in values)
        total = 0
        for key in ("data", "series", "signals", "results"):
            if key in obj:
                total += count_native_points(obj[key])
        return total
    if isinstance(obj, list):
        return sum(count_native_points(x) for x in obj)
    return 0


def summarize_payload(payload):
    if not isinstance(payload, dict):
        return {"classification": "UNEXPECTED_ENVELOPE", "numeric_points": 0}
    if payload.get("error"):
        return {"classification": "API_ERROR_ENVELOPE", "numeric_points": 0, "api_error": str(payload["error"])[:400]}
    pts = count_native_points(payload.get("data", payload))
    if pts:
        return {"classification": "NATIVE_SERIES_PRESENT_NOT_YET_VALIDATED", "numeric_points": pts}
    data = payload.get("data")
    return {
        "classification": "HTTP_200_EMPTY_ARCHIVE_RESPONSE" if isinstance(data, list) and not any(data) else "NO_RECOGNIZED_NATIVE_SERIES",
        "numeric_points": 0,
        "data_shape": repr(data)[:160],
    }


def request_one(case, out, timeout):
    tag, entity_type, entity_code, start, end, datasource = case
    query = {"from": unix(start), "until": unix(end)}
    if datasource:
        query["datasource"] = datasource
    url = f"{BASE}/{entity_type}/{entity_code}?" + urllib.parse.urlencode(query)
    result = {"case": tag, "entity_type": entity_type, "entity_code": entity_code,
              "from_utc": start, "until_utc": end, "datasource_filter": datasource}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read(10_000_001)
            if len(raw) > 10_000_000:
                raise ValueError("Response exceeded the 10 MB safety cap")
            result["http_status"] = response.status
        result["sha256"] = hashlib.sha256(raw).hexdigest()
        raw_path = out / f"{tag}.json"
        raw_path.write_bytes(raw)
        result["source_response"] = raw_path.name
        payload = json.loads(raw)
        result.update(summarize_payload(payload))
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        result.update({"classification": "TRANSPORT_OR_JSON_ERROR", "numeric_points": 0,
                       "error": f"{type(exc).__name__}: {str(exc)[:350]}"})
    return result


def run(out, timeout):
    out.mkdir(parents=True, exist_ok=True)
    cases = [request_one(c, out, timeout) for c in CASES]
    old_cases = [x for x in cases if x["case"].startswith("2020_")]
    control_cases = [x for x in cases if x["case"].startswith("2026_")]
    old_nonempty = any(x["numeric_points"] for x in old_cases)
    controls_nonempty = any(x["numeric_points"] for x in control_cases)
    result = {
        "evaluated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status": ("2020_NATIVE_AVAILABLE_REQUIRES_SEMANTIC_VALIDATION" if old_nonempty else
                   "2020_EMPTY_BUT_RECENT_CONTROL_AVAILABLE" if controls_nonempty else
                   "2020_EMPTY_AND_RECENT_CONTROL_UNAVAILABLE_OR_EMPTY"),
        "release_approved": False,
        "warning": "HTTP 200 is not evidence of historical data. BGP and ping samples require source-name, timestamp, baseline and coverage audits before publication.",
        "cases": cases,
    }
    (out / "availability_report.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"status": result["status"], "results": [
        {"case": x["case"], "classification": x["classification"], "points": x["numeric_points"]} for x in cases]}, indent=2))
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="_artifacts/ioda_diagnostic")
    ap.add_argument("--timeout", type=float, default=25)
    args = ap.parse_args()
    run(Path(args.out), args.timeout)
