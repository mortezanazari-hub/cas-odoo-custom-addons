# مرجع فنی استخراج‌شده از کد: CAS Action Hub

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_action_hub` |
| نسخه | `19.0.1.1.0` |
| عنوان | CAS Action Hub |
| خلاصه | Secure unified action inbox for CAS and Odoo work items |
| دسته | Productivity |
| نوع برنامه | Application |
| نصب خودکار | — |
| post-init hook | `post_init_hook` |
| uninstall hook | — |
| وابستگی | `mail` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 4 | مدل و منطق دامنه |
| `views/` | 3 | نما، action و menu |
| `security/` | 2 | گروه، ACL و record rule |
| `data/` | 1 | داده پایه، sequence و cron |
| `static/src/` | 2 | OWL/JavaScript/XML/SCSS |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `cas.action.event` — کلاس `CasActionEvent`

- منبع: `models/action_event.py:5`
- inherits: —
- توضیح فنی: CAS Action Hub Append-only Event

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `item_id` | `Many2one` | اقدام | `cas.action.item` | True | — | — | — | — |
| `company_id` | `Many2one` | شرکت | — | — | — | — | — | — / True |
| `event_type` | `Selection` | رویداد | — | True | True | — | — | — |
| `actor_user_id` | `Many2one` | اقدام‌کننده | `res.users` | True | True | — | — | — |
| `event_at` | `Datetime` | زمان رویداد | — | True | True | — | `fields.Datetime.now` | — |
| `note` | `Text` | توضیح | — | — | True | — | — | — |
| `snapshot` | `Json` | تصویر متادیتا | — | — | True | — | — | — |

**مقادیر Selection/State**

- `event_type`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 42 |
| `write()` | — | 47 |
| `unlink()` | — | 50 |

### `cas.action.item` — کلاس `CasActionItem`

- منبع: `models/action_item.py:16`
- inherits: `mail.thread`، `mail.activity.mixin`
- توضیح فنی: CAS Unified Action Item

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `source_model` | `Char` | مدل منبع | — | True | True | — | — | — |
| `source_record_id` | `Integer` | شناسه منبع | — | True | True | — | — | — |
| `action_key` | `Char` | کلید اقدام | — | True | True | — | — | — |
| `source_adapter` | `Char` | آداپتر منبع | — | True | True | — | — | — |
| `action_type` | `Selection` | نوع اقدام | — | True | True | — | — | — |
| `title` | `Char` | عنوان | — | True | True | — | — | — |
| `summary` | `Text` | شرح | — | — | True | — | — | — |
| `assignee_user_id` | `Many2one` | مسئول جاری | `res.users` | True | True | — | — | — |
| `original_assignee_user_id` | `Many2one` | مسئول اصلی | `res.users` | — | True | — | — | — |
| `delegate_user_id` | `Many2one` | جانشین | `res.users` | — | True | — | — | — |
| `actor_user_id` | `Many2one` | اقدام‌کننده واقعی | `res.users` | — | True | — | — | — |
| `referred_by_user_id` | `Many2one` | ارجاع‌دهنده | `res.users` | — | True | — | — | — |
| `manager_user_id` | `Many2one` | مدیر مسئول | `res.users` | — | True | — | — | — |
| `visibility_user_ids` | `Many2many` | کاربران مجاز | `res.users` | — | True | — | — | — |
| `priority` | `Selection` | اولویت | — | True | True | — | `normal` | — |
| `priority_rank` | `Integer` | رتبه اولویت | — | True | True | — | — | — |
| `deadline` | `Datetime` | مهلت | — | — | True | — | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | True | — | — | — |
| `status` | `Selection` | وضعیت | — | True | True | — | `pending` | — |
| `source_status` | `Char` | وضعیت در منبع | — | — | True | — | — | — |
| `destination_model` | `Char` | مدل مقصد | — | — | True | — | — | — |
| `destination_record_id` | `Integer` | شناسه مقصد | — | — | True | — | — | — |
| `destination_data` | `Json` | اطلاعات مقصد | — | — | True | — | — | — |
| `source_created_at` | `Datetime` | زمان ایجاد در منبع | — | — | True | — | — | — |
| `completed_at` | `Datetime` | زمان تکمیل | — | — | True | — | — | — |
| `last_synced_at` | `Datetime` | آخرین همگام‌سازی | — | True | True | — | — | — |
| `last_reminder_at` | `Datetime` | آخرین یادآوری | — | — | True | — | — | — |
| `reminder_count` | `Integer` | تعداد یادآوری | — | — | True | — | — | — |
| `escalation_level` | `Integer` | سطح تصعید | — | — | True | — | — | — |
| `escalated_to_user_id` | `Many2one` | تصعیدشده به | `res.users` | — | True | — | — | — |
| `delegation_reference` | `Char` | مرجع تفویض | — | — | True | — | — | — |
| `delegation_valid_from` | `Datetime` | اعتبار تفویض از | — | — | True | — | — | — |
| `delegation_valid_to` | `Datetime` | اعتبار تفویض تا | — | — | True | — | — | — |
| `active` | `Boolean` | فعال | — | — | True | — | `True` | — |
| `is_delegated` | `Boolean` | تفویض‌شده | — | — | — | — | — | _compute_flags / True |
| `is_overdue` | `Boolean` | موعد گذشته | — | — | — | — | — | _compute_is_overdue / — |
| `event_ids` | `One2many` | تاریخچه رسمی | `cas.action.event` | — | True | — | — | — |

**مقادیر Selection/State**

- `action_type`: —
- `priority`: —
- `status`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_compute_flags()` | `api.depends('original_assignee_user_id', 'delegate_user_id')` | 129 |
| `_compute_is_overdue()` | `api.depends('deadline', 'status')` | 138 |
| `_search_is_overdue()` | `api.model` | 146 |
| `create()` | `api.model_create_multi` | 166 |
| `write()` | — | 171 |
| `unlink()` | — | 176 |
| `_model_available()` | `api.model` | 180 |
| `_source_record()` | `api.model` | 184 |
| `_user_can_read()` | `api.model` | 190 |
| `_manager_for_user()` | `api.model` | 200 |
| `_normalize_status()` | `api.model` | 206 |
| `_normalize_descriptor()` | `api.model` | 227 |
| `_publish()` | `api.model` | 311 |
| `_update()` | `api.model` | 343 |
| `_cancel()` | `api.model` | 348 |
| `_check_source_access()` | `api.model` | 352 |
| `_resolve_destination()` | — | 363 |
| `_event_snapshot()` | — | 373 |
| `_append_event()` | — | 389 |
| `_complete()` | `api.model` | 407 |
| `action_open_source()` | — | 428 |
| `action_refresh_item()` | — | 446 |
| `get_my_counts()` | `api.model` | 452 |
| `_cron_process_sla()` | `api.model` | 476 |
| `action_sync_all()` | `api.model` | 552 |
| `_cron_sync_all()` | `api.model` | 558 |
| `_cron_sync_recent()` | `api.model` | 562 |
| `_recent_domain()` | `api.model` | 571 |
| `_sync_all()` | `api.model` | 575 |
| `_adapter_methods()` | `api.model` | 609 |
| `_descriptor()` | `api.model` | 624 |
| `_adapt_correspondence()` | `api.model` | 645 |
| `_adapt_approval()` | `api.model` | 661 |
| `_adapt_workflow()` | `api.model` | 688 |
| `_adapt_work_report()` | `api.model` | 714 |
| `_employee_manager_user()` | `api.model` | 733 |
| `_adapt_attendance_discrepancy()` | `api.model` | 737 |
| `_adapt_attendance_request()` | `api.model` | 758 |
| `_adapt_overtime()` | `api.model` | 776 |
| `_adapt_kardex()` | `api.model` | 797 |
| `_adapt_shift()` | `api.model` | 831 |
| `_adapt_odoo_activity()` | `api.model` | 864 |

