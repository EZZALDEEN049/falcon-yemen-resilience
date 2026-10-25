#!/usr/bin/env python3
"""Independent archive discovery for IODA's 2020 original BGP and active /24 series.

Queries Internet Archive/CDX availability for exact legacy API paths; responses
are evidence about archival accessibility, not substitutes for source samples.
Only a verified time-labelled native data series can trigger recovery approval.
"""
import concurrent.futures,datetime as dt,hashlib,json,urllib.error,urllib.parse,urllib.request
from pathlib import Path

START=int(dt.datetime(2020,1,8,tzinfo=dt.timezone.utc).timestamp())
END=int(dt.datetime(2020,1,12,tzinfo=dt.timezone.utc).timestamp())
BASE=Path("_artifacts/ioda_2020_wayback")
BASE.mkdir(parents=True,exist_ok=True)
Q=urllib.parse.urlencode({"from":START,"until":END})
legacy=[
  "https://api.ioda.caida.org/signals/asn/30873?"+Q,
  "https://api.ioda.caida.org/signals/asn/12486?"+Q,
  "https://api.ioda.caida.org/signals/country/YE?"+Q,
  "https://api.ioda.caida.org/dev/signals/asn/30873?"+Q,
  "https://api.ioda.caida.org/dev/signals/asn/12486?"+Q,
  "https://ioda.caida.org/ioda/data/signals?meta=asn&code=30873&"+Q
]
tasks=[]
for i,u in enumerate(legacy):
  tasks.append((f"ia_available_{i}", "https://archive.org/wayback/available?"+urllib.parse.urlencode({"url":u,"timestamp":"20200201"})))
for i,pattern in enumerate((
 "api.ioda.caida.org/signals/asn/30873*",
 "api.ioda.caida.org/signals/asn/12486*",
 "api.ioda.caida.org/*signals*",
 "ioda.caida.org/ioda/data/*",
)):
  tasks.append((f"ia_cdx_{i}","https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode({
    "url":pattern,"output":"json","filter":"statuscode:200","collapse":"urlkey","limit":25
  })))
def get(item):
 name,url=item;r={"name":name,"request_url":url,"classification":"NOT_FOUND","checked_at_utc":dt.datetime.now(dt.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"FALCON-Yemen-Research-Archive-Audit/1.0","Accept":"application/json"})
  with urllib.request.urlopen(req,timeout=14) as res:
   b=res.read(350001);r["http_status"]=res.status
  if len(b)>350000:raise ValueError("Bounded read exceeded")
  r["sha256"]=hashlib.sha256(b).hexdigest();r["response_bytes"]=len(b)
  (BASE/(name+".response")).write_bytes(b)
  j=json.loads(b)
  if name.startswith("ia_available"):
   a=j.get("archived_snapshots",{}).get("closest",{})
   r["classification"]="SNAPSHOT_METADATA_ONLY" if a.get("available") else "NO_ARCHIVED_SNAPSHOT"
   r["snapshot"]=a
  else:
   count=max(0,len(j)-1) if isinstance(j,list) else 0
   r["matching_url_count"]=count
   r["classification"]="CDX_LIST_ONLY_NO_SERIES_VERIFIED" if count else "NO_CDX_MATCH"
   r["matched_urls"]=j[1:9] if isinstance(j,list) else []
 except Exception as e:
  r["classification"]="REMOTE_QUERY_FAILED_NOT_PROOF_OF_ABSENCE"
  r["error"]=str(e)[:300]
 return r

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 results=list(pool.map(get,tasks))
manifest={
 "conclusion":"THIS_AUDIT_DOES_NOT_RECOVER_OR_VERIFY_NATIVE_2020_IODA_SIGNAL_SERIES",
 "archives":["Internet Archive Wayback Availability API","Internet Archive CDX Search API"],
 "request_range_utc":["2020-01-08T00:00:00Z","2020-01-12T00:00:00Z"],
 "results":results,
 "caveat":"An archived URL or UI page does NOT authenticate a numerical bgp or ping-slash24 series; timestamps, metadata, value arrays, origin and licence must be independently checked.",
}
(BASE/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print(json.dumps([{"name":v["name"],"classification":v["classification"],"matches":v.get("matching_url_count"),"snapshot":v.get("snapshot",{}).get("url"),"error":v.get("error")} for v in results],indent=2))
