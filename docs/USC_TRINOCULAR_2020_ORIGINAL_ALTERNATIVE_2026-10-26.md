# January 2020 original measurements — new verified USC/ISI avenue (26 Oct 2026)

## Finding: contemporaneous archived *original* active probing dataset exists, but is NOT IODA
USC/ISI ANT Trinocular publishes dataset identifiers (not unrestricted downloads) covering the 9 Jan 2020 Yemen FALCON outage:
- `internet_outage_adaptive_a39all-20200101`, **1 Jan–1 Apr 2020**, published 2.13 GB, post-processed /24 down/up or outage data (~3.5M globally responsive /24 subnets). **Priority for access.**
- `internet_outage_adaptive_a39_supplement-20200101`, 165 MB of AS, IP, organization supplemental mappings. **Needed for event-time AS30873 / AS12486 matching.**
- `internet_outage_adaptive_a39c-20200101`, `a39e`, `a39g`, `a39j`, `a39n`, `a39w`: separate-site raw probing feeds, approximately 694–932 GB **each**, not necessary unless an event-time slice can be shared; request a filtered Jan 8–12 2020 UTC export for the two ASNs and Yemen-address /24s instead.
- IMPACT dataset DS-1450 / DOI **10.23721/109/1518595** is `internet_outage_adaptive_a39e-20200101` (one raw vantage), requires registered account and access approval.

Authoritative sources:
- https://ant.isi.edu/datasets/all.html (dataset names, sizes and dates)
- https://ant.isi.edu/datasets/outage/ (raw-versus-processed distinction)
- https://ant.isi.edu/datasets/requests.html (data access and institutional email requirements)
- https://ant.isi.edu/datasets/request/ (backup form and signed DUA)
- https://comunda.isi.edu/ (primary request portal)
- https://ant.isi.edu/outage/wm/index.html (historical map since 2018)
- https://outage.ant.isi.edu/ (historical interactive outages)
- https://www.impactcybertrust.org/dataset_view?idDataset=1450
- https://ant.isi.edu/~johnh/CONTACT/ (John Heidemann, johnh@isi.edu)

## Dataset access is NOT done
USC requests an institutional email from the researcher, affiliation, research justification, and signed Data Use Agreement (DUA). The portal may require registration. The USC data archive entry and publicly readable README are **metadata**, not the actual observations. No authorized access was obtained, and no 2020 Yemen subset was downloaded this turn. An interactive world map is **not equivalent to a source numeric time-series export**.

## Data request fields for human completion

WHAT DATASETS:
`internet_outage_adaptive_a39all-20200101` and `internet_outage_adaptive_a39_supplement-20200101`. If possible, grant only Jan 8 00:00 – Jan 12 00:00 UTC /24 records geolocated to Yemen and original Jan 2020 prefix-to-AS mappings identifying AS30873 and AS12486. Site-specific `a39c/e/g/j/n/w-20200101` records for the same /24s/window would support observer-specific sensitivity and are optional.

PROJECT:
"Structural–Functional Divergence During Submarine-Cable Disruptions: Evidence from Yemen's FALCON Dependence", Taiz University, Yemen; nonprofit academic study of Jan 9 2020 FALCON submarine cable outage. Funding status to be stated accurately by the researcher.

WHY:
"We seek independent **contemporaneous Trinocular/ANT active-probing data** to measure the January 2020 event without raster-digitizing published graphics, compare AS30873 with AS12486 using a validated event-date ASN prefix inventory, and distinguish BGP routing visibility from active /24 reachability. We will cite USC/ISI and respect license restrictions. These data will not be claimed as IODA native time-series or as proof of cable-level attribution."

## Official IODA originals still absent
- Source-native `bgp` and `ping-slash24` IODA 2020 series still not recovered after current API and Wayback audits (see `docs/IODA_2020_CUSTODY_RECOVERY_AUDIT_2026-10-26.md`).
- A real IODA recovery requires pre-2021 CAIDA historical DBATS/Graphite partitions or an authenticated historical export by the custodian. Current IODA download-to-CSV capability (introduced in 2023) does not guarantee old 2020 data exist in today's backend.
- Historical ANT Trinocular is an **independent alternative**, and historical RIPE RIS MRT is an **independent BGP source**; never relabel either as original IODA BGP/active aggregates.

## Remaining tasks
1. USC/ISI Comunda application + signed DUA via university email (cannot be completed by assistant unauthenticated).
2. Obtain dataset export or approved access; verify SHA256, timestamp coverage, observed /24s, original ASN mapping, provenance, license.
3. Obtain CAIDA/Georgia Tech reply on 2020 native IODA DBATS status independently.
4. If data arrive, recompute descriptive and robustness results and reconcile *measurement-method differences* openly.

No outgoing email was sent in this turn. A prior connected Gmail send action was denied; do not retry it.
