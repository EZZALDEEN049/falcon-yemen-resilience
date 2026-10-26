#!/usr/bin/env python3
"""Audit-only January 2020 RRC00 baseline RIB + full 16h A/W replay.

Fail closed on unmatched original source archive hashes, missing 5min intervals,
or irreconcilable second source RIB. Never equate BGP path state with data-plane
IODA active reachability, physical FALCON cable attribution, or independent
samples of prefix observations.
"""
import collections,concurrent.futures,datetime as dt,gzip,hashlib,json,re,subprocess,sys
from pathlib import Path
from pybgpkit_parser import Parser
OUT=Path("_artifacts/2020_ripe_verified_full_replay");OUT.mkdir(parents=True,exist_ok=True)
INPUT=Path("_tmp/2020_replay_chunks")
ORIGINAL=json.loads(Path("results/ripe_2020_source_original_16h_aw_manifest.json").read_text())
SRC=ORIGINAL["all_192_original_checksum_anchored_file_summaries"]
ASNS=(12486,30873)
prefixes={}
for asn in ASNS:
 name=Path("_tmp")/str(asn)/"candidate_historical_prefixes_2020.txt"
 prefixes[asn]={s.strip() for s in name.read_text().splitlines() if s.strip() and not s.startswith("#")}
 if not prefixes[asn]:raise SystemExit(f"No independent 2020 prefix inventory for AS{asn}")
UNIVERSE=set.union(*prefixes.values())
if len(SRC)!=192 or len({v["name"] for v in SRC})!=192:raise SystemExit("Invalid permanent original-source 192-file manifest")
BY_SOURCE={s["name"]:s for s in SRC}
BASE="https://data.ris.ripe.net/rrc00/2020.01/"
RIBS={
"seed":("bview.20200109.0800.gz","a55cfb90f54c38452f851f6a13c8a96bd93e8a3f4aeedb48e84357b31d5e05d2"),
"end":("bview.20200110.0000.gz","3d2147cc860c534829cd89beec115487d97281c45c2a520d8c7469bb605fd38c")
}
def download(entry):
 key,(name,expected)=entry
 p=Path("/tmp")/name
 c=subprocess.run(["curl","--fail","--location","--retry","3","--retry-all-errors","--max-time","240","--connect-timeout","20","--silent","--show-error","-o",str(p),BASE+name],capture_output=True,text=True)
 if c.returncode:raise RuntimeError(f"missing RIB {name}: {c.stderr[-250:]}")
 sha=hashlib.sha256()
 with open(p,"rb") as f:
  for block in iter(lambda:f.read(4*1024*1024),b""):sha.update(block)
 if sha.hexdigest()!=expected:raise RuntimeError(f"RIB SHA256 mismatch {name}")
 with gzip.open(p,"rb") as f:
  while f.read(4*1024*1024):pass
 return key,p
def parse_RIB(path):
 routes={}
 cols=["peer_asn","peer_ip","prefix","origin_asns","as_path"]
 for batch in Parser(url=str(path),filters={"prefixes":",".join(sorted(UNIVERSE))}).iter_tuple_batches(cols,batch_size=30000):
  for peer_asn,peer_ip,pfx,origins,path_s in batch:
   if not peer_ip or not peer_asn:raise RuntimeError("RIB missing peer identity")
   k=(int(peer_asn),str(peer_ip),str(pfx))
   if k in routes:raise RuntimeError(f"multiple native RIB paths for a peer/prefix {k}")
   routes[k]=(tuple(sorted(int(x) for x in (origins or []))),str(path_s or ""))
 return routes
def peerlist(path):
 pe=set()
 for batch in Parser(url=str(path)).iter_tuple_batches(["peer_asn","peer_ip"],batch_size=50000):
  for asn,ip in batch:
   if asn and ip:pe.add((int(asn),str(ip)))
 if len(pe)<40:raise RuntimeError("RIB full-peer list fails positive control")
 return pe
files=sorted(INPUT.glob("*/audit.json"))
if len(files)!=8:raise RuntimeError(f"Missing 8 independent chunk audits, got {len(files)}")
allstreams=[]
verified=[]
for audit_file in files:
 audit=json.loads(audit_file.read_text())
 if audit.get("status")!="SOURCE_ORIGINAL_MRT_AW_EVENTS_EXPORTED_NOT_REPLAYED":raise RuntimeError("Chunk not fully exported: "+str(audit_file))
 chunk=int(audit_file.parent.name.rsplit("-",1)[-1])
 if len(audit["records"])!=24:raise RuntimeError("Incomplete 2h segment "+str(chunk))
 for row in audit["records"]:
  if row["name"] not in BY_SOURCE or row["original_sha256"]!=BY_SOURCE[row["name"]]["original_sha256"]:
   raise RuntimeError("Original source hash drift "+row["name"])
  verified.append(row["name"])
 stream=audit_file.parent/f"event_stream_{chunk:02}.jsonl.gz"
 if not stream.exists():raise RuntimeError("Missing native event stream "+str(stream))
 allstreams.append((chunk,stream,dict((e["name"],e) for e in audit["records"])))
