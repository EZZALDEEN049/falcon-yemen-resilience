# Completed one-week-prior 16-hour RIS RIB reference-window test

**Result gate: COMPLETE and source-audited (28 October 2026).** This supersedes the earlier provisional note that extraction had not completed.

The 2 January 2020 08:00 UTC → 3 January 2020 00:00 UTC window was chosen and its source-extractor script committed **before its results were inspected**. Six original reference RIBs from RRC00, RRC01 and RRC10 were downloaded from RIPE RIS, each gzip CRC-validated and SHA-256 recorded in `Supplement/Reference_And_Event_Original_RIB_12_SHA256.json`. The same peer-presence, target-origin, retention and immediate-AS_PATH adjacency parser was used for January 9–10 event RIBs.

Source artifact run: https://github.com/EZZALDEEN049/falcon-yemen-resilience/actions/runs/40609642587

Frozen reference result commit: https://github.com/EZZALDEEN049/falcon-yemen-resilience/commit/e7d0f51729ef8fffe138fa7fc34a3130455e1ad2

Source code, pre-outcome definition: https://github.com/EZZALDEEN049/falcon-yemen-resilience/blob/55c02029f7fc0e41c94655a2f131adbac4f2df2a/tools/ripe2020_non_event_20200102_20200103.py

Original event data: https://github.com/EZZALDEEN049/falcon-yemen-resilience/commit/907b59027807ab292d33886d36e65e2bb07f63c6

**Primary six fractions:** AS30873 event 66.83%, 67.98%, 64.73%, reference 0.48%, 0.90%, 0.41%; AS12486 event 6.28%, 4.05%, 14.10%, reference 0.00% in all three collectors.

This is a single historical comparison, not a representative sample of ordinary BGP churn or direct identification of a specific physical cable, end-user reachability or causal fault attribution. The separate conditions and unequal prefix sets still apply. See Tables S14–S15 and Figure S4.
