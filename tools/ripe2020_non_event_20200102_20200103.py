#!/usr/bin/env python3
"""2020 RIPE RIS RRC00: two genuine MRT snapshots and all-prefix peer-coverage audit.

IMPORTANT:
- Source-native RIPE RIS MRT; NOT source-native 2020 IODA.
- 2020-01-09 08 UTC and 2020-01-10 00 UTC are check-points, not validated
  pre-incident and post-incident boundaries.
- All-route peer identity in second RIB is independent of seeing the target ASN.
- Prefix-observation retention below is two-snapshot, same-peer, target-origin
  visibility; it is not cable-causal reachability, withdrawal count or traffic.
"""
from collections import Counter,defaultdict
import csv
import gzip,hashlib,json,os,statistics,subprocess,sys
from pathlib import Path
from pybgpkit_parser import Parser

RRC=os.environ.get("FALCON_RRC","rrc00")
if RRC not in {"rrc00","rrc01","rrc10"}:raise RuntimeError("Unsupported research collector")
OUT=Path("_artifacts")/f"2020_ripe_peer_coverage_{RRC}"; OUT.mkdir(parents=True,exist_ok=True)
FILES=[
    ("2020-01-02T08:00:00Z","bview.20200102.0800.gz"),
    ("2020-01-03T00:00:00Z","bview.20200103.0000.gz"),
]
ASNS=(12486,30873)
ROOT=f"https://data.ris.ripe.net/{RRC}/2020.01/"
MAX_GZ=1500000000
# The Jan 2-3 reference window was chosen before inspecting its outcomes. Source SHA256 is recorded on original RIB download.

def acquire(filename):
    file=Path("/tmp")/filename
    url=ROOT+filename
    ret=subprocess.run(["curl","-fL","--retry","3","--retry-all-errors","--connect-timeout","20","--max-time","240","-sS","-o",str(file),url],capture_output=True,text=True)
    if ret.returncode: raise RuntimeError("source download error "+ret.stderr[-300:])
    n=file.stat().st_size
    if n<1000000 or n>MAX_GZ:raise RuntimeError("impossible source length "+str(n))
    sha=hashlib.sha256()
    with open(file,"rb") as f:
        for part in iter(lambda:f.read(4*1024*1024),b""):sha.update(part)
    with gzip.open(file,"rb") as f:
        while f.read(4*1024*1024):pass
    return file,{"url":url,"bytes":n,"sha256":sha.hexdigest(),"gzip_crc":"passed"}

def collect(file,ts):
    # Independent peer coverage: read ALL routes, not only target AS.
    all_peers=set();route_records=0
    for batch in Parser(url=str(file)).iter_tuple_batches(["peer_asn","peer_ip"],batch_size=50000):
        for peer_asn,peer_ip in batch:
            if peer_asn and peer_ip:all_peers.add((int(peer_asn),str(peer_ip)))
            route_records+=1
    if not all_peers or route_records<10000:raise RuntimeError("Full-RIB coverage insufficient")
    targets={asn:{} for asn in ASNS};discarded=Counter()
    columns=["peer_ip","peer_asn","prefix","as_path","origin_asns"]
    for batch in Parser(url=str(file),filters={"origin_asns":",".join(map(str,ASNS))}).iter_tuple_batches(columns,batch_size=20000):
        for peer_ip,peer_asn,prefix,path,origins in batch:
            o=[int(x) for x in (origins or [])]
            if len(o)!=1 or o[0] not in ASNS:
                discarded["ambiguous_origin"]+=1;continue
            if not (peer_ip and peer_asn and prefix):
                discarded["missing_identity"]+=1;continue
            peer=(int(peer_asn),str(peer_ip))
            if peer not in all_peers:raise AssertionError("Target peer absent from all-prefix RIB")
            key=peer+(str(prefix),)
            if key in targets[o[0]]:
                discarded["duplicate_origin_per_peer_prefix"]+=1
                # All duplicate paths are ambiguous, and a comparison of these
                # requires explicit best-route tie-breaking; refuse to publish.
                raise RuntimeError("Duplicate target-origin RIB entry for same peer/prefix")
            targets[o[0]][key]=str(path or "")
    if any(len(targets[asn])==0 for asn in ASNS):raise RuntimeError("No target-origin observations")
    return {"timestamp":ts,"full_rib_elements":route_records,"all_peer_sessions":all_peers,"targets":targets,"discarded":dict(discarded)}

