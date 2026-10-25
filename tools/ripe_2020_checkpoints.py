#!/usr/bin/env python3
"""Historical RIPEstat snapshot discovery, not native IODA or event-time BGP replay."""
import concurrent.futures,csv,datetime as dt,hashlib,json,time,urllib.parse,urllib.request
from pathlib import Path
out=Path('_artifacts/ripe_2020');out.mkdir(parents=True,exist_ok=True)
times=['2020-01-08T16:00:00Z','2020-01-09T00:00:00Z','2020-01-09T08:00:00Z','2020-01-09T16:00:00Z','2020-01-10T00:00:00Z','2020-01-10T08:00:00Z','2020-01-10T16:00:00Z','2020-01-11T00:00:00Z']
def get(arg):
 asn,t=arg
 url='https://stat.ripe.net/data/routing-status/data.json?'+urllib.parse.urlencode({'resource':asn,'timestamp':t,'min_peers_seeing':10})
 row={'asn':asn,'requested_utc':t,'url':url,'status':'NO_VALIDATED_RESPONSE'}
 try:
  for trial in range(3):
   try:
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Yemen-FALCON-academic-2020/1.0','Accept':'application/json'}),timeout=28) as r:
     data=r.read(2000001)
     if len(data)>2000000:raise ValueError('response too large')
     row['http_status']=r.status
    obj=json.loads(data)
    if obj.get('status')!='ok' or not isinstance(obj.get('data'),dict):raise ValueError('API returned error/empty')
    d=obj['data'];space=(d.get('announced_space') or {}).get('v4') or {};v=(d.get('visibility') or {}).get('v4') or {}
    row.update(returned_time=d.get('query_time'),v4_prefixes=space.get('prefixes'),v4_addresses=space.get('ips'),peer_seen=v.get('ris_peers_seeing'),peer_total=v.get('total_ris_peers'),observed_neighbours=d.get('observed_neighbours'),sha256=hashlib.sha256(data).hexdigest())
    (out/(asn+'_'+t.replace(':','-')+'.json')).write_bytes(data)
    if isinstance(row['v4_prefixes'],int) and row['returned_time']:row['status']='VALID_RIPESTAT_SNAPSHOT_NOT_IODA'
    else:row['status']='INCOMPLETE_SCHEMA'
    break
   except Exception as e:
    row['error']=str(e)[:200]
    if trial<2:time.sleep(trial+1)
 except Exception as e:row['error']=str(e)[:200]
 return row
tasks=[(a,t) for a in ('AS30873','AS12486') for t in times]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(get,tasks))
with open(out/'snapshot_summary.csv','w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=sorted(set().union(*(x.keys() for x in rows))));wr.writeheader();wr.writerows(rows)
(out/'manifest.json').write_text(json.dumps({'purpose':'historical routing context; NOT IODA original samples, cable physical paths, user traffic or complete peer-matched replay','retrieval_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'source':'https://stat.ripe.net/docs/data-api/api-endpoints/routing-status','rows':rows},indent=2))
print(json.dumps([{k:r.get(k) for k in ('asn','requested_utc','status','v4_prefixes','peer_seen','peer_total','error')} for r in rows],indent=2))
