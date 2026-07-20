# فهرست جامع ماژول‌های متأثر و ماژول‌های جدید Workspace v7

| مشخصه | مقدار |
|---|---|
| شناسه | `MOD-V7-IMPACT-001` |
| خط مبنا | `CAS_UI_Prototype_V4` |
| نسخه هدف | `CAS UI Workspace v7` |
| وضعیت | `Needs Review` |
| مجوز پیاده‌سازی | ندارد |

## هدف

این سند مرجع مرکزی و یکپارچه برای پاسخ به چهار سؤال است:

1. کدام ماژول‌های موجود تحت تأثیر نسخه ۷ قرار گرفته‌اند؟
2. چه تغییراتی باید در هر ماژول موجود اعمال شود؟
3. چه ماژول‌های جدیدی احتمالاً باید ایجاد شوند؟
4. کدام قابلیت‌ها باید فعلاً به‌صورت Service یا Adapter داخل `cas_workspace` باقی بمانند و ماژول مستقل نشوند؟

> این سند نتیجه جمع‌بندی اثر نسخه ۴ تا نسخه ۷ است، اما تا زمان تأیید مرزبندی‌های معماری و تبدیل وضعیت به `Implementation Ready` دستور پیاده‌سازی محسوب نمی‌شود.

## خلاصه تصمیم

### ماژول‌های موجود با اثر بسیار زیاد

- `cas_workspace`

### ماژول‌های موجود با اثر زیاد

- `cas_action_hub`
- `cas_work_report`

### ماژول‌های موجود با اثر متوسط

- `cas_attendance_core`
- `cas_attendance_operations`
- `cas_shift_management`
- `cas_correspondence`
- `cas_correspondence_advanced`
- `cas_document_core`
- `cas_form_core`
- `cas_dynamic_form`
- `cas_workflow_core`
- `cas_workflow_designer`
- `cas_approval_core`
- `cas_kardex_management`
- `cas_kardex_report`
- مجموعه Jalali

### زیرساخت‌های Odoo که Adapter لازم دارند

- Employees / HR
- Mail / Discuss / Bus
- Calendar / Event
- ACL / Record Rule / User Groups

### ماژول‌های جدید پیشنهادی با اولویت بالا

- `cas_personal_task`
- `cas_notification_core`
- `cas_recent_history`
- `cas_activity_catalog`

### قابلیت‌هایی که فعلاً باید داخل `cas_workspace` بمانند

- Workspace Router
- Widget Registry
- Workspace Preference
- Global Search Provider Registry
- Calendar Aggregator
- Mail/Discuss Adapter
- Notification Adapter
- History Adapter
- Access Resolver Adapter

### ماژول‌هایی که فعلاً نباید مستقل ایجاد شوند

- `cas_global_search`
- `cas_workspace_calendar`
- `cas_conversation`
- `cas_theme`
- `cas_widget`

## ۱. ماژول‌های موجود متأثر

### `cas_workspace` — اثر بسیار زیاد

مسئولیت‌های جدید یا توسعه‌یافته:

- Shell کامل Workspace
- Router و Deep Link
- Route Registry
- Capability Mapping
- Sidebar جمع‌شونده و پایدار
- Topbar شامل Search، Conversation، Notification، Appearance و Profile
- Hero سه‌ردیفه
- Command Launcher
- Action Strip
- Widget Registry
- Drag & Drop Widgetها
- ذخیره ترتیب و وضعیت Widgetها
- Theme، Accent، Dark Mode، Font Scale و Density
- Drawer و Modal Infrastructure
- صفحه کارهای شخصی
- صفحه تقویم
- صفحه گفتگوها
- صفحه جست‌وجوی سراسری
- مرکز اعلان‌ها
- تاریخچه اخیر
- Provider Registryهای Search، Calendar، Notification و History
- Adapterهای اتصال به ماژول‌های منبع

Routeهای جدید:

- `personal-tasks`
- `calendar`
- `messages`
- `global-search-page`
- `notifications-center`
- `recent-history`

وضعیت: `Needs Review`

### `cas_action_hub` — اثر زیاد