def immediate_upstream(as_path,asn):
    tokens=as_path.split()
    if len(tokens)<2 or not all(v.isdigit() for v in tokens) or int(tokens[-1])!=asn:return None
    i=len(tokens)-1
    while i>0 and tokens[i-1]==tokens[-1]:i-=1
    return tokens[i-1] if i>0 else None

def assess(first,second,asn):
    pre=first["targets"][asn];post=second["targets"][asn]
    alive=first["all_peer_sessions"] & second["all_peer_sessions"]
    pre_peers={k[:2] for k in pre};post_peers={k[:2] for k in post}
    common_target_peer=pre_peers & post_peers
    eligible={key for key in pre if key[:2] in alive}
    retained=eligible & set(post)
    lost=eligible-set(post)
    excluded_pre=set(pre)-eligible
    if not eligible:raise RuntimeError("No independently observable target-origin vantage")
    by_peer=defaultdict(lambda:[0,0])
    for key in eligible:
        peer=key[:2]
        by_peer[peer][0]+=1
        if key in retained:by_peer[peer][1]+=1
    ratios=[b/a for a,b in by_peer.values()]
    upstream_pairs=[]
    provider_transitions=Counter()
    upstream_pre=Counter();upstream_post=Counter()
    peer_changes=defaultdict(lambda:[0,0]);prefix_changes=defaultdict(lambda:[0,0])
    missing_aspaths=0
    for k in retained:
        p1=immediate_upstream(pre[k],asn)
        p2=immediate_upstream(post[k],asn)
        if p1 is None or p2 is None:missing_aspaths+=1
        else:
            upstream_pairs.append((p1,p2))
            provider_transitions[(p1,p2)]+=1
            upstream_pre[p1]+=1
            upstream_post[p2]+=1
            peer_changes[k[:2]][0]+=1
            prefix_changes[k[2]][0]+=1
            if p1!=p2:
                peer_changes[k[:2]][1]+=1
                prefix_changes[k[2]][1]+=1
    result={
      "asn":asn,
      "two_snapshot_target_origin_rows":{"first":len(pre),"second":len(post)},
      "target_origin_peer_sessions":{"first":len(pre_peers),"second":len(post_peers),
        "both_target_origin":len(common_target_peer)},
      "all_origin_independent_peer_sessions":{"first":len(first["all_peer_sessions"]),"second":len(second["all_peer_sessions"]),"both":len(alive)},
      "peer_liveness_verified_with_unrelated_origins":{
        "first_target_peers_seen_in_second_FULL_RIB":len(pre_peers & second["all_peer_sessions"]),
        "first_target_peers_NOT_seen_in_second_FULL_RIB":len(pre_peers-second["all_peer_sessions"]),
        "fraction":len(pre_peers & second["all_peer_sessions"])/len(pre_peers)},
      "controlled_two_snapshot_route_observations":{
        "first_target_origin_routes_on_independently_alive_peers":len(eligible),
        "also_target_origin_on_same_peer_prefix_second":len(retained),
        "absent_target_origin_on_same_peer_prefix_second":len(lost),
        "excluded_first_routes_no_second_peer_coverage":len(excluded_pre),
        "target_origin_retention_fraction_on_alive_peers":len(retained)/len(eligible),
        "peer_equal_weight_median_retention":statistics.median(ratios),
        "number_independent_matched_peers":len(by_peer)
      },
      "upstream_change_observations":{
        "common_target_origin_routes_with_parsable_immediate_upstream":len(upstream_pairs),
        "changed":sum(a!=b for a,b in upstream_pairs),
        "fraction":(sum(a!=b for a,b in upstream_pairs)/len(upstream_pairs) if upstream_pairs else None),
        "unparseable_common_routes":missing_aspaths,
        "adjacent_upstream_most_common_before":upstream_pre.most_common(12),
        "adjacent_upstream_most_common_after":upstream_post.most_common(12),
        "top_upstream_transitions":[{"from_asn":k[0],"to_asn":k[1],"route_observations":v} for k,v in provider_transitions.most_common(14)],
        "adjacent_AS15412_route_observations_before":upstream_pre.get("15412",0),
        "adjacent_AS15412_route_observations_after":upstream_post.get("15412",0),
        "distinct_prefixes_with_parsable_upstream":len(prefix_changes),
        "distinct_prefixes_with_any_neighbor_change":sum(y>0 for x,y in prefix_changes.values()),
        "distinct_peer_sessions_with_parsable_upstream":len(peer_changes),
        "distinct_peer_sessions_with_any_neighbor_change":sum(y>0 for x,y in peer_changes.values()),
        "peer_equal_weight_median_upstream_change_fraction":statistics.median([y/x for x,y in peer_changes.values()]) if peer_changes else None,
        "prefix_equal_weight_median_upstream_change_fraction":statistics.median([y/x for x,y in prefix_changes.values()]) if prefix_changes else None,
        "counting_caveat":"Route-observation transitions share prefixes, collectors, and upstreams; never claim independent samples or causal attribution."},
      "scope_limits":[
        "Not comparable to IODA /24-visible signal percentages",
        "First snapshot not independently confirmed pre-cable-failure",
        "No A/W update replay; reason for route absence (withdrawal, origin change, local policy) not established",
        "Peer seen in both RIB snapshots does not prove continuous operation between snapshots",
        "Only one RIPE RRC collector per run, not a full nationally representative sample",
        "No inference about actual path taken by customer packets, traffic, or physical cable backup"
      ]
    }
    return result

