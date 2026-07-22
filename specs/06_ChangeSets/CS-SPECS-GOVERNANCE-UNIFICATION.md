---
document_id: CS-SPECS-GOVERNANCE-UNIFICATION
title: Documentation Governance and Registry Unification
document_type: Change Set
document_status: Active
implementation_status: In Development
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Documentation Governance
reviewers: [Product Owner, Architecture, Security, QA]
domain_owner: Documentation Governance
created_at: 2026-07-22
updated_at: 2026-07-22
canonical: true
supersedes: []
superseded_by: []
related_decisions: []
related_observations: []
related_change_sets: []
related_modules: []
related_pages: []
related_capabilities: []
---

# Change Set — یکپارچه‌سازی حاکمیت و دسترسی‌پذیری مستندات CAS

## Scope

ایجاد لایه مرکزی Registry و Navigation برای Decision، Capability، Page، Role، Module، Open Item و Implementation Gap؛ تثبیت Metadata/ID Standard؛ همگام‌سازی Indexها با Cycle 10؛ بدون تغییر کد محصول یا Odoo Core.

## Baseline

- Constitution فعال و Cycle 10 ثبت شده بود؛
- Registryهای موضوعی پراکنده بودند؛
- Indexهای پوشه هنوز Cycle 8 یا 9 را آخرین مرجع نشان می‌دادند؛
- شناسه‌های `DEC-010` و `DEC-016` تکرار شده بودند؛
- Open Itemها و Gapها میان چند سند پخش بودند؛
- Page/Role/Module navigation مرکزی کامل وجود نداشت.

## Added

- `00_Project/Documentation_Map.md`
- `00_Project/Metadata_And_ID_Standard.md`
- `00_Project/Decision_Registry.md`
- `00_Project/Capability_Registry.md`
- `00_Project/Page_Registry.md`
- `00_Project/Role_To_Page_Matrix.md`
- `00_Project/Module_Registry.md`
- `00_Project/Open_Item_Registry.md`
- `00_Project/Implementation_Gap_Registry.md`
- `00_Project/Documentation_Validation_Report.md`

## Changed

Indexهای `00_Project`, `01_Product`, `02_UI_UX`, `03_Modules`, `04_Decisions`, `05_Architecture` و `06_ChangeSets` برای:

- معرفی Cycle 10 به‌عنوان آخرین چرخه فعال Review؛
- لینک به Registryهای مرکزی؛
- جداسازی Current Effective Specifications از Historical Review Source؛
- نمایش Page/Module/Decisionهای Cycle 10؛
- حفظ Backward Compatibility لینک‌های قدیمی.

همچنین `Historical_Document_Register`, `Open_Questions` و `Traceability_Matrix` با لایه مرکزی هماهنگ شدند.

## Not Changed

- هیچ فایل کد، Model، View، Security Rule، Manifest یا Migration؛
- هیچ فایل خارج از `specs`؛
- هیچ Decision محصولی یا معماری جدید؛
- هیچ حذف یا Rename فیزیکی سند؛
- هیچ تغییر Odoo Core؛
- هیچ Merge به `main`.

## ID Migration

شناسه‌های قدیمی حفظ شده‌اند. برای Collisionهای شناخته‌شده Canonical Registry Key تعریف شد:

- `DEC-V7-010-PROVIDER-REGISTRY`
- `DEC-UIR09-010-CONSOLIDATED`
- `DEC-V8-016-SEARCH-HISTORY`
- `DEC-UIR10-016-CONSOLIDATED`

Rename فیزیکی فقط در Change Set مستقل با link migration مجاز است.

## Status Migration

مقادیر قدیمی مانند `Consolidated`, `Needs Review`, `Active Review Source` و statusهای چندبخشی فوراً به‌صورت bulk بازنویسی نشده‌اند. استاندارد نگاشت تعریف و Migration تدریجی به Open Item تبدیل شده است تا معنای تاریخی از بین نرود.

## Historical Preservation

- تمام اسناد Historical در محل فعلی باقی می‌مانند؛
- Registryها به Current Canonical Reference لینک می‌دهند؛
- Cycle قدیمی به‌تنهایی تصمیم‌هایش را Supersede نمی‌کند؛
- Prototype و ZIP فقط Evidence Review هستند.

## Risks

- Registry ممکن است با Source Document در آینده Drift کند؛
- لینک‌های Relative در صورت Rename آینده نیازمند Migration Map هستند؛
- نبود validator خودکار می‌تواند Duplicate ID جدید ایجاد کند؛
- بعضی Pageها و Module Placementها هنوز Open هستند.

## Mitigation

- Registry update در Definition of Done هر Change Set؛
- Source Document مرجع حقیقت؛
- Open Item صریح برای تعارض‌ها؛
- عدم Rename یا حذف مخرب؛
- validation دستی Diff و لینک‌ها در این Change Set.

## Validation Result

نتیجه کامل در [`../00_Project/Documentation_Validation_Report.md`](../00_Project/Documentation_Validation_Report.md) ثبت شده است.

- تمام تغییرات فقط داخل `specs` هستند؛
- Branch نسبت به Base عقب نیست؛
- هیچ فایل کد یا Odoo Core تغییر نکرده است؛
- Collisionهای شناخته‌شده ID ثبت شده‌اند؛
- مراجع کلیدی Page/Module/Architecture بررسی شده‌اند؛
- validator خودکار سراسری هنوز Open Item است.

## Rollback

Rollback با حذف Registryهای جدید و بازگرداندن Indexها ممکن است و هیچ داده محصولی را تحت تأثیر قرار نمی‌دهد. اسناد قدیمی دست‌نخورده باقی می‌مانند. بااین‌حال برای حفظ لینک‌های PR و Review، حذف پس از Merge باید فقط با Change Set جدید انجام شود.

## Open Items

تمام موارد unresolved در [`../00_Project/Open_Item_Registry.md`](../00_Project/Open_Item_Registry.md) ثبت شده‌اند.
