#!/usr/bin/env python3
"""Aggregate original 192 source MRT SHA-256 records, rejecting gaps and double counts.

Downloads are native RIPE RIS RRC00 MRT; no original IODA 2020 is recovered.
This is an observation count/provenance table, not a complete BGP state replay.
"""
import collections,datetime as dt,hashlib,json,re
from pathlib import Path
ROOT=Path("_tmp/2020_16h_downloads")
FILES=sorted(ROOT.glob("*/audit.json"))
if len(FILES)!=8:raise SystemExit("FAIL CLOSED expected 8 valid chunk artifacts, got "+str(len(FILES)))
chunks={};items=[]
for p in FILES:
 x=json.loads(p.read_text())
 if x.get("status")!="SOURCE_ORIGINAL_MRT_SAMPLE_VALIDATED_NOT_REPLAY":raise SystemExit(f"failed {p}")
 if len(x.get("records",[]))!=24:raise SystemExit(f"not 24 intervals in {p}")
 j=int(p.parent.name.rsplit("-",1)[-1])
 if j not in range(8) or j in chunks:raise SystemExit(f"invalid duplicate chunk {j}")
 if x.get("asns",{}).get("30873",{}).get("candidate_prefixes")!=109 or x.get("asns",{}).get("12486",{}).get("candidate_prefixes")!=7:
  raise SystemExit("historical candidate prefix inventory not as expected")
 chunks[j]=x
 items+=x["records"]
if set(chunks)!=set(range(8)):raise SystemExit("missing a 2-hour segment")
by_name={}
for v in items:
 name=v["name"]
 if name in by_name:raise SystemExit("duplicate MRT file "+name)
 expected_url=f"https://data.ris.ripe.net/rrc00/2020.01/{name}"
 if v["source_url"]!=expected_url or v["gzip_crc"]!="passed" or not re.fullmatch(r"[0-9a-f]{64}",v["original_sha256"]):
  raise SystemExit("source URL/checksum/gzip validation missing for "+name)
 by_name[name]=v
if len(by_name)!=192:raise SystemExit("not precisely 192 historical source files")
expected=[f"updates.{(dt.datetime(2020,1,9,8,tzinfo=dt.timezone.utc)+dt.timedelta(minutes=5*i)):%Y%m%d.%H%M}.gz" for i in range(192)]
if set(expected)!=set(by_name):raise SystemExit("file missing, duplicate or out of period")
ordered=[by_name[x] for x in expected]
counts={a:collections.Counter() for a in ("30873","12486")}
hours=collections.defaultdict(lambda:{"30873":collections.Counter(),"12486":collections.Counter()})
for row in ordered:
 hour=row["name"].split(".")[2][:2]
 for a,d in row.get("per_asn",{}).items():
  counts[a].update(d)
  hours[hour][a].update(d)
