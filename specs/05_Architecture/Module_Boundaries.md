# Module Boundaries — CAS Workspace v8

| مشخصه | مقدار |
|---|---|
| وضعیت | `Consolidated` |
| نسخه | `v8 through iteration 12` |

## هدف

این سند تعیین می‌کند هر ماژول چه چیزی را می‌داند، چه چیزی را مالک است و از چه Serviceی باید استفاده کند.

## `cas_workspace_contract`

### مالک

هیچ داده کسب‌وکاری ندارد.

### ارائه می‌کند

- Provider Protocol
- Resource Reference Schema
- Widget/Search/Action Metadata
- Contract Versioning
- Error Contract

### نباید

- به `cas_workspace` UI وابسته شود.
- Domain Modelها را import کند.

## `cas_workspace`

### مالک

- Shell
- UI Preferences
- Dashboard Configuration
- Widget Placement
- Recent Resource Reference
- Command Palette Orchestration

### مصرف می‌کند

Provider Contractها و Odoo UI Services.

### نباید

- Domain Record ذخیره کند.
- Permission Logic منبع را بازنویسی کند.

## `cas_personal_task`

### مالک

Personal Task و Categoryهای آن.

### نباید

Action سازمانی برای شخص دیگر ایجاد کند.

## `cas_action_hub`

### مالک

Action سازمانی و Lifecycle تخصیص آن.

### نباید

Personal Task خصوصی را نگهداری کند.

## `cas_organization_core`

### مالک

Organization Scope، Effective Assignment، Reporting Line و Delegation سازمانی.

### نباید

Permission اختصاصی Work Report یا Calendar را مالک شود.

## `cas_activity_catalog`

### مالک

Activity Definition و Proposal.

### نباید

Work Report Record یا Form Answer را نگهداری کند.

## `cas_work_report`

### مالک

Report، Section، Profile، Applicability، Access Grant، Evidence Relation و Reporting Projection.

### مصرف می‌کند

- Organization Core
- Form Engine
- Workflow Core
- Approval Core
- Activity Catalog
- Shift/Attendance Contract
- Attachment/Document Contract

### نباید

- Form Schema مستقل موازی بسازد.
- Assignment Master را کپی کند.
- Notification Delivery موازی بسازد.

## Form Engine

### مالک

Form Definition، Version، Field، Conditional Logic، Submission، Answer و Snapshot فنی.

### نباید

Work Report Lifecycle یا Reviewer Scope را مالک شود.

## Workflow Core

مالک Process State و Transition است. تصمیم رسمی Approval در Approval Core باقی می‌ماند.

## Approval Core

مالک Approval Request و Decision است و نباید Workflow Definition را کپی کند.

## Odoo Mail/Discuss/Bus

مالک Message، Thread و Delivery پایه Notification است. CAS فقط Adapter یا Gap Extension ایجاد می‌کند.

## Calendar Domain

مالک Event و Invitation است. ایجاد Self Task یا Assigned Action از طریق Service مقصد انجام می‌شود.

## Attachment/Document

مالک Binary و Storage است. Evidence Semantics نزد Domain مصرف‌کننده باقی می‌ماند.

## مرزهای Cross-domain

### Calendar → Task/Action

- Self: Personal Task Service
- Other: Action Hub Service
- Idempotency Key اجباری

### Workspace → Domain

- Provider Contract
- Deep Link
- Command Service
- بدون دستکاری مستقیم Model

### Work Report → Form

- Pin Form Version
- Create/Link Submission
- No schema duplication

### Work Report → Organization

- Resolve Effective Assignments
- Store Snapshot/Reference، نه Master Copy

### Notification

- Domain Event
- Odoo Notification Adapter
- Optional CAS Metadata

## قاعده ایجاد ماژول جدید

ماژول جدید فقط زمانی مجاز است که:

- Lifecycle مستقل واقعی داشته باشد.
- مالکیت فعلی آن در Odoo یا CAS وجود نداشته باشد.
- مدل جدید Projection ساده قابل Rebuild نباشد.
- وابستگی‌ها Circular نشوند.
- Security Boundary مستقل لازم باشد.