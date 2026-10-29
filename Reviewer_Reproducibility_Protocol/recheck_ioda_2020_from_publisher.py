#!/usr/bin/env python3
"""Fetch/check original third-party 2020 PNGs *locally*; never redistribute them."""
import argparse, hashlib, json, subprocess, sys, urllib.request
from pathlib import Path

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--manifest',type=Path,required=True)
 p.add_argument('--code-dir',type=Path,required=True,help='Code/ from tagged v1.0.1 software')
 p.add_argument('--work-dir',type=Path,default=Path('reviewer_private_ioda2020'))
 p.add_argument('--preflight',action='store_true')
 p.add_argument('--offline-image-dir',type=Path,help='Optional locally provided source PNG directory; file names AS30873.png and AS12486.png')
 a=p.parse_args();j=json.loads(a.manifest.read_text(encoding='utf8'))
 ims={x['caption_as']:x for x in j['images']}
 assert set(ims)=={'AS30873','AS12486'}
 for k,v in ims.items():assert len(v['sha256'])==64 and v['size_px']==[1840,874] and v['publisher_url'].startswith('https://internetdisruption.report/')
 for f in ['recheck_ioda2020_original_pngs.py','digitization_sensitivity.py']:
  if not (a.code_dir/f).exists():raise FileNotFoundError(a.code_dir/f)
 print('PASS IODA2020 source-link/sha preflight: 2 third-party PNG source URLs and exact expected hashes')
 if a.preflight:return
 dest=a.work_dir/'source_images_PRIVATE_do_not_upload'; dest.mkdir(parents=True,exist_ok=True)
 for k,v in ims.items():
  target=dest/(k+'.png')
  if a.offline_image_dir:
   data=(a.offline_image_dir/(k+'.png')).read_bytes(); target.write_bytes(data)
  elif not target.exists():
   req=urllib.request.Request(v['publisher_url'],headers={'User-Agent':'FALCON-academic-source-audit/1.0'})
   with urllib.request.urlopen(req,timeout=60) as response:
    target.write_bytes(response.read())
  if sha(target)!=v['sha256']:raise RuntimeError('Original publisher SHA mismatch for '+k)
  from PIL import Image
  with Image.open(target) as image:
   if list(image.size)!=v['size_px']:raise RuntimeError('Original PNG geometry mismatch '+k)
  print('PASS IODA2020 unchanged published PNG bytes '+k)
 out=a.work_dir/'derived_local_outputs';out.mkdir(parents=True,exist_ok=True)
 subprocess.run([sys.executable,str((a.code_dir/'recheck_ioda2020_original_pngs.py').absolute()),'--as30873',str((dest/'AS30873.png').absolute()),'--as12486',str((dest/'AS12486.png').absolute()),'--out-dir',str(out.absolute())],check=True)
 # Original sensitivity script uses its own provenance path. Copy the *code* only,
 # then pass local original PNG at its documented private path (never include in a release).
 script=(a.code_dir/'digitization_sensitivity.py').read_text(encoding='utf8')
 pscript=a.work_dir/'sensitivity_private'/'digitization_sensitivity.py';pscript.parent.mkdir(parents=True,exist_ok=True);pscript.write_text(script)
 pp=pscript.parent/'provenance';pp.mkdir(exist_ok=True)
 (pp/'jan-9-10-yemen-AS30873-IODA.png').write_bytes((dest/'AS30873.png').read_bytes())
 csvpath=out/'IODA_2020_20250_source_raster_reproduced.csv'
 subprocess.run([sys.executable,str(pscript.absolute()),'--out-csv',str(csvpath.absolute()),'--out-json',str((out/'IODA_2020_20250_summary.json').absolute())],check=True)
 expected='fa9720246ec52edb6770c8637f52da260856908574fb490a4d49f0e825245e12'
 if sha(csvpath)!=expected:raise RuntimeError('Deterministic sensitivity full-grid checksum mismatch')
 print('PASS 20,250-setting raster-derived IODA2020 grid: exact expected SHA-256. PRIVATE publisher PNGs MUST NOT BE REUPLOADED.')
if __name__=='__main__':main()
