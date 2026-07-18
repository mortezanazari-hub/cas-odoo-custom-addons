# مرجع فنی استخراج‌شده از کد: CAS Dynamic Form Runtime

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_dynamic_form` |
| نسخه | `19.0.1.0.6` |
| عنوان | CAS Dynamic Form Runtime |
| خلاصه | Persian and RTL runtime for secure CAS dynamic forms |
| دسته | Productivity |
| نوع برنامه | Technical/Extension |
| نصب خودکار | — |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `cas_form_core`, `cas_jalali`, `web` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 2 | مدل و منطق دامنه |
| `views/` | 3 | نما، action و menu |
| `static/src/` | 7 | OWL/JavaScript/XML/SCSS |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `افزونه مدل` — کلاس `CasFormDefinitionRuntime`

- منبع: `models/form_runtime.py:17`
- inherits: `cas.form.definition`
- توضیح فنی: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_runtime_action()` | — | 20 |
| `action_open_dynamic_runtime()` | — | 32 |
| `runtime_start_submission()` | — | 43 |
| `runtime_catalog()` | `api.model` | 62 |

### `افزونه مدل` — کلاس `CasFormVersionRuntime`

- منبع: `models/form_runtime.py:107`
- inherits: `cas.form.version`
- توضیح فنی: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_runtime_field_payload()` | — | 110 |
| `_runtime_layout_payload()` | — | 135 |
| `runtime_schema()` | — | 157 |

### `افزونه مدل` — کلاس `CasFormSubmissionRuntime`

- منبع: `models/form_runtime.py:180`
- inherits: `cas.form.submission`
- توضیح فنی: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_runtime_summary()` | — | 183 |
| `action_open_dynamic_runtime()` | — | 196 |
| `_runtime_answers()` | — | 201 |
| `runtime_load()` | — | 219 |
| `runtime_save()` | — | 228 |
| `runtime_submit()` | — | 233 |

### `افزونه مدل` — کلاس `CasFormFieldRuntime`

- منبع: `models/form_runtime.py:239`
- inherits: `cas.form.field`
- توضیح فنی: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `runtime_reference_options()` | — | 242 |

## گروه‌های امنیتی

گروه اختصاصی در XML این ماژول تعریف نشده است.

## ماتریس ACL

ACL اختصاصی ندارد؛ دسترسی از وابستگی یا مدل پایه می‌آید.

## Record Ruleها

Record rule اختصاصی در XML این ماژول تعریف نشده است.

## منوها

| XML ID | عنوان | والد | action | گروه |
|---|---|---|---|---|
| `menu_cas_dynamic_form_runtime` | فرم‌های قابل ثبت | `cas_form_core.menu_cas_forms_root` | `action_cas_dynamic_form_runtime` | `cas_form_core.group_cas_form_user` |

## Actionها

| XML ID | نوع | عنوان | مدل/تگ | view mode | فایل |
|---|---|---|---|---|---|
| `action_cas_dynamic_form_runtime` | `ir.actions.client` | فرم‌های قابل ثبت | `cas_dynamic_form.Runtime` | — | `views/cas_dynamic_form_actions.xml` |

## Cron و Sequence

Cron یا sequence اختصاصی در XML ندارد.

## Assetهای رابط کاربری

### `web.assets_backend`

- `cas_dynamic_form/static/src/js/dynamic_reference_field.js`
- `cas_dynamic_form/static/src/js/dynamic_form_app.js`
- `cas_dynamic_form/static/src/xml/dynamic_reference_field.xml`
- `cas_dynamic_form/static/src/xml/dynamic_form_app.xml`
- `cas_dynamic_form/static/src/scss/dynamic_form.scss`

## داده‌های بارگذاری‌شده از manifest

- `views/cas_dynamic_form_actions.xml`
- `views/cas_dynamic_form_views.xml`
- `views/cas_dynamic_form_menus.xml`

## آزمون‌های موجود

- `tests/test_dynamic_form_runtime.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
