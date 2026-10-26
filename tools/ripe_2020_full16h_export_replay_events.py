#!/usr/bin/env python3
"""Scoped source-original 2020 RIS A/W update extraction for 2020 RIB candidates.

Prefix sets are from 2020 RRC00 origin-RIB *discovery* artifacts, not a complete
2020 national inventory. Withdrawals carry no origin, so they are classified
by candidate prefix only; never infer the original announcing ASN from W.
"""
import concurrent.futures,datetime as dt,gzip,hashlib,json,subprocess,sys
from collections import Counter
from pathlib import Path
from pybgpkit_parser import Parser
OUT=Path("_artifacts")/("2020_full_replay_chunk_"+__import__("os").environ.get("FALCON_CHUNK","unknown"));OUT.mkdir(parents=True,exist_ok=True)
BASE="https://data.ris.ripe.net/rrc00/2020.01/"
import os
CHUNK=int(os.environ.get("FALCON_CHUNK","-1"))
if CHUNK not in range(8):raise RuntimeError("FALCON_CHUNK 0..7 required")
start_time=dt.datetime(2020,1,9,8,0,tzinfo=dt.timezone.utc)+dt.timedelta(hours=CHUNK*2)
finish_time=start_time+dt.timedelta(hours=2)
WINDOWS={f"continuous_chunk_{CHUNK:02}":(start_time.isoformat(),finish_time.isoformat())}
NAMES=[];FILE_TO_WINDOW={}
current=start_time
while current<finish_time:
 fn=f"updates.{current:%Y%m%d.%H%M}.gz"
 NAMES.append(fn); FILE_TO_WINDOW[fn]=next(iter(WINDOWS))
 current+=dt.timedelta(minutes=5)
if len(NAMES)!=24:raise AssertionError("Exactly 24 original MRT files per chunk required")
prefixsets={}
for asn in ("30873","12486"):
 p=Path("_tmp")/asn/"candidate_historical_prefixes_2020.txt"
 prefixes={x.strip() for x in p.read_text().splitlines() if x.strip() and not x.startswith("#")}
 if not prefixes:raise RuntimeError("Missing historical RRC00 discovery prefixes: "+asn)
 prefixsets[asn]=prefixes
universe=set.union(*prefixsets.values())
report={
 "title":"Source-original 2020 RRC00 A/W observations for historical RIB-discovered candidate prefix universe",
 "asns":{a:{"candidate_prefixes":len(pfx)} for a,pfx in prefixsets.items()},
 "candidate_prefixes_union":len(universe),
 "status":"INCOMPLETE",
 "windows":WINDOWS,
 "source_inventory":"2020-01-09T08:00 UTC RRC00 origin RIB discovery files, not exhaustive AS inventory",
 "notes":["W messages lack origin AS and may involve non-target-origin paths","One continuous two-hour segment of an eight-segment 08:00–00:00 UTC coverage audit; only eight successful segments cover the entire period","Global event-time update counts cannot be interpreted as cable-caused changes","This original A/W event stream is retained for independent baseline RIB state replay; no p-values"],
 "records":[]
}
def fetch(name):
 path=Path("/tmp")/name
 proc=subprocess.run(["curl","--fail","--location","--retry","2","--retry-all-errors","--connect-timeout","20","--max-time","100","--silent","--show-error","-o",str(path),BASE+name],capture_output=True,text=True)
 if proc.returncode:raise RuntimeError("failed "+name+" "+proc.stderr[-180:])
 if not 1000<path.stat().st_size<100000000:raise RuntimeError("bad file size "+name)
 h=hashlib.sha256(path.read_bytes()).hexdigest()
 with gzip.open(path,"rb") as f:
  while f.read(1024*1024):pass
 return path,{"name":name,"source_url":BASE+name,"original_sha256":h,"size_bytes":path.stat().st_size,"gzip_crc":"passed"}
def analyze(item):
 path,src=item
 counts={a:Counter() for a in prefixsets};tot=Counter();samples=[]
 for batch in Parser(url=str(path),filters={"prefixes":",".join(sorted(universe))}).iter_tuple_batches(["timestamp","elem_type","prefix","origin_asns","peer_ip","peer_asn","as_path"],batch_size=10000):
  for t,elem,pfx,origins,peer_ip,peer_asn,as_path in batch:
   typ=str(elem).upper()
   if typ in ("A","ANNOUNCE","ANNOUNCEMENT"):kind="announcement"
   elif typ in ("W","WITHDRAW","WITHDRAWAL"):kind="withdrawal"
   else:raise RuntimeError("unsupported update type "+typ)
   if not (peer_ip and peer_asn and pfx):raise RuntimeError("missing peer identity")
   origs={int(x) for x in (origins or [])}
   EVENTS.write(json.dumps([t,kind,int(peer_asn),str(peer_ip),str(pfx),sorted(origs),str(as_path or "")],separators=(",",":"))+"\n")
   tot[kind]+=1
   for asn,prefixes in prefixsets.items():
    if pfx not in prefixes:continue
    if kind=="withdrawal":counts[asn]["candidate_prefix_W_origin_unknown"]+=1
    elif int(asn) in origs and len(origs)==1:counts[asn]["candidate_prefix_A_target_origin"]+=1
    else:counts[asn]["candidate_prefix_A_other_or_ambiguous_origin"]+=1
   if len(samples)<4:
    samples.append({"ts_unix":t,"kind":kind,"prefix":pfx,"asn_origin_known_for_announcement":sorted(origs) if kind=="announcement" else []})
 return dict(src,window=FILE_TO_WINDOW[src["name"]],filter_matched_elements=dict(tot),per_asn={a:dict(c) for a,c in counts.items()},examples=samples)
EVENTS=gzip.open(OUT/f"event_stream_{CHUNK:02}.jsonl.gz","wt",encoding="utf8")
try:
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:items=list(pool.map(fetch,NAMES))
 for item in items:
  row=analyze(item);report["records"].append(row)
  print(json.dumps({"file":row["name"],"matched":row["filter_matched_elements"],"per_asn":row["per_asn"]}),flush=True)
 report["window_summary"]={}
 for label in WINDOWS:
  selected=[row for row in report["records"] if row["window"]==label]
  counts={asn:Counter() for asn in prefixsets}
  for row in selected:
   for asn,metrics in row["per_asn"].items():counts[asn].update(metrics)
  report["window_summary"][label]={"complete_intervals":len(selected),"candidate_prefix_updates":{a:dict(v) for a,v in counts.items()}}
 report["status"]="SOURCE_ORIGINAL_MRT_AW_EVENTS_EXPORTED_NOT_REPLAYED" if len(report["records"])==len(NAMES) else "INCOMPLETE"
finally:
 EVENTS.close()
 (OUT/"audit.json").write_text(json.dumps(report,indent=2),encoding="utf8")
if report["status"]!="SOURCE_ORIGINAL_MRT_SAMPLE_VALIDATED_NOT_REPLAY":sys.exit("not all 2020 5min windows validated")
