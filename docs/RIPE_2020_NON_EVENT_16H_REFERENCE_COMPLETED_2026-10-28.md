# FALCON: pre-outcome-fixed 16-hour 2020 historical reference vs Jan 9–10 route-adjacency contrast

**Date of audit:** 28 October 2026.  
**Source:** Six new gzip-CRC-verified RIPE RIS MRT bview files at **2 Jan 2020 08:00 UTC** and **3 Jan 2020 00:00 UTC** for RRC00, RRC01, RRC10; six already frozen original files at 9 Jan 08:00 and 10 Jan 00:00 UTC. The reference window was selected and committed before its outcomes were inspected. This is a single historical reference, not a population distribution of normal churn or an assured incident-free interval.

| RRC | AS | 2–3 Jan changed / comparable | 2–3 Jan rate | 9–10 Jan changed / comparable | 9–10 Jan rate | Difference pp | Exact peer ASN/IP/prefix intersection | Difference on same keys pp |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| RRC00 | 30873 | 29/6047 | 0.48% | 4157/6220 | 66.83% | +66.35 | 5965 | +66.67 |
| RRC00 | 12486 | 0/410 | 0.00% | 23/366 | 6.28% | +6.28 | 349 | +6.59 |
| RRC01 | 30873 | 23/2549 | 0.90% | 1482/2180 | 67.98% | +67.08 | 2180 | +66.97 |
| RRC01 | 12486 | 0/172 | 0.00% | 6/148 | 4.05% | +4.05 | 143 | +4.20 |
| RRC10 | 30873 | 6/1464 | 0.41% | 868/1341 | 64.73% | +64.32 | 1341 | +64.35 |
| RRC10 | 12486 | 0/97 | 0.00% | 11/78 | 14.10% | +14.10 | 78 | +14.10 |

The original source extracted **10,968 reference first-snapshot peer–prefix rows** and the event extraction retained **11,419 first-snapshot rows**. The 12 original RIB source URLs, SHA-256, sizes, peer coverage and extraction exclusions are traceable in each collector's source `audit.json`.

**Immutable evidence**:
- Non-event source output commit: [e7d0f51729ef8fffe138fa7fc34a3130455e1ad2](https://github.com/EZZALDEEN049/falcon-yemen-resilience/commit/e7d0f51729ef8fffe138fa7fc34a3130455e1ad2)
- Original event source output commit: [907b59027807ab292d33886d36e65e2bb07f63c6](https://github.com/EZZALDEEN049/falcon-yemen-resilience/commit/907b59027807ab292d33886d36e65e2bb07f63c6)
- Script with fixed reference dates prior to examining results, [source](https://github.com/EZZALDEEN049/falcon-yemen-resilience/blob/55c02029f7fc0e41c94655a2f131adbac4f2df2a/tools/ripe2020_non_event_20200102_20200103.py).

**Scientific interpretation:** These data show that the event-associated snapshot interval had much greater origin-adjacent AS_PATH reconfiguration than the particular one-week-earlier interval in all three collectors. The reference is **not** a causal control, the two observed intervals contain dependent prefix/peer observations, different origin prefix inventories and collector coverage; no inferential p-value or source-confirmed physical cable path can follow. Further non-event reference windows and event-time observations would improve inference. Do not confuse initial-row coverage, comparable-route denominators, target-origin absence, and explicit withdrawals.