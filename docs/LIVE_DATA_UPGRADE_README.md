# Optional Path-B empirical upgrade

The submission-safe manuscript does **not** release unsupported route-level BGP metrics. The scripts below are provided for a future stronger empirical revision.

## Raw IODA
Official API base: https://api.ioda.inetintel.cc.gatech.edu/v2/

Run from `Supplement/` in a network-enabled environment:

```bash
python code/download_ioda_raw.py --out raw_ioda --event ALL
```

Release rule: replace raster-derived proxy results only if the downloaded responses contain validated non-empty time-series for the required event/entity windows. Analyze each datasource separately (BGP, active probing, telescope/traffic where available); do not collapse them into one latent Q without calibration.

## Historical BGP
CAIDA BGPReader supplies historical Route Views and RIPE RIS records through BGPStream. Install BGPStream/bgpreader using CAIDA's official instructions, then run:

```bash
python code/historical_bgp_bgpreader.py --out raw_bgp
```

Release rule: publish PVR/ROR/USF/provider-set churn/AS-path inflation/path diversity only after non-empty reconstruction and comparison on matched collector-peer vantage points.

## Fail-closed policy
Empty API/MRT responses are acquisition failures, not evidence of outage. No scientific metric is generated from an empty retrieval.
