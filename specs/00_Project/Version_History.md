# تاریخچه نسخه‌های رسمی رابط CAS

| مشخصه | مقدار |
|---|---|
| وضعیت | `Agreed` |
| دامنه | Product / UI Versioning |
| نسخه فعال | `CAS UI Workspace v8 — Through Iteration 12` |
| مرجع | `V8_Canonical_Baseline.md` |

## خط نسخه‌بندی رسمی

```text
CAS UI Prototype v4 → CAS UI Workspace v7 → CAS UI Workspace v8
```

نسخه‌های ۵ و ۶ Release رسمی مستقل نیستند و Iterationهای داخلی طراحی محسوب می‌شوند.

## نسخه ۴ — Historical Baseline

- معماری اولیه نقش‌محور
- صفحات تخصصی ماژول‌ها
- نگهبانی کارت‌محور
- داشبوردهای سرپرست، مدیر و مدیرعامل
- قراردادهای اولیه Workspace و Odoo

## نسخه ۷ — Historical Baseline

- تبدیل میزکار کاربر عادی به مرکز فرمان شخصی
- Routeهای مستقل Personal Tasks، Calendar، Conversations، Search، Notifications و History
- Widgetهای قابل جابه‌جایی
- تقویم تعاملی
- گفتگو به‌عنوان قابلیت سطح اول
- Theme و خوانایی سراسری
- Sidebar جمع‌شونده
- Provider Registryهای اولیه

نسخه ۷ برای تاریخچه نگهداری می‌شود. هر بخش آن که با v8 تعارض داشته باشد، مرجع پیاده‌سازی نیست.

مرجع تاریخی: `../06_ChangeSets/CS-WORKSPACE-V7.md`

## نسخه ۸ — Baseline فعال

نسخه ۸ مجموعه تصمیم‌های تأییدشده تا Iteration 12 است و باید بدون کاهش دامنه مبنای طراحی و اصلاح ماژول‌ها قرار گیرد.

### Iteration 1 — Personal Task Categories و عملیات پایه پیام

- تفکیک دسته‌های سیستمی و شخصی
- CRUD دسته شخصی
- حذف امن دسته و انتقال Taskها
- عملیات پایه پیام

### Iteration 2 — Scroll، Context Menu و Assignment Rule

- قرارداد Scroll برای گفتگوها
- Context Menu و Emoji
- تفکیک Invitation و Task Assignment

### Iteration 3 — Attendee Selector مقیاس‌پذیر

- جست‌وجوی Server-side
- فیلتر واحد و Scope سازمانی
- Selection Summary و Chip

### Iteration 4 — Overlay، Layering و Focus

- Overlay Stack
- Focus Trap و Focus Restore
- Scroll Lock
- Outside Click
- Child Overlay روی Parent

### Iteration 5 و 6 — اصلاحات داخلی طراحی

این Iterationها Release مستقل نیستند و در Specificationهای نهایی نسخه ۸ جذب شده‌اند.

### Iteration 7 تا 11 — Consolidation نسخه ۸

- حذف Route مستقل `global-search-page`
- حذف Route مستقل `recent-history`
- Command Palette مشترک از Topbar، Hero و `Ctrl+K`
- Recent Items در Query خالی
- Scroll بومی Routeهای عادی
- Scroll مستقل فهرست گفتگو و Message Body
- شروع گفتگو از آخرین پیام و حفظ انتهای چت پس از Send
- فشرده‌سازی ردیف‌های گفتگو
- اصلاح جهت ماه قبل و بعد در RTL
- تک‌انتخابی‌شدن منبع در Action Hub

### Iteration 12 — Dynamic Work Report

- گزارش کار مبتنی بر Profile، Assignment و Form Version
- یک گزارش برای هر Shift Occurrence
- گزارش ترکیبی با Sectionهای چند Assignment
- قابلیت `Required`، `Optional` و `Disabled` در Profile یا شخص
- Activity Catalog مستقل
- Snapshot و Context خودکار
- دسترسی Reviewer، سازمانی و تفویض‌شده
- Reporting Projection برای داده‌های پویا

## تصمیم‌های تکمیلی تثبیت‌شده در Consolidation

- Workspace فقط مالک تنظیمات ظاهری و Preferenceهای خودش است.
- `cas_personal_task` مالک Personal Task است.
- `cas_organization_core` مالک Organization Scope و Assignment مؤثر است.
- `cas_activity_catalog` مالک فرهنگ فعالیت‌های استاندارد است.
- Notification Center از زیرساخت Odoo استفاده می‌کند و CAS فقط Gapها را تکمیل می‌کند.
- Dashboard Management Center برای ادمین به نسخه ۸ افزوده شده است.
- بازطراحی زیرساخت Document/File خارج از دامنه v8 و موضوع نسخه آینده است.

## قاعده نسخه‌بندی آینده

یک نسخه فقط زمانی Release رسمی محسوب می‌شود که:

1. دامنه و Baseline آن ثبت شود.
2. Page Specificationها به‌روزرسانی شوند.
3. Decision Recordها ثبت شوند.
4. Architecture Contractها و Module Ownership مشخص شوند.
5. Change Set و Traceability Matrix به‌روزرسانی شوند.
6. برای اجرا، API، Security، Migration و Test Strategy تصویب شوند.