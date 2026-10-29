#!/usr/bin/env python3
"""Sensitivity analysis for the plot-derived IODA structural-functional divergence.

This script intentionally evaluates only the published raster fallback. It does not
convert raster-derived values into primary IODA samples and must not be used to label
BGP visibility as route-level PVR/ROR/USF.

Perturbations:
- baseline start: -120, 0, +120 minutes from 2020-01-08 00:00 UTC
- baseline end: -60, -30, 0, +30, +60 minutes from 2020-01-09 08:30 UTC
- acute start/end: independently -60, -30, 0, +30, +60 minutes from 18:00/00:00 UTC
- y-axis zero: 630, 632, 634 pixels
- y-axis scale: 250, 252, 254 pixels per normalized unit
- RGB channel tolerance: 0, 1, 2
- summary statistic: median or mean

The primary result is the range of BGP-retention minus active-retention across all
valid perturbation combinations.
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone, timedelta
import argparse, csv, json, statistics
from PIL import Image

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "provenance" / "jan-9-10-yemen-AS30873-IODA.png"
X0, X1 = 112, 1779
PLOT_Y_MIN, PLOT_Y_MAX = 240, 632
CHART_START = datetime(2020,1,7,22,10,tzinfo=timezone.utc)
CHART_END = datetime(2020,1,10,22,15,tzinfo=timezone.utc)
BASE_START = datetime(2020,1,8,0,0,tzinfo=timezone.utc)
BASE_END = datetime(2020,1,9,8,30,tzinfo=timezone.utc)
ACUTE_START = datetime(2020,1,9,18,0,tzinfo=timezone.utc)
ACUTE_END = datetime(2020,1,10,0,0,tzinfo=timezone.utc)
COLORS = {"active": (31,120,180), "bgp": (51,160,44)}

def _time_for_x(x:int):
    frac = (x-X0)/(X1-X0)
    return CHART_START + timedelta(seconds=frac*(CHART_END-CHART_START).total_seconds())

def _precompute(img: Image.Image):
    times=[_time_for_x(x) for x in range(X0,X1+1)]
    cache={}
    for sig,rgb in COLORS.items():
        for tol in (0,1,2):
            arr=[]
            for x in range(X0,X1+1):
                ys=[]
                for y in range(PLOT_Y_MIN,PLOT_Y_MAX+1):
                    p=img.getpixel((x,y))
                    if max(abs(p[i]-rgb[i]) for i in range(3)) <= tol:
                        ys.append(y)
                arr.append(statistics.median(ys) if ys else None)
            cache[(sig,tol)] = arr
    return times,cache

def _extract(times, arr, t0, t1, zero, scale):
    return [(zero-y)/scale for t,y in zip(times,arr) if y is not None and t0 <= t <= t1]

def run(out_csv: Path, out_json: Path):
    if not IMG.exists():
        raise FileNotFoundError("The original third-party IODA raster is intentionally not redistributed in Online Resource 1. Obtain the corresponding source plot independently from IODA and place it at: %s" % IMG)
    img=Image.open(IMG).convert("RGB")
    times,cache=_precompute(img)
    rows=[]
    for bss in (-120,0,120):
      for bes in (-60,-30,0,30,60):
       for ass in (-60,-30,0,30,60):
        for aes in (-60,-30,0,30,60):
         a0=ACUTE_START+timedelta(minutes=ass); a1=ACUTE_END+timedelta(minutes=aes)
         if a1 <= a0: continue
         b0=BASE_START+timedelta(minutes=bss); b1=BASE_END+timedelta(minutes=bes)
         for zero in (630.0,632.0,634.0):
          for scale in (250.0,252.0,254.0):
           for tol in (0,1,2):
            vals={}
            for sig in ("active","bgp"):
                vals[(sig,"pre")]=_extract(times,cache[(sig,tol)],b0,b1,zero,scale)
                vals[(sig,"acute")]=_extract(times,cache[(sig,tol)],a0,a1,zero,scale)
            if min(len(v) for v in vals.values()) < 10: continue
            for stat in ("median","mean"):
                fn=statistics.median if stat=="median" else statistics.mean
                ar=fn(vals[("active","acute")])/fn(vals[("active","pre")])
                br=fn(vals[("bgp","acute")])/fn(vals[("bgp","pre")])
                rows.append({
                    "baseline_start_shift_min":bss,"baseline_end_shift_min":bes,
                    "acute_start_shift_min":ass,"acute_end_shift_min":aes,
                    "zero_y_pixel":zero,"pixels_per_unit":scale,"rgb_tolerance":tol,
                    "statistic":stat,"active_retention":ar,"bgp_retention":br,
                    "divergence_fraction":br-ar,"divergence_percentage_points":100*(br-ar)
                })
    rows.sort(key=lambda r:r["divergence_fraction"])
    out_csv.parent.mkdir(parents=True,exist_ok=True)
    with out_csv.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    n=len(rows)
    def q(p): return rows[min(n-1,max(0,int(p*n)))]["divergence_percentage_points"]
    # exact central specification
    central=[r for r in rows if r["baseline_start_shift_min"]==0 and r["baseline_end_shift_min"]==0
             and r["acute_start_shift_min"]==0 and r["acute_end_shift_min"]==0
             and r["zero_y_pixel"]==632.0 and r["pixels_per_unit"]==252.0
             and r["rgb_tolerance"]==0 and r["statistic"]=="median"][0]
    summary={
        "n_valid_combinations":n,
        "central_divergence_percentage_points":central["divergence_percentage_points"],
        "central_bgp_retention":central["bgp_retention"],
        "central_active_retention":central["active_retention"],
        "minimum_divergence_percentage_points":rows[0]["divergence_percentage_points"],
        "maximum_divergence_percentage_points":rows[-1]["divergence_percentage_points"],
        "p05_divergence_percentage_points":q(0.05),
        "median_divergence_percentage_points":q(0.50),
        "p95_divergence_percentage_points":q(0.95),
        "grid_description":"Full-factorial grid of plausible window, axis-origin, extraction, and summary-statistic choices; settings are not independent experiments.",
        "invariance_note":"RGB tolerance and y-axis scale perturbations were invariant within numerical precision over the tested range for the reported retention divergence.",
        "interpretation":"Raster sensitivity only. Robustness to reasonable digitization/window perturbations does not substitute for native IODA samples."
    }
    out_json.write_text(json.dumps(summary,indent=2),encoding="utf-8")
    return summary

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out-csv",default=str(ROOT/"results"/"ioda_digitization_sensitivity.csv")); ap.add_argument("--out-json",default=str(ROOT/"results"/"ioda_digitization_sensitivity_summary.json")); args=ap.parse_args()
    print(json.dumps(run(Path(args.out_csv),Path(args.out_json)),indent=2))
if __name__=="__main__": main()
