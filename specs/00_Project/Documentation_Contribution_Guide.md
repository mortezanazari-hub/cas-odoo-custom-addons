---
document_id: GOV-DOC-001
title: CAS Documentation Contribution Guide
document_type: Governance Guide
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
owner: Documentation Governance
domain_owner: Project Governance
created_at: 2026-07-22
updated_at: 2026-07-22
canonical: true
related_documents:
  - Metadata_And_ID_Standard.md
  - Documentation_Map.md
  - Cycle_Closeout_Checklist.md
---

# راهنمای مشارکت و نگهداری مستندات CAS

این سند روش اجباری ایجاد، اصلاح، جایگزینی، بایگانی و اتصال مستندات CAS را تعریف می‌کند. هدف آن این است که حتی در Cycleهای بسیار دور، مانند Cycle 50 یا Cycle 200، وضعیت جاری پروژه بدون خواندن کامل تاریخچه قابل تشخیص باشد.

## ۱. اصل منبع حقیقت

هیچ Cycle، Iteration، جلسه، یادداشت یا فایل Review به‌تنهایی منبع نهایی حقیقت نیست. نتیجه هر Review باید در یکی از مراجع Canonical زیر منعکس شود:

- `Documentation_Map.md`
- `Decision_Registry.md`
- `Capability_Registry.md`
- `Page_Registry.md`
- `Role_To_Page_Matrix.md`
- `Module_Registry.md`
- `Open_Item_Registry.md`
- `Implementation_Gap_Registry.md`
- `Traceability_Matrix.md`
- Specification فعال ماژول، صفحه یا معماری

فایل Review فقط سابقه تصمیم‌گیری است؛ Registry و Specification فعال، وضعیت جاری را نشان می‌دهند.

## ۲. محل ذخیره هر نوع سند

| نوع سند | محل اصلی |
|---|---|
| اطلاعات و Governance پروژه | `specs/00_Project/` |
| Product Scope و جریان‌ها | `specs/01_Product/` |
| UI/UX، Page Spec و Review Cycle | `specs/02_UI_UX/` |
| Specification ماژول | `specs/03_Modules/<module>/` |
| تصمیم‌های رسمی | `specs/04_Decisions/` |
| معماری و Contractها | `specs/05_Architecture/` |
| Change Setها | `specs/06_ChangeSets/` |

سندی که محل مشخص ندارد نباید در ریشه Repository یا پوشه‌ای موقت رها شود.

## ۳. قواعد نام‌گذاری

- نام فایل باید پایدار، توصیفی و بدون عبارت‌هایی مانند `final`, `new`, `last`, `corrected`, `v2-final` باشد.
- نسخه و وضعیت در Metadata ثبت می‌شود، نه در نام مبهم فایل.
- شناسه‌ها باید مطابق `Metadata_And_ID_Standard.md` یکتا باشند.
- Page، Decision، Capability، Module، Open Item و Change Set باید شناسه رسمی داشته باشند.
- Rename فایل Canonical فقط با Migration Map و اصلاح همه ارجاعات مجاز است.

## ۴. Metadata اجباری

هر سند جدید باید حداقل این فیلدها را داشته باشد:

```yaml
document_id: UNIQUE-ID
title: Human readable title
document_type: Document Type
document_status: Draft|Under Review|Agreed|Active|Superseded|Historical|Rejected|Archived
implementation_status: Not Assessed|Planned|Gap Identified|In Development|Implemented|Verified|N/A
ui_validation_status: Not Assessed|Pending Revalidation|Prototype Reviewed|Accepted|Rejected|N/A
owner: Responsible owner
domain_owner: Business or technical domain
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
canonical: true|false
supersedes: []
superseded_by: []
related_decisions: []
related_modules: []
related_pages: []
related_capabilities: []
```

فیلدهای بی‌ربط می‌توانند `N/A` یا آرایه خالی باشند، اما نباید وضعیت‌های متفاوت در یک فیلد ترکیب شوند.

## ۵. ایجاد سند جدید یا اصلاح سند موجود

### سند موجود را اصلاح کن وقتی:

- همان موضوع، همان مالک و همان مرجع Canonical ادامه دارد.
- تغییر باعث شکستن برداشت تاریخی نمی‌شود.
- تصمیم جدید، ماهیت سند را عوض نمی‌کند.

### سند جدید ایجاد کن وقتی:

