# مرجع فنی استخراج‌شده از کد: CAS Visual Workflow Designer

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_workflow_designer` |
| نسخه | `19.0.1.0.0` |
| عنوان | CAS Visual Workflow Designer |
| خلاصه | Node-based visual designer and form binding for CAS workflows |
| دسته | Productivity |
| نوع برنامه | Technical/Extension |
| نصب خودکار | — |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `cas_workflow_core`, `cas_form_core`, `web` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 2 | مدل و منطق دامنه |
| `views/` | 1 | نما، action و menu |
| `static/src/` | 3 | OWL/JavaScript/XML/SCSS |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `افزونه مدل` — کلاس `CasWorkflowDefinitionFormBinding`

- منبع: `models/workflow_designer.py:12`
- inherits: `cas.workflow.definition`
- توضیح فنی: —

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `form_definition_id` | `Many2one` | فرم متصل | `cas.form.definition` | — | — | — | — | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_check_form_target_model()` | `api.constrains('form_definition_id', 'target_model_id')` | 24 |
| `write()` | — | 29 |
| `action_start()` | — | 38 |
| `action_start_submission()` | — | 49 |

Constraints سمت سرور: `_check_form_target_model()`

### `افزونه مدل` — کلاس `CasWorkflowVersionNodeDesigner`

- منبع: `models/workflow_designer.py:58`
- inherits: `cas.workflow.version`
- توضیح فنی: —

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `designer_revision` | `Integer` | — | — | — | True | — | — | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_require_designer()` | — | 63 |
| `action_open_node_designer()` | — | 70 |
| `designer_get_graph()` | — | 80 |
| `_validate_graph_payload()` | — | 116 |
| `designer_save_graph()` | — | 182 |

### `افزونه مدل` — کلاس `CasWorkflowStateVisualPosition`

- منبع: `models/workflow_designer.py:248`
- inherits: `cas.workflow.state`
- توضیح فنی: —

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `designer_x` | `Integer` | — | — | — | — | — | `80` | — |
| `designer_y` | `Integer` | — | — | — | — | — | `80` | — |
| `designer_color` | `Char` | — | — | — | — | — | `blue` | — |

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

- `cas_workflow_designer/static/src/workflow_designer.js`
- `cas_workflow_designer/static/src/workflow_designer.xml`
- `cas_workflow_designer/static/src/workflow_designer.scss`

## داده‌های بارگذاری‌شده از manifest

- `views/cas_workflow_designer_views.xml`

## آزمون‌های موجود

- `tests/test_workflow_designer.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
