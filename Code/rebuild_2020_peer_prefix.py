#!/usr/bin/env python3
"""Source-native, SHA-gated, per-peer-per-prefix two-RIB analysis.

Requires original RIPE RIS 2020 RIBs. This script does NOT claim that archived
aggregate audit JSON are the primary MRT data. Does not infer cable cause or
independent data-plane reachability. Supports all three RRCs and both origins.

Install: pip install pybgpkit-parser
Run: python Code/rebuild_2020_peer_prefix.py --input-dir /path/to/mrt \
      --manifest Supplement/BGP_RIB_original_hash_manifest_from_authors_audit.csv \
      --output-dir /path/to/results
Run synthetic unit tests: python Code/rebuild_2020_peer_prefix.py --self-test
"""
import argparse,csv,gzip,hashlib,json,statistics,sys
from collections import defaultdict
from pathlib import Path

ASNS=(30873,12486)
COLLECTORS=('rrc00','rrc01','rrc10')

def upstream(path,asn):
    parts=str(path or '').split()
    if not parts or any(not x.isdecimal() for x in parts) or int(parts[-1])!=asn:return None
    i=len(parts)-1
    while i>0 and parts[i-1]==parts[-1]:i-=1
    return parts[i-1] if i>0 else None

def digest_and_check(path, expected_sha, expected_bytes):
    if not path.is_file(): raise FileNotFoundError(str(path))
    if path.stat().st_size != expected_bytes: raise RuntimeError(f'Source file size mismatch: {path}')
    h=hashlib.sha256()
    with path.open('rb') as fp:
        for chunk in iter(lambda:fp.read(4*1024*1024),b''):h.update(chunk)
    if h.hexdigest().lower()!=expected_sha.lower():raise RuntimeError(f'Source SHA256 mismatch: {path}')
    with gzip.open(path,'rb') as fp:
        for _ in iter(lambda:fp.read(4*1024*1024),b''):pass
    return h.hexdigest()

def source_rib(file):
    try:from pybgpkit_parser import Parser
    except ImportError as e:raise RuntimeError('Install pybgpkit-parser before empirical run') from e
    peers=set(); count=0
    # Full-RIB peer census is independent of the two target origins.
    for batch in Parser(url=str(file)).iter_tuple_batches(['peer_asn','peer_ip'],batch_size=50000):
        for peer_asn,peer_ip in batch:
            if peer_asn and peer_ip:peers.add((int(peer_asn),str(peer_ip)))
            count+=1
    if count<10000 or len(peers)<20:raise RuntimeError('Insufficient full-RIB coverage')
    routes={asn:{} for asn in ASNS}
    columns=['peer_ip','peer_asn','prefix','as_path','origin_asns']
    for batch in Parser(url=str(file),filters={'origin_asns':','.join(map(str,ASNS))}).iter_tuple_batches(columns,batch_size=20000):
        for ip,asn,prefix,aspath,origins in batch:
            orig=[int(x) for x in (origins or [])]
            if len(orig)!=1 or orig[0] not in ASNS:continue
            if not ip or not asn or not prefix:raise RuntimeError('Missing route observer identity')
            peer=(int(asn),str(ip))
            if peer not in peers:raise RuntimeError('Target peer missing from full-RIB census')
            key=peer+(str(prefix),)
            if key in routes[orig[0]]:raise RuntimeError(f'Ambiguous duplicate peer-prefix: {key}')
            routes[orig[0]][key]=str(aspath or '')
    if any(not routes[a] for a in ASNS):raise RuntimeError('Empty historic target origin in RIB')
    return {'all_peers':peers,'routes':routes,'original_elements':count}

def make_rows(first,second,collector):
    records=[]
    alive=first['all_peers'] & second['all_peers']
    for asn in ASNS:
        pre=first['routes'][asn]; post=second['routes'][asn]
        for (peer_asn,peer_ip,prefix),path in pre.items():
            peer=(peer_asn,peer_ip)
            observed=peer in alive
            retained=observed and (peer_asn,peer_ip,prefix) in post
            a=upstream(path,asn) if retained else None
            b=upstream(post[(peer_asn,peer_ip,prefix)],asn) if retained else None
            comparable=retained and a is not None and b is not None
            records.append({'collector':collector,'origin_as':asn,'peer_asn':peer_asn,'peer_ip':peer_ip,'prefix':prefix,
              'peer_present_at_both_checkpoints':int(observed),'eligible':int(observed),
              'same_origin_retained':int(retained),'target_origin_absent_or_changed':int(observed and not retained),
              'initial_immediate_as':a or '', 'endpoint_immediate_as':b or '',
              'neighbor_comparable':int(comparable),
              'neighbor_changed':int(a!=b) if comparable else ''})
    return records

