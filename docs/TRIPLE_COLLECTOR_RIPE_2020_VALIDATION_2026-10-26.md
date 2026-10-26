# Triple-collector source-original 2020 RIPE RIS BGP validation — 26 October 2026

## Reproducible source and time boundaries
All runs use the same native MRT collection definition on **three independent RIS collector machines**, the 2020-01-09 **08:00 UTC** full RIB snapshot and the 2020-01-10 **00:00 UTC** full RIB snapshot. The first is before *reported* visible gradual decline at ~09 UTC in published 2020 outage reporting, not an independently proven physical-cable-cut time. The second is after the 18 UTC severe active-probing impact reported in the same contemporary source.

Official source: https://ris.ripe.net/docs/mrt/
Event report: https://internetdisruption.report/2020/02/23/internet-disruption-report-january-2020/

### Original source file provenance (full gzip CRC verified, bytes and SHA-256)
| Collector | 2020 historical filename | Original bytes | Full SHA-256 |
| --- | --- | ---: | --- |
| rrc00 | bview.20200109.0800.gz | 628186527 | a55cfb90f54c38452f851f6a13c8a96bd93e8a3f4aeedb48e84357b31d5e05d2 |
| rrc00 | bview.20200110.0000.gz | 627746537 | 3d2147cc860c534829cd89beec115487d97281c45c2a520d8c7469bb605fd38c |
| rrc01 | bview.20200109.0800.gz | 211083656 | eb2910a382dd21a537a971145734a6c3a00ccd035e17261643eb3f2359750d7c |
| rrc01 | bview.20200110.0000.gz | 200387843 | 00086b6f66483d8f7860ea841bba2cdfdcf4e4a3887b9f677957b32f3123c2cb |
| rrc10 | bview.20200109.0800.gz | 106261086 | d76503427bde035a55ae0f540ee2c1a683b7c068c55547669e947313a423d33d |
| rrc10 | bview.20200110.0000.gz | 106610362 | f7f08e3bc76d9d70ab541261bb32b335e6ba7c340fe1a0310df343c990a08671 |

Downloader/parser: `tools/peer_qualified_rib_2020.py`, using `pybgpkit-parser` from PyPI. Peer identity is `(collector, peer_asn, peer_ip)` (collector is isolated by run). Peer existence in a snapshot is measured by **any BGP route in that full MRT RIB** before selecting target-origin ASN and prefix. Ambiguous origins, duplicate peer-prefix routes, empty/bad downloads trigger failure.

Verified independent runs:
- RRC00: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40248087605
- RRC01: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40248495385
- RRC10: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40248686102

## Same-peer same-prefix origin visibility between two checkpoints
Observations are *BGP collector route rows* (peer-prefix samples), not independent paths, packet traffic, or users. Exact denominator includes only target-origin observations from first full RIB where the **same peer has any route** in second full RIB.

| AS | RRC | eligible pre target-origin observations | same-peer-prefix target-origin post | ratio | immediate-neighbor ASN changed among same-origin observations | distinct prefix changed / common |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| AS30873 | rrc00 | 6602 | 6220 | **94.21%** | **4157/6220 = 66.83%** | 79/105 |
| AS30873 | rrc01 | 2582 | 2180 | **84.43%** | **1482/2180 = 67.98%** | 79/105 |
| AS30873 | rrc10 | 1419 | 1341 | **94.50%** | **868/1341 = 64.73%** | 75/105 |
| AS12486 | rrc00 | 427 | 366 | **85.71%** | 23/366 = 6.28% | 4/6 |
| AS12486 | rrc01 | 172 | 148 | **86.05%** | 6/148 = 4.05% | 2/6 |
| AS12486 | rrc10 | 91 | 78 | **85.71%** | 11/78 = 14.10% | 2/6 |

## Directly observed AS_PATH adjacency transitions

The **ASN immediately preceding target origin AS30873** in the observed BGP AS_PATH shifted as follows on matched peer-prefix observations:

| Collector | pre adjacent AS15412 | post adjacent AS15412 | pre adjacent AS174 | post adjacent AS174 | AS15412 → AS174 transitions |
| --- | ---: | ---: | ---: | ---: | ---: |
| rrc00 | 2793 | **0** | 2063 | **6220** | **2793** |
| rrc01 | 1089 | **0** | 698 | **2180** | **1089** |
| rrc10 | 593 | **0** | 473 | **1341** | **593** |

The remaining pre AS30873 neighbors AS3491/AS8529 also shifted to AS174 on retained observations. Across all three collectors, **no matched post AS30873 observation kept AS15412 as immediate AS_PATH predecessor**, whereas **all retained observations had AS174 adjacent at the second checkpoint**.

AS12486 *did not display the same universal adjacency change*: retained post observations with adjacent AS15412 numbered **279/366 (rrc00)**, **120/148 (rrc01)**, and **51/78 (rrc10)**.

### Scientific interpretation, not overreach
**Supported**: a source-original, cross-collector reproducible and network-specific BGP adjacency change concurrent with the documented January 2020 disruption. This is independent context corroborating earlier contemporaneous reports of AS15412 upstream loss and alternative upstream routing for AS30873.

**NOT supported**: that any given cable break physically caused a specified BGP AS_PATH edge to disappear, that AS174 is a physically disjoint/capacity-adequate failover cable, that users could actually connect, that global BGP retained a particular fraction, or that BGP peers represent independent samples from the whole Internet. AS_PATHs are control-plane representations and can reflect policy choices not user packet forwarding.

**Critical remaining BGP limitation**: these are two source-original full-RIB **snapshots** plus separately audited limited update files. They are **not** a complete MRT A/W replay across every intermediate five-minute interval. A source file can contain routes to a prefix with another origin, so no-origin-in-second-snapshot does not necessarily mean a withdrawal. Peer presence in both snapshots also does not prove uninterrupted session operation between them.

**Critical remaining cross-layer limitation**: direct *source-native IODA 2020* `bgp` / `ping-slash24` is still unrecovered; published-figure IODA 2020 values are digitized proxies, and source-original IODA Nov 2023 is a distinct event. USC Trinocular 2020 original active probes require institutional data-use authorization.

## Scientific contribution candidate, bounded
Multi-collector observed BGP origin/neighbor continuity with a notable AS30873 neighbor change and AS12486 contrast; combined with source-qualified published IODA active reachability proxies and documentary evidence, this supports an **evidence-bounded structural–functional divergence case study**, not a novel universal cable-failure causal model.

## Other source-original timing results
- The original 2020 RRC00 archive also yielded full gzip-verified A/W update samples and **48 contiguous five-minute updates across two separate two-hour windows** (07–09 UTC, 17–19 UTC; gap not covered).
- In candidate historical origin prefix universe (109 AS30873 and 7 AS12486 prefixes), 07–09 UTC count was 1623 AS30873-origin A + 110 AS12486-origin A and zero W; 17–19 count was 572 AS30873-origin A + 237 AS12486-origin A, 3 W for AS12486 candidate prefixes and 0 W for AS30873 candidate prefixes. This is a *prefix-scoped source observation*, not absence of all withdrawals or a cause.
- Source run https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40248133135

Only validated claims may be integrated into final manuscript; author requested no intermediate artifact delivery.
