# FALCON — Independent Q1-style Editorial Reassessment
**Manuscript reviewed:** `FALCON_Revised_Q1_Editorial_2026-10-28.pdf` (25 pages, 28 October 2026)
**Review type:** editorial screening + network-measurement technical peer-review simulation
**Scope:** the attached PDF, comparisons with the previous 28-page manuscript and selected connected GitHub commit/files. The latest journal-specific author instructions and the complete new reviewer ZIP were not supplied.

## 1. Editorial disposition
**CONDITIONALLY SUITABLE FOR EXTERNAL PEER REVIEW AFTER SUBMISSION-PACKAGE AND TECHNICAL CHECKS — NOT GUARANTEED ACCEPTANCE.**

Most previous *documentary consistency* blockers are corrected. The paper is now explicitly a narrow empirical BGP measurement case study, not a general causal cable-resilience model. Original 2020 IODA raster/derived checks are consistently qualified, and the original 2020 numerical series are consistently described as unavailable. The paper correctly disclaims per-route cable causality, user reachability, continuous peer-session health, and equality of control- and active-measurement denominators. The title is notably more defensible.

However, the more selective the Q1 venue, the more likely an editor will ask whether a two-checkpoint historical measurement + reproducibility protocol adds enough *generalizable knowledge* beyond an interesting case. No journal can be guaranteed to send a paper for peer review or accept it.

## 2. Checks actually performed
- Read and visually inspected the 25-page PDF, including Figures 1–6 and Tables 1–10.
- Arithmetic checks reproduced the six Table 5 changed/retained percentages: RRC00 AS30873 4157/6220=66.83%, AS12486 23/366=6.28%; RRC01 1482/2180=67.98%, 6/148=4.05%; RRC10 868/1341=64.73%, 11/78=14.10%. All six sum to 6547 changes in 10333 retained comparable routes, and the listed first-snapshot counts sum to 11419.
- Other arithmetic cross-checks: 3343/3360=99.49%; 356/884=40.27%; unrounded published raster proxy 95.6522−44.8378=+50.8144 percentage points.
- Located GitHub commits 907b59027807ab292d33886d36e65e2bb07f63c6 (2020 peer-prefix outputs) and a51805e39f900ca0bdcbd83a32b6dce597b9a345 (IODA raster verification). Inspected selected code and raw row-level CSV examples.
- **Not performed:** full independent re-download/reprocessing of six MRT RIB binaries; reprocessing of 192 RRC00 UPDATE archives; full independently executed 20,250-setting raster grid; verification of complete latest Online Resource 1 (not included with this upload); journal-specific compliance review.

## 3. What is resolved from the previous review
| Prior issue | Current finding | Evidence in revised PDF |
|---|---|---|
| Contradictory IODA-2020 image verification status | **Resolved in this PDF**: publisher PNGs retrieved and pixel-calibration reproduced; raw provider numeric series unavailable | Abstract p2; §4.2 p7; §8.1.1 pp13; §8.5 p17; §12 p21; declarations p24 |
| Overbroad title and contributions | **Materially improved** by focusing on network-specific route reconfiguration | Title p1; Abstract p2; C1–C5 pp2–3 |
| Missing clarity about event temporal boundaries | **Improved**: explicit UTC timeline and caution about differing estimands | §4.1 p7; §4.3 p8 |
| Prepending/selection/peer-presence and unequal denominators | **Improved**: method now explicitly distinguishes matching and invalid AS_PATH entries | §4.3 p8; §6.1 pp9–10 |
| No per-prefix or per-peer assessment | **Resolved descriptively** in main text and released outputs | Fig.2 p12; Table 6 p13 |
| IODA sensitivity shown as confidence interval | **Resolved**: Figure 3 includes an explicitly deterministic analyst-choice range | Fig.3 p13 |
| Heavy repetition of results | **Reduced, not wholly eliminated** | Results pp11–18 and Discussion pp18–20 |
| Restricted UPDATE replay described too broadly | **Corrected**: clearly RRC00-only, candidate-prefix-bounded and not independently rerun in this revision | Abstract p2; §4.3 p8; §12 p21 |

## 4. Remaining issues and required actions

### P0 — Submission gates (mandatory before upload)
**P0-A. Deliver and verify the actually promised supplementary archive.** The manuscript says the reviewer package includes all 11,419 peer-prefix rows, per-prefix/per-peer distributions, source SHA256, 2020 PNG calibration data and 2023 JSON/replication outputs (pp21,24–25). Only the 25-page PDF was provided for this round. Supply `Online Resource 1` and the reviewer ZIP; match every figure/table to the frozen data and links. Provide run instructions and a clean-machine smoke test. Do not describe the package as included in a submission unless it is actually attached to that submission.

**P0-B. Journal-specific compliance.** Choose a named target venue and check article type, word/figure/supplement limits, title page, double-blind rules (if any), required data/code licenses, and reference style. The current title page and signed GitHub author repository can deanonymize the submission if the journal is double blind.

