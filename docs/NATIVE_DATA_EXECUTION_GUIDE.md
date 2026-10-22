# Practical primary-data upgrade (do not mistake this guide for completed acquisition)

Execute these commands on a computer with reliable outbound HTTPS and no institutional firewall restrictions:

```bash
python -m pip install requests matplotlib
python code/download_ioda_raw.py --event FALCON_2020 --out raw_ioda
```

**Check** `raw_ioda/manifest.json`: confirm nonempty `successes`, inspect original per-entity `.json` manually, confirm observed datasource IDs (the parser's generic `signal` strings can differ across server versions). Once `FALCON_2020_asn_30873.csv` has been verified as a native export of both distinct signal families:

```bash
python code/validate_native_ioda.py --csv raw_ioda/FALCON_2020_asn_30873.csv --out results/native_ioda_AS30873.json
```

The native validator will abort on empty/ambiguous signals, duplicates, inadequate window coverage, invalid baselines, and malformed timestamps. It **does not infer customer traffic** or historical routes. API server defaults and rate limits should be checked on the official Swagger before retrieval.

## Historical BGP: critical correction

The pre-existing `code/historical_bgp_bgpreader.py` **must not be used to release numbers**: filtering BGP UPDATE records by origin ASN loses originless `W` withdrawal records. Instead:

1. Install CAIDA BGPReader following https://bgpstream.caida.org/docs/tools/bgpreader .
2. Verify 2020 prefix inventory from a historical origin-filtered RIB for AS30873 / AS12486 across selected RIS or RouteViews collectors, **not** the August 2026 snapshot.
3. Obtain one archived RIB (same collectors and peer IPs) preceding PRE, and an **all-announcement/all-withdrawal** update stream for the corresponding historical prefix set: apply *prefix* filters (`-k CIDR`) rather than `-a AS30873` on updates. When using a large prefix set, design an archive-efficient acquisition and check coverage independently.
4. Check that the export covers the entire seed-to-event time window and that a disappearance of a collector-peer vantage is distinguishable from a withdrawal. The guarded analyzer refuses unexplained disappearances.
5. Create a UTF-8 `historical_prefixes_2020.txt` file with one validated historical prefix per line; obtain the two BGPReader element-format files (one RIB, one updates):

```bash
python code/historical_bgp_replay_v2.py \
 --rib verified_2020_seed_rib.txt \
 --updates verified_2020_prefix_updates.txt \
 --inventory historical_prefixes_2020.txt \
 --asn 30873 \
 --pre 2020-01-09T08:30:00Z \
 --event 2020-01-09T18:30:00Z \
 --out results/2020_scoped_replay.json
```

**Important:** this offline scoped analyzer is a safeguard prototype, not a full validated route-reconstruction package. Replaying only a prefix-scoped archive cannot itself prove that all event-time prefixes are represented, that peer status is constant, or that the initiating cable path caused a route change. Do not publish route-level effect sizes until those items are verified independently. Source: https://bgpstream.caida.org/docs/api/pybgpstream/_pybgpstream.html .

## Reproduce results already supported by evidence

```bash
python code/test_guardrails.py
python code/reproduce_all.py
# Source: results/phase_specific_plot_proxy_comparison.csv (Table S1)
```

No API secret or paid-access credential is required for the scripts as written. This guide does not require a Scopus API key.
