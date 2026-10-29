# FALCON Yemen 2020 — reviewer source-verification protocol (30 October 2026)

**Purpose.** Give editors and reviewers an executable, transparent route from the official *original-source* archives to the author-prepared BGP and IODA results. This protocol is published within the **software v1.0.2** release; it was absent from v1.0.1. The author authorizes this original script-and-provenance documentation release. It contains **no RIPE MRT binaries, observer-level source-derived CSV, IODA publisher PNG bytes, or IODA provider-native JSON**.

**Do not mistake test levels:** (1) prior source-native project execution of twelve RIS RIBs, (2) the **30 October 2026 independent recomputation of 11,419 archived event rows and 10,968 archived reference rows**, (3) the 30 October public-source IODA raster verification from original previously collected publisher PNGs with full 20,250-grid SHA256 match, (4) the 30 October IODA 2023 check from previously archived raw JSON, and (5) full *fresh source-native reread of all twelve MRT files* — **not executed on 30 October**. The script below provides a fail-closed executable method for (5), not evidence that it passed.

## Original RIPE RIS — 12 RIBs / six collector-window pairs

Source: RIPE RIS official **data.ris.ripe.net**, not the RIPE Registry/Database or unrelated RIPE Data Repository; source terms must be checked specifically for RIS. Event: **2020-01-09 08:00 UTC to 2020-01-10 00:00 UTC**. Reference: **2020-01-02 08:00 UTC to 2020-01-03 00:00 UTC**. Collectors: **RRC00, RRC01, RRC10**. Target origin ASes: **AS30873 and AS12486**. The reference date was chosen retrospectively and locked before reference outcomes were inspected.

The self-contained JSON `Reviewer_Reproducibility_Protocol/RIPE_RIS_12_RIB_Source_URLs_SHA256.json` records all **twelve original RIPE URLs, exact source bytes and SHA-256 digests**. Total compressed source size across all URLs is **3,748,928,807 bytes** (about 3.75 GB, plus local temporary/decoded output space). The downloaded originals remain **on the editor/reviewer's machine**; do not upload them or redistribute third-party source data without authorization.

