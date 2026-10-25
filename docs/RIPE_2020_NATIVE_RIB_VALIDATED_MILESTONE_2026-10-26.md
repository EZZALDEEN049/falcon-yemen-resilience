# January 2020 RIPE RIS original RIB acquisition milestone — 26 October 2026

## Verified acquisition, not outage inference
One complete historical `rrc00` `bview.20200109.0800.gz` from https://data.ris.ripe.net/rrc00/2020.01/ was downloaded in GitHub Actions, checked by full gzip integrity stream and original-file SHA-256, and decoded with the BGPKIT Python MRT parser. All validated origins include explicit peer IP and peer ASN, avoiding peer identity collisions.

**Run:** https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40246225960
**Script:** `tools/ripe_2020_native_rib_pilot.py`

| ASN | origin route rows | candidate prefixes | distinct peer IP+ASN sessions |
| --- | ---: | ---: | ---: |
| AS30873 | 6,611 | 109 | 121 |
| AS12486 | 428 | 7 | 117 |

These are one-collector, one-timestamp (2020-01-09 08:00 UTC) *origin matches*, not all announced prefixes in Yemen, not packet reachability and not pre-to-event route-retention. The archived MRT source is distinct from the unavailable January 2020 original IODA `bgp` and `ping-slash24` series.

## Invalid endpoints and known gaps
RIPEstat `bgp-state` returned zero routes not only for AS30873 but also public controls, so use raw MRT. RIPEstat `bgp-updates` documentation states only Jan 2024+ is indexed as of July 2025; older RIB and update MRT files remain publicly catalogued. Don't infer a complete outage from empty indexed API results.

## Next empirical gate
- Verify a second event-time/post-event 2020 original MRT RIB snapshot, preserving original checksums, peer IPs, and archive completeness.
- Validate that the same peer sessions were observable independently, not just that they retained target prefixes.
- Obtain *all* update A/W observations for the matched historical prefix inventory; withdrawals have no origin AS, so never origin-filter all updates.
- Only after collecting complete checkpoints and updates, compute peer-matched route retention and AS-path change. RRC00 alone gives one collector's perspective.
- USC Trinocular `internet_outage_adaptive_a39all-20200101` offers original contemporary reachability but requires institutional access approval; never call it original IODA samples.
- If original 2020 IODA never recovered, keep only digitization-proxy claims for the IODA-based 2020 contrast, supplemented by separate genuine RIS and USC observations.

**This is a verified extraction milestone only, NOT proof of final historical path reconstruction.**
