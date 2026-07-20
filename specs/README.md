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

1. بررسی صفحه و نقش‌های مرتبط
2. ثبت سند صفحه در `02_UI_UX`
3. ثبت تصمیم مشترک در `04_Decisions`
4. ثبت اثر در `Module_Aggregation_Matrix.md`
5. ثبت Change Set
6. بررسی سایر نقش‌ها و صفحات وابسته
7. تجمیع براساس ماژول در `03_Modules`
8. تدوین Architecture، API، Security، Migration و Test Strategy
9. تغییر وضعیت به `Implementation Ready`
10. پیاده‌سازی و تطبیق با کد

## وضعیت اسناد

- `Draft`
- `Agreed`
- `Needs Review`
- `Superseded`
- `Implementation Ready`
- `Implemented`

## قواعد سخت

- تصمیم محصولی، معماری و دستور اجرا از هم جدا هستند.
- سند صفحه به‌تنهایی مجوز تغییر کد نیست.
- هر تصمیم شناسه یکتا و قابلیت ردیابی دارد.
- تغییرات مشترک چند صفحه براساس ماژول تجمیع می‌شوند.
- هیچ تغییری در Odoo Core مجاز نیست.
- Workspace مالک داده کسب‌وکاری ماژول‌های منبع نیست.
- UI جایگزین ACL، Record Rule و Method Check نیست.

## خط نسخه‌بندی فعال

```text
CAS UI Prototype v4 → CAS UI Workspace v7
```

نسخه‌های ۵ و ۶ Release رسمی مستقل نیستند و Iterationهای داخلی طراحی بوده‌اند.

## Audit نسخه ۷

مقایسه مستقیم Prototype نسخه ۴ و نسخه ۷ نشان داد:

- ۶ Route عمومی جدید
- ۶ Capability عمومی جدید
- افزایش Functionهای رابط از ۹۷ به ۱۲۲
- افزایش Actionهای UI از ۴۴ به ۸۰
- توسعه Navigation تمام نقش‌ها
- بیش از ۱۵۰۰ خط تغییر خالص در بسته Prototype

مرجع کامل: [Change Set جامع Workspace v7](06_ChangeSets/CS-WORKSPACE-V7.md)

## اسناد صفحه‌ای v7

### کاربر عادی

- [میزکار](02_UI_UX/Employee/Workspace.md)
- [کارهای شخصی](02_UI_UX/Employee/Personal_Tasks.md)
- [تقویم](02_UI_UX/Employee/Calendar.md)
- [گفت‌وگوها](02_UI_UX/Employee/Conversations.md)
- [جست‌وجوی سراسری](02_UI_UX/Employee/Global_Search.md)
- [مرکز اعلان‌ها](02_UI_UX/Employee/Notifications_Center.md)
- [تاریخچه اخیر](02_UI_UX/Employee/Recent_History.md)

### مشترک همه نقش‌ها

- [پوسته Workspace](02_UI_UX/Shared/Workspace_Shell.md)

## Decision Recordهای v7

- [سیستم Widget](04_Decisions/DEC-004-Workspace-Widget-System.md)
- [گفتگو قابلیت سطح اول](04_Decisions/DEC-005-Conversations-Are-First-Class.md)
- [Theme و خوانایی](04_Decisions/DEC-006-Workspace-Theme-And-Readability.md)
- [Sidebar جمع‌شونده](04_Decisions/DEC-007-Collapsible-Sidebar.md)
- [تقویم تعاملی](04_Decisions/DEC-008-Embedded-Calendar.md)
- [Route و Capabilityهای جدید](04_Decisions/DEC-009-Workspace-Route-And-Capability-Expansion.md)
- [Provider Registryها](04_Decisions/DEC-010-Global-Provider-Registries.md)
- [تفکیک Task، Action، Notification و History](04_Decisions/DEC-011-Separate-Task-Action-Notification-History.md)

## ارزیابی اثر ماژول‌ها

- [مرجع جامع ماژول‌های متأثر، ماژول‌های جدید، سرویس‌های داخلی و Adapterها](03_Modules/V7_Module_Impact_And_New_Modules.md)
- [`cas_workspace`](03_Modules/cas_workspace/V7_Impact_Assessment.md)
- [`cas_action_hub`](03_Modules/cas_action_hub/V7_Impact_Assessment.md)
- [`cas_work_report`](03_Modules/cas_work_report/V7_Impact_Assessment.md)
- [اثر بین‌ماژولی سایر ماژول‌ها](03_Modules/Cross_Module_V7_Impact_Assessment.md)
- [ماتریس تجمیع کامل](Module_Aggregation_Matrix.md)

## Change Setها

- [میزکار کاربر عادی](06_ChangeSets/CS-EMPLOYEE-WORKSPACE.md)
- [Change Set جامع نسخه ۴ تا ۷](06_ChangeSets/CS-WORKSPACE-V7.md)

## وضعیت فعلی

صفحات جدید، تغییرات Shell، Routeها، Capabilityها، آثار ماژول‌های موجود، ماژول‌های جدید پیشنهادی، سرویس‌های داخلی Workspace و Adapterهای Odoo ثبت شده‌اند. این مجموعه هنوز `Implementation Ready` نیست، زیرا باید اثر نسخه ۷ بر صفحه‌های نقش‌های سرپرست، مدیر، مدیرعامل، نگهبان، دبیرخانه، طراح فرم، طراح گردش‌کار، مدیر اسناد و مدیر سامانه نیز صفحه‌به‌صفحه بررسی و سپس Specification نهایی هر ماژول تدوین شود.
