# IODA original January 2020 archive-recovery verification

**Scope:** January 8–12, 2020 UTC; AS30873 (PTC YemenNet), AS12486 (TeleYemen), and Yemen. Last verified 24 October 2026.

## Outcome

**NATIVE_BGP_AND_ACTIVE_IODA_2020_NOT_RECOVERED_FROM_TESTED_APIS.** This is a documented negative retrieval result, **not confirmation that the original 2020 measurements were deleted or are unavailable in every backup**.

## Executed tests and source evidence

1. Official current `GET https://api.ioda.inetintel.cc.gatech.edu/v2/signals/raw/asn/30873?from=1578441600&until=1578787200`: HTTP 200, no API error, but `data:[[]]`; zero native samples. Equivalently empty for AS12486 and `country/YE`, and when requesting BGP/ping specifically. Related execution: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40025032008
2. Calendar controls: the same present API returned native points for AS30873 in November 2023 (1,413 points in one diagnostic), October 2026, and January 2022 (611 points from a tested window). January 2021 was empty in that tested window. This shows API operation, but NOT the full archive start date.
3. Historical endpoints and alternate v2 paths were tested via GitHub Actions: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40026956956. CAIDA legacy hosts could not be reached from that runner (network/TLS failures); two alternate v2 outage paths returned HTTP 404. These results do not establish the legacy databases were deleted.
4. `/v2/signals/events/asn/30873` did yield ~386 values for 2020. A separate forensic raw download found these values are **`datasource: outages`** event indicators, mostly zeros; they are NOT `bgp` visibility, `ping-slash24` active reachability, or traffic measurements. Therefore they do not recover the original time series. Raw endpoint remains empty. Source: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40032653939
5. This distinction corrected a temporary false-positive flag in `tools/test_historical_ioda_endpoints.py` (commit `4e1dabc9766587acdab96c9f93420b84080792e9`).

## Historical custody / next route

IODA was developed at CAIDA (UC San Diego). CAIDA states the operational service moved to Georgia Tech in August 2021: https://www.caida.org/projects/ioda/

Georgia Tech IODA lists `ioda-info@cc.gatech.edu` for research inquiries (https://ioda.inetintel.cc.gatech.edu/about/) and its Markup Studio documentation describes a dashboard CSV download method (https://ioda.inetintel.cc.gatech.edu/reports/ioda-markup/). CAIDA's data contact list is `data-info@caida.org` (https://mailman.caida.org/mailman/listinfo/data-info).

**The research team should request in writing:** Jan 8–12 2020 unnormalized `bgp` and `ping-slash24` per-AS and country time series, timestamps, sample cadence, collection/vantage metadata, original signal identifiers, licence and authorized use, whether data were migrated, and either archive access or an explicit archival-availability statement. No maintainer confirmation has been received through this project.

## Publication language allowed

> As of 24 October 2026, attempts to retrieve IODA numerical BGP visibility and active-probing measurements for 8–12 January 2020 through the tested public API endpoints returned empty data. Legacy CAIDA endpoints could not be verified from the cloud runner. A distinct IODA outage-event indicator remains available but is not a substitute for source-specific measurements. Therefore the January 2020 estimates in this study remain plot-digitized descriptive proxies; they are not independent estimates from recovered IODA native samples.

**Prohibited overclaims:** "IODA data permanently deleted", "all archives exhausted", "2020 data successfully recovered" (from outage events), "2022/2023 data substantiate original 2020 numbers", and any causal inference from the lack of records.

## Next action

Obtain explicit archival answer from IODA/CAIDA stewards and preserve correspondence in the private research records. The automated retrieval checks are complete; the archival-custodian response is the remaining external dependency.
