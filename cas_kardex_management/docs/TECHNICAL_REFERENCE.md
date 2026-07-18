# مرجع فنی استخراج‌شده از کد: CAS Kardex Management

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_kardex_management` |
| نسخه | `19.0.1.0.1` |
| عنوان | CAS Kardex Management |
| خلاصه | Minute-accurate attendance kardex, requests, overtime and monthly locks |
| دسته | Human Resources |
| نوع برنامه | Application |
| نصب خودکار | — |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `cas_attendance_core`, `mail` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 5 | مدل و منطق دامنه |
| `views/` | 5 | نما، action و menu |
| `security/` | 2 | گروه، ACL و record rule |
| `data/` | 1 | داده پایه، sequence و cron |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `cas.attendance.request` — کلاس `CasAttendanceRequest`

- منبع: `models/attendance_request.py:7`
- inherits: `mail.thread`، `mail.activity.mixin`، `cas.kardex.approval.mixin`
- توضیح فنی: CAS Leave or Mission Request

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `number` | `Char` | شماره | — | — | True | — | `New` | — |
| `employee_id` | `Many2one` | کارمند | `hr.employee` | True | — | True | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `request_type` | `Selection` | نوع درخواست | — | True | — | True | — | — |
| `duration_type` | `Selection` | نوع مدت | — | True | — | — | `hourly` | — |
| `date_from` | `Date` | از روز | — | True | — | — | — | — |
| `date_to` | `Date` | تا روز | — | True | — | — | — | — |
| `datetime_from` | `Datetime` | از ساعت | — | — | — | — | — | — |
| `datetime_to` | `Datetime` | تا ساعت | — | — | — | — | — | — |
| `requested_minutes` | `Integer` | دقایق پوشش تعهد | — | — | — | — | — | _compute_requested_minutes / True |
| `reason` | `Text` | دلیل / شرح | — | True | — | — | — | — |
| `source_attendance_day_id` | `Many2one` | روز حضور مبدأ | `cas.attendance.day` | — | — | — | — | — |
| `approver_user_id` | `Many2one` | تأییدکننده | `res.users` | — | True | — | — | — |
| `approver_role` | `Selection` | مسیر تأیید | — | — | True | — | — | — |
| `state` | `Selection` | وضعیت | — | True | True | True | `draft` | — |
| `submitted_at` | `Datetime` | — | — | — | True | — | — | — |
| `decided_at` | `Datetime` | — | — | — | True | — | — | — |
| `decision_user_id` | `Many2one` | — | `res.users` | — | True | — | — | — |
| `decision_note` | `Text` | توضیح تصمیم | — | — | — | — | — | — |

**مقادیر Selection/State**

- `request_type`: —
- `duration_type`: —
- `approver_role`: —
- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 37 |
| `_compute_requested_minutes()` | `api.depends('duration_type', 'date_from', 'date_to', 'datetime_from', 'datetime_to', 'employee_id')` | 44 |
| `_check_request_range()` | `api.constrains('date_from', 'date_to', 'duration_type', 'datetime_from', 'datetime_to', 'employee_id')` | 56 |
| `write()` | — | 71 |
| `unlink()` | — | 84 |
| `action_submit()` | — | 89 |
| `_check_approver()` | — | 97 |
| `action_approve()` | — | 104 |
| `action_reject()` | — | 110 |
| `action_cancel()` | — | 117 |

Constraints سمت سرور: `_check_request_range()`

### `افزونه مدل` — کلاس `ResCompany`

- منبع: `models/company_config.py:5`
- inherits: `res.company`
- توضیح فنی: —

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `cas_ceo_user_id` | `Many2one` | مدیرعامل برای تأییدهای کاردکس | `res.users` | — | — | — | — | — |
| `cas_kardex_lock_day` | `Integer` | روز قفل کاردکس ماه قبل | — | — | — | — | `4` | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_check_cas_kardex_config()` | `api.constrains('cas_kardex_lock_day', 'cas_ceo_user_id')` | 15 |

Constraints سمت سرور: `_check_cas_kardex_config()`

### `cas.kardex.approval.mixin` — کلاس `CasKardexApprovalMixin`

