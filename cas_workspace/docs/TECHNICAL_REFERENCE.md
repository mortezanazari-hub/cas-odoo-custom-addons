# مرجع فنی استخراج‌شده از کد: CAS Organizational Workspace

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_workspace` |
| نسخه | `19.0.2.0.1` |
| عنوان | CAS Organizational Workspace |
| خلاصه | A fully custom RTL operational workspace for CAS on Odoo |
| دسته | Productivity |
| نوع برنامه | Application |
| نصب خودکار | — |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `web`, `cas_action_hub`, `cas_correspondence`, `cas_attendance_core`, `cas_workflow_core`, `cas_form_core` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 2 | مدل و منطق دامنه |
| `views/` | 1 | نما، action و menu |
| `static/src/` | 4 | OWL/JavaScript/XML/SCSS |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `cas.workspace.dashboard` — کلاس `CasWorkspaceDashboard`

- منبع: `models/workspace.py:96`
- inherits: —
- توضیح فنی: CAS Organizational Workspace Data Service

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `get_navigation()` | `api.model` | 101 |
| `get_workspace_data()` | `api.model` | 115 |
| `get_page_data()` | `api.model` | 146 |
| `get_record_detail()` | `api.model` | 180 |
| `_serialize_value()` | `api.model` | 195 |
| `_selection_label()` | `api.model` | 217 |
| `_value_tone()` | `api.model` | 223 |
| `_safe_order()` | `api.model` | 235 |
| `_source_label()` | `api.model` | 243 |
| `_source_icon()` | `api.model` | 249 |
| `_initials()` | `api.model` | 255 |

## گروه‌های امنیتی

گروه اختصاصی در XML این ماژول تعریف نشده است.

## ماتریس ACL

ACL اختصاصی ندارد؛ دسترسی از وابستگی یا مدل پایه می‌آید.

## Record Ruleها

Record rule اختصاصی در XML این ماژول تعریف نشده است.

## منوها

| XML ID | عنوان | والد | action | گروه |
|---|---|---|---|---|
| `menu_cas_workspace_root` | فضای کار سازمانی | — | `action_cas_workspace` | `base.group_user` |

## Actionها

| XML ID | نوع | عنوان | مدل/تگ | view mode | فایل |
|---|---|---|---|---|---|
| `action_cas_workspace` | `ir.actions.client` | فضای کار سازمانی | `cas_workspace.organizational_workspace` | — | `views/cas_workspace_views.xml` |

## Cron و Sequence

Cron یا sequence اختصاصی در XML ندارد.

## Assetهای رابط کاربری

### `web.assets_backend`

- `cas_workspace/static/src/workspace.js`
- `cas_workspace/static/src/workspace.xml`
- `cas_workspace/static/src/workspace.scss`

### `web.assets_frontend`

- `cas_workspace/static/src/login_theme.scss`

## داده‌های بارگذاری‌شده از manifest

- `views/cas_workspace_views.xml`

## آزمون‌های موجود

- `tests/test_workspace.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
