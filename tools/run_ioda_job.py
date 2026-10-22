#!/usr/bin/env python3
"""Cloud orchestration: fetch, preserve sources, validate only when both families are recognized."""
import argparse,json,subprocess,sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--event',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
job=subprocess.run([sys.executable,'code/download_ioda_raw.py','--event',a.event,'--out',str(out)],capture_output=True,text=True)
(out/'console.log').write_text('stdout:\n'+job.stdout+'\nstderr:\n'+job.stderr[-10000:],encoding='utf8')
validations=[]
manifest_file=out/'manifest.json'
manifest=json.loads(manifest_file.read_text()) if manifest_file.exists() else {'successes':[],'failures':[{'error':'downloader produced no manifest'}]}
if a.event=='FALCON_2020':
  for entry in manifest['successes']:
    if entry['entity_type']!='asn' or entry['entity_code'] not in ('30873','12486'):continue
    csvfile=out/entry['csv']; outfile=out/f'native_ioda_{entry["entity_code"]}_validation.json'
    verify=subprocess.run([sys.executable,'code/validate_native_ioda.py','--csv',str(csvfile),'--out',str(outfile)],capture_output=True,text=True)
    validations.append({'asn':entry['entity_code'],'validated':verify.returncode==0,'error':None if verify.returncode==0 else verify.stderr[-3000:]})
(out/'validation_status.json').write_text(json.dumps({'event':a.event,'retrieval_successes':len(manifest['successes']),'retrieval_failures':len(manifest['failures']),'validation':validations,'warning':'Raw signal family names and IODA API schema still require author review. This is not causal/route-level validation.'},indent=2),encoding='utf8')
print((out/'validation_status.json').read_text())
if not manifest['successes'] or job.returncode!=0:sys.exit(2)
# Refuse green success if either target ASN is not fully validated for Jan 2020.
if a.event=='FALCON_2020' and (len(validations)!=2 or not all(x['validated'] for x in validations)):
  sys.exit(3)
if manifest['failures']:sys.exit(4)
