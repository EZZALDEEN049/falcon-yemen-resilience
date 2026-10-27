#!/usr/bin/env python3
"""Audit historical published IODA raster provenance; no raw IODA/causality claims."""
import datetime as dt, hashlib, json, os, pathlib, time, urllib.request, urllib.error
from PIL import Image
ROOT=pathlib.Path("_artifacts/ioda2020_publisher_raster");ROOT.mkdir(parents=True,exist_ok=True)
SOURCES={
 "AS30873":"jan-910-yemen-as30783-ioda.png",
 "AS12486":"jan-910-yemen-as12486-ioda.png",
}
BASES=[
 "https://internetdisruption.report/wp-content/uploads/2020/02/",
 "https://internetdisruptionreport.home.blog/wp-content/uploads/2020/02/",
 "https://i0.wp.com/internetdisruption.report/wp-content/uploads/2020/02/",
 "https://i1.wp.com/internetdisruption.report/wp-content/uploads/2020/02/",
]
EXPECTED={"active":(31,120,180),"bgp":(51,160,44)}
SPEC={"x_min":112,"x_max":1779,"y_top":240,"y_zero":632,"pixels_per_unit":252}
def inspect(path):
  im=Image.open(path);im.load();rgb=im.convert("RGB")
  w,h=im.size
  results={"width":w,"height":h,"format":im.format,"calibration_as_given_in_old_bundle":SPEC}
  if w<=1779 or h<=632:
    results["status"]="FAIL_SOURCE_IMAGE_TOO_SMALL_FOR_ORIGINAL_CALIBRATION"
    return results
  counts={};columns={}
  pix=rgb.load()
  for key,color in EXPECTED.items():
    n=0;xs=0
    for x in range(112,1780):
      hit=0
      for y in range(240,633):
        r,g,b=pix[x,y]
        if max(abs(r-color[0]),abs(g-color[1]),abs(b-color[2]))<=2:hit+=1
      n+=hit;xs+=int(hit>0)
    counts[key]=n;columns[key]=xs
  results["exact_RGB_hit_counts"]=counts;results["x_columns_with_line"]=columns
  results["status"]="PASS_CALIBRATION_PIXEL_GEOMETRY_ONLY" if min(columns.values())>=100 else "FAIL_RGB_OR_CALIBRATION_GEOMETRY"
  return results
report={"article":"https://internetdisruption.report/2020/02/23/internet-disruption-report-january-2020/",
 "event":"January 9, 2020","kind":"publisher_raster_retrieval_and_calibration_only",
 "run_utc":dt.datetime.now(dt.timezone.utc).isoformat(),"github_run_id":os.getenv("GITHUB_RUN_ID"),"results":{},"raw_ioda2020_recovered":False}
for asn,file in SOURCES.items():
  result={"reported_article_caption":asn,"publisher_filename":file,"attempts":[]}
  if asn=="AS30873":result["warning"]="Publisher name as30783 differs from article caption AS30873; this is not proof of wrong plotted AS."
  for base in BASES:
    for suffix in ["","?w=2048","?w=1024"]:
      url=base+file+suffix
      attempt={"url":url}
      try:
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; FALCON-Research-Audit/1.0; journal source verification)","Accept":"image/png,image/*;q=0.9,*/*;q=0.1"})
        with urllib.request.urlopen(req,timeout=28) as r:
          buf=r.read(7_000_001);ct=r.headers.get("content-type");effective=r.geturl();status=r.status
        attempt.update(http_status=status,content_type=ct,redirect_target=effective,bytes=len(buf))
        if len(buf)>7_000_000 or not buf.startswith(b"\x89PNG\r\n\x1a\n"):raise ValueError("No normal bounded PNG response")
        name=ROOT/(asn+"__"+str(len(result["attempts"]))+".png");name.write_bytes(buf)
        attempt.update(sha256=hashlib.sha256(buf).hexdigest(),image_file=name.name)
        attempt.update(inspect(name))
        result["attempts"].append(attempt)
        if attempt["status"]=="PASS_CALIBRATION_PIXEL_GEOMETRY_ONLY":break
      except Exception as e:
        attempt.update(status="RETRIEVAL_FAILED",error=str(e)[:350])
        result["attempts"].append(attempt)
    if any(x.get("status")=="PASS_CALIBRATION_PIXEL_GEOMETRY_ONLY" for x in result["attempts"]):break
  valid=[a for a in result["attempts"] if a.get("status")=="PASS_CALIBRATION_PIXEL_GEOMETRY_ONLY"]
  result["final_gate"]="RASTER_GEOMETRY_PASS_PROVENANCE_SOURCE_URL_LOGGED" if valid else "NOT_CALIBRATION_VERIFIED"
  result["image_available"]=any("sha256" in a for a in result["attempts"])
  report["results"][asn]=result
  print(asn,result["final_gate"],len(result["attempts"]),flush=True)
(ROOT/"source_raster_audit.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
# Audit always succeeds as a workflow for producing a negative result; the source validity is separate.
