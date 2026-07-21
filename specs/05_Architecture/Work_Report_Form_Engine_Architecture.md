# معماری جامع گزارش کار مبتنی بر Form Engine

| مشخصه | مقدار |
|---|---|
| وضعیت | `Consolidated` |
| نسخه | `Workspace v8 through iteration 12` |
| تصمیم‌های مرجع | `DEC-017`, `DEC-019`, `DEC-020` |
| دامنه | Work Report, Form Engine, Workflow, Approval, Organization, Shift, Activity, Evidence |

## ۱. هدف

ایجاد یک دامنه واحد Work Report که Lifecycle، Review، Approval و Reporting را یکپارچه نگه دارد، در حالی که هر Assignment بتواند Form تخصصی و نسخه‌دار خود را در یک گزارش ترکیبی داشته باشد.

## ۲. Invariant اصلی

```text
هر Person/Employee + هر Shift Occurrence = حداکثر یک Work Report
```

- Shift عبوری از نیمه‌شب یک Report است.
- ایجاد Report و Draft باید Idempotent باشد.
- چند Assignment هم‌زمان یک Report با چند Section می‌سازد.
- Policy `multiple_reports` برای Assignmentهای یک Shift در Baseline v8 پذیرفته نیست.

## ۳. مرز مالکیت

### Form Engine

- Form Definition و Version
- Section/Field/Rule/Validation
- Conditional Logic
- Submission و Answer
- Technical Snapshot/Revision
- Runtime Contract
- File/Evidence Field Contract

### `cas_work_report`

- Work Report Identity و Shift Relation
- Work Report Section
- Report Profile و Applicability
- Assignment/Form Version Pinning
- Reviewer Resolution
- Access Grant
- Evidence Semantics
- Attendance Reconciliation
- Reporting Projection
- UX State Projection

### `cas_organization_core`

- Effective Assignment
- Organization Scope
- Reporting Relationship
- Delegation سازمانی
- Reviewer Candidate پایه

### Shift/Attendance

- Shift Occurrence
- planned/actual context
- attendance summary
- mismatch data

### Workflow Core

- Process Definition/Instance
- Transition و Process State

### Approval Core

- Approval Request
- Decision
- Approver Authority

### Activity Catalog

- Activity Definition
- Proposal
- Evidence Policy Reference
- KPI Mapping Reference

### Odoo Attachment/Document

- File Binary و Storage
- File Permission پایه

### Workspace

- Route، Shell و Dynamic Renderer
- Profile Explanation UI
- Review/Monitoring Entry Point
- مالک هیچ داده Report نیست

## ۴. مدل مفهومی

### Work Report

```text
employee_id
company_id
shift_occurrence_ref
shift_start_snapshot
shift_end_snapshot
timezone_snapshot
applicability
applicability_source
state_projection
workflow_instance_id
approval_instance_id
submitted_at
reviewed_at
approved_at
locked_at
overall_summary
```

Unique Constraint مفهومی:

```text
(employee_id, shift_occurrence_ref)
```

### Work Report Section

```text
report_id
assignment_ref
assignment_snapshot
report_profile_id
form_definition_id
form_version_id
submission_id
reviewer_policy
section_state_projection
confidentiality_level
sequence
```

### Report Profile

```text
name/code
company/job/assignment scope
applicability
form resolver policy
reviewer resolver policy
workflow/approval references
evidence defaults
activity catalog scope
priority
effective_from/effective_to
active
```

### Work Report Access Grant

```text
grantee
scope_type/scope_values
report/profile/assignment/section filters
operations
valid_from/valid_to
grantor
reason
status
revoked_at/revoked_by
```

### Reporting Projection

```text
report_id
section_id
profile_id
form_version_id
metric_key
typed value fields
source_field_key
security_classification
effective_datetime
```

## ۵. Applicability Resolver

Resolution:

```text
Company Default
→ Job/Report Profile
→ Assignment-specific Policy
→ Authorized User Override
```

Values:

- `required`
- `optional`
- `disabled`

در `disabled`:

- Report/Draft شخصی ساخته نمی‌شود.
- Form شخصی نمایش داده نمی‌شود.
- Reminder ارسال نمی‌شود.
- Review/Monitoring دیگران مستقل باقی می‌ماند.

## ۶. Assignment و Section Resolver

1. دریافت Shift Occurrence و Effective Datetime.
2. Resolve تمام Assignmentهای مؤثر شخص.
3. Resolve Profile برای هر Assignment.
4. تشخیص Profile Conflict.
5. Pin Form Version منتشرشده.
6. ساخت یا Reconcile Sectionها.
7. ثبت دلیل Resolution و Snapshot.

ترتیب Specificity پیشنهادی:

```text
assignment exact
> position/job exact
> organization unit exact
> role/profile
> company default
```

در تعارض هم‌امتیاز، سیستم Form تصادفی انتخاب نمی‌کند و Configuration Error نشان می‌دهد.

## ۷. قرارداد ایجاد Report

```text
open_report_for_shift(employee, shift_occurrence)
  → resolve applicability
  → if disabled: return no_personal_report
  → get-or-create report idempotently
  → resolve effective assignments
  → resolve section profiles and form versions
  → create/link submissions
  → hydrate context snapshots
  → resolve permissions/reviewers
  → return composite render contract
```

## ۸. Render Contract مفهومی

