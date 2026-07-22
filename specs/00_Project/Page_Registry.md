---
document_id: REG-PAGE-001
title: CAS Page Registry
document_type: Page Registry
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Product & UX Governance
domain_owner: Page Governance
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

# رجیستری مرکزی صفحات CAS

Registry فقط Index است. Layout، رفتار، State، Security و Acceptance در Page Specification اصلی قرار دارد. Document، Backend Implementation و UI Validation سه محور مستقل‌اند.

## ۱. صفحات Workspace و کاربر

| Page ID | عنوان فارسی / English | Route / Entry | Provider/Module Owner | نقش‌ها | Capability | Source Cycle | UI Status | Backend Status | Canonical Page Spec | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| `PAGE-WORKSPACE-HOME-V8` | میزکار / Workspace Home | `workspace-home` | `cas_workspace` + Domain Providers | همه کاربران داخلی مجاز | `workspace.use` | Cycle 8؛ اصلاح Cycle 9 | Pending Revalidation | Gap Identified | [Workspace V8](../02_UI_UX/Employee/Workspace_V8.md) | Historical predecessor: `Workspace.md`. |
| `PAGE-EMP-TASK-001` | کارهای شخصی / Personal Tasks | `personal-tasks` | `cas_personal_task` | کاربر عادی و نقش‌های دارای Capability | `personal_task.use` | Cycle 8 | Pending Revalidation | Gap Identified | [Personal Tasks](../02_UI_UX/Employee/Personal_Tasks.md) | ماژول مالک در فهرست ۲۴ ماژول فعلی وجود ندارد. |
| `PAGE-EMP-CAL-001` | تقویم / Calendar | `calendar` | Calendar Domain + Workspace | کاربران مجاز | `calendar.use` | Cycle 8 | Pending Revalidation | Gap Identified | [Calendar](../02_UI_UX/Employee/Calendar.md) | Invitation، Self Task و Assigned Action جدا هستند. |
| `PAGE-EMP-CONV-001` | گفت‌وگوها / Conversations | Route در Metadata اعلام نشده | Odoo Mail/Discuss + Workspace Adapter | کاربران مجاز گفتگو | `conversation.use` | Cycle 8 | Pending Revalidation | Not Assessed | [Conversations](../02_UI_UX/Employee/Conversations.md) | نیازمند Odoo 19 verification. |
| `PAGE-EMP-SEARCH-001` | جست‌وجوی سازمانی / Command Palette | Overlay؛ بدون Route مستقل | `cas_workspace` + Search Providers | همه کاربران دارای Search | `search.use` | Cycle 8 | Pending Revalidation | Gap Identified | [Global Search](../02_UI_UX/Employee/Global_Search.md) | `global-search-page` Superseded. |
| `PAGE-EMP-HISTORY-001` | تاریخچه اخیر / Recent History | داخل Command Palette؛ بدون Route مستقل | `cas_workspace` + Resource Resolver | کاربران مجاز | مجوز Resource؛ `history.read` حذف شده | Cycle 8 | Pending Revalidation | Gap Identified | [Recent History](../02_UI_UX/Employee/Recent_History.md) | Audit Log نیست. |
| `PAGE-EMP-NOTIF-001` | مرکز اعلان‌ها / Notification Center | `notifications-center` | Workspace View + Odoo Delivery | کاربران مجاز | `notifications.use` | Cycle 8/9 | Pending Revalidation | Not Assessed | [Notifications](../02_UI_UX/Employee/Notifications_Center.md) | نیازمند Odoo Gap Verification. |
| `PAGE-EMP-WR-001` | گزارش کار پویا / Dynamic Work Report | Route در Page Spec اعلام نشده | `cas_work_report` | Employee، Supervisor، Reviewer، Auditor با Scope | `work_report.*` | Cycle 8؛ اصلاح Cycle 9 | Pending Revalidation | Gap Identified | [Dynamic Work Report](../02_UI_UX/Employee/Dynamic_Work_Report.md) | My Report، Team Review و Delegated Monitoring. |

## ۲. تفویض و مدیریت

| Page ID | عنوان | Route | Owner | نقش‌ها | Capability | Source | UI Status | Backend Status | Spec |
|---|---|---|---|---|---|---|---|---|---|
| `PAGE-EMP-DELEGATION-MY` | تفویض‌های من / My Delegations | `/workspace/delegations` | Delegation Domain | کاربر عمومی، سرپرست، مدیر واحد برای خود | `CAP-DELEGATION-001` | Cycle 10 I3–I8 | Pending Revalidation | Gap Identified | [Delegation](../02_UI_UX/Employee/Delegation.md) |
| `PAGE-ADMIN-DELEGATION-MANAGEMENT` | مدیریت تفویض‌ها / Delegation Management | `/workspace/admin/delegations` | Delegation Governance | مدیر دارای Capability | `CAP-DELEGATION-002` | Cycle 10 I3–I8 | Pending Revalidation | Gap Identified | [Delegation](../02_UI_UX/Employee/Delegation.md) |
| `PAGE-ADMIN-DASHBOARD-MGMT-V8` | مرکز مدیریت داشبورد / Dashboard Management Center | Route در Metadata اعلام نشده | `cas_workspace` | Workspace/System Administrators | `workspace.manage_dashboard` | Cycle 8/9 | Pending Revalidation | Gap Identified | [Dashboard Management](../02_UI_UX/Admin/Dashboard_Management_Center.md) |

## ۳. دبیرخانه

