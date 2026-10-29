#!/usr/bin/env python3
"""Source-visible, wholly descriptive comparison; no independent-sampling or cable-causality claims.
Window choice 2020-01-02 08:00 to 2020-01-03 00:00 UTC was committed before baseline output inspection.
"""
import argparse, pathlib, csv, json, hashlib, statistics, ipaddress
from collections import defaultdict, Counter

def read(path):
    with open(path,encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def write(path,rows):
    with open(path,'w',encoding='utf-8',newline='') as f:
        if not rows: raise ValueError('empty '+str(path))
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def calc(rows):
    comparable=[r for r in rows if int(r['neighbor_comparable'])==1]
    eligible=sum(int(x['eligible']) for x in rows)
    retained=sum(int(x['same_origin_retained']) for x in rows)
    changed=sum(int(x['neighbor_changed']) for x in comparable)
    groups=defaultdict(list)
    for r in comparable:groups[r['prefix']].append(int(r['neighbor_changed']))
    peers=defaultdict(list)
    for r in comparable:peers[(r['peer_asn'],r['peer_ip'])].append(int(r['neighbor_changed']))
    q={k:sum(v)/len(v)*100 for k,v in groups.items()}
    p={k:sum(v)/len(v)*100 for k,v in peers.items()}
    return dict(initial_rows=len(rows),eligible=eligible,retained=retained,comparable=len(comparable),changed=changed,
                rate=changed/len(comparable)*100 if comparable else None,
                matched_prefixes=len(groups),matched_peers=len(peers),
                prefix_equal_mean=statistics.mean(q.values()) if q else None,
                prefix_equal_median=statistics.median(q.values()) if q else None,
                peer_equal_mean=statistics.mean(p.values()) if p else None,
                peer_equal_median=statistics.median(p.values()) if p else None,
                ipv4_comparable=sum(':' not in x['prefix'] for x in comparable),
                ipv6_comparable=sum(':' in x['prefix'] for x in comparable),
                prefix_rates=q,peer_rates=p)
def key(r):return (r['peer_asn'],r['peer_ip'],r['prefix'])
def main():
    a=argparse.ArgumentParser();a.add_argument('--event-root',required=True);a.add_argument('--reference-root',required=True);a.add_argument('--output-dir',required=True);args=a.parse_args()
    e=pathlib.Path(args.event_root);b=pathlib.Path(args.reference_root);o=pathlib.Path(args.output_dir);o.mkdir(parents=True,exist_ok=True)
    out=[]; controls=[]; manifests=[]; differences=[]
    for c in ('rrc00','rrc01','rrc10'):
        for period,root in [('event',e),('reference',b)]:
            p=root/c/'BGP_2020_peer_prefix_records.csv';audit=root/c/'audit.json';status=root/c/'individual_output_status.json'
            if not p.is_file() or not audit.is_file() or not status.is_file():raise FileNotFoundError(str(p))
            rows=read(p);source=json.loads(audit.read_text());statusdata=json.loads(status.read_text())
            assert source['status']=='VALIDATED_TWO_SNAPSHOT_DESCRIPTIVE_NOT_EVENT_CAUSAL', (c,period,source['status'])
            assert statusdata['rows']==len(rows)
            ts=('2020-01-02T08:00:00Z','2020-01-03T00:00:00Z') if period=='reference' else ('2020-01-09T08:00:00Z','2020-01-10T00:00:00Z')
            assert [x['time_utc'] for x in source['snapshots']]==list(ts), (c,period)
            originals=[dict(time_utc=x['time_utc'],sha256=x['source']['sha256'],url=x['source']['url'],bytes=x['source']['bytes'],gzip_crc=x['source']['gzip_crc']) for x in source['snapshots']]
            assert all(x['gzip_crc']=='passed' and len(x['sha256'])==64 for x in originals)
            manifests.append(dict(collector=c,period=period,first=originals[0],last=originals[1],row_sha256=digest(p),rows=len(rows)))
            groups={str(asn):[r for r in rows if r['target_as']==str(asn)] for asn in (30873,12486)}
            if sum(len(x) for x in groups.values())!=len(rows):raise ValueError('ASN universe mismatch')
            for asn,r in groups.items():
                q=calc(r); meta={k:v for k,v in q.items() if k not in ('prefix_rates','peer_rates')}
                out.append(dict(collector=c,asn=asn,period=period,**meta))
                controls.append({'collector':c,'asn':asn,'period':period,'records':r,'summary':q})
        for asn in ('30873','12486'):
            x=next(z for z in controls if z['collector']==c and z['asn']==asn and z['period']=='event');y=next(z for z in controls if z['collector']==c and z['asn']==asn and z['period']=='reference')
            ex=calc(x['records']);by=calc(y['records']);
            def comparable_dict(s):return {key(r):r for r in s if int(r['neighbor_comparable'])==1}
            ea=comparable_dict(x['records']);ba=comparable_dict(y['records']);common=set(ea)&set(ba)
            assert len(ea)==ex['comparable'] and len(ba)==by['comparable']
            ef=sum(int(ea[k]['neighbor_changed']) for k in common);bf=sum(int(ba[k]['neighbor_changed']) for k in common)
            pref_inter=set(ex['prefix_rates'])&set(by['prefix_rates']);peer_inter=set(ex['peer_rates'])&set(by['peer_rates'])
            differences.append(dict(collector=c,asn=asn,event_rate_pct=ex['rate'],reference_rate_pct=by['rate'],delta_pp=(ex['rate']-by['rate']) if ex['rate'] is not None and by['rate'] is not None else None,
                event_comparable=ex['comparable'],reference_comparable=by['comparable'],common_comparable_peer_prefixes=len(common),
                event_common_key_change_rate=100*ef/len(common) if common else None,reference_common_key_change_rate=100*bf/len(common) if common else None,
                common_key_delta_pp=100*(ef-bf)/len(common) if common else None,
                common_prefixes=len(pref_inter),common_prefix_event_equal_mean=statistics.mean(ex['prefix_rates'][p] for p in pref_inter) if pref_inter else None,
                common_prefix_reference_equal_mean=statistics.mean(by['prefix_rates'][p] for p in pref_inter) if pref_inter else None,
                common_peers=len(peer_inter)))
    assert len(out)==12 and len(differences)==6 and len(manifests)==6
    write(o/'Table_Reference_vs_Event_2020_12_Groups.csv',out)
    write(o/'Table_Differences_and_Common_Cohorts.csv',differences)
    (o/'Original_RIB_Source_And_Hashes.json').write_text(json.dumps(manifests,indent=2)+'\n')
    def fmt(v):return f'{v:.2f}' if isinstance(v,(float,int)) else 'NA'
    lines=['# Non-event 16-hour historical RIPE RIS baseline: evidence audit','',
        '**Reference window:** 2020-01-02 08:00 UTC → 2020-01-03 00:00 UTC. **Event-associated window:** 2020-01-09 08:00 UTC → 2020-01-10 00:00 UTC.',
        'The reference date was frozen in the research repository before examination of its outputs; one reference window is not a statistical estimate of ordinary variation.',
        'Source: six historical reference MRT RIBs and the previously published six event MRT RIBs; individual peer-prefix AS_PATH adjacency observations.',
        'The comparisons below are descriptive only. Neither baseline period is guaranteed to have zero unrelated network incidents, nor does a large difference identify a specific cable mechanism.', '',
        '| Collector | Origin AS | Event changed/comp. | Reference changed/comp. | Event % | Reference % | Difference pp | Fixed-comparable peer-prefixes | Fixed-cohort Δ pp |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for d in differences:
        x=next(z for z in out if z['collector']==d['collector'] and z['asn']==d['asn'] and z['period']=='event')
        y=next(z for z in out if z['collector']==d['collector'] and z['asn']==d['asn'] and z['period']=='reference')
        lines.append(f"| {d['collector'].upper()} | {d['asn']} | {x['changed']}/{x['comparable']} | {y['changed']}/{y['comparable']} | {fmt(d['event_rate_pct'])} | {fmt(d['reference_rate_pct'])} | {fmt(d['delta_pp'])} | {d['common_comparable_peer_prefixes']} | {fmt(d['common_key_delta_pp'])} |")
    lines.extend(['','## Interpretation gate','- Changed neighbor is origin-adjacent AS_PATH at **two RIB endpoints**, not data-plane or cable observations.','- Event and reference route populations differ; fixed-key comparison is supplemental and conditions on presence in both periods and endpoints.','- AS12486 has a distinct six-prefix inventory vs AS30873 ≈105 prefixes; it is not a causal control.','- Peer-route records overlap across collectors and prefix groups; no p-value or independent-sample CI is computed.','- Multiple non-event windows would be preferable for characterizing the *distribution* of ordinary churn.','- The original six source filenames, URLs, sizes and hashes are recorded in Original_RIB_Source_And_Hashes.json.'])
    (o/'SOURCE_NATIVE_REFERENCE_COMPARISON.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    print('\n'.join(lines[:13]));print('PASS: 6 source audits, 12 group summaries, 6 contrasts, cohort sensitivity')
if __name__=='__main__':main()
