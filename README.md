# FALCON Yemen 2020 — curated public-source candidate

**Author-owned code licensed under MIT; not yet a Zenodo release.** This separate, reduced branch contains research software and source URL/checksum provenance. It excludes internal reviews, manuscript drafts, row-level routing tables, third-party data ZIPs, provider JSON and original images. It must not be presented as a complete scientific data deposit. A separate final release review and outstanding prior-version assessment remain necessary.

**Researcher:** Ezzaldeen Al-Tayar, Faculty of Engineering and Information Technology, Taiz University, Taiz, Yemen.

## Contents
- `Code/`: Python analysis, original data extraction and source-checking programs. The original, author-owned scripts under `Code/` are licensed under the MIT License in `Code/LICENSE` on confirmation from the sole researcher. This grant does not license third-party packages or source datasets; a provenance/third-party code audit is still advisable.
- `Provenance/RIPE_RIS_12_RIB_Source_URLs_SHA256.json`: official RIPE RIS source RIB links/checksums; original MRT binary archives are not included.
- `Provenance/IODA_2020_Publisher_Image_Links_SHA256.json`: publisher source-image links/checksums; image bytes and source-native numerical 2020 time series are not included.

**Scientific interpretation:** Descriptive BGP AS_PATH observations, not causal cable routing attribution or user connectivity. The earlier Jan 2–3 window is one retrospectively fixed reference, not a statistical population of ordinary conditions.

**What this does not contain:** RIPE source-derived peer-prefix CSV rows, original IODA JSON datasets, RIPE Atlas audit ZIP, internal reviewer reports, submitted manuscript, supplementary tables or figures. As a result, numeric results cannot be fully reproduced using this branch alone. Scripts needing source-derived exports or provider JSON require those inputs separately, consistent with provider licensing.

## Before creating a public `v1.0.1` Release
1. Verify the final branch contains only the intended original code plus source URL/checksum documentation and does not contain embedded third-party code with incompatible rights.
2. `.zenodo.json` declares the MIT license for the software-only archive; that license does not cover the underlying RIPE RIS or IODA records, or other files omitted from this edition.
3. Decide how rights-cleared numerical data will be made available to editors and readers, or document official source access and regeneration procedures.
4. Inspect the exact branch SHA before creating a separate `v1.0.1` release; do not move existing `v1.0.0` tags.
5. Address the already public, older Zenodo `v1.0.0` ZIP and repository history independently. This branch does not erase those copies.

This branch is a separate preparation snapshot, not an editor-approved submission to Scientific Reports.
