# Complete 16-hour original RIPE RRC00 MRT A/W file audit (26 Oct 2026)

## Audit
- The **192** original five-minute `updates` MRT files, from 2020-01-09 08:00 inclusive to 2020-01-10 00:00 UTC exclusive, were downloaded, CRC-gzip decoded and SHA-256-hashed without missing slices.
- Source and full 192-row original checksum manifest: `results/ripe_2020_source_original_16h_aw_manifest.json`.
- RIPE docs: https://ris.ripe.net/docs/mrt/
- 8 independently completed chunk source run: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40250556262

## Historical origin-filtered candidate-prefix observation counts, RRC00 only
| Measurement | AS30873 | AS12486 |
| --- | ---: | ---: |
| Candidate-origin announcement *messages* | 102,836 | 2,859 |
| Candidate-prefix withdrawal *messages* (origin unknown) | 4,904 | 120 |

Candidate prefix universe: 109 AS30873-origin and 7 AS12486-origin prefixes from first historical RRC00 RIB discovery only. Files were confirmed contiguous, but an archived announcement or withdrawal does NOT prove a cable-related event, outage, route withdrawal from the target AS, customer traffic change, or globally complete BGP behavior.

Messages may be repetitive, are highly dependent by peer and prefix, and are not independent samples. The 16-hour sample begins at the first 08:00 UTC RIB; per-peer route state requires replay, RIB reconciliation and validation of monitor sessions. This dataset is distinct from missing 2020 IODA raw `bgp` and `ping-slash24` measurements.

## Distinct original-MRT BGP evidence already validated
Three independent RIS RRC full-RIB collectors `rrc00`, `rrc01`, `rrc10` found the same AS30873 immediate AS_PATH neighbor transition toward AS174. See `docs/TRIPLE_COLLECTOR_RIPE_2020_VALIDATION_2026-10-26.md` for original SHA-256s and peer-verified matching methodology.

## Decision
This fills the source **collection/integrity** gap for 192 consecutive RRC00 update files, but does not yet fill the **event-time full BGP state reconstruction** or **original 2020 active probing** gaps. Do not report the UPDATE message counts as scientific estimates of cable-induced lost routes.