- یک تصمیم رسمی جدید ایجاد شده است.
- یک صفحه یا ماژول مستقل ایجاد شده است.
- قرارداد معماری جدیدی با چرخه عمر مستقل لازم است.
- سند قبلی باید به‌عنوان تاریخچه ثابت باقی بماند.

### سند قبلی را Supersede کن وقتی:

- مرجع جدید جایگزین کامل آن شده است.
- رفتار یا ساختار قبلی دیگر مبنای اجرا نیست.

در این حالت هر دو سمت رابطه باید ثبت شوند:

```yaml
# سند قدیمی
document_status: Superseded
superseded_by:
  - NEW-DOC-ID

# سند جدید
supersedes:
  - OLD-DOC-ID
```

## ۶. قواعد Review Cycle و Iteration

هر Cycle باید در مسیر استاندارد خود نگهداری شود و حداقل شامل موارد زیر باشد:

- `README.md`: Scope، وضعیت و Baseline Cycle
- فایل‌های Iteration
- تصمیم‌های استخراج‌شده
- Change Summary
- Validation یا Closeout Report

هر Iteration باید مشخص کند:

- چه چیزی بررسی شد؛
- چه چیزی پذیرفته شد؛
- چه چیزی رد شد؛
- چه چیزی Deferred شد؛
- چه چیزی نیازمند تصمیم یا پیاده‌سازی است؛
- کدام Registry و Specification باید اصلاح شود.

## ۷. به‌روزرسانی اجباری پس از هر Cycle

در پایان هر Cycle باید همه مراجع زیر بررسی شوند، حتی اگر بعضی از آن‌ها تغییر نکنند:

1. Documentation Map
2. Decision Registry
3. Capability Registry
4. Page Registry
5. Role-to-Page Matrix
6. Module Registry
7. Open Item Registry
8. Implementation Gap Registry
9. Traceability Matrix
10. Historical Document Register
11. Specificationهای تحت تأثیر

هیچ تصمیمی نباید فقط در فایل Cycle باقی بماند.

## ۸. قواعد Baseline

- آخرین Cycle به‌طور خودکار همه تصمیم‌های Cycleهای قبلی را باطل نمی‌کند.
- تصمیم قدیمی تا زمانی Active است که Supersede یا Revoke صریح شود.
- `Documentation_Map.md` باید آخرین Baseline قابل اتکا را نشان دهد.
- Registryها باید وضعیت جاری را نمایش دهند، نه صرفاً آخرین تاریخ فایل را.

## ۹. قواعد Traceability

هر تغییر مهم باید حداقل این زنجیره را پوشش دهد:

```text
Review Source
→ Decision
→ Page/Capability
→ Module/Architecture
→ Implementation Gap یا Implementation Evidence
→ Change Set
```

تصمیم بدون Source، صفحه بدون مالک، Capability بدون دامنه و Gap بدون مرجع قابل قبول نیست.

## ۱۰. قواعد حذف و بایگانی

- حذف سند تاریخی ممنوع است مگر اینکه تکراری، محرمانه، مخرب یا اشتباه قطعی باشد.
- حذف باید در Change Set ثبت شود.
- برای اسناد معتبر قدیمی، `Historical` یا `Superseded` ترجیح دارد.
- فایل Archived نباید به‌عنوان مرجع جاری لینک شود.

## ۱۱. مسئولیت‌ها

| نقش | مسئولیت |
|---|---|
| Document Author | Metadata، لینک‌ها و محتوای صحیح |
| Domain Owner | صحت دامنه و تصمیم‌های تخصصی |
| Documentation Maintainer | Registryها، Indexها و سازگاری ساختار |
| Reviewer | کنترل تناقض، Traceability و وضعیت‌ها |
| Product/Architecture Owner | تصویب تغییر Baseline یا تصمیم‌های حساس |

یک نویسنده نباید تصمیم محصولی یا معماری حل‌نشده را صرفاً برای تکمیل سند قطعی جلوه دهد.

## ۱۲. قاعده Merge

تغییر مستنداتی که Baseline، تصمیم، صفحه، Capability، ماژول یا Gap را عوض می‌کند، فقط زمانی آماده Merge است که `Cycle_Closeout_Checklist.md` یا چک‌لیست متناظر Change Set تکمیل شده باشد.

## ۱۳. قاعده همکاری با AI

هر عامل هوش مصنوعی قبل از تولید یا اصلاح مستندات باید `AI_Working_Guide.md` را بخواند و Registryهای مرکزی را نسبت به فایل‌های تاریخی مقدم بداند.
