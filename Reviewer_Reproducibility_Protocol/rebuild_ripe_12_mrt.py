#!/usr/bin/env python3
"""RIPE RIS on-demand source-native reviewer reconstruction; no source archive redistribution.

Requires source-owned official compressed RIBs and pybgpkit-parser. We have not
executed the full ~3.8-GB original-source download/reparse in this environment.
The --preflight path exercises manifests and instructions without network access.
"""
import argparse, csv, gzip, hashlib, json, shutil, subprocess, sys, urllib.request
from pathlib import Path
from urllib.parse import urlparse

COLLECTORS = ('rrc00','rrc01','rrc10')
WINDOWS = {'event': ('2020-01-09T08:00:00Z','2020-01-10T00:00:00Z'),
           'reference': ('2020-01-02T08:00:00Z','2020-01-03T00:00:00Z')}

def hexdigest(p):
    d=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''): d.update(b)
    return d.hexdigest()

def check(p,info):
    if not p.is_file(): raise FileNotFoundError(str(p))
    if p.stat().st_size != info['bytes']:raise ValueError('BYTES mismatch '+str(p))
    if hexdigest(p).lower() != info['sha256'].lower():raise ValueError('SHA256 mismatch '+str(p))
    with gzip.open(p,'rb') as f:
        for _ in iter(lambda:f.read(4*1024*1024),b''):pass
    return str(p)

def download(info,p):
    if p.exists(): return
    p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+'.partial');tmp.unlink(missing_ok=True)
    try:
        req=urllib.request.Request(info['url'],headers={'User-Agent':'FALCON-academic-reviewer-source-rebuild/1.0'})
        with urllib.request.urlopen(req,timeout=180) as src, tmp.open('wb') as dest:
            while True:
                b=src.read(4*1024*1024)
                if not b:break
                dest.write(b)
        check(tmp,info)
        tmp.replace(p)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise

def row_count_check(out_dir,expected,period):
    p=out_dir/'BGP_2020_unit_sensitivity_summary.csv'
    with p.open(newline='',encoding='utf8') as f: rows=list(csv.DictReader(f))
    assert len(rows)==6, ('six collector/AS groups required',rows)
    for x in rows:
        k=(x['collector'],str(x['origin_as']),period)
        if k not in expected:raise RuntimeError('Unexpected group '+str(k))
        a=expected[k]
        observations={'initial_rows':'initial_origin_rows','eligible':'eligible','retained':'retained','comparable':'comparable','changed':'changed'}
        for akey,bkey in observations.items():
            if int(a[akey])!=int(x[bkey]):
                raise RuntimeError(f'SOURCE RECONSTRUCTION DIFFERENCE {k} {akey}: new={x[bkey]}, archived={a[akey]}. DO NOT CLAIM SUCCESS. Inspect parser, peer census, AS_PATH semantics and duplicate policy.')
    print('PASS six source-native collector/AS group count comparisons for',period)
    return rows

def fixed_key_check(outroot,expected):
    def read(w):
        p=outroot/w/'BGP_2020_peer_prefix_records.csv'
        with p.open(newline='',encoding='utf8') as f:return list(csv.DictReader(f))
    data={w:read(w) for w in WINDOWS}
    for k,a in expected.items():
        collector,asn=k
        group={}
        for w,rows in data.items():
            subset={ (r['peer_asn'],r['peer_ip'],r['prefix']): int(r['neighbor_changed'])
                for r in rows if r['collector']==collector and r['origin_as']==asn and int(r['neighbor_comparable'])==1 }
            group[w]=subset
        common=set(group['event'])&set(group['reference'])
        ev=sum(group['event'][k] for k in common)
        ref=sum(group['reference'][k] for k in common)
        if len(common)!=int(a['common_comparable_peer_prefixes']):
            raise RuntimeError(f'FIXED COHORT mismatch {k}: {len(common)} vs {a["common_comparable_peer_prefixes"]}')
        if common:
            diff=100*(ev-ref)/len(common)
            if abs(diff-float(a['common_key_delta_pp']))>1e-8:
                raise RuntimeError(f'FIXED COHORT delta mismatch {k}: {diff} vs {a["common_key_delta_pp"]}')
    print('PASS six independent fixed-key intersection checks (each window reconstructed from original RIBs)')

