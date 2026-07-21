# Module Specification — `cas_personal_task`

| مشخصه | مقدار |
|---|---|
| وضعیت محصول | `Agreed` |
| وضعیت اجرا | `Needs API/Security/Migration/Test Completion` |
| مالک دامنه | Personal Task |

## هدف

این ماژول مالک کامل Taskهای شخصی کاربر است. Workspace یا Calendar حق ذخیره مدل موازی Personal Task ندارند.

## مرزبندی

Personal Task:

- توسط کاربر برای خودش ایجاد می‌شود.
- ممکن است دسته، Deadline، Reminder و وضعیت داشته باشد.
- فرایند رسمی تخصیص سازمانی نیست.

Organizational Action:

- برای شخص دیگر ایجاد یا تخصیص داده می‌شود.
- متعلق به `cas_action_hub` است.

## مدل‌های مفهومی

### Personal Task

- owner user
- title
- description
- category
- priority
- due datetime
- status
- completed at
- source reference اختیاری
- company context
- active

### Personal Task Category

- owner user، برای دسته شخصی
- system key، برای دسته سیستمی
- name
- sequence
- color token
- system flag
- active

## قواعد دسته

- دسته سیستمی از Backend حذف یا تغییر ماهیت نمی‌دهد.
- کاربر فقط دسته شخصی خودش را مدیریت می‌کند.
- حذف دسته شخصی نیازمند انتخاب مقصد برای Taskهای موجود یا انتقال به Default است.
- نام تکراری براساس Policy مشخص کنترل می‌شود.

## Calendar Integration

ایجاد Task برای خود کاربر از Calendar، Service رسمی این ماژول را فراخوانی می‌کند. Calendar فقط Source Reference را منتقل می‌کند.

## Workspace Provider

Provider باید عرضه کند:

- Widget خلاصه Personal Tasks
- Search Provider
- Quick Action ایجاد Task
- Route و Deep Link
- Badgeهای مجاز

Provider مالکیت را به Workspace منتقل نمی‌کند.

## امنیت

- کاربر فقط Task و Category شخصی خود را می‌بیند و ویرایش می‌کند.
- Admin Access باید جدا و Audit‌شونده باشد.
- Company Context نباید باعث نشت Task میان کاربران شود.
- Share یا Delegation در v8 فقط با Decision جدا مجاز است.

## Stateها

حداقل:

- open
- completed
- cancelled یا archived، در صورت نیاز نهایی

State Machine نباید با Action Hub یکی فرض شود.

## API مفهومی

- create self task
- update own task
- complete own task
- reopen own task
- create/update/delete personal category
- delete category with reassignment
- search authorized tasks

## Migration

اگر داده Personal Task قبلاً در Workspace یا مدل دیگری نگهداری شده باشد:

- Source Mapping ثبت شود.
- مالک و Category حفظ شود.
- Duplicate Detection اجرا شود.
- Workspace Referenceها به Deep Link جدید نگاشت شوند.

## Test Strategy

- Owner isolation
- System category protection
- Category reassignment
- Calendar self-task idempotency
- Provider Permission
- Multi-company behavior
- Search leakage

## معیار پذیرش

- Workspace هیچ Personal Task Record ذخیره نکند.
- Task برای دیگری در این ماژول ایجاد نشود.
- دسته سیستمی از RPC قابل حذف نباشد.
- حذف دسته شخصی Taskها را یتیم نکند.
- Search فقط Taskهای مجاز را نشان دهد.