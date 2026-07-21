# تاریخچه چرخه‌های بازنگری رابط کاربری CAS

| مشخصه | مقدار |
|---|---|
| وضعیت | `Active` |
| دامنه | UI Review History |
| آخرین چرخه فعال | `CAS UI Review Cycle 9 — Through Iteration 13` |
| نسخه نرم‌افزار | مستقل و در این سند تعریف نمی‌شود |
| مرجع فرایند | `UI_Review_Lifecycle.md` |

## اصل تفسیری

اعداد 4، 7، 8 و 9 در این سند شماره چرخه بازنگری UI هستند، نه نسخه نرم‌افزار و نه Release محصول.

## خط تاریخی

```text
UI Review Cycle 4
→ UI Review Cycle 7
→ UI Review Cycle 8 / Iteration 12
→ UI Review Cycle 9 / Iteration 13
```

نسخه‌های 5 و 6 Release یا Cycle رسمی مستقل ثبت‌شده نیستند و در تاریخ پروژه به‌عنوان Iterationهای میانی طراحی شناخته می‌شوند.

## Cycle 4 — منبع تاریخی

- معماری اولیه نقش‌محور
- صفحات تخصصی ماژول‌ها
- نگهبانی کارت‌محور
- داشبوردهای نقش‌های مدیریتی
- قراردادهای اولیه Workspace و Odoo

## Cycle 7 — منبع تاریخی

- تبدیل میزکار به مرکز فرمان شخصی
- Routeهای مستقل
- Widgetهای قابل جابه‌جایی
- تقویم تعاملی
- گفتگو به‌عنوان قابلیت سطح اول
- Theme و Sidebar
- Provider Registryهای اولیه

Cycle 7 منبع تاریخی است. تصمیم‌های آن فقط در صورت Supersede صریح بی‌اعتبار می‌شوند.

## Cycle 8 — منبع تاریخی فعال برای تصمیم‌های بدون Supersede

Cycle 8 مجموعه مشاهدات، اصلاحات و تصمیم‌های UI تا Iteration 12 را ثبت می‌کند.

### Iteration 1 تا 4

- Personal Task Categories
- عملیات پایه پیام
- Scroll و Context Menu
- Assignment Rule
- Attendee Selector
- Overlay، Layering و Focus

### Iteration 5 تا 11

- Command Palette
- حذف Routeهای مستقل Search و Recent History
- Scroll بومی Routeهای عادی
- Scroll مستقل گفتگو
- شروع گفتگو از آخرین پیام
- اصلاح تراکم
- RTL Calendar
- Action Hub Source Filter

### Iteration 12

- Dynamic Work Report
- Shift Occurrence به‌عنوان واحد گزارش
- Sectionهای چند Assignment
- Applicability
- Activity Catalog
- Snapshot
- Delegated Access
- Reporting Projection

Cycle 8 اکنون Historical Review Source است، اما تصمیم‌های Active آن که در Cycle 9 صریحاً Supersede نشده‌اند همچنان مرجع هستند.

## Cycle 9 — آخرین چرخه فعال بازنگری UI

| مشخصه | مقدار |
|---|---|
| تاریخ ثبت | `2026-07-21` |
| آخرین Iteration | `13` |
| Prototype source | `CAS_UI_Review_Cycle_9_Iteration_13.zip` |
| Observation Register | `UI_Review_Cycle_9_Register.md` |
| Decision | `../04_Decisions/DEC-010-UIR09-Consolidated-Workspace-And-Operational-UX.md` |
| Change Set | `../06_ChangeSets/CS-UIR09-WORKSPACE-UX-CONSOLIDATION.md` |
| Implementation Status | `Gap Identified` |
| UI Revalidation | `Pending Revalidation` |

### Iteration 1 تا 3 — Navigation

- Navigation درختی و Submenu
- Collapse/Expand و حفظ وضعیت
- Breadcrumb و مسیر بازگشت
- جابه‌جایی Notification Center و Communications
- Parent click به اولین Child مجاز

### Iteration 4 — Attendance و Overtime Governance

- محدودکردن مغایرت Employee به Missing Check-in/Check-out
- درخواست اصلاح با تأیید سرپرست و Correction Ledger مستقل
- بازبینی تصادفی تفویضی
- ارجاع مستقیم مغایرت کشف‌شده به مدیرعامل
- تفکیک تأخیر از ثبت ناقص
- Capabilityهای مستقل Overtime

### Iteration 5 تا 7 — Work Report و Form Builder

- Activity خارج از Catalog بدون توقف Submission
- حفظ Original Label و Standardization proposal
- Custom duration
- Activity Category و Recurring Activity field providers
- Dynamic Matrix field

### Iteration 8 تا 11 — Dashboard Personalization

- تنظیمات از آیکون Header Dashboard
- Widget visibility بدون کنترل روی کارت
- Shortcut customization
- قابل مخفی‌کردن‌بودن Command Center
- کلیک برند Workspace به Dashboard home

### Iteration 12 و 13 — Final Layout Fixes

- Searchable Activity dropdown
- نمایش شرطی Custom Duration
- حذف دکمه مستقل Unknown Activity
- حذف Work Progress widget
- تمام‌عرض‌شدن Quick Work Report
- افزایش فاصله و کاهش تراکم Dashboard

## موارد Deferred به Cycle بعد

- تنظیمات پیشرفته اختصاصی هر Widget
- CSS و Responsive polish باقی‌مانده پس از پیاده‌سازی Odoo
- بازبینی Breakpointها و تراکم نهایی روی داده واقعی

## قاعده ثبت Cycle جدید

1. شناسه Cycle
2. تاریخ شروع
3. محدوده صفحات و نقش‌ها
4. Build یا Prototype منبع
5. Observation Register
6. Decision Links
7. Module Impacts
8. Change Set
9. Revalidation Plan
10. وضعیت پایان Cycle
