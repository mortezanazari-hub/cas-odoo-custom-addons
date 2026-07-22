---
document_id: REG-CAP-001
title: CAS Capability Registry
document_type: Capability Registry
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Security & Architecture Governance
domain_owner: Capability Governance
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

# رجیستری مرکزی Capabilityهای CAS

Capability برای Navigation و فعال‌سازی تجربه کاربری است و جای ACL، Record Rule، Method Check، Scope Resolver یا Field/Section Security را نمی‌گیرد.

## ۱. Workspace، Search و Dashboard

| Capability ID | نام فنی/مترادف | مالک | Provider/Consumer | صفحات | وضعیت اجرا | مرجع Canonical | محدودیت امنیتی |
|---|---|---|---|---|---|---|---|
| `CAP-WORKSPACE-001` | `workspace.use` / استفاده از میزکار | Workspace | `cas_workspace` / همه نقش‌ها | Workspace Shell/Home | Gap Identified | [Capability Model](../05_Architecture/Capability_And_Security_Model.md) | Direct route همچنان Backend check دارد. |
| `CAP-WORKSPACE-002` | `workspace.manage_dashboard` | Workspace Governance | Workspace / Dashboard Admin | Dashboard Management Center | Gap Identified | Capability Model + `DEC-V8-018-DASHBOARD-GOVERNANCE` | Company Policy و SoD. |
| `CAP-WORKSPACE-003` | `workspace.publish_dashboard` | Workspace Governance | Workspace | Dashboard Management Center | Gap Identified | Capability Model | Publish/Rollback باید Audit شود. |
| `CAP-WORKSPACE-004` | `workspace.audit_dashboard` | Workspace Governance | Workspace/Audit | Dashboard audit | Gap Identified | Capability Model | Read-only audit viewer. |
| `CAP-SEARCH-001` | `search.use` / جست‌وجوی سازمانی / Command Palette | Workspace | Search Providers | Command Palette | Gap Identified | [Search Contract](../05_Architecture/V8-Search-History-And-Scroll-Contracts.md) | Search مجوز Resource ایجاد نمی‌کند؛ count/metadata leakage ممنوع. |

## ۲. Personal Task، Calendar، Conversation و Notification

| Capability ID | نام فنی | مالک | صفحات/مصرف‌کننده | وضعیت اجرا | مرجع |
|---|---|---|---|---|---|
| `CAP-PERSONAL-TASK-001` | `personal_task.use` | `cas_personal_task` | Personal Tasks، Calendar Self Task | Gap Identified | Capability Model |
| `CAP-PERSONAL-TASK-002` | `personal_task.manage_categories` | `cas_personal_task` | Personal Task settings | Gap Identified | `DEC-V8-012-PERSONAL-TASK-CATEGORIES` |
| `CAP-CALENDAR-001` | `calendar.use` | Calendar Domain | Calendar | Gap Identified | Capability Model |
| `CAP-CALENDAR-002` | `calendar.invite` | Calendar Domain | Attendee Picker | Gap Identified | `DEC-V8-013-CALENDAR-AUTH` |
| `CAP-CALENDAR-003` | `calendar.assign_action` | Action Hub + Calendar Bridge | Calendar → Organizational Action | Gap Identified | `DEC-V8-013-CALENDAR-AUTH` |
| `CAP-CONVERSATION-001` | `conversation.use` | Odoo Mail/Discuss | Conversations | Not Assessed | `DEC-V8-014-DISCUSS-REUSE` |
| `CAP-NOTIFICATION-001` | `notifications.use` | Workspace View + Odoo Delivery | Notification Center | Not Assessed | Capability Model |

## ۳. گزارش کار

نام‌های زیر در Security Specification «مفهومی» هستند و نام فنی نهایی باید در Security Implementation تثبیت شود.

