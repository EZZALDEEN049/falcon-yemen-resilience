# January 2020 IODA published-original image reproducibility closure — 28 October 2026

The original publisher-linked 1840 × 874 PNGs were retrieved with unchanged source URLs and recorded hashes:

| Caption AS | Original publisher image URL | SHA-256 |
| --- | --- | --- |
| AS30873 | https://internetdisruption.report/wp-content/uploads/2020/02/jan-910-yemen-as30783-ioda.png | 229b9ed3e0e169c78331b7e50f0a2af9f47f88c3d0b73d0524db633d14977efd |
| AS12486 | https://internetdisruption.report/wp-content/uploads/2020/02/jan-910-yemen-as12486-ioda.png | fb4be5c7d169a659a1b7f5c207eb56c5390d20faaf60705dc0d34610466a612c |

The AS30873 chart label was directly inspected and read **AS30873**, although its publisher URL spells `as30783`.

Independently repeated exact RGB extraction (BGP 51/160/44, active 31/120/180; tolerance ±2), pixel x 112–1779, zero Y 632 and 252 pixels per normalized unit reproduced baseline/acute values in the author's prior source-raster analysis:
- AS30873 BGP median retention 95.652173913%, active 44.837758112%, gap **+50.814415801 percentage points**.
- AS12486 BGP and active median retentions 100% each, gap **0 percentage points**.
- Re-running the prior 20,250-setting sensitivity script directly on the unchanged downloaded AS30873 image produced an **exact byte-for-byte SHA256-identical CSV** to the archive: `fa9720246ec52edb6770c8637f52da260856908574fb490a4d49f0e825245e12`. Range +45.8074 to +55.1698 pp.

Original source article: https://internetdisruption.report/2020/02/23/internet-disruption-report-january-2020/

Initial provider retrieval/geometry evidence is in [source_raster_audit.json](../results/ioda2020_source_audit/source_raster_audit.json), and the fetch/geometry gate script in [audit_ioda2020_source_rasters.py](../tools/audit_ioda2020_source_rasters.py). Downloaded copies of publisher-owned PNGs have not been committed to this repository; only the source URLs and verified SHA-256 values are stored.

**Scientific classification:** original publisher *raster* provenance verified; *raster-derived numerical calculations* independently re-executed; raw 2020 IODA provider numerical time-series NOT recovered; analyst settings are NOT independent experiments or confidence intervals; BGP and active measures have different semantics and denominators; no affected-user or cable-causality fraction can be inferred.

The raster reproducibility reviewer objection can be **closed**, while original 2020 IODA numeric data remain an explicit unfulfilled high-grade evidence source.