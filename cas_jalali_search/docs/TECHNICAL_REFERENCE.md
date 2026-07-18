# مرجع فنی استخراج‌شده از کد: CAS Jalali - Search Bridge

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_jalali_search` |
| نسخه | `19.0.2.1.0` |
| عنوان | CAS Jalali - Search Bridge |
| خلاصه | Organization-wide Jalali date range filters for search views |
| دسته | Technical |
| نوع برنامه | Technical/Extension |
| نصب خودکار | True |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `cas_jalali`, `web` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `static/src/` | 5 | OWL/JavaScript/XML/SCSS |
| `tests/` | 1 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

این ماژول مدل ORM ندارد و نقش آن asset، bridge یا meta-module است.

## گروه‌های امنیتی

گروه اختصاصی در XML این ماژول تعریف نشده است.

## ماتریس ACL

ACL اختصاصی ندارد؛ دسترسی از وابستگی یا مدل پایه می‌آید.

## Record Ruleها

Record rule اختصاصی در XML این ماژول تعریف نشده است.

## منوها

منوی مستقیم ندارد.

## Actionها

Action سروری/پنجره‌ای اختصاصی در XML ندارد.

## Cron و Sequence

Cron یا sequence اختصاصی در XML ندارد.

## Assetهای رابط کاربری

### `web.assets_backend`

- `cas_jalali_search/static/src/js/jalali_date_filter_dialog.js`
- `cas_jalali_search/static/src/js/search_bar_menu_patch.js`
- `cas_jalali_search/static/src/xml/jalali_date_filter_dialog.xml`
- `cas_jalali_search/static/src/xml/search_bar_menu_patch.xml`
- `cas_jalali_search/static/src/css/jalali_search.css`

## داده‌های بارگذاری‌شده از manifest

داده XML/CSV اعلام‌شده ندارد.

## آزمون‌های موجود

فایل آزمون Python با الگوی `test_*.py` در ماژول موجود نیست.

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