| Page ID | عنوان | Route | Owner | نقش/Capability | Document Status | UI Status | Backend Status | Spec |
|---|---|---|---|---|---|---|---|---|
| `PAGE-ADM-SECRETARIAT-INCOMING` | ثبت وارده خارجی | `/workspace/secretariat/incoming` | Secretariat Registry | کاربر مجاز دبیرخانه / `CAP-SECRETARIAT-001` | Active | Pending Revalidation | Gap Identified | [Secretariat](../02_UI_UX/Administrative/Secretariat.md) |
| `PAGE-ADM-SECRETARIAT-OUTGOING` | ثبت نهایی صادره | `/workspace/secretariat/outgoing` | Secretariat Registry | `CAP-SECRETARIAT-002` | Active | Pending Revalidation | Gap Identified | همان |
| `PAGE-ADM-SECRETARIAT-REGISTER` | دفتر وارده و صادره | `/workspace/secretariat/register` | Secretariat Registry | `CAP-SECRETARIAT-003` | Active | Pending Revalidation | Gap Identified | همان |
| `PAGE-ADM-SECRETARIAT-REPORTS` | گزارش دفتر | `/workspace/secretariat/reports` | Secretariat Registry | `CAP-SECRETARIAT-004` | Active | Pending Revalidation | Gap Identified | همان |

دبیرخانه Role Title نیست؛ Access Domain است. نام و ownership نهایی ماژول هنوز Open است.

## ۴. نگهبانی و Attendance

| Page ID | عنوان | Route | Owner | نقش | Capability | Document Status | UI Status | Backend Status | Spec |
|---|---|---|---|---|---|---|---|---|---|
| `PAGE-GUARD-ATTENDANCE-STATION` | ایستگاه سریع ثبت تردد نگهبانی | `/workspace/guard/attendance` | Attendance Operations | Guard Operator | `CAP-GUARD-001`؛ زمان دستی `CAP-GUARD-002` | Active | Pending Revalidation | Gap Identified | [Guard Attendance Station](../02_UI_UX/Security/Guard_Attendance_Station.md) |

صفحه باید روی `cas.guard.batch`, `cas.guard.batch.line`, `cas.attendance.event`, `cas.attendance.site` و `action_confirm` ساخته شود و مدل موازی ایجاد نکند.

## ۵. کامپوننت‌های مشترک بدون Route

| Component/Page ID | عنوان | Owner | Consumerها | Document Status | UI Status | Backend Status | Spec |
|---|---|---|---|---|---|---|---|
| `PAGE-COMMON-PEOPLE-PICKER` | Shared People Picker | Workspace Shared Components؛ محل فنی نهایی Open | Correspondence، Delegation، Task، Workflow، Approval، Report، Form | Active | Pending Revalidation | Gap Identified | [People Picker](../02_UI_UX/Common/Shared_People_Picker.md) |

## ۶. صفحات/Surfaceهای ثبت‌شده در Decision بدون Page Specification مستقل

| Registry Key | Surface | Source Decision/Register | وضعیت مستند | Backend Status | اقدام مستندی لازم |
|---|---|---|---|---|---|
| `PAGE-PENDING-ATT-CORRECTION` | Attendance Correction Request/Ledger | Cycle 9 Register و Decision | Not Indexed as Page Spec | Gap Identified | Page Specification و Route لازم است. |
| `PAGE-PENDING-ATT-AUDIT` | Delegated Random Attendance Audit | Cycle 9 Register | Not Indexed as Page Spec | Gap Identified | Role/Capability/Page Spec لازم است. |
| `PAGE-PENDING-OVERTIME` | Overtime own/request/history/cancel | Cycle 9 Decision | Not Indexed as Page Spec | Gap Identified | Page Registry mapping و Page Spec لازم است. |
| `PAGE-PENDING-FORM-BUILDER-MATRIX` | Form Builder Activity Providers/Dynamic Matrix | Cycle 9 Decision | Not Indexed as Page Spec | Gap Identified | Page ID و Page Spec تکمیل شود. |
| `PAGE-PENDING-ADMIN-CENTER` | مدیریت کاربران، سازمان، تفویض، تنظیمات و Audit | Cycle 10 Register | Partial Page Coverage | Gap Identified | Pageهای تفصیلی و Routeها هنوز ثبت نشده‌اند. |
| `PAGE-PENDING-CORRESPONDENCE-C10` | جریان مکاتبات اصلاح‌شده Cycle 10 | Cycle 10 Register | Backlink Coverage Pending | Gap Identified | Page Specهای مکاتبات باید به Decision جدید Backlink دهند. |

## ۷. صفحات Historical/Superseded

| سند/Route | Document Status / Scope | جایگزین |
|---|---|---|
| `Employee/Workspace.md` | Historical Cycle 7 | `Workspace_V8.md` + Cycle 9/10 changes |
| `Shared/Workspace_Shell.md` | Historical Cycle 7 | `Workspace_Shell_V8.md` |
| `global-search-page` | Superseded | Command Palette |
| `recent-history` | Superseded | Recent History داخل Command Palette |
| UI لیستی ثبت نگهبانی | Superseded baseline | Guard Attendance Station Cycle 10 |
| OCR و DMS Navigation در آلفا | Out of Scope؛ implementation removal Planned | Attachment مجاز باقی می‌ماند |

## ۸. قاعده نگهداری

هر Page Specification باید Page ID، Route یا Entry، Roles، Capability، Owner، Source Cycle، Decision، Backend/UI status، Prototype reference و dependent pages را مشخص کند. Page بدون Route می‌تواند Overlay/Component باشد، اما این موضوع باید صریح اعلام شود.
