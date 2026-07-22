---
document_id: INDEX-DECISIONS-001
title: Decision Documentation Index
document_type: Section Index
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Product & Architecture Governance
domain_owner: Decision Governance
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

# 04 — Decisions

این بخش Decision Recordهای رسمی پروژه را نگهداری می‌کند. نقطه ورود و رفع ابهام شناسه‌ها [Decision Registry](../00_Project/Decision_Registry.md) است.

## تصمیم تجمیعی Cycle 10

- [`DEC-016-UIR10-CONSOLIDATED` — اصلاح Workspace آلفا](DEC-016-UIR10-Consolidated-Alpha-Workspace-Refinement.md)

این تصمیم مکاتبات، تفویض، Shared People Picker، گروه‌های مدیریت سامانه، دبیرخانه، نگهبانی و Scope OCR/DMS آلفا را پوشش می‌دهد. وضعیت Backend=`Gap Identified` و Production UI=`Pending Revalidation` است.

## تصمیم تجمیعی Cycle 9

- [`DEC-010-UIR09-CONSOLIDATED` — Workspace و جریان‌های عملیاتی](DEC-010-UIR09-Consolidated-Workspace-And-Operational-UX.md)

Cycle 9 Navigation، Attendance correction/audit، Overtime، Activity Proposal، Dynamic Matrix و Dashboard personalization را تثبیت می‌کند. بخش‌های بدون Supersede در Cycle 10 همچنان معتبرند.

## تصمیم‌های پایه و Cycle 8

- [`DEC-001` — Workspace عملیاتی](DEC-001-Workspace-Is-Operational.md)
- [`DEC-002` — عدم نمایش SLA فنی در Employee UI](DEC-002-No-SLA-In-Employee-UI.md)
- [`DEC-003` — Activity Standardization](DEC-003-Activity-Standardization.md)
- [`DEC-004` — Widget System](DEC-004-Workspace-Widget-System.md)
- [`DEC-005` — Conversations First-Class](DEC-005-Conversations-Are-First-Class.md)
- [`DEC-006` — Theme and Readability](DEC-006-Workspace-Theme-And-Readability.md)
- [`DEC-007` — Collapsible Sidebar](DEC-007-Collapsible-Sidebar.md)
- [`DEC-008` — Embedded Calendar](DEC-008-Embedded-Calendar.md)
- [`DEC-009` — Route and Capability Expansion](DEC-009-Workspace-Route-And-Capability-Expansion.md) — Partially Superseded
- [`DEC-010` — Global Provider Registries](DEC-010-Global-Provider-Registries.md) — Legacy metadata Under Review
- [`DEC-011` — Domain Separation](DEC-011-Separate-Task-Action-Notification-History.md)
- [`DEC-012` — Personal Task Category Governance](DEC-012-Personal-Task-Category-Governance.md)
- [`DEC-013` — Calendar Attendee/Assignment Authorization](DEC-013-Calendar-Attendee-Selection-And-Assignment-Authorization.md)
- [`DEC-014` — Discuss Reuse](DEC-014-Discuss-Reuse-And-Message-Interaction.md)
- [`DEC-015` — Overlay and Focus](DEC-015-Overlay-Layering-And-Focus-Management.md)
- [`DEC-016` — Search and Recent History Consolidation](DEC-016-Search-And-Recent-History-Consolidation.md)
- [`DEC-017` — Work Report Uses Form Engine](DEC-017-Work-Report-Domain-Uses-Form-Engine.md)
- [`DEC-018` — Dashboard Administration](DEC-018-Dashboard-Administration-And-Governance.md)
- [`DEC-019` — Work Report Shift/Applicability](DEC-019-Work-Report-Applicability-And-Shift-Period.md)
- [`DEC-020` — Delegated Work Report Access](DEC-020-Delegated-Work-Report-Access.md)

## شناسه‌های متعارض

`DEC-010` و `DEC-016` در نام چند سند تکرار شده‌اند. فایل‌ها برای حفظ لینک‌ها Rename نشده‌اند. کلیدهای یکتا و Migration Map در [Metadata and ID Standard](../00_Project/Metadata_And_ID_Standard.md) ثبت شده‌اند.

## قواعد

- Source Document مرجع تفصیلی است؛ Registry مرجع Navigation و Status خلاصه؛
- Decision Active با محدودیت کد تضعیف نمی‌شود؛
- `Agreed/Active` معادل `Implemented/Accepted in Production` نیست؛
- Supersede باید صریح، دوطرفه و قابل ردیابی باشد؛
- Prototype، Commit Message یا گفتگو به‌تنهایی Decision رسمی نیست.
