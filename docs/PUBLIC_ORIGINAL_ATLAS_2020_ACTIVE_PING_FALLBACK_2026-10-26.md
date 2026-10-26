# No-custodian fallback for January 2020 native IODA gap — independent original active-ping recovery

**Date:** 2026-10-26. **Strict source classification: RIPE Atlas is NOT IODA.**
**Current IODA 2020 native state:** Unrecovered despite API/archive tests. This note records actual public independent 2020 ICMP data, not a recovery of IODA's native `ping-slash24` or `bgp`.

## Authentic source-original public ICMP result found NOW
Original publicly accessible RIPE Atlas measurement ID **8307351**, ping target IPv4 **195.94.0.34**, catalog target AS **12486** (TeleYemen). Query https://atlas.ripe.net/api/v2/measurements/8307351/results/?start=1578441600&stop=1578873599 .

- UTC window **8 Jan 2020 00:00–13 Jan 2020 00:00 (exclusive)**.
- Returned **3,360 timestamped source results**, across **seven RIPE Atlas probing IDs**, independently traceable to the measurement ID. Each result contained one sent ICMP packet (`sent=1`), `rcvd=0` or `1`.
- **3,343** results had at least one received reply; **17** did not.
- Historical results were retrieved from RIPE Atlas public original results API, not inferred from screenshots.
- Reproducible Python tool: `tools/ripe_atlas_2020_source_active_ping_audit.py`.
- Two source-audit runs https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40330126740 and https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40330653011 (source-response SHA256, probe list, daily and hourly data in archived audit).

| UTC date in January 2020 | Original test results | Positive reply | No reply | Reply fraction for this *single destination* |
| --- | ---: | ---: | ---: | ---: |
| Jan 08 | 673 | 663 | 10 | 98.51% |
| Jan 09 | 672 | 670 | 2 | 99.70% |
| Jan 10 | 672 | 669 | 3 | 99.55% |
| Jan 11 | 672 | 670 | 2 | 99.70% |
| Jan 12 | 671 | 671 | 0 | 100% |
| **All five days** | **3,360** | **3,343** | **17** | **99.49%** |

These values **must never be titled** `Yemen reachability`, `AS12486 reachability`, `/24 reachability fraction`, `IODA 2020 active probing`, or independent observations across 3,360 networks. They concern **one target IPv4 and seven probing IDs** and different sources/vantage coverage. The catalog ASN is a metadata value; the historical origin on each date requires separate routing verification if a stronger assertion is needed. The result is a narrowly useful independent *single-target control*, not country-wide inference.

## Rigorous negative tests for the primary Yemeni ASN, AS30873
- The public RIPE Atlas measurement discovery endpoint for `target_asn=30873&type=ping` returned **27** catalog entries, many individual stopped tests with April 2019 start timestamps; the first three had **zero** raw results in Jan 8–12, 2020. Do not infer the others were exhaustive; a wider search may still recover relevant historic targets using prefix/IP rather than current ASN metadata.
- Source catalog included five RIPE Atlas probes currently associated with AS30873 (13655, 14138, 14148, 14176, 26226), and two with AS12486 (14193, 17661). A historical public RIPE Atlas built-in IPv4 ICMP sample for measurement IDs **1001**, **1009**, **1010**, probed by each of these seven probe IDs, yielded **zero** native source-probe results over Jan 8–12, 2020. **This does not prove network-wide probe outage**: some devices may have been retired before 2020; latest probe ASN is not a documented historical time-specific mapping, and no actual measurement samples were returned. Run https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40330905956 .
- Source information about RIPE Atlas built-in root-server ping measurements: https://atlas.ripe.net/docs/getting-started/built-in-measurements
- Result history source API: https://atlas.ripe.net/docs/apis/rest-api-manual/measurements/results-and-latest/
- **Original IODA 2020 native BGP and ping-slash24 series remain uncollected.** No public substitute may be mislabeled IODA original.


### Historical-origin-prefix exhaustive public ping search (additional negative test)
We also searched RIPE Atlas by **all 109 original 2020 RRC00 AS30873 origin candidate prefixes**, avoiding the weaknesses of current `target_asn` indexing. All 109 public per-prefix catalog requests returned without API errors; they collectively disclosed **112 unique candidate ping measurement IDs**. We queried the actual original archived ping result endpoint for **all 112** IDs for 8–12 January 2020 and **none returned observations in that window**. Source-native logged test: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40331800608; script `tools/find_2020_public_atlas_for_original_as30873_prefixes.py`.

**Precise scope of this negative evidence:** each queried prefix catalog was limited to its first **80** entries (pagination not exhausted), the input included only **109 historically discovered RRC00 prefixes**, the indexing semantics can omit other measured targets and 2020 AS assignments, and only published public RIPE Atlas tests were checked. Thus we cannot assert no other 2020 active measurements exist; we can assert these **112 specific public measurements** returned none for the chosen window.

## No-email, scientifically defensible use
1. **Primary control plane (original)**: six native Jan 2020 RIPE RIS RIB snapshots from RRC00/01/10, with replicated immediate-AS_PATH-neighbor shift for AS30873 from AS15412 to AS174. RRC00 192 genuine 5-minute A/W files fully replayed and matched authenticated next RIB, per repository evidence manifests.
2. **Limited independent active example (original)**: RIPE Atlas ping measurement 8307351 of one target in catalog-AS12486, five days, 7 probing IDs, daily counts above. No claim that this dataset represents AS30873 functional connectivity; the observed near-complete response is consistent with one reachable test target only.
3. **Published 2020 IODA data**: retain digitized figure estimates with measurement and digitization uncertainty, publication provenance, and clear labels `plot digitization proxies`. Do not call raw source samples or regress them together as if commensurate with RIS/Atlas.
4. **Final claim**: `2020 cross-collector control-plane adjacency changes were reconstructed from native MRT, while independently published active reachability evidence was available only through digitized plots for the primary affected AS; a public Atlas single-target control supports only that specific control address remained mostly reachable.` NO native source IODA numeric recovery claim; NO cable causal certainty.
5. **Paper can progress now** with an explicit Data Availability/Limitations statement instead of waiting on unreturned emails. IODA/USC archival authorization is valuable for stronger inference but not a prerequisite for an honestly bounded descriptive case study, subject to publication suitability assessment.

## Further methods needed before journal submission
- Check whether targeting particular 2020 historic /24s yields other public RIPE Atlas measurements not indexed by target ASN today; don't announce universal nonavailability.
- Verify historical source AS for RIPE Atlas 8307351 target IPv4 at Jan 2020 through original RIS route data before mapping strongly to TeleYemen.
- The 3,360 ICMP test results cluster by probe and target; no independent-binomial 95% confidence interval; compute probe-by-time sensitivity if desired, rather than national statistical estimates.
- Review data licensing/citation of source-original RIPE Atlas measurement; cite RIPE Atlas directly, separately from IODA.
