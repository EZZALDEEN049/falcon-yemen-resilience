# Data dictionary and methodological separation

**RIPE RIS 2020:** `BGP_2020_peer_prefix_records.csv` is the exported first-snapshot tuple `(collector,target_as,peer_asn,peer_ip,prefix)`; same-source `eligible` flags identify peers also found anywhere in the final full RIB, not continuously healthy sessions; `same_origin_retained` indicates the target origin at the same peer/prefix in the second RIB. `neighbor_comparable` requires retained and parsable origin-adjacent AS_PATH; `neighbor_changed` compares the immediate AS_PATH neighbor after collapsing repeated origin prepend. `origin_absent_or_changed_at_endpoint` must not be relabeled a source-observed withdrawal. Prefix and peer distributions aggregate **only comparable** rows. `BGP_2020_validated_unit_summaries.csv` records matched denominators and descriptive medians. Six source RIB filenames, byte sizes and hashes are in each original `audit.json` and `Table_S5_Original_RIB_Manifest.csv`. Full source-native RIB binary archives are **not enclosed**.

**IODA 2020:** The two published PNGs were retrieved and independently pixel-read (publisher URL, source SHA-256 and calibration metadata included). Derived CSV columns represent image raster x-columns and deterministic analyst-grid variants; **not** provider-original 2020 signal samples or independent replications. Publisher-owned original images are deliberately not redistributed as publication figures. Raw source numeric arrays not recovered.

**IODA 2023:** Original provider-JSON archive and separate 150-setting, nonoverlapping window grid; distinct maintenance episode, not the 2020 cable cut.

**RIPE Atlas 2020:** only archived source-qualified one-target (measurement 8307351) aggregate evidence; no population-wide estimate.

**Observational units:** first-row peer-prefix count 11,419; eligible matched 11,293; retained/comparable 10,333; changed 6,547 across six AS/collector cells. Peer, prefix and collector repetitions are dependent.
