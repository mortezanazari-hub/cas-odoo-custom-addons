---
document_id: INDEX-CHANGESETS-001
title: Change Set Documentation Index
document_type: Section Index
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Product & Architecture Governance
domain_owner: Change Governance
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

# 06 — Change Sets

Change Set تفاوت، اثر و مسیر Migration/Revalidation را ثبت می‌کند و به‌تنهایی مجوز تغییر Production نیست.

## Change Set مستندسازی جاری

- [Documentation Governance and Registry Unification](CS-SPECS-GOVERNANCE-UNIFICATION.md)

این Change Set فقط `specs` را به‌صورت additive و non-destructive یکپارچه می‌کند و هیچ تصمیم محصولی یا تغییر کد ایجاد نمی‌کند.

## Cycle 10 — آخرین Review فعال

- [Cycle 10 Alpha Workspace Refinement](CS-UIR10-ALPHA-WORKSPACE-REFINEMENT.md)

Scope: مکاتبات، تفویض، People Picker، مدیریت سامانه، دبیرخانه، نگهبانی و حذف OCR/DMS داخلی از آلفا. وضعیت اجرا=`Gap Identified` و UI Production=`Pending Revalidation`.

## Cycle 9 — Historical Review Source با Decisionهای مؤثر

- [Cycle 9 Workspace UX Consolidation](CS-UIR09-WORKSPACE-UX-CONSOLIDATION.md)

تصمیم‌های بدون Supersede در Cycle 10 همچنان مؤثرند.

## Change Setهای پایه Cycle 8

- [Specs v8 Consolidation](CS-SPECS-V8-CONSOLIDATION.md)
- [Workspace v8](CS-WORKSPACE-V8.md)
- [Dynamic Work Report](CS-WORK-REPORT-DYNAMIC-FORM.md)
- [Employee Workspace](CS-EMPLOYEE-WORKSPACE.md)

## Historical

- `CS-WORKSPACE-V7.md` مرجع Historical انتقال Cycle 4 به Cycle 7 است.
- `CS-SPECS-UI-REVIEW-MODEL-CORRECTION.md` اصلاح مدل تفسیری Cycle و Version را ثبت می‌کند.

## الزام هر Change Set

- Baseline و Target؛
- Source Cycle/Observations؛
- Added/Changed/Removed/Superseded؛
- Decision و Module/Page impacts؛
- Security، Data، Migration، Test و Audit؛
- Revalidation Plan؛
- Open Items و Risks؛
- Rollback؛
- Registry updates؛
- عدم اعلام `Implemented/Accepted` بدون Evidence.
