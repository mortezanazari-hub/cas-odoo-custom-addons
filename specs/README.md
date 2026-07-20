# CAS Design & Product Specifications

این پوشه مرجع رسمی تصمیمات محصول، طراحی رابط کاربری، تحلیل اثر تغییرات و مشخصات نهایی ماژول‌های پروژه **CAS Organizational Workspace** است.

> این اسناد به‌تنهایی دستور پیاده‌سازی Production نیستند. تا زمانی که Specification اجرایی، API، Security، Migration و Test Strategy هر ماژول تصویب نشده است، تغییر کد یا Schema نباید صرفاً بر اساس یک سند صفحه انجام شود.

## چرخه تصمیم تا اجرا

1. بررسی صفحه و نقش
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

- هیچ تغییری در Odoo Core مجاز نیست.
- Workspace مالک داده کسب‌وکاری Providerها نیست.
- UI جایگزین ACL، Record Rule و Method Check نیست.
- هر تصمیم شناسه و قابلیت ردیابی دارد.

## خط نسخه‌بندی

```text
CAS UI Prototype v4 → CAS UI Workspace v7 → CAS UI Workspace v8
```

Prototype مرجع فعلی این مرحله:

```text
ui-workspace-v8-iteration11.zip
```

## اسناد اصلی Workspace v8

### صفحات

- [کارهای من](02_UI_UX/Employee/Personal_Tasks.md)
- [تقویم](02_UI_UX/Employee/Calendar.md)
- [گفت‌وگوها](02_UI_UX/Employee/Conversations.md)
- [جست‌وجوی سازمانی به‌صورت Command Palette](02_UI_UX/Employee/Global_Search.md)
- [تاریخچه اخیر داخل Command Palette](02_UI_UX/Employee/Recent_History.md)

### تصمیم‌ها

- [DEC-012 — حاکمیت دسته‌های کار شخصی](04_Decisions/DEC-012-Personal-Task-Category-Governance.md)
- [DEC-013 — انتخاب شرکت‌کننده و مجوز Task](04_Decisions/DEC-013-Calendar-Attendee-Selection-And-Assignment-Authorization.md)
- [DEC-014 — استفاده از Discuss](04_Decisions/DEC-014-Discuss-Reuse-And-Message-Interaction.md)
- [DEC-015 — Overlay و Focus](04_Decisions/DEC-015-Overlay-Layering-And-Focus-Management.md)
- [DEC-016 — ادغام Search و Recent History](04_Decisions/DEC-016-Search-And-Recent-History-Consolidation.md)

### معماری و Change Set

- [قراردادهای Interaction و Integration](05_Architecture/V8-Interaction-And-Integration-Contracts.md)
- [قراردادهای Search، History و Scroll](05_Architecture/V8-Search-History-And-Scroll-Contracts.md)
- [ارزیابی اثر ماژولی](03_Modules/V8_Impact_Assessment.md)
- [Change Set جامع v8](06_ChangeSets/CS-WORKSPACE-V8.md)
- [ماتریس تجمیع](Module_Aggregation_Matrix.md)

## تصمیمات نهایی Iterationهای 7 تا 11

- حذف صفحه و Route مستقل `global-search-page`
- حذف صفحه و Route مستقل `recent-history`
- Command Palette مشترک از Topbar، Hero و `Ctrl+K`
- نمایش Recent Items در Query خالی
- بازگرداندن Scroll بومی و Auto-scroll مرورگر در Routeهای عادی
- نبود Scroll کلی در Route گفت‌وگو
- Scroll مستقل فهرست گفتگو و Message Body
- شروع گفت‌وگو از آخرین پیام
- حفظ انتهای چت پس از Send
- فشرده‌سازی ردیف‌های گفتگو
- اصلاح جهت ماه قبل/بعد در RTL
- چیپ تک‌انتخابی منبع در Action Hub

## وضعیت فعلی

مستندات محصول، تصمیم، معماری و Change Set تا Iteration 11 ثبت شده‌اند. مجموعه هنوز `Implementation Ready` نیست؛ مالکیت Personal Task، Search Provider API، History Storage، Organization Scope Resolver، قرارداد Event/Task و تطبیق Discuss با Odoo 19 Community باید در Specificationهای اجرایی نهایی شوند.
