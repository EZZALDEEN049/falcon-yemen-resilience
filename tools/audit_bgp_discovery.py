#!/usr/bin/env python3
"""Fail closed on empty/incorrect output; derive only an historical prefix *candidate* list."""
import argparse,csv,json,sys,ipaddress
from collections import Counter
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--asn',required=True);p.add_argument('--collector',required=True);p.add_argument('--out',required=True);a=p.parse_args()
out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
src=Path(a.input);prefixes=set(); peers=set(); n=0;rejected=0
for line in src.open(encoding='utf8'):
  t=line.strip().split('|')
  if len(t)<13 or t[0]!='R' or t[1]!='R' or t[3]!='ris' or t[4]!=a.collector or t[12]!=a.asn:rejected+=1;continue
  try: ipaddress.ip_network(t[9],strict=False)
  except ValueError:rejected+=1;continue
  prefixes.add(t[9]);peers.add((t[7],t[8]));n+=1
(out/'candidate_historical_prefixes_2020.txt').write_text('\n'.join(sorted(prefixes))+'\n',encoding='utf8')
stats={'origin_asn':a.asn,'collector':a.collector,'rib_rows':n,'candidate_prefixes':len(prefixes),'distinct_peers':len(peers),'rejected_lines':rejected,'status':'DISCOVERY_ONLY_NOT_A_VALIDATED_INVENTORY','evidence_date':'2020-01-09','caveat':'Origin-filtered RIB is appropriate for discovery only. For replay, export all announcements/withdrawals by historical prefix; validate collector peer continuity and full archive coverage.'}
(out/'discovery_manifest.json').write_text(json.dumps(stats,indent=2),encoding='utf8')
print(json.dumps(stats,indent=2))
if not prefixes or not peers:sys.exit('No valid Jan 2020 candidate observations; no historical conclusions can be released')
