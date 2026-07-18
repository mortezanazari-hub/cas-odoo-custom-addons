# مرجع فنی استخراج‌شده از کد: CAS Workflow Core

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_workflow_core` |
| نسخه | `19.0.1.0.3` |
| عنوان | CAS Workflow Core |
| خلاصه | Versioned and auditable workflow foundation for CAS business processes |
| دسته | Productivity |
| نوع برنامه | Technical/Extension |
| نصب خودکار | — |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `cas_form_core`, `mail` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 3 | مدل و منطق دامنه |
| `views/` | 3 | نما، action و menu |
| `security/` | 2 | گروه، ACL و record rule |
| `data/` | 1 | داده پایه، sequence و cron |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `cas.workflow.definition` — کلاس `CasWorkflowDefinition`

- منبع: `models/workflow_definition.py:16`
- inherits: `mail.thread`، `mail.activity.mixin`
- توضیح فنی: CAS Workflow Definition

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `name` | `Char` | عنوان گردش‌کار | — | True | — | True | — | — |
| `code` | `Char` | کد فنی | — | True | — | — | — | — |
| `description` | `Text` | توضیحات | — | — | — | — | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `owner_user_id` | `Many2one` | مالک فرایند | `res.users` | — | — | True | `lambda self: self.env.user` | — |
| `target_model_id` | `Many2one` | مدل مقصد | `ir.model` | True | — | — | — | — |
| `version_ids` | `One2many` | نسخه‌ها | `cas.workflow.version` | — | — | — | — | — |
| `current_version_id` | `Many2one` | نسخه فعال | `cas.workflow.version` | — | True | — | — | — |
| `active` | `Boolean` | — | — | — | — | True | `True` | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 64 |
| `write()` | — | 70 |
| `unlink()` | — | 86 |
| `_check_code()` | `api.constrains('code')` | 98 |
| `action_create_initial_version()` | — | 103 |
| `action_start()` | — | 118 |

Constraints سمت سرور: `_check_code()`

### `cas.workflow.version` — کلاس `CasWorkflowVersion`

- منبع: `models/workflow_definition.py:137`
- inherits: `mail.thread`، `mail.activity.mixin`
- توضیح فنی: CAS Workflow Version

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `definition_id` | `Many2one` | — | `cas.workflow.definition` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `name` | `Char` | عنوان نسخه | — | True | — | — | — | — |
| `revision` | `Integer` | بازنگری | — | True | — | — | `1` | — |
| `state` | `Selection` | وضعیت نسخه | — | True | — | True | `draft` | — |
| `notes` | `Text` | یادداشت بازنگری | — | — | — | — | — | — |
| `published_at` | `Datetime` | — | — | — | True | — | — | — |
| `published_by_id` | `Many2one` | — | `res.users` | — | True | — | — | — |
| `schema_hash` | `Char` | — | — | — | True | — | — | — |
| `state_ids` | `One2many` | وضعیت‌های گردش‌کار | `cas.workflow.state` | — | — | — | — | — |
| `transition_ids` | `One2many` | — | `cas.workflow.transition` | — | — | — | — | — |

**مقادیر Selection/State**

- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 178 |
| `write()` | — | 185 |
| `unlink()` | — | 192 |
| `_check_publish_access()` | — | 197 |
| `_schema_payload()` | — | 204 |
| `_validate_publishable()` | — | 217 |
| `action_publish()` | — | 231 |
| `action_new_revision()` | — | 253 |

### `cas.workflow.versioned.mixin` — کلاس `CasWorkflowVersionedMixin`

- منبع: `models/workflow_definition.py:285`
- inherits: —
- توضیح فنی: CAS Workflow Versioned Mixin

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `version_id` | `Many2one` | — | `cas.workflow.version` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 293 |
| `write()` | — | 301 |
| `unlink()` | — | 308 |

### `cas.workflow.state` — کلاس `CasWorkflowState`

- منبع: `models/workflow_definition.py:314`
- inherits: `cas.workflow.versioned.mixin`
- توضیح فنی: CAS Workflow State

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `sequence` | `Integer` | — | — | — | — | — | `10` | — |
| `name` | `Char` | عنوان وضعیت | — | True | — | — | — | — |
| `code` | `Char` | کد فنی | — | True | — | — | — | — |
| `kind` | `Selection` | — | — | True | — | — | `normal` | — |
| `sla_hours` | `Float` | مهلت مرحله (ساعت) | — | — | — | — | — | — |
| `fold` | `Boolean` | جمع‌شده در کانبان | — | — | — | — | — | — |

**مقادیر Selection/State**

- `kind`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 340 |
| `_check_code()` | `api.constrains('code')` | 347 |
| `_schema_payload()` | — | 352 |

Constraints سمت سرور: `_check_code()`

### `cas.workflow.transition` — کلاس `CasWorkflowTransition`

- منبع: `models/workflow_definition.py:363`
- inherits: `cas.workflow.versioned.mixin`
- توضیح فنی: CAS Workflow Transition

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `sequence` | `Integer` | — | — | — | — | — | `10` | — |
| `name` | `Char` | عنوان انتقال | — | True | — | — | — | — |
| `code` | `Char` | کد فنی | — | True | — | — | — | — |
| `from_state_id` | `Many2one` | — | `cas.workflow.state` | True | — | — | — | — |
| `to_state_id` | `Many2one` | — | `cas.workflow.state` | True | — | — | — | — |
| `allowed_group_ids` | `Many2many` | گروه‌های مجاز | `res.groups` | — | — | — | — | — |
| `responsible_mode` | `Selection` | — | — | True | — | — | `keep` | — |
| `note_required` | `Boolean` | یادداشت اجباری | — | — | — | — | — | — |
| `condition_config` | `Json` | شرط ساختاریافته | — | — | — | — | `dict` | — |

**مقادیر Selection/State**

- `responsible_mode`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 397 |
| `_check_code()` | `api.constrains('code')` | 404 |
| `_check_state_versions()` | `api.constrains('from_state_id', 'to_state_id', 'version_id')` | 410 |
| `_validate_definition()` | — | 418 |
| `_schema_payload()` | — | 426 |

Constraints سمت سرور: `_check_code()`, `_check_state_versions()`

### `cas.workflow.instance` — کلاس `CasWorkflowInstance`

- منبع: `models/workflow_runtime.py:11`
- inherits: `mail.thread`، `mail.activity.mixin`
- توضیح فنی: CAS Workflow Instance

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `number` | `Char` | — | — | — | True | — | `New` | — |
| `definition_id` | `Many2one` | — | `cas.workflow.definition` | True | — | — | — | — |
| `version_id` | `Many2one` | — | `cas.workflow.version` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `resource_model` | `Char` | مدل رکورد | — | True | True | — | — | — |
| `resource_id` | `Integer` | شناسه رکورد | — | True | True | — | — | — |
| `resource_display_name` | `Char` | عنوان رکورد | — | True | True | — | — | — |
| `current_state_id` | `Many2one` | — | `cas.workflow.state` | True | — | True | — | — |
| `status` | `Selection` | — | — | True | True | True | `running` | — |
| `responsible_user_id` | `Many2one` | مسئول جاری | `res.users` | True | — | True | — | — |
| `started_by_id` | `Many2one` | — | `res.users` | True | True | — | — | — |
| `started_at` | `Datetime` | — | — | True | True | — | — | — |
| `state_entered_at` | `Datetime` | — | — | True | True | — | — | — |
| `state_deadline` | `Datetime` | مهلت مرحله | — | — | True | — | — | — |
| `completed_at` | `Datetime` | — | — | — | True | — | — | — |
| `history_ids` | `One2many` | — | `cas.workflow.history` | — | — | — | — | — |

**مقادیر Selection/State**

- `status`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 56 |
| `write()` | — | 61 |
| `unlink()` | — | 83 |
| `_deadline_for_state()` | `api.model` | 87 |
| `_start_instance()` | `api.model` | 93 |
| `_user_can_execute()` | — | 167 |
| `_available_transitions()` | — | 188 |
| `action_get_available_transitions()` | — | 197 |
| `action_execute_transition()` | — | 211 |
| `_sync_responsible_activity()` | — | 266 |

### `cas.workflow.history` — کلاس `CasWorkflowHistory`

- منبع: `models/workflow_runtime.py:295`
- inherits: —
- توضیح فنی: CAS Workflow History

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `instance_id` | `Many2one` | — | `cas.workflow.instance` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `event_type` | `Selection` | — | — | True | — | — | — | — |
| `transition_id` | `Many2one` | — | `cas.workflow.transition` | — | — | — | — | — |
| `from_state_id` | `Many2one` | — | `cas.workflow.state` | — | — | — | — | — |
| `to_state_id` | `Many2one` | — | `cas.workflow.state` | True | — | — | — | — |
| `actor_user_id` | `Many2one` | — | `res.users` | True | — | — | — | — |
| `event_at` | `Datetime` | — | — | True | — | — | `fields.Datetime.now` | — |
| `note` | `Text` | — | — | — | — | — | — | — |

**مقادیر Selection/State**

- `event_type`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 315 |
| `write()` | — | 320 |
| `unlink()` | — | 323 |
| `_append_event()` | `api.model` | 327 |

## گروه‌های امنیتی

| XML ID | عنوان | implied groups | فایل |
|---|---|---|---|
| `group_cas_workflow_user` | کاربر گردش‌کار سازمانی | [(4, ref('cas_form_core.group_cas_form_user'))] | `security/cas_workflow_security.xml` |
| `group_cas_workflow_designer` | طراح گردش‌کار سازمانی | [(4, ref('cas_workflow_core.group_cas_workflow_user'))] | `security/cas_workflow_security.xml` |
| `group_cas_workflow_publisher` | منتشرکننده گردش‌کار سازمانی | [(4, ref('cas_workflow_core.group_cas_workflow_designer'))] | `security/cas_workflow_security.xml` |
| `group_cas_workflow_manager` | مدیر گردش‌کار سازمانی | [(4, ref('cas_workflow_core.group_cas_workflow_publisher'))] | `security/cas_workflow_security.xml` |
| `base.group_system` | — | [(4, ref('cas_workflow_core.group_cas_workflow_manager'))] | `security/cas_workflow_security.xml` |

## ماتریس ACL

| ACL | مدل | گروه | Read | Write | Create | Unlink |
|---|---|---|---:|---:|---:|---:|
| `access_workflow_definition_user` | `model_cas_workflow_definition` | `group_cas_workflow_user` | 1 | 0 | 0 | 0 |
| `access_workflow_version_user` | `model_cas_workflow_version` | `group_cas_workflow_user` | 1 | 0 | 0 | 0 |
| `access_workflow_state_user` | `model_cas_workflow_state` | `group_cas_workflow_user` | 1 | 0 | 0 | 0 |
| `access_workflow_transition_user` | `model_cas_workflow_transition` | `group_cas_workflow_user` | 1 | 0 | 0 | 0 |
| `access_workflow_instance_user` | `model_cas_workflow_instance` | `group_cas_workflow_user` | 1 | 1 | 0 | 0 |
| `access_workflow_history_user` | `model_cas_workflow_history` | `group_cas_workflow_user` | 1 | 0 | 0 | 0 |
| `access_workflow_definition_designer` | `model_cas_workflow_definition` | `group_cas_workflow_designer` | 1 | 1 | 1 | 1 |
| `access_workflow_version_designer` | `model_cas_workflow_version` | `group_cas_workflow_designer` | 1 | 1 | 1 | 1 |
| `access_workflow_state_designer` | `model_cas_workflow_state` | `group_cas_workflow_designer` | 1 | 1 | 1 | 1 |
| `access_workflow_transition_designer` | `model_cas_workflow_transition` | `group_cas_workflow_designer` | 1 | 1 | 1 | 1 |
| `access_workflow_instance_manager` | `model_cas_workflow_instance` | `group_cas_workflow_manager` | 1 | 1 | 0 | 0 |
| `access_workflow_history_manager` | `model_cas_workflow_history` | `group_cas_workflow_manager` | 1 | 0 | 0 | 0 |

## Record Ruleها

| XML ID | عنوان | مدل | گروه‌ها | Domain |
|---|---|---|---|---|
| `rule_workflow_definition_company` | گردش‌کار: محدوده شرکت | `model_cas_workflow_definition` | [(4, ref('cas_workflow_core.group_cas_workflow_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_workflow_version_company` | نسخه گردش‌کار: محدوده شرکت | `model_cas_workflow_version` | [(4, ref('cas_workflow_core.group_cas_workflow_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_workflow_state_company` | وضعیت گردش‌کار: محدوده شرکت | `model_cas_workflow_state` | [(4, ref('cas_workflow_core.group_cas_workflow_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_workflow_transition_company` | انتقال گردش‌کار: محدوده شرکت | `model_cas_workflow_transition` | [(4, ref('cas_workflow_core.group_cas_workflow_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_workflow_instance_personal` | نمونه گردش‌کار: آغازکننده یا مسئول | `model_cas_workflow_instance` | [(4, ref('cas_workflow_core.group_cas_workflow_user'))] | `['&', ('company_id', 'in', company_ids), '\|', ('started_by_id', '=', user.id), ('responsible_user_id', '=', user.id)]` |
| `rule_workflow_instance_manager` | نمونه گردش‌کار: مدیر شرکت | `model_cas_workflow_instance` | [(4, ref('cas_workflow_core.group_cas_workflow_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_workflow_history_personal` | تاریخچه گردش‌کار: نمونه قابل مشاهده | `model_cas_workflow_history` | [(4, ref('cas_workflow_core.group_cas_workflow_user'))] | `['&', ('company_id', 'in', company_ids), '\|', ('instance_id.started_by_id', '=', user.id), ('instance_id.responsible_user_id', '=', user.id)]` |
| `rule_workflow_history_manager` | تاریخچه گردش‌کار: مدیر شرکت | `model_cas_workflow_history` | [(4, ref('cas_workflow_core.group_cas_workflow_manager'))] | `[('company_id', 'in', company_ids)]` |

## منوها

| XML ID | عنوان | والد | action | گروه |
|---|---|---|---|---|
| `menu_cas_workflow_instances` | کارتابل گردش‌کار | `cas_form_core.menu_cas_forms_root` | `action_cas_workflow_instance` | `cas_workflow_core.group_cas_workflow_user` |
| `menu_cas_workflow_configuration` | گردش‌کارها | `cas_form_core.menu_cas_forms_configuration` | — | `cas_workflow_core.group_cas_workflow_designer` |
| `menu_cas_workflow_definitions` | تعریف گردش‌کارها | `menu_cas_workflow_configuration` | `action_cas_workflow_definition` | — |
| `menu_cas_workflow_versions` | نسخه‌های گردش‌کار | `menu_cas_workflow_configuration` | `action_cas_workflow_version` | — |

## Actionها

| XML ID | نوع | عنوان | مدل/تگ | view mode | فایل |
|---|---|---|---|---|---|
| `action_cas_workflow_definition` | `ir.actions.act_window` | تعریف گردش‌کارها | `cas.workflow.definition` | `list,form` | `views/cas_workflow_definition_views.xml` |
| `action_cas_workflow_version` | `ir.actions.act_window` | نسخه‌های گردش‌کار | `cas.workflow.version` | `list,form` | `views/cas_workflow_definition_views.xml` |
| `action_cas_workflow_instance` | `ir.actions.act_window` | کارتابل گردش‌کار | `cas.workflow.instance` | `list,form` | `views/cas_workflow_runtime_views.xml` |

## Cron و Sequence

**Sequenceها**

| XML ID | عنوان | code | prefix |
|---|---|---|---|
| `seq_cas_workflow_instance` | شماره گردش‌کار سازمانی | `cas.workflow.instance` | `WF/%(year)s/` |

## Assetهای رابط کاربری

Asset اختصاصی ندارد.

## داده‌های بارگذاری‌شده از manifest

- `data/cas_workflow_sequence.xml`
- `security/cas_workflow_security.xml`
- `security/ir.model.access.csv`
- `views/cas_workflow_definition_views.xml`
- `views/cas_workflow_runtime_views.xml`
- `views/cas_workflow_menus.xml`

## آزمون‌های موجود

- `tests/test_workflow_core.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
