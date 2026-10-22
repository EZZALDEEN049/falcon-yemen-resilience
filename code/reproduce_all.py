#!/usr/bin/env python3
"""Reproduce all quantitative results supportable from files redistributed in Online Resource 1.

This CLEAN submission package does not redistribute the original third-party IODA plot
images. Therefore:
- current origin-concentration HHI values and Figure 2 are recalculated from the frozen
  prefix-level snapshot;
- the central IODA retention/divergence and Figure 3 are recalculated from the included
  digitized-signal table;
- sensitivity bounds/quantiles are independently recalculated from the complete included
  sensitivity-result table generated during the authors' raster audit.

The package does not manufacture raw IODA or historical BGP results.
"""
from __future__ import annotations
import argparse,csv,json,statistics
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent.parent

def read_csv(p):
    with open(p,encoding="utf-8-sig") as f:return list(csv.DictReader(f))

def write_csv(p,rows):
    with open(p,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)

def reproduce_origin():
    from ipaddress import ip_network, collapse_addresses
    rows=read_csv(ROOT/"data"/"bgp_origin_snapshot_2026-08-09.csv")
    by={}
    for r in rows: by.setdefault(r["origin_asn"],[]).append(ip_network(r["prefix"]))
    summary=[]; total_prefixes=sum(len(v) for v in by.values())
    union24={asn:sum(n.num_addresses/256 for n in collapse_addresses(nets)) for asn,nets in by.items()}
    total24=sum(union24.values())
    for asn in ("AS30873","AS12486","AS204317"):
        summary.append({"origin_asn":asn,"prefix_count":len(by[asn]),"prefix_share":len(by[asn])/total_prefixes,
                        "unique_24_equivalent":union24[asn],"address_space_share":union24[asn]/total24})
    prefix_hhi=sum(float(r["prefix_share"])**2 for r in summary)
    space_hhi=sum(float(r["address_space_share"])**2 for r in summary)
    out={"prefix_hhi":prefix_hhi,"address_space_hhi":space_hhi,"n_prefixes":total_prefixes,
         "unique_24_equivalent_total":total24,
         "scope":"frozen present-day assembled snapshot dated 2026-08-09 only; not a 2020 reconstruction"}
    (ROOT/"results"/"origin_concentration_reproduced.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    write_csv(ROOT/"data"/"current_origin_concentration_summary.csv",summary)
    labels=[r["origin_asn"] for r in summary]; prefix=[100*float(r["prefix_share"]) for r in summary]; space=[100*float(r["address_space_share"]) for r in summary]
    x=range(len(labels)); width=.36
    fig,ax=plt.subplots(figsize=(9,5.3))
    ax.bar([i-width/2 for i in x],prefix,width,label="IPv4 prefix share",facecolor="white",edgecolor="black",hatch="///",linewidth=1)
    ax.bar([i+width/2 for i in x],space,width,label="Unique /24-equivalent address-space share",facecolor="0.75",edgecolor="black",hatch="...",linewidth=1)
    ax.set_xticks(list(x),labels); ax.set_ylabel("Share of frozen current baseline (%)"); ax.legend(); fig.tight_layout()
    fig.savefig(ROOT/"figures"/"Figure2_origin_concentration.png",dpi=600); plt.close(fig)
    return out

def summarize_saved_sensitivity():
    rows=read_csv(ROOT/"results"/"ioda_digitization_sensitivity.csv")
    vals=sorted(float(r["divergence_percentage_points"]) for r in rows)
    n=len(vals)
    def q(p): return vals[min(n-1,max(0,int(p*n)))]
    central=None
    for r in rows:
        if (r["baseline_start_shift_min"]=="0" and r["baseline_end_shift_min"]=="0" and
            r["acute_start_shift_min"]=="0" and r["acute_end_shift_min"]=="0" and
            float(r["zero_y_pixel"])==632.0 and float(r["pixels_per_unit"])==252.0 and
            r["rgb_tolerance"]=="0" and r["statistic"]=="median"):
            central=r; break
    if central is None: raise RuntimeError("Central sensitivity specification not found")
    summary={
        "n_valid_combinations":n,
        "central_divergence_percentage_points":float(central["divergence_percentage_points"]),
        "central_bgp_retention":float(central["bgp_retention"]),
        "central_active_retention":float(central["active_retention"]),
        "minimum_divergence_percentage_points":vals[0],
        "maximum_divergence_percentage_points":vals[-1],
        "p05_divergence_percentage_points":q(0.05),
        "median_divergence_percentage_points":q(0.50),
        "p95_divergence_percentage_points":q(0.95),
        "grid_description":"Summary recomputed from the complete sensitivity-result table included in Online Resource 1; the original third-party IODA raster is not redistributed.",
        "interpretation":"Sensitivity-summary reproduction only; this does not substitute for native IODA samples or a fresh pixel-level extraction from the source raster."
    }
    (ROOT/"results"/"ioda_digitization_sensitivity_summary_reproduced.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    return summary

def reproduce_ioda():
    src=read_csv(ROOT/"data"/"stage9_ioda_digitized_signal_validation_v0_1.csv")
    by={(r["asn"],r["window"],r["signal"]):r for r in src}
    rows=[]
    for asn in ("AS30873","AS12486"):
        for sig in ("bgp","active"):
            pre=float(by[(asn,"pre_event_baseline",sig)]["median_normalized"])
            acute=float(by[(asn,"acute_event",sig)]["median_normalized"])
            rows.append({"asn":asn,"signal":sig,"pre_median":pre,"acute_median":acute,
                         "acute_to_pre_retention":acute/pre,"relative_loss":1-acute/pre,
                         "evidence_class":"PLOT_DERIVED_FALLBACK"})
    write_csv(ROOT/"results"/"reproduced_plot_proxy_retention.csv",rows)
    a={r["signal"]:r for r in rows if r["asn"]=="AS30873"}
    divergence=100*(a["bgp"]["acute_to_pre_retention"]-a["active"]["acute_to_pre_retention"])
    sens=summarize_saved_sensitivity()
    labels=["AS30873","AS12486"]
    bgp=[100*next(r["acute_to_pre_retention"] for r in rows if r["asn"]==a0 and r["signal"]=="bgp") for a0 in labels]
    active=[100*next(r["acute_to_pre_retention"] for r in rows if r["asn"]==a0 and r["signal"]=="active") for a0 in labels]
    x=range(len(labels)); width=.34
    fig,ax=plt.subplots(figsize=(9.4,5.3))
    ax.bar([i-width/2 for i in x],bgp,width,label="BGP visibility proxy",facecolor="white",edgecolor="black",hatch="///",linewidth=1)
    ax.bar([i+width/2 for i in x],active,width,label="Active-probing proxy",facecolor="0.75",edgecolor="black",hatch="...",linewidth=1)
    ax.axhline(100,linestyle="--",linewidth=1); ax.set_xticks(list(x),labels)
    ax.set_ylabel("Acute-window median / pre-event median (%)"); ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=2, frameon=False); fig.tight_layout()
    fig.savefig(ROOT/"figures"/"Figure3_ioda_structural_functional_proxy.png",dpi=600); plt.close(fig)
    return {"central_divergence_percentage_points":divergence,"sensitivity":sens}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--raw-ioda"); ap.add_argument("--raw-bgp"); args=ap.parse_args()
    origin=reproduce_origin(); ioda=reproduce_ioda()
    from phase_audit import compute as phase_compute
    phase_audit=phase_compute()
    status={"origin_concentration":origin,"ioda_plot_proxy":ioda,
            "phase_audit":phase_audit,
            "raw_ioda_present":bool(args.raw_ioda and Path(args.raw_ioda).exists()),
            "raw_bgp_present":bool(args.raw_bgp and Path(args.raw_bgp).exists()),
            "third_party_source_images_redistributed":False,
            "interpretation":"Local reproduction from redistributed derived evidence only. Distinct IODA signal families are not relabeled as route-level PVR/ROR/USF."}
    (ROOT/"results"/"reproduced_summary.json").write_text(json.dumps(status,indent=2),encoding="utf-8")
    print(json.dumps(status,indent=2))
if __name__=="__main__": main()