**P0-C. Final proofing.** PDF document metadata `Title` still says `Structural–Functional Divergence During FALCON Disruptions — Major Revision, evidence-gated`, instead of the new paper title. Replace it and check all author/revision fields and URL hyperlinks. Recheck every Table/Figure/Online Resource cross-reference. Current PDF includes 25 pages and six figures; it appears to have a stand-alone title page (verify journal policy).

### P1 — Key scientific improvements for an ambitious Q1 venue
**P1-A. Establish a non-event baseline (recommended strongest new empirical test).** Apply the same two-checkpoint method, ideally 16 hours apart, to a nearby non-disruption date for AS30873 and AS12486 with the same three RIS collectors; report how much ordinary AS_PATH adjacent-neighbor churn occurs. Prespecify the date and exclusion/eligibility criteria, give original file hashes, and avoid choosing a baseline to produce a large result. This would test whether the reported January 9 change is exceptional rather than merely large between two arbitrary snapshots. This test is *not* already performed by the presented 2023 IODA comparison.

**P1-B. Expose the actual AS_PATH adjacency transitions.** The text says AS15412 disappeared and AS174 appeared at the origin-adjacent position (p11), but the central figure mainly shows incidence of change. Compute a compact before→after immediate-neighbor transition table/matrix with actual counts per collector (and preferably distinct-prefix summaries), directly from the released peer–prefix CSVs. Show principal flows and 'unchanged/other' groups, not just percentages. Avoid calling the immediate neighbor a physically independent cable path.

**P1-C. Verify address-family and observation-selection sensitivity.** At minimum stratify original route counts and change shares by IPv4 vs IPv6 and report comparable-route exclusions/unparseable cases per AS/collector. The source CSVs can include IPv6 rows. If sample counts are too small, report descriptively; do not create unreliable significance tests.

**P1-D. Tighten novelty framing.** A checklist of G1–G6 admissibility rules is useful research integrity practice, but not necessarily a novel validated methodological contribution. Lead with the source-auditable historical routing case and label the protocol a transferable reporting practice, not a new formally validated method. State what kind of broader claim the evidence can and cannot sustain, and why three collector observations add beyond the established literature.

### P2 — Editorial, graphics and numerical presentation
**P2-A. Figure 2 p12:** the three-panel graphic contains very small labels at printed-page size, and the 105-vs-six prefix imbalance drives the interpretation of Panel B. Supply vector PDF/SVG or high-quality original plot file with journal-sized labels. Consider an ECDF/point-interval supplementary panel instead of only Q1/median/Q3 if heterogeneity/bimodality is central.

**P2-B. Figure 3 p13:** the revised dual-panel figure is an improvement. Keep the range labeled `deterministic analyst-choice range, NOT a 95% confidence interval`; optionally explain the plotted central estimate in full precision, because displayed 95.7% minus 44.8% rounds to 50.9 pp while the difference of underlying values is 50.8144 pp (shown as 50.8). This is only a rounding-display issue, not an arithmetic error.

**P2-C. Narrow the Results/Discussion overlap.** §8.4–8.6 and §9 repeat aspects of §8.1, and §10 again summarizes them. Move some verification and sensitivity mechanics to the supplement to retain a single clean main scientific narrative.

**P2-D. Verify citation formatting and bibliographic metadata for every reference and link.** Spot-checks found the July 2026 ITU communication and the cited 2026 arXiv works exist, but this is not a reference-by-reference DOI/venue audit.

## 5. Simulated reviewer outcomes
**Handling editor:** `Editorial technical check and missing supplement; then consider sending for peer review.` In an especially selective Q1, the narrow novelty may still trigger editorial rejection.

**Reviewer 1 — Internet measurement:** `Major revision` if the non-event baseline or actual neighbor-transition evidence is absent and the venue demands strong event-specific interpretation; otherwise potentially `minor revision` after clear limitations and reproducibility package.

**Reviewer 2 — Statistics:** `Minor/targeted revision`; no unsupported p-values or confidence intervals should be manufactured. Maintain separation of conditional observation-, prefix- and peer-based rates and deterministic IODA perturbation ranges.

**Reviewer 3 — Contribution and presentation:** `Major/targeted revision`; prove that the event-based measurement is more than a case description, and deliver readable publishable figures and an inspectable supplement.

## 6. Release gate / sign-off checklist
- [ ] `Online Resource 1` and all referenced frozen reviewer ZIP files supplied, checksums compared, scripts smoke-tested.
- [ ] Target journal specified and full guide-for-authors checked.
- [ ] PDF/document metadata corrected; final references and all section/table cross-references checked.
- [ ] At least a transparent answer to the **non-event 16-hour baseline question**; preferably run the comparison.
- [ ] Include origin-adjacent AS_PATH before→after transition totals by collector; consider address-family strata.
- [ ] Readability of Figure 2, Figure 3 and captions checked at journal printed width.
- [ ] Final abstract, conclusions and cover letter aligned with limited observational claims.

**Final position:** Compared with the previous 28-page version, the revised 25-page paper has made genuine progress and resolved its serious internal IODA contradictions. The remaining most meaningful opportunity is a bounded *new test* (non-event reference window) and a direct transition visualization, not another round of rhetorical polishing. Submit only when the evidence package and the chosen journal's requirements are independently checked.
