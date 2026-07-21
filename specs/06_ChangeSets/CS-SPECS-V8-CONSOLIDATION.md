# Change Set — Consolidation کامل Specificationهای Workspace v8

| مشخصه | مقدار |
|---|---|
| شناسه | `CS-SPECS-V8-CONSOLIDATION` |
| Baseline | Workspace v8 تا Iteration 11 + Dynamic Work Report Iteration 12 |
| Target | `CAS UI Workspace v8 — Through Iteration 12` |
| وضعیت | `Consolidated` |
| تاریخ | `2026-07-21` |

## هدف

یکپارچه‌کردن پوشه `specs` بر پایه نسخه ۸ بدون مقایسه یا کاهش دامنه براساس ماژول‌های فعلی.

## تصمیم‌های تثبیت‌شده

- Iteration 12 جزو نسخه رسمی v8 است.
- v7 Historical است و در محل فعلی می‌ماند.
- Workspace فقط مالک UI Configuration و Preference است.
- Personal Task مالک مستقل دارد.
- Self Task در Personal Task و Task برای دیگری در Action Hub است.
- Odoo Notification Reuse می‌شود و Extension فقط Gap-driven است.
- Recent History ماژول یا Route مستقل ندارد.
- Provider Contract در لایه مشترک تعریف می‌شود.
- Organization Scope در `cas_organization_core` متمرکز است.
- `search.use` فقط مجوز ابزار Search است.
- Notification Center مستقل باقی می‌ماند.
- Overlay از Odoo UI Services استفاده می‌کند.
- Preference Resolution و Company Lock تعیین شده است.
- Dashboard Management Center برای ادمین افزوده شده است.
- Multi-assignment یک گزارش ترکیبی با Sectionهای مجزا می‌سازد.
- واحد گزارش Shift Occurrence است.
- File/Document Redesign خارج از v8 است.
- Activity Catalog مستقل است.
- Report Applicability قابل Required/Optional/Disabled است.
- Report Access مستقل از زیردستی قابل تفویض است.

## اسناد جدید

### Project

- `V8_Canonical_Baseline.md`
- `Documentation_Governance.md`
- `Traceability_Matrix.md`
- `Open_Questions.md`

### Product

- `Terminology.md`

### UI/UX

- `Employee/Workspace_V8.md`
- `Shared/Workspace_Shell_V8.md`
- `Admin/Dashboard_Management_Center.md`

### Modules

- `V8_Module_Ownership_Map.md`
- `V8_Dependency_Map.md`
- `V8_Provider_Registry.md`
- Specificationهای Workspace، Personal Task، Organization Core، Activity Catalog و Work Report
- Security مستقل Work Report

### Decisions

- `DEC-001`, `DEC-002`, `DEC-003`
- `DEC-018`, `DEC-019`, `DEC-020`

### Architecture

- System Context
- Domain Model
- Module Boundaries
- Data Flow
- Integration Map
- Assignment Model
- Capability and Security Model
- Provider Architecture
- Dashboard Configuration Architecture
- Odoo Notification Gap Analysis

## اسناد به‌روزشده

- Root README
- Project README و Version History
- Product README و UX Principles
- UI/UX Index
- Modules Index
- Decisions Index
- Architecture Index
- Change Sets Index
- Module Aggregation Matrix

## اسناد Historical یا Partially Superseded

- Page و Shell نسخه ۷
- Module Impactهای v7
- `DEC-009` در بخش Routeهای Search و History
- Routeهای `global-search-page` و `recent-history`
- Capability مستقل `history.read`
- پیشنهاد ماژول مستقل `cas_recent_history`
- پیشنهاد ساخت Notification Core کامل بدون Gap Analysis

## اثر ماژولی

### ماژول‌های جدید یا تفکیک‌شده

- `cas_workspace_contract`
- `cas_personal_task`
- `cas_organization_core`
- `cas_activity_catalog`

### ماژول‌های نیازمند بازطراحی

- `cas_workspace`
- `cas_work_report`
- Form Engine modules
- Calendar Integration
- Action Hub Integration
- Discuss/Notification Adapter

## Migrationهای آینده

- Route و Navigation
- Dashboard Preference
- Personal Task Ownership
- Static-to-dynamic Work Report
- Form Snapshot Revision
- Reviewer/Form Answer Security
- Provider Keys و Deep Links

## ریسک‌ها

- Circular Dependency در صورت ثبت Provider داخل Workspace UI Module
- State Machineهای موازی در Form/Workflow/Approval/Report
- Security Leakage در Search، Section و Export
- Duplicate Work Report بدون Shift Unique Key
- Notification System موازی
- Snapshot تاریخی قابل بازنویسی

## خروجی مورد انتظار

پس از این Change Set، هر استناد جدید باید از Canonical Baseline و Indexهای v8 شروع شود. اسناد تاریخی برای منشأ تصمیم قابل استفاده‌اند، اما مرجع کاهش نسخه ۸ نیستند.