# مرجع فنی استخراج‌شده از کد: CAS Jalali - QWeb & Reports Bridge

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_jalali_qweb` |
| نسخه | `19.0.2.1.0` |
| عنوان | CAS Jalali - QWeb & Reports Bridge |
| خلاصه | Jalali Date/Datetime t-field rendering in QWeb and reports |
| دسته | Technical |
| نوع برنامه | Technical/Extension |
| نصب خودکار | True |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `cas_jalali`, `base` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 3 | مدل و منطق دامنه |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `افزونه مدل` — کلاس `IrQWeb`

- منبع: `models/ir_qweb.py:14`
- inherits: `ir.qweb`
- توضیح فنی: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_cas_qweb_format_date()` | `api.model` | 18 |
| `_cas_qweb_format_datetime()` | `api.model` | 41 |
| `_prepare_environment()` | `api.model` | 72 |

### `افزونه مدل` — کلاس `IrQwebFieldDate`

- منبع: `models/ir_qweb_fields.py:19`
- inherits: `ir.qweb.field.date`
- توضیح فنی: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `get_available_options()` | `api.model` | 23 |
| `value_to_html()` | `api.model` | 46 |

### `افزونه مدل` — کلاس `IrQwebFieldDatetime`

- منبع: `models/ir_qweb_fields.py:65`
- inherits: `ir.qweb.field.datetime`
- توضیح فنی: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `get_available_options()` | `api.model` | 69 |
| `value_to_html()` | `api.model` | 92 |

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

Asset اختصاصی ندارد.

## داده‌های بارگذاری‌شده از manifest

داده XML/CSV اعلام‌شده ندارد.

## آزمون‌های موجود

- `tests/test_qweb_jalali.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
