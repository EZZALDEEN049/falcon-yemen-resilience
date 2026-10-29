"""Independent analysis of redistributed original 2023 IODA source JSON and
previously validated 2020 collector/Atlas summary counts. Descriptive only."""
import json,hashlib,csv,statistics,io
from zipfile import ZipFile
from datetime import datetime,timezone,timedelta
from pathlib import Path
ROOT=Path(__file__).parent
OUTPUT=ROOT.parent/'Results'
OUTPUT.mkdir(parents=True,exist_ok=True)
SRC=ROOT.parent/'Supplement'/'IODA_2023_Original_JSON_SourceArtifact.zip'
if not SRC.exists(): raise FileNotFoundError('IODA 2023 original source ZIP not found in Supplement: '+str(SRC))
EPOCH=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp())
BASE_END=EPOCH('2023-11-10T00:00:00Z')
EVENT_S=EPOCH('2023-11-10T00:10:00Z')
EVENT_E=EPOCH('2023-11-10T04:45:00Z')
series={};shas={}
with ZipFile(SRC) as z:
 for asn in ('30873','12486'):
  name=f'FALCON_2023_asn_{asn}.json'; raw=z.read(name)
  shas[asn]=hashlib.sha256(raw).hexdigest()
  expected_hash={'30873':'47870f9259cc948af8c5390d59754bdb82702b0fca3624dbcfad5c5dec050641','12486':'8f504b8cd68abdf0f48803b66340d25881b3bbdd5b5f80035283af3a82a28b6a'}[asn]
  if shas[asn] != expected_hash: raise RuntimeError(f'Original IODA source hash mismatch: AS{asn}')
  obj=json.loads(raw)
  for group in obj['data']:
   for s in group:
    if s.get('entityType')=='asn' and str(s.get('entityCode'))==asn and s.get('datasource') in ('bgp','ping-slash24'):
     key=(asn,s['datasource']);assert key not in series; series[key]=s

def vals(s,lo,hi):
 out=[float(v) for i,v in enumerate(s['values']) if isinstance(v,(int,float)) and not isinstance(v,bool) and lo<=s['from']+i*s['step']<hi]
 from math import ceil
 expected=ceil((hi-s['from'])/s['step'])-ceil((lo-s['from'])/s['step'])
 if len(out)!=expected: raise ValueError((s['entityCode'],s['datasource'],lo,hi,len(out),expected))
 return out
out=[]; per_asn={a:[] for a in ('30873','12486')}
for hours in (12,18,24):
 for so in (-10,-5,0,5,10):
  for eo in (-10,-5,0,5,10):
   for asn in ('30873','12486'):
    ret={};retmean={}
    for typ in ('bgp','ping-slash24'):
     s=series[asn,typ]
     baseline=vals(s,BASE_END-hours*3600,BASE_END)
     event=vals(s,EVENT_S+so*60,EVENT_E+eo*60)
     ret[typ]=100*statistics.median(event)/statistics.median(baseline)
     retmean[typ]=100*statistics.mean(event)/statistics.mean(baseline)
    item={'asn':asn,'baseline_hours':hours,'start_offset_min':so,'end_offset_min':eo,'bgp_retention_median':ret['bgp'],'ping_retention_median':ret['ping-slash24'],'median_gap_pp':ret['bgp']-ret['ping-slash24'],'bgp_retention_mean':retmean['bgp'],'ping_retention_mean':retmean['ping-slash24'],'mean_gap_pp':retmean['bgp']-retmean['ping-slash24']}
    out.append(item);per_asn[asn].append(item)
collectors={'rrc00':{'30873':(4157,6220,6602),'12486':(23,366,427)},'rrc01':{'30873':(1482,2180,2582),'12486':(6,148,172)},'rrc10':{'30873':(868,1341,1419),'12486':(11,78,91)}}
agg=[]
for c,v in collectors.items():
 a=v['30873'];b=v['12486']; d=100*(a[0]/a[1]-b[0]/b[1]);agg.append({'collector':c,'AS30873_neighbor_change_pct':100*a[0]/a[1],'AS12486_neighbor_change_pct':100*b[0]/b[1],'within_collector_difference_pp':d,'AS30873_route_retention_pct':100*a[1]/a[2],'AS12486_route_retention_pct':100*b[1]/b[2]})
# using original Atlas logged daily aggregates, NOT independent per-ping samples
days={'2020-01-08':(663,673),'2020-01-09':(670,672),'2020-01-10':(669,672),'2020-01-11':(670,672),'2020-01-12':(671,671)}
jack={day:100*sum(v[0] for k,v in days.items() if k!=day)/sum(v[1] for k,v in days.items() if k!=day) for day in days}
summary={'status':'DERIVED_FROM_ARCHIVED_SOURCE_2023_JSON_AND_VALIDATED_AGGREGATES','source_zip_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'native_ioda_sha256':shas,'native_2023_grid_tested':len(out),'per_asn':{},'2020_rrc_comparisons':agg,'atlas_single_target_leave_one_day_out_reply_pct':jack,'atlas_5_day_reply_pct':100*sum(v[0] for v in days.values())/sum(v[1] for v in days.values()),'limitations':['No novel original 2020 IODA data','2020 RIS raw MRT bytes not re-fetched; numbers re-computed from archived audit counts','75 grids per AS not 75 statistically independent experiments','Mean and median use separate signal-specific baseline; no shared traffic unit','RIPE Atlas day aggregates are single-destination repeated probes; no national population inference']}
for asn,rows in per_asn.items():
 summary['per_asn'][asn]={}
 for key in ('bgp_retention_median','ping_retention_median','median_gap_pp','mean_gap_pp'):
  arr=[x[key] for x in rows]
  summary['per_asn'][asn][key]={'min':min(arr),'max':max(arr),'negative':sum(v<0 for v in arr),'positive':sum(v>0 for v in arr),'zero':sum(v==0 for v in arr)}
 with0=[r for r in rows if r['baseline_hours']==24 and r['start_offset_min']==0 and r['end_offset_min']==0][0]
 summary['per_asn'][asn]['original_window_crosscheck']=with0
assert len(out)==150
assert abs(summary['atlas_5_day_reply_pct']-100*3343/3360)<1e-10
p=OUTPUT/'q1_evidence_numeric_audit.json';p.write_text(json.dumps(summary,indent=2),encoding='utf8')
with (OUTPUT/'q1_2023_sensitivity_150_rows.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=out[0].keys());w.writeheader();w.writerows(out)
print(json.dumps(summary,indent=2))
