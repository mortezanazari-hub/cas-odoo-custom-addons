# Change Set جامع — CAS UI Workspace v8

| مشخصه | مقدار |
|---|---|
| شناسه | `CS-WORKSPACE-V8` |
| خط مبنا | `CAS UI Workspace v7` |
| نسخه هدف | `CAS UI Workspace v8` |
| دامنه | Personal Tasks، Calendar Event Modal، Conversations، Overlay Infrastructure |
| وضعیت | `Collected` |
| مجوز پیاده‌سازی Production | ندارد تا Specificationها تصویب شوند |

## هدف نسخه ۸

نسخه ۸ یک Iteration صرفاً ظاهری نیست. این نسخه سه مسئله عملیاتی نسخه ۷ را تکمیل می‌کند:

1. حاکمیت دسته‌های کار شخصی
2. انتخاب مقیاس‌پذیر شرکت‌کنندگان و تفکیک دعوت از تخصیص وظیفه
3. تبدیل صفحه گفتگو به تجربه عملیاتی مبتنی بر Mail/Discuss، همراه با قرارداد مشترک Overlay و Focus

## دامنه Prototype

خروجی تأییدشده:

```text
ui-workspace-v8-iteration4.zip
```

Iterationهای داخلی نسخه ۸:

- Iteration 1: مدیریت دسته‌ها، شرکت‌کنندگان اولیه، قابلیت‌های پیام
- Iteration 2: اصلاح Scroll، Context Menu، Emoji و محدودیت Task
- Iteration 3: Selector مستقل و مقیاس‌پذیر شرکت‌کنندگان
- Iteration 4: اصلاح Layering و Focus Selector روی Modal

## تغییرات صفحه «کارهای من»

- دسته‌های سیستمی قفل و غیرقابل حذف هستند.
- دسته‌های شخصی قابل افزودن، تغییر نام، حذف، مرتب‌سازی و فیلتر هستند.
- حذف دسته شخصی Taskهای آن را حذف نمی‌کند.
- Taskهای متاثر به دسته پیش‌فرض منتقل می‌شوند.
- کنترل مالکیت و دسته سیستمی در Backend الزامی است.

### تصمیم‌های مرتبط

- `PAGE-EMP-TASK-DEC-008..010`
- `DEC-012`

## تغییرات تقویم و Modal رویداد

- فهرست کامل کارکنان از Modal حذف شد.
- انتخاب شرکت‌کنندگان در Selector مستقل انجام می‌شود.
- جست‌وجو پس از حداقل دو حرف و به‌صورت Server-side اجرا می‌شود.
- نتایج محدود، صفحه‌بندی‌شده یا Virtualized هستند.
- فیلتر واحد، محدوده سازمانی و زیرمجموعه‌های من وجود دارد.
- انتخاب‌شده‌ها به‌صورت Chip جمع‌بندی می‌شوند.
- نوع ارسال برای هر فرد مستقل تعیین می‌شود.
- زیرمجموعه مجاز می‌تواند دعوت، Task یا هر دو دریافت کند.
- فرد خارج از Scope فقط دعوت دریافت می‌کند.
- کنترل نوع ارسال برای فرد انتخاب‌نشده نمایش داده نمی‌شود.
- کنترل عمومی متناقض روش ارسال حذف شد.
- Header/Footer Modal ثابت و Scroll کنترل‌شده است.
- Selector به‌عنوان Child Overlay روی Modal باز می‌شود.
- Modal زیرین Inert و State آن محفوظ است.
- Focus پس از بستن Selector به Trigger بازمی‌گردد.

### تصمیم‌های مرتبط

- `PAGE-EMP-CAL-DEC-008..012`
- `DEC-013`
- `DEC-015`

## تغییرات گفتگوها

- آیکن نامه با نماد گفت‌وگو جایگزین شد.
- Header معرفی و توضیح غیرضروری حذف شد.
- جست‌وجوی تکراری حذف شد.
- دکمه «گفت‌وگوی جدید» Floating Action شد.
- آواتارها اصلاح و یکپارچه شدند.
- ردیف‌های گفتگو فشرده و Preview یک‌خطی شدند.
- Scroll کل صفحه حذف شد.
- Composer همیشه در دسترس باقی می‌ماند.
- Context Menu اختصاصی برای پیام و گفتگو اضافه شد.
- Reply، Forward، Copy، Pin، Reaction و Delete مجاز افزوده شد.
- Pin، Mute، Archive و Read State برای گفتگو تعریف شد.
- Emoji Picker در Composer و Reaction فعال شد.
- Context Menu و Picker با Outside Click و Escape بسته می‌شوند.
- مالکیت داده در Mail/Discuss/Bus باقی می‌ماند.

### تصمیم‌های مرتبط

- `PAGE-EMP-CONV-DEC-009..013`
- `DEC-014`
- `DEC-015`

## تغییرات مشترک Overlay

