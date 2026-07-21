# Change Set — گزارش کار پویا، شیفت‌محور و مبتنی بر Form Engine

| مشخصه | مقدار |
|---|---|
| شناسه | `CS-WORK-REPORT-DYNAMIC-FORM` |
| نسخه | `Workspace v8 Iteration 12` |
| وضعیت | `Consolidated` |
| مجوز Production | پس از تکمیل API، Migration، Security و Test Strategy |
| Decisionها | `DEC-017`, `DEC-019`, `DEC-020` |

## تغییر محصولی

- Form ثابت عمومی کنار گذاشته می‌شود.
- `cas_work_report` مالک Lifecycle گزارش باقی می‌ماند.
- Form Engine ساختار تخصصی و نسخه‌دار هر Section را ارائه می‌کند.
- واحد گزارش Shift Occurrence است.
- چند Assignment در یک Shift یک Report ترکیبی می‌سازد.
- Applicability در Profile یا User Override قابل Required، Optional یا Disabled است.
- Reviewer و Access می‌توانند مستقل از رابطه زیردستی تعیین شوند.

## تغییر مدل

### Work Report

- Person/Employee
- Shift Occurrence
- Shift Snapshot
- Applicability و Source
- Workflow/Approval References
- State Projection

### Work Report Section

- Effective Assignment
- Assignment Snapshot
- Report Profile
- Form Definition/Version
- Form Submission
- Reviewer Policy
- Section Security

### Access Grant

- Grantee
- Scope
- Operations
- Validity
- Grantor/Reason
- Audit/Revocation

## تغییر UI

- Header شیفت و Applicability
- Profile Resolution Explanation
- Composite Assignment Sections
- Dynamic Form Runtime
- Evidence و Activity Catalog
- Review/Monitoring Mode
- Delegated Scope Mode
- Section-level Forbidden/Unavailable
- State و Snapshot Version

## رفتار Disabled

اگر گزارش‌دهی شخص Disabled باشد:

- Form شخصی وجود ندارد.
- Draft ساخته نمی‌شود.
- Reminder ارسال نمی‌شود.
- فقط در صورت Scope، فهرست گزارش دیگران را می‌بیند.

## دسترسی کنترل عملکرد

شخص بدون زیردست می‌تواند با Access Grant:

- همه یا بخشی از گزارش‌ها را ببیند.
- فقط Sectionها یا Fieldهای مشخص را ببیند.
- View، Comment، Audit یا Export داشته باشد.
- بدون Permission صریح Approve یا Edit نکند.

## Activity Catalog

- `cas_activity_catalog` مستقل است.
- Activity Proposal گزارش را متوقف نمی‌کند.
- Snapshot عنوان و توضیح اولیه حفظ می‌شود.
- Evidence Policy می‌تواند از Catalog Resolve شود.

## File و Document

در v8:

- Form Engine Field Contract را تعریف می‌کند.
- Odoo Attachment/Document فایل را نگهداری می‌کند.
- Work Report Evidence Relation را نگهداری می‌کند.

بازطراحی بنیادی File/Document Infrastructure خارج از دامنه v8 است.

## اثر ماژولی

- `cas_work_report`: Report، Section، Profile، Applicability، Access Grant، Projection
- Form Engine: Definition، Version، Rule، Submission، Answer، Snapshot
- `cas_organization_core`: Effective Assignment و Scope
- Shift/Attendance: Shift Occurrence و Context
- `cas_activity_catalog`: Activity و Evidence Policy
- Workflow/Approval: Process و Decision
- Workspace: UI و Provider Consumption
- Odoo Mail/Discuss/Bus: Reminder و State Notification
- Attachment/Document: File Storage

## State Ownership

- Submission State: Form Engine
- Process State: Workflow
- Approval Decision: Approval Core
- Report State: Projection در Work Report

State Machine موازی مستقل ممنوع است.

## Migration

1. شناسایی فرم و مدل ثابت.
2. Mapping رکورد قدیمی به Shift یا Legacy Period.
3. ایجاد Form Definition/Version.
4. ایجاد Report Profile و Applicability.
5. ایجاد Report و Section.
6. انتقال Answer، Evidence و Snapshot.
7. حفظ State و Audit.
8. Dual Read محدود.
9. Reconciliation.
10. Rollback Plan.

## ریسک‌ها

- Duplicate Report بدون Unique Shift Key
- Profile Conflict
- Assignment Resolution نادرست
- Snapshot قابل بازنویسی
- Stateهای متناقض
- Section Security Leakage
- Export/Attachment Leakage
- Reporting روی داده پویا
- Migration بدون Reconciliation

## تست

- Shift crossing midnight
- Idempotent Report creation
- Multi-assignment Sections
- Required/Optional/Disabled
- User Override
- Profile Conflict
- Form Version Immutability
- Append-only Revision
- Reviewer Answer Access
- Delegated Grant Scope/Expiry/Revocation
- Section/Export Security
- Workflow/Approval Projection
- Multi-company
- Migration Reconciliation
- Performance و Mobile/RTL

## مراجع

- `../04_Decisions/DEC-017-Work-Report-Domain-Uses-Form-Engine.md`
- `../04_Decisions/DEC-019-Work-Report-Applicability-And-Shift-Period.md`
- `../04_Decisions/DEC-020-Delegated-Work-Report-Access.md`
- `../05_Architecture/Work_Report_Form_Engine_Architecture.md`
- `../02_UI_UX/Employee/Dynamic_Work_Report.md`
- `../03_Modules/cas_work_report/Specification.md`
- `../03_Modules/cas_work_report/Security.md`