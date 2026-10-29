#!/usr/bin/env python3
"""Independent transparent calibration check against original published IODA PNGs.

Source images are third-party published raster plots, not raw IODA numeric samples.
The script checks their pixel-colored traces using the historical 2020 calibration.
"""
import argparse, csv, hashlib, json, statistics
from datetime import datetime, timezone, timedelta
from pathlib import Path
from PIL import Image

START=datetime(2020,1,7,22,10,tzinfo=timezone.utc)
END=datetime(2020,1,10,22,15,tzinfo=timezone.utc)
CAL=dict(x_min=112,x_max=1779,y_min=240,y_zero=632,pixels_per_unit=252)
COLORS={'bgp':(51,160,44),'active':(31,120,180)}
BASE=(datetime(2020,1,8,0,tzinfo=timezone.utc),datetime(2020,1,9,8,30,tzinfo=timezone.utc))
ACUTE=(datetime(2020,1,9,18,tzinfo=timezone.utc),datetime(2020,1,10,0,tzinfo=timezone.utc))
PUBLISHED_PRIOR=dict(AS30873=dict(bgp_retention_pct=95.65217391304348,active_retention_pct=44.83775811209439,gap_pp=50.81441580094909),AS12486=dict(bgp_retention_pct=100,active_retention_pct=100,gap_pp=0))

def parse_signal(file,tolerance=2):
    bs=file.read_bytes();im=Image.open(file);im.load();im=im.convert('RGB');W,H=im.size
    if W<=CAL['x_max'] or H<=CAL['y_zero']:raise RuntimeError('Publisher image is not original-scale 1840x874 raster: '+str(file))
    data=[];arr=im.load()
    for x in range(CAL['x_min'],CAL['x_max']+1):
        t=START+(END-START)*((x-CAL['x_min'])/(CAL['x_max']-CAL['x_min']))
        row={'x':x,'time_utc':t.isoformat()}
        for k,c in COLORS.items():
            yy=[y for y in range(CAL['y_min'],CAL['y_zero']+1) if all(abs(arr[x,y][i]-c[i])<=tolerance for i in range(3))]
            row[k]=((CAL['y_zero']-statistics.median(yy))/CAL['pixels_per_unit'] if yy else None)
            row[k+'_line_pixels']=len(yy)
        data.append(row)
    return dict(size=[W,H],sha256=hashlib.sha256(bs).hexdigest(),all_columns=len(data),columns_with_bgp=sum(x['bgp'] is not None for x in data),columns_with_active=sum(x['active'] is not None for x in data),data=data)

def calc(samples,kind,t1,t2):
    x=[r[kind] for r in samples if t1<=datetime.fromisoformat(r['time_utc'])<t2 and r[kind] is not None]
    return dict(n_columns=len(x),median=statistics.median(x),mean=statistics.mean(x)) if x else dict(n_columns=0,median=None,mean=None)

def main():
    p=argparse.ArgumentParser();p.add_argument('--as30873',type=Path,required=True);p.add_argument('--as12486',type=Path,required=True);p.add_argument('--out-dir',type=Path,required=True);args=p.parse_args();args.out_dir.mkdir(parents=True,exist_ok=True)
    report={'definition':'published-raster column trace, not native IODA samples','calibration':CAL,'time_utc':[START.isoformat(),END.isoformat()],'baseline':[x.isoformat() for x in BASE],'acute':[x.isoformat() for x in ACUTE],'results':{}}
    for asn,f in [('AS30873',args.as30873),('AS12486',args.as12486)]:
        v=parse_signal(f)
        values=v.pop('data')
        with (args.out_dir/f'{asn}_published_plot_colored_columns.csv').open('w',newline='') as fd:
            w=csv.DictWriter(fd,fieldnames=list(values[0]));w.writeheader();w.writerows(values)
        base={k:calc(values,k,*BASE) for k in COLORS};acute={k:calc(values,k,*ACUTE) for k in COLORS}
        derived={k:100*acute[k]['median']/base[k]['median'] for k in COLORS}
        gap=derived['bgp']-derived['active']
        previous=PUBLISHED_PRIOR[asn]
        report['results'][asn]={**v,'baseline':base,'acute':acute,'calculated_retention_percent':derived,'calculated_gap_pp':gap,'previous_published_plot_proxy':previous,'difference_from_previous_pp':gap-previous['gap_pp'],'pixel_geometry_pass':min(v['columns_with_bgp'],v['columns_with_active'])>=100}
    (args.out_dir/'pixel_level_recalibration_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:{'gap_pp':round(v['calculated_gap_pp'],5),'prev_gap_pp':round(v['previous_published_plot_proxy']['gap_pp'],5),'difference_pp':round(v['difference_from_previous_pp'],5),'columns':[v['columns_with_bgp'],v['columns_with_active']]} for k,v in report['results'].items()},indent=2))
if __name__=='__main__':main()
