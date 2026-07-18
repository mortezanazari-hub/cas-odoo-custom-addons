# مرجع فنی استخراج‌شده از کد: CAS Approval Core

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_approval_core` |
| نسخه | `19.0.1.0.2` |
| عنوان | CAS Approval Core |
| خلاصه | Versioned approval policies and auditable decisions for CAS workflows |
| دسته | Productivity |
| نوع برنامه | Technical/Extension |
| نصب خودکار | — |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `cas_workflow_core`, `mail`, `hr` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 4 | مدل و منطق دامنه |
| `views/` | 4 | نما، action و menu |
| `security/` | 2 | گروه، ACL و record rule |
| `data/` | 1 | داده پایه، sequence و cron |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `cas.approval.delegation` — کلاس `CasApprovalDelegation`

- منبع: `models/approval_delegation.py:9`
- inherits: `mail.thread`
- توضیح فنی: CAS Approval Delegation

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `delegator_user_id` | `Many2one` | تفویض‌کننده | `res.users` | True | — | True | — | — |
| `delegate_user_id` | `Many2one` | جانشین | `res.users` | True | — | True | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `date_from` | `Date` | از تاریخ | — | True | — | — | `fields.Date.context_today` | — |
| `date_to` | `Date` | تا تاریخ | — | — | — | — | — | — |
| `policy_ids` | `Many2many` | سیاست‌های محدودشده | `cas.approval.policy` | — | — | — | — | — |
| `reason` | `Text` | دلیل جانشینی | — | True | — | — | — | — |
| `active` | `Boolean` | — | — | — | — | True | `True` | — |
| `decision_line_ids` | `One2many` | تصمیم‌های استفاده‌شده | `cas.approval.line` | — | True | — | — | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_check_delegation_contract()` | `api.constrains('delegator_user_id', 'delegate_user_id', 'company_id', 'date_from', 'date_to', 'policy_ids', 'active')` | 69 |
| `_check_overlap()` | — | 86 |
| `write()` | — | 105 |
| `unlink()` | — | 121 |
| `_find_for()` | `api.model` | 127 |

Constraints سمت سرور: `_check_delegation_contract()`

### `cas.approval.policy` — کلاس `CasApprovalPolicy`

- منبع: `models/approval_policy.py:14`
- inherits: `cas.workflow.versioned.mixin`
- توضیح فنی: CAS Approval Policy

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `sequence` | `Integer` | — | — | — | — | — | `10` | — |
| `name` | `Char` | عنوان سیاست تأیید | — | True | — | — | — | — |
| `code` | `Char` | کد فنی | — | True | — | — | — | — |
| `state_id` | `Many2one` | مرحله گردش‌کار | `cas.workflow.state` | True | — | — | — | — |
| `approve_transition_id` | `Many2one` | انتقال پس از تأیید | `cas.workflow.transition` | True | — | — | — | — |
| `reject_transition_id` | `Many2one` | انتقال پس از رد | `cas.workflow.transition` | — | — | — | — | — |
| `execution_mode` | `Selection` | روش اجرا | — | True | — | — | `parallel` | — |
| `decision_rule` | `Selection` | قاعده تصمیم | — | True | — | — | `all` | — |
| `quorum_count` | `Integer` | حد نصاب تأیید | — | — | — | — | `1` | — |
| `step_ids` | `One2many` | تأییدکنندگان | `cas.approval.step` | — | — | — | — | — |

**مقادیر Selection/State**

- `execution_mode`: —
- `decision_rule`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 69 |
| `write()` | — | 75 |
| `_check_policy_contract()` | `api.constrains('code', 'version_id', 'state_id', 'approve_transition_id', 'reject_transition_id', 'decision_rule', 'quorum_count')` | 89 |
| `_validate_definition()` | — | 95 |
| `_schema_payload()` | — | 115 |

Constraints سمت سرور: `_check_policy_contract()`

### `cas.approval.step` — کلاس `CasApprovalStep`

