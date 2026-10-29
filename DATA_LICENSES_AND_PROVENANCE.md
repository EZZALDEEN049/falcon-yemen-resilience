# FALCON data licenses, authorship, source rights and provenance

**Rights audit status: OPEN — no repository-wide open-license grant.**  
**Review snapshot:** 29 October 2026. This document is an evidence/permissions inventory, **not legal advice or a declaration that third-party redistribution is allowed**.

## Components and separate licensing decisions

| Component | Origin | Provisional public class | Rights status | Intended disposition |
|---|---|---|---|---|
| FALCON-authored Python in `code/`, `tools/`, `tests/`, latest `releases/.../Code/` | Researcher/assistive development; exact ownership and contributions to be confirmed | **A candidate** | Source files currently have **no granted open-source license**; sole author must explicitly approve licensing, warranties and contributors | Candidate **MIT** or **BSD-3-Clause** *for confirmed original code only*, after author sign-off; do not automatically license third-party snippets |
| Author-produced figure SVG/PNG/PDF, analysis narratives and table schemas | Author-generated transformations | **A/B case by case** | Some figures and tables derive from publisher imagery or provider measurements; transformation does **not** automatically clear source rights | A possible **CC BY 4.0** grant *for eligible independently authored portions only*, after confirmation; label adapted/derived elements and exclude unclear rights |
| Original RIPE RIS MRT files and RIPE-origin route data | RIPE RIS public archive; sources in the twelve-RIB URL+SHA manifests | **B** | Public research access confirmed, **redistribution and downstream relicensing not established**; RIPE terms may vary by service and dataset | Publish **official URLs, retrieval commands, source hashes, timestamps and algorithm**; do not upload full original MRT binaries until written terms or permissions checked |
| FALCON RIPE source-derived peer–prefix CSV and aggregated routing tables | Individual observations extracted from RIPE RIS RIBs | **B** | Rights in source and database-derived exports not independently cleared merely by transformation | Keep computation reproducible from source; seek confirmation on redistribution of row-level exports; aggregation alone does not imply an unrestricted license |
| Original January 2020 IODA publisher PNG images | Georgia Tech / internetdisruption.report | **B** | Original image bytes not included in the latest reviewer ZIP; reuse/redistribution rights not verified | Link publisher URL + SHA-256 only until permission for verbatim/adapted image republication is obtained |
| IODA January 2020 pixel traces, calibration and 20,250-choice sensitivity | Author-derived from the published original PNG | **B** | Secondary digitization and deterministic analytical variation; still potentially dependent on publisher source rights | Attribute visibly, retain source and procedure, review extent of digitized data being openly redistributed; never call them source-native numerical data |
| IODA November 2023 original provider JSON ZIP | Provider-origin numerical responses | **B** | Original provider data retention/republication rights not verified | Prefer linked source/fetch script and hashes if redistribution not licensed |
| RIPE Atlas source metadata and archived aggregated audit ZIP | RIPE Atlas | **B** | Source terms and redistribution rights have not been validated for this exact metadata subset | Preserve source links and minimal author-made aggregates subject to original service terms |
| Main manuscript and supplementary PDF/DOCX | Single researcher manuscript in pre-submission state | **C until author sign-off** | Not published or accepted; third-party figure quotations/rights and journal policy still require review | Obtain explicit public-preprint permission before making part of DOI archive |
| Independent reviewer reports, response tables, trace memos and Historical_Superseded material | Internal editorial/reviewer work | **C** | Research workflow records not approved for permanent public deposit | **Exclude** from public Zenodo source snapshot and public release assets |
| Older 2026 context figures and obsolete scripts | Early workspace; may be superseded or incomplete | **D** | Cannot be treated as finalized evidence or current methods | Exclude from Zenodo unless necessary for a specifically justified historical reproducibility appendix |

### License file policy

No `LICENSE` file is currently added. Do not assume default open licensing from GitHub's public visibility. If the sole author signs off on a code license, add a **code-only** grant with scope in a separate `LICENSE-CODE` or `Code/LICENSE`; for eligible author-owned tabulations use a separate `LICENSE-DATA` **only for named files**. Explicitly exclude all source images, downloaded JSON, third-party RIPE observations, reviewers' materials and metadata with unresolved rights. Zenodo's own default license, if any, must not be mistaken for a grant of these third-party rights.

### Provenance/reproducibility references

- Event raw-source extraction checkpoints: 9 January 2020 08:00 UTC and 10 January 2020 00:00 UTC; official RIB URL/SHA hashes under `releases/FALCON-v1.0-2026-10-29-reviewer/Supplement/Reference_And_Event_Original_RIB_12_SHA256.json`.
- Reference-window checkpoints: 2 January 2020 08:00 UTC and 3 January 2020 00:00 UTC; same source manifest.
- Original-source RIB export commits: event `907b59027807ab292d33886d36e65e2bb07f63c6`, reference `e7d0f51729ef8fffe138fa7fc34a3130455e1ad2`.
- 2020 IODA images: `releases/FALCON-v1.0-2026-10-29-reviewer/Evidence/IODA_2020_Original_Publisher_Image_URLs_and_SHA256.json`; raw provider 2020 numerical series unavailable.
- Software and observed outputs: `releases/FALCON-v1.0-2026-10-29-reviewer/Code/REPRODUCE.md`.

### External source terms requiring author/legal review

- [RIPE NCC copyright statement](https://www.ripe.net/about-us/legal/copyright-statement/)
- [RIPE NCC publicly available services terms](https://www.ripe.net/about-us/legal/terms-of-service/)
- [RIPE Data Repository terms](https://www.ripe.net/about-us/legal/ripe-data-repository-terms-and-conditions/) — **not assumed to apply identically to the separate RIS MRT public archive; verify the exact service-specific terms**
- [Zenodo GitHub metadata and license priority](https://support.zenodo.org/help/en-gb/24-github-integration/149-how-to-specify-a-license-for-a-software-record-on-github)

**Before Zenodo Publish:** obtain file-level rights clearance, decide which manuscript version can be public, remove internal materials from the deposited snapshot, check archive contents, adopt explicit scope-limited licenses with the author's authorization, then approve immutable final SHA. **No publishing is authorized by this document.**
