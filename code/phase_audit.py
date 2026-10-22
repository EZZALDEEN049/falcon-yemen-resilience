#!/usr/bin/env python3
"""Recalculate *descriptive* phased retention from the redistributed plot-digitized table.
No source image / native IODA trace is implied. No pseudo-replication or confidence intervals.
"""
import csv, json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
WINDOWS=['pre_event_baseline','early_degradation','acute_event','post_midnight']
ASNS=['AS30873','AS12486']

def read_rows():
    with (ROOT/'data'/'stage9_ioda_digitized_signal_validation_v0_1.csv').open(newline='',encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def compute():
    rows=read_rows()
    by={(r['asn'],r['window'],r['signal']):r for r in rows}
    assert len(by)==len(rows)==16, 'Expected exactly 16 unique source aggregates'
    out=[]
    for asn in ASNS:
        for phase in WINDOWS:
            v={}
            for signal in ('bgp','active'):
                r=by[(asn,phase,signal)]
                b=by[(asn,'pre_event_baseline',signal)]
                assert r['evidence_class']=='DERIVED_FROM_PUBLISHED_NORMALIZED_PLOT'
                for stat in ('median','mean'):
                    base=float(b[f'{stat}_normalized'])
                    assert base>0
                    v[f'{signal}_{stat}_retention_pct']=100*float(r[f'{stat}_normalized'])/base
                v[f'{signal}_n_columns']=int(r['n_digitized_columns'])
            for stat in ('median','mean'):
                v[f'divergence_{stat}_pp']=v[f'bgp_{stat}_retention_pct']-v[f'active_{stat}_retention_pct']
            out.append({'asn':asn,'window':phase,**v,'evidence_class':'PLOT_DERIVED_AGGREGATE','independent_samples':False})
    csvpath=ROOT/'results'/'phase_specific_plot_proxy_comparison.csv'
    with csvpath.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
    # Plot series are already *within-signal* normalized to baselines; not a traffic or customer-service measure.
    x=list(range(len(WINDOWS)))
    fig,ax=plt.subplots(figsize=(9.7,5.4))
    for asn,signal,style in [('AS30873','bgp','o--'),('AS30873','active','s-'),('AS12486','bgp','^:'),('AS12486','active','x-.')]:
        values=[next(r[f'{signal}_median_retention_pct'] for r in out if r['asn']==asn and r['window']==phase) for phase in WINDOWS]
        ax.plot(x,values,style,lw=1.7,markersize=6,label=f'{asn}: {"BGP" if signal=="bgp" else "active probing"}')
    ax.axhline(100,color='0.4',linestyle=':',lw=1)
    ax.set_xticks(x,['Baseline','Early degradation','Acute event','Post-midnight'])
    ax.set_ylabel('Within-signal window median / baseline median (%)')
    ax.set_ylim(0,112)
    ax.grid(axis='y',linestyle=':',alpha=.35)
    ax.legend(loc='lower center',bbox_to_anchor=(.5,1.01),ncol=2,fontsize=9,frameon=False)
    fig.tight_layout()
    fig.savefig(ROOT/'figures'/'Figure4_phase_specific_plot_proxy_retention.png',dpi=350,bbox_inches='tight')
    plt.close(fig)
    a=[r for r in out if r['asn']=='AS30873']
    b=[r for r in out if r['asn']=='AS12486']
    summary={
      'scope':'Descriptive recomputation from per-window aggregates digitized from third-party plot; not native samples; no time-series or route-level inference',
      'as30873_gap_early_pp':next(r['divergence_median_pp'] for r in a if r['window']=='early_degradation'),
      'as30873_gap_acute_pp':next(r['divergence_median_pp'] for r in a if r['window']=='acute_event'),
      'as30873_gap_post_midnight_pp':next(r['divergence_median_pp'] for r in a if r['window']=='post_midnight'),
      'as12486_acute_active_mean_retention_pct':next(r['active_mean_retention_pct'] for r in b if r['window']=='acute_event'),
      'as12486_acute_active_median_retention_pct':next(r['active_median_retention_pct'] for r in b if r['window']=='acute_event'),
      'interpretation':'AS12486 median 100% does not establish no transient disruption; acute mean is below 100%. Raster columns are not independent measurements.',
    }
    (ROOT/'results'/'phase_audit_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    print(json.dumps(summary,indent=2))
    return summary
if __name__=='__main__': compute()
