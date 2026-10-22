#!/usr/bin/env python3
"""Guarded *offline* historical BGP reader for two timestamps from one RIS/RV seed RIB.

IMPORTANT: `bgpreader -a <origin-asn>` must NEVER be used for updates if withdrawals
are required; W records have no origin AS. Acquire RIB and ALL A/W updates with
prefix filters (`-k <prefix>`) and with identical project/collector settings.

Requires manually validated historical prefix inventory; never use 2026 inventory
as if it were the 2020 original. Any output remains scoped to that inventory.

BGPReader elem format: dump|elem|timestamp|project|collector|router|router_ip|
peer_asn|peer_ip|prefix|next_hop|as_path|origin_as|...
"""
import argparse,csv,datetime as dt,ipaddress,json,statistics
from collections import defaultdict
from pathlib import Path


def utc(t):
    return dt.datetime.fromisoformat(t.replace('Z','+00:00')).timestamp()

def parse_line(line):
    cols=line.strip().split('|')
    if len(cols)<13 or cols[0] not in ('R','U') or cols[1] not in ('R','A','W'): return None
    _,elem,ts,project,collector,router,router_ip,peer_asn,peer_ip,prefix,next_hop,as_path,origin=cols[:13]
    if not all((project,collector,peer_asn,peer_ip,prefix)): return None
    try:
        ipaddress.ip_network(prefix,strict=False); float(ts)
    except (ValueError,TypeError): return None
    # Peer address is necessary: peer ASN alone is not a unique collector-peer vantage.
    return {'type':elem,'timestamp':float(ts),'vantage':(project,collector,router,router_ip,peer_asn,peer_ip),
            'prefix':prefix,'path':as_path,'origin':origin}

def read_records(path,valid_types):
    with open(path,encoding='utf8') as f:
        for line in f:
            rec=parse_line(line)
            if rec and rec['type'] in valid_types: yield rec

def upstream(as_path,origin):
    tok=[x for x in as_path.split() if x.isdigit()]
    if len(tok)<2 or tok[-1]!=str(origin): return None
    end=len(tok)-1
    while end>0 and tok[end-1]==tok[-1]:end-=1
    return tok[end-1] if end>0 else None

def states_at(rib,updates,prefixes,asn,pre_ts,event_ts):
    state={}; base={}; counts={'rib_target':0,'announce':0,'withdrawal':0,'origin_change':0,'universe_updates':0}
    for r in rib:
        if r['prefix'] not in prefixes:continue
        if r['origin']==str(asn):
            state[(r['vantage'],r['prefix'])]=r; counts['rib_target']+=1
    if counts['rib_target']==0:raise ValueError('No validated origin routes in the RIB: no historical metrics')
    for r in sorted(updates,key=lambda x:x['timestamp']):
        if r['timestamp']>event_ts:break
        if r['prefix'] not in prefixes:continue
        counts['universe_updates']+=1
        key=(r['vantage'],r['prefix'])
        if r['type']=='W':
            state.pop(key,None);counts['withdrawal']+=1
        elif r['type']=='A':
            # Reannouncing this prefix with a DIFFERENT origin deletes target origin observation.
            if r['origin']==str(asn):state[key]=r
            else:state.pop(key,None);counts['origin_change']+=1
            counts['announce']+=1
        # Replay of complete baseline state is performed separately below.
    base={}
    # Reconstruct baseline from same initial RIB through pre boundary.
    for r in rib:
        if r['prefix'] in prefixes and r['origin']==str(asn):base[(r['vantage'],r['prefix'])]=r
    for r in sorted(updates,key=lambda x:x['timestamp']):
        if r['timestamp']>pre_ts:break
        if r['prefix'] not in prefixes:continue
        k=(r['vantage'],r['prefix'])
        if r['type']=='W' or r['origin']!=str(asn):base.pop(k,None)
        else:base[k]=r
    return base,state,counts