- منبع: `models/company_config.py:24`
- inherits: —
- توضیح فنی: CAS Kardex Approval Routing

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_cas_manager_or_ceo()` | `api.model` | 29 |
| `_cas_require_ceo()` | — | 52 |

### `cas.kardex.period` — کلاس `CasKardexPeriod`

- منبع: `models/kardex.py:10`
- inherits: `mail.thread`، `cas.kardex.approval.mixin`
- توضیح فنی: CAS Monthly Kardex Lock

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `month_start` | `Date` | ماه | — | True | — | — | — | — |
| `month_end` | `Date` | پایان ماه | — | — | — | — | — | _compute_dates / True |
| `lock_deadline` | `Datetime` | مهلت ویرایش | — | — | — | — | — | _compute_dates / True |
| `state` | `Selection` | وضعیت | — | True | True | True | `open` | — |
| `locked_at` | `Datetime` | — | — | — | True | — | — | — |
| `locked_by_id` | `Many2one` | — | `res.users` | — | True | — | — | — |
| `reopen_ids` | `One2many` | مجوزهای بازگشایی | `cas.kardex.reopen` | — | — | — | — | — |

**مقادیر Selection/State**

- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_compute_dates()` | `api.depends('month_start', 'company_id.cas_kardex_lock_day')` | 28 |
| `_check_month()` | `api.constrains('month_start')` | 40 |
| `period_for()` | `api.model` | 46 |
| `action_lock()` | — | 53 |
| `_cron_lock_due_periods()` | `api.model` | 60 |
| `allows_edit()` | — | 66 |

Constraints سمت سرور: `_check_month()`

### `cas.kardex.reopen` — کلاس `CasKardexReopen`

- منبع: `models/kardex.py:73`
- inherits: `mail.thread`، `cas.kardex.approval.mixin`
- توضیح فنی: CAS Scoped Kardex Reopening

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `period_id` | `Many2one` | دوره قفل‌شده | `cas.kardex.period` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `scope` | `Selection` | محدوده | — | True | — | — | `employees` | — |
| `employee_ids` | `Many2many` | کارکنان | `hr.employee` | — | — | — | — | — |
| `date_from` | `Date` | از تاریخ | — | True | — | — | — | — |
| `date_to` | `Date` | تا تاریخ | — | True | — | — | — | — |
| `reason` | `Text` | دستور و دلیل مدیرعامل | — | True | — | — | — | — |
| `active` | `Boolean` | — | — | — | True | True | `True` | — |
| `opened_by_id` | `Many2one` | — | `res.users` | — | True | — | — | — |
| `opened_at` | `Datetime` | — | — | — | True | — | — | — |
| `closed_by_id` | `Many2one` | — | `res.users` | — | True | — | — | — |
| `closed_at` | `Datetime` | — | — | — | True | — | — | — |

**مقادیر Selection/State**

- `scope`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 93 |
| `_check_scope()` | `api.constrains('period_id', 'date_from', 'date_to', 'scope', 'employee_ids')` | 101 |
| `action_close()` | — | 110 |
| `unlink()` | — | 115 |

Constraints سمت سرور: `_check_scope()`

### `cas.kardex.day` — کلاس `CasKardexDay`

