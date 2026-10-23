# Stepwise manuscript development — 24 October 2026

## Rules
- One scoped scientific change at a time, verified before beginning the next.
- Do not relabel plot-digitized January 2020 signals as original IODA samples.
- A passing GitHub action is code execution evidence, not validation of the scientific claim.
- Keep the original manuscript, sources, and rerunnable scripts.

## 1 — Correct the current evidence status in the manuscript [COMPLETED LOCALLY AND ON GITHUB]
Scope: Abstract, §4.2, BGP limitations, reproducibility (§12). Four paragraphs changed, no numeric claims changed. Correct the outdated statement that January 2020 IODA acquisition merely failed due to DNS: v2 returned HTTP 200 and no native samples for the requested series. Describe exploratory RIPE RIS records without claiming a validated event-time prefix universe. Explicitly distinguish recovered 2023 native IODA data from unavailable 2020 samples.

New locally rendered and quality-checked document, now also committed by GitHub Actions: `paper/Manuscript_2026-10-24_Evidence_Status_Updated.docx`. The original and prior revised manuscript files remain unchanged.
Verified successful step-1 cloud job: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40042125287

## 2 — Integrate November 2023 native IODA evidence [NEXT]
- Verify the exact raw JSON and independent timestamp windows, median definitions, signal identities, coverage, and event provenance.
- Insert a dedicated quantitative 2023 paragraph/table in §8.4; update the abstract, §4.2 methodology, provenance, and limitations consistently.
- Distinguish native 2023 BGP/ping from plot-derived 2020 BGP/ping; do not treat the event regimes as exchangeable or assert cable causality.

## 3 — Historical BGP audit and reconstruction [OPEN]
- Resolve incomplete/erroring rrc00 archive transfers and try independently verifiable RIPE RIS/RouteViews archives.
- Audit historical originated prefix universe, peer uptime, collector-vantage continuity, RIB + unfiltered announcements and withdrawals, and event-time sampling.
- Only after coverage passes, publish route-level metrics. Previous 109 and 7 candidate prefixes are discovery-only.

## 4 — January 2020 IODA archive custody [EXTERNAL DEPENDENCY]
- Request original BGP-visibility and ping-slash24 timeseries from the IODA/CAIDA custodians, including provenance and permission, or secure written archival-availability confirmation.
- Current v2 raw endpoint returns empty 2020 data. IODA outage-event series are **not** original BGP/ping measurements.
- If the original records cannot be recovered, retain the plot-derived limitation prominently.

## 5 — Scientific contribution and robustness [AFTER 2–4]
- Reassess cross-event comparability, sensitivity to temporal windows, event-selection bias, alternative explanations and novelty.
- Make Q1/Q2 journal targeting evidence-based; do not claim causal multilayer cascade or predictive ML without real tests.

## 6 — Final manuscript and supplemental release
- Align methods/results/abstract/captions/conclusion, references, supplementary data and scripts.
- Review source licences, anonymization, submission policies, image rights; then package Zenodo materials after the authors approve public release.

## Evidence status
Successful CI reproduction: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40032784633
Native IODA 2023 validation: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40025268544
IODA 2020 audit: https://github.com/EZZALDEEN049/falcon-yemen-resilience/blob/main/docs/IODA_2020_ARCHIVE_RECOVERY_AUDIT.md
