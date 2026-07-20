# CAS Design & Product Specifications

این پوشه مرجع رسمی تصمیمات محصول، طراحی رابط کاربری، تحلیل اثر تغییرات و مشخصات نهایی ماژول‌های پروژه **CAS Organizational Workspace** است.

> این اسناد در مرحله فعلی دستور پیاده‌سازی نیستند. تا زمانی که تصمیمات صفحات مرتبط تجمیع و Specification اجرایی هر ماژول تصویب نشده‌اند، توسعه‌دهنده نباید صرفاً بر اساس یک سند صفحه، کد یا Schema را تغییر دهد.

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
6. تدوین قرارداد معماری
7. تجمیع بر اساس ماژول در `03_Modules`
8. تدوین API، Security، Migration و Test Strategy
9. تغییر وضعیت به `Implementation Ready`
10. پیاده‌سازی و تطبیق با کد

## قواعد سخت

- تصمیم محصولی، معماری و دستور اجرا از هم جدا هستند.
- سند صفحه به‌تنهایی مجوز تغییر کد نیست.
- هیچ تغییری در Odoo Core مجاز نیست.
- Workspace مالک داده کسب‌وکاری ماژول‌های منبع نیست.
- UI جایگزین ACL، Record Rule و Method Check نیست.
- هر تصمیم باید شناسه و قابلیت ردیابی داشته باشد.

## خط نسخه‌بندی فعال

```text
CAS UI Prototype v4 → CAS UI Workspace v7 → CAS UI Workspace v8
```

نسخه‌های ۵ و ۶ Release رسمی مستقل نیستند. تاریخچه کامل در [Version History](00_Project/Version_History.md) ثبت شده است.

## Workspace v7

نسخه ۷ Routeهای عمومی، Capabilityها، Widget System، Calendar، Conversations، Search، Notification، History، Theme و Sidebar را ایجاد یا توسعه داد.

- [Change Set جامع v7](06_ChangeSets/CS-WORKSPACE-V7.md)
- [مرجع ماژول‌های v7](03_Modules/V7_Module_Impact_And_New_Modules.md)

## Workspace v8

نسخه ۸ سه صفحه و یک زیرساخت مشترک را تکمیل کرد:

### صفحات به‌روزشده

- [کارهای من](02_UI_UX/Employee/Personal_Tasks.md)
- [تقویم](02_UI_UX/Employee/Calendar.md)
- [گفت‌وگوها](02_UI_UX/Employee/Conversations.md)

### تصمیم‌های نسخه ۸

- [حاکمیت دسته‌های کار شخصی](04_Decisions/DEC-012-Personal-Task-Category-Governance.md)
- [انتخاب شرکت‌کنندگان و مجوز Task](04_Decisions/DEC-013-Calendar-Attendee-Selection-And-Assignment-Authorization.md)
- [استفاده از Discuss و تعامل پیام](04_Decisions/DEC-014-Discuss-Reuse-And-Message-Interaction.md)
- [Overlay و مدیریت Focus](04_Decisions/DEC-015-Overlay-Layering-And-Focus-Management.md)

### معماری و اثر ماژولی

- [قراردادهای تعامل و Integration v8](05_Architecture/V8-Interaction-And-Integration-Contracts.md)
- [ارزیابی اثر ماژولی v8](03_Modules/V8_Impact_Assessment.md)
- [Change Set جامع v8](06_ChangeSets/CS-WORKSPACE-V8.md)
- [ماتریس تجمیع ماژول‌ها](Module_Aggregation_Matrix.md)

## خلاصه دامنه نسخه ۸

- CRUD دسته‌های شخصی و قفل دسته‌های سیستمی
- حذف امن دسته بدون حذف Task
- Selector مستقل و Server-side شرکت‌کنندگان
- فیلتر واحد و محدوده سازمانی
- تفکیک دعوت‌نامه از تخصیص وظیفه
- Task فقط برای زیرمجموعه مجاز
- Reply، Forward، Pin، Reaction، Mute و Archive در گفتگو
- Composer ثابت و حذف Scroll صفحه
- Context Menu و Emoji Picker اختصاصی
- استفاده از Odoo Mail/Discuss/Bus به‌جای مدل پیام موازی
- Overlay Manager، Focus Restore و Scroll Lock

## وضعیت فعلی

مستندات کامل محصول، تصمیم، معماری، Change Set و اثر ماژولی نسخه ۸ ثبت شده‌اند. این مجموعه هنوز `Implementation Ready` نیست؛ مالکیت `cas_personal_task`، Organization Scope Resolver، API Directory Search، قرارداد Event/Task و تطبیق دقیق قابلیت‌های Discuss با Odoo 19 باید در Specificationهای اجرایی تصویب شوند.
