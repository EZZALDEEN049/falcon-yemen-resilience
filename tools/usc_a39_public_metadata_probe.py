#!/usr/bin/env python3
"""Read public USC dataset *metadata only*, not protected Trinocular data."""
from pathlib import Path
import hashlib,json,urllib.request,re
O=Path("_artifacts/usc_2020_public_readme");O.mkdir(parents=True,exist_ok=True)
datasets=[
 "internet_outage_adaptive_a39all-20200101",
 "internet_outage_adaptive_a39_supplement-20200101",
]
results=[]
for name in datasets:
 url=f"https://ant.isi.edu/datasets/readmes/{name}.README.txt"
 row={"name":name,"metadata_url":url}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"academic-trinocular-provenance-check/1.0"})
  with urllib.request.urlopen(req,timeout=25) as resp:
   raw=resp.read(100000)
   row["http_status"]=resp.status
  if len(raw)>=100000:raise RuntimeError("unexpected public README size")
  text=raw.decode("utf-8",errors="replace")
  row["readme_bytes"]=len(raw);row["readme_sha256"]=hashlib.sha256(raw).hexdigest()
  lines=text.splitlines()
  terms=["data/","outagedownup","outages.fsdb","supplement","asn","geo","route","mapping","format","fsdb","2020","download","README","period"]
  hits=[]
  for i,l in enumerate(lines):
   if any(t.lower() in l.lower() for t in terms):
    hits.append({"line":i+1,"text":l[:240]})
  row["metadata_excerpts"]=hits[:85]
 except Exception as e:row["error"]=repr(e)
 results.append(row)
 print(json.dumps({"name":name,"status":row.get("http_status"),"sha":row.get("readme_sha256"),"error":row.get("error"),"snippets":row.get("metadata_excerpts",[])[:45]},ensure_ascii=False),flush=True)
(O/"metadata_public_readmes.json").write_text(json.dumps(results,indent=2))
