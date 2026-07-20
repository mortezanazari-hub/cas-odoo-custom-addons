# Change Set — میزکار کاربر عادی v7

| مشخصه | مقدار |
|---|---|
| شناسه | `CS-EMPLOYEE-WORKSPACE` |
| سند منبع | `../02_UI_UX/Employee/Workspace.md` |
| خط مبنا | `CAS_UI_Prototype_V4` |
| نسخه مقصد | `CAS UI Workspace v7` |
| وضعیت | `Collected` |
| مجوز پیاده‌سازی | ندارد |

## هدف

ثبت متمرکز تصمیمات محصولی و UX میزکار v7 و آماده‌سازی آن‌ها برای تجمیع آینده بر اساس ماژول.

## دامنه تصمیم‌های ثبت‌شده

### تجربه روزانه

- تبدیل داشبورد به میزکار عملیاتی
- Hero سه‌ردیفه و منظم
- برنامه امروز و کارهای نیازمند اقدام
- جست‌وجوی سراسری
- خلاصه حضور و شیفت

### فعالیت و گزارش کار

- ثبت سریع و تدریجی فعالیت
- ادغام ثبت فعالیت و آخرین فعالیت‌ها
- فرهنگ استاندارد فعالیت
- ثبت فعالیت ناموجود بدون توقف گزارش
- حفظ Snapshot اولیه
- مجموع زمان و هشدار اختلاف حضور

### گفتگو

- عنوان نمایشی «گفت‌وگوها»
- حفظ Route فنی `messages`
- دسترسی از Sidebar، Topbar و میزکار
- آیکن دو حباب گفتگو
- انتقال اطلاعات جانبی به Drawer

### تقویم

- Widget تعاملی روز، هفته و ماه
- نمای ماهانه شمسی
- نام ماه، سال و روزهای هفته
- روز جاری و روزهای دارای رویداد
- ناوبری ماه قبل و بعد

### Widget و شخصی‌سازی

- Drag & Drop Widgetها
- حفظ ترتیب کاربر
- ارتفاع ثابت Widgetها
- Scroll داخلی Body
- Header، Tab و Footer ثابت
- ظرفیت ثابت فهرست‌ها و ردیف خالی غیرفعال
- اندازه متن، تراکم، Accent و Light/Dark Mode
- Collapse/Expand پایدار Sidebar
- ادغام میانبرهای تکراری در نوار عملیات

## ماژول‌ها و دامنه‌های احتمالی

- `cas_workspace`
- `cas_work_report`
- `cas_action_hub`
- `cas_attendance_core`
- `cas_shift_management`
- `cas_correspondence`
- Odoo Mail/Bus
- Odoo Calendar
- User Preference
- فرهنگ فعالیت
- Assignment سازمانی

## Decision Recordهای مرتبط

- `../04_Decisions/DEC-004-Workspace-Widget-System.md`
- `../04_Decisions/DEC-005-Conversations-Are-First-Class.md`
- `../04_Decisions/DEC-006-Workspace-Theme-And-Readability.md`
- `../04_Decisions/DEC-007-Collapsible-Sidebar.md`
- `../04_Decisions/DEC-008-Embedded-Calendar.md`

## وابستگی به بررسی‌های آینده

این Change Set پیش از تبدیل به Specification اجرایی باید با اسناد زیر تجمیع شود:

- صفحه کامل گزارش کار
- کارتابل کاربر
- صفحه کامل گفتگوها
- صفحه کامل تقویم
- Workspace Settings
- میزکار سرپرست، مدیر و مدیرعامل
- حضور و غیاب
- شیفت و ثبت نگهبانی
- ساختار سازمانی و Assignment
- گزارش‌های مدیریتی

## خروجی نهایی مورد انتظار

پس از بررسی صفحات مرتبط، تصمیم‌ها باید در Specification نهایی ماژول‌های متأثر ادغام شوند. تا آن زمان این Change Set مجوز کدنویسی، Migration یا تغییر Schema نیست.