The canonical source extractor `Code/rebuild_2020_peer_prefix.py` is included in this v1.0.2 release, and also existed in software v1.0.1 (DOI: <https://doi.org/10.5281/zenodo.23751733>). Suggested reproducible workflow from a directory containing this protocol:

```bash
# Python 3.10+; download historical RIBs only if permissions and disk space permit.
git clone --depth 1 --branch v1.0.2 https://github.com/EZZALDEEN049/falcon-yemen-resilience.git falcon-software
cd falcon-software
python -m pip install 'pybgpkit-parser>=0.6,<1' 'Pillow>=10,<13'

# Offline checks: source URL layout, SHA format, expected table content, parser presence.
python Reviewer_Reproducibility_Protocol/rebuild_ripe_12_mrt.py \
  --manifest Reviewer_Reproducibility_Protocol/RIPE_RIS_12_RIB_Source_URLs_SHA256.json \
  --expected-s14 Reviewer_Reproducibility_Protocol/Table_S14_2020_Reference_vs_Event_Collector_Summaries.csv \
  --expected-s15 Reviewer_Reproducibility_Protocol/Table_S15_2020_Reference_vs_Event_Common_Peer_Prefix.csv \
  --canonical-parser Code/rebuild_2020_peer_prefix.py --preflight

# On a networked computer: download all 12 original MRT files (3.75 GB),
# verify each original byte count, SHA256 and gzip CRC, reparse, and fail
# if any collector-AS-period count or fixed-key comparator differs.
python Reviewer_Reproducibility_Protocol/rebuild_ripe_12_mrt.py \
  --manifest Reviewer_Reproducibility_Protocol/RIPE_RIS_12_RIB_Source_URLs_SHA256.json \
  --expected-s14 Reviewer_Reproducibility_Protocol/Table_S14_2020_Reference_vs_Event_Collector_Summaries.csv \
  --expected-s15 Reviewer_Reproducibility_Protocol/Table_S15_2020_Reference_vs_Event_Common_Peer_Prefix.csv \
  --canonical-parser Code/rebuild_2020_peer_prefix.py \
  --work-dir reviewer_local_RIPE_source_rebuild
```

Check outputs in `reviewer_local_RIPE_source_rebuild/reconstructed/`. The original extractor's ASN/peer/prefix rules are supplied in the tagged code. It does not estimate cable causality, user reachability, continuous BGP UPDATE chronology, or typical background churn. The full source replay is resource-intensive and may reveal archival/parser-version differences that **must be reported rather than overwritten**. For source validation, `--verify-only` can be used after acquiring all original files separately. **The unverified tool-specific full 12-MRT rerun does not currently qualify as a passed QA test.**

## IODA January 2020 — 20,250 deterministic settings

Official **publisher raster** provenance: `IODA_2020_Publisher_Image_Links_SHA256.json`, including unchanged source URLs and exact original PNG byte hashes. Note the AS30873 publisher filename **as30783**, while the verified raster's caption is AS30873; do not silently correct or infer identity from filename alone. These are **published plots, not source-native IODA time series**. The analysis must be described as calibrated extraction; calibration perturbations are NOT 20,250 independent network observations.

```bash
python Reviewer_Reproducibility_Protocol/recheck_ioda_2020_from_publisher.py \
  --manifest Reviewer_Reproducibility_Protocol/IODA_2020_Publisher_Image_Links_SHA256.json \
  --code-dir falcon-software/Code \
  --work-dir reviewer_local_IODA2020
```

This script downloads only locally, verifies both original publisher PNG SHA-256 values and full-size pixel geometry, runs `Code/recheck_ioda2020_original_pngs.py` and regenerates 20,250 settings via `Code/digitization_sensitivity.py`. **Expected full CSV SHA-256:** `fa9720246ec52edb6770c8637f52da260856908574fb490a4d49f0e825245e12`. This exact full-grid SHA was independently reproduced from the author's original publisher images on 30 October 2026. Original images are NOT included in the protocol, Zenodo datasets or publication supplement. Publisher website uptime is external and not guaranteed.

## IODA November 2023 — secondary event, not January 2020 validation

`IODA_2023_API_ORIGINAL_RESPONSE_URLS_SHA256.json` contains source API request URLs and archived **raw-response SHA-256 values** for AS30873 and AS12486. Original provider JSON is **not** in public dataset v1.0.2 and cannot be automatically relicensed. This auxiliary event does not contribute to core January 2020 BGP results or constitute a control. When public provider endpoints still serve *identical* 2023 response bytes, a reviewer may run:

```bash
python Reviewer_Reproducibility_Protocol/verify_ioda_2023_api.py \
  --manifest Reviewer_Reproducibility_Protocol/IODA_2023_API_ORIGINAL_RESPONSE_URLS_SHA256.json \
  --reproduce-script Code/reproduce_native_ioda_2023_v2.py \
  --private-working-dir reviewer_local_IODA2023
```

This fails if the historical API is blocked or the response differs, **without inventing values**. On an internal author-controlled copy, the 30 October verifier reproduced all four previously reported values; legal redistribution of that provider JSON to readers/reviewers is **not** established. The editor can ask the author for a source-compliant verification route; if neither source endpoint access nor licensed supervised access is available, the 2023 ancillary analysis must be **removed from the final claims** rather than declared publicly reproducible.

## What reviewers can check now vs open conditions

| Gate | 30 October verified status |
|---|---|
| Canonical public 2020 aggregate dataset, source provenance and DOI | PRESENT on tagged GitHub/Zenodo metadata, not source-level dump |
| From archived route-level CSVs: 11,419 event, 10,968 reference, 12 groups, six common cohorts | **PASS**, internal research audit (source-derived observations not for re-upload) |
| Twelve original RIB URLs, byte counts, checksum completeness and command preflight | **PASS** |
| Fresh download/decode all twelve ~3.75 GB original RIBs | **NOT RUN**, requires network, time, disk and third-party parser |
| 2020 publisher original-size raster byte fingerprints, proxy recheck, all 20,250 calibration settings | **PASS** from source PNGs held locally; full-grid SHA matched exactly |
| 2023 source JSON four-value replay from author-held original response | **PASS** internally; independent API re-fetch **NOT VERIFIED** |
| 2020 original provider-native IODA numeric series | **UNAVAILABLE; not claimed** |
| Third-party source data redistribution permissions | **UNRESOLVED**, so do not include source files in open deposits |

## Journal policy and source-terms caution

[Scientific Reports editorial policy](https://www.nature.com/srep/journal-policies/editorial-policies) requires supporting data for editors and referees at submission and a meaningful access route. If an archival source is inaccessible or source-origin data use terms prevent the necessary access, **the author must resolve the constraint with the source provider and journal rather than simply cite a DOI for aggregates**. The RIPE NCC's RIS service is distinct from the RIPE Data Repository; do not apply the latter's restrictions uncritically to RIS. RIPE RIS official access: <https://www.ripe.net/analyse/internet-measurements/routing-information-service-ris/>. IODA source terms for provider data should be established before redistributing raw JSON or publisher PNGs.

**Status:** The **documentary reproducibility gap has been addressed with working source reconstruction scripts and archived-data tests**. Full external primary-source access and any permissions conditions remain distinct requirements, not silently marked complete.
