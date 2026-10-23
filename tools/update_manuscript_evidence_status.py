#!/usr/bin/env python3
"""Step 1: precise non-numerical scientific evidence-status update only."""
from docx import Document
from pathlib import Path
source=Path("paper/Manuscript_Revised_Evidence_Bounded.docx")
target=Path("paper/Manuscript_2026-10-24_Evidence_Status_Updated.docx")
doc=Document(source)
original=[p.text for p in doc.paragraphs]
patches={
 6:[("Native historical IODA samples and matched-vantage MRT/BGPStream reconstructions were not available for this analysis;",
     "Native January 2020 IODA samples and complete matched-vantage MRT/BGPStream reconstructions remain unavailable for this analysis;")],
 50:[("The official IODA HTTP API supports raw time-series retrieval, but an attempt to retrieve the necessary 2020 series from this execution environment failed at the network/DNS stage. The failure is not treated as evidence that IODA lacks the data; native samples remain the priority for future inference.",
      "Later GitHub Actions tests of the official IODA v2 raw endpoint returned HTTP 200 with an empty data envelope for 8–12 January 2020 for AS30873, AS12486, and Yemen; BGP- and active-probing-specific requests also provided no original samples. Attempts to verify legacy CAIDA endpoints from the cloud runner failed at the network/TLS stage. These results establish non-retrieval from the tested interfaces, not permanent absence from every archive. Native IODA data for November 2023 were retrieved in a separate subsequent workflow and have not been substituted for the 2020 plot-derived measurements in this manuscript.")],
 127:[("A prior RIPEstat checkpoint bundle contained empty route states; a subsequent check could not access MRT/BGPStream archives from the available execution environment. Neither retrieval failure is interpreted as zero routes.",
       "A prior RIPEstat checkpoint bundle contained empty route states. Later exploratory RIPE RIS collection retrieved candidate January 2020 origin observations (109 candidate prefixes for AS30873 and 7 for AS12486 in the selected rrc00 query), but the downloader also logged HTTP transfer errors, preventing any claim of complete event-time inventory or validated route-state reconstruction. These acquisition limitations are not interpreted as zero routes.")],
 133:[("Four offline guardrail tests passed, but no native IODA or event-time BGP measurements were obtained here, and no new historical network metrics are claimed.",
       "Automated code guardrails and derived-evidence reproduction tests have passed; however, native January 2020 IODA measurements have not been recovered from the tested APIs, and no complete, validated event-time BGP replay has been released. Native November 2023 IODA measurements were subsequently retrieved and analyzed in the research repository, but the resulting numerical analysis has not yet been incorporated into this manuscript. No route-level metrics are claimed.")]
}
for idx,items in patches.items():
    p=doc.paragraphs[idx]
    assert len(p.runs)==1, ("Expected single run in paragraph",idx)
    text=p.runs[0].text
    for old,new in items:
        assert text.count(old)==1,(idx,old[:70])
        text=text.replace(old,new)
    p.runs[0].text=text
assert len(doc.tables)==6
assert len(doc.paragraphs)==188
assert [i for i,p in enumerate(doc.paragraphs) if p.text!=original[i]] == [6,50,127,133]
target.parent.mkdir(exist_ok=True)
doc.save(target)
print("New version:",target,"(only paragraphs 6, 50, 127 and 133 updated)")
