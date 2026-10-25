#!/usr/bin/env python3
"""Fail-closed historical 2020 RIPE RIS rrc00 BGP RIB pilot.

Original 2020 public MRT is distinct from unavailable original 2020 IODA.
This pilot inspects only explicit origin routes for two ASNs in two historical
snapshots; it never claims to replay updates or infer per-path cable mechanisms.
"""
import collections,datetime as dt,gzip,hashlib,json,os,subprocess,sys,time
from pathlib import Path

OUT=Path("_artifacts/2020_ripe_rib_pilot");OUT.mkdir(parents=True,exist_ok=True)
FILES=[
  ("2020-01-09T08:00:00Z","bview.20200109.0800.gz"),
  # second snapshot gated until the first full historical file has been successfully parsed
]
BASE="https://data.ris.ripe.net/rrc00/2020.01/"
ASNS={30873,12486}
def get_file(name):
 path=Path("/tmp")/name
 args=["curl","--fail","--location","--retry","3","--retry-all-errors","--retry-delay","3","--connect-timeout","20","--max-time","240","--silent","--show-error","-o",str(path),BASE+name]
 c=subprocess.run(args,capture_output=True,text=True)
 if c.returncode:raise RuntimeError("MRT download failed: "+c.stderr[-450:])
 size=path.stat().st_size
 if size<1_000_000:raise RuntimeError("Unexpectedly small MRT file")
 if size>1_500_000_000:raise RuntimeError(f"MRT pilot size guard: {size} bytes")
 h=hashlib.sha256()
 with open(path,"rb") as f:
  for chunk in iter(lambda:f.read(1024*1024),b""):h.update(chunk)
 with gzip.open(path,"rb") as f:
  while f.read(4*1024*1024):pass   # checks gzip stream integrity and CRC
 return path,{"url":BASE+name,"size_bytes":size,"sha256":h.hexdigest(),"integrity":"gzip_crc_verified"}
def scan(path):
 from pybgpkit_parser import Parser
 counts=collections.Counter();by_peer=collections.defaultdict(set);by_prefix=collections.defaultdict(set)
 strict=collections.Counter();sample=[]
 cols=["timestamp","elem_type","peer_ip","peer_asn","prefix","as_path","origin_asns"]
 parser=Parser(url=str(path), filters={"origin_asns":"30873,12486"})
 for batch in parser.iter_tuple_batches(cols,batch_size=10000):
  for t,etype,peer_ip,peer_asn,prefix,path,origin_asns in batch:
   origins=[int(x) for x in (origin_asns or [])]
   if len(origins)!=1 or origins[0] not in ASNS:
    strict["discarded_ambiguous_or_wrong_origin"]+=1;continue
   asn=origins[0]
   if not peer_ip or not peer_asn or not prefix:strict["discarded_missing_peer_identity"]+=1;continue
   if not any(str(x) in str(etype).lower() for x in ("a","r")):
    strict["discarded_unexpected_elem_type"]+=1;continue
   counts[asn]+=1
   peer=f"{peer_asn}|{peer_ip}"
   by_peer[asn].add(peer);by_prefix[asn].add(str(prefix))
   if len(sample)<8:sample.append({"asn":asn,"peer":peer,"prefix":prefix,"as_path":str(path)[:130]})
 result={}
 for asn in sorted(ASNS):
  result[str(asn)]={"origin_rows":counts[asn],"unique_peer_sessions":len(by_peer[asn]),"candidate_prefix_count":len(by_prefix[asn]),"nonexhaustive_origin_view":True}
 return result,strict,sample,by_peer,by_prefix
recs=[];seen=[]
for timestamp,name in FILES:
 row={"snapshot_utc":timestamp,"collector":"rrc00","file":name,"status":"NO_VALIDATED_RIB"}
 try:
  path,source=get_file(name);row["source"]=source
  info,discarded,samples,peers,prefixes=scan(path)
  row["asns"]=info;row["discarded"]=dict(discarded);row["examples"]=samples
  if all(info[str(a)]["origin_rows"]>0 for a in ASNS):
   row["status"]="VALIDATED_ORIGIN_RIB_PILOT_NOT_FULL_BGP_REPLAY"
  else:row["status"]="INCOMPLETE_TARGET_ORIGINS"
  seen.append((timestamp,peers,prefixes))
 except Exception as e:row["error"]=repr(e)
 recs.append(row)
 print(json.dumps({"time":timestamp,"status":row["status"],"asns":row.get("asns"),"error":row.get("error")}))
 if row["status"]!="VALIDATED_ORIGIN_RIB_PILOT_NOT_FULL_BGP_REPLAY":break
report={"scope":"Historical peer-IP-specific RIPE RIS RRC00 RIB discovery. No unfiltered update replay, no native IODA, no outage inference.", "source_project":"RIPE RIS","rows":recs,"comparisons":{}}
if len(seen)==2 and all(r["status"]=="VALIDATED_ORIGIN_RIB_PILOT_NOT_FULL_BGP_REPLAY" for r in recs):
 for asn in sorted(ASNS):
  peers0,peers1=seen[0][1][asn],seen[1][1][asn]
  prefixes0,prefixes1=seen[0][2][asn],seen[1][2][asn]
  report["comparisons"][str(asn)]={"common_target_origin_peer_sessions":len(peers0&peers1),"pre_target_origin_peer_sessions":len(peers0),"post_target_origin_peer_sessions":len(peers1),"common_prefixes_at_origin_across_RIBs":len(prefixes0&prefixes1),"not_route_survival":True,"requires":"All A/W updates, full-sequence/peer liveness, archival completeness and timestamp matching"}
(OUT/"manifest.json").write_text(json.dumps(report,indent=2))
if not (len(recs)==len(FILES) and all(r["status"]=="VALIDATED_ORIGIN_RIB_PILOT_NOT_FULL_BGP_REPLAY" for r in recs)):
 sys.exit("FAIL CLOSED: one or more historical RIB pilot snapshots unavailable/unverified")
