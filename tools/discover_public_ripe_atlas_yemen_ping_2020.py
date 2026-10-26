#!/usr/bin/env python3
"""Discover PUBLIC 2020 RIPE Atlas active ping evidence by target ASN.

This accesses independently sourced RIPE Atlas measurements, not source-native
IODA or USC data. Fail closed on absent source readings, errors or wrong dates.
"""
from pathlib import Path
import datetime as dt,hashlib,json,urllib.parse,urllib.request,time
O=Path("_artifacts/ripe_atlas_public_2020_discovery");O.mkdir(parents=True,exist_ok=True)
ROOT="https://atlas.ripe.net/api/v2/measurements/"
START=1578441600 # 2020-01-08 UTC
END=1578873600 # 2020-01-13 UTC exclusive
ASNS=[30873,12486]
def fetch(url,max_bytes=6000000):
 req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"FALCON-2020-academic-independent-validation/1.0"})
 with urllib.request.urlopen(req,timeout=45) as r:
  content=r.read(max_bytes+1)
  if len(content)>max_bytes:raise ValueError("source response too large; rerun narrower")
  return json.loads(content),hashlib.sha256(content).hexdigest()
catalog=[]
for asn in ASNS:
 p={"target_asn":asn,"type":"ping","start_time__lte":END,"stop_time__gte":START,"page_size":60}
 url=ROOT+"?"+urllib.parse.urlencode(p)
 row={"asn":asn,"catalog_url":url}
 try:
  data,sha=fetch(url)
  row["catalog_response_sha256"]=sha;row["count"]=data.get("count")
  mids=[]
  for m in data.get("results",[]):
   rid=m.get("id")
   st=m.get("start_time");et=m.get("stop_time")
   mids.append({"id":rid,"target":m.get("target"),"target_ip":m.get("target_ip"),"target_asn":m.get("target_asn"),"start_time":st,"stop_time":et,"type":m.get("type"),"status":m.get("status",{}).get("name") if isinstance(m.get("status"),dict) else m.get("status")})
  row["measurements"]=mids
 except Exception as e:row["error"]=repr(e)
 catalog.append(row)
 print(json.dumps({"asn":asn,"count":row.get("count"),"examples":row.get("measurements",[])[:10],"error":row.get("error")}),flush=True)
report={"window_start_unix":START,"window_end_exclusive_unix":END,"scope":"RIPE Atlas PUBLIC independently archived ping target-ASN measurements; not native IODA/USC, not representative sampling of all /24s","catalog":catalog,"test_results":[]}
for item in catalog:
 for m in item.get("measurements",[])[:3]:
  id=m.get("id")
  if not isinstance(id,int):continue
  p={"start":START,"stop":END-1}
  url=f"{ROOT}{id}/results/?"+urllib.parse.urlencode(p)
  q={"asn":item["asn"],"measurement_id":id,"target_ip":m.get("target_ip"),"request":url}
  try:
   data,sha=fetch(url,12000000)
   if not isinstance(data,list):raise ValueError("expected ping result list")
   sample=[]
   probes=set();responses=0;failures=0;total=0
   for event in data:
    t=event.get("timestamp")
    if not isinstance(t,(int,float)) or not START<=t<END:continue
    total+=1
    if event.get("prb_id") is not None:probes.add(event["prb_id"])
    if isinstance(event.get("rcvd"),(int,float)):
     if event["rcvd"]>0:responses+=1
     else:failures+=1
    if len(sample)<8:sample.append({k:event.get(k) for k in ("timestamp","prb_id","from","dst_addr","sent","rcvd","avg","min","max")})
   q.update(source_response_sha256=sha,returned_measurement_results=len(data),historical_results_in_window=total,unique_probe_ids=len(probes),results_with_reply=responses,results_with_zero_replies=failures,samples=sample)
  except Exception as e:q["error"]=repr(e)
  report["test_results"].append(q)
  print(json.dumps({"asn":item["asn"],"id":id,"results":q.get("historical_results_in_window"),"reply":q.get("results_with_reply"),"zero":q.get("results_with_zero_replies"),"error":q.get("error")}),flush=True)
(O/"audit.json").write_text(json.dumps(report,indent=2),encoding="utf8")