- منبع: `models/kardex.py:119`
- inherits: `mail.thread`
- توضیح فنی: CAS Minute Accurate Daily Kardex

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `employee_id` | `Many2one` | کارمند | `hr.employee` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `work_date` | `Date` | روز کاردکس | — | True | — | — | — | — |
| `attendance_day_id` | `Many2one` | نتیجه حضور | `cas.attendance.day` | True | — | — | — | — |
| `shift_day_id` | `Many2one` | برنامه شیفت | — | — | True | — | — | — / True |
| `period_id` | `Many2one` | دوره | `cas.kardex.period` | True | — | — | — | — |
| `day_kind` | `Selection` | نوع روز | — | — | True | — | — | — / True |
| `planned_base_minutes` | `Integer` | موظفی برنامه | — | — | True | — | — | — |
| `planned_break_minutes` | `Integer` | استراحت برنامه | — | — | True | — | — | — |
| `planned_presence_minutes` | `Integer` | حضور برنامه | — | — | True | — | — | — |
| `presence_minutes` | `Integer` | حضور واقعی | — | — | True | — | — | — |
| `deducted_break_minutes` | `Integer` | استراحت کسرشده | — | — | True | — | — | — |
| `net_work_minutes` | `Integer` | کار خالص واقعی | — | — | True | — | — | — |
| `leave_minutes` | `Integer` | مرخصی تأییدشده | — | — | True | — | — | — |
| `mission_minutes` | `Integer` | مأموریت تأییدشده | — | — | True | — | — | — |
| `credited_base_minutes` | `Integer` | موظفی پوشش‌داده‌شده | — | — | True | — | — | — |
| `absence_minutes` | `Integer` | کسری / غیبت | — | — | True | — | — | — |
| `tardy_minutes` | `Integer` | تأخیر ورود | — | — | True | — | — | — |
| `early_exit_minutes` | `Integer` | تعجیل خروج | — | — | True | — | — | — |
| `mandatory_overtime_minutes` | `Integer` | اضافه‌کاری اجباری برنامه | — | — | True | — | — | — |
| `discretionary_overtime_minutes` | `Integer` | اضافه‌کاری نیازمند مجوز | — | — | True | — | — | — |
| `approved_overtime_minutes` | `Integer` | اضافه‌کاری اختیاری نهایی | — | — | True | — | — | — |
| `holiday_work_minutes` | `Integer` | کار در روز تعطیل | — | — | True | — | — | — |
| `break_waiver_state` | `Selection` | تصمیم استراحت | — | — | True | True | `none` | — |
| `break_waiver_reason` | `Text` | دلیل تصمیم استراحت | — | — | — | — | — | — |
| `break_waiver_by_id` | `Many2one` | — | `res.users` | — | True | — | — | — |
| `break_waiver_at` | `Datetime` | — | — | — | True | — | — | — |
| `state` | `Selection` | وضعیت | — | True | True | — | `draft` | — |

**مقادیر Selection/State**

