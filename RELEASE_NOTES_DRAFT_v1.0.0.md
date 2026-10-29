# Draft release notes — v1.0.0 (NOT FOR PUBLICATION UNTIL CLEARED)

**Proposed title:** FALCON Yemen 2020 — BGP Routing Measurement Code and Auditable Research Data, v1.0.0

**Status:** GitHub RELEASE DRAFT — publication BLOCKED pending rights and confidentiality review.

This candidate source archive contains software and provenance records for the pre-submission research study *Network-Specific BGP Route Reconfiguration During Yemen's January 2020 FALCON Disruption: A Multi-Collector Measurement Study*. The study documents two-checkpoint origin-adjacent AS_PATH observations for AS30873 and AS12486 at RIPE RIS RRC00, RRC01, and RRC10, using 9 January 08:00 to 10 January 00:00 UTC 2020 and one retrospectively selected earlier 16-hour reference interval from 2 January 08:00 to 3 January 00:00 UTC.

The retained and comparable AS30873 route observations show changed-neighbor shares of approximately 64.73–67.98% in the event window and 0.41–0.90% in the earlier reference. These are **descriptive differences**, not an anomaly distribution, confidence interval, causal attribution to a physical cable path, user reachability estimate, or proof of all-collector UPDATE replay.

**Proposed archive contents after curation only:**
- Version-fixed, author-owned reproducibility scripts, parser tests and usage instructions.
- Public-redistribution-cleared derived BGP aggregate tables and source manifests; row-level exports **only if source license/permission authorizes redistributing them**.
- Audit tables and original source URLs/SHA-256 for 12 RIPE RIS MRT RIBs without claiming the original full MRT binaries are embedded.
- January 2020 IODA raster *provenance and derived-method explanation only*, not unauthorized original publisher PNG bytes or nonexistent provider-native numerical 2020 time-series.
- November 2023 native IODA JSON only after source terms/rights review, or a reference/retrieval procedure instead.
- File-specific license notices and a complete SHA-256 manifest of **the cleaned public archive only**.

**Explicit exclusions from the final Zenodo snapshot:** internal reviewer responses and review reports, pre-submission-only author correspondence and manuscript drafts without consent, superseded files, unknown-rights images/source datasets, transient GitHub Actions and expired transfer URLs, and any private data.

The manuscript is **not submitted, accepted or published** in *Scientific Reports*. The Zenodo DOI must be inserted only **after** an actual successful, rights-cleared archival deposit. The software archive is not an endorsement by Scientific Reports, Zenodo, RIPE NCC or IODA.

**Current blockers:** review and separate licensing of code/data/third-party figures, removal of C/D and unapproved B files from the release snapshot, prior public reviewer prerelease/history exposure, complete scientific-bibliography check, author sign-off, and journal-specific statements. Refer to `PUBLIC_RELEASE_AUDIT_2026-10-29.md`, `PUBLIC_RELEASE_FILE_CLASSIFICATION_2026-10-29.csv`, and `DATA_LICENSES_AND_PROVENANCE.md`.

**Do not click Publish release.** The working draft `v1.0.0` must continue targeting `main`, and the release tag does not exist as of the 29 October audit. At final approval, recheck current `main` SHA, ensure the archive contains `README.md`, `CITATION.cff`, `.zenodo.json`, licensing notices and only cleared materials, and verify that the final `v1.0.0` tag would resolve to that same exact SHA.
