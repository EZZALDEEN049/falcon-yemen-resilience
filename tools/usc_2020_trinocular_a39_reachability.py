#!/usr/bin/env python3
"""Analyze **authorized** USC ANT/Trinocular a39 2020 source files.

USC a39all is a post-processed, multi-vantage integrated active-outage estimate,
NOT raw IODA ping-slash24 observations. The USC a39_supplement Jan-2020
block_to_as file supplies event-period AS labels. No online data is downloaded.
Fail closed on missing input/FSDB schema. Unknown and uncertainty are not down.

Official format: https://ant.isi.edu/datasets/outage/format.html
Dataset catalog: https://ant.isi.edu/datasets/all.html
"""
import argparse,bisect,bz2,collections,datetime as dt,gzip,hashlib,ipaddress,json,lzma,re,sys
from pathlib import Path
TARG={30873,12486}
UTC=dt.timezone.utc

def ep(t):
    return int(dt.datetime.fromisoformat(t.replace("Z","+00:00")).timestamp())

def opener(p):
    name=str(p)
    return (bz2.open if name.endswith(".bz2") else
            lzma.open if name.endswith(".xz") else
            gzip.open if name.endswith(".gz") else open)(p,"rt",encoding="utf-8",errors="strict")

def file_sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(4*1024*1024),b""):h.update(chunk)
    return h.hexdigest()

def fsdb(path,required):
    """Read exact FSDB header, stream rows. Do not infer undocumented columns."""
    got_header=False
    with opener(path) as f:
        for lineno,raw in enumerate(f,1):
            line=raw.strip()
            if not line:continue
            if line.startswith("#fsdb"):
                tokens=line.split()
                if "t" not in tokens:raise ValueError(f"{path}:{lineno}: unsupported FSDB delimiter")
                cols=tokens[tokens.index("t")+1:]
                if not set(required).issubset(cols):raise ValueError(f"{path}:{lineno}: expected {required}, found {cols}")
                got_header=True
                continue
            if line.startswith("#"):continue
            if not got_header:raise ValueError(f"{path}:{lineno}: no FSDB schema before data")
            parts=line.split(None,len(cols)-1)
            if len(parts)!=len(cols):raise ValueError(f"{path}:{lineno}: wrong number of columns")
            yield dict(zip(cols,parts))
    if not got_header:raise ValueError(f"{path}: no FSDB header")

def norm_block(value):
    if not re.fullmatch(r"[a-fA-F0-9]{8}",value):
        raise ValueError(f"invalid /24 hex block {value!r}")
    if int(value,16) & 255:raise ValueError(f"not a canonical /24 base {value}")
    return value.lower()

def norm_asn(value):
    """Accept one unambiguous origin AS only; multi-AS mappings excluded."""
    token=value.strip()
    if re.fullmatch(r"(?:AS)?\d+",token,re.IGNORECASE):
        return int(re.sub(r"^AS","",token,flags=re.I))
    return None

def mapped_as(path):
    candidates=collections.defaultdict(set)
    counts=collections.Counter()
    for row in fsdb(path,{"block","AS"}):
        block=norm_block(row["block"]);n=norm_asn(row["AS"])
        counts["mapping_rows"]+=1
        if n is None:
            candidates[block].add(None)
            counts["mapping_ambiguous_as"]+=1
        else:candidates[block].add(n)
    by_as={a:set() for a in TARG}
    unresolved=0
    for block,v in candidates.items():
        if len(v)!=1 or None in v:
            unresolved+=1
            continue
        asn=next(iter(v))
        if asn in TARG:by_as[asn].add(block)
    counts["ambiguous_block_mappings"]=unresolved
    return by_as,dict(counts)

def load_intervals(path,selected):
    allset=set.union(*selected.values())
    info=collections.Counter()
    ev=collections.defaultdict(list)
    for row in fsdb(path,{"block","start","duration","uncertainty","downup"}):
        info["source_outagedownup_rows"]+=1
        block=norm_block(row["block"])
        if block not in allset:continue
        start=int(row["start"]);duration=int(row["duration"])
        uncertainty=int(row["uncertainty"]);status=int(row["downup"])
        if duration<=0 or uncertainty<0 or status not in (-2,-1,0,1):
            raise ValueError(f"unexpected Trinocular outage state: {row}")
        ev[block].append((start,start+duration,uncertainty,status))
        info["target_outagedownup_rows"]+=1
    for block,rows in ev.items():rows.sort()
    return ev,dict(info)

def one_status(intervals,t):
    """Return one of up/down/unmeasurable/gone_dark/uncertain/no_data.

    Conservative exclusion of edge timestamps near documented start uncertainty.
    Uncertainty on an endpoint is treated symmetrically, not resolved by guess.
    """
    if not intervals:return "no_data"
    active=[r for r in intervals if r[0]<=t<r[1]]
    if not active:return "no_data"
    if len(active)>1:return "uncertain"
    start,end,unc,state=active[0]
    if unc>0 and (t-start<=unc or end-t<=unc):return "uncertain"
    return {1:"up",0:"down",-1:"unmeasurable",-2:"gone_dark"}[state]