- منبع: `models/approval_policy.py:129`
- inherits: —
- توضیح فنی: CAS Approval Step

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `policy_id` | `Many2one` | — | `cas.approval.policy` | True | — | — | — | — |
| `version_id` | `Many2one` | — | — | — | True | — | — | — / True |
| `company_id` | `Many2one` | — | — | — | True | — | — | — / True |
| `sequence` | `Integer` | — | — | — | — | — | `10` | — |
| `name` | `Char` | عنوان گام تأیید | — | True | — | — | — | — |
| `role_label` | `Char` | نقش سازمانی | — | True | — | — | — | — |
| `approver_type` | `Selection` | نوع تأییدکننده | — | True | — | — | `user` | — |
| `approver_user_id` | `Many2one` | کاربر تأییدکننده | `res.users` | — | — | — | — | — |
| `approver_group_id` | `Many2one` | گروه تأییدکننده | `res.groups` | — | — | — | — | — |
| `deadline_hours` | `Float` | مهلت تصمیم (ساعت) | — | — | — | — | — | — |

**مقادیر Selection/State**

- `approver_type`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 175 |
| `write()` | — | 183 |
| `unlink()` | — | 190 |
| `_check_approver_contract()` | `api.constrains('approver_type', 'approver_user_id', 'approver_group_id')` | 196 |
| `_validate_definition()` | — | 200 |
| `_schema_payload()` | — | 218 |

Constraints سمت سرور: `_check_approver_contract()`

### `افزونه مدل` — کلاس `CasWorkflowVersion`

