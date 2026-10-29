# FALCON Yemen 2020 — Version 1.0.2 reviewer source-reconstruction protocol

**Pre-submission research software; not an accepted/published Scientific Reports article.**

This is a curated, author-owned software-only release for **Ezzaldeen Al-Tayar**, Faculty of Engineering and Information Technology, Taiz University, Yemen. It extends software v1.0.1 by adding command-line checks for publisher sources, historical RIPE RIS RIB reconstruction, fixed-peer–prefix cohorts, and 2023 IODA provider API response checks.

The separate **aggregated research dataset v1.0.2** is available under DOI [10.5281/zenodo.23752785](https://doi.org/10.5281/zenodo.23752785). The software edition v1.0.1 remains available under DOI [10.5281/zenodo.23751733](https://doi.org/10.5281/zenodo.23751733). A new software DOI is **not assumed until Zenodo finishes processing the v1.0.2 GitHub release**.

## What is and is not included

The public release contains Python scripts under `Code/` and `Reviewer_Reproducibility_Protocol/`, provider source URL/checksum **text-only** manifests, author-produced *aggregate comparison reference tables* S14 and S15, and documentation. Source-derived RIPE peer–prefix individual CSVs, original RIPE MRT binary archives, IODA 2020 publisher PNG bytes, IODA 2023 provider JSON response payloads, internal reviewer memos, unpublished manuscript drafts, and other rights-unclear materials are **excluded**.

Original source data are independently available from the provider subject to their terms. Neither the public repository nor the DOI dataset contains all the primary data needed for full source-level reconstruction, and the scripts below must be run on a machine with sufficient external source access. Publisher PNG-derived proxies are secondary estimates, not 2020 provider-native IODA numeric time series.

## Offline quick checks (Python >=3.10)

Run from this repository root:

```bash
python -m compileall -q Code Reviewer_Reproducibility_Protocol
python Code/rebuild_2020_peer_prefix.py --self-test
python Reviewer_Reproducibility_Protocol/rebuild_ripe_12_mrt.py \
  --manifest Reviewer_Reproducibility_Protocol/RIPE_RIS_12_RIB_Source_URLs_SHA256.json \
  --expected-s14 Reviewer_Reproducibility_Protocol/Table_S14_2020_Reference_vs_Event_Collector_Summaries.csv \
  --expected-s15 Reviewer_Reproducibility_Protocol/Table_S15_2020_Reference_vs_Event_Common_Peer_Prefix.csv \
  --canonical-parser Code/rebuild_2020_peer_prefix.py --preflight
python Reviewer_Reproducibility_Protocol/recheck_ioda_2020_from_publisher.py \
  --manifest Reviewer_Reproducibility_Protocol/IODA_2020_Publisher_Image_Links_SHA256.json \
  --code-dir Code --preflight
python Reviewer_Reproducibility_Protocol/verify_ioda_2023_api.py \
  --manifest Reviewer_Reproducibility_Protocol/IODA_2023_API_ORIGINAL_RESPONSE_URLS_SHA256.json \
  --reproduce-script Code/reproduce_native_ioda_2023_v2.py --preflight
```

Offline *preflight* tests only check configuration, paths, expected counts, schema and parser self-test. They do **not** prove a clean 12-MRT re-download, IODA API availability or access permission.

## Networked source reconstruction (reviewer-controlled local files only)

Requirements: 12 public RIPE RIS original MRT archives (~3.75 GB compressed), Python 3.10+, `pybgpkit-parser` for independent MRT decoding, `Pillow` for 2020 raster verification, sufficient disk/memory and the source providers' permitted access.

```bash
python -m pip install 'pybgpkit-parser>=0.6,<1' 'Pillow>=10,<13'
python Reviewer_Reproducibility_Protocol/rebuild_ripe_12_mrt.py \
  --manifest Reviewer_Reproducibility_Protocol/RIPE_RIS_12_RIB_Source_URLs_SHA256.json \
  --expected-s14 Reviewer_Reproducibility_Protocol/Table_S14_2020_Reference_vs_Event_Collector_Summaries.csv \
  --expected-s15 Reviewer_Reproducibility_Protocol/Table_S15_2020_Reference_vs_Event_Common_Peer_Prefix.csv \
  --canonical-parser Code/rebuild_2020_peer_prefix.py \
  --work-dir ./reviewer_local_RIPE_rebuild
python Reviewer_Reproducibility_Protocol/recheck_ioda_2020_from_publisher.py \
  --manifest Reviewer_Reproducibility_Protocol/IODA_2020_Publisher_Image_Links_SHA256.json \
  --code-dir Code --work-dir ./reviewer_local_IODA2020
python Reviewer_Reproducibility_Protocol/verify_ioda_2023_api.py \
  --manifest Reviewer_Reproducibility_Protocol/IODA_2023_API_ORIGINAL_RESPONSE_URLS_SHA256.json \
  --reproduce-script Code/reproduce_native_ioda_2023_v2.py \
  --private-working-dir ./reviewer_local_IODA2023
```

**Expected source limits:** the RIPE 12-MRT fresh reparse is runnable but **has not been fully rerun in the author test**. IODA 2020 full 20,250-setting sensitivity table was reproduced from the author's previously retained original publisher PNGs, with output SHA-256 `fa9720246ec52edb6770c8637f52da260856908574fb490a4d49f0e825245e12`. November 2023 original JSON was verified privately, **not independently refetched from the live historical API**. A remote source change or unavailable endpoint must cause a failure, not a made-up PASS.

## Measurement scope and attribution limits

Event: January 9 08:00 to January 10 00:00 UTC 2020; retrospectively fixed earlier reference: January 2 08:00 to January 3 00:00 UTC 2020. RIPE RIS collectors **RRC00, RRC01 and RRC10**; origin ASes **AS30873 and AS12486**. Observed BGP peer–prefix AS_PATH data support descriptive origin-adjacent reconfiguration only. A single earlier reference is not an empirical background-churn distribution; IPv6 same-origin endpoint nonretention is not equivalent to confirmed withdrawal or customer outage. Neither these controls nor the separately analysed 2023 IODA event prove physical FALCON cable causality.

## Licenses and source provenance

The original author-owned source software under `Code/` and `Reviewer_Reproducibility_Protocol/*.py` is MIT licensed as stated in `Code/LICENSE`. The small author-prepared aggregate S14/S15 reference CSVs and original accompanying documentation are **CC BY 4.0**, matching the separate author-prepared aggregate-data deposit; this grant does not apply to source-level third-party data. External RIPE/Atlas/IODA data, publisher images, provider-native JSON, and material not written by the author remain subject to their separate terms and are **not sublicensed here**. See `RIGHTS_STATUS.md` and `Reviewer_Reproducibility_Protocol/README_REVIEWER_SOURCE_RECONSTRUCTION.md`.