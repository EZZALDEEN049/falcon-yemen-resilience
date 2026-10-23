# Native IODA 2023: descriptive audit — 24 October 2026

This is an **additional same-cable, different-operational-regime observation**, not a substitute for the unavailable native January 2020 samples.

**Reproducible cloud job:** https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40025268544

- Official IODA `/v2/signals/raw/asn/30873`, UTC 9–11 November 2023.
- Baseline: 2023-11-09 00:00 to 2023-11-10 00:00 UTC.
- Maintenance disruption: 2023-11-10 00:10 to 04:45 UTC.
- Post window: 2023-11-10 05:00 to 2023-11-11 00:00 UTC.
- Native `bgp` median baseline 884; event median 356; 55/55 event 5-minute samples; **40.27% median retention**.
- Native `ping-slash24` median baseline 10; event median 6; 28/28 event 10-minute samples; **60.00% median retention**.
- Native signal-family contrast (BGP minus active retention) = **−19.73 percentage points** in this 2023 window, versus the opposite *plot-derived* sign in the January 2020 analysis. This does **not** establish comparable mechanisms, because operational regimes and measurement provenance differ.
- These are source-specific normalized proportions of the IODA signals, **not traffic percentages, share of affected people, or route-level effects**. The event window follows external reported timing, not automatic outage detection.
- Both native series passed the script's coverage checks for the specified windows.

**Critical blocker:** the official IODA API returned HTTP-200 **empty** `data: [[]]` for January 2020 (AS30873, AS12486, Yemen, including signal-specific attempts), while returning populated series for November 2023 and October 2026. This proves availability differs for tested windows *in this API response*, not that every independent archive lacks original 2020 data. Do not publish native 2020 results until that source-data blocker is independently resolved.

Recalculate with `code/analyze_native_ioda_2023.py` using the unmodified `FALCON_2023_asn_30873.json` response in the above run's 30-day Actions artifact.
