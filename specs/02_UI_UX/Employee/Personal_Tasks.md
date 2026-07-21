# Page Specification — کارهای شخصی

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-EMP-TASK-001` |
| نسخه هدف | `CAS UI Workspace v8 — Through Iteration 12` |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Consolidated` |
| Route | `personal-tasks` |
| Capability | `personal_task.use` |
| مالک داده | `cas_personal_task` |
| مالک UI Shell | `cas_workspace` |

## هدف

فضای مستقل برای ثبت و مدیریت کارهای شخصی و روزمره‌ای که توسط خود کاربر برای خودش ایجاد می‌شوند و الزاماً Workflow، Approval یا Action سازمانی نیستند.

## مرزبندی دامنه

- `cas_personal_task` مالک کامل Task و Category است.
- Workspace فقط Route، Widget و Provider UI را ارائه می‌کند.
- `my-actions` یا Action Hub فقط اقدام رسمی سازمانی را نمایش می‌دهد.
- Task برای شخص دیگر Personal Task نیست و به `cas_action_hub` می‌رود.
- Self Task ایجادشده از Calendar در `cas_personal_task` ذخیره می‌شود.
- Task شخصی به‌خودی‌خود Work Report Activity نیست؛ تبدیل نیازمند اقدام صریح است.

## ساختار صفحه

1. Header و Quick Capture
2. فیلتر زمان و وضعیت
3. Category Navigation
4. مدیریت Category شخصی
5. Task List
6. Inline Actions
7. Loading، Empty، Forbidden، Error و Unavailable

## Categoryهای سیستمی

حداقل View/Categoryهای سیستمی:

- همه
- امروز
- برنامه‌ریزی‌شده
- تکمیل‌شده
- شخصی/بدون دسته

قواعد:

- Stable System Key
- غیرقابل حذف
- هویت غیرقابل تغییر توسط کاربر عادی
- Backend-protected در UI، RPC، Import و Server Action

## Categoryهای شخصی

کاربر می‌تواند:

- ایجاد کند.
- نام را ویرایش کند.
- ترتیب را تغییر دهد.
- Task را جابه‌جا کند.
- Category را حذف کند.

قواعد حذف:

- تعداد Taskهای متأثر پیش از تأیید نمایش داده می‌شود.
- مقصد انتقال Taskها مشخص می‌شود یا Default Category استفاده می‌شود.
- انتقال و حذف/Archive در یک Transaction انجام می‌شود.
- هیچ Taskی حذف یا یتیم نمی‌شود.

## Task Operations

- Quick Create
- Edit
- Complete
- Reopen
- Schedule
- Move to Category
- Archive، در صورت Policy
- Convert to Work Report Activity، با Action صریح و Permission مقصد

## Category Validation

- نام Trim و Normalize می‌شود.
- نام خالی پذیرفته نمی‌شود.
- طول محدود و قابل تنظیم است.
- یکتایی در Scope مالک اعمال می‌شود.
- Category کاربر دیگر قابل ویرایش نیست.

## Calendar Integration

Calendar برای Self Task فقط Service رسمی `cas_personal_task` را فراخوانی می‌کند و Source Event Reference اختیاری را منتقل می‌کند. Retry باید Idempotent باشد.

## Workspace Integration

Providerهای لازم:

- Navigation
- Widget
- Search
- Quick Action
- Resource Resolver

Workspace Model داخلی یا Cache دائمی Task نمی‌سازد.

## Reminder و Notification

- زیرساخت Odoo Mail/Activity/Notification تا حد امکان Reuse می‌شود.
- ماژول Notification کامل موازی ساخته نمی‌شود.
- Reminder Policy و Archive/Retention در Implementation Specification تکمیل می‌شوند.

## Stateها

- Open
- Completed
- Archived/Cancelled، در صورت تصمیم اجرایی

State این Domain با Action Hub یکی فرض نمی‌شود.

## امنیت

- Scope پیش‌فرض Task و Category مالک جاری است.
- مدیر به‌صورت پیش‌فرض Personal Task دیگران را نمی‌بیند.
- Category سیستمی قابل حذف نیست.
- Non-owner Operation رد می‌شود.
- تبدیل به Activity یا Action، Permission ماژول مقصد را دوباره بررسی می‌کند.
- Search و Badge نباید Task کاربر دیگر را افشا کنند.

## معیار پذیرش

1. هیچ Personal Task در Workspace ذخیره نشود.
2. Task برای شخص دیگر به Action Hub برود.
3. Category شخصی CRUD شود.
4. Category سیستمی از Backend محافظت شود.
5. حذف Category Taskها را حذف نکند.
6. Calendar Self Task تکراری نسازد.
7. Widget و صفحه از یک Provider استفاده کنند.
8. RPC مستقیم مالکیت را دور نزند.
9. Loading، Empty، Error و Unavailable کامل باشند.
10. RTL، Keyboard و Mobile قابل استفاده باشند.

## موضوعات آینده

- Sharing Personal Task، فقط با Decision مستقل
- Retention و Archive Policy دقیق
- Reminderهای پیشرفته

## اسناد مرتبط

- `../../04_Decisions/DEC-012-Personal-Task-Category-Governance.md`
- `../../03_Modules/cas_personal_task/Specification.md`
- `../../05_Architecture/Module_Boundaries.md`
- `../../00_Project/V8_Canonical_Baseline.md`