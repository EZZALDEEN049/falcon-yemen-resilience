#!/usr/bin/env python3
"""Reconstruct historical origin-AS route state using CAIDA BGPStream's bgpreader.

Design principles:
- Uses RIPE RIS collectors through the BGPStream broker (multiple collectors/peers).
- Uses official origin-AS filtering (-a) instead of downloading the full global table.
- For each checkpoint, seeds from the preceding 00/08/16 UTC RIS RIB and applies
  announcements/withdrawals up to the checkpoint.
- Computes metrics only on comparable collector-peer vantage points.
- Fails closed on empty states; an empty retrieval is never interpreted as an outage.

Requires bgpreader from CAIDA BGPStream on PATH.
"""
from __future__ import annotations
import argparse, csv, datetime as dt, json, math, random, shutil, statistics, subprocess, sys
from collections import defaultdict
from pathlib import Path

DEFAULT_PLAN = Path(__file__).resolve().parent.parent / "data" / "historical_checkpoint_plan.csv"

def parse_utc(s): return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
def epoch(x): return int(x.timestamp())
def seed_rib_time(t):
    h=max(h for h in (0,8,16) if h <= t.hour)
    return t.replace(hour=h, minute=0, second=0, microsecond=0)

def clean_path(s):
    toks=[]
    for x in str(s).split():
        if x.startswith("{"): continue
        if x.isdigit() and (not toks or toks[-1] != x): toks.append(x)
    return toks

def upstream(path, origin):
    p=clean_path(path); o=str(origin)
    while len(p)>=2 and p[-1]==o and p[-2]==o: p.pop()
    if not p or p[-1] != o: return None
    return p[-2] if len(p)>=2 else None

def run_reader(asn, t):
    start=seed_rib_time(t)
    # interval remains <8h for RIS, so one seed RIB plus subsequent updates is sufficient.
    cmd=["bgpreader","-p","ris","-w",f"{epoch(start)},{epoch(t)}","-t","ribs","-t","updates","-a",str(asn)]
    proc=subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0: raise RuntimeError(proc.stderr[-4000:])
    state={}
    n_rib=n_a=n_w=0
    for line in proc.stdout.splitlines():
        parts=line.split("|")
        if len(parts) < 14: continue
        dump, elem=parts[0],parts[1]
        if elem not in {"R","A","W"}: continue
        collector=parts[4]; peer=parts[7]; prefix=parts[9]
        if not collector or not peer or not prefix: continue
        key=(collector,peer,prefix)
        if elem=="W":
            state.pop(key,None); n_w+=1; continue
        aspath=parts[11]; origin=parts[12]
        # Defend against filter/parser anomalies.
        if str(origin) != str(asn): continue
        state[key]={"collector":collector,"peer":peer,"prefix":prefix,"as_path":aspath,
                    "origin":origin,"timestamp":float(parts[2]),"immediate_upstream":upstream(aspath,asn)}
        if elem=="R": n_rib+=1
        else: n_a+=1
    if not state: raise RuntimeError(f"Empty reconstructed state for AS{asn} at {t.isoformat()}; refuse outage interpretation")
    return start,state,{"n_rib_elems":n_rib,"n_announcements":n_a,"n_withdrawals":n_w,"command":" ".join(cmd)}

def vantage_sets(state):
    d=defaultdict(dict)
    for (c,p,pfx),r in state.items(): d[(c,p)][pfx]=r
    return d

def percentile(xs,q):
    if not xs: return None
    ys=sorted(xs); pos=(len(ys)-1)*q; lo=int(pos); hi=min(lo+1,len(ys)-1); frac=pos-lo
    return ys[lo]*(1-frac)+ys[hi]*frac

def bootstrap_ci(vals, reps=2000, seed=1):
    if not vals: return None,None
    rng=random.Random(seed); n=len(vals); means=[]
    for _ in range(reps): means.append(sum(vals[rng.randrange(n)] for _ in range(n))/n)
    return percentile(means,.025),percentile(means,.975)

