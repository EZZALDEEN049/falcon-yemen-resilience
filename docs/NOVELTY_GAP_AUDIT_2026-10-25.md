# Novelty and Research Gap Audit — 25 October 2026

## Evidence base and editorial decision

This audit strengthens the manuscript without changing the topic or claiming unsupported originality. The current manuscript is **Structural-Functional Divergence During Submarine-Cable Disruptions: Evidence from Yemen's FALCON Dependence**.

**Prior art that constrains novelty**
1. Ramanathan & Abdu Jyothi (2023), Nautilus (doi:10.1145/3626777): confidence-scored cross-layer IP-to-submarine-cable mapping, including failure-validation. The authors' public research summary explicitly reports evaluation on the 2022 Yemen FALCON / SeaMeWe-5 event: https://pulse.internetsociety.org/en/blog/2024/04/nautilus-cross-layer-cartography-of-the-undersea-internet-backbone/
2. Ramanathan, Sankaran & Abdu Jyothi (2024), Xaminer (doi:10.1145/3639042): cross-layer physical-to-network failure risk profiles; https://arxiv.org/abs/2401.08073
3. Wang et al. (2025), Calypso: traceroute-informed cable/route mapping; https://aqualab.cs.northwestern.edu/publication/2025/cwang-sigcomm25/
4. Dainotti et al. (2014), country-scale multi-source BGP/control-versus-data plane outages; https://www-old.caida.org/publications/papers/2014/outages_censorship/
5. Jahromi & Jaskolka (2026), Iranian shutdowns with BGP-active-passive divergence; https://arxiv.org/abs/2605.00187
6. David Belson (2020), January 2020 Internet Disruption Report: **already reported** Yemen FALCON cut, the differential effect on AS30873 and AS12486, IODA graphs and AS15412 upstream-failover interpretation; https://internetdisruption.report/2020/02/23/internet-disruption-report-january-2020/

**Prohibited originality claims**
- First study linking submarine cables to IP paths.
- First to identify or quantify broadly that BGP visibility and active reachability can diverge.
- First academic examination of a Yemen submarine-cable outage.
- First report of the 2020 Yemen incident, the two affected ASes, or their reported upstream failover.
- New multilayer cable failure cascade model, independently validated 2020 MRT route survival, physically independent backup paths, population-wide impact, or universal 2020/2023 event law.

## Defensible gap statement (English, ready for manuscript)

The reviewed literature leaves a narrower, operational research gap than “cables affect IP” or “BGP does not equal reachability.” Cable-mapping and cross-layer risk frameworks chiefly infer exposure and vulnerability; multi-source outage studies already identify control/data-plane disagreement; and the contemporaneous Yemen disruption report documents the incident and its basic AS-level contrasts. What these antecedents do not provide is a transparent, uncertainty-qualified **quantitative case audit** of the January 2020 FALCON observations that (i) keeps capacity, BGP and active probing in their original measurement domains, (ii) quantifies the normalized AS30873 signal gap across event phase and source-extraction choices, (iii) separately tests a distinct FALCON maintenance episode using native 2023 time series without assuming common mechanisms or denominators, and (iv) identifies the historical physical paths, original signals and peer-continuity observations needed before redundancy claims are admissible. This bounded gap is addressed in the present manuscript, but cannot be represented as a new cable mapping model or a general causal theory.

## Contribution structure aligned with actually available evidence

- **C1 Provenance:** event-anchored chronology separating TeleYemen capacity reporting, upstream-change reporting, normalized IODA visibility and active probing.
- **C2 Quantification:** reproducible 2020 AS30873 acute **50.8 pp** descriptive signal gap reconstructed from published raster graphics.
- **C3 Analyst-choice robustness:** 2020 **20,250** deterministic combinations (45.8–55.2 pp tested range); 2020 event phase and AS12486 median-versus-mean qualifications. No confidence interpretation.
- **C4 Independent within-2023 diagnostic:** source-original IODA signal-family data, **75** tested window settings per signal for the AS30873 within-2023 comparison, separately from 2020. Explicitly not a like-for-like severity contrast.
- **C5 Evidence-admissibility implementation:** source type, observation date, measurement family and retrieval completeness recorded; origin-filtered 2020 RIB discovery not misinterpreted as a route-state replay; present 2026 topology not projected to 2020.

## Working manuscript revision completed locally, not a user-facing deliverable

Source: local v4 manuscript; working draft: `Manuscript_FALCON_v5_Novelty_Working_DO_NOT_DELIVER.docx`. Revised 19 paragraphs in the Introduction, Research Aim and Questions, Contributions, Related Work, Research Gap and Discussion; inserted contemporary report as a standalone row in Table 1 and corrected Nautilus 2022 Yemen overlap; edited 250-word abstract final novelty sentence.

The draft was rendered locally to 23 pages and inspected for layout quality. **It has not been released to the user or committed as a replacement DOCX in GitHub**, consistent with the author's instruction to receive only a completed final file.

## Remaining scientific limitations to revisit before final release

- January 2020 original numeric IODA time series not retrieved.
- Historically complete, peer-matched 2020 BGP RIB+updates / alternate-path attribution remains unavailable.
- The 2020 50.8 pp value remains **plot-derived**, not native IODA.
- Same signed gap across analyst windows is not independent replication and is not an uncertainty probability.
- Native 2023 operating regime and normalization are not interchangeable with the 2020 unplanned cable cut.
- As of this audit, **novelty strength is bounded incremental empiricism**; stronger Q1 claims require additional verified event-time data or an independently validated method. No journal acceptance probability can be asserted.