- منبع: `models/approval_policy.py:235`
- inherits: `cas.workflow.version`
- توضیح فنی: —

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `approval_policy_ids` | `One2many` | سیاست‌های تأیید | `cas.approval.policy` | — | — | — | — | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_schema_payload()` | — | 242 |
| `_validate_publishable()` | — | 249 |
| `action_new_revision()` | — | 255 |

### `cas.approval.request` — کلاس `CasApprovalRequest`

- منبع: `models/approval_runtime.py:11`
- inherits: `mail.thread`، `mail.activity.mixin`
- توضیح فنی: CAS Approval Request

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `number` | `Char` | — | — | — | True | — | `New` | — |
| `instance_id` | `Many2one` | — | `cas.workflow.instance` | True | — | — | — | — |
| `policy_id` | `Many2one` | — | `cas.approval.policy` | True | — | — | — | — |
| `state_id` | `Many2one` | — | `cas.workflow.state` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | True | — | — | — / True |
| `status` | `Selection` | — | — | True | True | True | `pending` | — |
| `execution_mode` | `Selection` | — | — | True | True | — | — | — |
| `decision_rule` | `Selection` | — | — | True | True | — | — | — |
| `quorum_count` | `Integer` | — | — | — | True | — | — | — |
| `requested_at` | `Datetime` | — | — | True | True | — | — | — |
| `completed_at` | `Datetime` | — | — | — | True | — | — | — |
| `outcome_transition_id` | `Many2one` | — | `cas.workflow.transition` | — | True | — | — | — |
| `line_ids` | `One2many` | — | `cas.approval.line` | — | — | — | — | — |
| `history_ids` | `One2many` | — | `cas.approval.history` | — | — | — | — | — |

**مقادیر Selection/State**

- `status`: —
- `execution_mode`: —
- `decision_rule`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 68 |
| `write()` | — | 73 |
| `unlink()` | — | 78 |
| `_start_for_instance()` | `api.model` | 82 |
| `_resolve_step_users()` | `api.model` | 165 |
| `_resolve_manager_user()` | `api.model` | 197 |
| `_activate_next_sequence()` | — | 233 |
| `_evaluate()` | — | 253 |
| `_complete()` | — | 281 |
| `_sync_activities()` | — | 320 |

### `cas.approval.line` — کلاس `CasApprovalLine`

- منبع: `models/approval_runtime.py:326`
- inherits: `mail.thread`، `mail.activity.mixin`
- توضیح فنی: CAS Approval Decision Line

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `request_id` | `Many2one` | — | `cas.approval.request` | True | — | — | — | — |
| `step_id` | `Many2one` | — | `cas.approval.step` | True | — | — | — | — |
| `instance_id` | `Many2one` | — | — | — | True | — | — | — / True |
| `state_id` | `Many2one` | — | — | — | True | — | — | — / True |
| `company_id` | `Many2one` | — | — | — | True | — | — | — / True |
| `sequence` | `Integer` | — | — | True | True | — | — | — |
| `role_label` | `Char` | نقش تأیید | — | True | True | — | — | — |
| `approver_user_id` | `Many2one` | تأییدکننده منصوب | `res.users` | True | — | — | — | — |
| `delegate_user_id` | `Many2one` | جانشین | `res.users` | — | True | — | — | — |
| `delegation_id` | `Many2one` | مجوز جانشینی | `cas.approval.delegation` | — | True | — | — | — |
| `decision_user_id` | `Many2one` | تصمیم‌گیرنده واقعی | `res.users` | — | True | — | — | — |
| `status` | `Selection` | — | — | True | True | True | — | — |
| `assigned_at` | `Datetime` | — | — | — | True | — | — | — |
| `decided_at` | `Datetime` | — | — | — | True | — | — | — |
| `deadline` | `Datetime` | — | — | — | True | — | — | — |
| `delay_hours` | `Float` | تأخیر تصمیم (ساعت) | — | — | True | — | — | — |
| `comment` | `Text` | نظر تصمیم‌گیرنده | — | — | True | — | — | — |
| `rejection_reason` | `Text` | دلیل رد | — | — | True | — | — | — |

**مقادیر Selection/State**

- `status`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 387 |
| `write()` | — | 392 |
| `unlink()` | — | 397 |
| `_check_decision_access()` | — | 400 |
| `action_approve()` | — | 412 |
| `action_open_reject_wizard()` | — | 419 |
| `action_reject()` | — | 432 |
| `_record_decision()` | — | 441 |
| `_sync_activity()` | — | 467 |

### `cas.approval.history` — کلاس `CasApprovalHistory`

- منبع: `models/approval_runtime.py:501`
- inherits: —
- توضیح فنی: CAS Approval Immutable History

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `request_id` | `Many2one` | — | `cas.approval.request` | True | — | — | — | — |
| `line_id` | `Many2one` | — | `cas.approval.line` | — | — | — | — | — |
| `instance_id` | `Many2one` | — | — | — | True | — | — | — / True |
| `company_id` | `Many2one` | — | — | — | True | — | — | — / True |
| `event_type` | `Selection` | — | — | True | — | — | — | — |
| `actor_user_id` | `Many2one` | — | `res.users` | True | — | — | — | — |
| `event_at` | `Datetime` | — | — | True | — | — | `fields.Datetime.now` | — |
| `note` | `Text` | — | — | — | — | — | — | — |

**مقادیر Selection/State**

- `event_type`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 534 |
| `write()` | — | 539 |
| `unlink()` | — | 542 |
| `_append_event()` | `api.model` | 546 |

### `cas.approval.reject.wizard` — کلاس `CasApprovalRejectWizard`

- منبع: `models/approval_runtime.py:559`
- inherits: —
- توضیح فنی: CAS Approval Rejection Wizard

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `line_id` | `Many2one` | تصمیم تأیید | `cas.approval.line` | True | True | — | — | — |
| `reason` | `Text` | دلیل رد | — | True | — | — | — | — |
| `comment` | `Text` | توضیحات تکمیلی | — | — | — | — | — | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `action_confirm()` | — | 569 |

### `افزونه مدل` — کلاس `CasWorkflowInstance`

- منبع: `models/approval_runtime.py:575`
- inherits: `cas.workflow.instance`
- توضیح فنی: —

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `approval_request_ids` | `One2many` | درخواست‌های تأیید | `cas.approval.request` | — | — | — | — | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_start_instance()` | `api.model` | 583 |
| `action_execute_transition()` | — | 591 |
| `_ensure_approval_for_current_state()` | — | 631 |

## گروه‌های امنیتی

