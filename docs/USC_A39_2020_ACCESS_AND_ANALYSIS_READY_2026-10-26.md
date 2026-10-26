# USC/ISI ANT Trinocular A39 January 2020 acquisition / analysis gate

**Review date:** 2026-10-26. **CUSTODY: ACCESS NOT GRANTED / SOURCE MEASUREMENTS NOT DOWNLOADED**. This dossier is not a substitute for real observations. No email/portal application was submitted by the assistant.

## Original 2020 source identifiers and verified public readmes

1. **Priority:** `internet_outage_adaptive_a39all-20200101`, 2020-01-01 to 2020-04-01, approximately **2.13 GB** combined quarterly dataset of /24-level active reachability from 6 observer sites. Public README version 11071, modified 2020-04-22; original public README SHA-256 `0167920ba5f7d2d6454d874fbd3e990dcf907b76f4dc2869814a60950b39d670`. Within authorized delivery locate **`a39all.{version}.outagedownup.fsdb.bz2`**, or equivalent **`.xz`** as listed for some variants. The README also identifies `a39all.{version}.outages.fsdb.bz2` as a secondary less-processed multi-VP representation.
2. **Required:** `internet_outage_adaptive_a39_supplement-20200101`, 2020-01-01, approximately **165 MB**. Public README version 11475, modified 2021-01-27; original public README SHA-256 `e647320ef62227e5dd7fc2cdf5fa1cc2de545230e99abacb19a58e052e5e2ef6`. Within authorized delivery locate **`block_to_as.fsdb.bz2`** (mapping made at January 1, 2020). USC README schema: `#fsdb -F t block IP AS ASname`.
3. The a39all outagedownup schema is `#fsdb -F t block start duration uncertainty downup`: `block` 8-hex-digit /24 base, seconds from Unix epoch, duration seconds, uncertainty seconds; status up `1`, down `0`, unmeasurable `-1`, gone-dark `-2`. Unlike raw probe packets, `outagedownup` is USC's best **postprocessed combined-site** estimate. This is independent active reachability, **not** the missing IODA 2020 `ping-slash24` signal, not raw single-vantage ICMP packet traces.
4. Requested analysis scope **Jan 8–12 2020 UTC** (inclusive beginning / exclusive ending); **AS30873 and AS12486** at historically mapped /24 level, 15-minute checkpoints, with unmeasurable/gone-dark/unknown/uncertain as separate categories. For national `YE` conclusions request an independent IP geolocation reference if permitted; USC explicitly warns that MaxMind geolocation cannot be redistributed. Do **not** infer country of IP block from AS geography or `block_to_org_caida` company-country field.
5. A defensible source-specific output is a time series of measured-up, measured-down and unmeasurable /24 prefixes for each historical ASN plus bounds on retained baseline-up /24s. This **cannot be numerically equated** to IODA's `ping-slash24` denominator, and is NOT evidence of a specific physical FALCON cable path.

## Source verification
- USC dataset catalog: https://ant.isi.edu/datasets/all.html
- Source-specific README A39 all: https://ant.isi.edu/datasets/readmes/internet_outage_adaptive_a39all-20200101.README.txt
- Source-specific README supplement: https://ant.isi.edu/datasets/readmes/internet_outage_adaptive_a39_supplement-20200101.README.txt
- Official status data schema: https://ant.isi.edu/datasets/outage/format.html
- Official request requirements: https://ant.isi.edu/datasets/requests.html
- COMUNDA: https://comunda.isi.edu/
- USC backup request form: https://ant.isi.edu/datasets/request/
- Official owner contact: https://ant.isi.edu/~johnh/CONTACT/ (johnh@isi.edu)
- Public metadata verification code `tools/usc_a39_public_metadata_probe.py`, run https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40317987790 .

## Verified tool readiness, synthetic only
- `tools/usc_2020_trinocular_a39_reachability.py` reads authorized bzip2/xz FSDB files, matches 2020 per-AS /24 block IDs, excludes ambiguous/missing mappings, and never converts unmeasurable/gone-dark into down. Relative baseline default Jan 9 08:00 UTC.
- `tools/test_usc_2020_trinocular_a39.py`: five synthetic tests passed after strict zero-uncertainty boundary correction. Run: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40318591465 .
- The synthetic tests demonstrate parser mechanics **only**. They do NOT contain original USC observations and cannot validate representativeness, VP consistency, real-data event timings, or 2020 measurement coverage.
- **Fail-closed** script requires approved original dataset files and refuses to output data without them. After approval, record original file SHA-256 and exact internal dataset version, then run, inspect coverage and uncertainty and compare with RIPE only at compatible UTC timestamps.

### Command after duly authorized dataset transfer (not executable on unavailable datasets)
```bash
python tools/usc_2020_trinocular_a39_reachability.py \
  --downup /authorized/a39all.vXX.outagedownup.fsdb.bz2 \
  --block-to-as /authorized/block_to_as.fsdb.bz2 \
  --from-utc 2020-01-08T00:00:00Z --until-utc 2020-01-12T00:00:00Z \
  --baseline-utc 2020-01-09T08:00:00Z --step-minutes 15 \
  --output _artifacts/approved_usc_2020/asn24_active_reachability.json
```

## Access request content (never sent)
**Requested via USC/ISI COMUNDA** (rather than IMPACT, whose official country list is restricted):
- Institution: Taiz University, Yemen, **subject to author confirmation of the affiliation shown in final author list**.
- Project: Structural–Functional Divergence During Submarine-Cable Disruptions: Evidence from Yemen's FALCON Dependence.
- Data requested: `internet_outage_adaptive_a39all-20200101` and `internet_outage_adaptive_a39_supplement-20200101` or a provider-prepared **Jan 8–12, 2020 UTC** filtered export for YE historical /24 prefixes and AS30873, AS12486 that preserves timestamp, duration, uncertainty, `downup` and January-2020 block-AS membership.
- Purpose: independent active-probing validation of coverage/loss during FALCON outage, cross-checking native historical RIPE RIS 2020 BGP data to assess structural versus functional divergence, without equating measurement systems.
- Requested conditions: scholarly non-commercial research, original provenance/version, source timestamps, licensing permitted statistics/figures, DUA completion by researcher.
- USC requires a signed data use agreement, institutional email contact and provider approval. **User must personally sign and authorize**; assistant did not contact, submit, register or download restricted content.

## Current sign-off
- **Done:** exact original source dataset discovery, public README/source schema provenance, analysis code and passing synthetic QA, provider-compliant request prepared.
- **NOT done:** user-authorized access application/DUA, USC raw/processed source file reception, 2020 actual independent ping values, validation of AS30873/AS12486 measurement coverage, manuscript numeric conclusions from USC.

**Do not mark USC 2020 original active probing completed until genuine files are received and audited.**
