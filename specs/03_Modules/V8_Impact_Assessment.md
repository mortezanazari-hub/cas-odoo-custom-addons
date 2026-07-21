# ارزیابی اثر ماژولی نسخه ۸

| مشخصه | مقدار |
|---|---|
| نسخه | `CAS UI Workspace v8 — Through Iteration 12` |
| وضعیت | `Consolidated` |
| نوع سند | Impact Assessment؛ نه مجوز Production |
| مرجع | `../00_Project/V8_Canonical_Baseline.md` |

## خلاصه

نسخه ۸ شامل Workspace Home، Personal Tasks، Calendar، Conversations، Command Palette، Recent History، Notifications Center، Dashboard Management و Dynamic Work Report است.

تصمیم‌های مالکیت و معماری اصلی دیگر باز نیستند:

- Personal Task ماژول مستقل دارد.
- Workspace فقط مالک UI Configuration است.
- Organization Scope ماژول مستقل دارد.
- Notification زیرساخت Odoo را Reuse می‌کند.
- Work Report Shift-based و Multi-assignment است.
- Access Report مستقل از زیردستی قابل تفویض است.

## ۱. `cas_workspace` — اثر بسیار زیاد

### مسئولیت‌ها

- Shell، Router و Navigation
- Command Palette
- Dashboard Configuration و User Preference
- Widget Provider Orchestration
- Recent Resource Reference
- Overlay Coordination بر پایه Odoo UI Services
- Notification Center View
- Scroll Policy

### مالک نیست

- Personal Task
- Action
- Calendar Event
- Message/Conversation
- Notification Delivery
- Work Report
- Organization Assignment
- Document

### وضعیت

Specification پایه تدوین شده است؛ API، Migration و Test Strategy اجرایی لازم است.

## ۲. `cas_workspace_contract` — ماژول فنی جدید

### مسئولیت

- Provider Protocol
- Widget/Search/Action Metadata
- Resource Reference
- Contract Versioning
- Error Contract

### دلیل

Domain Providerها نباید برای ثبت Provider به UI Module وابسته شوند.

### وضعیت

معماری Consolidated؛ نام و API نهایی نیازمند Implementation Specification است.

## ۳. `cas_personal_task` — ماژول مستقل قطعی

### مسئولیت

- Personal Task
- Personal/System Category
- Reminder و State شخصی
- Self Task از Calendar
- Workspace/Search Provider

### قواعد

- Task برای شخص دیگر به Action Hub می‌رود.
- Workspace هیچ Personal Task ذخیره نمی‌کند.
- دسته سیستمی Backend-protected است.

### وضعیت

Specification پایه تدوین شده است.

## ۴. `cas_action_hub` — اثر زیاد

- مالک Action سازمانی برای دیگران
- دریافت Assigned Action از Calendar
- حفظ تفکیک از Personal Task
- Provider برای Workspace و Search
- استفاده از Organization Scope برای مجوز تخصیص

Specification اجرایی v8 مستقل هنوز باید تکمیل شود.

## ۵. `cas_organization_core` — ماژول مستقل قطعی

### مسئولیت

- Effective Assignment
- Reporting Relationship
- Delegation سازمانی
- Purpose-aware Scope
- Directory Search Scope
- Reviewer Candidate Resolution پایه

### مصرف‌کنندگان

Calendar، Action Hub، Work Report، Search و Directory.

### وضعیت

Specification و Assignment Architecture تدوین شده است؛ Domain/API/Security Detail لازم است.

## ۶. Calendar/Event Integration — اثر زیاد

### مسئولیت

- Event، Attendee، Invitation و RSVP
- Timezone و Jalali Adapter
- Self Task از Personal Task Service
- Assigned Action از Action Hub Service
- Idempotency و Result Contract

### تصمیم Transaction

- Event و داده هم‌دامنه Transactional هستند.
- Cross-domain Actionها Command UUID و Retry امن دارند.
- Notification پس از موفقیت داده اصلی ارسال می‌شود.
- Partial Failure باید صریح به کاربر گزارش شود و رکورد تکراری نسازد.

### وضعیت

محصول Consolidated؛ API دقیق و Test Strategy لازم است.

## ۷. Odoo Mail/Discuss/Bus — اثر زیاد

### Reuse

- Conversation/Thread
- Message
- Member
- Unread
- Reaction/Reply و قابلیت‌های استاندارد
- Realtime Bus
- Notification Delivery

### قواعد

- مدل موازی Message/Conversation ممنوع است.
- Extension فقط برای Gap تأییدشده است.
- Notification Center یک View تجمیعی است، نه Delivery System جدید.

### وضعیت