| XML ID | عنوان | implied groups | فایل |
|---|---|---|---|
| `group_cas_approval_user` | کاربر تأیید سازمانی | [(4, ref('cas_workflow_core.group_cas_workflow_user'))] | `security/cas_approval_security.xml` |
| `group_cas_approval_manager` | مدیر تأیید سازمانی | [(4, ref('cas_approval_core.group_cas_approval_user')), (4, ref('cas_workflow_core.group_cas_workflow_manager'))] | `security/cas_approval_security.xml` |
| `base.group_system` | — | [(4, ref('cas_approval_core.group_cas_approval_manager'))] | `security/cas_approval_security.xml` |

## ماتریس ACL

| ACL | مدل | گروه | Read | Write | Create | Unlink |
|---|---|---|---:|---:|---:|---:|
| `access_approval_policy_user` | `model_cas_approval_policy` | `group_cas_approval_user` | 1 | 0 | 0 | 0 |
| `access_approval_step_user` | `model_cas_approval_step` | `group_cas_approval_user` | 1 | 0 | 0 | 0 |
| `access_approval_delegation_user` | `model_cas_approval_delegation` | `group_cas_approval_user` | 1 | 0 | 0 | 0 |
| `access_approval_request_user` | `model_cas_approval_request` | `group_cas_approval_user` | 1 | 0 | 0 | 0 |
| `access_approval_line_user` | `model_cas_approval_line` | `group_cas_approval_user` | 1 | 0 | 0 | 0 |
| `access_approval_history_user` | `model_cas_approval_history` | `group_cas_approval_user` | 1 | 0 | 0 | 0 |
| `access_approval_policy_designer` | `model_cas_approval_policy` | `cas_workflow_core.group_cas_workflow_designer` | 1 | 1 | 1 | 1 |
| `access_approval_step_designer` | `model_cas_approval_step` | `cas_workflow_core.group_cas_workflow_designer` | 1 | 1 | 1 | 1 |
| `access_approval_request_manager` | `model_cas_approval_request` | `group_cas_approval_manager` | 1 | 0 | 0 | 0 |
| `access_approval_line_manager` | `model_cas_approval_line` | `group_cas_approval_manager` | 1 | 0 | 0 | 0 |
| `access_approval_history_manager` | `model_cas_approval_history` | `group_cas_approval_manager` | 1 | 0 | 0 | 0 |
| `access_approval_delegation_manager` | `model_cas_approval_delegation` | `group_cas_approval_manager` | 1 | 1 | 1 | 1 |
| `access_approval_reject_wizard_user` | `model_cas_approval_reject_wizard` | `group_cas_approval_user` | 1 | 1 | 1 | 1 |

## Record Ruleها

