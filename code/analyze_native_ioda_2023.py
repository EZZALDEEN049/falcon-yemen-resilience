#!/usr/bin/env python3
"""Recalculate descriptive retention in the 2023 FALCON maintenance window from native IODA JSON.

Source input: unchanged official IODA raw envelope, manually archived as GitHub
Actions artifact. This script does not assert cable-route causality, and never
substitutes 2023 signals for unavailable January 2020 native samples.
"""
import argparse
import datetime as dt
import json
import math
import statistics
from pathlib import Path

UTC = dt.timezone.utc
BASE_START = dt.datetime(2023, 11, 9, 0, 0, tzinfo=UTC).timestamp()
BASE_END = dt.datetime(2023, 11, 10, 0, 0, tzinfo=UTC).timestamp()
EVENT_START = dt.datetime(2023, 11, 10, 0, 10, tzinfo=UTC).timestamp()
EVENT_END = dt.datetime(2023, 11, 10, 4, 45, tzinfo=UTC).timestamp()
POST_START = dt.datetime(2023, 11, 10, 5, 0, tzinfo=UTC).timestamp()
POST_END = dt.datetime(2023, 11, 11, 0, 0, tzinfo=UTC).timestamp()
TARGETS = ("bgp", "ping-slash24")


def extract(payload):
    if not isinstance(payload, dict) or payload.get("error"):
        raise ValueError("Invalid/error IODA response")
    data = payload.get("data")
    if not isinstance(data, list):
        raise ValueError("No data envelope")
    records = [item for group in data if isinstance(group, list) for item in group if isinstance(item, dict)]
    out = {}
    for sig in TARGETS:
        matches = [item for item in records if item.get("datasource") == sig
                   and item.get("entityType") == "asn" and str(item.get("entityCode")) == "30873"]
        if len(matches) != 1:
            raise ValueError("Expected exactly one native IODA series for " + sig)
        item = matches[0]
        step = item.get("step")
        start = item.get("from")
        values = item.get("values")
        if not isinstance(start, int) or not isinstance(step, int) or step <= 0 or not isinstance(values, list):
            raise ValueError("Invalid native series schema")
        points = [(start + i*step,float(v)) for i,v in enumerate(values)
                  if isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(float(v))]
        out[sig] = (step,points)
    return out


def window(points, step, start, end):
    vals = [v for t,v in points if start <= t < end]
    expected = math.ceil((end-start)/step)
    if len(vals) < .95*expected:
        raise ValueError(f"Missing data in requested window: {len(vals)}/{expected}")
    return {"n":len(vals),"expected":expected, "median":statistics.median(vals),
            "mean":statistics.mean(vals),"minimum":min(vals),"maximum":max(vals)}


def analyze(payload):
    series = extract(payload)
    metrics = {}
    for sig,(step,points) in series.items():
        baseline=window(points,step,BASE_START,BASE_END)
        event=window(points,step,EVENT_START,EVENT_END)
        post=window(points,step,POST_START,POST_END)
        if baseline["median"] <= 0:
            raise ValueError("Nonpositive baseline")
        metrics[sig] = {"cadence_seconds":step,"baseline":baseline,"disruption":event,"post":post,
                        "median_retention_pct":100*event["median"]/baseline["median"]}
    return {"event":"FALCON_MAINTENANCE_2023","entity":"AS30873",
            "source":"IODA_HTTP_API_UNMODIFIED_JSON",
            "measurement_status":"NATIVE_SIGNAL_DESCRIPTIVE_ONLY",
            "time_windows_utc":{"baseline":["2023-11-09T00:00:00Z","2023-11-10T00:00:00Z"],
                  "disruption":["2023-11-10T00:10:00Z","2023-11-10T04:45:00Z"],
                  "post":["2023-11-10T05:00:00Z","2023-11-11T00:00:00Z"]},
            "metrics":metrics,"scope_warning":"Separate IODA signal families; no claim of user traffic percentages, cable causality or transfer to 2020."}


if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--raw",required=True,help="Official IODA JSON archive of AS30873 Nov 9-11 2023")
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    report=analyze(json.loads(Path(args.raw).read_text(encoding="utf-8")))
    target=Path(args.out); target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
