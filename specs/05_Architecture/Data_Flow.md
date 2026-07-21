# Data Flow — CAS Workspace v8

| مشخصه | مقدار |
|---|---|
| وضعیت | `Consolidated` |

## Workspace Load

```text
User Session
→ Resolve Company/Role Context
→ Resolve Capabilities
→ Resolve Navigation
→ Resolve Dashboard Configuration
→ Apply User Preferences within Locks
→ Fetch Widget Providers independently
→ Render Ready/Partial Failure States
```

داده Provider در Workspace ذخیره نمی‌شود؛ فقط نتیجه نمایشی کوتاه‌عمر است.

## Command Palette

```text
Open Palette
→ check search.use
→ load Quick Actions and Recent References
→ query active Search Providers
→ provider applies record permission
→ merge/group/rank results
→ open Deep Link
→ record authorized Recent Reference
```

Recent Reference هنگام نمایش دوباره Resolve می‌شود.

## Calendar Event و Task

```text
Submit Calendar Modal
→ validate Event input
→ resolve attendees by purpose scope
→ create/update Calendar Event
→ for self-task: call Personal Task Service
→ for assigned task: call Action Hub Service
→ enqueue notifications after successful transaction
→ return per-operation result
```

Cross-domain command باید Command UUID و Idempotency داشته باشد. Partial Result باید صریح باشد و رکورد تکراری نسازد.

## Work Report Creation

```text
User opens Work Report
→ resolve active Shift Occurrence
→ resolve Applicability
→ if Disabled: no form/draft
→ get-or-create Report idempotently
→ resolve Effective Assignments at shift context
→ create/update Sections
→ resolve Report Profile per Section
→ pin Form Version
→ create/link Form Submission
→ render composite report
```

## Work Report Submit

```text
Validate all visible/required Sections
→ validate Evidence Policy
→ save immutable revision/snapshot
→ submit Form Submissions
→ trigger Workflow transition
→ create Approval/Review work if configured
→ update Report projection
→ request Odoo notifications
```

## Work Report Review

```text
Reviewer opens report
→ resolve ACL/Record Rule
→ resolve organization scope
→ resolve reviewer/approver role
→ resolve active Access Grants
→ filter Sections and operations
→ show authorized content
→ execute comment/return/approve through Domain Service
→ audit action
```

## Dashboard Publish

```text
Admin edits Draft Configuration
→ validate Widget Registry and Capabilities
→ preview resolution
→ create immutable published snapshot
→ increment version
→ activate by effective date
→ invalidate relevant preference cache
→ audit publish
```

## Notification

```text
Domain Event
→ Notification Adapter
→ reuse Odoo Mail/Discuss/Bus
→ attach CAS deep-link/action metadata when needed
→ Notification Center aggregates authorized items
```

CAS نباید Delivery Pipeline موازی ایجاد کند.

## Error Handling

- Provider Error: local
- Security Error: fail closed
- Cross-domain Conflict: explicit and idempotent retry
- Invalid Configuration: block publish
- Missing Shift/Profile: explainable Unavailable State
- Notification Failure after transaction: retryable delivery، بدون rollback داده اصلی مگر Policy صریح

## Audit Data Flow

Audit باید Command، Actor، Scope، Source، Result و Timestamp را ثبت کند، اما محتوای حساس Form/Message را بدون نیاز ذخیره نکند.