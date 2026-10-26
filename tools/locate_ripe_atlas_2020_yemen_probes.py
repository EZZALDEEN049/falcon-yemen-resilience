#!/usr/bin/env python3
"""Find source-native RIPE Atlas 2020 built-in ICMP ping data from historical
Yemeni probes (not IODA or all-of-Yemen representativeness).
"""
import concurrent.futures,datetime as dt,hashlib,json,urllib.parse,urllib.request
from pathlib import Path
O=Path("_artifacts/2020_yemeni_ripe_atlas_source_probe_audit");O.mkdir(parents=True,exist_ok=True)
A=1578441600;B=1578873600
ASN_PROBES={30873:[13655,14138,14148,14176,26226],12486:[14193,17661]}
BUILTINS={1001:"k.root-servers.net",1009:"a.root-servers.net",1010:"b.root-servers.net"}
tasks=[(asn,pid,msm) for asn,prs in ASN_PROBES.items() for pid in prs for msm in BUILTINS]
def test(task):
 asn,probe,msm=task
 url=f"https://atlas.ripe.net/api/v2/measurements/{msm}/results/?"+urllib.parse.urlencode({"start":A,"stop":B-1,"probe_ids":probe})
 row={"catalog_asn":asn,"probe_id":probe,"built_in_measurement_id":msm,"built_in_target":BUILTINS[msm],"source_url":url}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Falcon-2020-source-probe-historical-audit/1.0","Accept":"application/json"}),timeout=50) as resp:
   raw=resp.read(10000000)
  row["response_sha256"]=hashlib.sha256(raw).hexdigest()
  data=json.loads(raw)
  if not isinstance(data,list):raise RuntimeError("API must return JSON result array")
  valid=[x for x in data if isinstance(x.get("timestamp"),(int,float)) and A<=x["timestamp"]<B and x.get("prb_id")==probe]
  n_reply=sum(1 for x in valid if isinstance(x.get("rcvd"),int) and x["rcvd"]>0)
  n_zero=sum(1 for x in valid if x.get("rcvd")==0)
  row.update(observations_in_2020_window=len(valid),with_reply=n_reply,with_no_reply=n_zero,
   min_utc=dt.datetime.fromtimestamp(min(x["timestamp"] for x in valid),dt.timezone.utc).isoformat() if valid else None,
   max_utc=dt.datetime.fromtimestamp(max(x["timestamp"] for x in valid),dt.timezone.utc).isoformat() if valid else None,
   source_ips=list(sorted(set(x.get("from") for x in valid if x.get("from"))))[:5])
 except Exception as e:row["error"]=repr(e)
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: rows=list(ex.map(test,tasks))
for x in rows:print(json.dumps({"asn":x["catalog_asn"],"probe":x["probe_id"],"msm":x["built_in_measurement_id"],"rows":x.get("observations_in_2020_window"),"reply":x.get("with_reply"),"zero":x.get("with_no_reply"),"error":x.get("error")}),flush=True)
(O/"probe_source_audit.json").write_text(json.dumps({"note":"Original public RIPE Atlas built-in ping results; catalog ASN may not prove a probe's 2020 AS assignment; validate source IP historical ASN before strong classification.","rows":rows},indent=2))