def aggregate(rows, keycols, name):
    groups=defaultdict(list)
    for r in rows:
        if r['neighbor_comparable']:
            groups[tuple(r[k] for k in keycols)].append(int(r['neighbor_changed']))
    out=[]
    for k,v in sorted(groups.items(),key=lambda z:tuple(map(str,z[0]))):
        item=dict(zip(keycols,k));item.update({'comparable_observations':len(v),'changed_observations':sum(v),
                  'fraction_changed':sum(v)/len(v),'any_changed':int(any(v)),'aggregation_unit':name})
        out.append(item)
    return out

def summarize(rows):
    summary=[]; prefix_rows=[];peer_rows=[]
    for rrc in COLLECTORS:
        for asn in ASNS:
            sub=[x for x in rows if x['collector']==rrc and x['origin_as']==asn]
            if not sub:continue
            pre=len(sub);eligible=sum(int(x['eligible']) for x in sub)
            kept=sum(int(x['same_origin_retained']) for x in sub)
            comparable=sum(int(x['neighbor_comparable']) for x in sub)
            changed=sum(int(x['neighbor_changed']) for x in sub if x['neighbor_comparable'])
            if not (eligible<=pre and kept<=eligible and comparable<=kept):raise AssertionError('Flow invariant')
            pr=aggregate(sub,['collector','origin_as','prefix'],'prefix')
            pe=aggregate(sub,['collector','origin_as','peer_asn','peer_ip'],'peer')
            prefix_rows+=pr;peer_rows+=pe
            item={'collector':rrc,'origin_as':asn,'initial_origin_rows':pre,'excluded_absent_end_peer':pre-eligible,
                'eligible':eligible,'retained':kept,'not_retained':eligible-kept,
                'unparsable_retained':kept-comparable,'comparable':comparable,'changed':changed,
                'change_pct':100*changed/comparable if comparable else None,
                'retention_pct':100*kept/eligible if eligible else None,
                'prefix_count_with_comparable':len(pr),'prefix_any_change':sum(z['any_changed'] for z in pr),
                'prefix_equal_mean_pct':100*statistics.mean(z['fraction_changed'] for z in pr) if pr else None,
                'prefix_equal_median_pct':100*statistics.median(z['fraction_changed'] for z in pr) if pr else None,
                'peer_count_with_comparable':len(pe),'peer_any_change':sum(z['any_changed'] for z in pe),
                'peer_equal_mean_pct':100*statistics.mean(z['fraction_changed'] for z in pe) if pe else None,
                'peer_equal_median_pct':100*statistics.median(z['fraction_changed'] for z in pe) if pe else None}
            for typ,gr in (('prefix',pr),('peer',pe)):
                fractions=sorted(z['fraction_changed'] for z in gr)
                for pct in (25,75):
                    if fractions:
                        v=(len(fractions)-1)*pct/100;j=int(v);weight=v-j
                        item[f'{typ}_q{pct}_pct']=100*(fractions[j]*(1-weight)+fractions[min(j+1,len(fractions)-1)]*weight)
            summary.append(item)
    # Optional like-for-like observer subset where one physical session saw both ASes.
    common=[]
    for rrc in COLLECTORS:
        rrows=[r for r in rows if r['collector']==rrc and r['neighbor_comparable']]
        peer_sets={a:{(r['peer_asn'],r['peer_ip']) for r in rrows if r['origin_as']==a} for a in ASNS}
        peers=peer_sets[ASNS[0]]&peer_sets[ASNS[1]]
        for a in ASNS:
            sub=[r for r in rrows if r['origin_as']==a and (r['peer_asn'],r['peer_ip']) in peers]
            common.append({'collector':rrc,'origin_as':a,'same_observers_for_two_ASes':len(peers),
                'matched_peer_prefix_records':len(sub),'changed':sum(r['neighbor_changed'] for r in sub),
                'changed_pct':100*sum(r['neighbor_changed'] for r in sub)/len(sub) if sub else None})
    return summary,prefix_rows,peer_rows,common

