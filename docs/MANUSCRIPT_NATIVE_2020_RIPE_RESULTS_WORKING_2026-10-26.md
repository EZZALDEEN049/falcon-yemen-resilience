# Working manuscript section — original January 2020 BGP observations

**INTERNAL WORKING TEXT. Not a submitted manuscript or a recovery of IODA's 2020 original signal data.**

## Source data and reproducibility

We obtained source-native MRT routing data from RIPE RIS for 9–10 January 2020. Three independently located RRC collectors (`rrc00`, `rrc01`, `rrc10`) each supplied two 2020 RIB dumps, at 08:00 UTC on January 9 and 00:00 UTC on January 10, retaining source URL, byte length and SHA-256. Full gzip streams passed integrity checks. Native BGP record decoding used `pybgpkit-parser`, with collector/peer-ASN/peer-IP identity retained.

For each ASN `a`, we established historical prefixes by origin-AS membership in the first RIB (not from contemporary topology). A candidate observation is a tuple `(collector, peer_asn, peer_ip, prefix)` whose AS_PATH resolves unambiguously to origin ASN `a`. We considered a first-checkpoint observation eligible only if the same peer was observed with **any BGP origin** in the second **full** RIB, to reduce false disappearances from collector peer dropouts. We measured retention of the original peer-prefix-origin tuple at the second checkpoint. The result is a two-snapshot, single-collector descriptive view, **not IODA's visible /24 BGP index**, a user reachability statistic, a full event-time state replay, or proof of uninterrupted peer uptime.

Among observations retained with the same origin at both checkpoints, we compared the immediately preceding ASN in the reported AS_PATH. Repeated peer-prefix observations are correlated, so we report the numerator and denominator, alternative peer-balanced summaries and independent RRC views rather than claiming route counts are independent samples or computing conventional binomial confidence intervals.

## Original 2020 routing findings

| 2020 RIPE RRC | AS30873 matched-route observations | AS30873 immediate-AS_PATH-neighbor change | AS12486 matched-route observations | AS12486 immediate-AS_PATH-neighbor change |
| --- | --- | --- | --- | --- |
| rrc00 | 6,220/6,602 (94.21%) | 4,157/6,220 (66.83%) | 366/427 (85.71%) | 23/366 (6.28%) |
| rrc01 | 2,180/2,582 (84.43%) | 1,482/2,180 (67.98%) | 148/172 (86.05%) | 6/148 (4.05%) |
| rrc10 | 1,341/1,419 (94.50%) | 868/1,341 (64.73%) | 78/91 (85.71%) | 11/78 (14.10%) |

Across all three collectors, on **matched AS30873 observations**, no retained route had AS15412 as the ASN immediately before AS30873 at the second checkpoint; every retained route had AS174 adjacent. Earlier matched AS30873 observations showed adjacent AS15412, AS174, AS3491 and AS8529. Specifically, paired AS15412→AS174 transitions numbered 2,793 (rrc00), 1,089 (rrc01) and 593 (rrc10) **route observations, not independent distinct prefixes**. Some 79/105 matched AS30873 prefixes showed at least one neighbor change in rrc00 and rrc01, versus 75/105 in rrc10. This robust cross-collector observation is **consistent with** the contemporaneous incident report's account of upstream-change behavior, but the original AS_PATH evidence does not establish a physical cable route, the precise cause of each update, or a functioning backup path for customer traffic.

**AS12486 contrasted structurally**: despite reductions in some observed origins, its AS15412 adjacency was retained in 279/366 (rrc00), 120/148 (rrc01) and 51/78 (rrc10) matched source-route observations at the second checkpoint. RRC00 and RRC01 alone therefore would not support the claim that this AS was "unaffected" in every BGP dimension. The earlier plot-digitized 2020 IODA active-probing median of 100% is an *incomparable measurement family*, and should not be conflated with MRT prefix-route retention.

## Complete 08:00–00:00 UTC original MRT UPDATE interval audit

We independently retrieved **192 consecutive original five-minute RRC00 UPDATE archives** (all 8 two-hour partitions passed), validated the archive gzip integrity and original SHA-256 file hash, and permanently preserved the resulting 192-fingerprint data-custody audit in `results/ripe_2020_source_original_16h_aw_manifest.json`. RIPE RIS MRT source naming and five-minute update cadence are documented at https://ris.ripe.net/docs/mrt/.

Restricting extraction to **109 AS30873 + 7 AS12486 historically discovered candidate prefixes**, the sixteen-hour dataset included 102,836 announcements with explicit AS30873 origin and 2,859 announcements with explicit AS12486 origin. Source-prefix-related withdrawal messages numbered 4,904 and 120, respectively; **withdrawal messages contain no origin AS**, so an observation involving a prefix in the AS30873 candidate set cannot be asserted to be an AS30873-origin withdrawal without replaying the prior peer-prefix state. Five-minute candidate-prefix update bursts were prominent at **09:55, 19:35, 19:50 and 20:40 UTC**; these are message-count peaks and cannot be equated to reachability-loss peaks or independent cable-induced events.