def export_individual_and_unit_distributions(first, second, collector):
    """All first-origin observations; no invented missing routes or confidence intervals."""
    pre_alive=first["all_peer_sessions"] & second["all_peer_sessions"]
    detailed=[];prefix_groups=defaultdict(list);peer_groups=defaultdict(list)
    # Non-event outcomes not fixed in advance; all observed data must be exported, including zero-change cases.
    for target_as in ASNS:
        first_routes=first["targets"][target_as];last_routes=second["targets"][target_as]
        for key,path in sorted(first_routes.items()):
            peer_as,peer_ip,prefix=key
            alive=key[:2] in pre_alive
            retained=alive and key in last_routes
            before=immediate_upstream(path,target_as)
            after=immediate_upstream(last_routes[key],target_as) if retained else None
            comparable=retained and before is not None and after is not None
            changed=(int(before!=after) if comparable else "")
            row={"collector":collector,"target_as":target_as,"peer_asn":peer_as,"peer_ip":peer_ip,"prefix":prefix,
             "peer_present_in_both_full_RIBs":int(alive),"eligible":int(alive),
             "same_origin_retained":int(retained),"origin_absent_or_changed_at_endpoint":int(alive and not retained),
             "pre_adjacent_as":before or "","post_adjacent_as":after or "",
             "neighbor_comparable":int(comparable),"neighbor_changed":changed}
            detailed.append(row)
            if comparable:
                prefix_groups[(collector,target_as,prefix)].append(changed)
                peer_groups[(collector,target_as,peer_as,peer_ip)].append(changed)
    def group_rows(groups, keys):
        out=[]
        for k,vals in sorted(groups.items()):
            r=dict(zip(keys,k))
            r.update({"comparable":len(vals),"changed":sum(vals),
               "changed_pct":100*sum(vals)/len(vals),"any_changed":int(any(vals))})
            out.append(r)
        return out
    per_prefix=group_rows(prefix_groups,["collector","target_as","prefix"])
    per_peer=group_rows(peer_groups,["collector","target_as","peer_asn","peer_ip"])
    summary=[]
    for target_as in ASNS:
        sub=[r for r in detailed if r["target_as"]==target_as]
        psub=[r for r in per_prefix if r["target_as"]==target_as]
        qsub=[r for r in per_peer if r["target_as"]==target_as]
        eligible=sum(r["eligible"] for r in sub)
        retained=sum(r["same_origin_retained"] for r in sub)
        changed=sum(r["neighbor_changed"] for r in sub if r["neighbor_comparable"])
        comparable=sum(r["neighbor_comparable"] for r in sub)


        # Explicitly allow missing parseable adjacency: report comparable denominators separately.
        pr=[r["changed_pct"] for r in psub];qr=[r["changed_pct"] for r in qsub]
        summary.append({"collector":collector,"target_as":target_as,"initial_rows":len(sub),
          "excluded_peer_absent":len(sub)-eligible,"eligible":eligible,"retained":retained,
          "not_retained":eligible-retained,"changed":changed,"comparable":comparable,
          "peer_prefix_changed_pct":100*changed/comparable,
          "prefix_count":len(psub),"prefix_any_changed":sum(r["any_changed"] for r in psub),
          "prefix_equal_mean_pct":statistics.mean(pr),"prefix_equal_median_pct":statistics.median(pr),
          "peer_count":len(qsub),"peer_any_changed":sum(r["any_changed"] for r in qsub),
          "peer_equal_mean_pct":statistics.mean(qr),"peer_equal_median_pct":statistics.median(qr)})
    def csv_write(name,items):
        p=OUT/name
        with p.open("w",newline="",encoding="utf-8") as f:
            writer=csv.DictWriter(f,fieldnames=list(items[0]))
            writer.writeheader();writer.writerows(items)
    csv_write("BGP_2020_peer_prefix_records.csv",detailed)
    csv_write("BGP_2020_prefix_distributions.csv",per_prefix)
    csv_write("BGP_2020_peer_distributions.csv",per_peer)
    csv_write("BGP_2020_validated_unit_summaries.csv",summary)
    (OUT/"individual_output_status.json").write_text(json.dumps({
        "status":"PREDECLARED_NON_EVENT_BASELINE_SOURCE_RIBS_PROCESSED",
        "collector":collector,
        "first_timestamp":"2020-01-02T08:00:00Z","second_timestamp":"2020-01-03T00:00:00Z",
        "rows":len(detailed),"prefix_groups":len(per_prefix),"peer_groups":len(per_peer),
        "expected_exact_numbers_compared":0,
        "baseline_predeclared":"2020-01-02T08:00:00Z to 2020-01-03T00:00:00Z, 16 hours (one week before reported Jan 9 disruption)",
        "limitations":["two snapshots","selected origin networks",
          "peer seen at endpoints does not prove continuous uptime",
          "observations are dependent and not packet reachability"]},indent=2)+"\n")
    return summary