def write_csv(p,items):
    if not items:return
    with p.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)

def selftest():
    pre={'all_peers':{(10,'1.1.1.1'),(10,'2.2.2.2'),(30,'3.3.3.3')},'routes':{
      30873:{(10,'1.1.1.1','x/24'):'10 15412 30873',(10,'2.2.2.2','x/24'):'10 174 30873',(30,'3.3.3.3','y/24'):'30 174 30873'},
      12486:{(10,'1.1.1.1','z/24'):'10 15412 12486',(10,'2.2.2.2','z/24'):'10 15412 12486'}}}
    post={'all_peers':{(10,'1.1.1.1'),(10,'2.2.2.2')},'routes':{
      30873:{(10,'1.1.1.1','x/24'):'10 174 30873',(10,'2.2.2.2','x/24'):'10 174 30873'},
      12486:{(10,'1.1.1.1','z/24'):'10 15412 12486',(10,'2.2.2.2','z/24'):'10 15412 12486'}}}
    rows=make_rows(pre,post,'rrc00');metrics,prefix,peer,common=summarize(rows)
    a=next(v for v in metrics if v['origin_as']==30873)
    b=next(v for v in metrics if v['origin_as']==12486)
    assert a['initial_origin_rows']==3 and a['eligible']==2 and a['changed']==1 and a['prefix_count_with_comparable']==1
    assert b['changed']==0 and a['peer_count_with_comparable']==2
    assert len(common)==6 and common[0]['same_observers_for_two_ASes']==2
    assert upstream('123 {456,789} 30873',30873) is None
    assert upstream('123 30873 30873',30873)=='123'
    print('PASS synthetic tests: peer-IP isolation, absent-endpoint peer exclusion, matched origins, prefix aggregation, common observers, invalid AS_PATH')

def main():
    p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true')
    p.add_argument('--input-dir',type=Path);p.add_argument('--output-dir',type=Path)
    p.add_argument('--manifest',type=Path);p.add_argument('--collectors',nargs='+',choices=COLLECTORS,default=list(COLLECTORS))
    args=p.parse_args()
    if args.self_test:return selftest()
    if not args.input_dir or not args.output_dir or not args.manifest:p.error('input-dir, output-dir and manifest are required for original-MRT execution')
    with args.manifest.open(encoding='utf-8-sig',newline='') as f: entries=list(csv.DictReader(f))
    if len(entries)!=6:raise RuntimeError('Expected exact six historical original RIB entries')
    rows=[];sources=[]
    for rrc in args.collectors:
        these=sorted([r for r in entries if r['collector'].lower()==rrc],key=lambda x:x['timestamp_UTC'])
        if len(these)!=2:raise RuntimeError(f'Expected two original RIB files for {rrc}')
        dumps=[]
        for entry in these:
            name=entry['source_URL'].rsplit('/',1)[-1]
            local=args.input_dir/rrc/name
            if not local.exists():local=args.input_dir/name
            sha=digest_and_check(local,entry['SHA256_as_reported'],int(entry['original_compressed_bytes']))
            sources.append({'collector':rrc,'original_url':entry['source_URL'],'local_file':str(local),'sha256_verified':sha})
            dumps.append(source_rib(local))
        rows+=make_rows(dumps[0],dumps[1],rrc)
    metrics,prefix,peer,common=summarize(rows)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    write_csv(args.output_dir/'BGP_2020_peer_prefix_records.csv',rows)
    write_csv(args.output_dir/'BGP_2020_per_prefix_distribution.csv',prefix)
    write_csv(args.output_dir/'BGP_2020_per_peer_distribution.csv',peer)
    write_csv(args.output_dir/'BGP_2020_unit_sensitivity_summary.csv',metrics)
    write_csv(args.output_dir/'BGP_2020_common_observer_sensitivity.csv',common)
    (args.output_dir/'source_manifest_verified.json').write_text(json.dumps(sources,indent=2)+'\n')
    print('PASS source-native source-SHA-gated MRT analysis for',','.join(args.collectors))
    print(json.dumps(metrics,indent=2))
if __name__=='__main__':main()
