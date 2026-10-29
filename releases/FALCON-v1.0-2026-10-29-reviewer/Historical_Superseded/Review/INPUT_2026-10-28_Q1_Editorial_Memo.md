# FALCON — Independent Q1-Style Editorial and Technical Peer-Review Memorandum
**Manuscript evaluated:** `FALCON_2026-10-28_2020_IODA_Raster_Verified_Manuscript.pdf` (28 pages)  
**Assessment date:** 28 October 2026  
**Status:** Conditional editorial hold / Major revision before journal submission.  
**Scope:** This memorandum evaluates the submitted PDF, performs an internal numerical cross-check of the six Table 5 fractions, inspects its embedded figures, reads the RIPE extractor and GitHub reaggregation memo via the connected repository, and cross-checks selected external sources. It **does not** independently rerun all six original RIPE MRT RIBs, the 192 RRC00 UPDATE files, or the 20,250 IODA image-perturbation trials, because the current submission consists of the PDF rather than a frozen full reproduction bundle. It does not attest to acceptance prospects or validate every reference.

## A. Simulated Editor-in-Chief Decision
**Disposition: NOT READY AS SUBMITTED; fixable, potentially reviewable after targeted pre-submission revision.** The central contribution is a reproducible, limited-scope two-checkpoint 2020 multi-collector BGP route-adjacency case study with per-prefix and per-peer diagnostics. It is not a novel general cable-to-AS mapping method, a causal effect identification study, nor a continuous data-plane recovery measurement. Major concern: inconsistent statements about completion of 2020 IODA original-raster validation and an overlong, repetitive presentation that obscures the narrower novelty. A strict, highly selective measurement journal may additionally find the methodological advance insufficient without a stronger nontrivial comparator or a sharply articulated generalizable evidence-to-claim protocol.

## B. Confirmed positives
1. The Table 5 six retention and changed-neighbor percentages recompute from the printed numerators/denominators: AS30873 changed 66.83%, 67.98%, 64.73%; AS12486 changed 6.28%, 4.05%, 14.10%, by RRC00/01/10. Totals from the six rows: 11,293 eligible, 10,333 retained and 6,547 changed. The paper also reports 11,419 first-snapshot rows.
2. Three observational units are distinguished: peer–prefix record, equally weighted prefix, and equally weighted peer; same-peer diagnostic has 62, 21, 13 collector-specific pairs. The 105-versus-six-prefix mismatch and correlated observations are expressly acknowledged.
3. The paper explicitly withholds causal attribution of all BGP changes to FALCON, quantitative nationally representative user reachability, physical path disjointness, and data-plane restoration claims.
4. The GitHub commit `907b59027807ab292d33886d36e65e2bb07f63c6` is present; the source-native extractor and the latest default-branch independent reaggregation memo are retrievable via the connected GitHub tools. The memo documents an internal row-level audit, not a fresh fourth independent data source.
5. Figure 2 uses a multi-panel presentation to distinguish units; Figure 4 uses unconnected categorical phase points; the native 2023 IODA comparison correctly states it is not a replication of the 2020 cable cut.

## C. Required revisions in priority order

### CRITICAL-1 — Contradictory IODA raster-verification status (editorial blocker)
The same PDF asserts that original publisher-linked 2020 PNG rasters and pixel extraction were retrieved/reproduced (pp. 7, 13, 24 and 27–28), while simultaneously claiming retrieval/pixel verification remain OPEN (p. 19 §8.5; p. 25 §12.1 and §13; p. 27 Data Availability). **Action:** designate one evidence gate that reflects actual supporting records; synchronize every occurrence. If the rerun truly completed, change all old statements to distinguish *source-published raster verified* from *native IODA 2020 time series unavailable*. Require attached image hashes, original article URLs, calibration script, output CSV and execution log before marking resolved.

### CRITICAL-2 — Old methodological status remains after newer route-level release
At p. 5 §3: “because route-level historical reconstruction is not yet validated” is inconsistent with the source-native two-checkpoint peer–prefix release (pp. 7–8, 23–24). **Action:** distinguish valid *endpoint AS_PATH neighbor reconstruction* from *unobserved event-time physical/cable-to-AS topology*. Do not say the former is unvalidated.

### MAJOR-1 — Clearly define timing and observational estimand
On p. 10 §6.1 and p. 11 §8.1 state precisely that 9 Jan 08:00 and 10 Jan 00:00 UTC are two sampled BGP RIB checkpoints; they are not verified exact fault onset/repair boundaries, and a peer present at both endpoints is not guaranteed continuously online. Distinguish missing target origin from explicit BGP withdrawal. Include a small source-qualified UTC event timeline (publisher-reported deterioration approximately 09:00 UTC, major active-impact around 18:00, snapshot boundaries) without inventing minute-level source-native fault time.

