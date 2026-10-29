# FALCON — 29 October 2026 pre-Zenodo public-repository audit

**Decision: HOLD the draft release `v1.0.0`. Do not publish it or claim a Zenodo DOI.**

## Verified current repository/release state
- Repo: `EZZALDEEN049/falcon-yemen-resilience`, **public**, default branch `main`.
- The current README was rewritten as a truthful, English evidence-bounded project overview, including all 12 original-source RIB reference/event checkpoints, data provenance and executable commands.
- A draft release with tag proposal `v1.0.0` exists (release ID `427350341`), currently targeting branch `main`, without attached assets. At the first audit `refs/tags/v1.0.0` did not exist. There is **no final approved publication SHA** until all release blockers are closed.
- Separately, the earlier `FALCON-v1.0-2026-10-29` **published prerelease** already has a historical reviewer ZIP; that is a distinct tag and must not be silently moved.
- `CITATION.cff` and `.zenodo.json` each contain a single creator **Ezzaldeen Al-Tayar**, university affiliation in Taiz, no unverified ORCID and no fabricated DOI. Both share a software archive title and have descriptive keywords. In GitHub+Zenodo integration, the Zenodo JSON metadata has priority when present.
- `RELEASE_NOTES_DRAFT_v1.0.0.md` contains a corrected release narrative; the actual GitHub draft release description has **not** been updated (the current connector lacks a release-edit action). Its phrase “published analyses” should be changed to “analyses documented in a pre-submission manuscript.”
- A one-use GitHub Actions transfer workflow containing an expiring signed file URL was deleted from the active `main` tree; its old content **remains reachable in Git history**. A signed URL is not proof of long-lived credential exposure, but any genuinely leaked secrets must be revoked/rotated. History audit/purge has not been performed.

## Whole-tree A/B/C/D triage (path metadata only; provisional)
The complete per-file snapshot is `PUBLIC_RELEASE_FILE_CLASSIFICATION_2026-10-29.csv` and covered **354 blobs** in a complete, untruncated GitHub tree immediately after removing the one-use workflow. 80 A candidates, 113 B rights review, 45 C internal/confidential, 116 D historical/superseded. Later new documentation files are not part of that initial 354-row CSV.

**A — candidates**: author-origin scripts and tests, public documentation, safe method/provenance notices and eligible self-made figures. **A means pending author sign-off**, not that licenses have already been granted.

**B — third-party rights unresolved**: RIPE RIS routing data and source-derived CSV rows, IODA 2023 native JSON and 2020 publisher-derived plotted traces, Atlas materials, and any figures derived from third-party publisher assets. Their official URLs and SHA-256 can be published as provenance, but open sublicensing or redistribution cannot be assumed.

**C — exclude from public Zenodo source snapshot**: `releases/FALCON-v1.0-2026-10-29-reviewer/Review/`, `Historical_Superseded/Review/`, `paper/`, internal cover letter, internal review response and unapproved pre-submission manuscript and supplementary materials. These are *already present* on the public GitHub branch; do not assume staging/deleting them in a later commit erases exposure from history.

**D — exclude or document as historical**: old `docs/`, `archive/legacy/`, old staging results, obsolete workflows/triggers, duplicate smoke-test outputs, outdated research descriptions.

## Scientific verification and what it does not show
- Prior GitHub Actions run successfully downloaded the exact 29-Oct reviewer ZIP, verified its SHA-256, validated the file manifest (151 entries), ran `Code/verify_reviewer_bundle.py`, `Code/compare_2020_event_vs_non_event.py`, and `Code/rebuild_2020_peer_prefix.py --self-test`, and published a distinct historical prerelease. Checks were on archived extracts, not new complete RIPE MRT binary reprocessing.
- Latest review package resides at `releases/FALCON-v1.0-2026-10-29-reviewer/`; main event: 9 Jan 08:00 to 10 Jan 00:00 UTC; one earlier reference: 2 Jan 08:00 to 3 Jan 00:00 UTC; RRC00/RRC01/RRC10, AS30873/AS12486.
- Neither BGP path change nor missing same-origin endpoint IPv6 entries proves physical cable path causality, withdrawal, outage of individual subscribers, or a population distribution of normal churn.
- Original numerical 2020 IODA provider series have not been recovered; published 2020 plot-derived values are secondary estimates.

## Release blockers — mandatory before `Publish release`
1. **Remove unapproved C materials and source-redistribution-unapproved B materials from the exact archive to be deposited.** A full GitHub snapshot cannot be safely archived merely by adding `README` or excluding a few paths from a README. Consider a separate clean release-only branch or repository, after confirming Zenodo's GitHub integration can archive that exact intended snapshot. If it cannot, curate the existing repository before tagging, without deleting necessary evidence irreversibly.
2. **Assess exposure in published historical Git releases/assets and commit history**, decide whether any sensitive details require a private incident response or repository-history purge, and revoke any real live credentials exposed.
3. Obtain explicit author permission for the public manuscript/preprint and research-code license; source-specific RIPE, IODA and Atlas redistribution terms must be checked. See `DATA_LICENSES_AND_PROVENANCE.md`.
4. Decide the **scoped** license for author-owned code and separately for eligible author-owned derived data; no blanket MIT/CC BY and no third-party sublicensing.
5. Verify the actual `v1.0.0` draft title/description/asset list is consistent with a clean package and the code-vs-data archive type. Fix the ambiguous draft description. Do not claim the study was published in Scientific Reports.
6. Complete bibliography checks of 38 references, policies and relevant author declarations; perform a clean independent smoke test from a **curated, rights-cleared** archive.
7. Inspect `CITATION.cff`, `.zenodo.json` and the final `README.md` **at the exact final SHA**, and confirm that `v1.0.0` resolves to that SHA. No tag/DOI should be fabricated in advance.

## Security and completeness limits
The inventory covers GitHub's current tree paths, sizes and blob SHAs and a focused inspection of selected code/README/workflows. It does **not** represent a full byte-by-byte scan of all 354 files, compressed archives, full Git history or Actions logs. No conclusive statement that there are no hidden credentials, personal information or third-party rights restrictions is made.

**Current release status: BLOCKED / DRAFT ONLY.** Scientific code/data remain useful for internal review, but *Zenodo public snapshot safety has not been certified*.

Related documents: `PUBLIC_RELEASE_FILE_CLASSIFICATION_2026-10-29.csv`, `DATA_LICENSES_AND_PROVENANCE.md`, `RELEASE_NOTES_DRAFT_v1.0.0.md`, `README.md`.
