# DEC-001 — Workspace عملیاتی و Action-First است

| مشخصه | مقدار |
|---|---|
| وضعیت | `Agreed` |
| نسخه | `v8` |
| تاریخ تثبیت | `2026-07-21` |

## زمینه

صفحه اصلی نباید صرفاً داشبورد آماری یا فهرست منوهای Odoo باشد. کاربر باید اقدام بعدی، برنامه، گزارش و ارتباطات جاری را سریع تشخیص دهد.

## تصمیم

Workspace یک محیط عملیاتی Action-First است. ترتیب اولویت محتوا:

1. اقدام‌ها و تصمیم‌های لازم
2. برنامه، شیفت و رویداد
3. Personal Task و Action سازمانی
4. Conversation و Notification
5. گزارش کار
6. KPI و اطلاعات تحلیلی

## پیامدها

- Widgetهای صرفاً تزئینی یا غیرقابل اقدام اولویت پایین دارند.
- هر Card باید Primary Action یا Deep Link روشن داشته باشد.
- خرابی یک Provider نباید کل Workspace را متوقف کند.
- Workspace مالک داده Providerها نمی‌شود.

## گزینه ردشده

نمایش داشبوردی متراکم و KPI-first به‌عنوان صفحه اصلی عمومی رد شد.

## اسناد مرتبط

- `../02_UI_UX/Employee/Workspace_V8.md`
- `../01_Product/UX_Principles.md`
- `../00_Project/V8_Canonical_Baseline.md`