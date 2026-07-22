# تاریخچه چرخه‌های بازنگری رابط کاربری CAS

| مشخصه | مقدار |
|---|---|
| وضعیت | `Active` |
| دامنه | UI Review History |
| آخرین چرخه فعال | `CAS UI Review Cycle 10 — Through Iteration 13` |
| نسخه نرم‌افزار | مستقل و در این سند تعریف نمی‌شود |
| مرجع فرایند | `UI_Review_Lifecycle.md` |

## اصل تفسیری

اعداد 4، 7، 8، 9 و 10 در این سند شماره چرخه بازنگری UI هستند، نه نسخه نرم‌افزار و نه Release محصول.

## خط تاریخی

```text
UI Review Cycle 4
→ UI Review Cycle 7
→ UI Review Cycle 8 / Iteration 12
→ UI Review Cycle 9 / Iteration 13
→ UI Review Cycle 10 / Iteration 13
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

Cycle 8 Historical Review Source است، اما تصمیم‌های Active آن که صریحاً Supersede نشده‌اند همچنان مرجع هستند.

## Cycle 9 — منبع تاریخی فعال برای تصمیم‌های بدون Supersede

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

### Navigation و Governance

- Navigation درختی، Submenu، Collapse/Expand و Breadcrumb
- Parent click به اولین Child مجاز
- Correction Ledger حضور و غیاب
- Random delegated audit و CEO escalation
- Overtime capabilityهای مستقل

### Work Report، Form Builder و Dashboard

- Activity خارج از Catalog با original label
- Custom duration و searchable selector
- Activity/Recurring providers و Dynamic Matrix
- Dashboard settings، visibility، shortcuts و command center
- حذف Work Progress و تمام‌عرض‌شدن Quick Work Report
- CSS و Design System contract

Cycle 9 با ورود Cycle 10 حذف نشده و تصمیم‌های Active آن فقط در موارد صریح Cycle 10 Supersede شده‌اند.

## Cycle 10 — آخرین چرخه فعال بازنگری UI

| مشخصه | مقدار |
|---|---|
| تاریخ ثبت | `2026-07-22` |
| آخرین Iteration | `13` |
| Prototype review baseline | `Cycle 10 Iteration 12` |
| Documentation consolidation | `Cycle 10 Iteration 13` |
| Observation Register | `UI_Review_Cycle_10_Register.md` |
| Decision | `../04_Decisions/DEC-016-UIR10-Consolidated-Alpha-Workspace-Refinement.md` |
| Change Set | `../06_ChangeSets/CS-UIR10-ALPHA-WORKSPACE-REFINEMENT.md` |
| Implementation Status | `Gap Identified` |
| UI Revalidation | `Pending Revalidation` |

### Iteration 1 و 2 — مکاتبات

- تکمیل عملیات نامه، گیرنده/رونوشت، چاپ/PDF
- official sender و actual actor
- درخواست اقدام بدون ساخت خودکار Task
- تصمیم گیرنده درباره Task، مسئول و مهلت

### Iteration 3 تا 8 — تفویض و People Picker

- مسیر مستقل تفویض‌های من و مدیریت تفویض‌ها
- Shared People Picker
- صاحب اختیار readonly در فرم عمومی
- حوزه‌های مکاتبات، Task، Approval و گزارش کار
- اعتبار موقت، تا اطلاع ثانوی و بر اساس حکم

### Iteration 9 — مدیریت سامانه

- تفکیک گروه‌های user/access، organization، delegation، settings و audit
- مدیر ارشد به‌عنوان نقش تجمیعی
- عدم ایجاد دسترسی از عنوان شغلی مسئول IT

### Iteration 10 — دبیرخانه و Scope آلفا

- دبیرخانه به‌عنوان Access Domain برای کارشناس اداری مجاز
- وارده خارجی، ثبت نهایی صادره و شماره‌گذاری خودکار
- گزارش دفتر
- حذف OCR و DMS داخلی از آلفا

### Iteration 11 و 12 — نگهبانی

- ایستگاه سریع ثبت گروهی روی `cas.guard.batch`
- ساعت زنده و اصلاح ممیزی‌پذیر
- انتخاب چندگانه و حذف Chip
- append-only بودن رخداد رسمی Attendance

### Iteration 13 — مستندسازی

- Observation، Decision، Page Spec، Module Impact، Acceptance، Out of Scope، Change Set و Traceability

## موارد Deferred به Cycle بعد

- تعیین ownership و نام نهایی ماژول دبیرخانه
- تصمیم نهایی محل Shared People Picker
- threshold و approval policy زمان دستی Attendance
- قرارداد Integration با Nextcloud
- CSS و Responsive polish پس از پیاده‌سازی Odoo و داده واقعی

## قاعده ثبت Cycle جدید

هر Cycle جدید باید شناسه، تاریخ، Scope، Prototype source، Observation Register، Decision Links، Module Impacts، Change Set، Revalidation Plan و وضعیت پایان داشته باشد.
