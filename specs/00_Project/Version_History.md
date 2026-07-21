# تاریخچه چرخه‌های بازنگری رابط کاربری CAS

| مشخصه | مقدار |
|---|---|
| وضعیت | `Active` |
| دامنه | UI Review History |
| آخرین چرخه فعال | `CAS UI Review Cycle 8 — Through Iteration 12` |
| نسخه نرم‌افزار | مستقل و در این سند تعریف نمی‌شود |
| مرجع فرایند | `UI_Review_Lifecycle.md` |

## اصل تفسیری

اعداد 4، 7 و 8 در این سند شماره چرخه بازنگری UI هستند، نه نسخه نرم‌افزار و نه Release محصول.

## خط تاریخی

```text
UI Review Cycle 4
→ UI Review Cycle 7
→ UI Review Cycle 8 / Iteration 12
→ Future UI Review Cycle 9
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

## Cycle 8 — آخرین چرخه فعال بازنگری UI

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

## ورود Cycle 9

با ورود Cycle 9:

- Cycle 9 آخرین چرخه فعال می‌شود.
- Cycle 8 حذف نمی‌شود.
- تصمیم‌های Active Cycle 8 باقی می‌مانند.
- تغییرات Cycle 9 در Change Set جدید ثبت می‌شوند.
- فقط تصمیم‌هایی که صریحاً جایگزین شده‌اند Superseded می‌شوند.

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
