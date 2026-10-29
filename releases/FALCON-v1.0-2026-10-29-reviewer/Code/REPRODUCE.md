# FALCON — clean-machine verification of the frozen 2026-10-29 reviewer archive

Python >=3.10; the exported-record checks need the Python standard library only.
Unzip the archive, change to the extracted **root**, and run in this order:

```bash
python Code/verify_reviewer_bundle.py
python Code/compare_2020_event_vs_non_event.py \
  --event-root Evidence/BGP_2020 \
  --reference-root Evidence/Reference_2020_20200102 \
  --output-dir QA/REPRODUCED_REFERENCE
python Code/reproduce_native_ioda_2023_v2.py \
  --source-zip Supplement/IODA_2023_Original_JSON_SourceArtifact.zip \
  --out QA/REPRODUCED_IODA_2023.csv
python Code/rebuild_2020_peer_prefix.py --self-test
```

Expected: first verifier PASS (11,419 event rows, original-source export checksums and sensitivity-table checksum); reference comparator PASS (6 source audits, 12 AS/collector/window rows, 6 contrasts and exact peer–prefix key intersections); 2023 IODA reproducer matches the four retentions. The synthetic self-test does **not** re-download original MRT files.

The archive includes 12 ORIGINAL-SOURCE-DERIVED output sets as six collector/windows: RRC00/01/10 for 9–10 January 2020 (event) and 2–3 January 2020 (preselected reference). Check original 12-RIB SHA-256 and URLs in `Supplement/Reference_And_Event_Original_RIB_12_SHA256.json`, and use the pinned official RIPE RIS source URLs when performing a full source-native rerun. **All twelve original large .gz MRT binaries are NOT in this ZIP**; independent refetch and parse requires network access and `pybgpkit-parser`. Event extraction commit: `907b59027807ab292d33886d36e65e2bb07f63c6`. Reference extraction commit: `e7d0f51729ef8fffe138fa7fc34a3130455e1ad2`. Source image provenance commit: `a51805e39f900ca0bdcbd83a32b6dce597b9a345`.

To verify publisher-original January 2020 IODA raster sources, download each PNG without resizing from URLs under `Evidence/IODA_2020_Original_Publisher_Image_URLs_and_SHA256.json`, verify source-byte digests and run `Code/recheck_ioda2020_original_pngs.py` and `Code/digitization_sensitivity.py` after installing Pillow. The archived deterministic 20,250-choice result is plot-derived and is not the unavailable provider-native 2020 IODA numerical series. Permissions to redistribute publisher images are not granted by this bundle.

**Interpretation:** one prespecified historical reference is not a normal-churn sampling distribution, a causal control, or an estimate of customer reachability. AS12486 has 0/54, 0/24, 0/13 eligible event IPv6 routes retaining the same origin at the endpoint; its adjacency-change comparator is effectively retained IPv4 only. RIPE files and peer–prefix records are observational and correlated.

The manuscript's final editorial status is a scoped pre-submission revision, not a publisher acceptance or verified author sign-off. See `QA/FINAL_RELEASE_GATES_2026-10-29.json`.
