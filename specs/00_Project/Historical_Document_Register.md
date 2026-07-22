---
document_id: REG-HIST-001
title: Historical and Superseded Document Register
document_type: Historical Register
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Documentation Governance
domain_owner: Historical Records Governance
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

# فهرست اسناد Historical، Superseded و منابع Review قدیمی

این Register اسناد قدیمی را حذف نمی‌کند؛ فقط جایگاه مرجعیت و مسیر مرجع فعلی را روشن می‌کند.

> آخرین چرخه فعال Review: **Cycle 10 — Through Iteration 13**.  
> Cycle 8 و 9 Historical Review Source هستند، اما Decisionهای Active/Agreed آن‌ها بدون Supersede صریح معتبر می‌مانند.

## ۱. Cycle 7 — Historical UI Baselines

| سند | وضعیت | مرجع فعلی |
|---|---|---|
| `02_UI_UX/Employee/Workspace.md` | Historical | `02_UI_UX/Employee/Workspace_V8.md` + Cycle 9/10 Decisions |
| `02_UI_UX/Shared/Workspace_Shell.md` | Historical | `02_UI_UX/Shared/Workspace_Shell_V8.md` |
| `03_Modules/V7_Module_Impact_And_New_Modules.md` | Historical | Module Registry + Cycle 8/9/10 impacts |
| `03_Modules/Cross_Module_V7_Impact_Assessment.md` | Historical | current Module/Gap Registries |
| `03_Modules/cas_workspace/V7_Impact_Assessment.md` | Historical | `cas_workspace/Specification.md` |
| `03_Modules/cas_action_hub/V7_Impact_Assessment.md` | Historical | Module Boundaries/Registry |
| `03_Modules/cas_work_report/V7_Impact_Assessment.md` | Historical | `cas_work_report/Specification.md` |
| `05_Architecture/Workspace_UI_Integration_Notes.md` | Historical | active Architecture Contracts |
| `06_ChangeSets/CS-WORKSPACE-V7.md` | Historical | Cycle 8+ Change Sets |

## ۲. Cycle 8 — Historical Review Source، با تصمیم‌های مؤثر بدون Supersede

- `00_Project/V8_Canonical_Baseline.md` یک Review Record است، نه Software Version یا Canonical Product Release؛
- `Workspace_V8`, `Workspace_Shell_V8`, Module Maps، Provider Registry و Architecture Contracts در بخش‌های بدون Supersede همچنان فعال‌اند؛
- Routeهای مستقل Search و Recent History و Capability `history.read` Superseded شده‌اند؛
- تصمیم Dashboard reorder-only در Cycle 9 با visibility/shortcut customization گسترش یافته است.

## ۳. Cycle 9 — Historical Review Source، با تصمیم‌های مؤثر بدون Supersede

- `00_Project/UI_Review_Cycle_9_Register.md`؛
- `04_Decisions/DEC-010-UIR09-Consolidated-Workspace-And-Operational-UX.md`؛
- `06_ChangeSets/CS-UIR09-WORKSPACE-UX-CONSOLIDATION.md`.

Cycle 9 آخرین Cycle فعال نیست. تصمیم‌های Navigation، Attendance correction/audit، Overtime، Activity Proposal، Form Matrix و Dashboard که در Cycle 10 تغییر نکرده‌اند همچنان مؤثرند.

## ۴. Cycle 10 — Current Review Source

مرجع فعلی:

- `00_Project/UI_Review_Cycle_10_Register.md`؛
- `04_Decisions/DEC-016-UIR10-Consolidated-Alpha-Workspace-Refinement.md`؛
- `03_Modules/V10_Module_Impact_Assessment.md`؛
- `05_Acceptance/V10_Alpha_Acceptance_Criteria.md`؛
- `07_Out_Of_Scope/V10_Alpha_Out_Of_Scope.md`؛
- `06_ChangeSets/CS-UIR10-ALPHA-WORKSPACE-REFINEMENT.md`.

## ۵. Partially Superseded

### `DEC-009-Workspace-Route-And-Capability-Expansion.md`

Route مستقل Search/Recent History و `history.read` توسط تصمیم Search/History Cycle 8 جایگزین شده‌اند. سایر بخش‌ها فقط در صورت تعارض صریح بی‌اعتبارند.

### `DEC-010-Global-Provider-Registries.md`

شناسه Legacy با تصمیم تجمیعی Cycle 9 Collision دارد. محتوای Provider Registry باید همراه `03_Modules/V8_Provider_Registry.md` خوانده شود. وضعیت Source metadata=`Needs Review` است.

### پیشنهاد `cas_recent_history`

ماژول مستقل ساخته نمی‌شود؛ Recent Resource Reference در Workspace باقی می‌ماند.

### Notification Core کامل

ساخت سیستم موازی تصویب نشده است. Odoo Mail/Discuss/Bus Reuse می‌شود و Extension فقط پس از Gap Analysis مجاز است.

### UI لیستی ثبت نگهبانی

با Page Specification ایستگاه سریع Cycle 10 Superseded شده است. مالک Backend و مدل‌های Attendance تغییر نمی‌کنند.

### OCR و DMS داخلی در آلفا

وجود module/code تاریخی یا عمومی به معنی حضور در Alpha Navigation نیست. Cycle 10 آن‌ها را از Alpha Scope خارج کرده و Attachment مجاز باقی مانده است.

## ۶. اسناد Active با منشأ قدیمی

قدیمی‌بودن Source Cycle به‌تنهایی سند را Historical یا Superseded نمی‌کند. Decisionهای پایه، Module Specs و Architecture Contracts فقط با رابطه صریح Supersede تغییر می‌کنند.

## ۷. انتقال فیزیکی

اسناد Historical فعلاً در مسیر اصلی باقی می‌مانند تا لینک‌ها نشکنند. انتقال، Rename یا Archive فیزیکی فقط در Change Set مستقل همراه Link Migration Map مجاز است.

## ۸. مسیر مرجع فعلی

برای استفاده روزمره ابتدا [Documentation Map](Documentation_Map.md)، سپس Registry مرتبط و در نهایت Source Document خوانده شود.
