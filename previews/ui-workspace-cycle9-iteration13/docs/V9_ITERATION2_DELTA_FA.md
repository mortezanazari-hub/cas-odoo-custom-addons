# UI Review Cycle 9 — Iteration 2 Delta

## وضعیت
Accepted / Implemented in prototype package

## مسئله
در Iteration 1 ساختار زیرمنو ایجاد شده بود، اما روش CSS مبتنی بر Grid باعث می‌شد بخش فرزندان به‌صورت قابل اتکا Collapse نشود.

## اصلاح
- جایگزینی مکانیزم Collapse با `max-height + overflow + visibility + opacity`
- افزودن wrapper داخلی برای فهرست فرزندان
- همگام‌سازی `aria-expanded`، `aria-hidden`، عنوان و برچسب کنترل
- نگهداری وضعیت هر گروه در Preference محلی نمونه

## Backend Impact
بدون تغییر Business Model. در پیاده‌سازی Odoo، وضعیت باز/بسته بودن می‌تواند در UI Preference کاربر ذخیره شود.
