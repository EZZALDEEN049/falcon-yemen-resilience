# Original historical 2020 BGP evidence — source-validated interim research audit (26 October 2026)

## Why this is substantively new evidence
The study previously relied on plot digitization of published IODA graphs for **January 2020**. We now obtained, checksum-verified, decoded, and compared **original 2020 RIPE RIS MRT BGP data**. This is **independent of and not a recovery of original IODA**. A single RIPE collector does not substitute for active reachability.

Raw source: `rrc00` at `https://data.ris.ripe.net/rrc00/2020.01/`. Official MRT format and interval docs: https://ris.ripe.net/docs/mrt/.

Published event timing for external context: Internet Disruption Report (2020) observed gradual deterioration **around 09:00 GMT**, stronger active-probing impacts near **18:00 GMT** on 9 January; https://internetdisruption.report/2020/02/23/internet-disruption-report-january-2020/. We cannot assign an exact physical-cut timestamp from those plotted observations.

## Two original full RIB snapshots, integrity validated
Source BGP snapshots:
- `bview.20200109.0800.gz`, 628,186,527 bytes, original SHA256 `a55cfb90f54c38452f851f6a13c8a96bd93e8a3f4aeedb48e84357b31d5e05d2`, gzip CRC passed, 53,257,223 total original route elements.
- `bview.20200110.0000.gz`, 627,746,537 bytes, SHA256 `3d2147cc860c534829cd89beec115487d97281c45c2a520d8c7469bb605fd38c`, gzip CRC passed, 53,015,538 total original route elements.
- All-prefix peer identities, defined by `(peer_asn,peer_ip)` at RRC00, checked independent of each target origin: 132 first, 129 second, 129 common.
- Source script: `tools/peer_qualified_rib_2020.py`. Passing archived run: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40247341314.

### Strict same-peer, same-prefix, same-origin observations

Define the source-specific two-snapshot retention ratio for AS `a`, counting peer-prefix observations rather than independently sampled networks:

\[ R_a = \frac{\#\{(peer,prefix):\ \\mathrm{origin}_{t0}=a\ \land\ \mathrm{origin}_{t1}=a\ \land\ peer\ observed\ at\ t1\}}{\#\{(peer,prefix):\ \\mathrm{origin}_{t0}=a\ \land\ peer\ observed\ at\ t1\}} \]

This is **not** the IODA BGP metric, active probing, independently sampled routes, or the percentage of affected users. Last-hop ASN change is computed **only** for keys visible with the same target origin in both snapshots.

| Source-native historical RRC00 observation | AS30873 | AS12486 |
| :--- | ---: | ---: |
| Original RIB origin rows at first checkpoint | 6,611 | 428 |
| Original RIB origin rows at second checkpoint | 6,220 | 366 |
| Initial target peers still present with **any-origin route** in second full RIB | 119/121 | 116/117 |
| First route observations eligible after peer coverage filter | 6,602 | 427 |
| Same peer-prefix with target origin still visible at second checkpoint | 6,220 | 366 |
| Source-specific route observation retention | **94.21%** | **85.71%** |
| Peer-equal-weight median source-specific retention | **96.04%** | **85.71%** |
| Matched origin observations with different penultimate ASNs between RIB snapshots | **4,157 / 6,220 (66.83%)** | **23 / 366 (6.28%)** |

Thousands of peer–prefix route observations are correlated. These ratios are descriptive, not confidence intervals or 6,220 independent experiments; peers visible at both endpoints need not remain active throughout the entire window. Immediate-upstream inference from an AS path is **not** evidence of a physical submarine-cable route or the actual packet-forwarding path.

## Substantial original AS_PATH finding: AS30873's immediate neighbor ASN

A second full peer-liveness-qualified execution, independently replaying both original RIB snapshots, shows that among **6,220 same-peer same-prefix route observations with unchanged origin AS30873**, the ASN immediately before 30873 in the observed `AS_PATH` changed as follows:

| Immediate AS_PATH neighbor | 9 Jan 08:00 UTC | 10 Jan 00:00 UTC |
| --- | ---: | ---: |
| AS15412 | **2,793** | **0** |
| AS174 | 2,063 | **6,220** |
| AS3491 | 729 | 0 |
| AS8529 | 635 | 0 |

- **2,793** observed `AS15412 → AS174` neighbor transitions on matched peer-prefix-origin routes.
- **729** observed `AS3491 → AS174` and **635** `AS8529 → AS174` transitions.
- **2,063** already showed `AS174 → AS174` unchanged across checkpoints.
- **79 of 105** shared prefixes had at least one observed neighbor ASN change, **100 of 110** independently covered matched peer sessions had at least one neighbor change.
- AS30873 peer-equal-weight median fraction of changed matched observations: **69.07%**. Prefix-equal-weight median fraction: **96.67%** (interpret with strong within-prefix clustering; these are descriptive distributions).
- AS12486 is strikingly different: adjacent AS15412 appeared in **302 of 366** matched observations at first checkpoint and **279 of 366** second; only **23 of 366** matched observations changed, including **12 AS15412→AS197206** and **11 AS15412→AS6762**. Peer-equal-weight median fraction of changed observations: **0%**.

**Interpretation guardrails:** AS_PATH neighbor is an observation about control-plane topology, not a verified contractual upstream, physical fiber route, actual data traffic, user connectivity or causal mechanism. These are peer-prefix repeated observations (non-independent); the matched set may not represent all announcements from either ASN. An outage report published contemporaneously mentions AS15412 upstream loss, and this source-original route result is consistent with the reported rerouting **without independently proving the cable failure caused each observed path change**.

Validated re-run: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40248087605, `tools/peer_qualified_rib_2020.py`. Numeric source checksums and complete original-RIB methodology included in archived job artifact.

## Original MRT A/W update records — provenance test
- Downloaded and verified six original 5-minute RRC00 `updates` files in a separate trial (08:55 and 17:55–18:15 UTC), each gzip CRC plus SHA256.
- 48 original 5-minute update files passed an expanded scope test covering **07:00–09:00 UTC** (24 consecutive files) and **17:00–19:00 UTC** (24 consecutive files) on Jan 9. The eight-hour gap between these two windows is **not covered** by this test. Scope uses 109 AS30873 + seven AS12486 prefixes discovered by a Jan 9 RRC00 historical RIB; **not an exhaustive national prefix universe**.
- Run https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40248133135; script `tools/ripe_2020_historical_candidate_update_sample.py`.
- 07–09 UTC original source announcements: AS30873-origin candidate prefixes **1,623**, AS12486 **110**; no candidate-prefix W.
- 17–19 UTC: AS30873 **572** announcements, AS12486 **237**; **three withdrawal observations involving** candidate prefixes of AS12486 and **zero** withdrawal observations involving candidate prefixes of AS30873. Every BGP withdrawal record is inherently *origin-unspecified*: the same prefix may have been announced from another origin; the record must not be automatically assigned to AS12486 as withdrawn origin.
- The 48-file observation covers two separate fixed intervals only; it cannot establish continuous changes between those windows, an event-window-wide absence of withdrawals, or source-original 2020 IODA reachability values.

## Manuscript-safe conclusions
1. At RRC00, AS30873 **remained widely visible by same-peer and same-origin prefix observations** between these two historical checkpoints, while the immediate upstream AS within many still-visible AS paths changed.
2. Two-snapshot prefix-origin retention and upstream-AS changes are complementary control-plane evidence, not interchangeable with capacity, normalized IODA BGP visibility or active probing.
3. The original RIPE result may be discussed as **new single-collector historical contextual evidence** supporting the thesis that structural routing visibility can persist under reported substantial service deterioration. However the causal cable–path association, physical path redundancy, nationwide representativeness and exact timing of individual control-plane changes are **not established by the present datasets**.
4. No original IODA 2020 BGP/ping numeric series has been recovered. **Do not relabel RIPE MRT or USC Trinocular original measurements as IODA source-native samples**.
5. Stronger paper result requires third-party peer-cluster robustness, independent RIS collectors, complete unfiltered A/W replay for tracked historical prefixes and an independently acquired 2020 active-probing dataset.

## Repeatability
- All downloaded 2020 source MRT archives cryptographically hashed and verified with full gzip CRC.
- Archived GitHub Actions retain numeric manifests for 30 days; if retaining source-local audits for a manuscript, deposit checksum manifests separately as authorized.
- The user requested **no intermediate Word/PDF/ZIP deliverables**, so audit kept inside research repository only.