| Capability ID | نام فنی | عملیات | وضعیت اجرا | مرجع |
|---|---|---|---|---|
| `CAP-WORK-REPORT-001` | `work_report.use` | ورود به دامنه گزارش کار | Gap Identified | [Work Report Security](../03_Modules/cas_work_report/Security.md) |
| `CAP-WORK-REPORT-002` | `work_report.view_own` | مشاهده گزارش خود | Gap Identified | همان |
| `CAP-WORK-REPORT-003` | `work_report.edit_own_draft` | ویرایش پیش‌نویس خود | Gap Identified | همان |
| `CAP-WORK-REPORT-004` | `work_report.submit_own` | ارسال گزارش خود | Gap Identified | همان |
| `CAP-WORK-REPORT-005` | `work_report.view_scope` | مشاهده Scope مجاز | Gap Identified | همان |
| `CAP-WORK-REPORT-006` | `work_report.comment` | Comment | Gap Identified | همان |
| `CAP-WORK-REPORT-007` | `work_report.review` | Review | Gap Identified | همان |
| `CAP-WORK-REPORT-008` | `work_report.request_correction` | درخواست اصلاح | Gap Identified | همان |
| `CAP-WORK-REPORT-009` | `work_report.return` | بازگرداندن | Gap Identified | همان |
| `CAP-WORK-REPORT-010` | `work_report.approve` | تأیید | Gap Identified | همان |
| `CAP-WORK-REPORT-011` | `work_report.export` | Export | Gap Identified | همان |
| `CAP-WORK-REPORT-012` | `work_report.audit` | ممیزی | Gap Identified | همان |
| `CAP-WORK-REPORT-013` | `work_report.manage_profiles` | مدیریت Profile | Gap Identified | همان |
| `CAP-WORK-REPORT-014` | `work_report.manage_access_grants` | مدیریت تفویض دسترسی | Gap Identified | همان |

## ۴. اضافه‌کاری

