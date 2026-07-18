# مرجع فنی استخراج‌شده از کد: CAS Shift Management

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_shift_management` |
| نسخه | `19.0.1.0.3` |
| عنوان | CAS Shift Management |
| خلاصه | Effective-dated attendance policies, shift patterns and daily schedules |
| دسته | Human Resources |
| نوع برنامه | Application |
| نصب خودکار | — |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `hr`, `mail` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 7 | مدل و منطق دامنه |
| `views/` | 7 | نما، action و menu |
| `security/` | 2 | گروه، ACL و record rule |
| `data/` | 1 | داده پایه، sequence و cron |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `cas.attendance.policy` — کلاس `CasAttendancePolicy`

- منبع: `models/attendance_policy.py:5`
- inherits: `mail.thread`
- توضیح فنی: CAS Attendance Policy

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `name` | `Char` | عنوان سیاست | — | True | — | True | — | — |
| `code` | `Char` | کد | — | True | — | — | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `attendance_mode` | `Selection` | حالت حضور و غیاب | — | True | — | True | `simple` | — |
| `source_tolerance_minutes` | `Integer` | حد تطبیق دستگاه و نگهبانی (دقیقه) | — | True | — | — | `5` | — |
| `normal_work_minutes` | `Integer` | موظفی روز عادی | — | True | — | — | `480` | — |
| `normal_break_minutes` | `Integer` | استراحت روز عادی | — | True | — | — | `30` | — |
| `short_work_minutes` | `Integer` | موظفی روز کوتاه | — | True | — | — | `330` | — |
| `short_day_extended_break_minutes` | `Integer` | استراحت در صورت ادامه کار روز کوتاه | — | True | — | — | `30` | — |
| `allow_guard_work_date_choice` | `Boolean` | اجازه انتخاب روز کاری توسط نگهبان | — | — | — | — | — | — |
| `auto_close_mixed_sources` | `Boolean` | بستن ساده با ترکیب منابع | — | — | — | — | `True` | — |
| `active` | `Boolean` | — | — | — | — | True | `True` | — |

**مقادیر Selection/State**

- `attendance_mode`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 45 |
| `write()` | — | 51 |
| `_check_minutes()` | `api.constrains('source_tolerance_minutes', 'normal_work_minutes', 'normal_break_minutes', 'short_work_minutes', 'short_day_extended_break_minutes')` | 60 |

Constraints سمت سرور: `_check_minutes()`

### `cas.shift.assignment` — کلاس `CasShiftAssignment`

- منبع: `models/shift_assignment.py:16`
- inherits: `mail.thread`، `mail.activity.mixin`
- توضیح فنی: CAS Effective-Dated Shift Assignment

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `number` | `Char` | شماره انتساب | — | — | True | — | `New` | — |
| `name` | `Char` | عنوان انتساب | — | True | — | True | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `employee_ids` | `Many2many` | کارکنان | `hr.employee` | True | — | — | — | — |
| `department_id` | `Many2one` | واحد برنامه‌ریز | `hr.department` | — | — | — | — | — |
| `supervisor_user_id` | `Many2one` | مسئول برنامه | `res.users` | True | — | — | — | — |
| `policy_id` | `Many2one` | سیاست حضور و غیاب | `cas.attendance.policy` | True | — | True | — | — |
| `pattern_id` | `Many2one` | الگوی شیفت | `cas.shift.pattern` | True | — | True | — | — |
| `anchor_date` | `Date` | روز اول چرخه | — | True | — | — | — | — |
| `date_from` | `Date` | از تاریخ | — | True | — | True | — | — |
| `date_to` | `Date` | تا تاریخ | — | True | — | True | — | — |
| `weekly_rest_day` | `Selection` | WEEKDAY_SELECTION | — | True | — | True | `4` | — |
| `roster_respects_weekly_rest` | `Boolean` | تعطیل هفتگی نوبت را تعطیل می‌کند | — | — | — | — | `True` | — |
| `short_day_enabled` | `Boolean` | روز قبل از تعطیل، کوتاه است | — | — | — | — | `True` | — |
| `short_day_template_id` | `Many2one` | شیفت مخصوص روز کوتاه | `cas.shift.template` | — | — | — | — | — |
| `roster_respects_official_holiday` | `Boolean` | تعطیل رسمی نوبت را تعطیل می‌کند | — | — | — | — | `True` | — |
| `state` | `Selection` | — | — | True | True | True | `draft` | — |
| `published_at` | `Datetime` | زمان انتشار | — | — | True | — | — | — |
| `published_by_id` | `Many2one` | منتشرکننده | `res.users` | — | True | — | — | — |
| `day_ids` | `One2many` | برنامه‌های روزانه | `cas.shift.day` | — | — | — | — | — |
| `day_count` | `Integer` | — | — | — | — | — | — | _compute_day_count / — |
| `note` | `Text` | توضیحات | — | — | — | — | — | — |

**مقادیر Selection/State**

- `weekly_rest_day`: —
- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_compute_day_count()` | `api.depends('day_ids')` | 77 |
| `create()` | `api.model_create_multi` | 82 |
| `write()` | — | 88 |
| `unlink()` | — | 101 |
| `_check_contract()` | `api.constrains('date_from', 'date_to', 'anchor_date', 'employee_ids', 'company_id', 'policy_id', 'pattern_id', 'short_day_template_id', 'supervisor_user_id')` | 110 |
| `_check_publish_access()` | — | 130 |
| `_local_datetime()` | `staticmethod` | 135 |
| `_pattern_line_for()` | — | 147 |
| `_day_values()` | — | 152 |
| `action_publish()` | — | 212 |
| `action_close()` | — | 245 |
| `action_cancel()` | — | 252 |
| `action_open_days()` | — | 260 |

