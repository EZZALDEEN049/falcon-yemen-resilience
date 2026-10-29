#!/usr/bin/env python3
"""Explicit, checksum-gated download of six historical RIPE RIS RIBs.
Large downloads require network access and a few GB of free disk. Not run in
this sandbox; this tool never creates synthetic empirical rows.
"""
import argparse,csv,gzip,hashlib,urllib.request,sys
from pathlib import Path

def verify(p,size,sha):
 if p.stat().st_size!=size:raise RuntimeError('Size mismatch '+str(p))
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
 if h.hexdigest().lower()!=sha.lower():raise RuntimeError('SHA256 mismatch '+str(p))
 with gzip.open(p,'rb') as f:
  while f.read(4*1024*1024):pass
 return h.hexdigest()

p=argparse.ArgumentParser();p.add_argument('--manifest',type=Path,required=True);p.add_argument('--out-dir',type=Path,required=True);p.add_argument('--verify-only',action='store_true')
a=p.parse_args()
with a.manifest.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
if len(rows)!=6:raise RuntimeError('Exactly six original RIB entries are required')
for r in rows:
 rrc=r['collector']; u=r['source_URL']; target=a.out_dir/rrc/u.rsplit('/',1)[-1]; target.parent.mkdir(parents=True,exist_ok=True)
 if not target.exists() and not a.verify_only:
  req=urllib.request.Request(u,headers={'User-Agent':'FALCON-reproducibility-research/1.0'})
  temp=target.with_name(target.name+'.partial')
  with urllib.request.urlopen(req,timeout=120) as src, temp.open('wb') as dst:
   while chunk:=src.read(4*1024*1024):dst.write(chunk)
  temp.rename(target)
 if not target.exists():raise FileNotFoundError('Original source missing: '+str(target))
 print(rrc,target.name,verify(target,int(r['original_compressed_bytes']),r['SHA256_as_reported']),flush=True)
print('PASS: all six historical RIB gzip CRC and source SHA256 files verified')
