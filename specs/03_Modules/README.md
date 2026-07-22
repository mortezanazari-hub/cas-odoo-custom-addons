---
document_id: INDEX-MODULES-001
title: Module Documentation Index
document_type: Section Index
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Architecture Governance
domain_owner: Module Ownership Governance
created_at: N/A
updated_at: 2026-07-22
canonical: true
supersedes: []
superseded_by: []
related_decisions: [DEC-UIR09-010-CONSOLIDATED, DEC-UIR10-016-CONSOLIDATED]
related_modules: []
related_pages: []
related_capabilities: []
---

# 03 — Modules

این بخش مالکیت دامنه‌ها، Dependency، Provider Contract، Module Specification و Impact Assessmentها را نگهداری می‌کند.

## Navigation مرکزی

- [Module Registry](../00_Project/Module_Registry.md)
- [Capability Registry](../00_Project/Capability_Registry.md)
- [Implementation Gap Registry](../00_Project/Implementation_Gap_Registry.md)
- [Open Item Registry](../00_Project/Open_Item_Registry.md)

## Architecture Maps فعال

- [Module Ownership Map](V8_Module_Ownership_Map.md)
- [Dependency Map](V8_Dependency_Map.md)
- [Provider Registry](V8_Provider_Registry.md)
- [Module Boundaries](../05_Architecture/Module_Boundaries.md)
- [Capability and Security Model](../05_Architecture/Capability_And_Security_Model.md)

اسناد بالا با منشأ Cycle 8 همچنان فعال‌اند، مگر بخش‌هایی که Cycle 9 یا 10 صریحاً تغییر داده است.

## Impact Assessmentهای جاری

- [Cycle 10 Module Impact](V10_Module_Impact_Assessment.md)
- [Cycle 9 Cross-module Impact](Cross_Module_UIR09_Impact_Assessment.md)
- [Cycle 8 Impact](V8_Impact_Assessment.md)

## Specificationهای پایه

- [`cas_workspace`](cas_workspace/Specification.md)
- [`cas_personal_task`](cas_personal_task/Specification.md)
- [`cas_organization_core`](cas_organization_core/Specification.md)
- [`cas_activity_catalog`](cas_activity_catalog/Specification.md)
- [`cas_work_report`](cas_work_report/Specification.md)
- [امنیت `cas_work_report`](cas_work_report/Security.md)

## دامنه‌های Cycle 10 نیازمند تعیین Placement نهایی

- Delegation Domain؛
- Secretariat Registry؛
- Shared People Picker technical placement.

این موارد Requirement و Ownership مفهومی دارند، اما نام یا محل فنی نهایی آن‌ها در [Open Item Registry](../00_Project/Open_Item_Registry.md) باز است.

## تفکیک Repository Presence و Specification Status

فهرست ۲۴ ماژول موجود در `MODULES.md` با تمام module/domainهای مصوب Specification یکسان نیست. Module Registry برای هر مورد به‌صورت جدا مشخص می‌کند:

- موجود در Repository؛
- Specified/Proposed؛
- Gap Identified؛
- Out of Alpha؛
- نیازمند تصمیم Placement.

وجود کد به معنی Implementation Ready یا انطباق با اسناد Active نیست.

## Historical

اسناد `V7_*` و Impactهای Cycle 7 Historical Reference هستند. انتقال فیزیکی یا Rename آن‌ها فقط با Link Migration Change Set مجاز است.

## Definition of Implementation Ready

Specification، API Contract، Security، Migration، Test Strategy، Acceptance، Observability، Rollback و Open Itemهای مسدودکننده باید کامل و تصویب شده باشند. Impact Assessment به‌تنهایی مجوز اجرا نیست.
