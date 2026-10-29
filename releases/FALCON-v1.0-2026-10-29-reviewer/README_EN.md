# FALCON — 29 October 2026 independent reviewer release, E1–E4 repairs

**Status: pre-submission peer-review handoff only; NOT submission-ready or an editorial approval.**

## Current exact paths
- `Manuscript/FALCON_Final_Editorial_Revision_2026-10-29.docx` and `.pdf`
- `Supplement/Online_Resource_1_FALCON_Final_2026-10-29.docx` and `.pdf` (Tables S1–S15)
- `Review/Response_to_Reviewers_FALCON_Final_2026-10-29.docx` and `.pdf` (independent/internal review only)
- `Supplement/Atlas_2020_audit.zip` (aggregated source-audit JSON, not original raw per-result source payload)
- `Evidence/BGP_2020/`, `Evidence/Reference_2020_20200102/` and `Supplement/Reference_And_Event_Original_RIB_12_SHA256.json`
- `QA/FINAL_RELEASE_GATES_2026-10-29.json`, `FILES_MANIFEST_SHA256.json`
- `Review/REFERENCE_AUDIT_38_INTERNAL_FORMAT.csv` (internal formatting/indexing only; NOT comprehensive independent external DOI/metadata verification)

## Reproduce from unpacked archive root

```bash
python Code/verify_reviewer_bundle.py
python Code/compare_2020_event_vs_non_event.py --event-root Evidence/BGP_2020 --reference-root Evidence/Reference_2020_20200102 --output-dir QA/REPRODUCED_REFERENCE_LOCAL
python Code/reproduce_native_ioda_2023_v2.py --source-zip Supplement/IODA_2023_Original_JSON_SourceArtifact.zip --out QA/REPRODUCED_IODA_2023.csv
```

**Design limit:** The January 2–3 reference was retrospectively fixed before examining its own outcomes, not prospectively preregistered before the January 9 incident or event analysis. It is one descriptive interval, not a normal-churn population distribution or counterfactual. All BGP observations share correlated vantages and are not measurements of physical cable usage or end-user traffic. 2020 IODA is image-derived secondary evidence, not original numerical provider series.

**Before journal upload:** independent verification of all 38 references, publisher image reuse rights, every author's explicit approval, official journal article type/template and declarations, repository access and record permissions. Do not file internal responses as a formal journal response to reviewers.