| XML ID | عنوان | مدل | گروه‌ها | Domain |
|---|---|---|---|---|
| `rule_approval_policy_company` | سیاست تأیید: محدوده شرکت | `model_cas_approval_policy` | [(4, ref('cas_approval_core.group_cas_approval_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_approval_step_company` | گام تأیید: محدوده شرکت | `model_cas_approval_step` | [(4, ref('cas_approval_core.group_cas_approval_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_approval_delegation_user` | جانشینی تأیید: تفویض‌کننده یا جانشین | `model_cas_approval_delegation` | [(4, ref('cas_approval_core.group_cas_approval_user'))] | `['&', ('company_id', 'in', company_ids), '\|', ('delegator_user_id', '=', user.id), ('delegate_user_id', '=', user.id)]` |
| `rule_approval_delegation_manager` | جانشینی تأیید: مدیر شرکت | `model_cas_approval_delegation` | [(4, ref('cas_approval_core.group_cas_approval_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_approval_request_user` | درخواست تأیید: ذی‌نفع یا تأییدکننده | `model_cas_approval_request` | [(4, ref('cas_approval_core.group_cas_approval_user'))] | `['&', ('company_id', 'in', company_ids), '\|', '\|', '\|', ('instance_id.started_by_id', '=', user.id), ('instance_id.responsible_user_id', '=', user.id), ('line_ids.approver_user_id', '=', user.id), ('line_ids.delegate_user_id', '=', user.id)]` |
| `rule_approval_request_manager` | درخواست تأیید: مدیر شرکت | `model_cas_approval_request` | [(4, ref('cas_approval_core.group_cas_approval_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_approval_line_user` | خط تأیید: ذی‌نفع یا تأییدکننده | `model_cas_approval_line` | [(4, ref('cas_approval_core.group_cas_approval_user'))] | `['&', ('company_id', 'in', company_ids), '\|', '\|', '\|', ('approver_user_id', '=', user.id), ('delegate_user_id', '=', user.id), ('instance_id.started_by_id', '=', user.id), ('instance_id.responsible_user_id', '=', user.id)]` |
| `rule_approval_line_manager` | خط تأیید: مدیر شرکت | `model_cas_approval_line` | [(4, ref('cas_approval_core.group_cas_approval_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_approval_history_user` | تاریخچه تأیید: درخواست قابل مشاهده | `model_cas_approval_history` | [(4, ref('cas_approval_core.group_cas_approval_user'))] | `['&', ('company_id', 'in', company_ids), '\|', '\|', '\|', ('request_id.instance_id.started_by_id', '=', user.id), ('request_id.instance_id.responsible_user_id', '=', user.id), ('request_id.line_ids.approver_user_id', '=', user.id), ('request_id.line_ids.delegate_user_id', '=', user.id)]` |
| `rule_approval_history_manager` | تاریخچه تأیید: مدیر شرکت | `model_cas_approval_history` | [(4, ref('cas_approval_core.group_cas_approval_manager'))] | `[('company_id', 'in', company_ids)]` |

## منوها

| XML ID | عنوان | والد | action | گروه |
|---|---|---|---|---|
| `menu_cas_approval_inbox` | کارتابل تأیید | `cas_form_core.menu_cas_forms_root` | `action_cas_approval_inbox` | `cas_approval_core.group_cas_approval_user` |
| `menu_cas_approval_requests` | درخواست‌های تأیید | `cas_form_core.menu_cas_forms_root` | `action_cas_approval_request` | `cas_approval_core.group_cas_approval_user` |
| `menu_cas_approval_policies` | سیاست‌های تأیید | `cas_workflow_core.menu_cas_workflow_configuration` | `action_cas_approval_policy` | `cas_workflow_core.group_cas_workflow_designer` |
| `menu_cas_approval_delegations` | جانشینی تأییدها | `cas_workflow_core.menu_cas_workflow_configuration` | `action_cas_approval_delegation` | `cas_approval_core.group_cas_approval_manager` |

## Actionها

| XML ID | نوع | عنوان | مدل/تگ | view mode | فایل |
|---|---|---|---|---|---|
| `action_cas_approval_delegation` | `ir.actions.act_window` | جانشینی تأییدها | `cas.approval.delegation` | `list,form` | `views/cas_approval_delegation_views.xml` |
| `action_cas_approval_policy` | `ir.actions.act_window` | سیاست‌های تأیید | `cas.approval.policy` | `list,form` | `views/cas_approval_policy_views.xml` |
| `action_cas_approval_request` | `ir.actions.act_window` | درخواست‌های تأیید | `cas.approval.request` | `list,form` | `views/cas_approval_runtime_views.xml` |
| `action_cas_approval_inbox` | `ir.actions.act_window` | کارتابل تأیید | `cas.approval.line` | `list,form` | `views/cas_approval_runtime_views.xml` |

## Cron و Sequence

**Sequenceها**

| XML ID | عنوان | code | prefix |
|---|---|---|---|
| `seq_cas_approval_request` | درخواست تأیید CAS | `cas.approval.request` | `APR/%(year)s/` |

## Assetهای رابط کاربری

Asset اختصاصی ندارد.

## داده‌های بارگذاری‌شده از manifest

- `data/cas_approval_sequence.xml`
- `security/cas_approval_security.xml`
- `security/ir.model.access.csv`
- `views/cas_approval_policy_views.xml`
- `views/cas_approval_delegation_views.xml`
- `views/cas_approval_runtime_views.xml`
- `views/cas_approval_menus.xml`

## آزمون‌های موجود

- `tests/test_approval_core.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
