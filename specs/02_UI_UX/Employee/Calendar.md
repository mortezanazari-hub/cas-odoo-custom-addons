# Page Specification — تقویم

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-EMP-CAL-001` |
| نسخه هدف | `CAS UI Workspace v8 — Through Iteration 12` |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Consolidated` |
| Route | `calendar` |
| Capability پایه | `calendar.use` |
| مالک Event | Calendar Domain |
| مالک UI | Workspace Calendar Experience |

## هدف

تقویم قابلیت سطح اول Workspace برای مشاهده Eventها، ساخت جلسه، دریافت Invitation، مشاهده موعدها و ایجاد Self Task یا Assigned Action در محدوده مجاز است.

## تفکیک قطعی مفاهیم

### Invitation

دعوت شخص به Event. مالک آن Calendar Domain است.

### Self Task

کاری که Actor برای خودش ایجاد می‌کند. مالک آن `cas_personal_task` است.

### Assigned Action

کاری که Actor برای شخص دیگری ایجاد یا تخصیص می‌دهد. مالک آن `cas_action_hub` است.

این سه Operation می‌توانند از یک Modal آغاز شوند، ولی مدل، Permission و نتیجه مستقل دارند.

## ساختار صفحه

1. Header و نمای روز/هفته/ماه
2. کنترل امروز و ماه/بازه قبل و بعد
3. Event Feed تجمیعی
4. Modal ساخت یا ویرایش Event
5. Attendee Selector
6. Self Task و Assigned Action Options
7. Event Detail
8. Loading، Empty، Forbidden، Error و Unavailable

## Calendar View

- Day، Week و Month الزامی‌اند.
- نمای ماه شمسی کامل است.
- ماه قبل و بعد در RTL معنای صحیح دارند.
- Date/Datetime در Odoo Standard و UTC/Timezone صحیح ذخیره می‌شود.
- Jalali فقط Input/Display Layer است.

## Event Modal

فیلدهای پایه:

- عنوان
- تاریخ
- زمان شروع و پایان
- نوع Event
- توضیح
- Attendees
- Self Task اختیاری
- Assigned Actions اختیاری، فقط با Capability

قواعد Layout:

- Header و Footer پایدار
- Body Scroll کنترل‌شده در صورت نیاز
- Footer محتوای Form را نمی‌پوشاند
- Viewport کوچک Responsive
- State Modal هنگام بازشدن Selector حفظ می‌شود

## Attendee Selector

### Data Loading

- کل Directory در Client بارگذاری نمی‌شود.
- Query Server-side و صفحه‌بندی‌شده است.
- حالت اولیه فقط Recent، Frequent و Direct Scope محدود را نشان می‌دهد.
- Query آزاد پس از Threshold مناسب اجرا می‌شود.
- Stale Request لغو می‌شود.

### فیلتر و Purpose

- Organization Unit
- My Direct Reports
- Recent People
- All Invite-eligible People

Scope با Purpose `calendar_invite` از `cas_organization_core` Resolve می‌شود.

### اطلاعات نتیجه

- نام و Avatar
- Job Title
- Organization Unit
- Relationship
- Invite Eligibility
- Action Assignment Eligibility، در صورت نمایش
- Restriction Reason

### Selection

- افراد انتخاب‌شده Chip دارند.
- حذف Chip Selection را حذف می‌کند.
- Confirm Selection تغییر را به Modal والد برمی‌گرداند.
- Cancel تغییر موقت را کنار می‌گذارد.

## Assigned Action Selector

فقط افراد دارای Scope `action_assign` مجازند. Invite Eligibility به معنی Action Eligibility نیست.

برای شخص خارج از Action Scope:

- Invitation ممکن است مجاز باشد.
- Assigned Action غیرفعال است.
- دلیل محدودیت قابل مشاهده است.

## Self Task

Self Task به Service رسمی `cas_personal_task` ارسال می‌شود. Calendar هیچ Personal Task Record نگهداری نمی‌کند.

## Command و Transaction

Command دارای UUID است و این مراحل را هماهنگ می‌کند:

1. Validate Event و Timezone.
2. Resolve Attendee و Action Scope.
3. Create/Update Event و Attendees.
4. Create Self Task در Personal Task، در صورت درخواست.
5. Create Assigned Actions در Action Hub، در صورت درخواست.
6. ثبت Source Link.
7. درخواست Notification از Odoo Infrastructure.
8. بازگرداندن نتیجه تفصیلی.

قواعد:

- Retry نباید Event، Task یا Action تکراری بسازد.
- Failure هر بخش به‌صورت شفاف نمایش داده می‌شود.
- داده هم‌دامنه Transactional است.
- Side Effectهای Cross-domain Retry-safe هستند.
- Notification System موازی ساخته نمی‌شود.

## Overlay و Focus

- Attendee Selector Child Overlay از Event Modal است.
- Primitive از Odoo UI Services استفاده می‌کند.
- Overlay زیرین Inert است.
- Escape ابتدا Child را می‌بندد.
- Focus به Trigger Selector برمی‌گردد.
- Route Change Overlayها را Clean up می‌کند.

## Timezone

- Local DateTime بدون Offset به‌صورت دستی UTC فرض نمی‌شود.
- افزودن دستی `Z` ممنوع است.
- Odoo User Timezone/Date Utility مرجع است.
- شیفت و Event عبوری از نیمه‌شب درست نمایش داده می‌شوند.

## Provider Feed

Calendar Feed می‌تواند از این منابع Item دریافت کند:

- Event
- Shift
- Action Deadline
- Work Report Deadline/Status
- Correspondence Deadline
- Workflow Milestone

Provider Failure باید محلی باشد و Eventهای اصلی Calendar را از بین نبرد.

## امنیت

- Invitation و Assigned Action Permission جدا هستند.
- Actor، Company، Target و Purpose در Backend Resolve می‌شوند.
- Client نمی‌تواند با تغییر Target ID Scope را دور بزند.
- Directory Result حداقل Metadata لازم دارد.
- Multi-company isolation الزامی است.
- Action Creation از Method Check ماژول مقصد استفاده می‌کند.

## معیار پذیرش

1. Modal به تعداد کل کارکنان وابسته نباشد.
2. Directory کاملاً Server-side باشد.
3. Invitation، Self Task و Assigned Action به مالک درست بروند.
4. Person خارج از Action Scope فقط در صورت مجوز Invitation دریافت کند.
5. Retry رکورد تکراری نسازد.
6. Partial Failure واضح و قابل بازیابی باشد.
7. Selector State، Focus و Escape صحیح باشند.
8. Timezone و Jalali صحیح باشند.
9. نبود Provider اختیاری Crash ایجاد نکند.
10. RPC مستقیم Action غیرمجاز نسازد.

## اسناد مرتبط

- `../../04_Decisions/DEC-013-Calendar-Attendee-Selection-And-Assignment-Authorization.md`
- `../../04_Decisions/DEC-015-Overlay-Layering-And-Focus-Management.md`
- `../../05_Architecture/V8-Interaction-And-Integration-Contracts.md`
- `../../05_Architecture/Assignment_Model.md`
- `../../03_Modules/cas_personal_task/Specification.md`
- `../../00_Project/V8_Canonical_Baseline.md`