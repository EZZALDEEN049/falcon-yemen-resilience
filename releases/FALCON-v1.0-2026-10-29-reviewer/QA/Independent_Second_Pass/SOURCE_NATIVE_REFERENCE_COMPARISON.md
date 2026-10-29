# Non-event 16-hour historical RIPE RIS baseline: evidence audit

**Reference window:** 2020-01-02 08:00 UTC → 2020-01-03 00:00 UTC. **Event-associated window:** 2020-01-09 08:00 UTC → 2020-01-10 00:00 UTC.
The reference date was frozen in the research repository before examination of its outputs; one reference window is not a statistical estimate of ordinary variation.
Source: six historical reference MRT RIBs and the previously published six event MRT RIBs; individual peer-prefix AS_PATH adjacency observations.
The comparisons below are descriptive only. Neither baseline period is guaranteed to have zero unrelated network incidents, nor does a large difference identify a specific cable mechanism.

| Collector | Origin AS | Event changed/comp. | Reference changed/comp. | Event % | Reference % | Difference pp | Fixed-comparable peer-prefixes | Fixed-cohort Δ pp |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| RRC00 | 30873 | 4157/6220 | 29/6047 | 66.83 | 0.48 | 66.35 | 5965 | 66.67 |
| RRC00 | 12486 | 23/366 | 0/410 | 6.28 | 0.00 | 6.28 | 349 | 6.59 |
| RRC01 | 30873 | 1482/2180 | 23/2549 | 67.98 | 0.90 | 67.08 | 2180 | 66.97 |
| RRC01 | 12486 | 6/148 | 0/172 | 4.05 | 0.00 | 4.05 | 143 | 4.20 |
| RRC10 | 30873 | 868/1341 | 6/1464 | 64.73 | 0.41 | 64.32 | 1341 | 64.35 |
| RRC10 | 12486 | 11/78 | 0/97 | 14.10 | 0.00 | 14.10 | 78 | 14.10 |

## Interpretation gate
- Changed neighbor is origin-adjacent AS_PATH at **two RIB endpoints**, not data-plane or cable observations.
- Event and reference route populations differ; fixed-key comparison is supplemental and conditions on presence in both periods and endpoints.
- AS12486 has a distinct six-prefix inventory vs AS30873 ≈105 prefixes; it is not a causal control.
- Peer-route records overlap across collectors and prefix groups; no p-value or independent-sample CI is computed.
- Multiple non-event windows would be preferable for characterizing the *distribution* of ordinary churn.
- The original six source filenames, URLs, sizes and hashes are recorded in Original_RIB_Source_And_Hashes.json.