Constraints سمت سرور: `_check_contract()`

### `cas.official.holiday` — کلاس `CasOfficialHoliday`

- منبع: `models/shift_day.py:7`
- inherits: `mail.thread`
- توضیح فنی: CAS Official Holiday

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `name` | `Char` | عنوان تعطیل | — | True | — | True | — | — |
| `date` | `Date` | تاریخ | — | True | — | True | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `active` | `Boolean` | — | — | — | — | True | `True` | — |
| `note` | `Text` | توضیحات | — | — | — | — | — | — |

### `cas.shift.day` — کلاس `CasShiftDay`

- منبع: `models/shift_day.py:26`
- inherits: `mail.thread`
- توضیح فنی: CAS Effective Daily Schedule

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `assignment_id` | `Many2one` | انتساب مبدأ | `cas.shift.assignment` | True | — | — | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | — | — |
| `employee_id` | `Many2one` | کارمند | `hr.employee` | True | — | — | — | — |
| `department_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `schedule_date` | `Date` | تاریخ واقعی | — | True | — | — | — | — |
| `rule_origin_date` | `Date` | مبدأ قانون روز | — | True | — | — | — | — |
| `policy_id` | `Many2one` | سیاست حضور | `cas.attendance.policy` | True | — | — | — | — |
| `attendance_mode` | `Selection` | حالت حضور | — | True | True | — | — | — |
| `source_tolerance_minutes` | `Integer` | حد تطبیق منابع | — | True | True | — | — | — |
| `template_id` | `Many2one` | شیفت مؤثر | `cas.shift.template` | — | — | — | — | — |
| `day_kind` | `Selection` | نوع روز مؤثر | — | True | True | — | — | — |
| `planned_start` | `Datetime` | شروع برنامه | — | — | True | — | — | — |
| `planned_end` | `Datetime` | پایان برنامه | — | — | True | — | — | — |
| `base_work_minutes` | `Integer` | موظفی | — | — | True | — | — | — |
| `break_minutes` | `Integer` | استراحت | — | — | True | — | — | — |
| `required_presence_minutes` | `Integer` | حضور الزامی | — | — | True | — | — | — |
| `mandatory_overtime_minutes` | `Integer` | اضافه‌کاری اجباری برنامه | — | — | True | — | — | — |
| `calendar_date_is_official_holiday` | `Boolean` | تاریخ واقعی تعطیل رسمی است | — | — | True | — | — | — |
| `rule_is_official_holiday` | `Boolean` | قانون منتقل‌شده تعطیل رسمی | — | — | True | — | — | — |
| `rule_is_weekly_rest` | `Boolean` | قانون منتقل‌شده تعطیل هفتگی | — | — | True | — | — | — |
| `rule_is_short_day` | `Boolean` | قانون منتقل‌شده روز کوتاه | — | — | True | — | — | — |
| `swapped_by_id` | `Many2one` | آخرین جابه‌جایی | `cas.shift.swap` | — | True | — | — | — |
| `state` | `Selection` | وضعیت | — | True | True | — | `planned` | — |

**مقادیر Selection/State**

- `attendance_mode`: —
- `day_kind`: —
- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 72 |
| `write()` | — | 77 |
| `unlink()` | — | 83 |
| `_check_contract()` | `api.constrains('day_kind', 'template_id', 'planned_start', 'planned_end', 'base_work_minutes', 'break_minutes', 'required_presence_minutes', 'mandatory_overtime_minutes')` | 90 |
| `_snapshot()` | — | 103 |
| `_values_from_snapshot()` | — | 116 |

Constraints سمت سرور: `_check_contract()`

### `cas.shift.pattern` — کلاس `CasShiftPattern`

- منبع: `models/shift_pattern.py:5`
- inherits: `mail.thread`
- توضیح فنی: CAS Shift Pattern

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `name` | `Char` | عنوان الگو | — | True | — | True | — | — |
| `code` | `Char` | کد | — | True | — | — | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `cycle_length` | `Integer` | طول چرخه (روز) | — | True | — | True | `7` | — |
| `line_ids` | `One2many` | روزهای چرخه | `cas.shift.pattern.line` | — | — | — | — | — |
| `active` | `Boolean` | — | — | — | — | True | `True` | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 25 |
| `write()` | — | 31 |
| `_check_cycle()` | `api.constrains('cycle_length', 'line_ids')` | 43 |

Constraints سمت سرور: `_check_cycle()`

### `cas.shift.pattern.line` — کلاس `CasShiftPatternLine`

- منبع: `models/shift_pattern.py:52`
- inherits: —
- توضیح فنی: CAS Shift Pattern Day

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `pattern_id` | `Many2one` | — | `cas.shift.pattern` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `cycle_day` | `Integer` | روز چرخه | — | True | — | — | — | — |
| `day_kind` | `Selection` | نوع روز | — | True | — | — | `work` | — |
| `template_id` | `Many2one` | شیفت | `cas.shift.template` | — | — | — | — | — |

**مقادیر Selection/State**

- `day_kind`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `write()` | — | 69 |
| `unlink()` | — | 78 |
| `_check_line()` | `api.constrains('day_kind', 'template_id', 'pattern_id')` | 88 |

Constraints سمت سرور: `_check_line()`

### `cas.shift.swap` — کلاس `CasShiftSwap`

- منبع: `models/shift_swap.py:5`
- inherits: `mail.thread`، `mail.activity.mixin`
- توضیح فنی: CAS Bulk Day Rule Swap

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `name` | `Char` | عنوان جابه‌جایی | — | True | — | True | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `date_a` | `Date` | روز اول | — | True | — | True | — | — |
| `date_b` | `Date` | روز دوم | — | True | — | True | — | — |
| `scope` | `Selection` | دامنه | — | True | — | True | `company` | — |
| `department_id` | `Many2one` | واحد | `hr.department` | — | — | — | — | — |
| `employee_ids` | `Many2many` | افراد منتخب | `hr.employee` | — | — | — | — | — |
| `reason` | `Text` | دلیل | — | True | — | — | — | — |
| `state` | `Selection` | — | — | True | True | True | `draft` | — |
| `applied_at` | `Datetime` | زمان اعمال | — | — | True | — | — | — |
| `applied_by_id` | `Many2one` | اعمال‌کننده | `res.users` | — | True | — | — | — |
| `affected_count` | `Integer` | تعداد افراد | — | — | True | — | — | — |

**مقادیر Selection/State**

- `scope`: —
- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_check_contract()` | `api.constrains('date_a', 'date_b', 'scope', 'department_id', 'employee_ids', 'company_id')` | 34 |
| `write()` | — | 47 |
| `unlink()` | — | 55 |
| `_target_employees()` | — | 60 |
| `action_apply()` | — | 77 |

