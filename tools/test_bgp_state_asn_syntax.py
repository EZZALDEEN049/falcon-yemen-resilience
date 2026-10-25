#!/usr/bin/env python3
"""Test whether AS prefix notation vs numeric resource produces empty bgp-state responses."""
import concurrent.futures, datetime, hashlib,json,urllib.parse,urllib.request
from pathlib import Path
p=Path("_artifacts/bgp_state_resource_syntax");p.mkdir(parents=True,exist_ok=True)
checks=[
 ("asn_plain_2020","30873","2020-01-09T08:30:00"),
 ("asn_as_2020","AS30873","2020-01-09T08:30:00"),
 ("asn_plain_2023","30873","2023-11-10T00:30:00"),
 ("asn_as_2023","AS30873","2023-11-10T00:30:00"),
 ("known_prefix_2023","8.8.8.0/24","2023-11-10T00:30:00"),
 ("known_prefix_2024","140.78/16","2024-12-21T12:00:00"),
 ("known_ASN_2023","AS3333","2023-11-10T00:30:00")
]
def get(x):
 label,resource,t=x;url="https://stat.ripe.net/data/bgp-state/data.json?"+urllib.parse.urlencode({"resource":resource,"timestamp":t})
 out={"label":label,"resource":resource,"timestamp":t,"url":url}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"Academic-FALCON-2020-validation/1.0"}),timeout=28) as r:raw=r.read(10000000);out["http_status"]=r.status
  obj=json.loads(raw)
  d=obj.get("data",{})
  out.update(api_status=obj.get("status"),data_call_status=obj.get("data_call_status"),returned_resource=d.get("resource"),returned_timestamp=d.get("timestamp"),returned_nr_routes=d.get("nr_routes"),list_count=len(d.get("bgp_state",[])) if isinstance(d.get("bgp_state"),list) else None,sha256=hashlib.sha256(raw).hexdigest(),messages=obj.get("messages"))
  (p/(label+".json")).write_bytes(raw)
 except Exception as e:out["error"]=str(e)
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(get,checks))
(p/"manifest.json").write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
