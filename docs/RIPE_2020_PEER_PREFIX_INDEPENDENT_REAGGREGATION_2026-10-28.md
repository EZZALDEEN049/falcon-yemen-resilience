# Independent re-aggregation of original RIPE RIS January 2020 peer–prefix exports — 28 October 2026

## Evidence provenance and execution status

The original two-RIB extractor finished for all three collectors and its 18 CSV/JSON files were committed in [commit 907b590](https://github.com/EZZALDEEN049/falcon-yemen-resilience/commit/907b59027807ab292d33886d36e65e2bb07f63c6). The extractor checks all six original RIB SHA-256 digests against hardcoded historical source hashes and gzip CRC before decoding, refuses duplicate peer-IP/ASN/prefix states, and fails if six baseline route counts differ from the earlier independently archived collector runs.

On 28 October 2026 we re-aggregated the actual committed **11,419 row-level CSV observations** by a separate implementation, independently counting retained and changed observations and recomputing every per-prefix and per-peer distribution. All **24** summary-vs-row consistency checks passed (two group levels × changed/comparable numerators and denominators × three collectors × two ASes). Identity and flag consistency tests passed for all six AS-collector subsets. These are computational tests of published outputs, not an independently collected fourth source or proof of continuous peer uptime.

The six source-native RIBs are the RIPE RIS `bview.20200109.0800.gz` and `bview.20200110.0000.gz` for `rrc00`, `rrc01`, `rrc10`; download base `https://data.ris.ripe.net/{collector}/2020.01/`. Complete actual original SHA-256 values are in each collector's `audit.json` and in `docs/TRIPLE_COLLECTOR_RIPE_2020_VALIDATION_2026-10-26.md`.

## Independently re-aggregated within-collector results

All change fractions and medians below are conditional on same-origin retained peer–prefix observations with parsable immediate AS_PATH-neighbor information. Prefix means/medians weight each matched prefix equally. Peer means/medians weight each matched peer (ASN+IP) equally. These units are *not* independent samples.

| Collector | AS | First-origin route rows | Eligible after second-RIB full-peer presence | Retained comparable | Changed | Distinct matched prefixes | Prefix-equal mean | Prefix-equal median | Matched peers | Peer-equal mean | Peer-equal median |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| rrc00 | 30873 | 6611 | 6602 | 6220 | 4157 | 105 | 67.01% | 96.67% | 110 | 67.74% | 69.07% |
| rrc00 | 12486 | 428 | 427 | 366 | 23 | 6 | 6.42% | 1.64% | 62 | 6.18% | 0% |
| rrc01 | 30873 | 2691 | 2582 | 2180 | 1482 | 105 | 68.04% | 100% | 40 | 74.19% | 69.07% |
| rrc01 | 12486 | 179 | 172 | 148 | 6 | 6 | 3.95% | 0% | 26 | 3.85% | 0% |
| rrc10 | 30873 | 1419 | 1419 | 1341 | 868 | 105 | 64.75% | 100% | 23 | 65.34% | 65.98% |
| rrc10 | 12486 | 91 | 91 | 78 | 11 | 6 | 14.10% | 0% | 13 | 14.10% | 16.67% |

Observed number of first-origin peer–prefix rows (both ASes): RRC00=7039, RRC01=2870, RRC10=1510, grand total=11419. The non-retained and excluded rows are not automatically route withdrawals; endpoint absence can reflect other-origin routes or lost sessions.

### Distribution detail: matched prefix-level change fractions

| Collector | AS | Q1 | Median | Q3 | No changes / matched prefixes | 100% changed / matched prefixes |
|---|---|---:|---:|---:|---:|---:|
| rrc00 | 30873 | 8.06% | 96.67% | 100% | 26/105 | 45/105 |
| rrc00 | 12486 | 0.41% | 1.64% | 5.25% | 2/6 | 0/6 |
| rrc01 | 30873 | 4.76% | 100% | 100% | 26/105 | 53/105 |
| rrc01 | 12486 | 0% | 0% | 5.77% | 4/6 | 0/6 |
| rrc10 | 30873 | 0% | 100% | 100% | 30/105 | 53/105 |
| rrc10 | 12486 | 0% | 0% | 17.31% | 4/6 | 0/6 |

This distribution is skewed/bimodal for AS30873. Do not turn the prefix-level "any observer changed" frequency into the peer–prefix fraction.

### Restricting comparisons to the *same historical observing peers*

Join the two AS peer distributions within each collector by the complete pair `(peer_asn, peer_ip)`, and compute `AS30873 neighbor-change percentage - AS12486 neighbor-change percentage` for that same peer.

| Collector | Common peers with retained observations in BOTH ASes | Positive differences | Median paired difference | Interquartile difference |
|---|---:|---:|---:|---|
| rrc00 | 62 | 62/62 | +63.92 percentage points | +51.37 to +69.07 |
| rrc01 | 21 | 21/21 | +69.07 percentage points | +59.79 to +69.07 |
| rrc10 | 13 | 13/13 | +49.31 percentage points | +47.25 to +51.37 |

All **96 collector-specific matched-peers** showed a positive descriptive paired difference. These are NOT 96 independent samples: peers and routes correlate across collectors, and the ASes have sharply different historical prefix inventories (105 versus six), so no standard independent-Bernoulli p-values or causal effect estimate may be inferred.

### Leave-one-prefix-out robustness for the observation-weighted fraction

| Collector | AS30873 range | AS12486 range | Worst-case remaining cross-AS gap |
|---|---:|---:|---:|
| rrc00 | 66.51–67.51% | 1.95–7.57% | +58.94 pp |
| rrc01 | 67.67–68.64% | 1.63–4.92% | +62.75 pp |
| rrc10 | 64.38–65.36% | 4.62–16.92% | +47.46 pp |

Remove *one* eligible matched prefix from each AS's prefix distribution at a time; this is descriptive perturbation, not formal statistical inference. The gap remains positive but the highly unequal prefix universes prohibit asserting a common causal contrast.

## Reviewer-ready interpretation

Original six-RIB, peer-IP-qualified evidence confirms that the scale of observed origin-adjacent AS_PATH-neighbor changes in AS30873 greatly exceeds the observed changes in AS12486 across the three collectors, including prefix-equal and peer-equal summaries and within-identical-peer descriptive contrasts. This strengthens the network-specific **control-plane reconfiguration** finding.

It **does not** prove that the FALCON cable break caused each changed route; provide user reachability; imply route disjointness; estimate all internet paths; demonstrate continuously healthy peer sessions; or claim 105 and six prefixes form comparable samples. The full 16-hour intermediate A/W event-state replay remains separately available for RRC00 only.

## Original source exports, each complete and commit-addressed

- [RRC00 row-level data](https://github.com/EZZALDEEN049/falcon-yemen-resilience/blob/main/results/ripe2020_peer_prefix_original/rrc00/BGP_2020_peer_prefix_records.csv)
- [RRC00 per-prefix distribution](https://github.com/EZZALDEEN049/falcon-yemen-resilience/blob/main/results/ripe2020_peer_prefix_original/rrc00/BGP_2020_prefix_distributions.csv)
- [RRC00 per-peer distribution](https://github.com/EZZALDEEN049/falcon-yemen-resilience/blob/main/results/ripe2020_peer_prefix_original/rrc00/BGP_2020_peer_distributions.csv)
- [RRC01 row-level data](https://github.com/EZZALDEEN049/falcon-yemen-resilience/blob/main/results/ripe2020_peer_prefix_original/rrc01/BGP_2020_peer_prefix_records.csv)
- [RRC01 per-prefix distribution](https://github.com/EZZALDEEN049/falcon-yemen-resilience/blob/main/results/ripe2020_peer_prefix_original/rrc01/BGP_2020_prefix_distributions.csv)
- [RRC01 per-peer distribution](https://github.com/EZZALDEEN049/falcon-yemen-resilience/blob/main/results/ripe2020_peer_prefix_original/rrc01/BGP_2020_peer_distributions.csv)
- [RRC10 row-level data](https://github.com/EZZALDEEN049/falcon-yemen-resilience/blob/main/results/ripe2020_peer_prefix_original/rrc10/BGP_2020_peer_prefix_records.csv)
- [RRC10 per-prefix distribution](https://github.com/EZZALDEEN049/falcon-yemen-resilience/blob/main/results/ripe2020_peer_prefix_original/rrc10/BGP_2020_prefix_distributions.csv)
- [RRC10 per-peer distribution](https://github.com/EZZALDEEN049/falcon-yemen-resilience/blob/main/results/ripe2020_peer_prefix_original/rrc10/BGP_2020_peer_distributions.csv)

All links require repository permission while private.
