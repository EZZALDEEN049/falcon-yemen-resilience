#!/usr/bin/env python3
"""Optional November 2023 IODA API re-fetch + native JSON audit. Distinct from 2020.

A historical API may be unavailable or return revised data. In that case do
not assert validation; original source response access remains pending.
"""
import argparse, hashlib, io, json, subprocess, sys, urllib.request, zipfile
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('--manifest',type=Path,required=True)
 p.add_argument('--reproduce-script',type=Path,required=True)
 p.add_argument('--private-working-dir',type=Path,default=Path('reviewer_ioda2023_private'))
 p.add_argument('--preflight',action='store_true')
 p.add_argument('--author-archived-source-zip',type=Path,help='For an authorized internal audit only; source JSON must not be republished')
 a=p.parse_args();d=json.loads(a.manifest.read_text(encoding='utf8'))
 assert set(d)=={'30873','12486'}
 for asn,x in d.items():
  assert x['url'].startswith('https://api.ioda.inetintel.cc.gatech.edu/v2/signals/raw/asn/'+asn+'?')
  assert len(x['sha256'])==64
 assert a.reproduce_script.is_file()
 print('PASS IODA2023 audit plan: 2 historical API requests; original response SHA-256 required')
 if a.preflight:return
 a.private_working_dir.mkdir(parents=True,exist_ok=True)
 zip_path=a.private_working_dir/'source_original_2023_PRIVATE.zip'
 if a.author_archived_source_zip:
  # Original author-held archive: no re-fetch or publicity claim.
  zip_path.write_bytes(a.author_archived_source_zip.read_bytes())
 else:
  with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
   for asn,x in d.items():
    req=urllib.request.Request(x['url'],headers={'User-Agent':'FALCON-academic-2023-ioda-audit/1.0'})
    with urllib.request.urlopen(req,timeout=100) as resp:raw=resp.read()
    if hashlib.sha256(raw).hexdigest()!=x['sha256']:raise RuntimeError('API returned different/unverifiable original historical JSON AS'+asn)
    z.writestr('FALCON_2023_asn_'+asn+'.json',raw)
 with zipfile.ZipFile(zip_path) as z:
  for asn,x in d.items():
   raw=z.read('FALCON_2023_asn_'+asn+'.json')
   if hashlib.sha256(raw).hexdigest()!=x['sha256']:raise RuntimeError('IODA2023 source JSON checksum mismatch AS'+asn)
 subprocess.run([sys.executable,str(a.reproduce_script.absolute()),'--source-zip',str(zip_path.absolute()),'--out',str((a.private_working_dir/'IODA2023_reproduced_4values.csv').absolute())],check=True)
 print('PASS source-original IODA2023 four values (separate event). Original JSON is not licensed for blanket redistribution.')
if __name__=='__main__':main()
