# Page Specification — گزارش کار پویا و شیفت‌محور

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-EMP-WR-001` |
| نسخه هدف | `Workspace v8 through iteration 12` |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Consolidated` |
| ماژول مالک دامنه | `cas_work_report` |
| Decisionها | `DEC-017`, `DEC-019`, `DEC-020` |

## هدف

نمایش و مدیریت گزارش کار مناسب شخص براساس Shift Occurrence، Applicability، Effective Assignment و Form Version، بدون ساخت صفحه و ماژول جدا برای هر شغل.

## Entry Modeها

### My Report

برای کاربری که Applicability او `Required` یا `Optional` است.

### Team Review

برای مدیر، سرپرست یا Reviewer دارای Scope.

### Delegated Monitoring

برای مسئول کنترل عملکرد، ممیز یا شخص دارای Access Grant، حتی اگر هیچ زیردستی نداشته باشد.

### No Personal Report

اگر Applicability شخص `Disabled` باشد، Form و Draft شخصی وجود ندارد. در صورت داشتن Scope، فقط Review/Monitoring نمایش داده می‌شود.

## واحد گزارش

```text
هر شخص + هر Shift Occurrence = حداکثر یک گزارش
```

- شیفت عبوری از نیمه‌شب یک گزارش واحد است.
- کارکنان اداری نیز براساس Shift Occurrence روزانه گزارش می‌دهند.
- Refresh یا ورود مجدد نباید Draft تکراری بسازد.

## ساختار صفحه

### Report Header

- شخص و Company
- Shift start/end و وضعیت
- Applicability و Source آن
- Profile Resolution
- Report State
- Completion Summary

### Assignment Sections

اگر شخص چند Assignment مؤثر دارد، یک گزارش ترکیبی با چند Section نمایش داده می‌شود. هر Section:

- Assignment و Unit/Job
- Form Profile و Version
- Dynamic Form Runtime
- Activityها
- Evidence
- Reviewer و وضعیت بررسی
- Validation Summary

### Overall Summary

- موانع مشترک
- پیگیری‌ها
- جمع‌بندی شیفت
- Submit State

## Profile Banner

Banner باید نشان دهد:

- نام Profile
- کد Profile
- Assignment مؤثر
- Form Version
- تاریخ اعتبار
- دلیل انتخاب Profile
- وضعیت پویا

کاربر باید بتواند بفهمد چرا این Form و Sectionها انتخاب شده‌اند.

## Applicability

- `Required`: Submit لازم است و Reminder مجاز است.
- `Optional`: Form وجود دارد ولی Submit اجباری نیست.
- `Disabled`: Form، Draft و Reminder شخصی وجود ندارد.

User Override فقط با Permission مدیریتی قابل تنظیم است.

## نقش‌ها و عملیات

### مالک گزارش

- مشاهده Context فقط‌خواندنی
- ثبت Activity و Answer
- ذخیره Draft
- Submit
- مشاهده Return Reason
- اصلاح و Resubmit، در صورت Workflow

### Reviewer

براساس Operation مجاز:

- View
- Comment
- Review
- Request Correction
- Return
- Approve

### مسئول کنترل عملکرد یا ممیز

ممکن است بدون زیردست، براساس Access Grant این موارد را ببیند:

- همه یا بخشی از گزارش‌ها
- Summary
- KPI
- مغایرت
- Evidence
- Sectionهای تفویض‌شده

View، Export یا Audit به معنی Approve نیست.

## Section-level Security

- Section غیرمجاز اصلاً به Client ارسال نمی‌شود.
- Export فقط Section و Field مجاز را شامل می‌شود.
- دسترسی Report Header به معنی دسترسی همه Sectionها نیست.
- Evidence از Permission همان Section پیروی می‌کند.

## Activity Catalog

- Activity استاندارد جست‌وجو و انتخاب می‌شود.
- Activity ناموجود می‌تواند Proposal ایجاد کند.
- گزارش منتظر تأیید Proposal نمی‌ماند.
- عنوان و توضیح اولیه Snapshot می‌شوند.

## Evidence و فایل

در v8:

- Form Engine Field Type و Validation را تعریف می‌کند.
- Odoo Attachment/Document فایل واقعی را نگهداری می‌کند.
- Work Report ارتباط فایل با Report، Section، Assignment و Activity را نگه می‌دارد.

بازطراحی File/Document Infrastructure در نسخه آینده انجام می‌شود و این صفحه را در v8 متوقف نمی‌کند.

## Stateها

- Loading
- No Active Shift
- Reporting Disabled
- Profile Not Found
- Profile Conflict
- Form Version Missing
- Provider Unavailable
- Draft
- Submitted
- Returned
- Under Review
- Approved
- Locked
- Forbidden
- Partial Section Error

در خطاهای Resolution، Form پیش‌فرض تصادفی نمایش داده نمی‌شود.

## Scroll و Responsive

- Route از Native Page Scroll استفاده می‌کند.
- Table یا Repeatable Grid عریض Scroll داخلی دارد.
- Sectionها در Mobile Collapse منطقی دارند.
- Submit Summary همیشه قابل دسترسی است ولی محتوای فرم را نمی‌پوشاند.

## امنیت

- Employee، Shift، Assignment، Profile و Reviewer از Payload Client پذیرفته نمی‌شوند و Server Resolve می‌شوند.
- Access Grant زمان و Scope را در Backend بررسی می‌کند.
- Multi-company isolation الزامی است.
- Direct RPC و ID Tampering نباید Report یا Section غیرمجاز را باز کند.

## معیار پذیرش

1. شیفت عبوری از نیمه‌شب یک گزارش بسازد.
2. چند Assignment یک گزارش ترکیبی با Sectionهای مستقل بسازند.
3. `Disabled` هیچ Form یا Draft شخصی نمایش ندهد.
4. شخص بدون زیردست بتواند با Grant گزارش‌های تفویض‌شده را ببیند.
5. Section غیرمجاز در UI، API و Export افشا نشود.
6. گزارش موجود با Form Version و Snapshot خودش باز شود.
7. Profile Resolution قابل توضیح باشد.
8. Retry یا Refresh گزارش تکراری نسازد.
9. Mobile، RTL، Keyboard و Validation قابل استفاده باشند.