- Overlay Manager مشترک برای Modal، Drawer، Popover، Context Menu و Picker لازم است.
- Child Overlay باید نسبت به Parent لایه بالاتر بگیرد.
- فقط بالاترین Overlay قابل تعامل است.
- Escape فقط لایه فعال را می‌بندد.
- Focus Trap و Focus Restore الزامی است.
- Scroll Lock و جلوگیری از Scroll تودرتو جزو قرارداد مشترک است.

## ماژول‌های موجود متأثر

| ماژول/دامنه | شدت | اثر نسخه ۸ |
|---|---:|---|
| `cas_workspace` | بسیار زیاد | صفحات، Modal، Selector، Overlay Manager، Context Menu، Layout و State |
| Odoo Mail/Discuss/Bus | زیاد | Reply، Forward، Reaction، Pin، Unread، Channel و Realtime |
| HR/Employee Directory | زیاد | جست‌وجوی Server-side کارکنان و Scope اطلاعات |
| Organization Hierarchy | زیاد | تعیین رابطه مدیریتی و مجوز Task |
| `cas_action_hub` | متوسط | ایجاد Task/Action برای زیرمجموعه مجاز |
| `cas_personal_task` پیشنهادی | متوسط | Category Governance و مالکیت Task شخصی |
| Calendar/Event Integration | زیاد | Event، Attendee، Invitation و پاسخ دعوت |
| `cas_document_core` | کم تا متوسط | Permission فایل‌های گفتگو |
| Notification Core | متوسط | دعوت، پیام جدید، Mute و Failure Feedback |
| Jalali Suite | کم | تاریخ Modal و نمایش رویداد |

## ماژول یا زیرساخت جدید موردنیاز

### قطعی در سطح زیرساخت Workspace

- Overlay Manager
- Directory Search Adapter
- Organization Scope Resolver
- Calendar Attendee Selector Component
- Discuss Adapter توسعه‌یافته

### پیشنهادی به‌عنوان ماژول مستقل

- `cas_personal_task` برای Task و Category شخصی

ایجاد ماژول مستقل فقط پس از تصویب Specification، Migration و Dependency Graph انجام می‌شود.

## قراردادهای Backend

### Category

- مالکیت User Scope
- ممنوعیت حذف دسته سیستمی
- انتقال اتمیک Taskها هنگام حذف دسته

### Directory Search

- Query Server-side
- حد نتیجه و Pagination
- رعایت Company و Record Rule
- عدم افشای اطلاعات خارج از Scope

### Task Assignment

- Operation مستقل از Invitation
- بررسی Hierarchy، Capability، ACL و Delegation
- جلوگیری از تغییر Target ID برای دورزدن مجوز

### Discuss

- استفاده از مدل‌های استاندارد Mail/Discuss
- کنترل مالکیت حذف
- کنترل Attachment و Forward
- Realtime از Bus با Fallback کنترل‌شده

## تست‌های Regression

### کارهای من

- CRUD دسته شخصی
- تلاش برای حذف دسته سیستمی از RPC
- حذف دسته دارای Task
- Refresh و همگام‌سازی Widget

### تقویم

- سازمان با داده حجیم
- جست‌وجو و Pagination
- Task برای زیرمجموعه مستقیم/غیرمستقیم
- دعوت برای فرد خارج از Scope
- تغییر Target در Request
- Modal + Selector + Escape + Focus
- Responsive و Scroll Lock

### گفتگو

- Outside Click Context Menu
- Emoji Picker در دو محل
- Composer ثابت
- ردیف‌های طولانی
- Reply و Forward
- Pin/Mute/Archive
- Delete مجاز و غیرمجاز
- قطع Bus و Reconnect

## Migration و سازگاری

- Routeهای نسخه ۷ حفظ می‌شوند.
- داده Prototype Migration محسوب نمی‌شود.
- در صورت ایجاد مدل Category، دسته‌های سیستمی با XML ID پایدار Seed می‌شوند.
- Preferenceهای Pin/Mute/Category باید Scope و Migration روشن داشته باشند.
- Extensionهای Discuss نباید مدل اصلی Odoo را Fork یا Core Edit کنند.

## موارد خارج از دامنه این Change Set

- تماس صوتی و تصویری
- رمزگذاری سرتاسری
- اشتراک عمومی Task شخصی
- Bulk Task Assignment خارج از سیاست مدیریتی
- Import کامل Contact Directory در Client
- جایگزینی کامل UI اصلی Discuss خارج از Workspace

## شرط تغییر به `Implementation Ready`

1. تصویب مالکیت `cas_personal_task`
2. مشخص‌شدن مدل Organization Scope Resolver
3. تعیین API جست‌وجوی Directory
4. تعیین مدل Event/Invitation/Task Creation
5. تطبیق دقیق قابلیت‌های Reply/Forward/Reaction/Pin با Odoo 19 Mail/Discuss
6. تصویب Overlay Manager و Accessibility Contract
7. تدوین Security، Migration و Test Strategy برای ماژول‌های متأثر
