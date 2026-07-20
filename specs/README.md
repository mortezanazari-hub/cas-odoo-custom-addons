# CAS Design & Product Specifications

این پوشه مرجع رسمی تصمیمات محصول، طراحی رابط کاربری، تحلیل اثر تغییرات و مشخصات نهایی ماژول‌های پروژه **CAS Organizational Workspace** است.

> این اسناد در مرحله فعلی دستور پیاده‌سازی نیستند. تا زمانی که تصمیمات صفحات مرتبط تجمیع و مشخصات اجرایی نهایی هر ماژول تصویب نشده‌اند، Agent یا توسعه‌دهنده نباید صرفاً بر اساس یک سند صفحه، کد یا Schema را تغییر دهد.

## ساختار

```text
specs/
├── 00_Project/
├── 01_Product/
├── 02_UI_UX/
├── 03_Modules/
├── 04_Decisions/
├── 05_Architecture/
├── 06_ChangeSets/
├── 07_Roadmaps/
├── Module_Aggregation_Matrix.md
└── README.md
```

## چرخه تصمیم تا اجرا

1. بررسی یک صفحه و نقش‌های مرتبط
2. ثبت سند تصمیم صفحه در `02_UI_UX`
3. ثبت تصمیم‌های مشترک در `04_Decisions`
4. ثبت اثر احتمالی در `Module_Aggregation_Matrix.md`
5. تکرار برای سایر صفحات
6. تجمیع تصمیم‌ها بر اساس ماژول
7. تولید Specification نهایی در `03_Modules`
8. تأیید Specification اجرایی
9. پیاده‌سازی، Migration و تست

## وضعیت اسناد

- `Draft`: در حال بررسی
- `Agreed`: تصمیم محصولی مورد توافق
- `Needs Review`: نیازمند بررسی صفحات یا نقش‌های دیگر
- `Superseded`: با تصمیم جدید جایگزین شده
- `Implementation Ready`: پس از تجمیع، آماده تبدیل به دستور اجرایی
- `Implemented`: پیاده‌سازی‌شده و تطبیق‌داده‌شده با کد

## قواعد سخت

- تصمیم محصولی، پیشنهاد معماری و دستور پیاده‌سازی از یکدیگر جدا هستند.
- سند صفحه به‌تنهایی مجوز تغییر کد نیست.
- هر تصمیم شناسه یکتا و قابلیت ردیابی به صفحه منبع دارد.
- تغییرات مشترک چند صفحه در پایان بر اساس ماژول تجمیع می‌شوند.
- تعارض‌ها پیش از طراحی Schema و API نهایی حل یا ثبت می‌شوند.
- هیچ تغییری در هسته Odoo مجاز نیست.
- اسناد فارسی، راست‌چین‌خوان و مناسب پردازش انسان و Agent هستند.

## خط نسخه‌بندی فعال

```text
CAS UI Prototype v4 → CAS UI Workspace v7
```

نسخه‌های ۵ و ۶ Release رسمی مستقل محسوب نمی‌شوند و Iterationهای داخلی طراحی بوده‌اند.

## اسناد فعال فعلی

### سطح پروژه و محصول

- [تاریخچه نسخه‌های رسمی رابط](00_Project/Version_History.md)
- [اصول UX محصول Workspace](01_Product/UX_Principles.md)

### UI و UX

- [میزکار کاربر عادی v7](02_UI_UX/Employee/Workspace.md)

### Decision Recordها

- [سیستم Widget میزکار](04_Decisions/DEC-004-Workspace-Widget-System.md)
- [گفتگو قابلیت سطح اول است](04_Decisions/DEC-005-Conversations-Are-First-Class.md)
- [خوانایی و Theme سراسری](04_Decisions/DEC-006-Workspace-Theme-And-Readability.md)
- [Sidebar جمع‌شونده](04_Decisions/DEC-007-Collapsible-Sidebar.md)
- [تقویم تعاملی میزکار](04_Decisions/DEC-008-Embedded-Calendar.md)

### معماری و تجمیع

- [یادداشت معماری اتصال Workspace v7](05_Architecture/Workspace_UI_Integration_Notes.md)
- [Change Set میزکار](06_ChangeSets/CS-EMPLOYEE-WORKSPACE.md)
- [ماتریس تجمیع ماژول‌ها](Module_Aggregation_Matrix.md)

## وضعیت فعلی

تصمیم‌های محصول و UX میزکار v7 ثبت شده‌اند، اما Specification ماژولی در `03_Modules` هنوز تولید نشده و پیاده‌سازی مجاز نیست تا صفحات و نقش‌های وابسته بررسی و تصمیم‌ها Consolidate شوند.