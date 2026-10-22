# FALCON–Yemen Internet Resilience Research

**Private research workspace (not final peer-reviewed findings).**

مشروع بحثي خاص لتحليل آثار انقطاع كابل FALCON على الاتصال بالإنترنت في اليمن. يحتوي على المخطوطة الحالية، البيانات **المشتقة من الرسوم المنشورة**، الشيفرة، اختبارات الحماية، وعمليات تشغيل تلقائية عبر **GitHub Actions** دون الحاجة إلى PowerShell على جهاز الباحث.

## شغّل المشروع من GitHub

1. افتح تبويب **Actions** داخل المستودع الخاص، وفعّل تشغيل الـ workflows إذا طُلب ذلك.
2. لاختبار الأكواد وإعادة إنتاج النتائج المتاحة: افتح **Reproduce and Test**؛ ويعمل تلقائيًا عند أول رفع إلى الفرع الرئيسي، ويمكن تشغيله يدويًا.
3. لطلب القياسات الرقمية الأصلية: اختر **Acquire Native IODA** → **Run workflow** → `FALCON_2020`.
4. لاستخراج قائمة **مرشحة فقط** للبادئات التاريخية: اختر **Historical BGP Discovery** → **Run workflow** وحدد ASN/collector.
5. نزّل ملفات التشغيل من **Artifacts** في نهاية كل عمل؛ الأكواد **لا تضع بيانات غير مدققة داخل الورقة** ولا تحفظ النتائج الأصلية تلقائيًا في Git.

## Evidence status / حالة الأدلة

| Component | Evidence status |
|---|---|
| Jan 2020 structural–functional gap (around 50.8 pp) | `DERIVED_FROM_PUBLISHED_PLOT` only |
| Plot sensitivity grid (20,250 configurations) | Reproduced from saved derived table, not independent trials |
| Phase-specific comparison | Reproduced from the included digitized evidence |
| 2026 BGP-origin HHI | Computed from selected frozen **2026** origin-prefix snapshot, not 2020 |
| Native IODA Jan 2020 | **Not yet verified** |
| Historical BGP RIB/updates & route-level effects | **Not yet validated** |
| Multilayer cascade / ML performance | **Not measured** |

## Layout

- `paper/`: revised and original manuscript, cover letter, Arabic revision report (keep repository **private**)
- `code/`: reproducible scripts and guarded analysis
- `tests/`: guardrails for withdrawals, origin changes and invalid data
- `data/`: included frozen/derived research inputs (no original IODA samples)
- `results/`, `figures/`: derived/reproduced outputs and figures
- `provenance/`: source-data redistribution boundaries
- `docs/`: execution details and limitations
- `archive/legacy/`: **unsafe earlier historical extractor, not executed**
- `.github/workflows/`: cloud workflows for GitHub Actions

## Scientific safeguard

A successful GitHub Actions job only means that the specific script executed. **It does not prove** that the external API returned complete valid data or that a peer-observed BGP change was physically caused by the cable failure. Check source manifests, collector coverage, peer continuity and timestamps before updating the manuscript.

No Elsevier/Scopus API key is required. Never paste credentials into scripts, commits or logs. The GitHub repository should remain private until the authors approve public release and third-party data licensing.

Official documentation: [IODA API](https://api.ioda.inetintel.cc.gatech.edu/v2/) · [RIPE RIS MRT](https://ris.ripe.net/docs/mrt/) · [CAIDA BGPStream](https://bgpstream.caida.org/docs/tutorials/docker).

## One-click cloud run / تشغيل شامل بزر واحد

From the private repository select **Actions → Full Research Pipeline → Run workflow**. The default is `FALCON_2020`, with optional BGP candidate discovery for AS30873 and AS12486 on `rrc00`.

This triggers three **independent** GitHub-hosted jobs: reproducibility checks, native IODA acquisition with a validation manifest, and historical BGP prefix *discovery*. Individual jobs may fail when archives are unavailable; their Artifacts remain available for audit. None of these jobs fabricates results, publishes data, or certifies cross-layer causal inferences.
