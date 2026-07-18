# مرجع فنی استخراج‌شده از کد: CAS Daily Work Reports

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_work_report` |
| نسخه | `19.0.1.0.0` |
| عنوان | CAS Daily Work Reports |
| خلاصه | Daily employee work reports with stations, representation, approval and Excel |
| دسته | Human Resources |
| نوع برنامه | Application |
| نصب خودکار | — |
| post-init hook | `post_init_hook` |
| uninstall hook | — |
| وابستگی | `hr`, `mail`, `cas_workflow_core`, `cas_approval_core` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 3 | مدل و منطق دامنه |
| `views/` | 5 | نما، action و menu |
| `security/` | 2 | گروه، ACL و record rule |
| `data/` | 1 | داده پایه، sequence و cron |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `cas.work.report.export.wizard` — کلاس `CasWorkReportExportWizard`

- منبع: `models/export_wizard.py:6`
- inherits: —
- توضیح فنی: CAS Work Report Excel Export

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `date_from` | `Date` | از تاریخ | — | — | — | — | — | — |
| `date_to` | `Date` | تا تاریخ | — | — | — | — | — | — |
| `employee_id` | `Many2one` | کارمند | `hr.employee` | — | — | — | — | — |
| `department_id` | `Many2one` | واحد سازمانی | `hr.department` | — | — | — | — | — |
| `work_station_id` | `Many2one` | ایستگاه کاری | `cas.work.station` | — | — | — | — | — |
| `state_code` | `Selection` | وضعیت | — | — | — | — | — | — |

**مقادیر Selection/State**

- `state_code`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `action_export()` | — | 20 |

### `cas.work.station` — کلاس `CasWorkStation`

- منبع: `models/work_report.py:13`
- inherits: `mail.thread`
- توضیح فنی: CAS Work Station

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `sequence` | `Integer` | — | — | — | — | — | `10` | — |
| `name` | `Char` | ایستگاه کاری | — | True | — | True | — | — |
| `code` | `Char` | کد فنی | — | True | — | — | — | — |
| `company_id` | `Many2one` | — | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `department_id` | `Many2one` | واحد میزبان | `hr.department` | True | — | — | — | — |
| `supervisor_user_id` | `Many2one` | سرپرست پیش‌فرض | `res.users` | True | — | True | — | — |
| `normal_shift_hours` | `Float` | ساعات عادی شیفت | — | — | — | — | `8.0` | — |
| `active` | `Boolean` | — | — | — | — | True | `True` | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 47 |
| `write()` | — | 53 |
| `_check_company_contract()` | `api.constrains('company_id', 'department_id', 'supervisor_user_id')` | 59 |

Constraints سمت سرور: `_check_company_contract()`

### `cas.work.report.delegation` — کلاس `CasWorkReportDelegation`

- منبع: `models/work_report.py:68`
- inherits: `mail.thread`
- توضیح فنی: CAS Work Report Representation Permission

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `representative_user_id` | `Many2one` | نماینده ثبت | `res.users` | True | — | — | — | — |
| `company_id` | `Many2one` | — | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `scope` | `Selection` | محدوده نمایندگی | — | True | — | — | `departments` | — |
| `department_ids` | `Many2many` | واحدهای مجاز | `hr.department` | — | — | — | — | — |
| `date_from` | `Date` | از تاریخ | — | True | — | — | `fields.Date.context_today` | — |
| `date_to` | `Date` | تا تاریخ | — | — | — | — | — | — |
| `reason` | `Text` | دلیل نمایندگی | — | True | — | — | — | — |
| `active` | `Boolean` | — | — | — | — | True | `True` | — |

**مقادیر Selection/State**

- `scope`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_check_contract()` | `api.constrains('date_from', 'date_to', 'scope', 'department_ids', 'company_id')` | 96 |
| `allows()` | — | 105 |

Constraints سمت سرور: `_check_contract()`

### `cas.work.report` — کلاس `CasWorkReport`

