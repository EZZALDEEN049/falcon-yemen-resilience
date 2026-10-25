# FALCON manuscript v4 research checkpoint — 25 October 2026

## Completed and verified in this session
- Prepared **local DOCX v4**: `Manuscript_FALCON_v4_2023_Robustness_and_BGP_Audit.docx`. This file is delivered through ChatGPT artifact, **not yet committed to this GitHub repository**. Its source is the user-provided v3 DOCX.
- 22 rendered pages checked visually; six numbered figures, eight existing tables, 37 numbered references, 250-word abstract.
- New Figure 6: deterministic window-sensitivity audit from original **Nov 2023 IODA** BGP and ping-slash24 measurements for two ASNs.
- Grid: three 2023 baseline lengths (12, 18, 24 h) × five window-start offsets × five window-end offsets = 75 configurations per AS/signal, 300 total. All satisfy specified 95% sample coverage.
- AS30873 2023 retention: BGP **37.557–40.271%**, active ping **55.0–65.0%**, paired BGP-minus-active **−24.729 to −14.729 pp**. AS12486 both median signal retentions **100%** across tested windows. Not independent observations, not confidence intervals, and the active /24 denominator is small.
- Re-checked **RIPE RIS rrc00 Jan 9 2020 08:00 UTC** origin-filtered historical discovery: AS30873: 6,611 origin RIB rows, 109 candidate prefixes, 121 peer IPs; AS12486: 428 rows, seven candidate prefixes, 117 peer IPs. Source archives recorded HTTP/connection transfer errors; these are **NOT complete inventories or route-retention results**.
- New RIPEstat routing-status cloud run: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40148121847. 16 historical AS snapshot results (8 times × two ASNs) returned all-zero IPv4 prefix counts, including before the 2020 failure. These conflict with the RRC00 origin RIB and were **discarded**, not treated as observed outages. The tool status was hardened in commit `e71ff8517e8ab9ce5a17b9d22717920bc3849306` to fail closed on such contradictory zeros.
- Built an offline ZIP for the authors containing v4 DOCX, original raw archived source ZIPs, Source SHA-256 manifests, Figure 6, complete supplementary 2023 robustness grid, BGP discovery audit and portable Python reproduction scripts. Re-ran both supplied Python checks from the copied release contents with exit status zero.

## Research not yet complete; do not call manuscript Q1-ready
1. Original January 2020 IODA BGP and active-probing numeric series remain unavailable in tested public endpoints. Official archival steward confirmation/access still pending.
2. Complete RIPE RIS/RouteViews historical MRT RIB+updates from independently complete collectors, unfiltered announcements/withdrawals and peer-liveness validation **not obtained**. No claims of physical cable-to-IP-route attribution, route-level survival or causal cascading effects.
3. Manuscript references and licences require final independent author verification; author sign-off, journal format check, data deposit and publication access/licence decision outstanding.
4. Original 2020 plot digitization does not reproduce directly from redistributed third-party image pixels; its full sensitivity grid is descriptive rather than inferential.

## Core official documentation
- https://ris.ripe.net/docs/mrt/
- https://stat.ripe.net/docs/data-api/api-endpoints/routing-status
- https://www.caida.org/projects/ioda/
- https://www.teleyemen.com.ye/index.php/media-center-ar/news-press-releases-events/72-80
