#!/usr/bin/env python3
"""Forensic capture of IODA 2020 event-signal JSON and adjacent raw-series samples.
Never classify event-specific indicators as original raw BGP/ping observations.
"""
from pathlib import Path
import datetime as dt, json,urllib.parse,urllib.request,hashlib
O=Path("_artifacts/ioda_2020_forensic");O.mkdir(parents=True,exist_ok=True)
start=int(dt.datetime(2020,1,8,tzinfo=dt.timezone.utc).timestamp());end=int(dt.datetime(2020,1,12,tzinfo=dt.timezone.utc).timestamp())
base="https://api.ioda.inetintel.cc.gatech.edu/v2"
for name,path in [
("event_asn_30873","/signals/events/asn/30873"),
("event_asn_12486","/signals/events/asn/12486"),
("event_country_YE","/signals/events/country/YE"),
("raw_asn_30873","/signals/raw/asn/30873"),
("raw_asn_12486","/signals/raw/asn/12486")
]:
 url=base+path+"?"+urllib.parse.urlencode({"from":start,"until":end})
 r={"case":name,"url":url}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"IODA-2020-source-provenance-research/1.0","Accept":"application/json"}),timeout=25) as response:
   raw=response.read(2_000_001);r["http_status"]=response.status
  if len(raw)>2_000_000: raise ValueError("response too large")
  (O/(name+".json")).write_bytes(raw)
  j=json.loads(raw);r["sha256"]=hashlib.sha256(raw).hexdigest()
  r["keys"]=list(j.keys()) if isinstance(j,dict) else []
  d=j.get("data") if isinstance(j,dict) else None
  r["data_type"]=type(d).__name__
  if isinstance(d,list):
   r["groups"]=len(d);r["group_counts"]=[len(v) if isinstance(v,list) else None for v in d]
   rows=[x for v in d if isinstance(v,list) for x in v if isinstance(x,dict)]
   r["metadata_sample"]=[{k:x.get(k) for k in ("datasource","entityType","entityCode","from","until","step","signal","start","timestamp","values") if k in x and k!="values"} for x in rows[:20]]
   r["series_lengths"]=[len(x.get("values",[])) if isinstance(x.get("values"),list) else None for x in rows[:20]]
   r["all_datasources"]=sorted({str(x.get("datasource")) for x in rows})
 except Exception as e:r["error"]=str(e)[:500]
 (O/(name+".meta.json")).write_text(json.dumps(r,indent=2))
 print(json.dumps({"case":name,"response":r.get("http_status"),"groups":r.get("group_counts"),"sources":r.get("all_datasources"),"error":r.get("error")},ensure_ascii=False))
