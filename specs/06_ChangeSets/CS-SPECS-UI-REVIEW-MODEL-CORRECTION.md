# Change Set — اصلاح مدل مفهومی پوشه specs

| مشخصه | مقدار |
|---|---|
| شناسه | `CS-SPECS-UI-REVIEW-MODEL-CORRECTION` |
| وضعیت | `Applied` |
| نوع | Documentation Governance Correction |
| Source | Product Owner Clarification |
| UI Review Cycle | `N/A` |

## مشکل

در تجمیع قبلی، `CAS UI Workspace v8 — Through Iteration 12` به‌اشتباه به‌عنوان نسخه محصول و Baseline نهایی معرفی شد.

## تفسیر صحیح

- Cycle 8 هشتمین بازنگری کلی UI است.
- Iteration 12 اصلاح داخلی Cycle 8 است.
- شماره Cycle با Software Version متفاوت است.
- Cycle بعدی می‌تواند آخرین مرجع بازنگری UI شود.
- Decisionهای Active خودکار با Cycle جدید منقضی نمی‌شوند.
- مرجع Backend مجموعه اسناد مؤثر و Active است.

## تغییرات

- بازنویسی `specs/README.md`
- افزودن `UI_Review_Lifecycle.md`
- اصلاح `Version_History.md`
- بازتعریف `V8_Canonical_Baseline.md` به‌عنوان رکورد Cycle 8
- اصلاح `Documentation_Governance.md`
- اصلاح `Traceability_Matrix.md`
- اصلاح Index سطح پروژه
- ثبت این Change Set

## اثر

از این پس مسیر رسمی چنین است:

```text
UI Review
→ Observation
→ Decision
→ Module Impact
→ Backend Change
→ Implementation
→ UI Revalidation
```

## Migration مستندات

اسناد قدیمی حذف نمی‌شوند. عبارت‌های «نسخه محصول»، «Baseline نهایی محصول» و «نسخه 8 غیرقابل‌تغییر» در اسناد مرکزی اصلاح می‌شوند. تصمیم‌های Active موجود حفظ می‌شوند.