تغییرات:

- تغییر مفهوم نمایشی `my-actions` از «کارهای من» به «نیازمند اقدام»
- جداسازی Action سازمانی از Personal Task
- منبع Widget «نیازمند اقدام»
- ارائه Deadline به Calendar Aggregator
- تولید یا تغذیه Notification
- حضور در Global Search
- Deep Link به رکورد منبع
- حذف واژه فنی SLA از UI کاربر عادی و تبدیل آن به برچسب‌های قابل فهم

وضعیت: `Needs Review`

### `cas_work_report` — اثر زیاد

تغییرات:

- ثبت سریع فعالیت از میزکار
- ساخت تدریجی گزارش روزانه
- گزارش چندفعالیتی
- Widget ترکیبی ثبت و مرور فعالیت
- نمایش مجموع زمان
- هشدار اختلاف حضور و گزارش
- تبدیل اختیاری Personal Task به Activity
- Search Provider
- History Provider
- حفظ Snapshot اولیه عنوان و شرح
- اتصال به Activity Catalog

وضعیت: `Needs Review`

### `cas_attendance_core` — اثر متوسط

تغییرات:

- Presence Summary برای Hero
- وضعیت حضور امروز
- مغایرت حضور و مسیر اقدام
- Notification مغایرت
- Deep Link به صفحه حضور
- Search و History محدود و مجاز
- داده لازم برای مقایسه حضور با گزارش کار

وضعیت: `Needs Review`

### `cas_attendance_operations` — اثر متوسط

تغییرات:

- حفظ صفحه تخصصی ثبت نگهبانی نسخه ۴
- Deep Link از Workspace
- ثبت History برای رخدادهای مشاهده‌شده یا ثبت‌شده
- Notification رخداد حساس در صورت نیاز
- اتصال کنترل‌شده به Attendance Core

وضعیت: `Needs Review`

### `cas_shift_management` — اثر متوسط

تغییرات:

- ارائه شیفت امروز به Hero
- Calendar Provider برای شیفت‌ها
- Notification تغییر یا جابه‌جایی شیفت
- History مشاهده و تغییرات مجاز
- Deep Link به برنامه شیفت

وضعیت: `Needs Review`

### `cas_correspondence` — اثر متوسط

تغییرات:

- جداسازی کامل مکاتبات رسمی از گفتگوها
- Search Provider نامه‌ها
- Calendar Provider برای مهلت‌ها
- Notification ارجاع، وصول یا مهلت
- Recent History
- Deep Link از Search، Notification و History

وضعیت: `Needs Review`

### `cas_correspondence_advanced` — اثر متوسط

تغییرات:

- Notification دفتر امضا و صف ثبت
- Calendar Provider برای مهلت‌های رسمی
- Search Provider دفتر وارده/صادره
- History Provider
- Deep Link مدیرعامل و دبیرخانه

وضعیت: `Needs Review`

### `cas_document_core` — اثر متوسط

تغییرات:

- Search Provider اسناد
- Recent History برای اسناد بازشده
- Notification OCR، نسخه جدید یا تغییر وضعیت
- ارائه فایل‌های مرتبط به Drawer گفتگو
- کنترل مجوز Download و Preview
- Deep Link به سند

وضعیت: `Needs Review`

### `cas_form_core` — اثر متوسط

تغییرات:

- Search Provider فرم‌ها
- Notification فرم قابل تکمیل یا دارای مهلت
- Calendar Provider برای موعد فرم
- Recent History
- Deep Link به تعریف یا اجرای فرم

وضعیت: `Needs Review`

### `cas_dynamic_form` — اثر متوسط

تغییرات:

- نمایش فرم‌های قابل اقدام در Workspace
- Action تولیدشده برای Submission
- Notification مهلت یا تغییر وضعیت
- Search و History
- حفظ Pin شدن Submission به نسخه منتشرشده فرم

وضعیت: `Needs Review`

### `cas_workflow_core` — اثر متوسط

تغییرات:

- Provider برای Action Hub
- Notification تغییر مرحله
- Calendar Provider برای Deadline مرحله
- Search Provider نمونه‌های Workflow
- Recent History
- Deep Link به Instance