res={
 "dataset":"RIPE RIS RRC00 source-native 2020 MRT UPDATE records; 192 consecutive files",
 "period_start_utc":"2020-01-09T08:00:00Z",
 "period_end_exclusive_utc":"2020-01-10T00:00:00Z",
 "integrity_status":"ALL_192_SOURCE_ARCHIVE_FILES_PASSED_SHA256_AND_GZIP_CRC",
 "file_count":len(ordered),
 "original_compressed_source_bytes":sum(x["size_bytes"] for x in ordered),
 "source_url_pattern":"https://data.ris.ripe.net/rrc00/2020.01/updates.YYYYMMDD.HHMM.gz",
 "original_RIB_candidate_prefix_counts":{"30873":109,"12486":7},
 "definition":{"candidate_prefix_A_target_origin":"Announcement messages whose explicitly parsed origin equals target ASN and whose prefix is in historical RRC00 candidate set",
 "candidate_prefix_W_origin_unknown":"Withdrawals matching historical candidate prefixes; no origin ASN in W; may reflect routes announced by other origins",
 "nonindependence":"Peer-prefix UPDATE messages are repeated and correlated, do not equal affected prefixes, users, or physical cable paths"},
 "summary_by_asn":{a:dict(c) for a,c in counts.items()},
 "summary_by_utc_hour":{h:{a:dict(d) for a,d in v.items()} for h,v in sorted(hours.items())},
 "highest_AS30873_candidate_announcement_bins":[{"name":x["name"],"A":x["per_asn"].get("30873",{}).get("candidate_prefix_A_target_origin",0),"W_candidate_prefix":x["per_asn"].get("30873",{}).get("candidate_prefix_W_origin_unknown",0)} for x in sorted(ordered,key=lambda q:q["per_asn"].get("30873",{}).get("candidate_prefix_A_target_origin",0),reverse=True)[:12]],
 "all_192_original_checksum_anchored_file_summaries":ordered,
 "limitation":"Complete archive file coverage for this collector/interval and candidate-prefix universe; NOT complete BGP state replay, NOT complete event monitoring across other RIS collectors, NOT 2020 IODA native reachability."
}
out=Path("results/ripe_2020_source_original_16h_aw_manifest.json");out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(res,indent=2)+"\n")
summary=Path("docs/RIPE_2020_FULL16H_SOURCE_MRT_AW_AUDIT.md")
summary.parent.mkdir(exist_ok=True)
a,b=counts["30873"],counts["12486"]
summary.write_text(f"""# Complete 16-hour original RIPE RRC00 MRT A/W file audit (26 Oct 2026)

## Audit
- The **192** original five-minute `updates` MRT files, from 2020-01-09 08:00 inclusive to 2020-01-10 00:00 UTC exclusive, were downloaded, CRC-gzip decoded and SHA-256-hashed without missing slices.
- Source and full 192-row original checksum manifest: `results/ripe_2020_source_original_16h_aw_manifest.json`.
- RIPE docs: https://ris.ripe.net/docs/mrt/
- 8 independently completed chunk source run: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40250556262

## Historical origin-filtered candidate-prefix observation counts, RRC00 only
| Measurement | AS30873 | AS12486 |
| --- | ---: | ---: |
| Candidate-origin announcement *messages* | {a.get("candidate_prefix_A_target_origin",0):,} | {b.get("candidate_prefix_A_target_origin",0):,} |
| Candidate-prefix withdrawal *messages* (origin unknown) | {a.get("candidate_prefix_W_origin_unknown",0):,} | {b.get("candidate_prefix_W_origin_unknown",0):,} |

Candidate prefix universe: 109 AS30873-origin and 7 AS12486-origin prefixes from first historical RRC00 RIB discovery only. Files were confirmed contiguous, but an archived announcement or withdrawal does NOT prove a cable-related event, outage, route withdrawal from the target AS, customer traffic change, or globally complete BGP behavior.

Messages may be repetitive, are highly dependent by peer and prefix, and are not independent samples. The 16-hour sample begins at the first 08:00 UTC RIB; per-peer route state requires replay, RIB reconciliation and validation of monitor sessions. This dataset is distinct from missing 2020 IODA raw `bgp` and `ping-slash24` measurements.

## Distinct original-MRT BGP evidence already validated
Three independent RIS RRC full-RIB collectors `rrc00`, `rrc01`, `rrc10` found the same AS30873 immediate AS_PATH neighbor transition toward AS174. See `docs/TRIPLE_COLLECTOR_RIPE_2020_VALIDATION_2026-10-26.md` for original SHA-256s and peer-verified matching methodology.

## Decision
This fills the source **collection/integrity** gap for 192 consecutive RRC00 update files, but does not yet fill the **event-time full BGP state reconstruction** or **original 2020 active probing** gaps. Do not report the UPDATE message counts as scientific estimates of cable-induced lost routes.
""",encoding="utf-8")
print("verified 192 complete 5m original-MRT updates, total bytes",res["original_compressed_source_bytes"])
print("counts",json.dumps(res["summary_by_asn"]))
print("outputs",out,summary)
