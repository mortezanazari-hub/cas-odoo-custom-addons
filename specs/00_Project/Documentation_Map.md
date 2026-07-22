---
document_id: MAP-DOCS-001
title: CAS Documentation Map
document_type: Project Navigation
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Product & Architecture Governance
domain_owner: Documentation Governance
created_at: 2026-07-22
updated_at: 2026-07-22
canonical: true
supersedes: []
superseded_by: []
related_decisions: []
related_modules: []
related_pages: []
related_capabilities: []
---

# نقشه مرکزی مستندات CAS

این فایل نقطه ورود روزمره به حافظه مهندسی پروژه است. مرجع قانونی بالادستی همچنان [`../README.md`](../README.md) است.

> آخرین چرخه فعال بازنگری UI: **CAS UI Review Cycle 10 — Through Iteration 13**  
> Cycle شماره نسخه نرم‌افزار نیست. تصمیم‌های Active چرخه‌های پیشین تا زمان Supersede صریح معتبر می‌مانند.

## ۱. مسیرهای اصلی

| سؤال | مرجع مرکزی |
|---|---|
| درباره یک موضوع چه تصمیمی گرفته شده است؟ | [Decision Registry](Decision_Registry.md) |
| مالک یک Capability یا نام مترادف آن چیست؟ | [Capability Registry](Capability_Registry.md) |
| یک صفحه، Route یا نقش به چه اسنادی متصل است؟ | [Page Registry](Page_Registry.md) و [Role-to-Page Matrix](Role_To_Page_Matrix.md) |
| مالک داده، ماژول و Provider چیست؟ | [Module Registry](Module_Registry.md) |
| چه چیزی هنوز اجرا نشده یا Gap دارد؟ | [Implementation Gap Registry](Implementation_Gap_Registry.md) |
| چه سؤال، تعارض، ریسک یا مورد Deferred باز است؟ | [Open Item Registry](Open_Item_Registry.md) |
| Metadata، Status و شناسه‌ها چگونه ثبت می‌شوند؟ | [Metadata and ID Standard](Metadata_And_ID_Standard.md) |
| Observation تا Implementation و Revalidation چگونه دنبال می‌شود؟ | [Traceability Matrix](Traceability_Matrix.md) |
| اسناد قدیمی چه وضعیتی دارند؟ | [Historical Document Register](Historical_Document_Register.md) |

## ۲. سلسله‌مراتب اطلاعات

### سطح اول — Registry و Navigation

- این فایل و Registryهای مرکزی؛
- فقط Index، وضعیت خلاصه و Link؛
- بدون کپی کامل محتوای اسناد تفصیلی.

### سطح دوم — اسناد Canonical و اجرایی

- Product و Architecture Decisions؛
- Security و Architecture Contracts؛
- Module Specifications؛
- Page Specifications؛
- Provider، Workflow و Data Contracts؛
- Change Sets و Acceptance Criteria.

### سطح سوم — شواهد و تاریخچه

- UI Review Registers و Observations؛
- Iteration Deltaها؛
- Prototype Notes و Screenshots؛
- Validation Reports؛
- Historical و Superseded Documents.

## ۳. ترتیب مطالعه اجباری

1. [`../README.md`](../README.md)
2. [UI Review Lifecycle](UI_Review_Lifecycle.md)
3. [Documentation Governance](Documentation_Governance.md)
4. [Version History](Version_History.md)
5. [Traceability Matrix](Traceability_Matrix.md)
6. [Historical Document Register](Historical_Document_Register.md)
7. [Open Item Registry](Open_Item_Registry.md)
8. [`../01_Product/Terminology.md`](../01_Product/Terminology.md)
9. [`../01_Product/UX_Principles.md`](../01_Product/UX_Principles.md)
10. [Module Registry](Module_Registry.md)
11. [`../03_Modules/V8_Dependency_Map.md`](../03_Modules/V8_Dependency_Map.md)
12. [`../03_Modules/V8_Provider_Registry.md`](../03_Modules/V8_Provider_Registry.md)
13. [`../05_Architecture/Module_Boundaries.md`](../05_Architecture/Module_Boundaries.md)
14. [`../05_Architecture/Capability_And_Security_Model.md`](../05_Architecture/Capability_And_Security_Model.md)
15. تمام Decisionها، Page Specها، Module Specها و Change Setهای مرتبط با موضوع.

## ۴. مراجع Cycle 10

- [Cycle 10 Register](UI_Review_Cycle_10_Register.md)
- [`DEC-016-UIR10-CONSOLIDATED`](../04_Decisions/DEC-016-UIR10-Consolidated-Alpha-Workspace-Refinement.md)
- [Cycle 10 Module Impact](../03_Modules/V10_Module_Impact_Assessment.md)
- [Cycle 10 Acceptance Criteria](../05_Acceptance/V10_Alpha_Acceptance_Criteria.md)
- [Cycle 10 Alpha Out of Scope](../07_Out_Of_Scope/V10_Alpha_Out_Of_Scope.md)
- [Cycle 10 Change Set](../06_ChangeSets/CS-UIR10-ALPHA-WORKSPACE-REFINEMENT.md)

## ۵. مراجع Cycleهای پیشین

Cycleهای 8 و 9 Historical Review Source هستند، اما Decisionهای Active و Agreed آن‌ها در صورت نبود Supersede صریح همچنان در مجموعه Specification مؤثر قرار می‌گیرند.

- [Cycle 8 Review Record](V8_Canonical_Baseline.md)
- [Cycle 9 Register](UI_Review_Cycle_9_Register.md)
- [`DEC-010-UIR09-CONSOLIDATED`](../04_Decisions/DEC-010-UIR09-Consolidated-Workspace-And-Operational-UX.md)

## ۶. قاعده نگهداری Registryها

هر Decision، Capability، Module، Page یا Gap جدید باید در همان Change Set به Registry متناظر افزوده شود. Registry Entry بدون Source Document، Owner یا Status ناقص است. اسناد تفصیلی مرجع حقیقت باقی می‌مانند و در تعارض، سلسله‌مراتب `specs/README.md` اعمال می‌شود.
