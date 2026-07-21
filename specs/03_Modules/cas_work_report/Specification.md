# Module Specification — `cas_work_report`

| مشخصه | مقدار |
|---|---|
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Consolidated` |
| وضعیت اجرا | `Needs API/Migration/Test Completion` |
| مالک دامنه | Work Report Lifecycle |
| Decisionها | `DEC-017`, `DEC-019`, `DEC-020` |

## هدف

`cas_work_report` مالک گزارش کار هر شخص در هر Shift Occurrence است. ساختار محتوای گزارش از Form Engine، Assignmentها از Organization Core و مسیر فرایند از Workflow/Approval دریافت می‌شود.

## واحد یکتای گزارش

```text
employee/user + shift_occurrence = maximum one work_report
```

- شیفت عبوری از نیمه‌شب یک گزارش واحد است.
- گزارش صرفاً براساس تاریخ تقویمی شکسته نمی‌شود.
- ایجاد Draft باید Idempotent باشد.
- در نبود Shift Occurrence معتبر، Policy صریح لازم است و سیستم نباید Shift خیالی بسازد.

## Applicability

وضعیت گزارش‌دهی:

- `required`
- `optional`
- `disabled`

Resolution:

```text
Company Default
→ Report Profile / Job / Assignment Policy
→ User Override
```

در `disabled`:

- Form شخصی نمایش داده نمی‌شود.
- Draft ساخته نمی‌شود.
- Reminder ارسال نمی‌شود.
- مسیر «گزارش من» مخفی است.
- Scope مشاهده گزارش دیگران مستقل باقی می‌ماند.

## گزارش چند Assignment

یک Work Report دارای اطلاعات مشترک و یک یا چند Section است:

```text
Work Report
├── Report Header / Shift Context
├── Assignment Section A
├── Assignment Section B
└── Overall Summary
```

هر Section به یک Effective Assignment متصل است و می‌تواند داشته باشد:

- Report Profile
- Form Definition/Version
- Reviewer Policy
- Evidence Policy
- Activity Scope
- KPI Mapping
- Weight
- Visibility Classification

## مدل‌های مفهومی

### Work Report

- employee/user
- company
- shift occurrence reference
- shift start/end snapshot
- applicability source
- state projection
- submitted/reviewed/approved timestamps
- overall summary
- active

### Work Report Section

- report
- effective assignment reference
- assignment snapshot
- report profile
- form definition/version
- form submission
- reviewer policy
- section state projection
- confidentiality level
- sequence

### Report Profile

- name/code
- company/job/assignment scope
- applicability
- form resolver policy
- reviewer resolver policy
- workflow/approval references
- evidence defaults
- activity catalog scope
- validity period

### Work Report Access Grant

- grantee user/role
- scope type and values
- report/profile/assignment/section filters
- allowed operations
- valid from/to
- grantor
- reason
- status
- revoked metadata

### Evidence Relation

- report/section/activity reference
- attachment/document reference
- evidence type
- required/optional source
- added by/at
- validation state

## Form Engine Integration

Form Engine مالک:

- Form Definition
- Form Version
- Field/Section Schema
- Conditional Logic
- Validation
- Answer
- Technical Submission Snapshot

Work Report مالک:

- گزارش و Shift Context
- Section و Assignment Relation
- Applicability
- Reviewer/Access Scope
- Evidence Semantics
- User-facing State Projection

Form Version در زمان ایجاد Section Pin می‌شود. انتشار Version جدید نباید گزارش تاریخی را تغییر دهد.

## State Ownership

- Form Submission State: Form Engine
- Process State: Workflow Core
- Approval Decision: Approval Core
- Report State: Projection قابل‌فهم از منابع فوق

تغییر مستقیم Report State بدون Service هماهنگ‌کننده ممنوع است.

## Lifecycle مفهومی

حداقل UX Stateها:

- draft
- submitted
- returned
- under_review
- approved
- locked
- cancelled، در صورت Policy

Mapping دقیق به Workflow و Approval در API/State Contract نهایی می‌شود.

## Reviewer Resolution

Reviewer فقط مدیر مستقیم نیست. منابع:

1. Report Profile
2. Effective Assignment / Organization Scope
3. Explicit Reviewer Assignment
4. Delegated Access Grant
5. Control/Audit Role

Resolution باید Explainable باشد و Source هر Reviewer را ثبت کند.

## دسترسی تفویض‌شده

Access Grant می‌تواند Scope را بر این اساس محدود کند:

- Company
- Organization Unit
- Job/Role
- Person
- Report Profile
- Assignment Type
- Specific Assignment
- Section Type یا Section ID
- Date/Shift Range

عملیات مستقل:

- view
- comment
- review
- request_correction
- return
- approve
- export
- audit

View به معنی Approve نیست.

## نمونه مسئول کنترل عملکرد

فرد می‌تواند بدون زیردست:

- گزارش‌های تمام یا بخشی از سازمان را ببیند.
- فقط Summary، KPI، Error یا Evidence را ببیند.
- Comment، Audit یا Export داشته باشد.
- بدون Permission صریح Approve یا Edit نکند.

## Activity Catalog

- فعالیت استاندارد از `cas_activity_catalog` انتخاب می‌شود.
- Activity Proposal گزارش را متوقف نمی‌کند.
- عنوان و توضیح اولیه کاربر Snapshot می‌شوند.
- Mapping بعدی تاریخچه را بازنویسی نمی‌کند.

## Evidence و File

در v8:

- Form Engine Field Type و Validation را تعریف می‌کند.
- Odoo Attachment/Document فایل واقعی را نگهداری می‌کند.
- Work Report Relation و Policy معنایی Evidence را نگه می‌دارد.

بازطراحی File/Document Infrastructure خارج از Scope v8 است.

## Context Providerها

Contextهای محتمل:

- Employee
- Company
- Effective Assignments
- Shift
- Attendance Summary
- Calendar/Action References
- Organization Unit
- Reviewer Candidates

Context Snapshot گزارش باید برای Audit حفظ شود.

## Reporting Projection

برای گزارش‌گیری روی داده پویا باید Projection تعریف شود:

- reportable field key
- typed value
- report/section/profile/form version
- effective date
- security classification
- index strategy

Export مستقیم از فیلدهای قدیمی ثابت مرجع آینده نیست.

## Notification

Reminder، Submit، Return و Approval از زیرساخت Odoo Notification استفاده می‌کنند. CAS فقط Metadata، Deep Link و Action Contract لازم را اضافه می‌کند.

## API مفهومی

- resolve applicability
- get or create report for shift
- resolve sections
- save draft
- submit report
- return/request correction
- review/approve through workflow services
- resolve authorized reports
- create/revoke access grant
- export authorized projection
- explain access/reviewer/profile resolution

## Migration

Migration از مدل ثابت باید شامل این موارد باشد:

- Mapping گزارش قدیمی به Shift Occurrence یا Legacy Period
- ساخت Section و Form Submission
- Pin کردن Form Version
- انتقال Evidence Reference
- حفظ State و Audit
- Dual Read محدود و زمان‌دار
- Validation Report
- Rollback Plan

## Test Strategy

- Shift crossing midnight
- Idempotent draft creation
- Multiple assignments in one report
- Applicability disabled
- User override
- Reviewer resolution
- Access Grant scope and expiry
- Section-level visibility
- Form version immutability
- Workflow/Approval projection
- Cross-company isolation
- Export authorization
- Migration reconciliation
- Performance روی داده پویا

## معیار پذیرش

1. هر Shift Occurrence حداکثر یک گزارش داشته باشد.
2. چند Assignment یک گزارش ترکیبی بسازند.
3. `disabled` هیچ Form یا Draft نسازد.
4. فرد بدون زیردست بتواند با Access Grant گزارش مجاز را ببیند.
5. Section غیرمجاز از RPC و Export نیز مخفی باشد.
6. تغییر Form Version گزارش تاریخی را تغییر ندهد.
7. Stateهای Form، Workflow، Approval و Report متناقض نشوند.
8. Workspace مالک هیچ داده Report نباشد.