#!/usr/bin/env python3
"""Independent original 2020 RIPE Atlas historical active-ping sources.

No USC access and NO IODA 2020 source-native data claimed.
"""
from collections import Counter,defaultdict
from datetime import datetime,timezone
import hashlib,json,urllib.parse,urllib.request
from pathlib import Path
O=Path("_artifacts/atlas_2020_original_public_active_probe");O.mkdir(parents=True,exist_ok=True)
ROOT="https://atlas.ripe.net/api/v2/"
A=1578441600;B=1578873600
def req(url,limit=18000000):
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"FALCON-2020-Reproducible-Atlas-Public/1.0","Accept":"application/json"}),timeout=90) as r:
  content=r.read(limit+1)
  if len(content)>limit:raise RuntimeError("Response too large: "+url)
  return json.loads(content),hashlib.sha256(content).hexdigest(),len(content)
data={"status":"PUBLIC_ATLAS_HISTORICAL_SOURCE_AUDIT","window":["2020-01-08T00:00:00Z","2020-01-13T00:00:00Z"],"traces":[],"probe_discovery":[]}
for asn in [30873,12486]:
 url=ROOT+"probes/?"+urllib.parse.urlencode({"asn_v4":asn,"page_size":100})
 row={"asn":asn,"url":url}
 try:
  payload,sha,n=req(url)
  row["sha256"]=sha;row["count"]=payload.get("count")
  row["probes"]=[{"id":p.get("id"),"asn_v4":p.get("asn_v4"),"first_connected":p.get("first_connected"),"last_connected":p.get("last_connected"),"status":p.get("status",{}).get("name") if isinstance(p.get("status"),dict) else p.get("status")} for p in payload.get("results",[])]
 except Exception as e:row["error"]=repr(e)
 data["probe_discovery"].append(row)
 print(json.dumps({"source_asn":asn,"probe_count":row.get("count"),"probes":row.get("probes",[])[:12],"error":row.get("error")}),flush=True)
for id,asn in [(8307351,12486)]:
 row={"measurement_id":id,"target_asn_catalog":asn}
 try:
  info,hash_meta,n=req(ROOT+f"measurements/{id}/")
  row["meta_sha256"]=hash_meta;row["target_ip"]=info.get("target_ip");row["target"]=info.get("target");row["measurement_type"]=info.get("type");row["target_asn"]=info.get("target_asn");row["start_time"]=info.get("start_time");row["status"]=info.get("status")
  if info.get("type")!="ping" or info.get("target_asn")!=asn:raise RuntimeError("Target ASN not validated by catalog")
  url=ROOT+f"measurements/{id}/results/?"+urllib.parse.urlencode({"start":A,"stop":B-1})
  events,source_hash,size=req(url)
  row["source_url"]=url;row["response_sha256"]=source_hash;row["response_bytes"]=size
  if not isinstance(events,list) or not events:raise RuntimeError("No public original 2020 ping observations")
  rows=[r for r in events if isinstance(r.get("timestamp"),(int,float)) and A<=r["timestamp"]<B]
  if not rows:raise RuntimeError("No matching 2020 ping timestamps")
  byhour=defaultdict(Counter);byday=defaultdict(Counter);probes=set()
  for r in rows:
   if "rcvd" not in r or "sent" not in r:raise RuntimeError("Ping sample lacks both sent/rcvd counts")
   sent,rec=r["sent"],r["rcvd"]
   if not isinstance(sent,int) or not isinstance(rec,int) or sent<0 or rec<0 or rec>sent:raise RuntimeError("Invalid ICMP sent/rcvd count")
   if r.get("prb_id") is not None:probes.add(r["prb_id"])
   hour=datetime.fromtimestamp(r["timestamp"],timezone.utc).strftime("%Y-%m-%dT%H:00:00Z")
   day=hour[:10]
   for c in (byhour[hour],byday[day]):
    c["measurement_results"]+=1;c["sent_packets"]+=sent;c["received_packets"]+=rec
    c["results_with_positive_reply"]+=int(rec>0)
    c["results_zero_reply"]+=int(rec==0)
  row["n_results"]=len(rows);row["n_unique_probe_ids"]=len(probes)
  row["source_probe_ids"]=sorted(probes)
  row["days"]={k:dict(v) for k,v in sorted(byday.items())}
  row["hours"]={k:dict(v) for k,v in sorted(byhour.items())}
  row["scope_warning"]="Historical ICMP responses to a single target (not native IODA ping-slash24 /24 coverage). Shared probe exposures; no per-AS geographic/general health inference. Probe loss/absence not equivalent to failures."
 except Exception as e:row["error"]=repr(e)
 data["traces"].append(row)
 print(json.dumps({"id":id,"n":row.get("n_results"),"unique_probes":row.get("n_unique_probe_ids"),"daily":row.get("days"),"error":row.get("error")}),flush=True)
(O/"audit.json").write_text(json.dumps(data,indent=2),encoding="utf8")