def compare(pre, cur):
    A,B=vantage_sets(pre),vantage_sets(cur); comp=sorted(set(A)&set(B))
    if not comp: raise RuntimeError("No comparable collector-peer vantages")
    pvr=[]; route_base=route_keep=route_common=route_changed_upstream=0; path_deltas=[]
    upstream_pre=set(); upstream_cur=set(); diversity_pre=[]; diversity_cur=[]
    for v in comp:
        pa,pb=A[v],B[v]; sa,sb=set(pa),set(pb)
        if not sa: continue
        pvr.append(len(sa&sb)/len(sa)); route_base += len(sa); route_keep += len(sa&sb)
        diversity_pre.append(len({pa[p]["as_path"] for p in sa})); diversity_cur.append(len({pb[p]["as_path"] for p in sb}))
        for pfx in sa&sb:
            ra,rb=pa[pfx],pb[pfx]; route_common+=1
            ua,ub=ra.get("immediate_upstream"),rb.get("immediate_upstream")
            if ua: upstream_pre.add(ua)
            if ub: upstream_cur.add(ub)
            if ua != ub: route_changed_upstream += 1
            la,lb=len(clean_path(ra["as_path"])),len(clean_path(rb["as_path"]))
            if la and lb: path_deltas.append(lb-la)
    lo,hi=bootstrap_ci(pvr)
    union=upstream_pre|upstream_cur; jaccard_churn=(1-len(upstream_pre&upstream_cur)/len(union)) if union else None
    return {
      "n_comparable_vantages":len(comp), "PVR_mean":statistics.mean(pvr), "PVR_median":statistics.median(pvr),
      "PVR_bootstrap95_low":lo,"PVR_bootstrap95_high":hi,
      "ROR":route_keep/route_base if route_base else None,
      "USF":route_changed_upstream/route_common if route_common else None,
      "provider_set_churn_jaccard":jaccard_churn,
      "upstreams_pre":";".join(sorted(upstream_pre,key=lambda x:int(x))),"upstreams_current":";".join(sorted(upstream_cur,key=lambda x:int(x))),
      "AS_path_inflation_median_hops":statistics.median(path_deltas) if path_deltas else None,
      "path_diversity_pre_mean":statistics.mean(diversity_pre) if diversity_pre else None,
      "path_diversity_current_mean":statistics.mean(diversity_cur) if diversity_cur else None,
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--plan",default=str(DEFAULT_PLAN)); ap.add_argument("--out",default="../raw_bgp")
    args=ap.parse_args()
    if not shutil.which("bgpreader"): raise SystemExit("bgpreader not found. Install CAIDA BGPStream first; no fallback values will be generated.")
    out=Path(args.out).resolve(); out.mkdir(parents=True,exist_ok=True)
    rows=list(csv.DictReader(open(args.plan,encoding="utf-8-sig")))
    states={}; metadata=[]
    for r in rows:
        k=(r["event_id"],r["asn"],r["label"]); t=parse_utc(r["timestamp"])
        seed,state,meta=run_reader(r["asn"],t); states[k]=state
        sf=out/f'{r["event_id"]}_AS{r["asn"]}_{r["label"]}.json'
        sf.write_text(json.dumps({"event":r["event_id"],"asn":r["asn"],"label":r["label"],"checkpoint":r["timestamp"],
                                  "seed_rib_utc":seed.isoformat(),"retrieval":meta,"routes":list(state.values())},indent=2),encoding="utf-8")
        metadata.append({**r,"seed_rib_utc":seed.isoformat(),"n_routes":len(state),**meta,"file":sf.name})
    # Compare every non-PRE checkpoint to event/ASN PRE.
    metrics=[]
    for r in rows:
        if r["label"]=="PRE": continue
        base_key=(r["event_id"],r["asn"],"PRE")
        cur_key=(r["event_id"],r["asn"],r["label"])
        if base_key not in states: continue
        metrics.append({"event_id":r["event_id"],"asn":r["asn"],"comparison":f'PRE->{r["label"]}',**compare(states[base_key],states[cur_key])})
    with (out/"retrieval_manifest.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=metadata[0].keys()); w.writeheader(); w.writerows(metadata)
    with (out/"historical_bgp_metrics.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=metrics[0].keys()); w.writeheader(); w.writerows(metrics)
    print(json.dumps({"checkpoints":len(metadata),"comparisons":len(metrics),"out":str(out)},indent=2))

if __name__=="__main__": main()
