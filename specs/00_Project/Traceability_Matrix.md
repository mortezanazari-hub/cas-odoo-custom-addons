# ماتریس ردیابی CAS Workspace v8

| مشخصه | مقدار |
|---|---|
| شناسه | `TRACE-CAS-V8` |
| نسخه | `v8 through iteration 12` |
| وضعیت | `Consolidated` |

این ماتریس مسیر Requirement تا تصمیم، صفحه، معماری و ماژول مالک را ثبت می‌کند. ستون‌های API، Migration و Test با تکمیل Specification اجرایی هر ماژول دقیق‌تر می‌شوند.

| Requirement | Decision | Page / Flow | Architecture | مالک | Provider / Integration | وضعیت |
|---|---|---|---|---|---|---|
| Workspace عملیاتی و Action-First | `DEC-001` | Workspace Home | Workspace Architecture | `cas_workspace` | Providerها | Agreed |
| عدم نمایش SLA فنی به کاربر عادی | `DEC-002` | Workspace, Actions | UX Principles | Provider مالک Deadline | Workspace Renderer | Agreed |
| فرهنگ فعالیت استاندارد و Snapshot | `DEC-003` | Work Report | Domain Model | `cas_activity_catalog` | `cas_work_report` | Agreed |
| Widget System | `DEC-004` | Workspace | Dashboard Configuration | `cas_workspace` | Widget Providers | Agreed |
| Conversations سطح اول | `DEC-005`, `DEC-014` | Conversations | Integration Map | Odoo Mail/Discuss | Workspace Discuss Adapter | Agreed |
| Theme و خوانایی | `DEC-006` | Shared Shell | Design Tokens | `cas_workspace` | Company Policy | Agreed |
| Sidebar پایدار | `DEC-007` | Shared Shell | Workspace Architecture | `cas_workspace` | — | Agreed |
| Calendar تعاملی | `DEC-008`, `DEC-013` | Calendar | Assignment Model | Calendar Integration | Organization Scope, Action Hub | Agreed |
| Route و Capability | `DEC-009`, `DEC-016` | Shell, Search | Capability Model | `cas_workspace` | Provider Permission | Partially Superseded by v8 |
| Provider Registry | `DEC-010` | همه صفحات تجمیعی | Provider Architecture | `cas_workspace_contract` | تمام Providerها | Agreed |
| تفکیک Task/Action/Notification/History | `DEC-011` | Tasks, Actions, Notifications | Domain Model | مالکان دامنه | Workspace Orchestration | Agreed |
| دسته‌های Personal Task | `DEC-012` | Personal Tasks | Domain Model | `cas_personal_task` | Workspace Provider | Agreed |
| Attendee و Assignment Authorization | `DEC-013` | Calendar | Assignment Model | Calendar / Action Hub | `cas_organization_core` | Agreed |
| Reuse Discuss | `DEC-014` | Conversations | Integration Map | Odoo Mail/Discuss/Bus | CAS Adapter | Agreed |
| Overlay و Focus | `DEC-015` | Shell و Modalها | Interaction Contract | Odoo UI Services + Workspace Shell | همه صفحات | Agreed |
| Search/History Consolidation | `DEC-016` | Command Palette | Search/History Contract | `cas_workspace` | Search Providers | Agreed |
| Work Report از Form Engine | `DEC-017` | Dynamic Work Report | Work Report Architecture | `cas_work_report` | Form/Workflow/Approval | Agreed |
| Dashboard Admin Center | `DEC-018` | Admin Dashboard Management | Dashboard Architecture | `cas_workspace` | Widget Providers | Agreed |
| Shift-based Report Applicability | `DEC-019` | Dynamic Work Report | Assignment Model | `cas_work_report` | Shift/Attendance, Profile Resolver | Agreed |
| Delegated Report Access | `DEC-020` | Report Review | Capability & Security Model | `cas_work_report` | Organization Core | Agreed |
| Personal Task مالک مستقل | Baseline v8 | Personal Tasks | Module Boundaries | `cas_personal_task` | Workspace | Agreed |
| Organization Scope مشترک | Baseline v8 | Calendar, Reports, Actions | Assignment Model | `cas_organization_core` | HR / Employee | Agreed |
| Notification Center با Reuse Odoo | Baseline v8 | Notifications Center | Notification Gap Analysis | Odoo + CAS Extension | Mail/Discuss/Bus | Needs Gap Analysis |
| یک گزارش ترکیبی چند Assignment | `DEC-019` | Dynamic Work Report | Work Report Architecture | `cas_work_report` | Form Engine | Agreed |
| Activity Catalog مستقل | `DEC-003` | Work Report / Quick Activity | Domain Model | `cas_activity_catalog` | KPI, Work Report | Agreed |
| File/Document Redesign آینده | Baseline v8 | Evidence Fields | Integration Map | Odoo Attachment فعلی | Document Core | Out of Scope v8 |

## ردیابی اسناد اجرایی

برای هر ماژول باید ردیف‌های زیر به این ماتریس افزوده شوند:

- API Contract
- ACL و Record Rule
- Method Check
- Migration Script
- Python Tests
- JS/HOOT Tests
- Tour / End-to-End Tests
- Acceptance Criteria
- Rollback Plan

## قانون تکمیل

هیچ ردیفی فقط با وضعیت محصولی `Agreed`، مجوز پیاده‌سازی Production نیست. وضعیت نهایی هر ماژول باید از Specification و Test Strategy همان ماژول استخراج شود.