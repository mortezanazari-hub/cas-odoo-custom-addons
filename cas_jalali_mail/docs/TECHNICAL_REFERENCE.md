# مرجع فنی استخراج‌شده از کد: CAS Jalali - Mail & Chatter Bridge

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_jalali_mail` |
| نسخه | `19.0.2.1.0` |
| عنوان | CAS Jalali - Mail & Chatter Bridge |
| خلاصه | Jalali dates in chatter messages, tracking values and tooltips |
| دسته | Technical |
| نوع برنامه | Technical/Extension |
| نصب خودکار | True |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `cas_jalali`, `mail` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 2 | مدل و منطق دامنه |
| `static/src/` | 2 | OWL/JavaScript/XML/SCSS |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `افزونه مدل` — کلاس `MailTrackingValue`

- منبع: `models/mail_tracking_value.py:13`
- inherits: `mail.tracking.value`
- توضیح فنی: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_cas_jalali_format_tracking_value()` | — | 16 |
| `_tracking_value_format_model()` | — | 35 |

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

- `cas_jalali_mail/static/src/js/message_model_patch.js`
- `cas_jalali_mail/static/src/css/mail_jalali.css`

## داده‌های بارگذاری‌شده از manifest

داده XML/CSV اعلام‌شده ندارد.

## آزمون‌های موجود

- `tests/test_tracking_value.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
