# ارزیابی اثر بین‌ماژولی Workspace v7

| مشخصه | مقدار |
|---|---|
| وضعیت | `Needs Review` |
| نوع سند | تجمیع اولیه اثر؛ نه Specification اجرایی |
| Change Set | `../06_ChangeSets/CS-WORKSPACE-V7.md` |

## `cas_attendance_core`

- ارائه Presence Summary به Hero
- ارائه مغایرت قابل اقدام
- Notification رخداد یا مغایرت
- Search/History فقط در Scope مجاز
- Deep Link به صفحه حضور

## `cas_attendance_operations`

- صفحه کارت‌محور ثبت نگهبانی نسخه ۴ حفظ می‌شود.
- جست‌وجوی فرد، فیلتر واحد، تغییر ساعت دستی و لاگ رخدادها پابرجاست.
- نسخه ۷ فقط Deep Link، Search محدود، Notification و Shell مشترک را به آن اضافه می‌کند.

## `cas_shift_management`

- ارائه شیفت امروز به Hero
- ارائه رویداد شیفت به Calendar Aggregator
- Notification انتشار یا جابه‌جایی شیفت
- Search و Recent History

## `cas_correspondence`

- مرزبندی رسمی با Conversation
- Search Provider برای نامه و ارجاع
- Calendar Provider برای موعدها
- Notification برای نامه یا ارجاع جدید
- Recent History و Deep Link

## `cas_correspondence_advanced`

- Search و Notification دفتر وارده/صادره
- Recent History دفتر امضا
- Deep Link امن برای رکوردهای محرمانه

## `cas_document_core`

- Global Search Provider
- Recent History Provider
- فایل‌های گفتگو و Permission Download
- Notification نسخه، OCR یا اشتراک در صورت تصویب

## `cas_form_core` و `cas_dynamic_form`

- Search Provider برای فرم و Submission
- Recent History برای Runtime و ثبت‌ها
- Deep Link به نسخه منتشرشده
- عدم نمایش نسخه Draft به کاربر Runtime

## `cas_workflow_core` و `cas_workflow_designer`

- Search Provider برای Definition و Instance
- Calendar Provider برای Deadline مرحله‌ها
- Notification تغییر مرحله یا انتظار اقدام
- Recent History
- Designer همچنان فقط Draft را ویرایش می‌کند

## `cas_approval_core`

- Provider «نیازمند اقدام»
- Notification تصمیم یا درخواست جدید
- Search و Recent History
- اجرای تصمیم از متد رسمی Approval، نه Action موازی Workspace

## `cas_kardex_management` و `cas_kardex_report`

- Search Provider
- Calendar Deadline برای دوره یا درخواست
- Notification قفل، بازگشایی و تصمیم
- Recent History درخواست‌ها و خروجی‌ها

## Jalali Suite

- تقویم ماهانه شمسی
- Parse تاریخ در Search
- نمایش تاریخ Notification و History
- Date استاندارد و Datetime UTC بدون تغییر باقی می‌ماند

## Odoo Mail/Discuss/Bus

- منبع Conversation، Message، Member و Unread
- Realtime Delivery
- Attachment Permission
- Workspace فقط Adapter و UI ارائه می‌کند

## Employee و Organization Directory

- Search Provider شخص، واحد و سمت
- Scope براساس شرکت، سایت، واحد و Assignment
- جلوگیری از نمایش اطلاعات پرسنلی غیرمجاز

## قاعده عمومی Providerها

هر Provider باید:

1. بدون `sudo` Query کند.
2. فیلدهای Search و Serialization را Whitelist کند.
3. Resource Reference و Route رسمی برگرداند.
4. حالت ماژول نصب‌نشده را به‌صورت `unavailable` کنترل کند.
5. Record Rule و Scope منبع را حفظ کند.
6. از کپی منطق تخصصی در Workspace خودداری کند.

## وضعیت

تمام موارد این سند تا بررسی صفحات تخصصی و تدوین Specification هر ماژول در وضعیت `Needs Review` باقی می‌مانند.
