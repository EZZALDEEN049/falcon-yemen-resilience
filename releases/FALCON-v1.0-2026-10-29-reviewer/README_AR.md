# FALCON — حزمة التحكيم المنقحة 29 أكتوبر 2026 (إصلاحات E1–E4)

**نوع الإصدار:** حزمة إعادة تحكيم علمي مستقلة، **ليست موافقة من المحرر وليست جاهزية إرسال رسمية**.

## أهم الملفات الموجودة فعليًا

- `Manuscript/FALCON_Final_Editorial_Revision_2026-10-29.docx` و`.pdf`: المخطوطة.
- `Supplement/Online_Resource_1_FALCON_Final_2026-10-29.docx` و`.pdf`: الملحق، Tables S1–S15، ومعايرة IODA.
- `Review/Response_to_Reviewers_FALCON_Final_2026-10-29.docx` و`.pdf`: رد المراجعة الداخلية.
- `Supplement/Atlas_2020_audit.zip`: تدقيق تجميعي لقياسات Atlas وليس ملفات القياس الفردية.
- `Evidence/BGP_2020/` و`Evidence/Reference_2020_20200102/`: سجلات peer–prefix الأصلية المصدّرة وملفات audit.json.
- `QA/FINAL_RELEASE_GATES_2026-10-29.json` و`FILES_MANIFEST_SHA256.json`: بوابات التحقق وبصمات جميع الملفات.
- `Review/REFERENCE_AUDIT_38_INTERNAL_FORMAT.csv`: فحص شكلي مرجعي؛ **ليس تحقيقًا خارجيًا شاملاً**.

## خطوات إعادة الحساب

من جذر الحزمة بعد الاستخراج شغّل:

```bash
python Code/verify_reviewer_bundle.py
python Code/compare_2020_event_vs_non_event.py --event-root Evidence/BGP_2020 --reference-root Evidence/Reference_2020_20200102 --output-dir QA/REPRODUCED_REFERENCE_LOCAL
python Code/reproduce_native_ioda_2023_v2.py --source-zip Supplement/IODA_2023_Original_JSON_SourceArtifact.zip --out QA/REPRODUCED_IODA_2023.csv
```

**ملاحظة منهجية:** نافذة 2–3 يناير اختيرت بعد حدوث الواقعة، وثُبّت تاريخها قبل فحص نتائجها. ليست دراسة مسجلة مسبقًا prospectively، ولا مجموعة ضابطة سببية أو توزيعًا للتقلب الطبيعي. صور IODA 2020 المنشورة موثقة بالبصمات والروابط لكن بياناتها الرقمية الأصلية غير متاحة.

**مطلوب قبل إرسال المجلة:** اعتماد كل المؤلفين، تدقيق المراجع الـ38 ومعلومات DOI، صلاحيات الصور، تعليمات IJCIP الفعلية، وتصريحات النشر والمصالح.