def main():
    a=argparse.ArgumentParser()
    a.add_argument('--manifest',required=True,type=Path,help='JSON with six collector/window pairs and two RIB entries per pair')
    a.add_argument('--expected-s14',required=True,type=Path)
    a.add_argument('--expected-s15',required=True,type=Path)
    a.add_argument('--canonical-parser',required=True,type=Path,help='File Code/rebuild_2020_peer_prefix.py from software tag v1.0.1')
    a.add_argument('--work-dir',type=Path,default=Path('reviewer_ripe_reconstruction'))
    a.add_argument('--preflight',action='store_true',help='Offline test only: no download and no parsing')
    a.add_argument('--verify-only',action='store_true',help='All original RIBs must already exist; do not fetch')
    args=a.parse_args();pairs=json.loads(args.manifest.read_text(encoding='utf8'))
    seen={};
    for r in pairs:
        c,w=r['collector'],r['period']
        if c not in COLLECTORS or w not in WINDOWS or (c,w) in seen:raise ValueError('Unexpected/duplicate collector-window '+str((c,w)))
        seen[c,w]=r
        for key,t in [('first',WINDOWS[w][0]),('last',WINDOWS[w][1])]:
            f=r[key];url=f['url'];name=urlparse(url).path.rsplit('/',1)[-1]
            if f['time_utc']!=t or urlparse(url).hostname!='data.ris.ripe.net' or f'{c}/2020.01/{name}' not in url:raise ValueError('Source URL/time inconsistent '+url)
            if len(f['sha256'])!=64 or not isinstance(f['bytes'],int) or f['bytes']<100000000:raise ValueError('Missing original source digest/size')
    assert len(seen)==6,'Exactly six collector/window input pairs required'
    with args.expected_s14.open(newline='',encoding='utf8') as f:sumrows=list(csv.DictReader(f))
    with args.expected_s15.open(newline='',encoding='utf8') as f:fixrows=list(csv.DictReader(f))
    expected={(x['collector'],x['asn'],x['period']):x for x in sumrows}
    fixed={(x['collector'],x['asn']):x for x in fixrows}
    assert len(expected)==12 and len(fixed)==6
    assert args.canonical_parser.is_file()
    size=sum(pair[key]['bytes'] for pair in pairs for key in ('first','last'))
    print(f'PASS manifest preflight: 12 official RIPE RIB source URLs, {size:,} compressed bytes total, six pairs; expected 12 group rows and six common-key contrasts')
    if args.preflight:return
    sourcebase=args.work_dir/'original_RIPE_downloads'
    for (c,w),row in sorted(seen.items()):
        for key in ('first','last'):
            info=row[key];p=sourcebase/c/info['url'].rsplit('/',1)[-1]
            if not p.exists() and not args.verify_only:download(info,p)
            check(p,info)
            print(f'PASS source SHA256/bytes/gzip {c} {w} {key}',flush=True)
    out=args.work_dir/'reconstructed'
    for w in WINDOWS:
        csvpath=args.work_dir/(w+'_six_RIB_manifest.csv');csvpath.parent.mkdir(parents=True,exist_ok=True)
        with csvpath.open('w',encoding='utf8',newline='') as f:
            wri=csv.DictWriter(f,fieldnames=['collector','timestamp_UTC','original_compressed_bytes','SHA256_as_reported','source_URL']);wri.writeheader()
            for c in COLLECTORS:
                x=seen[c,w]
                for key in ('first','last'):
                    info=x[key];wri.writerow(dict(collector=c,timestamp_UTC=info['time_utc'],original_compressed_bytes=info['bytes'],SHA256_as_reported=info['sha256'],source_URL=info['url']))
        result=out/w
        subprocess.run([sys.executable,str(args.canonical_parser.absolute()),'--input-dir',str(sourcebase.absolute()),'--manifest',str(csvpath.absolute()),'--output-dir',str(result.absolute())],check=True)
        row_count_check(result,expected,w)
    fixed_key_check(out,fixed)
    print('PASS SOURCE-NATIVE endpoint reconstruction; local output is for reviewer evaluation only and must not be republished absent source rights')
if __name__=='__main__':main()