# FALCON Yemen 2020 — curated public-source candidate

**NOT RELEASE-APPROVED.** This branch contains only research software and external source URL/checksum provenance, with no internal reviews, manuscript drafts, third-party data ZIPs, row-level routing tables, provider JSON or original images. It must not be presented as a complete scientific data deposit or as cleared for a Zenodo release.

**Researcher:** Ezzaldeen Al-Tayar, Faculty of Engineering and Information Technology, Taiz University, Taiz, Yemen.

## Contents
- `Code/`: Python analysis, original data extraction and source-checking programs. The independently generated scripts remain subject to an author-approved software license and third-party code audit.
- `Provenance/RIPE_RIS_12_RIB_Source_URLs_SHA256.json`: official RIPE RIS source RIB links/checksums; original MRT binary archives are not included.
- `Provenance/IODA_2020_Publisher_Image_Links_SHA256.json`: publisher source-image links/checksums; image bytes and source-native numerical 2020 time series are not included.

**Scientific interpretation:** Descriptive BGP AS_PATH observations, not causal cable routing attribution or user connectivity. The earlier Jan 2–3 window is one retrospectively fixed reference, not a statistical population of ordinary conditions.

**What this does not contain:** RIPE source-derived peer-prefix CSV rows, original IODA JSON datasets, RIPE Atlas audit ZIP, internal reviewer reports, submitted manuscript, supplementary tables or figures. As a result, numeric results cannot be fully reproduced using this branch alone. Scripts needing source-derived exports or provider JSON require those inputs separately, consistent with provider licensing.

## Before creating a public `v1.0.1` Release
1. Obtain explicit owner approval for the chosen code license and review code for third-party snippets/secrets.
2. Fix `.zenodo.json` licensing metadata. Zenodo will otherwise use its default CC BY 4.0, which must not be assumed to license third-party inputs or non-author materials.
3. Decide how rights-cleared numerical data are made available to editors and readers, or document official source access and regeneration procedures.
4. Inspect this exact branch's files and commit hash; create a new version rather than moving existing `v1.0.0` tags.
5. Independently review the older openly accessible GitHub history and previously published `v1.0.0` Zenodo ZIP for unapproved contents. This branch does not erase older copies.

This branch is a separate preparation snapshot, not an editor-approved submission to Scientific Reports.