| Capability ID | نام فنی | مالک | وضعیت اجرا | مرجع |
|---|---|---|---|---|
| `CAP-OVERTIME-001` | `overtime.view_own` | Overtime Domain | Gap Identified | [`DEC-UIR09-010-CONSOLIDATED`](Decision_Registry.md#۳-تصمیمهای-تجمیعی-cycle-9-و-cycle-10) |
| `CAP-OVERTIME-002` | `overtime.request` | Overtime Domain | Gap Identified | همان |
| `CAP-OVERTIME-003` | `overtime.view_history` | Overtime Domain | Gap Identified | همان |
| `CAP-OVERTIME-004` | `overtime.cancel_request` | Overtime Domain | Gap Identified | همان |

## ۵. تفویض اختیار Cycle 10

شناسه فنی نهایی Capabilityهای تفویض هنوز در Module/Security Specification تثبیت نشده است. تا آن زمان Registry Key زیر برای Traceability استفاده می‌شود.

| Capability ID | عنوان/مترادف | Domain Owner | عملیات/Scope | صفحات | وضعیت | مرجع |
|---|---|---|---|---|---|---|
| `CAP-DELEGATION-001` | ایجاد تفویض برای خود / My Delegations | Delegation Domain | ساخت، مشاهده، لغو در Scope خود | `/workspace/delegations` | Gap Identified | [Delegation Page](../02_UI_UX/Employee/Delegation.md) |
| `CAP-DELEGATION-002` | مدیریت تفویض سازمانی | Delegation Governance | ایجاد برای دیگران، suspend/revoke/replace | `/workspace/admin/delegations` | Gap Identified | Delegation Page |
| `CAP-DELEGATION-003` | مشاهده Audit تفویض | Audit Governance | read-only audit | Admin/Audit | Gap Identified | Cycle 10 Decision |
| `CAP-DELEGATION-004` | عملیات تفویض مکاتبات | Correspondence Provider | عملیات Provider-specific | Correspondence | Gap Identified | Cycle 10 Decision |
| `CAP-DELEGATION-005` | عملیات تفویض Task/Action | Action Provider | عملیات Provider-specific | Action Hub | Gap Identified | Cycle 10 Decision |
| `CAP-DELEGATION-006` | عملیات تفویض Approval/Request | Approval Provider | عملیات حساس مستقل | Approval/Request | Gap Identified | Cycle 10 Decision |
| `CAP-DELEGATION-007` | عملیات تفویض گزارش کار | Work Report Provider | view/edit/submit/review/approve طبق اختیار | Work Report | Gap Identified | Delegation Page + Work Report Security |

## ۶. مدیریت سامانه

| Capability ID | عنوان | گروه/مالک | وضعیت | محدودیت |
|---|---|---|---|---|
| `CAP-ADMIN-001` | مدیریت کاربران و دسترسی | Security Governance | Gap Identified | عنوان شغلی دسترسی ایجاد نمی‌کند. |
| `CAP-ADMIN-002` | مدیریت سازمان | Organization Governance | Gap Identified | Scope و SoD. |
| `CAP-ADMIN-003` | مدیریت تفویض | Delegation Governance | Gap Identified | privilege escalation ممنوع. |
| `CAP-ADMIN-004` | مدیریت تنظیمات | Settings Governance | Gap Identified | Audit اجباری. |
| `CAP-ADMIN-005` | مشاهده Audit | Audit Governance | Gap Identified | read-only. |
| `CAP-ADMIN-006` | مدیر ارشد تجمیعی | Security Governance | Gap Identified | Composite role از گروه‌های مصوب؛ گروه مطلق مستقل نیست. |

## ۷. دبیرخانه

| Capability ID | عنوان | عملیات | وضعیت | مرجع |
|---|---|---|---|---|
| `CAP-SECRETARIAT-001` | ثبت وارده خارجی | incoming register | Gap Identified | [Secretariat Page](../02_UI_UX/Administrative/Secretariat.md) |
| `CAP-SECRETARIAT-002` | ثبت نهایی صادره | outgoing final registry | Gap Identified | همان |
| `CAP-SECRETARIAT-003` | مشاهده دفتر | register view | Gap Identified | همان |
| `CAP-SECRETARIAT-004` | گزارش و Export دفتر | report/export | Gap Identified | همان |
| `CAP-SECRETARIAT-005` | اصلاح رسمی رکورد | correction ledger | Gap Identified | همان |

نام فنی نهایی این Capabilityها پس از تعیین ownership و نام نهایی ماژول دبیرخانه ثبت می‌شود.

## ۸. نگهبانی و Attendance Operations

| Capability ID | عنوان | عملیات | وضعیت | مرجع |
|---|---|---|---|---|
| `CAP-GUARD-001` | استفاده از ایستگاه ثبت تردد | view/search/select/confirm batch | Gap Identified | [Guard Attendance Station](../02_UI_UX/Security/Guard_Attendance_Station.md) |
| `CAP-GUARD-002` | تغییر زمان رخداد | manual occurred time + reason | Gap Identified | همان |
| `CAP-GUARD-003` | عبور مجاز از Conflict | acknowledge/override with reason | Gap Identified | همان |
| `CAP-GUARD-004` | اصلاح رسمی رخداد | void/replacement/reopen | Gap Identified | Attendance Core، نه صفحه ثبت عادی |

## ۹. Alias و جست‌وجو

| عبارت فارسی/انگلیسی | Capability/Domain |
|---|---|
| تفویض اختیار، نمایندگی، Delegation، Access Grant | `CAP-DELEGATION-*` و `work_report.manage_access_grants` |
| دبیرخانه، وارده، صادره، Secretariat Registry | `CAP-SECRETARIAT-*` |
| نگهبانی، ثبت ورود و خروج، Guard Attendance | `CAP-GUARD-*` |
| جست‌وجوی سراسری، Global Search، Command Palette | `search.use` |
| مدیریت میزکار، Dashboard Administration | `workspace.manage_dashboard` |
| گزارش کار، گزارش شیفت، Work Report | `work_report.*` |

## ۱۰. قاعده نگهداری

هر Capability جدید باید Owner، Provider، Consumer، Page، Method Check، Scope، Audit و Status داشته باشد. Capability بدون Backend enforcement فقط یک نشانه UX است و نباید به‌عنوان کنترل امنیتی معرفی شود.
