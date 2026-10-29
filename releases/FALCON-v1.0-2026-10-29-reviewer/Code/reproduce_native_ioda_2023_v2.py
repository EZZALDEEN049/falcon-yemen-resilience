#!/usr/bin/env python3
"""Reproduce supplementary Table 7 (AS30873/AS12486) from untouched native IODA JSON.

Usage:
  python reproduce_native_ioda_2023_v2.py --source-zip github-actions-artifact-12531758698.zip
No third-party libraries are required. This is NOT a 2020 route reconstruction.
"""
import argparse
import csv
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
from statistics import median,mean
from zipfile import ZipFile

UTC=timezone.utc
EPOCH=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp())
W={
 'baseline':(EPOCH('2023-11-09T00:00:00Z'),EPOCH('2023-11-10T00:00:00Z')),
 'event':(EPOCH('2023-11-10T00:10:00Z'),EPOCH('2023-11-10T04:45:00Z')),
 'post':(EPOCH('2023-11-10T05:00:00Z'),EPOCH('2023-11-11T00:00:00Z'))
}

def stats(series,win):
 start,end=W[win]; step=series['step']; ts0=series['from']
 assert isinstance(step,int) and step>0 and isinstance(ts0,int)
 samples=[float(v) for i,v in enumerate(series['values'])
          if isinstance(v,(int,float)) and not isinstance(v,bool) and start<=ts0+i*step<end]
 expected=(end-start+step-1)//step
 if len(samples)!=expected:
  raise ValueError(f'Incomplete {win} samples: {len(samples)}/{expected}')
 return {'n':len(samples),'expected':expected,'median':median(samples),'mean':mean(samples)}

def main(path, out):
 rows=[]
 with ZipFile(path) as arc:
  for asn in ('30873','12486'):
   name=f'FALCON_2023_asn_{asn}.json'; raw=arc.read(name)
   d=json.loads(raw)
   if d.get('error') or not isinstance(d.get('data'),list):
    raise ValueError(f'Bad raw response: {name}')
   all_series=[x for group in d['data'] if isinstance(group,list) for x in group if isinstance(x,dict)]
   for datasource in ('bgp','ping-slash24'):
    found=[x for x in all_series if x.get('datasource')==datasource and x.get('entityType')=='asn' and str(x.get('entityCode'))==asn]
    if len(found)!=1: raise ValueError(f'No unique series for AS{asn}/{datasource}')
    s=found[0]
    st={k:stats(s,k) for k in W}
    ret=100*st['event']['median']/st['baseline']['median']
    rows.append({'ASN':asn,'datasource':datasource,'source_json':name,'sha256':hashlib.sha256(raw).hexdigest(),
      'cadence_seconds':s['step'],'baseline_median':st['baseline']['median'],
      'event_median':st['event']['median'],'median_retention_pct':ret,
      'event_n':st['event']['n'],'baseline_n':st['baseline']['n'],'post_n':st['post']['n']})
 expected={('30873','bgp'):40.27149321266968,('30873','ping-slash24'):60.0,
           ('12486','bgp'):100.0,('12486','ping-slash24'):100.0}
 assert len(rows)==4
 for row in rows:assert abs(row['median_retention_pct']-expected[row['ASN'],row['datasource']])<1e-8
 out.parent.mkdir(parents=True,exist_ok=True)
 with out.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print('Verified original raw IODA JSON and independently reproduced all 4 retention values.')
 print('Output:',out)

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--source-zip',required=True,type=Path)
 p.add_argument('--out',type=Path,default=Path('native_2023_reproduced.csv'))
 a=p.parse_args();main(a.source_zip,a.out)
