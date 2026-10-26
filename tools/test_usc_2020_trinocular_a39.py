#!/usr/bin/env python3
"""Synthetic-only tests: never label synthetic observations as USC 2020 evidence."""
import bz2,importlib.util,json,tempfile,unittest
from pathlib import Path
from datetime import datetime,timezone
PATH=Path(__file__).with_name("usc_2020_trinocular_a39_reachability.py")
spec=importlib.util.spec_from_file_location("usc_analysis",PATH)
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)

class SourceSchemaTest(unittest.TestCase):
 def test_exact_2020_as_mapping_and_status(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   mapping=root/"block_to_as.fsdb.bz2"
   rows=[
      "#fsdb -F t block IP AS ASname",
      "01020300\t1.2.3.0\t30873\tNetwork A",
      "01020400\t1.2.4.0\tAS30873\tNetwork B",
      "02030400\t2.3.4.0\t12486\tNetwork C",
      "02030500\t2.3.5.0\t12486\tNetwork D",
      "02030600\t2.3.6.0\t30873,12486\tAMBIGUOUS",
   ]
   with bz2.open(mapping,"wt") as f:f.write("\n".join(rows)+"\n")
   data=root/"a39all.v1.outagedownup.fsdb.bz2"
   start=a.ep("2020-01-08T00:00:00Z")
   mid=a.ep("2020-01-09T17:00:00Z")
   midend=a.ep("2020-01-09T22:00:00Z")
   end=a.ep("2020-01-12T00:00:00Z")
   drows=["#fsdb -F t block start duration uncertainty downup"]
   drows.append(f"01020300\t{start}\t{mid-start}\t0\t1")
   drows.append(f"01020300\t{mid}\t{midend-mid}\t0\t0")
   drows.append(f"01020300\t{midend}\t{end-midend}\t0\t1")
   drows.append(f"01020400\t{start}\t{end-start}\t0\t1")
   drows.append(f"02030400\t{start}\t{end-start}\t0\t1")
   drows.append(f"02030500\t{start}\t{mid-start}\t0\t1")
   drows.append(f"02030500\t{mid}\t{midend-mid}\t0\t-1")
   drows.append(f"02030500\t{midend}\t{end-midend}\t0\t1")
   with bz2.open(data,"wt") as f:f.write("\n".join(drows)+"\n")
   output=a.analyze(data,mapping,a.ep("2020-01-09T08:00:00Z"),a.ep("2020-01-10T00:15:00Z"),15,a.ep("2020-01-09T08:00:00Z"))
   self.assertEqual(output["mapped_asn_candidate_prefix_counts"],{"30873":2,"12486":2})
   self.assertEqual(output["mapping_audit"]["ambiguous_block_mappings"],1)
   by_t={r["timestamp_utc"]:r["asns"] for r in output["series"]}
   pre=by_t["2020-01-09T08:00:00Z"]
   self.assertEqual(pre["30873"]["observed_status_counts"]["up"],2)
   event=by_t["2020-01-09T18:00:00Z"]
   self.assertEqual(event["30873"]["observed_status_counts"]["down"],1)
   self.assertEqual(event["30873"]["baseline_up_currently_up_lower_bound"],0.5)
   self.assertEqual(event["12486"]["observed_status_counts"]["unmeasurable"],1)
   self.assertEqual(event["12486"]["observed_status_counts"]["down"],0)
   self.assertEqual(event["12486"]["baseline_up_currently_up_upper_bound_if_unknown_assumed_up"],1)
   rec=by_t["2020-01-10T00:00:00Z"]
   self.assertEqual(rec["30873"]["observed_status_counts"]["up"],2)
 def test_uncertainty_indeterminate(self):
  t=1000
  self.assertEqual(a.one_status([(t,t+100,20,0)],t+5),"uncertain")
  self.assertEqual(a.one_status([(t,t+100,20,0)],t+50),"down")
  self.assertEqual(a.one_status([(t,t+100,0,0)],t),"down")
 def test_overlaps_not_double_counted(self):
  self.assertEqual(a.one_status([(100,200,0,1),(150,250,0,0)],170),"uncertain")
 def test_strict_asn_and_prefix(self):
  self.assertIsNone(a.norm_asn("30873,12486"))
  self.assertEqual(a.norm_asn("AS12486"),12486)
  with self.assertRaises(ValueError):a.norm_block("01020308")
 def test_status_has_no_data(self):
  self.assertEqual(a.one_status([],123456),"no_data")

if __name__=="__main__":unittest.main(verbosity=2)