### MAJOR-2 — Address the inequivalent prefix universes conspicuously
The AS30873 versus AS12486 comparison uses 105 versus six distinct matched prefixes per collector, with non-independent peer/collector observations; it is an illustrative contrast, **not** a matched untreated-control/causal design. Retain three units, paired descriptive results, and leave-one-prefix-out sensitivity. Rephrase all “falsification” language so that the test rejects only a narrow *descriptive common-observer equality pattern*, not causal nulls. If feasible, add per-prefix observational coverage / matched-peer counts to supplementary data. Do not invent inferential p-values.

### MAJOR-3 — Avoid treating cross-signal subtraction as direct functional availability
The 2020 +50.8-point IODA statistic subtracts separately normalized measurement families with unlike denominators. Define it as a **descriptive baseline-retention contrast between noncommensurate proxies**, not a percentage of service loss or physical restoration. Figure 3 should show the actual 95.7% and 44.8% normalized retention and, if graphical uncertainty is shown, label 45.8–55.2 as a deterministic analyst-choice sensitivity range (not a confidence interval). Keep 2020 IODA *secondary* to source-native BGP.

### MAJOR-4 — Reduce unnecessary repetition
The main analysis repeats the BGP comparison and its limitations in §§8.1, 8.6, 9 and 10.6; it repeats 2020 IODA robustness in §§8.1.1 and 8.5. Table 8 restates Table 5 without comparable new information. Move one duplicate table and the extensive audit narrative to Online Resource 1. Aim for a manuscript with one integrated Results narrative and a much shorter Discussion/Limitations, without removing key caveats.

### MAJOR-5 — Clarify manuscript novelty and refine title/abstract
Current title plural “Disruptions” and broad “FALCON Dependence” could imply broad causal evidence; the main original finding is the **2020 matched BGP-adjacency reconfiguration**. Suggested more precise title:
**“Network-Specific BGP Route Reconfiguration During Yemen’s January 2020 FALCON Disruption: A Multi-Collector Measurement Study”**
Alternative retaining the cross-signal aspect:
**“Routing Reconfiguration and Measurement-Signal Divergence During Yemen’s 2020 FALCON Cable Disruption”**.
Lead abstract with source-native contribution, the different observational units, the precise noncausal inference, and only then 2020 IODA and 2023 distinct-incident qualifications. Avoid framing the general warning that BGP reachability is not functional availability as a discovery; it is established prior art.

### MAJOR-6 — Freeze the Supplementary/Reproducibility bundle
Provide submission-matched Online Resource 1 with S1–S11, original PNG hashes and raster calibration code, the actual three-collector source-native CSVs, 2023 source JSON, executable scripts, environment/dependency file, license/permissions and a read-only tagged release or stable archive. Replace mutable `/blob/main/` references with commit-specific links; make the repository accessible to reviewers; verify linked filenames exist. The current PDF alone does not permit verifying all claimed pipelines.

### MINOR-1 — Figure and table editing
Figure 2 deserves vector export or adequate-resolution, larger typography and accessible palette; Panel B should state 'descriptive IQR, not inferential intervals'. Figure 3's sensitivity range is in the caption but not visually encoded. Standardize “Table 5a” to a normal journal sequence. Figure 5 should label the two baselines and the small integer ping-/24 denominators. References to Table S1 should not repeat awkwardly in §8.1.2.

### MINOR-2 — Do not claim prospective pre-specification without documented timestamp
Section 8.1.1 calls the 20,250-setting extraction grid “pre-specified.” If these choices were set after initial results, write “predefined sensitivity-analysis grid” or “documented robustness grid”; use “pre-registered” or “prospectively pre-specified” only if documentary provenance shows it.

### MINOR-3 — Avoid over-detailed rebuttal embedded in manuscript
Repeated statements about what reviewers questioned, audit statuses in ALL-CAPS, and 'refusal to infer' can read like a reviewer-response file, not a polished research article. Keep necessary version-specific data provenance in the reproducibility section or supplement, and make the main paper readable in its own right.

## D. Simulated reviewer comments

**Reviewer 1 — BGP measurement and routing (Major Revision):**
- Clarify the precise `immediate_upstream` parsing rule for AS_PATH prepending, invalid paths, multiple origins and duplicate peer-IP/prefix entries, and audit impact of excluded observations.
- Clearly separate 2-RIB RRC00/01/10 endpoint analysis from 16-hour RRC00 UPDATE replay; give matching/eligible/retained/unparseable counts and the exact 116-prefix candidate universe.
- Do not interpret AS_PATH neighbor changes as proof of data-plane rerouting via physically separate cable; path choice and IXP/multihop peer visibility remain unmeasured.
- Explain coverage biases: observers are not random; collectors can share routes and peers; 105 versus six prefixes limit cross-network inference.

**Reviewer 2 — Statistical interpretation / identification (Major Revision):**
- The observational unit is not a set of independent routes/users. The 96 common-peer pairs remain dependent across collectors and prefixes; leave out conventional independent-sample p-values.
- Distinguish observation-weighted 66.83–67.98% from prefix median 96.67–100%; one is not a validation of the other as the same estimand.
- A 20,250-point deterministic sensitivity grid is a set of analysis choices, not 20,250 replicates or sampling evidence; no percentile interval should be marketed as a confidence band.
- The 2023 opposite-sign IODA contrast is not a controlled counterfactual to 2020 and should be used for measurement-interpretation robustness only.

