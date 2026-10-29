# FALCON — Yemen Internet Routing Measurements and Reproducibility

**Status (29 October 2026):** Public research workspace containing a **pre-submission empirical measurement study** and a source-auditable reviewer package. The manuscript has **not been submitted to, accepted by, or published in** *Scientific Reports* (Nature Portfolio / Springer Nature). External journal review, bibliographic validation, author sign-off, and third-party rights clearance remain outstanding. **Do not treat this entire repository or the historical reviewer ZIP as cleared for redistribution or Zenodo archiving.**

## Study

**Manuscript title:** *Network-Specific BGP Route Reconfiguration During Yemen's January 2020 FALCON Disruption: A Multi-Collector Measurement Study*.

The study characterizes origin-adjacent BGP AS_PATH reconfiguration observed for **AS30873** and **AS12486** across RIPE RIS **RRC00, RRC01, and RRC10**. The principal event comparison uses the **9 January 2020, 08:00 UTC** and **10 January 2020, 00:00 UTC** MRT routing-table checkpoints (16 hours). A retrospectively selected, earlier 16-hour reference uses **2 January 2020, 08:00 UTC** and **3 January 2020, 00:00 UTC**. The reference dates were fixed before inspecting the **reference-window outcomes**, but **not preregistered prospectively** before the cable incident or the original event analysis.

Source-derived original-RIB exports cover **11,419 first-snapshot peer–prefix observations in the event window** and **10,968 in the reference window**. Among the *retained, comparable origin-adjacent AS_PATH observations* for AS30873, the reported event-window changed-neighbor shares are **66.83% / 67.98% / 64.73%** (RRC00 / RRC01 / RRC10), compared with **0.48% / 0.90% / 0.41%** in the single reference window. A sensitivity comparison using identical comparable (peer ASN, peer IP, prefix) keys retains the descriptive contrast. This evidence does **not** estimate typical churn across many reference periods, a statistical confidence interval, customer connectivity, or a causal cable-to-AS route mapping.

For AS12486, original event IPv6 origin-route observations present on eligible peers at the first checkpoint were **0/54**, **0/24**, and **0/13** retained under the same-origin endpoint criterion (RRC00/01/10), whereas corresponding reference-window observations were **54/54**, **23/23**, and **13/13**. Its published adjacent-neighbor-change percentages therefore describe *effectively retained IPv4 routes*; lack of endpoint origin visibility is **not proof** of a withdrawal or user-level IPv6 outage.

## Evidence types and boundaries

| Evidence source | Provenance | Appropriate interpretation |
|---|---|---|
| RIPE RIS January 2020 MRT RIB archives | Official 12 source URLs, source-byte SHA-256 and checksum-documented extraction manifests | Two-checkpoint BGP routing observations; not continuous UPDATE replay or physical cable path |
| January 2020 IODA | Two source-publisher raster images, preserved origin URLs and SHA-256; derived pixel calibration and deterministic sensitivity outputs | **Secondary image-digitized proxies, not provider-original numerical 2020 time series** |
| November 2023 IODA | Archived provider-native JSON for a separate incident | Distinct interpretive event, not a January 2020 control |
| RIPE Atlas / contextual figures | Limited published/aggregated sources with explicit scope constraints | Context only, not evidence of a complete independent 2020 active-probe series |
| 2026 origin-prefix context | Contemporary selected snapshots | **Not** retrospective observations from 2020 |

The original publisher PNG image bytes are not licensed for blanket reuse by this repository. Public data access does not by itself mean permission to redistribute or sublicense source data. See [data rights and provenance](DATA_LICENSES_AND_PROVENANCE.md) and the [public-release audit](PUBLIC_RELEASE_AUDIT_2026-10-29.md).

## Frozen 29 October 2026 reviewer package

The authoritative **reviewer** bundle is preserved at:

`releases/FALCON-v1.0-2026-10-29-reviewer/`

This directory contains:

- `Manuscript/FALCON_Final_Editorial_Revision_2026-10-29.docx` and `.pdf`;
- `Supplement/Online_Resource_1_FALCON_Final_2026-10-29.docx` and `.pdf`, Tables **S1–S15**;
- `Code/` source and reproducibility scripts, `Evidence/` derived data and documented source provenance, `Figures/`, and `QA/`;
- **internal** `Review/` and `Historical_Superseded/` material, which must **not** be assumed appropriate for Zenodo public deposit.

The GitHub **prerelease** `FALCON-v1.0-2026-10-29` is a historic internal reviewer snapshot; it is **not** the target `v1.0.0` publication draft. The latter is to remain unpublished until the rights, confidentiality and metadata release gates are satisfied.

## Reproduce the published descriptive calculations

Use Python **3.10+** and run the following from the repository root (or change into the extracted reviewer package root first):

```bash
cd releases/FALCON-v1.0-2026-10-29-reviewer
python Code/verify_reviewer_bundle.py
python Code/compare_2020_event_vs_non_event.py --event-root Evidence/BGP_2020 --reference-root Evidence/Reference_2020_20200102 --output-dir /tmp/falcon-reference-check
python Code/reproduce_native_ioda_2023_v2.py --source-zip Supplement/IODA_2023_Original_JSON_SourceArtifact.zip --out /tmp/falcon-ioda2023.csv
python Code/rebuild_2020_peer_prefix.py --self-test
```

These programs reaggregate **archived exported records**, compare the two windows, reproduce 2023 source-JSON-derived values and exercise a synthetic parser test. They do **not** independently download and reparse all 12 original MRT files, replay all RRC UPDATE archives, retrieve unavailable provider-native 2020 IODA numeric observations, or prove causal cable effects. For independently fetching original data, see `Code/REPRODUCE.md` and the pinned RIPE RIS source manifests. Some full original-source operations require additional third-party tools and substantial network access.

## Release and licensing controls

- **No repository-wide open license is currently granted**. Code, author-created tabulations, publisher-origin material, and internal review documents have different rights.
- Scientific provenance and source quotations must be attributed; publisher imagery and source-redistribution rights are subject to separate review.
- Do **not** include internal referee reports, obsolete editorial files, private correspondence, secrets or unknown-rights binaries in a public archival release.
- Zenodo archives the released repository snapshot. The **`v1.0.0` draft must not be published** before a clean public file-inventory/rights review, final author approval and a final pinned commit.
- The target journal is *Scientific Reports*; no journal submission, endorsement or acceptance is implied.

**Researcher:** Ezzaldeen Al-Tayar · Faculty of Engineering and Information Technology, Taiz University, Taiz, Yemen.

Source portals: [RIPE RIS](https://data.ris.ripe.net/) · [IODA](https://ioda.inetintel.cc.gatech.edu/) · [Zenodo GitHub archiving](https://help.zenodo.org/docs/github/archive-software/github-upload/).