- منبع: `models/work_report.py:117`
- inherits: `mail.thread`، `mail.activity.mixin`
- توضیح فنی: CAS Daily Work Report

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `number` | `Char` | شماره رهگیری | — | — | True | — | `New` | — |
| `company_id` | `Many2one` | — | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `work_date` | `Date` | تاریخ کار | — | True | — | True | `fields.Date.context_today` | — |
| `employee_id` | `Many2one` | کارمند | `hr.employee` | True | — | True | — | — |
| `employee_department_id` | `Many2one` | واحد سازمانی کارمند | `hr.department` | — | True | — | — | — / True |
| `work_station_id` | `Many2one` | ایستگاه کاری | `cas.work.station` | True | — | True | — | — |
| `station_department_id` | `Many2one` | واحد محل کار | — | — | — | — | — | — / True |
| `supervisor_user_id` | `Many2one` | سرپرست تأییدکننده | `res.users` | True | — | True | — | — |
| `submitted_by_id` | `Many2one` | ثبت‌کننده | `res.users` | — | True | — | — | — |
| `representation_delegation_id` | `Many2one` | مجوز نمایندگی | `cas.work.report.delegation` | — | True | — | — | — |
| `is_representative_entry` | `Boolean` | ثبت به نمایندگی | — | — | True | — | — | — |
| `shift_start` | `Datetime` | شروع کار/شیفت | — | True | — | True | — | — |
| `shift_end` | `Datetime` | پایان کار/شیفت | — | True | — | True | — | — |
| `duration_hours` | `Float` | مدت کار (ساعت) | — | — | — | — | — | _compute_hours / True |
| `normal_hours` | `Float` | ساعات عادی | — | — | — | — | — | _compute_hours / True |
| `overtime_hours` | `Float` | اضافه‌کاری | — | — | — | — | — | _compute_hours / True |
| `submission_deadline` | `Datetime` | مهلت ثبت | — | — | — | — | — | _compute_deadline / True |
| `submitted_at` | `Datetime` | زمان ارسال | — | — | True | — | — | — |
| `is_late` | `Boolean` | ثبت با تأخیر | — | — | True | — | — | — |
| `late_reason` | `Text` | دلیل ثبت با تأخیر | — | — | — | — | — | — |
| `task_title` | `Char` | عنوان فعالیت | — | True | — | True | — | — |
| `description` | `Text` | شرح فعالیت | — | True | — | — | — | — |
| `result` | `Text` | نتیجه/خروجی | — | — | — | — | — | — |
| `issues` | `Text` | مشکلات و موانع | — | — | — | — | — | — |
| `workflow_instance_id` | `Many2one` | — | `cas.workflow.instance` | — | True | — | — | — |
| `state_code` | `Char` | وضعیت | — | — | True | — | — | — / True |
| `state` | `Selection` | وضعیت گزارش | — | — | True | — | — | _compute_state / True |
| `approval_request_id` | `Many2one` | درخواست تأیید | `cas.approval.request` | — | — | — | — | _compute_approval_request / — |
| `authorized_user_ids` | `Many2many` | کاربران مجاز | `res.users` | — | True | — | — | — |

**مقادیر Selection/State**

- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_compute_hours()` | `api.depends('shift_start', 'shift_end', 'work_station_id.normal_shift_hours')` | 164 |
| `_compute_deadline()` | `api.depends('shift_end')` | 175 |
| `_compute_approval_request()` | `api.depends('workflow_instance_id.approval_request_ids', 'workflow_instance_id.approval_request_ids.status')` | 180 |
| `_compute_state()` | `api.depends('state_code')` | 186 |
| `_onchange_work_station_id()` | `api.onchange('work_station_id')` | 191 |
| `_check_shift_range()` | `api.constrains('shift_start', 'shift_end')` | 196 |
| `_check_company_contract()` | `api.constrains('company_id', 'employee_id', 'work_station_id', 'supervisor_user_id')` | 202 |
| `_active_actor_employees()` | `api.model` | 212 |
| `_is_manager_of()` | `api.model` | 218 |
| `_find_representation()` | `api.model` | 231 |
| `_authorize_employee_entry()` | `api.model` | 248 |
| `_authorized_users_for()` | `api.model` | 262 |
| `create()` | `api.model_create_multi` | 276 |
| `write()` | — | 312 |
| `unlink()` | — | 321 |
| `_cas_workflow_authorize_responsible_assignment()` | — | 324 |
| `_cas_workflow_user_can_execute_transition()` | — | 332 |
| `action_submit()` | — | 342 |
| `_xlsx_bytes()` | `api.model` | 371 |

Constraints سمت سرور: `_check_shift_range()`, `_check_company_contract()`

### `افزونه مدل` — کلاس `HrEmployee`

- منبع: `models/work_report.py:407`
- inherits: `hr.employee`
- توضیح فنی: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `write()` | — | 410 |

## گروه‌های امنیتی

| XML ID | عنوان | implied groups | فایل |
|---|---|---|---|
| `group_cas_work_report_user` | کاربر گزارش کار | [(4, ref('cas_workflow_core.group_cas_workflow_user')), (4, ref('cas_approval_core.group_cas_approval_user'))] | `security/cas_work_report_security.xml` |
| `group_cas_work_report_supervisor` | سرپرست گزارش کار | [(4, ref('group_cas_work_report_user'))] | `security/cas_work_report_security.xml` |
| `group_cas_work_report_manager` | مدیر گزارش کار | [(4, ref('group_cas_work_report_supervisor'))] | `security/cas_work_report_security.xml` |
| `base.group_system` | — | [(4, ref('cas_work_report.group_cas_work_report_manager'))] | `security/cas_work_report_security.xml` |

## ماتریس ACL

| ACL | مدل | گروه | Read | Write | Create | Unlink |
|---|---|---|---:|---:|---:|---:|
| `access_cas_work_station_user` | `model_cas_work_station` | `group_cas_work_report_user` | 1 | 0 | 0 | 0 |
| `access_cas_work_station_manager` | `model_cas_work_station` | `group_cas_work_report_manager` | 1 | 1 | 1 | 0 |
| `access_cas_work_report_user` | `model_cas_work_report` | `group_cas_work_report_user` | 1 | 1 | 1 | 0 |
| `access_cas_work_report_manager` | `model_cas_work_report` | `group_cas_work_report_manager` | 1 | 1 | 1 | 0 |
| `access_cas_work_report_delegation_user` | `model_cas_work_report_delegation` | `group_cas_work_report_user` | 1 | 0 | 0 | 0 |
| `access_cas_work_report_delegation_manager` | `model_cas_work_report_delegation` | `group_cas_work_report_manager` | 1 | 1 | 1 | 0 |
| `access_cas_work_report_export_wizard` | `model_cas_work_report_export_wizard` | `group_cas_work_report_user` | 1 | 1 | 1 | 1 |

## Record Ruleها

| XML ID | عنوان | مدل | گروه‌ها | Domain |
|---|---|---|---|---|
| `rule_cas_work_station_company` | ایستگاه‌های شرکت‌های مجاز | `model_cas_work_station` | [(4, ref('group_cas_work_report_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_cas_work_report_scope` | گزارش‌های حوزه سازمانی مجاز | `model_cas_work_report` | [(4, ref('group_cas_work_report_user'))] | `[('company_id', 'in', company_ids), ('authorized_user_ids', 'in', user.id)]` |
| `rule_cas_work_report_manager` | مدیر گزارش کار در شرکت‌های مجاز | `model_cas_work_report` | [(4, ref('group_cas_work_report_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_cas_work_report_delegation_user` | مجوزهای نمایندگی کاربر | `model_cas_work_report_delegation` | [(4, ref('group_cas_work_report_user'))] | `[('company_id', 'in', company_ids), ('representative_user_id', '=', user.id)]` |
| `rule_cas_work_report_delegation_manager` | مدیریت مجوزهای نمایندگی شرکت | `model_cas_work_report_delegation` | [(4, ref('group_cas_work_report_manager'))] | `[('company_id', 'in', company_ids)]` |

## منوها

| XML ID | عنوان | والد | action | گروه |
|---|---|---|---|---|
| `menu_cas_work_report_root` | گزارش کار | — | — | `group_cas_work_report_user` |
| `menu_cas_my_work_report` | گزارش‌های من | `menu_cas_work_report_root` | `action_cas_my_work_report` | — |
| `menu_cas_work_report_all` | گزارش‌های حوزه من | `menu_cas_work_report_root` | `action_cas_work_report` | — |
| `menu_cas_work_report_export` | خروجی Excel | `menu_cas_work_report_root` | `action_cas_work_report_export` | — |
| `menu_cas_work_report_config` | پیکربندی | `menu_cas_work_report_root` | — | `group_cas_work_report_manager` |
| `menu_cas_work_station` | ایستگاه‌های کاری | `menu_cas_work_report_config` | `action_cas_work_station` | — |
| `menu_cas_work_report_delegation` | مجوزهای نمایندگی | `menu_cas_work_report_config` | `action_cas_work_report_delegation` | — |

## Actionها

| XML ID | نوع | عنوان | مدل/تگ | view mode | فایل |
|---|---|---|---|---|---|
| `action_cas_work_report_delegation` | `ir.actions.act_window` | مجوزهای ثبت به نمایندگی | `cas.work.report.delegation` | `list,form` | `views/cas_work_report_delegation_views.xml` |
| `action_cas_work_report_export` | `ir.actions.act_window` | خروجی Excel | `cas.work.report.export.wizard` | `form` | `views/cas_work_report_export_views.xml` |
| `action_cas_work_report` | `ir.actions.act_window` | گزارش‌های کار | `cas.work.report` | `list,form` | `views/cas_work_report_views.xml` |
| `action_cas_my_work_report` | `ir.actions.act_window` | گزارش‌های من | `cas.work.report` | `list,form` | `views/cas_work_report_views.xml` |
| `action_cas_work_station` | `ir.actions.act_window` | ایستگاه‌های کاری | `cas.work.station` | `list,form` | `views/cas_work_station_views.xml` |

## Cron و Sequence

**Sequenceها**

| XML ID | عنوان | code | prefix |
|---|---|---|---|
| `seq_cas_work_report` | CAS Work Report | `cas.work.report` | `WR/%(year)s/` |

## Assetهای رابط کاربری

Asset اختصاصی ندارد.

## داده‌های بارگذاری‌شده از manifest

- `security/cas_work_report_security.xml`
- `security/ir.model.access.csv`
- `data/cas_work_report_sequence.xml`
- `views/cas_work_station_views.xml`
- `views/cas_work_report_delegation_views.xml`
- `views/cas_work_report_views.xml`
- `views/cas_work_report_export_views.xml`
- `views/cas_work_report_menus.xml`

## آزمون‌های موجود

- `tests/test_work_report.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
