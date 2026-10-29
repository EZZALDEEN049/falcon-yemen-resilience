#!/usr/bin/env python3
import csv,hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
D=ROOT/'Evidence'/'BGP_2020'
M=json.loads((D/'REVIEWER_MANIFEST.json').read_text())
for f in M['files']:
 p=D/f['path']; assert p.is_file(),p; assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256'],p
expect={'rrc00':{'30873':(6602,6220,4157),'12486':(427,366,23)},'rrc01':{'30873':(2582,2180,1482),'12486':(172,148,6)},'rrc10':{'30873':(1419,1341,868),'12486':(91,78,11)}}
total=0
for rr in expect:
 rd=D/rr
 def read(name):
  with (rd/name).open(newline='',encoding='utf8') as f:return list(csv.DictReader(f))
 rows=read('BGP_2020_peer_prefix_records.csv');prefix=read('BGP_2020_prefix_distributions.csv');peer=read('BGP_2020_peer_distributions.csv')
 total+=len(rows)
 for asn,expected in expect[rr].items():
  a=[r for r in rows if r['target_as']==asn];b=[r for r in prefix if r['target_as']==asn];c=[r for r in peer if r['target_as']==asn]
  assert len(a)==len({(r['peer_asn'],r['peer_ip'],r['prefix']) for r in a})
  eligible=sum(r['eligible']=='1' for r in a);retained=sum(r['same_origin_retained']=='1' for r in a);changed=sum(r['neighbor_changed']=='1' for r in a);comparable=sum(r['neighbor_comparable']=='1' for r in a)
  assert (eligible,retained,changed)==expected and retained==comparable
  for group in (b,c):
   assert sum(int(v['comparable']) for v in group)==retained
   assert sum(int(v['changed']) for v in group)==changed
assert total==M['verified_rows_total']==11419
path=ROOT/'Supplement'/'Table_S6_IODA_2020_20250_Deterministic_Settings.csv'
assert hashlib.sha256(path.read_bytes()).hexdigest()=='fa9720246ec52edb6770c8637f52da260856908574fb490a4d49f0e825245e12'
print('PASS: original-source BGP row-level 11419, six count triples, per-prefix/per-peer sums, all source CSV hashes and 2020 IODA 20250 sensitivity file hash')