نیازمند Spike و Verification روی Odoo 19 Community.

## ۸. Notification Extension — اثر مشروط

`cas_notification_core` کامل تصویب نشده است.

Extension فقط در صورت Gap واقعی برای این موارد مجاز است:

- CAS Deep Link
- Severity
- Action Metadata
- Aggregation Category
- Company Policy

مرجع: `../05_Architecture/Odoo_Notification_Gap_Analysis.md`.

## ۹. `cas_activity_catalog` — ماژول مستقل قطعی

### مسئولیت

- Activity Definition
- Activity Proposal
- Evidence Policy Reference
- KPI Mapping Reference
- Effective Scope

### قواعد

- گزارش منتظر Proposal نمی‌ماند.
- Snapshot اولیه کاربر حفظ می‌شود.

### وضعیت

Specification پایه تدوین شده است.

## ۱۰. `cas_work_report` — اثر بسیار زیاد

### تصمیم‌های قطعی

- یک Report برای هر Person + Shift Occurrence
- یک Report ترکیبی با Sectionهای چند Assignment
- Applicability: Required/Optional/Disabled
- Profile و Form Version در سطح Section
- Access Grant مستقل از زیردستی
- Reviewer/Approver و Operationهای جدا
- Reporting Projection برای داده پویا

### وابستگی‌ها

- Organization Core
- Shift/Attendance Contract
- Form Engine
- Workflow Core
- Approval Core
- Activity Catalog
- Attachment/Document

### وضعیت

Specification و Security پایه تدوین شده‌اند؛ Migration و Test Strategy کامل لازم است.

## ۱۱. Form Engine — اثر بسیار زیاد

برای Work Report باید پشتیبانی کند:

- Form Version Pinning
- Conditional Logic
- Typed Validation
- Structured/Repeatable Sections، در صورت نیاز Profile
- File/Image/Evidence Field Contract
- Immutable Revision/Snapshot
- Answer Access از رابطه Report Section
- Reporting Projection

Form Engine مالک Report Lifecycle نیست.

## ۱۲. Workflow و Approval — اثر زیاد

- Workflow مالک Process State است.
- Approval مالک Decision رسمی است.
- Work Report State Projection از این منابع مشتق می‌شود.
- State Machine موازی و مستقل ممنوع است.

## ۱۳. Attachment/Document — اثر محدود در v8

در v8:

- Odoo Attachment/Document فایل را نگهداری می‌کند.
- Form Engine Field Contract را تعریف می‌کند.
- Work Report Evidence Relation را نگهداری می‌کند.

بازطراحی بنیادی Document Infrastructure خارج از v8 است.

## ۱۴. Dashboard Administration — اثر جدید

`cas_workspace` باید پشتیبانی کند:

- Company/Role/Profile Scope
- Widget Registry Validation
- Draft/Publish/Version/Rollback
- Company Lock
- User Preference Reset
- Audit

## ۱۵. Jalali Suite — اثر متوسط

- ورودی و نمایش Jalali
- Timezone صحیح
- جهت ماه قبل/بعد در RTL
- ذخیره Date/Datetime استاندارد Odoo

## Dependency پیشنهادی

```text
Odoo Standard
↓
CAS Foundation
├── cas_workspace_contract
├── cas_organization_core
├── cas_activity_catalog
├── cas_form_core
├── cas_workflow_core
└── cas_approval_core
↓
CAS Domains
├── cas_personal_task
├── cas_action_hub
├── cas_work_report
└── سایر Domainها
↓
CAS Experience
└── cas_workspace + Bridge/Adapterها
```

## امنیت مشترک

- No broad `sudo`
- ACL + Record Rule + Method Check
- Provider Permission
- Purpose-aware Organization Scope
- Multi-company isolation
- Section/Field filtering
- Access Grant expiry/revocation
- Secure Export
- Audit

## Migration

- Routeهای v7 به v8
- Dashboard Preference/Version
- Personal Task Ownership
- Static Work Report به Shift Report و Dynamic Sections
- Form Snapshot Revision
- Reviewer Answer Access
- Provider Keys و Deep Links

## تست حداقلی

- Provider Partial Failure
- Search/History Leakage
- Calendar Event + Self/Assigned Task Idempotency
- Discuss Integration
- Dashboard Publish/Rollback
- Shift crossing midnight
- Multi-assignment Work Report
- Disabled Applicability
- Delegated Section Access
- Export/Attachment Security
- Multi-company
- RTL، Keyboard، Focus و Mobile

## وضعیت نهایی

مرزبندی و مالکیت نسخه ۸ Consolidated است. هیچ ماژولی صرفاً با این Impact Assessment `Implementation Ready` نیست.