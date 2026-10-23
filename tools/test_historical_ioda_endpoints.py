#!/usr/bin/env python3
"""Bounded, auditable checks of documented IODA historical and legacy endpoints.

An empty API response, blocked host, or API failure is NEVER interpreted as
proof of permanent archival loss. All remote measurements are kept separate
from published-figure digitization and BGP archive reconstructions.
"""
import concurrent.futures
import datetime as dt
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

def ep(s):
    return int(dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp())

T0,T1=ep("2020-01-08T00:00:00Z"),ep("2020-01-12T00:00:00Z")
J0,J1=ep("2020-01-30T00:00:00Z"),ep("2020-01-31T00:00:00Z")
R0,R1=ep("2021-01-08T00:00:00Z"),ep("2021-01-12T00:00:00Z")
S0,S1=ep("2022-01-08T00:00:00Z"),ep("2022-01-12T00:00:00Z")
BASE="https://api.ioda.inetintel.cc.gatech.edu/v2"
Q=lambda x,y: urllib.parse.urlencode({"from":x,"until":y})
TARGETS=[
 ("v2_signal_2020_AS30873",f"{BASE}/signals/raw/asn/30873?{Q(T0,T1)}"),
 ("v2_signal_2020_YE",f"{BASE}/signals/raw/country/YE?{Q(T0,T1)}"),
 ("v2_signal_Jan30_2020_AS30873",f"{BASE}/signals/raw/asn/30873?{Q(J0,J1)}"),
 ("v2_signal_Jan2021_AS30873",f"{BASE}/signals/raw/asn/30873?{Q(R0,R1)}"),
 ("v2_signal_Jan2022_AS30873",f"{BASE}/signals/raw/asn/30873?{Q(S0,S1)}"),
 ("v2_event_signals_2020_AS30873",f"{BASE}/signals/events/asn/30873?{Q(T0,T1)}"),
 ("v2_outage_events_2020_AS30873",f"{BASE}/outages/events/asn/30873?{Q(T0,T1)}"),
 ("v2_outage_alerts_2020_AS30873",f"{BASE}/outages/alerts/asn/30873?{Q(T0,T1)}"),
 ("legacy_api_caida_dev_2020",f"https://api.ioda.caida.org/dev/signals/asn/30873?{Q(T0,T1)}"),
 ("legacy_api_caida_2020",f"https://api.ioda.caida.org/signals/asn/30873?{Q(T0,T1)}"),
 ("legacy_ioda_caida_events_2020",f"https://ioda.caida.org/ioda/data/events?{Q(T0,T1)}&meta=asn"),
 ("legacy_ioda_caida_metadata", "https://ioda.caida.org/metadata/lookup/country/YE"),
]

def num_series(obj):
    if isinstance(obj,dict):
        vals=obj.get("values")
        if isinstance(vals,list) and ("datasource" in obj or "signal" in obj):
            return sum(isinstance(v,(int,float)) and not isinstance(v,bool) for v in vals)
        return sum(num_series(v) for key,v in obj.items() if key in ("data","series","results","signals"))
    if isinstance(obj,list):
        return sum(num_series(x) for x in obj)
    return 0

def fetch(entry):
    name,url=entry
    result={"label":name,"request_url":url,"tested_at":dt.datetime.now(dt.timezone.utc).isoformat(),
            "status":"NOT_YET_CLASSIFIED","numeric_native_samples":0}
    try:
        request=urllib.request.Request(url,headers={"User-Agent":"FALCON-research-historical-data-audit/1.0",
                       "Accept":"application/json"})
        with urllib.request.urlopen(request,timeout=12) as r:
            content=r.read(1_200_001)
            result.update(http_status=r.status,final_url=r.url,content_type=r.headers.get("content-type",""))
        if len(content)>1_200_000:
            result["status"]="RESPONSE_EXCEEDS_BOUND";return result
        result["response_sha256"]=hashlib.sha256(content).hexdigest()
        result["response_bytes"]=len(content)
        try:
            data=json.loads(content)
        except (ValueError,UnicodeError):
            result["status"]="NOT_JSON";result["body_prefix"]=content[:180].decode("utf-8","replace")
            return result
        if isinstance(data,dict) and data.get("error"):
            result["status"]="API_ERROR_ENVELOPE";result["api_error"]=str(data["error"])[:220]
        else:
            result["numeric_native_samples"]=num_series(data)
            if result["numeric_native_samples"]:
                result["status"]="SIGNALS_PRESENT_REQUIRE_VALIDATION"
            elif isinstance(data,dict) and data.get("data")==[[]]:
                result["status"]="EMPTY_DATA_ENVELOPE"
            elif isinstance(data,(dict,list)):
                result["status"]="VALID_JSON_NO_VALIDATED_SAMPLES"
            else:
                result["status"]="UNEXPECTED_RESPONSE"
            if isinstance(data,dict):
                result["data_type"]=type(data.get("data")).__name__
                result["data_keys"]=list(data.keys())[:12]
                if isinstance(data.get("data"),list):
                    result["data_length"]=len(data["data"])
    except urllib.error.HTTPError as e:
        result.update(status="HTTP_ERROR",http_status=e.code,error=str(e)[:240])
    except (urllib.error.URLError,TimeoutError,ValueError) as e:
        result.update(status="NETWORK_OR_TLS_ERROR",error=f"{type(e).__name__}: {str(e)[:240]}")
    return result

def main():
    out=Path("_artifacts/ioda_2020_legacy_diagnostic")
    out.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        result=list(pool.map(fetch,TARGETS))
    report={
      "scope":"Historical IODA January 2020 original-source archive discovery",
      "conclusion":"Outage event-series samples are event indicators, not original bgp or ping-slash24 raw samples. Their nonempty values cannot satisfy native signal recovery. Inaccessible endpoints do not prove global data loss.",
      "original_2020_recovered": any(r["numeric_native_samples"]>0 and r["label"] in ("v2_signal_2020_AS30873","v2_signal_2020_YE") and r["status"]=="SIGNALS_PRESENT_REQUIRE_VALIDATION" for r in result),
      "tested_urls":result,
      "sources":[
         "https://www.caida.org/projects/ioda/",
         "https://github.com/CAIDA/ioda-api/wiki/API-Specification",
         "https://api.ioda.inetintel.cc.gatech.edu/v2/",
         "https://ioda.inetintel.cc.gatech.edu/reports/ioda-markup/"
      ]
    }
    (out/"legacy_endpoint_test_results.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps({"original_2020_recovered":report["original_2020_recovered"],
        "cases":[{"label":r["label"],"status":r["status"],"code":r.get("http_status"),"samples":r["numeric_native_samples"]} for r in result]},indent=2))
    # A failed archaeological query is a documented result, not job failure.
if __name__=="__main__":
    main()