manifest={"measurement":"RIPE RIS collector-specific two full historical MRT RIB snapshots, peer-liveness-qualified target-origin audit (not IODA)","collector":RRC,
"status":"NOT_COMPLETED","snapshots":[],"results":[]}
try:
    snapshots=[]
    for ts,filename in FILES:
        path,src=acquire(filename)
        rows=collect(path,ts)
        manifest["snapshots"].append({"time_utc":ts,"source":src,"full_rib_elements":rows["full_rib_elements"],
          "all_peer_sessions":len(rows["all_peer_sessions"]),"target_origin_route_counts":{str(a):len(rows["targets"][a]) for a in ASNS},
          "target_origin_discarded":rows["discarded"]})
        snapshots.append(rows)
        print(json.dumps({"progress_time":ts,"source_bytes":src["bytes"],"all_peers":len(rows["all_peer_sessions"]),"targets":{str(a):len(rows["targets"][a]) for a in ASNS}}),flush=True)
    if len(snapshots)!=2:raise RuntimeError("not two snapshots")
    manifest["results"]=[assess(snapshots[0],snapshots[1],a) for a in ASNS]
    manifest["individual_unit_summary"]=export_individual_and_unit_distributions(snapshots[0],snapshots[1],RRC)
    manifest["status"]="VALIDATED_TWO_SNAPSHOT_DESCRIPTIVE_NOT_EVENT_CAUSAL"
    print(json.dumps({"status":manifest["status"],"results":manifest["results"]},indent=2),flush=True)
finally:
    (OUT/"audit.json").write_text(json.dumps(manifest,indent=2),encoding="utf8")
if manifest["status"]!="VALIDATED_TWO_SNAPSHOT_DESCRIPTIVE_NOT_EVENT_CAUSAL":sys.exit(2)
