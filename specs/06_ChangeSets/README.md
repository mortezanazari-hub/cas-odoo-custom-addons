# 06 — Change Sets

Change Set دامنه و اثر تغییر را ثبت می‌کند، اما به‌تنهایی مجوز تغییر Production نیست.

## Change Set فعال Cycle 9

- [UI Review Cycle 9 — Workspace UX Consolidation](CS-UIR09-WORKSPACE-UX-CONSOLIDATION.md)

این Change Set آخرین تغییرات پذیرفته‌شده UI Review Cycle 9 تا Iteration 13 را ثبت می‌کند. وضعیت اجرا `Gap Identified` و وضعیت UI Production برابر `Pending Revalidation` است.

## Change Setهای فعال و مرجع Cycle 8

- [تجمیع کامل Specificationهای Workspace v8](CS-SPECS-V8-CONSOLIDATION.md)
- [Workspace v8 نسبت به v7](CS-WORKSPACE-V8.md)
- [Dynamic Work Report مبتنی بر Form Engine](CS-WORK-REPORT-DYNAMIC-FORM.md)
- [میزکار کاربر عادی](CS-EMPLOYEE-WORKSPACE.md)

Cycle 8 اکنون Historical Review Source است، اما تصمیم‌های Active آن که در Cycle 9 صریحاً Supersede نشده‌اند همچنان مرجع Backend هستند.

## Change Set تاریخی

- `CS-WORKSPACE-V7.md` مرجع Historical انتقال Cycle 4 به Cycle 7 است.

## رابطه اسناد

- `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` تفاوت‌های پذیرفته‌شده Cycle 9 تا Iteration 13 را ثبت می‌کند.
- `CS-SPECS-V8-CONSOLIDATION` تصمیم‌های محصولی تا Cycle 8 / Iteration 12، مالکیت‌ها و معماری پایه را یکپارچه می‌کند.
- `CS-WORKSPACE-V8` تغییرات UI و Interaction Cycle 8 را ثبت می‌کند.
- `CS-WORK-REPORT-DYNAMIC-FORM` دامنه گزارش کار پویا را ثبت می‌کند.
- Constitution، Decision Recordها و Specificationهای Active در صورت تعارض مرجع بالاتر هستند.

## الزام Change Set

هر Change Set باید:

- Baseline و Target را مشخص کند.
- اسناد Superseded را فهرست کند.
- Module Impact را ثبت کند.
- Security، Migration و Test اثرپذیر را مشخص کند.
- سؤال‌های باز را از تصمیم‌های قطعی جدا کند.
- وضعیت `Implementation Ready` را فقط با وجود Specification اجرایی و شواهد لازم اعلام کند.