Constraints سمت سرور: `_check_contract()`

### `cas.shift.template` — کلاس `CasShiftTemplate`

- منبع: `models/shift_template.py:7`
- inherits: `mail.thread`
- توضیح فنی: CAS Shift Template

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `sequence` | `Integer` | — | — | — | — | — | `10` | — |
| `name` | `Char` | عنوان شیفت | — | True | — | True | — | — |
| `code` | `Char` | کد | — | True | — | — | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `shift_kind` | `Selection` | نوع حضور | — | True | — | True | `regular` | — |
| `timezone` | `Selection` | منطقه زمانی | — | True | — | — | `lambda self: self.env.user.tz or 'Asia/Tehran'` | — |
| `start_hour` | `Float` | ساعت شروع | — | True | — | True | `7.5` | — |
| `end_hour` | `Float` | ساعت پایان | — | True | — | True | `16.0` | — |
| `crosses_midnight` | `Boolean` | — | — | — | — | — | — | _compute_duration / True |
| `presence_minutes` | `Integer` | مدت حضور برنامه (دقیقه) | — | — | — | — | — | _compute_duration / True |
| `default_break_minutes` | `Integer` | استراحت پیش‌فرض | — | True | — | — | `30` | — |
| `work_date_rule` | `Selection` | روز کاری پیش‌فرض | — | True | — | — | `start` | — |
| `manual_work_date_allowed` | `Boolean` | اجازه انتخاب روز کاری توسط نگهبان | — | — | — | — | — | — |
| `active` | `Boolean` | — | — | — | — | True | `True` | — |