**Reviewer 3 — Novelty, reproducibility and presentation (Major Revision):**
- State a narrow, falsifiable contribution beyond Nautilus/Xaminer/prior BGP-active outage studies; a well-documented country case alone might not clear the novelty bar at highly selective venues.
- Remove unreconciled version statements on raster verification and route-level evidence.
- Provide a persistent release accessible to external referees, complete captions, precise Figure 3 sensitivity semantics, and a main text free of repeated defenses.
- Verify reference metadata, target-journal scope, page/figure limits, permissions for republishing source raster imagery, and author/declaration requirements.

## E. Exact replacement text proposed for the manuscript
These paragraphs assume that the reported original publisher-PNG retrieval and 20,250-setting rerun **really are backed by complete files/logs in the final supplement**. If not, retain 'unverified' status instead.

**Replacement for p. 5 §3 sentence:**
> “The two-checkpoint 2020 RIPE RIS peer–prefix AS_PATH observations have been reconstructed from source-native RIBs and independently reaggregated. However, these observations do not instantiate a verified event-time physical cable-to-AS dependency topology, nor do they identify topology-wide cascade effects.”

**Replacement for p. 19 §8.5 stale closing sentence:**
> “The original publisher-linked January 2020 IODA PNG rasters were retrieved, checksum-recorded and re-digitized using the documented pixel calibration. The resulting acute-window contrasts and 20,250-setting deterministic sensitivity outputs matched the archived analysis. The original source-native 2020 IODA numerical time series were not recovered; therefore, timing precision, sampling uncertainty and user-level functional availability cannot be inferred from these raster-derived summaries.”

**Replacement for p. 25 §12.1 stale assertion:**
> “The January 2020 IODA robustness grid was reproduced from the original publisher-linked raster pixels, but remains secondary plot-derived evidence rather than a source-native numerical time series. The analyst-choice settings do not constitute independent experimental replications or confidence intervals.”

**Replacement for p. 25 §13 open-requirements sentence:**
> “Full RRC01/RRC10 UPDATE replay, continuous peer-session telemetry, source-native January 2020 IODA time series, and final journal-specific reference and repository compliance remain unresolved. Original publisher-raster retrieval and pixel-level digitization reproducibility are documented separately and should not be described as open.”

**Replacement for p. 27 Data Availability contradictory sentence:**
> “Continuous peer-session status between the two RIB checkpoints and source-native January 2020 IODA numerical observations were not established. The original publisher-linked January 2020 IODA PNGs, their hashes, the pixel-extraction script and the reproduced deterministic sensitivity output are available in the raster-calibration supplement.”

**Proposed contribution/cover-letter summary:**
> “We present a source-auditable, multi-collector reconstruction of origin-adjacent BGP AS_PATH changes across two January 2020 checkpoints during Yemen’s FALCON disruption. The released observation-level records support peer-, prefix-, and collector-qualified descriptive checks, while a deliberately separate secondary analysis demonstrates why control-plane indicators cannot be treated as operational-capacity or reachability measurements. Rather than claiming cable-level causality or a novel generic cross-layer model, the work contributes an event-specific, reproducible evidence-to-claim workflow for infrastructure resilience analysis.”

## F. Final pre-submission gate
Release only when all are true:
1. Every claim of 2020 raster verification has one consistent, evidence-backed status (no stale OPEN statements).
2. §3/abstract/conclusion use the same distinction between endpoint BGP reconstruction and unmeasured physical topology.
3. Main text and supplement use consistent number tables, matching file hashes, and stable commit-linked data.
4. Coverage, selection, non-exchangeable prefix inventories, same-peer dependence and temporal sampling remain explicit.
5. The journal receives the actual Supplementary Resource and accessible artifact instructions, not only a PDF that points to potentially private files.
6. A qualified independent reader performs a final reference/figure/number sweep and checks the target journal's editorial scope and limits.

**Final recommendation:** Meaningful evidence-based improvement and real potential for external review after the above changes; **not ready to submit as the current PDF**. No scientific or editorial procedure can guarantee passage through Q1 editors/reviewers.

## Public sources checked (for context, not a replacement for manuscript source files)
- RIPE RIS MRT documentation: https://ris.ripe.net/docs/mrt/
- IODA methodology (Georgia Tech): https://ioda.inetintel.cc.gatech.edu/
- IODA signal descriptions (APNIC): https://blog.apnic.net/2024/09/11/ioda-internet-outage-detection-and-analysis/
- Original January 2020 disruption report: https://internetdisruption.report/2020/02/23/internet-disruption-report-january-2020/
- World Bank 2020 Yemen update: https://thedocs.worldbank.org/en/doc/901061582293682832-0280022020/original/YemenEconomicUpdateJanuaryEN.pdf
