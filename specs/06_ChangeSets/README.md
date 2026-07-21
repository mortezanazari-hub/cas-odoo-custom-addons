# 06 — Change Sets

Change Set دامنه و اثر تغییر را ثبت می‌کند، اما به‌تنهایی مجوز تغییر Production نیست.

## Change Setهای فعال نسخه ۸

- [تجمیع کامل Specificationهای Workspace v8](CS-SPECS-V8-CONSOLIDATION.md)
- [Workspace v8 نسبت به v7](CS-WORKSPACE-V8.md)
- [Dynamic Work Report مبتنی بر Form Engine](CS-WORK-REPORT-DYNAMIC-FORM.md)
- [میزکار کاربر عادی](CS-EMPLOYEE-WORKSPACE.md)

## Change Set تاریخی

- `CS-WORKSPACE-V7.md` مرجع Historical انتقال نسخه ۴ به ۷ است.

## رابطه اسناد

- `CS-SPECS-V8-CONSOLIDATION` تصمیم‌های محصولی تا Iteration 12، مالکیت‌ها، معماری پایه و سؤالات پاسخ‌داده‌شده را یکپارچه می‌کند.
- `CS-WORKSPACE-V8` تغییرات UI و Interaction نسخه ۸ را ثبت می‌کند.
- `CS-WORK-REPORT-DYNAMIC-FORM` دامنه گزارش کار پویا را ثبت می‌کند.
- Canonical Baseline و Decision Recordها در صورت تعارض مرجع بالاتر هستند.

## الزام Change Set

هر Change Set باید:

- Baseline و Target را مشخص کند.
- اسناد Superseded را فهرست کند.
- Module Impact را ثبت کند.
- Security، Migration و Test اثرپذیر را مشخص کند.
- سؤال‌های باز را از تصمیم‌های قطعی جدا کند.
- وضعیت `Implementation Ready` را فقط با وجود Specification اجرایی اعلام کند.