def comparable(pre,cur):
    A=defaultdict(dict);B=defaultdict(dict)
    for (v,p),row in pre.items():A[v][p]=row
    for (v,p),row in cur.items():B[v][p]=row
    dropped=set(A)-set(B)
    if dropped:
        raise ValueError(f'{len(dropped)} pre-event vantages have no target-origin routes at event time. Peer liveness cannot be inferred from prefix-scoped observations; require full-collector peer status to distinguish total withdrawal from peer loss before producing retention statistics.')
    vp=set(A)&set(B)
    if not vp: raise ValueError('No collector-peer matched vantage; refuse numeric inference')
    pre_total=retained=0; changes=0; common=0; old_providers=set(); new_providers=set()
    for v in vp:
        a,b=A[v],B[v]; pa,pb=set(a),set(b)
        pre_total+=len(pa); retained+=len(pa&pb)
        for prefix in pa&pb:
            common+=1
            x,y=upstream(a[prefix]['path'],a[prefix]['origin']),upstream(b[prefix]['path'],b[prefix]['origin'])
            if x:old_providers.add(x)
            if y:new_providers.add(y)
            if x!=y:changes+=1
    if pre_total==0:raise ValueError('Zero baseline among matched vantages')
    return {'n_matched_vantages':len(vp),'matched_collectors':len({v[:2] for v in vp}),
            'prefix_observation_retention':retained/pre_total,
            'upstream_switch_fraction_given_visible':(changes/common if common else None),
            'observed_upstreams_pre':sorted(old_providers),
            'observed_upstreams_event':sorted(new_providers),
            'coverage_caveat':'Only previously validated historical prefix inventory and matched observed vantages; no national traffic or causal cable-path mapping'}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--rib',required=True,help='Unfiltered-within-prefix BGPReader RIB records, one seed RIB for observed collector set')
    p.add_argument('--updates',required=True,help='BGPReader A and W records for ALL tracked prefixes, without -a filter')
    p.add_argument('--inventory',required=True,help='Externally verified historical prefix inventory, one CIDR per line; cannot use 2026 as substitute')
    p.add_argument('--asn',type=int,required=True)
    p.add_argument('--pre',required=True,help='e.g. 2020-01-09T08:30:00Z')
    p.add_argument('--event',required=True,help='e.g. 2020-01-09T18:30:00Z')
    p.add_argument('--out',required=True)
    a=p.parse_args(); start,end=utc(a.pre),utc(a.event)
    if end<=start:raise SystemExit('Event checkpoint must be after baseline checkpoint')
    prefixes={ln.strip() for ln in Path(a.inventory).read_text(encoding='utf8').splitlines() if ln.strip() and not ln.startswith('#')}
    if not prefixes:raise SystemExit('Validated historical prefix inventory required')
    rib=list(read_records(a.rib,{'R'}));updates=list(read_records(a.updates,{'A','W'}))
    if not rib or not updates:raise SystemExit('Missing RIB / updates; refusing metrics')
    if max(r['timestamp'] for r in rib)>start:raise SystemExit('RIB must precede pre checkpoint')
    # UPDATE message timestamps alone do not prove archive completeness; enforce documented, audited coverage separately.
    if min(r['timestamp'] for r in updates)>start or max(r['timestamp'] for r in updates)<end:
        raise SystemExit('The supplied records do not bracket both checkpoints. A no-message interval requires independently verified archive coverage; no metric is released here.')
    pre,cur,counts=states_at(rib,updates,prefixes,a.asn,start,end)
    result={'asn':a.asn,'pre':a.pre,'event':a.event,'tracked_prefixes':len(prefixes),'extraction_counts':counts,
            'metrics':comparable(pre,cur),'status':'SCOPED_REPLAY_ONLY_REQUIRES_INVENTORY_AND_ARCHIVE_AUDIT',
            'limits':['Does not claim full AS prefix completeness','Does not measure cross-layer cable dependency','Archive gaps & collector turnover need external verification']}
    Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    Path(a.out).write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
