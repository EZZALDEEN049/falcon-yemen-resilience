#!/usr/bin/env python3
"""Verify live availability of source-native historical RIPE RIS A/W MRT feeds.

Critical: withdrawal records typically have no origin ASN. Keep ALL A/W messages
during sample extraction; an origin ASN filter would silently erase withdrawals.
This is a limited interval availability/decoder audit, NOT an event replay.
"""
from collections import Counter
import datetime as dt,gzip,hashlib,json,subprocess,sys
from pathlib import Path
from pybgpkit_parser import Parser
OUT=Path("_artifacts/2020_mrt_update_interval_test");OUT.mkdir(parents=True,exist_ok=True)
ROOT="https://data.ris.ripe.net/rrc00/2020.01/"
NAMES=[
 "updates.20200109.0855.gz",
 "updates.20200109.1755.gz",
 "updates.20200109.1800.gz",
 "updates.20200109.1805.gz",
 "updates.20200109.1810.gz",
 "updates.20200109.1815.gz"
]
report={"case":"Six sample 2020 source-native RRC00 update files; NOT continuous event coverage","samples":[],"complete":False}
try:
 for name in NAMES:
  url=ROOT+name;file=Path("/tmp")/name
  proc=subprocess.run(["curl","-fLsS","--retry","2","--retry-all-errors","--connect-timeout","15","--max-time","90","-o",str(file),url],capture_output=True,text=True)
  if proc.returncode:raise RuntimeError("DOWNLOAD FAILED "+name+" "+proc.stderr[-160:])
  size=file.stat().st_size
  if not 1000<size<100000000:raise RuntimeError("bad file size "+name+" "+str(size))
  sha=hashlib.sha256(file.read_bytes()).hexdigest()
  with gzip.open(file,"rb") as f:
   while f.read(1024*1024):pass
  count=Counter();targets=Counter();origin_unknown_by_type=Counter()
  for batch in Parser(url=str(file)).iter_tuple_batches(["elem_type","peer_ip","peer_asn","prefix","origin_asns"],batch_size=10000):
   for etype,ip,peer_asn,prefix,origins in batch:
    kind=str(etype).upper()
    if kind in ("A","ANNOUNCE","ANNOUNCEMENT"):tag="announcement"
    elif kind in ("W","WITHDRAW","WITHDRAWAL"):tag="withdrawal"
    else:raise RuntimeError("Unknown update element type "+kind)
    count[tag]+=1
    if not (ip and peer_asn and prefix):raise RuntimeError("missing peer identity "+name)
    if not origins:origin_unknown_by_type[tag]+=1
    if tag=="announcement" and origins and len(origins)==1 and int(origins[0]) in (30873,12486):
     targets[str(int(origins[0]))]+=1
  if not count["announcement"] or not count["withdrawal"]:raise RuntimeError("Missing A/W control in "+name)
  row={"url":url,"sha256":sha,"bytes":size,"gzip_crc":"verified","elements":dict(count),"target_origin_announcement_rows":dict(targets),"no_origin_by_element_type":dict(origin_unknown_by_type)}
  report["samples"].append(row)
  print(json.dumps({"name":name,"A":count["announcement"],"W":count["withdrawal"],"AS_targets":dict(targets)}),flush=True)
 report["complete"]=len(report["samples"])==len(NAMES)
finally:
 (OUT/"audit.json").write_text(json.dumps(report,indent=2),encoding="utf8")
if not report["complete"]:sys.exit("Did not validate every sample update interval")
