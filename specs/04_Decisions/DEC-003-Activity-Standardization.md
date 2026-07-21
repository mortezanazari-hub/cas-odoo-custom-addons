# DEC-003 — فرهنگ فعالیت و Snapshot استاندارد می‌شود

| مشخصه | مقدار |
|---|---|
| وضعیت | `Agreed` |
| نسخه | `v8` |
| تاریخ تثبیت | `2026-07-21` |

## زمینه

ثبت آزاد فعالیت باعث چندگانگی نام‌ها، ضعف گزارش‌گیری و تفسیر متفاوت می‌شود. در عین حال نبود Activity مناسب نباید ثبت گزارش را متوقف کند.

## تصمیم

- `cas_activity_catalog` مالک Activity Definitionهای استاندارد است.
- کاربر Activity استاندارد را جست‌وجو و انتخاب می‌کند.
- در نبود Activity مناسب، عنوان و توضیح خود را ثبت می‌کند و Activity Proposal ساخته می‌شود.
- گزارش منتظر تأیید Proposal نمی‌ماند.
- عنوان و توضیح اولیه کاربر و تعریف مؤثر Catalog به‌صورت Snapshot حفظ می‌شوند.
- Mapping بعدی Proposal تاریخچه گزارش را بازنویسی نمی‌کند.

## پیامدها

- Activity Catalog مستقل از Work Report است.
- Evidence Policy و KPI Mapping می‌توانند از Catalog Resolve شوند.
- Form Engine یا Workspace مالک Catalog نیستند.

## گزینه‌های ردشده

- فقط متن آزاد بدون Catalog
- توقف گزارش تا تأیید Activity جدید
- بازنویسی گزارش تاریخی پس از اصلاح Catalog

## اسناد مرتبط

- `../03_Modules/cas_activity_catalog/Specification.md`
- `../03_Modules/cas_work_report/Specification.md`