def analyze(downup_path,map_path,start,end,step_minutes=15,pre_t=None):
    if step_minutes<5 or step_minutes>1440 or 60%step_minutes:
        raise ValueError("Use step minutes in 5,10,15,20,30,60")
    if not (start<end):raise ValueError("invalid analysis range")
    by_as,mapping_audit=mapped_as(map_path)
    if any(len(x)==0 for x in by_as.values()):
        raise ValueError("At least one target ASN lacks /24 blocks in source 2020 AS mapping")
    intervals,scan_audit=load_intervals(downup_path,by_as)
    checkpoints=list(range(start,end,step_minutes*60))
    if pre_t is None:pre_t=ep("2020-01-09T08:00:00Z")
    if pre_t not in checkpoints:raise ValueError("baseline UTC timestamp must lie on checkpoint grid")
    baseline={
        a:{b for b in blocks if one_status(intervals.get(b,[]),pre_t)=="up"}
        for a,blocks in by_as.items()
    }
    if any(len(s)==0 for s in baseline.values()):
        raise ValueError("At least one target ASN has zero pre-event measured-up baseline; refusing ratios")
    series=[]
    for t in checkpoints:
        row={"timestamp_utc":dt.datetime.fromtimestamp(t,UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),"asns":{}}
        for asn,blocks in sorted(by_as.items()):
            status=collections.Counter({k:0 for k in ("up","down","unmeasurable","gone_dark","uncertain","no_data")})
            active=collections.Counter()
            for b in blocks:
                val=one_status(intervals.get(b,[]),t)
                status[val]+=1
                if b in baseline[asn]:active[val]+=1
            known=status["up"]+status["down"]
            survival=active["up"]/len(baseline[asn])
            upper=(active["up"]+active["uncertain"]+active["no_data"]+active["unmeasurable"]+active["gone_dark"])/len(baseline[asn])
            if sum(status.values())!=len(blocks):raise AssertionError("coverage denominator mismatch")
            row["asns"][str(asn)]={
                "mapped_2020_blocks":len(blocks),
                "observed_status_counts":dict(status),
                "measurable_fraction":known/len(blocks),
                "up_fraction_among_current_measurable":status["up"]/known if known else None,
                "baseline_up_blocks":len(baseline[asn]),
                "baseline_up_currently_up_lower_bound":survival,
                "baseline_up_currently_up_upper_bound_if_unknown_assumed_up":upper,
                "baseline_up_currently_down":active["down"]
            }
        series.append(row)
    return {
      "status":"AUTHORIZED_SOURCE_ORIGINAL_USC_TRINOCULAR_ANALYSIS",
      "dataset":"USC ANT a39all outagedownup (postprocessed multi-vantage), plus Jan-2020 a39_supplement block_to_as",
      "not_ioda":True,
      "window_utc":[dt.datetime.fromtimestamp(start,UTC).isoformat(),dt.datetime.fromtimestamp(end,UTC).isoformat()],
      "baseline_utc":dt.datetime.fromtimestamp(pre_t,UTC).isoformat(),
      "step_minutes":step_minutes,
      "source":{str(downup_path):file_sha256(downup_path),str(map_path):file_sha256(map_path)},
      "mapping_audit":mapping_audit,"scan_audit":scan_audit,
      "mapped_asn_candidate_prefix_counts":{str(a):len(b) for a,b in by_as.items()},
      "cautions":[
        "Postprocessed source-native USC measurements are NOT individual raw probe packets and NOT source-native IODA ping-slash24",
        "Jan-2020 snapshot AS labels cannot be assumed stable for every minute of the quarter",
        "No Yemen country summary: AS membership is not geolocation and org country is not IP geolocation",
        "Unmeasurable, gone-dark, uncertain and missing are NOT converted to offline",
        "Measured-up count depends on observation coverage; upper bound counts unknown statuses conservatively",
        "Block status duration and start time carry an uncertainty interval",
        "Rows may represent correlated contiguous /24 blocks; no IID confidence interval or causal cable mechanism"
      ],
      "series":series
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--downup",type=Path,required=True,help="Authorized a39all.*.outagedownup.fsdb.bz2 or .xz")
    p.add_argument("--block-to-as",type=Path,required=True,help="Authorized a39 supplement block_to_as.fsdb.bz2")
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--from-utc",default="2020-01-08T00:00:00Z")
    p.add_argument("--until-utc",default="2020-01-12T00:00:00Z")
    p.add_argument("--baseline-utc",default="2020-01-09T08:00:00Z")
    p.add_argument("--step-minutes",type=int,default=15)
    a=p.parse_args()
    if not a.downup.is_file() or not a.block_to_as.is_file():
        p.error("Original authorized USC source datasets not supplied; do not fabricate output")
    result=analyze(a.downup,a.block_to_as,ep(a.from_utc),ep(a.until_utc),a.step_minutes,ep(a.baseline_utc))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"mapped_counts":result["mapped_asn_candidate_prefix_counts"],"n_timepoints":len(result["series"]),"input_files":[a.downup.name,a.block_to_as.name]}))
if __name__=="__main__":main()
