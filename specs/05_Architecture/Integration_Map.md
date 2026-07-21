# Integration Map — CAS Workspace v8

| مشخصه | مقدار |
|---|---|
| وضعیت | `Consolidated` |

## جدول Integration

| مبدأ | مقصد | روش | داده / Command | مالک Transaction |
|---|---|---|---|---|
| Workspace | Providerها | Contract Registry | Widget/Search/Action | Provider Service |
| Workspace | Odoo Web | Service/Registry | Dialog, Command, Router | Odoo UI Runtime |
| Calendar | Personal Task | Domain Service | Self Task | Command Coordinator |
| Calendar | Action Hub | Domain Service | Assigned Action | Command Coordinator |
| Calendar | Organization Core | Scope Resolver | Attendees/Assignable Users | Organization Core |
| Work Report | Organization Core | Resolver | Effective Assignments/Reviewer Candidates | Organization Core |
| Work Report | Shift/Attendance | Contract | Shift Occurrence/Context | Shift Domain |
| Work Report | Form Engine | Service | Form Version/Submission/Answer | Coordinated Domain Service |
| Work Report | Workflow | Service/Event | Process Transition | Workflow Core |
| Work Report | Approval | Service/Event | Approval Request/Decision | Approval Core |
| Work Report | Activity Catalog | Search/Resolver | Activity/Evidence Policy | Activity Catalog |
| Work Report | Attachment/Document | Reference/Service | Evidence Binary | Attachment/Document |
| Domainها | Odoo Mail/Discuss/Bus | Adapter | Notification/Message | Odoo Mail |
| Notification Center | Odoo/CAS Providers | Aggregation Provider | Authorized Notifications | Source Provider |

## قوانین Integration

- Direct Model Manipulation میان Domainها فقط در صورتی مجاز است که همان ماژول مالک هر دو مدل باشد.
- Cross-domain Command از Service رسمی استفاده می‌کند.
- هر Command چندمرحله‌ای Idempotency Key دارد.
- Notification پس از موفقیت Transaction اصلی ارسال می‌شود.
- Provider Failure نباید Scope را گسترده کند.
- API باید خطاهای Forbidden، Validation، Conflict و Unavailable را تفکیک کند.

## Odoo Reuse

### Mail/Discuss/Bus

برای Conversation، Mention، Thread، Realtime و Delivery اعلان استفاده می‌شود.

### Calendar

Event و Attendee را نگه می‌دارد؛ CAS تجربه UI و Policyهای سازمانی را Extend می‌کند.

### Attachment

Binary Storage را نگه می‌دارد؛ Domainها فقط Relation و Semantics را اضافه می‌کنند.

### Dialog و Command Services

برای Overlay و Shortcut استفاده می‌شوند؛ سیستم موازی ساخته نمی‌شود.

## Future Integration — خارج از v8

### Nextcloud

موضوع نسخه آینده برای Document Storage/Versioning/Sharing است. Integration آینده نباید Referenceهای Evidence v8 را بی‌اعتبار کند.

### External BI

فقط از Reporting Projection امن و API کنترل‌شده استفاده می‌کند؛ دسترسی مستقیم به Answerهای خام مجاز نیست.

## Transaction Policy

- تغییرات هم‌دامنه در یک Transaction.
- Cross-domain Side Effectها با Command UUID و Retry امن.
- Notification Failure داده کسب‌وکاری را تکراری نمی‌کند.
- Compensation فقط برای Flowهایی که Atomicity کامل ممکن نیست تعریف می‌شود.

## Observability

- correlation id
- command id
- provider key
- source/target domain
- duration
- result code
- retry count

Log محتوا باید حداقل و مطابق Classification باشد.