---
document_id: GOV-IA-001
title: CAS Repository Information Architecture
document_type: Information Architecture
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
owner: Documentation Governance
domain_owner: Project Governance
created_at: 2026-07-22
updated_at: 2026-07-22
canonical: true
related_documents:
  - Documentation_Map.md
  - Documentation_Contribution_Guide.md
---

# معماری اطلاعات Repository مستندات CAS

## ۱. هدف

ساختار Repository باید سه نیاز را هم‌زمان پوشش دهد:

1. دسترسی سریع به وضعیت جاری؛
2. حفظ کامل تاریخچه تصمیم‌ها و Reviewها؛
3. Traceability میان محصول، UI، ماژول، معماری و پیاده‌سازی.

## ۲. لایه‌های اطلاعات

### لایه ۱: Navigation و Governance

`specs/00_Project/`

شامل نقشه مستندات، استانداردها، Registryها، چک‌لیست‌ها، وضعیت پروژه و راهنمای AI است. این لایه نقطه شروع همه خوانندگان است.

### لایه ۲: Product Truth

`specs/01_Product/`

دامنه محصول، Scope، Actorها، جریان‌های کسب‌وکار و نیازمندی‌های سطح بالا را نگه می‌دارد.

### لایه ۳: Experience Truth

`specs/02_UI_UX/`

Page Specificationها، Role Viewها، Journeyها، Prototype Reviewها و Cycleهای UI را نگه می‌دارد.

### لایه ۴: Module Truth

`specs/03_Modules/`

برای هر ماژول، Specification، Security، Models، Views، Integration و Implementation Notes نگهداری می‌شود.

### لایه ۵: Decision Truth

`specs/04_Decisions/`

تصمیم‌های مستقل و قابل ارجاع محصولی، UI و معماری را نگه می‌دارد. Registry مرکزی وضعیت جاری آن‌ها را مشخص می‌کند.

### لایه ۶: Architecture Truth

`specs/05_Architecture/`

قراردادها، Boundaryها، Security Model، Eventها، APIها، Integrationها و اصول معماری را نگه می‌دارد.

### لایه ۷: Change Truth

`specs/06_ChangeSets/`

بسته تغییر، Scope، اثر، ریسک، Validation و Rollback را ثبت می‌کند.

## ۳. وضعیت جاری در برابر تاریخچه

- Registry و Specification Active وضعیت جاری‌اند.
- Review Cycle و Iteration تاریخچه شکل‌گیری تصمیم‌اند.
- Historical Register مسیر دستیابی به نسخه‌های قدیمی را حفظ می‌کند.
- هیچ خواننده‌ای برای فهم وضع جاری نباید همه Cycleها را مرور کند.

## ۴. مسیر استاندارد پاسخ به سؤال

```text
سؤال درباره قابلیت
→ Capability Registry
→ Page Registry
→ Module Registry
→ Specification و Decision

سؤال درباره صفحه
→ Page Registry
→ Page Specification
→ Role Matrix و Capability
→ Implementation Gap

سؤال درباره چرایی تصمیم
→ Decision Registry
→ Source Review
→ اسناد Superseded یا Historical
```

## ۵. اصل مالکیت

هر موضوع باید یک مالک دامنه و یک مرجع Canonical داشته باشد. چند فایل می‌توانند درباره یک موضوع توضیح دهند، اما فقط یک مرجع باید وضعیت جاری را تعیین کند.
