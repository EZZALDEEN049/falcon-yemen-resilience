# Implementation status — 22 October 2026

This is a **research revision**, not evidence of completed raw-data acquisition. All new numeric results below are DERIVED_FROM_PUBLISHED_NORMALIZED_PLOT aggregates already redistributed by the authors; they are **not raw IODA observations**.

## Completed and recalculated

- Executed the existing `code/reproduce_all.py`, checked the frozen 2026 origin HHI and reproduced the 2020 central *plot-derived* divergence of 50.8144 percentage points and the saved raster sensitivity range (45.8074–55.1698 pp).
- Added `code/phase_audit.py`, `results/phase_specific_plot_proxy_comparison.csv` (Table S1), `results/phase_audit_summary.json`, `figures/Figure4_phase_specific_plot_proxy_retention.png`.
- Phased median BGP-minus-active divergence in AS30873: early degradation **56.1242 pp**; acute **50.8144 pp**; post-midnight **44.6197 pp**. These are different source-window aggregate estimates, **not** samples on a continuous recovery curve.
- AS12486 acute active probing: median retention **100.0%**, mean retention **95.5709%** relative to the corresponding pre-event mean; avoids the mistaken inference of 'no effect' from the median alone.
- Refreshed Figure 3 to keep legend clear of bars, with reproducible source in `code/reproduce_all.py`.
- Added stricter `code/validate_native_ioda.py` (future use) and `code/historical_bgp_replay_v2.py` (future use), plus five passing **synthetic-code guardrail tests** in `code/test_guardrails.py`. Tests verify parser and rejection behavior; **not empirical truth of the 2020 route series**.
- Revised text, abstract, research question RQ2, main findings, scope limitations, discussion, reproducibility, conclusion, and Figure 4 in `Manuscript_Revised_Evidence_Bounded.docx`.

## Executed and blocked

- Direct IODA attempts for AS30873, AS12486, AS204317, and Yemen for January 2020: **0 downloads succeeded**, **4 connection errors** (network/DNS in this execution environment). See `results/raw_ioda_attempt_2026-10-22/manifest.json`.
- `bgpreader` is not installed on the current execution host and Internet/DNS prevents archive access: **no historical raw MRT/BGP reconstructed**.
- **No population-wide causal cascade estimate, route-level retention, formal time-series confidence interval, or intervention effect has been calculated.**

## Methodological qualification

- The 20,250 raster sensitivity combinations are analytic perturbations, *not independent experiments*. Grid quantiles are not confidence bounds.
- BGP and active-probing metrics observe different quantities and are not customer traffic proportions.
- The 2026 150-prefix origin snapshot is not a 2020 topology; three origins should not be taken as an exhaustive national inventory.
- Even the guarded replay cannot release a population-level number without independently verifying historical prefix inventory, full update-archive coverage and whether each baseline peer remained observable at the event checkpoint. It deliberately fails when liveness is unknown.

## Next empirical requirements

1. On a network-enabled host retrieve official IODA raw series for the event and inspect datasource names and time coverage. Run the guarded native analyzer and compare, **do not silently replace** the plot results.
2. Install CAIDA BGPReader and collect a relevant historical RIS/RouteViews seed RIB plus unfiltered-by-origin A/W updates for a verified historical prefix universe, checking archive completeness and peer liveness.
3. Release quantitative route-level and cross-layer findings only after those validations succeed. Update the manuscript and supplement together to avoid mismatched claims.

References: official IODA API https://api.ioda.inetintel.cc.gatech.edu/v2/ ; CAIDA BGPReader https://bgpstream.caida.org/docs/tools/bgpreader ; 2020 event report https://internetdisruption.report/2020/02/23/internet-disruption-report-january-2020/ .