Completeness of the sixteen-hour RRC00 archive was subsequently verified by **end-to-end historical RIB + A/W update replay** for the explicitly selected historical prefix universe. All **192** original five-minute update files were individually checksum/CRC verified; **110,719** source-native, candidate-prefix-matched update messages were decoded, consisting of **105,695** announcements and **5,024** withdrawals (withdrawal origins undefined). Replaying these messages against the authenticated 2020-01-09 08:00 UTC RIB produced **6,586** peer-prefix states among the independently observed end-snapshot peer sessions, matching **all 6,586** states in the original 2020-01-10 00:00 UTC RIB for this candidate universe with **zero origin mismatches** and **zero AS_PATH mismatches**. This is a **deterministic checkpoint reconciliation for RRC00 and 116 candidate historic prefixes**, not proof of continuously healthy peer sessions, nationally complete routing, data-plane reachability, or physical-cable causality. The snapshot-relative route retention and next-hop adjacency descriptions remain source-scoped descriptive evidence; we do not infer end-to-end user service availability from them. Reproducibility: `results/ripe_2020_full16h_replay_checkpoint_audit.json`, `tools/ripe_2020_full16h_event_state_reconcile.py`, and https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40251606127 .

## Public source-original RIPE Atlas active-ping control: limited, single destination

Because original 2020 IODA `ping-slash24` samples could not be retrieved from tested public endpoints, we independently audited public historical RIPE Atlas ICMP measurements. Public RIPE Atlas measurement **8307351**, catalog target-AS **AS12486**, probed the single address **195.94.0.34** from **seven different probing IDs**. It returned **3,360** dated ping results during **8–12 January 2020 UTC**, with **3,343** reporting a reply and **17** not reporting a reply. On January 9, **670 of 672** results contained a reply. These measurements are source-original RIPE Atlas observations, **not source-original IODA active /24 reachability or USC Trinocular records**. They offer a narrowly defined reachable-control address only; one address cannot represent all AS12486 or Yemen, and the clustered probe events cannot be treated as independent networks.

The public RIPE Atlas query for historical `target_asn=AS30873` yielded mostly stopped catalog measurements without validated source results in the first examined entries for the 2020 window; a targeted test of several currently AS30873-catalogued source probes against three built-in root-server ping measurements returned no historical samples. These limited negative tests do **not** prove there were no public historic AS30873 probes, or that AS30873 was offline. We therefore **do not** present any recovered numerical active-ping estimates for AS30873 under the RIPE Atlas program. The manuscript's primary affected-AS functional evidence remains source-qualified 2020 published IODA plot digitization, with uncertainty explicitly disclosed. Original data provenance and original-test logs: `docs/PUBLIC_ORIGINAL_ATLAS_2020_ACTIVE_PING_FALLBACK_2026-10-26.md`, https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40330653011 .

## Interpretation and limitations

Original source-routed control-plane observations now supplement, rather than replace, the manuscript's **plot-digitized January 2020 IODA BGP/active-probing proxies** and source-native November 2023 IODA measurements. The RIPE per-vantage prefix ratios have different units, peer exposures and denominators and must not be plotted directly as the same percentage as IODA active reachability.

These results are evidence of contemporaneous control-plane path reconfiguration and partial origin visibility continuity during the **reported** service decline. They cannot by themselves demonstrate the timing or physical location of the cable break, independent physical backup topology, cable-to-AS causality, packet delivery, national capacity, country-wide user impact or general cross-event causal laws. The November 2023 maintenance window used a distinct data source regime and operational event and is not a direct independent replication of January 2020.

### Unresolved work before publication
- The native January 2020 IODA `bgp` and `ping-slash24` numerical time series are still not retrieved; source-custodian follow-up may provide them or confirm archival unavailability.
- Obtain unrestricted historical original Trinocular data through USC's DUA access, if possible, for independent 2020 active-probing validation; do not relabel USC Trinocular data as IODA.
- **Completed for RRC00:** full 192-source replay matches the authenticated next RIB (zero origin or AS_PATH mismatches for the candidate prefix universe). **Still required:** validate any interim peer resets or session discontinuities, broaden beyond the 116 historical candidate prefixes and replicate full 16-hour replay in other RIPE collectors where feasible.
- Verify all final citations, bibliography, author declarations, rights and journal-specific submission requirements independently.

## Direct reproducibility links
- Multi-RRC original RIB (checksum/peer coverage): `docs/TRIPLE_COLLECTOR_RIPE_2020_VALIDATION_2026-10-26.md`
- All 192 original five-minute UPDATE files / checksum manifests: `docs/RIPE_2020_FULL16H_SOURCE_MRT_AW_AUDIT.md`; `results/ripe_2020_source_original_16h_aw_manifest.json`
- Original A/W acquisition script: `tools/ripe_2020_full_16h_updates_chunk.py`
- Source-native original data 2020 RIB+update overview: https://ris.ripe.net/docs/mrt/
- Contemporaneous event report: https://internetdisruption.report/2020/02/23/internet-disruption-report-january-2020/

**Draft research results from audited artifacts; final manuscript integration requires authors' editorial consistency checks.**
