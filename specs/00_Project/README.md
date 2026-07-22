---
document_id: INDEX-PROJECT-001
title: Project Governance Index
document_type: Section Index
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Product & Architecture Governance
domain_owner: Documentation Governance
created_at: N/A
updated_at: 2026-07-22
canonical: true
supersedes: []
superseded_by: []
related_decisions: []
related_modules: []
related_pages: []
related_capabilities: []
---

# 00 — Project Governance and Registries

این بخش نقطه ورود به حاکمیت مستندات، تاریخچه UI Review، Registryها، Traceability، وضعیت اجرا و اعتبارسنجی مجدد CAS است.

> آخرین چرخه فعال بازنگری UI: **CAS UI Review Cycle 10 — Through Iteration 13**  
> Cycle شماره Software Release نیست. تصمیم‌های Active چرخه‌های گذشته تا زمان Supersede صریح معتبر می‌مانند.

## شروع سریع

- [نقشه مرکزی مستندات](Documentation_Map.md)
- [قانون اساسی مستندات](../README.md)
- [استاندارد Metadata و شناسه‌ها](Metadata_And_ID_Standard.md)
- [معماری اطلاعات Repository](Repository_Information_Architecture.md)

## راهنمای اجرایی نگهداری مستندات

- [راهنمای مشارکت و نگهداری مستندات](Documentation_Contribution_Guide.md)
- [چرخه عمر مستندات](Documentation_Lifecycle.md)
- [راهنمای اجرای Review Cycle و Iteration](Review_Process_Guide.md)
- [چک‌لیست اجباری پایان Cycle](Cycle_Closeout_Checklist.md)
- [راهنمای کار هوش مصنوعی](AI_Working_Guide.md)
- [قالب استاندارد Cycle جدید](../02_UI_UX/Review_Cycles/_Template/README.md)

## Registryهای مرکزی

- [Decision Registry](Decision_Registry.md)
- [Capability Registry](Capability_Registry.md)
- [Page Registry](Page_Registry.md)
- [Role-to-Page Matrix](Role_To_Page_Matrix.md)
- [Module Registry](Module_Registry.md)
- [Implementation Gap Registry](Implementation_Gap_Registry.md)
- [Open Item Registry](Open_Item_Registry.md)

## اسناد حاکمیتی

- [چرخه بازنگری UI و حلقه QA](UI_Review_Lifecycle.md)
- [حاکمیت مستندات](Documentation_Governance.md)
- [تاریخچه چرخه‌ها](Version_History.md)
- [Traceability Matrix](Traceability_Matrix.md)
- [Historical/Superseded Register](Historical_Document_Register.md)
- [Open Questions قدیمی و سازگاری لینک‌ها](Open_Questions.md)

## Cycle 10 — آخرین Review فعال

- [Cycle 10 Register](UI_Review_Cycle_10_Register.md)
- [Cycle 10 Decision](../04_Decisions/DEC-016-UIR10-Consolidated-Alpha-Workspace-Refinement.md)
- [Cycle 10 Module Impact](../03_Modules/V10_Module_Impact_Assessment.md)
- [Cycle 10 Acceptance Criteria](../05_Acceptance/V10_Alpha_Acceptance_Criteria.md)
- [Cycle 10 Alpha Out of Scope](../07_Out_Of_Scope/V10_Alpha_Out_Of_Scope.md)
- [Cycle 10 Change Set](../06_ChangeSets/CS-UIR10-ALPHA-WORKSPACE-REFINEMENT.md)

## Historical Review Sources

- [Cycle 9 Register](UI_Review_Cycle_9_Register.md)
- [Cycle 8 Review Record](V8_Canonical_Baseline.md)

Cycle 8 و 9 Historical Review Source هستند، اما تصمیم‌های Agreed/Active آن‌ها که صریحاً Supersede نشده‌اند در مجموعه Specification مؤثر باقی می‌مانند.

## قاعده استفاده

هر سند یا تغییر جدید باید:

1. نوع نسخه را مشخص کند: UI Review Cycle، Iteration، Document Version یا Software Release؛
2. Observation/Source Cycle و Owner را ثبت کند؛
3. Decision، Capability، Page، Module، Gap و Change Set مرتبط را به Registryها متصل کند؛
4. Document، Implementation و UI Validation status را جدا نگه دارد؛
5. Supersede را صریح و دوطرفه ثبت کند؛
6. Security، Migration، Test، Audit و Revalidation را بررسی کند؛
7. Prototype یا کد فعلی را به‌جای Decision Active معرفی نکند؛
8. پیش از بسته‌شدن Cycle، `Cycle_Closeout_Checklist.md` را تکمیل کند.