if set(verified)!=set(BY_SOURCE) or len(verified)!=192:raise RuntimeError("Not every original MRT file hash validated exactly once")
if set(v[0] for v in allstreams)!=set(range(8)):raise RuntimeError("Chunk indexing incomplete")
replay_records=[]
for chunk,stream,rows in sorted(allstreams):
 linecount=0
 with gzip.open(stream,"rt",encoding="utf8") as f:
  for line in f:
   data=json.loads(line)
   if not isinstance(data,list) or len(data)!=7:raise RuntimeError("Malformed complete A/W event")
   t,kind,peer_asn,peer_ip,pfx,origins,aspath=data
   time=dt.datetime.fromtimestamp(float(t),dt.timezone.utc)
   # Source records can have timestamps slightly outside nominal file stamp; verify global event period.
   if not (dt.datetime(2020,1,9,7,55,tzinfo=dt.timezone.utc)<=time<=dt.datetime(2020,1,10,0,5,tzinfo=dt.timezone.utc)):
    raise RuntimeError("Update timestamp outside auditable source bracket")
   if pfx not in UNIVERSE:raise RuntimeError("Untracked prefix slipped through filter")
   replay_records.append((float(t),kind,int(peer_asn),str(peer_ip),pfx,tuple(int(x) for x in origins),str(aspath)))
   linecount+=1
 expected=sum(sum(row["filter_matched_elements"].values()) for row in rows.values())
 if linecount!=expected:raise RuntimeError(f"Event stream {chunk} has {linecount} rows vs {expected} native audited source rows")
replay_records.sort(key=lambda z:z[0])
pre=dt.datetime(2020,1,9,8,tzinfo=dt.timezone.utc).timestamp()
end=dt.datetime(2020,1,10,0,tzinfo=dt.timezone.utc).timestamp()
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 origins=dict(pool.map(download,RIBS.items()))
seed=parse_RIB(origins["seed"])
truth=parse_RIB(origins["end"])
alive=peerlist(origins["end"])
state=dict(seed)
# Withdrawal and announcements carry per-peer prefix state; W never contains an origin.
event_counts=collections.Counter();origin_transitions=collections.Counter()
for t,kind,pa,ip,pfx,origins,aspath in replay_records:
 if not pre<t<end:continue
 k=(pa,ip,pfx)
 old=state.get(k,((), ""))[0]
 if kind=="withdrawal":
  state.pop(k,None);event_counts["withdrawal"]+=1
 elif kind=="announcement":
  if len(origins)!=1:
   # Explicit ambiguity, reject a falsely precise origin state.
   state[k]=(origins,aspath);event_counts["ambiguous_origin_announcement"]+=1
  else:
   state[k]=(origins,aspath);event_counts["announcement"]+=1
  if old!=origins:origin_transitions[(str(old),str(origins))]+=1
 else:raise RuntimeError("Bad event type")
# Check the exact prefix/peer-origin state for active peers. The RIB is a
# checkpoint snapshot, not a perfect guarantee updates include session resets.
eligible={k for k in set(state)|set(truth) if k[:2] in alive}
origin_mismatch=[k for k in eligible if state.get(k,((),))[0]!=truth.get(k,((),))[0]]
path_mismatch=[k for k in eligible if k in state and k in truth and state[k][0]==truth[k][0] and state[k][1]!=truth[k][1]]
report={
 "status":"REPLAY_FAILED_CHECKPOINT_RECONCILIATION",
 "period_utc":["2020-01-09T08:00:00Z","2020-01-10T00:00:00Z"],
 "original_mrt_update_sources_verified":len(verified),
 "original_gzip_event_stream_records":len(replay_records),
 "historical_candidate_prefix_universe":{str(a):len(prefixes[a]) for a in ASNS},
 "original_rib_sha256":{k:RIBS[k][1] for k in RIBS},
 "comparable_second_RIB_peer_sessions":len(alive),
 "events_between_exact_RIB_boundaries":dict(event_counts),
 "replayed_state_count_on_alive_peers":sum(k[:2] in alive for k in state),
 "true_second_RIB_state_count":len(truth),
 "origin_mismatch_count":len(origin_mismatch),
 "path_mismatch_given_origin_count":len(path_mismatch),
 "origin_mismatch_examples":[{"peerASN":k[0],"prefix":k[2],"replay_origin":list(state.get(k,((),))[0]),"end_RIB_origin":list(truth.get(k,((),))[0])} for k in origin_mismatch[:12]],
 "source_scope":["RRC00 only","Historical RIB candidate universe only","Withdrawals have no origin","Peer remains observed at endpoint, no continuous uptime guarantee","Data-plane and cable-causality not inferred"],
}
if not origin_mismatch:
 report["status"]="REPLAY_ORIGIN_CHECKPOINT_RECONCILED_PATHS_REQUIRE_SEPARATE_AUDIT" if path_mismatch else "REPLAY_RIB_ORIGIN_AND_PATH_RECONCILED_FOR_THIS_CANDIDATE_UNIVERSE"
(OUT/"full_replay_validation.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({k:v for k,v in report.items() if k!="origin_mismatch_examples"},indent=2),flush=True)
# Always fail closed when checkpoint not reconciled.
if origin_mismatch or path_mismatch:sys.exit("CHECKPOINT RECONCILIATION FAILED; no event-time route-survival claims")
