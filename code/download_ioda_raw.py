#!/usr/bin/env python3
"""Acquire raw IODA time-series for the Yemen event study.

This script is deliberately fail-closed: an HTTP success with no recognized time-series
points is treated as a failure and is never converted into a scientific result.

Expected official API pattern (IODA v2):
  /v2/signals/raw/{entityType}/{entityCode}?from=<unix>&until=<unix>

The parser is intentionally tolerant of envelope/schema variations: it recursively
locates series-like objects containing numeric values plus a start time and step, or
explicit timestamp/value pairs. Raw JSON is always preserved before parsing.
"""
from __future__ import annotations
import argparse, csv, datetime as dt, json, math, os, sys, time
from pathlib import Path
from typing import Any, Iterable
try:
    import requests
except Exception as e:
    raise SystemExit("requests is required: pip install requests") from e

API_BASE = "https://api.ioda.inetintel.cc.gatech.edu/v2"
EVENTS = {
    "FALCON_2020": ("2020-01-08T00:00:00Z", "2020-01-12T00:00:00Z"),
    "YEMEN_2022":  ("2022-01-20T00:00:00Z", "2022-01-26T12:00:00Z"),
    "FALCON_2023": ("2023-11-09T00:00:00Z", "2023-11-11T12:00:00Z"),
}
ENTITIES = [("asn", "30873"), ("asn", "12486"), ("asn", "204317"), ("country", "YE")]

def epoch(s: str) -> int:
    return int(dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp())

def finite_number(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))

def walk(obj: Any, path=()):
    if isinstance(obj, dict):
        yield path, obj
        for k, v in obj.items():
            yield from walk(v, path + (str(k),))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, path + (str(i),))

def flatten_series(payload: Any) -> list[dict[str, Any]]:
    """Extract time-series points without assuming one exact IODA envelope."""
    out: list[dict[str, Any]] = []
    seen = set()
    for path, d in walk(payload):
        # Explicit point arrays: [{timestamp/time/ts:..., value:...}, ...]
        if any(k in d for k in ("timestamp", "time", "ts")) and any(k in d for k in ("value", "val", "y")):
            tk = next((k for k in ("timestamp", "time", "ts") if k in d), None)
            vk = next((k for k in ("value", "val", "y") if k in d), None)
            if tk and vk and finite_number(d[vk]):
                t = d[tk]
                if isinstance(t, str):
                    try: t = epoch(t)
                    except Exception: continue
                if finite_number(t):
                    label = str(d.get("datasource") or d.get("signal") or d.get("name") or "/".join(path[:-1]) or "unknown")
                    key = (label, int(float(t)), float(d[vk]))
                    if key not in seen:
                        seen.add(key); out.append({"signal": label, "timestamp": int(float(t)), "value": float(d[vk])})
        # Compact series: {from/start: epoch, step: sec, values:[...]}
        vals = d.get("values")
        if isinstance(vals, list) and vals and sum(finite_number(v) for v in vals) > 0:
            start = d.get("from", d.get("start", d.get("start_time", d.get("timestamp"))))
            step = d.get("step", d.get("interval", d.get("sampling_interval")))
            if isinstance(start, str):
                try: start = epoch(start)
                except Exception: start = None
            if finite_number(start) and finite_number(step) and float(step) > 0:
                label = str(d.get("datasource") or d.get("signal") or d.get("name") or "/".join(path) or "unknown")
                for i, v in enumerate(vals):
                    if not finite_number(v): continue
                    t = int(float(start) + i * float(step))
                    key = (label, t, float(v))
                    if key not in seen:
                        seen.add(key); out.append({"signal": label, "timestamp": t, "value": float(v)})
    out.sort(key=lambda r: (r["signal"], r["timestamp"]))
    return out

def fetch(session: requests.Session, entity_type: str, entity_code: str, start: int, end: int, timeout=60):
    url = f"{API_BASE}/signals/raw/{entity_type}/{entity_code}"
    r = session.get(url, params={"from": start, "until": end}, timeout=timeout)
    r.raise_for_status()
    return r.url, r.json()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="../raw_ioda")
    ap.add_argument("--event", choices=list(EVENTS)+["ALL"], default="ALL")
    args = ap.parse_args()
    out = Path(args.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    events = EVENTS.items() if args.event == "ALL" else [(args.event, EVENTS[args.event])]
    sess = requests.Session(); sess.headers.update({"User-Agent": "Yemen-FALCON-resilience-research/1.0"})
    manifest=[]; failures=[]
    for event, (s0, s1) in events:
        for et, ec in ENTITIES:
            stem=f"{event}_{et}_{ec}"
            try:
                final_url, payload = fetch(sess, et, ec, epoch(s0), epoch(s1))
                raw_path=out/f"{stem}.json"; raw_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
                points=flatten_series(payload)
                if not points:
                    raise RuntimeError("HTTP response contained no recognized numeric time-series points")
                csv_path=out/f"{stem}.csv"
                with csv_path.open("w", newline="", encoding="utf-8") as f:
                    w=csv.DictWriter(f, fieldnames=["signal","timestamp","utc","value"]); w.writeheader()
                    for p in points:
                        w.writerow({**p, "utc": dt.datetime.fromtimestamp(p["timestamp"], dt.timezone.utc).isoformat()})
                manifest.append({"event":event,"entity_type":et,"entity_code":ec,"request_url":final_url,
                                 "start":s0,"end":s1,"n_points":len(points),"raw_json":raw_path.name,"csv":csv_path.name})
            except Exception as e:
                failures.append({"event":event,"entity_type":et,"entity_code":ec,"error":repr(e)})
    (out/"manifest.json").write_text(json.dumps({"successes":manifest,"failures":failures}, indent=2), encoding="utf-8")
    print(json.dumps({"successes":len(manifest),"failures":len(failures),"out":str(out)}, indent=2))
    if not manifest:
        raise SystemExit(2)

if __name__ == "__main__":
    main()
