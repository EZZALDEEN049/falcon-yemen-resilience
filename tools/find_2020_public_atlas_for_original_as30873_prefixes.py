#!/usr/bin/env python3
"""Search historical RIPE Atlas target IP/prefix index for historical RRC00
AS30873 2020-origin prefixes. Never call this native IODA data.

The target_asn metadata can miss historical different-AS mapping. We use
verified 2020 RIS prefix candidates; find public Atlas ping tests that actually
have data from Jan 8–12 2020 and preserve exact test/probe/target scope.
"""
from pathlib import Path
import concurrent.futures,datetime as dt,hashlib,json,time,urllib.parse,urllib.request
O=Path("_artifacts/atlas_2020_historical_as30873_prefix_search");O.mkdir(parents=True,exist_ok=True)
P=Path("_tmp/30873/candidate_historical_prefixes_2020.txt")
PREFIXES=sorted({x.strip() for x in P.read_text().splitlines() if x.strip() and not x.startswith("#")})
if len(PREFIXES)!=109:raise RuntimeError(f"RRC00 original inventory changed: {len(PREFIXES)}")
A=1578441600;B=1578873600
ROOT="https://atlas.ripe.net/api/v2/measurements/"
def get(url,bytes_max=9000000):
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Falcon-2020-public-Atlas-historical-origin-inventory/1.0","Accept":"application/json"}),timeout=40) as x: raw=x.read(bytes_max+1)
 if len(raw)>bytes_max:raise RuntimeError("Oversize response")
 return json.loads(raw),hashlib.sha256(raw).hexdigest()
def lookup(prefix):
 params={"target_ip":prefix,"type":"ping","start_time__lte":B,"page_size":80}
 url=ROOT+"?"+urllib.parse.urlencode(params)
 row={"original_2020_RRC00_origin_candidate_prefix":prefix,"url":url}
 try:
  obj,sha=get(url);row["catalog_sha256"]=sha;row["catalog_count"]=obj.get("count");row["catalog_pagination_next"]=bool(obj.get("next"))
  row["matches"]=[{"id":x.get("id"),"target_ip":x.get("target_ip"),"start_time":x.get("start_time"),"stop_time":x.get("stop_time"),"target_asn_catalog":x.get("target_asn"),"type":x.get("type"),"status":x.get("status",{}).get("name") if isinstance(x.get("status"),dict) else x.get("status")} for x in obj.get("results",[]) if isinstance(x.get("id"),int)]
 except Exception as e:row["error"]=repr(e)
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as e:rows=list(e.map(lookup,PREFIXES))
mids={}
for row in rows:
 for m in row.get("matches",[]):
  if m["id"] not in mids:mids[m["id"]]=(row["original_2020_RRC00_origin_candidate_prefix"],m)
hits=[]
for msm,(prefix,m) in mids.items():
 if m["start_time"] is None:continue
 if isinstance(m["start_time"],(int,float)) and m["start_time"]>B:continue
 # Stop time null is not interpreted as continuously operating.
 hits.append((msm,prefix,m))
tested=[]
# Bound raw reads to 35 likely candidates; prefer 2019 and earlier start measurements.
for msm,pfx,meta in sorted(hits,key=lambda x:(x[2].get("start_time") or 0,x[0]))[:35]:
 url=f"{ROOT}{msm}/results/?"+urllib.parse.urlencode({"start":A,"stop":B-1})
 r={"id":msm,"historical_prefix":pfx,"catalog_target":meta.get("target_ip"),"catalog_asn":meta.get("target_asn_catalog"),"url":url}
 try:
  obj,sha=get(url)
  if not isinstance(obj,list):raise RuntimeError("Non-list source")
  values=[x for x in obj if A<=x.get("timestamp",0)<B]
  r.update(original_source_sha256=sha,actual_2020_ping_results=len(values),probes=len({x.get("prb_id") for x in values}),responded=sum(1 for x in values if isinstance(x.get("rcvd"),int) and x["rcvd"]>0),without_reply=sum(1 for x in values if x.get("rcvd")==0))
 except Exception as e:r["error"]=repr(e)
 tested.append(r)
 if r.get("actual_2020_ping_results",0):print(json.dumps({"FOUND_2020_PING":r}),flush=True)
errors=[x for x in rows if x.get("error")]
print(json.dumps({"prefixes_checked":len(rows),"catalog_errors":len(errors),"unique_measurements_found":len(mids),"historical_ping_measurements_tested":len(tested),"confirmed_actual_2020_measurements":sum(1 for z in tested if z.get("actual_2020_ping_results",0))}),flush=True)
(O/"audit.json").write_text(json.dumps({"status":"SOURCE_ORIGINAL_ATLAS_PREFIX_TARGET_DISCOVERY_ONLY","historical_prefixes":len(PREFIXES),"catalog_errors":errors,"prefix_catalog":rows,"actual_2020_ping_tests":tested,"limits":["Only first 80 catalog measurements per historical prefix","At most 35 returned candidate measurement IDs tested for 2020 actual results","Atlas target list is not complete coverage nor IODA native signal archive","Historic AS origin of individual target IP should be independently rechecked"]},indent=2))
