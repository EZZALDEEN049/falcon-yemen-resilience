# QA audit of user-supplied Stage 9 Historical BGP Execution v1.0 — 26 October 2026

## Intake and integrity
- Submitted file: `Stage9_Historical_BGP_Execution_v1_0.zip`, 31 ZIP entries (~51 KB compressed).
- Local ZIP integrity (CRC) passed; all **27** `SHA256SUMS.txt` manifest digest entries independently verified against archive members.
- All three main Python modules compile; `stage9_synthetic_selftest_v1_0.py` rerun on isolated standard Python and **PASS**.
- Gate report explicitly says **BLOCKED_ON_RAW_HISTORICAL_BGP_ACCESS**; `stage9_primary_execution_exit_code.txt = 2`, stderr says `pybgpstream is not installed`; no raw route-state empirical outputs.
- All source-derived 2020 IODA proxy values are plot-digitized only. A working codebase and self-test are not historical experimental validation.

## Critical correctness blockers before any reported historical metric
1. **Peer identity collision**: `stage9_historical_bgp_executor_v1_0.py` indexes routes by `(elem.collector, elem.peer_asn, prefix)`; the metric engine groups by `(collector, peer_asn)`. Multiple peer sessions with the same ASN at one collector can have different `peer_address` values. This code merges their RIB/update observations and could falsely register switching, withdrawal, visibility. Fix: carry `elem.peer_address` (peer IP) alongside collector, ASN, router identity consistently end to end, including every raw trace and tests. CAIDA documented API specifically exposes both `peer_address` and `peer_asn`: https://dev.bgpstream.caida.org/docs/api/pybgpstream/_pybgpstream.html
2. **Missing independent peer liveness**: A vantage with zero surviving target-origin routes at the event checkpoint is not necessarily a failed AS route. The RIS session/collector may be absent. Labeling every such case a `PVR_lower_bound=0` is an extreme assumption, not a verified failure. Establish collection coverage from unrelated prefix announcements, peer-state/RIB metadata at both checkpoints before inferring target route disappearance, and report both coverage-adjusted and sensitivity estimates.
3. **Historic archive completeness not established**: Recording any `EXECUTED` status after returned elements without verifying expected RIB dumps, collector synchronization, update-file intervals and transfer integrity risks partially reconstructed states. Fail closed if missing intervals, source errors, zero original route counts or untraceable timestamp boundaries.
4. **Bootstrap uncertainty is dependent**: `bootstrap_median_ci` resamples collector-peer rows as i.i.d. with no clustering by collector or correlated shared transit. This is not automatically a defensible 95% statistical CI. Reframe these as exploratory resampling intervals until a hierarchical/clustered method and sampling assumptions are justified.
5. **Origin parsing ambiguity**: `origin()` drops nonnumeric tokens, and terminal AS-SET/confederation strings are not explicitly rejected before metrics, despite protocol requiring flag/exclusion. Validate original AS-path representation and fail/flag ambiguous origin conditions.
6. **Non-independent route metrics**: the metric engine sets `ror_strict = pvr_strict` and `ror_lb = pvr_lb` identically by construction. Thus ROR and PVR are duplicate measurements, not independent corroboration. Either define a distinct route observation denominator or report only PVR with a footnote. Synthetic success cannot validate independent ROR.
7. **Proxy source and timing**: The source `stage9_ioda_retention_summary_PROXY_ONLY.csv` contains 2020 raster-digitized ratio values, not native IODA points nor peer-matched structural BGP. Do not feed this into PVR/ROR/USF or cross-event failure propagation claims.
8. **Fallback RIPEstat checkpoints all empty**: Previous input `AS30873_PRE/EVENT/POST...` returned `bgp_state=[]`; furthermore live sanity-tested AS30873, AS3333 and known 8.8.8.0/24 all zero for RIPEstat `bgp-state` in 2020–2024, so the fallback is not a validated source for these timestamps. A 200 `status:ok` envelope does not imply actual route sample retrieval. See https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40244964820

## Exact scope this package supports today
- Reproducible **synthetic logic demonstration** of a state comparator and provenance-aware methodological protocol.
- Audited planning inventory and descriptive 2020 plot-derived IODA proxies.
- No actual 2020 PVR, ROR, upstream switch fraction, prefix withdrawal rate, peer-matched BGP paths, verified AS15412 route-state loss or independent causal cable mapping has been calculated from raw event-time MRT in this ZIP.
- No original IODA `bgp`/`ping-slash24` for 2020 exists in this ZIP.

## Recommended empirical next sequence
1. Repair point-of-observation key and origin/path validation, add synthetic tests with equal peer ASN but different peer IP and lost-monitor scenario.
2. Retrieve **verified** RIPE RIS 2020-01-08 16:00 UTC RIB plus all relevant announcements and withdrawals through event window; validate full dump coverage and preserve original file checksums.
3. Replay an initial `rrc00` pilot subset before expanding to multiple collectors; independently test peer liveness.
4. Only then compute per-vantage route retention and path-switch evidence. Keep USC Trinocular original 2020 reachability and IODA plot proxies as separate sources.

**NO manuscript numerical claims from this archive are approved for release at this checkpoint.**
