#!/usr/bin/env python3
"""Fail-closed native IODA CSV analysis (after official raw downloader has produced verified source files).
Never silently conflate 'active' and 'bgp', or count image columns as native samples.

Usage: python code/validate_native_ioda.py --csv raw_ioda/FALCON_2020_asn_30873.csv --out results/native_ioda_30873.json
"""
import argparse,csv,datetime as dt,json,math,statistics
from collections import defaultdict
from pathlib import Path
PRE=(dt.datetime(2020,1,8,0,tzinfo=dt.timezone.utc).timestamp(),dt.datetime(2020,1,9,8,30,tzinfo=dt.timezone.utc).timestamp())
ACUTE=(dt.datetime(2020,1,9,18,tzinfo=dt.timezone.utc).timestamp(),dt.datetime(2020,1,10,0,tzinfo=dt.timezone.utc).timestamp())
# Source-specific datasource identification must be inspected against actual API returned names before acceptance.
ALIASES={'bgp':('bgp','routeviews','ripe ris'), 'active':('active','ping','probing')}

def parse(csv_file):
    signal_points=defaultdict(list)
    with open(csv_file,encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    if not rows: raise ValueError('No native IODA rows; failing closed.')
    for r in rows:
        raw_name=r.get('signal','').lower().strip()
        candidates=[family for family,terms in ALIASES.items() if any(word in raw_name for word in terms)]
        if len(candidates)!=1: continue
        ts=float(r['timestamp']); value=float(r['value'])
        if not all(map(math.isfinite,(ts,value))) or ts < 1e9 or value < 0: raise ValueError('Malformed time/value')
        signal_points[candidates[0]].append((ts,value,raw_name))
    return signal_points

def analyze(csv_file, min_samples=12,min_hours_coverage=.7):
    points=parse(csv_file)
    report={'source':'NATIVE_IODA_CSV','csv':str(csv_file),'windows_utc':{'baseline':list(PRE),'acute':list(ACUTE)},'metrics':{},'release_approved':False}
    for family in ('bgp','active'):
        data=points.get(family,[])
        names=set(x[2] for x in data)
        if len(names)!=1: raise ValueError(f'Multiple or zero raw datasource names for {family}: {sorted(names)}; manual verification required')
        d={float(t):v for t,v,_ in data}
        if len(d)!=len(data): raise ValueError(f'Duplicate timestamps for {family}: must resolve explicitly')
        for label,(start,end) in [('baseline',PRE),('acute',ACUTE)]:
            sample=sorted((t,v) for t,v in d.items() if start <= t < end)
            if len(sample)<min_samples: raise ValueError(f'Insufficient {family}/{label} native samples: {len(sample)}')
            gaps=[sample[i+1][0]-sample[i][0] for i in range(len(sample)-1)]
            cadence=statistics.median(gaps)
            if not (cadence>0 and math.isfinite(cadence)): raise ValueError('Invalid sample interval')
            # Detect gapped time coverage; a median cadence is computed within each window.
            covered=sum(min(x,2*cadence) for x in gaps)+cadence
            coverage=min(1,covered/(end-start))
            if coverage<min_hours_coverage: raise ValueError(f'Insufficient time coverage for {family}/{label}: {coverage:.1%}')
            report['metrics'].setdefault(family,{})[label]={'n_samples':len(sample),'median':statistics.median(v for _,v in sample),'mean':statistics.mean(v for _,v in sample),'coverage_fraction_estimated':coverage,'datasource_name':next(iter(names))}
        pre=report['metrics'][family]['baseline']['median']
        if pre<=0: raise ValueError(f'Nonpositive baseline: {family}')
        report['metrics'][family]['retention_pct']=100*report['metrics'][family]['acute']['median']/pre
    report['gap_percentage_points']=report['metrics']['bgp']['retention_pct']-report['metrics']['active']['retention_pct']
    report['release_approved']=True
    report['note']='Cross-family normalized difference is descriptive; not a confidence interval or route-level survival measure.'
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--csv',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    result=analyze(a.csv)
    Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    Path(a.out).write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps(result,indent=2))
