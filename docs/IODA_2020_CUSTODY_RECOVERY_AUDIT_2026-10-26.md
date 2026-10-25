# IODA January 2020 — archival restoration and custody audit (26 October 2026)

**Strict result: ORIGINAL_NATIVE_2020_BGP_AND_PING_DATA_NOT_RECOVERED.**

## Requested data, and why they matter
- Entities: AS30873, AS12486, Yemen (country code YE). Period **2020-01-08 00:00 UTC to 2020-01-12 00:00 UTC**.
- Source-native IODA signals `bgp` (visible /24s) and `ping-slash24` (up /24s), unnormalized values, native cadence, UTC timestamps, collection changes, entity mapping, usage permissions.
- Only these original IODA measurements can legitimately replace the manuscript's plot-digitized 2020 proxy values.

## Checks completed in GitHub Actions
1. **Official IODA v2 raw API:** HTTP 200, `data:[[]]` for the 2020 target ASes/country, including filtered requests. Requests for the independent 2023 event, January 2022 and October 2026 return samples, proving the service can return native signals for other dates. Runs: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40025032008 , https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40026956956.
2. **Legacy CAIDA hosts and alternate endpoints:** DNS/network/TLS access failed from prior cloud runners for legacy endpoints; outage-related endpoints differ from raw signal endpoint. A nonempty IODA `signals/events` response held `outages` indicators, **not** original BGP or ping samples. Forensic original responses saved in https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40032653939.
3. **Independent Internet Archive audit, 26 October 2026:** six precisely scoped Wayback Availability API requests had **no snapshot**. Three CDX searches for legacy signal-series paths had **no records**; a broad search found four JSON archive listings, all from 2021–2022 and documenting *alerts*, not original 2020 `bgp`/`ping-slash24` value arrays. The existence of listed 2021/2022 alert responses is no evidence the 2020 source time series were ever archived. The raw audit requests and responses are preserved in https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40238454010.
4. Search for downloadable independent original IODA samples for FALCON January 2020 found incident **figures**, third-party event descriptions, and other outage datasets, not an attributable original time series. Public GitHub repository `InetIntel/internet_outages` hosts a curated outage-event list, *not source-native 2020 BGP and ping measurement series*.
5. RIPE RIS/RouteViews archived MRT records are **independent BGP route observations**, not the proprietary historical IODA `bgp` aggregate. A custom reconstruction, even if successful, must not be relabelled as IODA original observations.

## Why historical DBATS custody is the primary remaining route
The CAIDA/UCSD IODA platform originally held time-series data in **DBATS / Graphite**. CAIDA's archival funding proposal for the 2021 transition discusses **migration of original IODA time series from DBATS to InfluxDB**. The public IODA service moved to Georgia Tech in August 2021.

Public technical sources:
- https://www.caida.org/funding/nea-iodamics/ — DBATS to InfluxDB migration planning, and 2021 relocation
- https://www.caida.org/projects/ioda/ — dates of stewardship
- https://github.com/CAIDA/ioda-api/wiki/API-Specification — pre-migration `/signals/{entityType}/{entityCode}` schema
- https://ioda.inetintel.cc.gatech.edu/about/ — IODA current steward and verified contact `ioda-info@cc.gatech.edu`

**Caveat:** published migration *plans* do **not** establish whether the January 2020 DBATS partitions were actually copied or deleted. Only IODA/CAIDA maintainers can verify custody and access.

## Specific archival preservation request — NOT SENT

To: `ioda-info@cc.gatech.edu`
Cc (if appropriate): CAIDA data liaison through https://www.caida.org/contact/

Subject: Academic preservation request — original January 2020 IODA BGP and active-probing data for Yemen

Dear IODA Internet Intelligence team,

We are conducting an academic study of the January 9, 2020 FALCON submarine-cable failure and its relationship to Yemen's connectivity resilience. We seek the **source-native historical numerical IODA BGP visibility and ping-slash24 time series** from 2020-01-08 00:00 to 2020-01-12 00:00 UTC for AS30873, AS12486, and country/YE, including raw counts, epoch timestamps, native cadence, any evolving IP-to-AS and prefix baselines, datasource identifiers and appropriate reuse/citation terms.

Queries of the current IODA v2 `signals/raw` API returned HTTP 200 but empty series during the requested 2020 window. The same API successfully returns original samples for later events. The 2020 `outages` event indicators are not the original BGP/ping values, and the legacy CAIDA API host could not be reached from our research runner. We also checked Internet Archive availability and CDX indexes for legacy signal endpoints without finding the desired 2020 numerical arrays.

CAIDA's publicly documented DBATS-to-InfluxDB transition raises a specific archival custody question: **Were January 2020 original IODA DBATS/Graphite series migrated to InfluxDB, and if not, are they retained in a frozen DBATS database, disk image, data export, offsite/tape backup, or research data snapshot held by CAIDA or Georgia Tech?**

If retained, would you be able to provide a source-authenticated CSV/JSON export (or restricted academic access), including collection and licensing metadata? If not retained or recoverable, we would appreciate a short dated statement of that fact, distinguishing public API availability from archival preservation. Either outcome would help the manuscript report the 2020 evidence limits correctly.

We do not intend to characterize digitized plots or independent RIPE RIS MRT datasets as original IODA samples.

Thank you for your assistance.

FALCON–Yemen Internet Resilience Research Team
Taiz University, Yemen

## Current evidence policy

Until verified source-native time series arrive: **no 2020 native measurements recovered; original-figure digitization remains a proxy; 2023 raw data cannot be transplanted; no assumption that the archives are permanently lost**. Keep custodian response (when received) and checksum of any archived export in private research provenance, then validate timestamps and signal semantics before recomputing manuscript numbers.