وضعیت: `Needs Review`

### `cas_workflow_designer` — اثر متوسط

تغییرات:

- Search Provider تعریف‌ها
- History برای تعریف‌های اخیر
- Notification خطای Publish یا Validation
- Route و Capability نقش طراح

وضعیت: `Needs Review`

### `cas_approval_core` — اثر متوسط

تغییرات:

- منبع Actionهای تأیید
- Notification درخواست تصمیم
- Deadline در Calendar
- Search Provider
- History تصمیم‌ها
- Deep Link از Widget و Notification
- حفظ تفکیک Approval از Workflow

وضعیت: `Needs Review`

### `cas_kardex_management` — اثر متوسط

تغییرات:

- Actionهای کاردکس در «نیازمند اقدام»
- Calendar Provider برای دوره‌ها و مهلت‌ها
- Notification قفل، بازگشایی یا نقص
- Global Search
- Recent History
- Deep Link به عملیات حساس

وضعیت: `Needs Review`

### `cas_kardex_report` — اثر متوسط

تغییرات:

- Notification آماده‌شدن خروجی
- History تولید یا دانلود فایل
- Search Provider گزارش‌ها
- Deep Link به خروجی

وضعیت: `Needs Review`

### مجموعه Jalali — اثر متوسط

ماژول‌های متأثر:

- `cas_jalali`
- `cas_jalali_hr`
- `cas_jalali_mail`
- `cas_jalali_search`
- `cas_jalali_qweb`
- `cas_jalali_suite`

تغییرات:

- نمایش ماه و سال شمسی
- ناوبری صحیح ماهانه
- Query تاریخ شمسی در Search
- نمایش تاریخ جلالی پیام‌ها و رویدادها
- حفظ ذخیره استاندارد Date و Datetime در Odoo
- رعایت Timezone کاربر

وضعیت: `Needs Review`

## ۲. زیرساخت‌های Odoo و Adapterهای لازم

### Mail / Discuss / Bus

برای گفتگوها، Unread Count، Channel، ارسال پیام، اعضا، فایل‌ها و همگام‌سازی زنده استفاده می‌شود. Workspace مالک پیام نیست.

Adapter پیشنهادی داخل `cas_workspace`:

- `workspace_mail_adapter`

### Calendar / Event

برای رویداد شخصی و سازمانی استفاده می‌شود. Calendar Aggregator باید رویدادهای ماژول‌های مختلف را در نمای واحد جمع کند.

Adapter پیشنهادی داخل `cas_workspace`:

- `workspace_calendar_aggregator`

### Employees / HR

برای هویت کاربر، سمت، واحد، تصویر، Scope سازمانی، Search اشخاص و Assignmentها استفاده می‌شود.

### ACL / Record Rule / Groups

تمام Routeها، Providerها و Deep Linkها باید کنترل سمت سرور داشته باشند. مخفی‌شدن UI جایگزین امنیت نیست.

## ۳. ماژول‌های جدید پیشنهادی

### `cas_personal_task` — پیشنهاد با اولویت بالا

مالکیت:

- Task شخصی کاربر
- وضعیت، موعد، اولویت و توضیح
- تکمیل، انتقال و زمان‌بندی
- تبدیل اختیاری به Activity

دلیل استقلال:

- Personal Task با Action سازمانی متفاوت است.
- Action Hub نباید مالک Task شخصی باشد.

وضعیت: `Proposed / Needs Review`

### `cas_notification_core` — پیشنهاد با اولویت بالا

مالکیت:

- Notification تجمیعی
- Read/Unread
- منبع، نوع، مقصد و Deep Link
- Delivery Policy
- Realtime و Cron fallback
- Provider Registry اعلان‌ها

دلیل استقلال:

- Notification با Action و Message متفاوت است.
- چندین ماژول منبع باید بتوانند Notification تولید کنند.

وضعیت: `Proposed / Needs Review`

### `cas_recent_history` — پیشنهاد با اولویت بالا

مالکیت:

- تاریخچه مرور کاربر
- Resource Reference
- حذف از History بدون حذف رکورد منبع
- بازبینی مجوز هنگام نمایش مجدد
- سیاست ثبت نکردن Routeهای حساس

دلیل استقلال:

- Recent History با Audit Log متفاوت است.

وضعیت: `Proposed / Needs Review`

### `cas_activity_catalog` — پیشنهاد با اولویت بالا

مالکیت:

- فعالیت استاندارد
- دسته‌بندی
- Alias
- دامنه انتشار
- پیشنهاد فعالیت جدید
- بررسی، اصلاح، ادغام یا رد
- حفظ Snapshot اولیه

دلیل استقلال:

- این فرهنگ باید توسط Work Report و احتمالاً سایر دامنه‌ها قابل استفاده باشد.

وضعیت: `Proposed / Needs Review`

## ۴. سرویس‌هایی که فعلاً داخل `cas_workspace` می‌مانند

- `workspace_router`
- `workspace_widget_registry`
- `workspace_preference`
- `workspace_global_search_registry`
- `workspace_calendar_aggregator`
- `workspace_mail_adapter`
- `workspace_notification_adapter`
- `workspace_history_adapter`
- `workspace_access_resolver`

قاعده:

تا زمانی که مصرف‌کننده مستقل، پیچیدگی دامنه‌ای یا نیاز به چرخه عمر جداگانه وجود ندارد، این موارد نباید زودهنگام به ماژول مستقل تبدیل شوند.

## ۵. ماژول‌هایی که فعلاً نباید ساخته شوند

### `cas_global_search`

فعلاً Search Registry و Provider Contract داخل `cas_workspace` کافی است. فقط در صورت نیاز به Index مستقل، Async Search یا مصرف‌کننده خارج Workspace جدا شود.

### `cas_workspace_calendar`

فعلاً Aggregator داخل Workspace کافی است. مالکیت رویداد در ماژول منبع باقی می‌ماند.

### `cas_conversation`

نباید جایگزین Odoo Mail/Discuss/Bus شود. فقط Adapter لازم است.

### `cas_theme`

Theme و Preference فعلاً بخشی از Workspace هستند.

### `cas_widget`

Widget Registry فعلاً زیرساخت داخلی Workspace است.

## ۶. ترتیب پیشنهادی تصمیم و پیاده‌سازی

1. نهایی‌کردن مرز `cas_workspace`
2. نهایی‌کردن تفکیک Personal Task، Action، Notification و History
3. تعیین تکلیف چهار ماژول پیشنهادی جدید
4. تعریف Provider Contractهای Search، Calendar، Notification و History
5. تکمیل Access Resolver و Capability Matrix
6. تولید Specification نهایی `cas_workspace`
7. تولید Specification ماژول‌های جدید تأییدشده
8. تولید API، Security، Migration و Test Strategy
9. پیاده‌سازی مرحله‌ای

## ۷. اسناد مرتبط

- `../Module_Aggregation_Matrix.md`
- `../06_ChangeSets/CS-WORKSPACE-V7.md`
- `cas_workspace/V7_Impact_Assessment.md`
- `cas_action_hub/V7_Impact_Assessment.md`
- `cas_work_report/V7_Impact_Assessment.md`
- `Cross_Module_V7_Impact_Assessment.md`
- `../04_Decisions/DEC-009-Workspace-Route-And-Capability-Expansion.md`
- `../04_Decisions/DEC-010-Global-Provider-Registries.md`
- `../04_Decisions/DEC-011-Separate-Task-Action-Notification-History.md`

## نتیجه

نسخه ۷ فقط تغییر UI در `cas_workspace` نیست. این نسخه مرز مسئولیت چند ماژول موجود را تغییر می‌دهد، چهار دامنه جدید بالقوه ایجاد می‌کند و نیازمند Adapter و Provider Contract مشترک میان Workspace و ماژول‌های منبع است. تا زمان تأیید ماژول‌های جدید، نام‌های پیشنهادی در وضعیت `Needs Review` باقی می‌مانند و نباید به‌عنوان تصمیم اجرایی قطعی تلقی شوند.