### `cas.action.sla.rule` — کلاس `CasActionSlaRule`

- منبع: `models/action_sla.py:5`
- inherits: —
- توضیح فنی: CAS Action Hub SLA Rule

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `sequence` | `Integer` | — | — | — | — | — | `10` | — |
| `name` | `Char` | عنوان | — | True | — | — | — | — |
| `active` | `Boolean` | — | — | — | — | — | `True` | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `source_adapter` | `Char` | آداپتر منبع | — | — | — | — | — | — |
| `action_type` | `Selection` | نوع اقدام | — | — | — | — | — | — |
| `reminder_interval_hours` | `Float` | فاصله یادآوری (ساعت) | — | True | — | — | `24.0` | — |
| `escalation_after_hours` | `Float` | تصعید پس از سررسید (ساعت) | — | True | — | — | `24.0` | — |
| `max_escalation_level` | `Integer` | حداکثر سطح تصعید | — | True | — | — | `3` | — |
| `escalation_user_id` | `Many2one` | مسئول تصعید ثابت | `res.users` | — | — | — | — | — |

**مقادیر Selection/State**

- `action_type`: `lambda self: self.env['cas.action.item']._fields['action_type'].selection`

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_check_contract()` | `api.constrains('reminder_interval_hours', 'escalation_after_hours', 'max_escalation_level', 'company_id', 'escalation_user_id')` | 38 |
| `_for_item()` | `api.model` | 48 |

Constraints سمت سرور: `_check_contract()`

## گروه‌های امنیتی

| XML ID | عنوان | implied groups | فایل |
|---|---|---|---|
| `group_cas_action_hub_user` | کاربر کارتابل یکپارچه | — | `security/cas_action_hub_security.xml` |
| `group_cas_action_hub_manager` | مدیر کارتابل یکپارچه | [(4, ref('group_cas_action_hub_user'))] | `security/cas_action_hub_security.xml` |
| `base.group_user` | — | [(4, ref('cas_action_hub.group_cas_action_hub_user'))] | `security/cas_action_hub_security.xml` |
| `base.group_system` | — | [(4, ref('cas_action_hub.group_cas_action_hub_manager'))] | `security/cas_action_hub_security.xml` |

## ماتریس ACL

| ACL | مدل | گروه | Read | Write | Create | Unlink |
|---|---|---|---:|---:|---:|---:|
| `access_cas_action_item_user` | `model_cas_action_item` | `group_cas_action_hub_user` | 1 | 0 | 0 | 0 |
| `access_cas_action_item_manager` | `model_cas_action_item` | `group_cas_action_hub_manager` | 1 | 0 | 0 | 0 |
| `access_cas_action_event_user` | `model_cas_action_event` | `group_cas_action_hub_user` | 1 | 0 | 0 | 0 |
| `access_cas_action_event_manager` | `model_cas_action_event` | `group_cas_action_hub_manager` | 1 | 0 | 0 | 0 |
| `access_cas_action_sla_user` | `model_cas_action_sla_rule` | `group_cas_action_hub_user` | 1 | 0 | 0 | 0 |
| `access_cas_action_sla_manager` | `model_cas_action_sla_rule` | `group_cas_action_hub_manager` | 1 | 1 | 1 | 1 |

## Record Ruleها

| XML ID | عنوان | مدل | گروه‌ها | Domain |
|---|---|---|---|---|
| `rule_cas_action_item_visible` | کارتابل: فقط اقدام‌های قابل مشاهده کاربر | `model_cas_action_item` | [(4, ref('group_cas_action_hub_user'))] | `[('company_id', 'in', company_ids), ('visibility_user_ids', 'in', user.id)]` |
| `rule_cas_action_event_visible` | رویداد کارتابل: اقدام قابل مشاهده | `model_cas_action_event` | [(4, ref('group_cas_action_hub_user'))] | `[('company_id', 'in', company_ids), ('item_id.visibility_user_ids', 'in', user.id)]` |
| `rule_cas_action_sla_company` | SLA کارتابل: شرکت‌های مجاز | `model_cas_action_sla_rule` | [(4, ref('group_cas_action_hub_user'))] | `[('company_id', 'in', company_ids)]` |

## منوها

| XML ID | عنوان | والد | action | گروه |
|---|---|---|---|---|
| `menu_cas_action_hub_root` | کارتابل یکپارچه | — | — | `group_cas_action_hub_user` |
| `menu_cas_action_hub_my_work` | کارهای من | `menu_cas_action_hub_root` | `action_cas_action_hub` | — |
| `menu_cas_action_hub_all_visible` | همه اقدام‌های قابل مشاهده | `menu_cas_action_hub_root` | `action_cas_action_hub_all_visible` | — |
| `menu_cas_action_hub_sync` | همگام‌سازی اکنون | `menu_cas_action_hub_root` | `server_action_cas_action_hub_sync` | `group_cas_action_hub_manager` |
| `menu_cas_action_hub_config` | پیکربندی | `menu_cas_action_hub_root` | — | `group_cas_action_hub_manager` |
| `menu_cas_action_sla_rules` | قوانین SLA و تصعید | `menu_cas_action_hub_config` | `action_cas_action_sla_rules` | — |

## Actionها

| XML ID | نوع | عنوان | مدل/تگ | view mode | فایل |
|---|---|---|---|---|---|
| `action_cas_action_hub` | `ir.actions.act_window` | کارتابل یکپارچه | `cas.action.item` | `list,form` | `views/cas_action_item_views.xml` |
| `action_cas_action_hub_all_visible` | `ir.actions.act_window` | همه اقدام‌های قابل مشاهده | `cas.action.item` | `list,form` | `views/cas_action_item_views.xml` |
| `server_action_cas_action_hub_sync` | `ir.actions.server` | همگام‌سازی کارتابل | `model_cas_action_item` | — | `views/cas_action_item_views.xml` |
| `action_cas_action_sla_rules` | `ir.actions.act_window` | قوانین SLA و تصعید | `cas.action.sla.rule` | `list,form` | `views/cas_action_sla_views.xml` |

## Cron و Sequence

**Cronها**

| XML ID | عنوان | مدل/کد | تناوب |
|---|---|---|---|
| `ir_cron_cas_action_hub_sync` | CAS Action Hub: همگام‌سازی اقدامات | `model._cron_sync_all()` | 1 days |
| `ir_cron_cas_action_hub_sync_recent` | CAS Action Hub: همگام‌سازی افزایشی | `model._cron_sync_recent()` | 2 minutes |
| `ir_cron_cas_action_hub_sla` | CAS Action Hub: یادآوری و تصعید SLA | `model._cron_process_sla()` | 15 minutes |

## Assetهای رابط کاربری

### `web.assets_backend`

- `cas_action_hub/static/src/js/action_hub_systray.js`
- `cas_action_hub/static/src/xml/action_hub_systray.xml`

## داده‌های بارگذاری‌شده از manifest

- `security/cas_action_hub_security.xml`
- `security/ir.model.access.csv`
- `data/cas_action_hub_cron.xml`
- `views/cas_action_item_views.xml`
- `views/cas_action_sla_views.xml`
- `views/cas_action_hub_menus.xml`

## آزمون‌های موجود

- `tests/test_action_hub.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