**مقادیر Selection/State**

- `shift_kind`: —
- `timezone`: `lambda self: [(tz, tz) for tz in pytz.common_timezones]`
- `work_date_rule`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_compute_duration()` | `api.depends('start_hour', 'end_hour')` | 46 |
| `create()` | `api.model_create_multi` | 58 |
| `write()` | — | 64 |
| `_check_contract()` | `api.constrains('start_hour', 'end_hour', 'default_break_minutes', 'timezone')` | 80 |

Constraints سمت سرور: `_check_contract()`

## گروه‌های امنیتی

| XML ID | عنوان | implied groups | فایل |
|---|---|---|---|
| `group_cas_shift_user` | کاربر شیفت | — | `security/cas_shift_security.xml` |
| `group_cas_shift_planner` | برنامه‌ریز شیفت | [(4, ref('group_cas_shift_user'))] | `security/cas_shift_security.xml` |
| `group_cas_shift_manager` | مدیر شیفت و تقویم | [(4, ref('group_cas_shift_planner'))] | `security/cas_shift_security.xml` |
| `base.group_system` | — | [(4, ref('cas_shift_management.group_cas_shift_manager'))] | `security/cas_shift_security.xml` |

## ماتریس ACL

| ACL | مدل | گروه | Read | Write | Create | Unlink |
|---|---|---|---:|---:|---:|---:|
| `access_cas_attendance_policy_user` | `model_cas_attendance_policy` | `group_cas_shift_user` | 1 | 0 | 0 | 0 |
| `access_cas_attendance_policy_manager` | `model_cas_attendance_policy` | `group_cas_shift_manager` | 1 | 1 | 1 | 0 |
| `access_cas_shift_template_user` | `model_cas_shift_template` | `group_cas_shift_user` | 1 | 0 | 0 | 0 |
| `access_cas_shift_template_planner` | `model_cas_shift_template` | `group_cas_shift_planner` | 1 | 1 | 1 | 0 |
| `access_cas_shift_pattern_user` | `model_cas_shift_pattern` | `group_cas_shift_user` | 1 | 0 | 0 | 0 |
| `access_cas_shift_pattern_planner` | `model_cas_shift_pattern` | `group_cas_shift_planner` | 1 | 1 | 1 | 0 |
| `access_cas_shift_pattern_line_user` | `model_cas_shift_pattern_line` | `group_cas_shift_user` | 1 | 0 | 0 | 0 |
| `access_cas_shift_pattern_line_planner` | `model_cas_shift_pattern_line` | `group_cas_shift_planner` | 1 | 1 | 1 | 1 |
| `access_cas_shift_assignment_user` | `model_cas_shift_assignment` | `group_cas_shift_user` | 1 | 0 | 0 | 0 |
| `access_cas_shift_assignment_planner` | `model_cas_shift_assignment` | `group_cas_shift_planner` | 1 | 1 | 1 | 0 |
| `access_cas_shift_day_user` | `model_cas_shift_day` | `group_cas_shift_user` | 1 | 0 | 0 | 0 |
| `access_cas_shift_day_planner` | `model_cas_shift_day` | `group_cas_shift_planner` | 1 | 0 | 0 | 0 |
| `access_cas_official_holiday_user` | `model_cas_official_holiday` | `group_cas_shift_user` | 1 | 0 | 0 | 0 |
| `access_cas_official_holiday_manager` | `model_cas_official_holiday` | `group_cas_shift_manager` | 1 | 1 | 1 | 0 |
| `access_cas_shift_swap_planner` | `model_cas_shift_swap` | `group_cas_shift_planner` | 1 | 1 | 1 | 0 |
| `access_cas_shift_swap_manager` | `model_cas_shift_swap` | `group_cas_shift_manager` | 1 | 1 | 1 | 0 |

## Record Ruleها

| XML ID | عنوان | مدل | گروه‌ها | Domain |
|---|---|---|---|---|
| `rule_cas_attendance_policy_company` | سیاست‌های حضور شرکت‌های مجاز | `model_cas_attendance_policy` | [(4, ref('group_cas_shift_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_cas_shift_template_company` | شیفت‌های شرکت‌های مجاز | `model_cas_shift_template` | [(4, ref('group_cas_shift_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_cas_shift_pattern_company` | الگوهای شیفت شرکت‌های مجاز | `model_cas_shift_pattern` | [(4, ref('group_cas_shift_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_cas_shift_pattern_line_company` | روزهای الگوی شرکت‌های مجاز | `model_cas_shift_pattern_line` | [(4, ref('group_cas_shift_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_cas_official_holiday_company` | تعطیلات رسمی شرکت‌های مجاز | `model_cas_official_holiday` | [(4, ref('group_cas_shift_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_cas_shift_assignment_own` | انتساب‌های خود کاربر | `model_cas_shift_assignment` | [(4, ref('group_cas_shift_user'))] | `[('company_id', 'in', company_ids), ('employee_ids.user_id', '=', user.id)]` |
| `rule_cas_shift_assignment_planner` | انتساب‌های شرکت برای برنامه‌ریز | `model_cas_shift_assignment` | [(4, ref('group_cas_shift_planner'))] | `[('company_id', 'in', company_ids)]` |
| `rule_cas_shift_day_own` | برنامه‌های روزانه خود کاربر | `model_cas_shift_day` | [(4, ref('group_cas_shift_user'))] | `[('company_id', 'in', company_ids), ('employee_id.user_id', '=', user.id)]` |
| `rule_cas_shift_day_planner` | برنامه‌های روزانه شرکت برای برنامه‌ریز | `model_cas_shift_day` | [(4, ref('group_cas_shift_planner'))] | `[('company_id', 'in', company_ids)]` |
| `rule_cas_shift_swap_company` | جابه‌جایی‌های شرکت‌های مجاز | `model_cas_shift_swap` | [(4, ref('group_cas_shift_planner'))] | `[('company_id', 'in', company_ids)]` |

## منوها

| XML ID | عنوان | والد | action | گروه |
|---|---|---|---|---|
| `menu_cas_shift_root` | شیفت و حضور | — | — | `group_cas_shift_user` |
| `menu_cas_my_shift_days` | برنامه من | `menu_cas_shift_root` | `action_cas_my_shift_day` | — |
| `menu_cas_shift_operations` | برنامه‌ریزی | `menu_cas_shift_root` | — | `group_cas_shift_planner` |
| `menu_cas_shift_assignments` | انتساب‌های تاریخ‌دار | `menu_cas_shift_operations` | `action_cas_shift_assignment` | — |
| `menu_cas_shift_days` | برنامه روزانه | `menu_cas_shift_operations` | `action_cas_shift_day` | — |
| `menu_cas_shift_swaps` | جابه‌جایی روزها | `menu_cas_shift_operations` | `action_cas_shift_swap` | — |
| `menu_cas_shift_config` | تنظیمات | `menu_cas_shift_root` | — | `group_cas_shift_planner` |
| `menu_cas_shift_templates` | شیفت‌ها | `menu_cas_shift_config` | `action_cas_shift_template` | — |
| `menu_cas_shift_patterns` | الگوهای گردشی | `menu_cas_shift_config` | `action_cas_shift_pattern` | — |
| `menu_cas_attendance_policies` | سیاست‌های حضور | `menu_cas_shift_config` | `action_cas_attendance_policy` | `group_cas_shift_manager` |
| `menu_cas_official_holidays` | تعطیلات رسمی | `menu_cas_shift_config` | `action_cas_official_holiday` | `group_cas_shift_manager` |

## Actionها

| XML ID | نوع | عنوان | مدل/تگ | view mode | فایل |
|---|---|---|---|---|---|
| `action_cas_shift_assignment` | `ir.actions.act_window` | انتساب‌های شیفت | `cas.shift.assignment` | `list,form` | `views/cas_shift_assignment_views.xml` |
| `action_cas_shift_day` | `ir.actions.act_window` | برنامه روزانه | `cas.shift.day` | `list,form` | `views/cas_shift_day_views.xml` |
| `action_cas_my_shift_day` | `ir.actions.act_window` | برنامه من | `cas.shift.day` | `list,form` | `views/cas_shift_day_views.xml` |
| `action_cas_official_holiday` | `ir.actions.act_window` | تعطیلات رسمی | `cas.official.holiday` | `list,form` | `views/cas_shift_day_views.xml` |
| `action_cas_shift_pattern` | `ir.actions.act_window` | الگوهای گردشی | `cas.shift.pattern` | `list,form` | `views/cas_shift_pattern_views.xml` |
| `action_cas_attendance_policy` | `ir.actions.act_window` | سیاست‌های حضور | `cas.attendance.policy` | `list,form` | `views/cas_shift_policy_views.xml` |
| `action_cas_shift_swap` | `ir.actions.act_window` | جابه‌جایی روزها | `cas.shift.swap` | `list,form` | `views/cas_shift_swap_views.xml` |
| `action_cas_shift_template` | `ir.actions.act_window` | شیفت‌ها | `cas.shift.template` | `list,form` | `views/cas_shift_template_views.xml` |

## Cron و Sequence

**Sequenceها**

| XML ID | عنوان | code | prefix |
|---|---|---|---|
| `seq_cas_shift_assignment` | CAS Shift Assignment | `cas.shift.assignment` | `CSA/%(year)s/` |

## Assetهای رابط کاربری

Asset اختصاصی ندارد.

## داده‌های بارگذاری‌شده از manifest

- `security/cas_shift_security.xml`
- `security/ir.model.access.csv`
- `data/cas_shift_sequences.xml`
- `views/cas_shift_template_views.xml`
- `views/cas_shift_policy_views.xml`
- `views/cas_shift_pattern_views.xml`
- `views/cas_shift_assignment_views.xml`
- `views/cas_shift_day_views.xml`
- `views/cas_shift_swap_views.xml`
- `views/cas_shift_menus.xml`

## آزمون‌های موجود

- `tests/test_shift_management.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
