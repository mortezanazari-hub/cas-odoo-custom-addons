# مرجع فنی استخراج‌شده از کد: CAS Visual Form Builder

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_form_builder` |
| نسخه | `19.0.1.0.0` |
| عنوان | CAS Visual Form Builder |
| خلاصه | Drag-and-drop visual designer for versioned CAS forms |
| دسته | Productivity |
| نوع برنامه | Technical/Extension |
| نصب خودکار | — |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `cas_form_core`, `web` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 2 | مدل و منطق دامنه |
| `views/` | 1 | نما، action و menu |
| `static/src/` | 3 | OWL/JavaScript/XML/SCSS |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `افزونه مدل` — کلاس `CasFormVersionVisualBuilder`

- منبع: `models/form_version.py:17`
- inherits: `cas.form.version`
- توضیح فنی: —

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `designer_revision` | `Integer` | — | — | — | True | — | — | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_require_designer()` | — | 22 |
| `action_open_visual_designer()` | — | 26 |
| `designer_get_schema()` | — | 36 |
| `_validate_designer_payload()` | — | 87 |
| `designer_save_schema()` | — | 141 |

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

- `cas_form_builder/static/src/form_builder.js`
- `cas_form_builder/static/src/form_builder.xml`
- `cas_form_builder/static/src/form_builder.scss`

## داده‌های بارگذاری‌شده از manifest

- `views/cas_form_builder_views.xml`

## آزمون‌های موجود

- `tests/test_form_builder.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