- `day_kind`: —
- `break_waiver_state`: —
- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_get_or_create()` | `api.model` | 157 |
| `create()` | `api.model_create_multi` | 168 |
| `_check_editable()` | — | 173 |
| `write()` | — | 178 |
| `unlink()` | — | 186 |
| `_approved_coverage()` | — | 189 |
| `recompute()` | — | 205 |
| `recompute_range()` | `api.model` | 253 |
| `action_approve_break_waiver()` | — | 261 |
| `action_reject_break_waiver()` | — | 270 |

### `افزونه مدل` — کلاس `CasAttendanceDay`

- منبع: `models/kardex.py:278`
- inherits: `cas.attendance.day`
- توضیح فنی: —

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `kardex_day_id` | `One2many` | کاردکس | `cas.kardex.day` | — | True | — | — | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `recompute()` | — | 283 |
| `action_new_attendance_request()` | — | 290 |

### `cas.overtime.authorization` — کلاس `CasOvertimeAuthorization`

- منبع: `models/overtime.py:7`
- inherits: `mail.thread`، `cas.kardex.approval.mixin`
- توضیح فنی: CAS CEO Overtime Auto Approval Authorization

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `employee_id` | `Many2one` | کارمند | `hr.employee` | True | — | True | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `grant_scope` | `Selection` | شروع اثر | — | True | — | — | `grant_date` | — |
| `effective_from` | `Date` | تاریخ شروع اثر | — | True | True | — | — | — |
| `date_to` | `Date` | تاریخ پایان | — | — | — | True | — | — |
| `reason` | `Text` | دلیل مجوز | — | True | — | — | — | — |
| `active` | `Boolean` | — | — | — | True | True | `True` | — |
| `granted_by_id` | `Many2one` | صادرکننده | `res.users` | — | True | — | — | — |
| `granted_at` | `Datetime` | زمان صدور | — | — | True | — | — | — |
| `revoked_by_id` | `Many2one` | لغوکننده | `res.users` | — | True | — | — | — |
| `revoked_at` | `Datetime` | زمان لغو | — | — | True | — | — | — |
| `revoke_reason` | `Text` | دلیل لغو | — | — | — | — | — | — |
| `review_rejected_cases` | `Boolean` | بازبینی موارد قبلاً ردشده | — | — | — | — | — | — |

**مقادیر Selection/State**

- `grant_scope`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 28 |
| `write()` | — | 39 |
| `unlink()` | — | 47 |
| `action_revoke()` | — | 50 |
| `authorization_for()` | `api.model` | 60 |

### `cas.overtime.request` — کلاس `CasOvertimeRequest`

- منبع: `models/overtime.py:67`
- inherits: `mail.thread`، `mail.activity.mixin`، `cas.kardex.approval.mixin`
- توضیح فنی: CAS Post Work Overtime Request

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `number` | `Char` | شماره | — | — | True | — | `New` | — |
| `employee_id` | `Many2one` | کارمند | `hr.employee` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `kardex_day_id` | `Many2one` | روز کاردکس | `cas.kardex.day` | True | — | — | — | — |
| `work_date` | `Date` | روز کار | — | — | — | — | — | — / True |
| `actual_minutes` | `Integer` | اضافه‌کاری واقعی قابل درخواست | — | True | True | — | — | — |
| `manager_approved_minutes` | `Integer` | دقایق تأیید مدیر | — | — | True | — | — | — |
| `ceo_approved_minutes` | `Integer` | دقایق تأیید نهایی مدیرعامل | — | — | True | — | — | — |
| `final_approved_minutes` | `Integer` | دقایق نهایی | — | — | True | — | — | — |
| `manager_user_id` | `Many2one` | مدیر رسیدگی‌کننده | `res.users` | — | True | — | — | — |
| `authorization_id` | `Many2one` | مجوز خودکار مدیرعامل | `cas.overtime.authorization` | — | True | — | — | — |
| `reason` | `Text` | شرح اضافه‌کاری | — | True | — | — | — | — |
| `manager_note` | `Text` | توضیح مدیر | — | — | — | — | — | — |
| `ceo_note` | `Text` | توضیح مدیرعامل | — | — | — | — | — | — |
| `state` | `Selection` | وضعیت | — | True | True | True | `draft` | — |
| `submitted_at` | `Datetime` | — | — | — | True | — | — | — |
| `finalized_at` | `Datetime` | — | — | — | True | — | — | — |

**مقادیر Selection/State**

- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 99 |
| `_check_minutes()` | `api.constrains('manager_approved_minutes', 'ceo_approved_minutes', 'final_approved_minutes', 'actual_minutes')` | 111 |
| `write()` | — | 120 |
| `unlink()` | — | 138 |
| `action_submit()` | — | 143 |
| `action_manager_approve()` | — | 166 |
| `action_ceo_finalize()` | — | 183 |

Constraints سمت سرور: `_check_minutes()`

## گروه‌های امنیتی

| XML ID | عنوان | implied groups | فایل |
|---|---|---|---|
| `group_cas_kardex_user` | کاربر کاردکس | [(4, ref('cas_attendance_core.group_cas_attendance_user'))] | `security/cas_kardex_security.xml` |
| `group_cas_kardex_supervisor` | سرپرست کاردکس | [(4, ref('group_cas_kardex_user')), (4, ref('cas_attendance_core.group_cas_attendance_supervisor'))] | `security/cas_kardex_security.xml` |
| `group_cas_kardex_manager` | مدیر کاردکس | [(4, ref('group_cas_kardex_supervisor'))] | `security/cas_kardex_security.xml` |
| `group_cas_kardex_ceo` | مدیرعامل کاردکس | [(4, ref('group_cas_kardex_manager'))] | `security/cas_kardex_security.xml` |
| `base.group_system` | — | [(4, ref('cas_kardex_management.group_cas_kardex_manager'))] | `security/cas_kardex_security.xml` |

## ماتریس ACL

| ACL | مدل | گروه | Read | Write | Create | Unlink |
|---|---|---|---:|---:|---:|---:|
| `access_cas_attendance_request_user` | `model_cas_attendance_request` | `group_cas_kardex_user` | 1 | 1 | 1 | 1 |
| `access_cas_attendance_request_supervisor` | `model_cas_attendance_request` | `group_cas_kardex_supervisor` | 1 | 1 | 1 | 0 |
| `access_cas_overtime_request_user` | `model_cas_overtime_request` | `group_cas_kardex_user` | 1 | 1 | 1 | 1 |
| `access_cas_overtime_request_supervisor` | `model_cas_overtime_request` | `group_cas_kardex_supervisor` | 1 | 1 | 1 | 0 |
| `access_cas_overtime_authorization_manager` | `model_cas_overtime_authorization` | `group_cas_kardex_manager` | 1 | 0 | 0 | 0 |
| `access_cas_overtime_authorization_ceo` | `model_cas_overtime_authorization` | `group_cas_kardex_ceo` | 1 | 1 | 1 | 0 |
| `access_cas_kardex_day_user` | `model_cas_kardex_day` | `group_cas_kardex_user` | 1 | 0 | 0 | 0 |
| `access_cas_kardex_day_supervisor` | `model_cas_kardex_day` | `group_cas_kardex_supervisor` | 1 | 1 | 0 | 0 |
| `access_cas_kardex_period_user` | `model_cas_kardex_period` | `group_cas_kardex_user` | 1 | 0 | 0 | 0 |
| `access_cas_kardex_period_manager` | `model_cas_kardex_period` | `group_cas_kardex_manager` | 1 | 1 | 1 | 0 |
| `access_cas_kardex_reopen_manager` | `model_cas_kardex_reopen` | `group_cas_kardex_manager` | 1 | 0 | 0 | 0 |
| `access_cas_kardex_reopen_ceo` | `model_cas_kardex_reopen` | `group_cas_kardex_ceo` | 1 | 1 | 1 | 0 |

## Record Ruleها

| XML ID | عنوان | مدل | گروه‌ها | Domain |
|---|---|---|---|---|
| `rule_cas_attendance_request_company` | درخواست‌های شرکت‌های مجاز | `model_cas_attendance_request` | — | `[('company_id','in',company_ids)]` |
| `rule_cas_attendance_request_own` | درخواست‌های خود کاربر | `model_cas_attendance_request` | [(4, ref('group_cas_kardex_user'))] | `[('employee_id.user_id','=',user.id)]` |
| `rule_cas_attendance_request_supervisor` | درخواست‌های قابل رسیدگی | `model_cas_attendance_request` | [(4, ref('group_cas_kardex_supervisor'))] | `[(1,'=',1)]` |
| `rule_cas_overtime_request_company` | اضافه‌کاری‌های شرکت‌های مجاز | `model_cas_overtime_request` | — | `[('company_id','in',company_ids)]` |
| `rule_cas_overtime_request_own` | اضافه‌کاری خود کاربر | `model_cas_overtime_request` | [(4, ref('group_cas_kardex_user'))] | `[('employee_id.user_id','=',user.id)]` |
| `rule_cas_overtime_request_supervisor` | اضافه‌کاری‌های قابل رسیدگی | `model_cas_overtime_request` | [(4, ref('group_cas_kardex_supervisor'))] | `[(1,'=',1)]` |
| `rule_cas_overtime_authorization_company` | مجوزهای شرکت‌های مجاز | `model_cas_overtime_authorization` | — | `[('company_id','in',company_ids)]` |
| `rule_cas_kardex_day_company` | کاردکس شرکت‌های مجاز | `model_cas_kardex_day` | — | `[('company_id','in',company_ids)]` |
| `rule_cas_kardex_day_own` | کاردکس خود کاربر | `model_cas_kardex_day` | [(4, ref('group_cas_kardex_user'))] | `[('employee_id.user_id','=',user.id)]` |
| `rule_cas_kardex_day_supervisor` | کاردکس قابل رسیدگی | `model_cas_kardex_day` | [(4, ref('group_cas_kardex_supervisor'))] | `[(1,'=',1)]` |
| `rule_cas_kardex_period_company` | دوره‌های شرکت‌های مجاز | `model_cas_kardex_period` | — | `[('company_id','in',company_ids)]` |
| `rule_cas_kardex_reopen_company` | بازگشایی‌های شرکت‌های مجاز | `model_cas_kardex_reopen` | — | `[('company_id','in',company_ids)]` |

## منوها

| XML ID | عنوان | والد | action | گروه |
|---|---|---|---|---|
| `menu_cas_my_kardex` | کاردکس من | `cas_shift_management.menu_cas_shift_root` | `action_cas_my_kardex_day` | `group_cas_kardex_user` |
| `menu_cas_my_requests` | درخواست‌های من | `cas_shift_management.menu_cas_shift_root` | `action_cas_my_attendance_request` | `group_cas_kardex_user` |
| `menu_cas_kardex_operations` | کاردکس و درخواست‌ها | `cas_shift_management.menu_cas_shift_root` | — | `group_cas_kardex_supervisor` |
| `menu_cas_kardex_days` | کاردکس روزانه | `menu_cas_kardex_operations` | `action_cas_kardex_day` | — |
| `menu_cas_request_review` | مرخصی و مأموریت | `menu_cas_kardex_operations` | `action_cas_attendance_request_review` | — |
| `menu_cas_overtime_requests` | اضافه‌کاری‌های انجام‌شده | `menu_cas_kardex_operations` | `action_cas_overtime_request` | — |
| `menu_cas_kardex_periods` | دوره‌ها و قفل ماه | `menu_cas_kardex_operations` | `action_cas_kardex_period` | `group_cas_kardex_manager` |
| `menu_cas_kardex_reopens` | بازگشایی کاردکس | `menu_cas_kardex_operations` | `action_cas_kardex_reopen` | `group_cas_kardex_ceo` |
| `menu_cas_overtime_authorizations` | مجوز خودکار اضافه‌کاری | `menu_cas_kardex_operations` | `action_cas_overtime_authorization` | `group_cas_kardex_ceo` |

## Actionها

| XML ID | نوع | عنوان | مدل/تگ | view mode | فایل |
|---|---|---|---|---|---|
| `action_cas_kardex_day` | `ir.actions.act_window` | کاردکس روزانه | `cas.kardex.day` | `list,form` | `views/kardex_views.xml` |
| `action_cas_my_kardex_day` | `ir.actions.act_window` | کاردکس من | `cas.kardex.day` | `list` | `views/kardex_views.xml` |
| `action_cas_kardex_period` | `ir.actions.act_window` | دوره‌ها و قفل ماه | `cas.kardex.period` | `list,form` | `views/kardex_views.xml` |
| `action_cas_kardex_reopen` | `ir.actions.act_window` | بازگشایی کاردکس | `cas.kardex.reopen` | `list,form` | `views/kardex_views.xml` |
| `action_cas_overtime_request` | `ir.actions.act_window` | اضافه‌کاری‌های انجام‌شده | `cas.overtime.request` | `list,form` | `views/overtime_views.xml` |
| `action_cas_overtime_authorization` | `ir.actions.act_window` | مجوز خودکار اضافه‌کاری | `cas.overtime.authorization` | `list,form` | `views/overtime_views.xml` |
| `action_cas_my_attendance_request` | `ir.actions.act_window` | درخواست‌های من | `cas.attendance.request` | `list,form` | `views/request_views.xml` |
| `action_cas_attendance_request_review` | `ir.actions.act_window` | مرخصی و مأموریت | `cas.attendance.request` | `list,form` | `views/request_views.xml` |

## Cron و Sequence

**Cronها**

| XML ID | عنوان | مدل/کد | تناوب |
|---|---|---|---|
| `ir_cron_cas_kardex_lock` | قفل خودکار دوره‌های کاردکس | `model._cron_lock_due_periods()` | 1 days |

**Sequenceها**

| XML ID | عنوان | code | prefix |
|---|---|---|---|
| `seq_cas_attendance_request` | درخواست مرخصی و مأموریت | `cas.attendance.request` | `ATR/%(year)s/` |
| `seq_cas_overtime_request` | درخواست اضافه‌کاری | `cas.overtime.request` | `OT/%(year)s/` |

## Assetهای رابط کاربری

Asset اختصاصی ندارد.

## داده‌های بارگذاری‌شده از manifest

- `security/cas_kardex_security.xml`
- `security/ir.model.access.csv`
- `data/cas_kardex_cron.xml`
- `views/company_views.xml`
- `views/request_views.xml`
- `views/overtime_views.xml`
- `views/kardex_views.xml`
- `views/kardex_menus.xml`

## آزمون‌های موجود

- `tests/test_kardex_management.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