```json
{
  "report": {
    "id": 501,
    "shift_occurrence": "SHIFT-2026-07-21-N1",
    "state": "draft",
    "applicability": "required"
  },
  "context": {
    "employee": {},
    "shift": {},
    "attendance": {},
    "resolution_explanation": {}
  },
  "sections": [
    {
      "assignment": {},
      "profile": {},
      "form": {"definition_id": 8, "version_id": 31, "schema": {}},
      "permissions": {},
      "review": {}
    }
  ],
  "permissions": {"submit": true, "export": false}
}
```

شناسه‌های Employee، Assignment، Profile و Form Version از Client قابل تحمیل نیستند و Server دوباره Resolve می‌کند.

## ۹. Snapshot و Revision

- Report به Shift و Assignment Snapshot متصل است.
- هر Section Form Version مشخص دارد.
- Label، Option، Rule و Activity Context مؤثر Snapshot می‌شوند.
- Return/Reopen Snapshot قبلی را پاک نمی‌کند.
- Revision جدید Append-only و قابل Audit است.
- گزارش تاریخی با Version جدید Revalidate یا Rewrite نمی‌شود، مگر Migration رسمی با Audit.

## ۱۰. Validation

### Form Validation

- Required
- Regex/Range/Type
- Conditional Logic
- Formula امن
- Evidence Field Rule

### Domain Validation

- Duplicate Report
- Valid Shift
- Applicability
- Effective Assignment
- Allowed Reporter
- Evidence Policy
- Workflow Preconditions
- Lock State
- Section Completeness

## ۱۱. State Ownership

| مفهوم | مالک |
|---|---|
| Submission State | Form Engine |
| Process State | Workflow Core |
| Approval Decision | Approval Core |
| Report/Section UX State | Projection در Work Report |

Work Report State مستقل و دستی نباید با منابع بالا متناقض شود.

UX Stateهای نمونه:

- draft
- submitted
- returned
- under_review
- approved
- locked

Mapping نهایی در State/API Contract تدوین می‌شود.

## ۱۲. Reviewer و Access

Reviewer فقط Manager مستقیم نیست.

منابع دسترسی:

- Owner
- Organization Scope
- Reviewer/Approver Assignment
- Access Grant
- Control/Audit Role

Access Grant Scope:

- Company
- Unit
- Job/Role
- Person
- Profile
- Assignment
- Report
- Section
- Date/Shift Range

Operationها:

- view
- comment
- review
- request_correction
- return
- approve
- export
- audit

Section غیرمجاز به Client یا Export ارسال نمی‌شود.

## ۱۳. Form Answer Security

دسترسی Reviewer به Report باید به Submission و Answerهای همان Section گسترش یابد، نه تمام Form Submissionها.

Rule باید از رابطه معتبر زیر مشتق شود:

```text
Authorized Work Report
→ Authorized Section
→ Linked Form Submission/Answers
```

## ۱۴. Activity و Evidence

- Activity از `cas_activity_catalog` Resolve می‌شود.
- Proposal گزارش را متوقف نمی‌کند.
- عنوان و توضیح اولیه Snapshot می‌شوند.
- Form Engine نوع Evidence Field را تعریف می‌کند.
- Odoo Attachment/Document فایل را ذخیره می‌کند.
- Work Report Relation و Policy Evidence را نگه می‌دارد.

File/Document Infrastructure Redesign خارج از Scope v8 است.

## ۱۵. Navigation و UX

Navigation براساس Capability، Applicability و Access Scope:

- گزارش من، فقط Required/Optional
- گزارش‌های من
- بررسی گزارش‌های حوزه
- Monitoring تفویض‌شده
- Profile Management
- Access Grant Management

برای هر Form Definition منوی مستقل ساخته نمی‌شود.

## ۱۶. Reporting

- Fieldهای Reportable به Projection تایپ‌شده نگاشت می‌شوند.
- Query مستقیم روی JSON خام بدون Index ممنوع است.
- Projection Security Classification دارد.
- Export از Projection مجاز و Section-filtered استفاده می‌کند.

## ۱۷. Migration

1. شناسایی مدل ثابت فعلی.
2. تعیین Legacy Period یا Shift Mapping.
3. ایجاد Form Definition/Version معادل.
4. ایجاد Profile و Applicability.
5. ساخت Report و Section.
6. انتقال Answer، Evidence و Snapshot.
7. حفظ State/Audit.
8. Dual Read محدود و زمان‌دار.
9. Reconciliation Report.
10. Rollback Plan.

## ۱۸. Performance

- Cache Resolver با Invalidation معتبر
- Lazy Load Sectionهای سنگین
- Projection برای Analytics
- Batch Missing-report analysis
- Pagination Review Lists
- Index روی Shift/Employee/Profile/Grant validity

## ۱۹. Observability

- applicability_resolution
- profile_resolution_success/conflict/error
- report_get_or_create
- section_resolution
- report_submitted/returned/approved/locked
- access_grant_used/denied
- section_filtered
- projection_failure
- unauthorized_operation

## ۲۰. تست‌های اجباری

- Shift crossing midnight
- Unique/idempotent Report
- Multiple Assignment Sections
- Disabled Applicability
- Profile Conflict
- Form Version Immutability
- Append-only Revision
- Reviewer Answer Access
- Access Grant Scope/Expiry/Revocation
- Section/Export Leakage
- Workflow/Approval Projection
- Migration Reconciliation
- Multi-company
- Load و Mobile/RTL UI

## ۲۱. خارج از دامنه v8

- KPI Engine مستقل داخل Work Report
- بازطراحی بنیادی Document/File Infrastructure
- ماژول جدا برای هر Form
- Message/Notification System موازی
- تغییر Odoo Core
- اجرای محاسبات ناامن در Browser