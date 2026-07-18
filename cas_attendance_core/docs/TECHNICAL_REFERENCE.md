# مرجع فنی استخراج‌شده از کد: CAS Attendance Core

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_attendance_core` |
| نسخه | `19.0.1.0.1` |
| عنوان | CAS Attendance Core |
| خلاصه | Auditable guard and device attendance reconciliation |
| دسته | Human Resources |
| نوع برنامه | Application |
| نصب خودکار | — |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `cas_shift_management`, `mail` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 4 | مدل و منطق دامنه |
| `views/` | 4 | نما، action و menu |
| `security/` | 2 | گروه، ACL و record rule |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `cas.attendance.day` — کلاس `CasAttendanceDay`

- منبع: `models/attendance_day.py:5`
- inherits: `mail.thread`
- توضیح فنی: CAS Reconciled Attendance Day

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `employee_id` | `Many2one` | کارمند | `hr.employee` | True | — | — | — | — |
| `company_id` | `Many2one` | شرکت | — | — | — | — | — | — / True |
| `work_date` | `Date` | روز کاری | — | True | — | — | — | — |
| `shift_day_id` | `Many2one` | برنامه شیفت | `cas.shift.day` | — | True | — | — | — |
| `attendance_mode` | `Selection` | روش محاسبه | — | True | True | — | — | — |
| `tolerance_minutes` | `Integer` | حد تطبیق منابع | — | — | True | — | — | — |
| `event_ids` | `One2many` | رخدادهای خام | `cas.attendance.event` | — | — | — | — | _compute_events / — |
| `interval_ids` | `One2many` | بازه‌های محاسباتی | `cas.attendance.interval` | — | True | — | — | — |
| `guard_entry` | `Datetime` | ورود نگهبانی | — | — | True | — | — | — |
| `guard_exit` | `Datetime` | خروج نگهبانی | — | — | True | — | — | — |
| `device_entry` | `Datetime` | شروع کار دستگاه | — | — | True | — | — | — |
| `device_exit` | `Datetime` | پایان کار دستگاه | — | — | True | — | — | — |
| `effective_entry` | `Datetime` | ورود مؤثر | — | — | True | — | — | — |
| `effective_exit` | `Datetime` | خروج مؤثر | — | — | True | — | — | — |
| `state` | `Selection` | وضعیت | — | True | True | True | `draft` | — |
| `warning_code` | `Selection` | هشدار | — | — | True | — | — | — |
| `resolution_entry_source` | `Selection` | مبنای ورود | — | — | — | — | — | — |
| `resolution_exit_source` | `Selection` | مبنای خروج | — | — | — | — | — | — |
| `custom_entry` | `Datetime` | ورود اصلاحی | — | — | — | — | — | — |
| `custom_exit` | `Datetime` | خروج اصلاحی | — | — | — | — | — | — |
| `resolution_reason` | `Text` | دلیل تصمیم سرپرست | — | — | — | — | — | — |
| `resolved_by_id` | `Many2one` | تصمیم‌گیرنده | `res.users` | — | True | — | — | — |
| `resolved_at` | `Datetime` | زمان تصمیم | — | — | True | — | — | — |

**مقادیر Selection/State**

- `attendance_mode`: —
- `state`: —
- `warning_code`: —
- `resolution_entry_source`: —
- `resolution_exit_source`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_compute_events()` | `api.depends('employee_id', 'work_date')` | 45 |
| `_get_or_create()` | `api.model` | 51 |
| `create()` | `api.model_create_multi` | 63 |
| `unlink()` | — | 68 |
| `_events()` | — | 71 |
| `_has_outage()` | — | 77 |
| `recompute()` | — | 86 |
| `_recompute_simple()` | — | 94 |
| `_recompute_advanced()` | — | 127 |
| `write()` | — | 162 |
| `action_resolve()` | — | 168 |

### `cas.attendance.interval` — کلاس `CasAttendanceInterval`

- منبع: `models/attendance_day.py:184`
- inherits: —
- توضیح فنی: CAS Attendance Computation Interval

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `attendance_day_id` | `Many2one` | روز حضور | `cas.attendance.day` | True | — | — | — | — |
| `employee_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `interval_type` | `Selection` | نوع بازه | — | True | — | — | — | — |
| `start_event_id` | `Many2one` | رخداد شروع | `cas.attendance.event` | True | — | — | — | — |
| `end_event_id` | `Many2one` | رخداد پایان | `cas.attendance.event` | True | — | — | — | — |
| `start_at` | `Datetime` | شروع | — | True | True | — | — | — |
| `end_at` | `Datetime` | پایان | — | True | True | — | — | — |
| `duration_minutes` | `Integer` | مدت (دقیقه) | — | — | — | — | — | _compute_duration / True |

**مقادیر Selection/State**

- `interval_type`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_compute_duration()` | `api.depends('start_at', 'end_at')` | 200 |
| `create()` | `api.model_create_multi` | 205 |
| `write()` | — | 210 |
| `unlink()` | — | 215 |

### `cas.attendance.event` — کلاس `CasAttendanceEvent`

- منبع: `models/attendance_event.py:21`
- inherits: `mail.thread`
- توضیح فنی: CAS Immutable Attendance Event

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `employee_id` | `Many2one` | کارمند | `hr.employee` | True | — | — | — | — |
| `company_id` | `Many2one` | شرکت | — | — | — | — | — | — / True |
| `occurred_at` | `Datetime` | زمان واقعی رخداد | — | True | True | — | — | — |
| `registered_at` | `Datetime` | زمان ثبت در سامانه | — | True | True | — | `fields.Datetime.now` | — |
| `source` | `Selection` | منبع | — | True | True | — | — | — |
| `event_kind` | `Selection` | EVENT_KINDS | — | True | True | — | — | — |
| `direction` | `Selection` | جهت | — | — | — | — | — | _compute_direction / True |
| `site_id` | `Many2one` | محل | `cas.attendance.site` | — | True | — | — | — |
| `device_id` | `Many2one` | دستگاه | `cas.attendance.device` | — | True | — | — | — |
| `work_date` | `Date` | روز کاری منتسب | — | True | True | — | — | — |
| `attribution_method` | `Selection` | روش انتساب روز | — | True | True | — | — | — |
| `external_uid` | `Char` | شناسه یکتای منبع | — | — | True | — | — | — |
| `note` | `Text` | توضیحات | — | — | True | — | — | — |
| `is_void` | `Boolean` | باطل شده | — | — | True | — | — | — |
| `voided_at` | `Datetime` | زمان ابطال | — | — | True | — | — | — |
| `voided_by_id` | `Many2one` | ابطال‌کننده | `res.users` | — | True | — | — | — |
| `void_reason` | `Text` | علت ابطال | — | — | — | — | — | — |
| `replacement_event_id` | `Many2one` | رکورد جایگزین | `cas.attendance.event` | — | True | — | — | — |

**مقادیر Selection/State**

- `source`: —
- `event_kind`: —
- `direction`: —
- `attribution_method`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_compute_direction()` | `api.depends('event_kind')` | 49 |
| `_minute()` | `api.model` | 54 |
| `_resolve_work_date()` | `api.model` | 59 |
| `create()` | `api.model_create_multi` | 71 |
| `write()` | — | 94 |
| `unlink()` | — | 103 |
| `action_void()` | — | 106 |
| `_recompute_days()` | — | 114 |

### `cas.attendance.site` — کلاس `CasAttendanceSite`

- منبع: `models/attendance_site.py:5`
- inherits: `mail.thread`
- توضیح فنی: CAS Attendance Site

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `name` | `Char` | ساختمان / محل | — | True | — | True | — | — |
| `code` | `Char` | کد | — | True | — | — | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `active` | `Boolean` | — | — | — | — | True | `True` | — |

### `cas.attendance.device` — کلاس `CasAttendanceDevice`

- منبع: `models/attendance_site.py:19`
- inherits: `mail.thread`
- توضیح فنی: CAS Attendance Device

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `name` | `Char` | نام دستگاه | — | True | — | True | — | — |
| `code` | `Char` | شناسه دستگاه | — | True | — | — | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `site_id` | `Many2one` | محل | `cas.attendance.site` | True | — | — | — | — |
| `active` | `Boolean` | — | — | — | — | True | `True` | — |
| `note` | `Text` | توضیحات | — | — | — | — | — | — |

### `cas.attendance.outage` — کلاس `CasAttendanceOutage`

- منبع: `models/attendance_site.py:35`
- inherits: `mail.thread`
- توضیح فنی: CAS Attendance Device Outage

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `name` | `Char` | عنوان خرابی | — | True | — | True | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `device_id` | `Many2one` | دستگاه | `cas.attendance.device` | — | — | True | — | — |
| `site_id` | `Many2one` | محل | `cas.attendance.site` | True | — | True | — | — |
| `start_at` | `Datetime` | شروع خرابی | — | True | — | True | — | — |
| `end_at` | `Datetime` | پایان خرابی | — | — | — | True | — | — |
| `state` | `Selection` | وضعیت | — | True | — | True | `open` | — |
| `reason` | `Text` | شرح خرابی | — | True | — | — | — | — |
| `reporter_id` | `Many2one` | گزارش‌دهنده | `res.users` | True | True | — | `lambda self: self.env.user` | — |

**مقادیر Selection/State**

- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_check_dates()` | `api.constrains('start_at', 'end_at', 'state')` | 52 |
| `action_recover()` | — | 59 |

Constraints سمت سرور: `_check_dates()`

## گروه‌های امنیتی

| XML ID | عنوان | implied groups | فایل |
|---|---|---|---|
| `group_cas_attendance_user` | کاربر حضور و غیاب | [(4, ref('cas_shift_management.group_cas_shift_user'))] | `security/cas_attendance_security.xml` |
| `group_cas_attendance_guard` | ثبت‌کننده نگهبانی | [(4, ref('group_cas_attendance_user'))] | `security/cas_attendance_security.xml` |
| `group_cas_attendance_supervisor` | سرپرست حضور و غیاب | [(4, ref('group_cas_attendance_user'))] | `security/cas_attendance_security.xml` |
| `group_cas_attendance_manager` | مدیر حضور و غیاب | [(4, ref('group_cas_attendance_supervisor')), (4, ref('group_cas_attendance_guard'))] | `security/cas_attendance_security.xml` |
| `group_cas_attendance_device_importer` | دریافت‌کننده رخداد دستگاه | — | `security/cas_attendance_security.xml` |
| `base.group_system` | — | [(4, ref('cas_attendance_core.group_cas_attendance_manager'))] | `security/cas_attendance_security.xml` |

## ماتریس ACL

| ACL | مدل | گروه | Read | Write | Create | Unlink |
|---|---|---|---:|---:|---:|---:|
| `access_cas_attendance_site_user` | `model_cas_attendance_site` | `group_cas_attendance_user` | 1 | 0 | 0 | 0 |
| `access_cas_attendance_site_manager` | `model_cas_attendance_site` | `group_cas_attendance_manager` | 1 | 1 | 1 | 0 |
| `access_cas_attendance_device_user` | `model_cas_attendance_device` | `group_cas_attendance_user` | 1 | 0 | 0 | 0 |
| `access_cas_attendance_device_manager` | `model_cas_attendance_device` | `group_cas_attendance_manager` | 1 | 1 | 1 | 0 |
| `access_cas_attendance_outage_user` | `model_cas_attendance_outage` | `group_cas_attendance_user` | 1 | 0 | 0 | 0 |
| `access_cas_attendance_outage_guard` | `model_cas_attendance_outage` | `group_cas_attendance_guard` | 1 | 1 | 1 | 0 |
| `access_cas_attendance_outage_manager` | `model_cas_attendance_outage` | `group_cas_attendance_manager` | 1 | 1 | 1 | 0 |
| `access_cas_attendance_event_user` | `model_cas_attendance_event` | `group_cas_attendance_user` | 1 | 0 | 0 | 0 |
| `access_cas_attendance_event_guard` | `model_cas_attendance_event` | `group_cas_attendance_guard` | 1 | 0 | 1 | 0 |
| `access_cas_attendance_event_supervisor` | `model_cas_attendance_event` | `group_cas_attendance_supervisor` | 1 | 1 | 1 | 0 |
| `access_cas_attendance_event_importer` | `model_cas_attendance_event` | `group_cas_attendance_device_importer` | 1 | 0 | 1 | 0 |
| `access_cas_attendance_day_user` | `model_cas_attendance_day` | `group_cas_attendance_user` | 1 | 0 | 0 | 0 |
| `access_cas_attendance_day_supervisor` | `model_cas_attendance_day` | `group_cas_attendance_supervisor` | 1 | 1 | 0 | 0 |
| `access_cas_attendance_interval_user` | `model_cas_attendance_interval` | `group_cas_attendance_user` | 1 | 0 | 0 | 0 |
| `access_cas_attendance_interval_supervisor` | `model_cas_attendance_interval` | `group_cas_attendance_supervisor` | 1 | 0 | 0 | 0 |

## Record Ruleها

| XML ID | عنوان | مدل | گروه‌ها | Domain |
|---|---|---|---|---|
| `rule_cas_attendance_site_company` | محل‌های شرکت‌های مجاز | `model_cas_attendance_site` | — | `[('company_id','in',company_ids)]` |
| `rule_cas_attendance_device_company` | دستگاه‌های شرکت‌های مجاز | `model_cas_attendance_device` | — | `[('company_id','in',company_ids)]` |
| `rule_cas_attendance_outage_company` | خرابی‌های شرکت‌های مجاز | `model_cas_attendance_outage` | — | `[('company_id','in',company_ids)]` |
| `rule_cas_attendance_event_company` | رخدادهای شرکت‌های مجاز | `model_cas_attendance_event` | — | `[('company_id','in',company_ids)]` |
| `rule_cas_attendance_day_company` | روزهای شرکت‌های مجاز | `model_cas_attendance_day` | — | `[('company_id','in',company_ids)]` |
| `rule_cas_attendance_interval_company` | بازه‌های شرکت‌های مجاز | `model_cas_attendance_interval` | — | `[('company_id','in',company_ids)]` |
| `rule_cas_attendance_event_own` | رخدادهای خود کاربر | `model_cas_attendance_event` | [(4, ref('group_cas_attendance_user'))] | `[('employee_id.user_id','=',user.id)]` |
| `rule_cas_attendance_event_guard` | رخدادهای نگهبانی | `model_cas_attendance_event` | [(4, ref('group_cas_attendance_guard'))] | `[(1,'=',1)]` |
| `rule_cas_attendance_event_supervisor` | رخدادهای قابل رسیدگی سرپرست | `model_cas_attendance_event` | [(4, ref('group_cas_attendance_supervisor'))] | `[(1,'=',1)]` |
| `rule_cas_attendance_day_own` | روزهای حضور خود کاربر | `model_cas_attendance_day` | [(4, ref('group_cas_attendance_user'))] | `[('employee_id.user_id','=',user.id)]` |
| `rule_cas_attendance_day_supervisor` | روزهای قابل رسیدگی سرپرست | `model_cas_attendance_day` | [(4, ref('group_cas_attendance_supervisor'))] | `[(1,'=',1)]` |
| `rule_cas_attendance_interval_own` | بازه‌های خود کاربر | `model_cas_attendance_interval` | [(4, ref('group_cas_attendance_user'))] | `[('employee_id.user_id','=',user.id)]` |
| `rule_cas_attendance_interval_supervisor` | بازه‌های قابل رسیدگی سرپرست | `model_cas_attendance_interval` | [(4, ref('group_cas_attendance_supervisor'))] | `[(1,'=',1)]` |

## منوها

| XML ID | عنوان | والد | action | گروه |
|---|---|---|---|---|
| `menu_cas_my_attendance` | حضور من | `cas_shift_management.menu_cas_shift_root` | `action_cas_my_attendance_day` | `group_cas_attendance_user` |
| `menu_cas_my_attendance_events` | ورود و خروج‌های من | `cas_shift_management.menu_cas_shift_root` | `action_cas_my_attendance_event` | `group_cas_attendance_user` |
| `menu_cas_attendance_operations` | ثبت و رسیدگی حضور | `cas_shift_management.menu_cas_shift_root` | — | `group_cas_attendance_guard,group_cas_attendance_supervisor` |
| `menu_cas_attendance_events` | رخدادهای ورود و خروج | `menu_cas_attendance_operations` | `action_cas_attendance_event` | — |
| `menu_cas_attendance_days` | روزهای حضور | `menu_cas_attendance_operations` | `action_cas_attendance_day` | `group_cas_attendance_supervisor` |
| `menu_cas_attendance_outages` | خرابی دستگاه | `menu_cas_attendance_operations` | `action_cas_attendance_outage` | — |
| `menu_cas_attendance_sites` | ساختمان‌ها و محل‌ها | `cas_shift_management.menu_cas_shift_config` | `action_cas_attendance_site` | `group_cas_attendance_manager` |
| `menu_cas_attendance_devices` | دستگاه‌های حضور | `cas_shift_management.menu_cas_shift_config` | `action_cas_attendance_device` | `group_cas_attendance_manager` |

## Actionها

| XML ID | نوع | عنوان | مدل/تگ | view mode | فایل |
|---|---|---|---|---|---|
| `action_cas_attendance_day` | `ir.actions.act_window` | روزهای حضور | `cas.attendance.day` | `list,form` | `views/attendance_day_views.xml` |
| `action_cas_my_attendance_day` | `ir.actions.act_window` | حضور من | `cas.attendance.day` | `list,form` | `views/attendance_day_views.xml` |
| `action_cas_attendance_event` | `ir.actions.act_window` | رخدادهای ورود و خروج | `cas.attendance.event` | `list,form` | `views/attendance_event_views.xml` |
| `action_cas_my_attendance_event` | `ir.actions.act_window` | ورود و خروج‌های من | `cas.attendance.event` | `list,form` | `views/attendance_event_views.xml` |
| `action_cas_attendance_site` | `ir.actions.act_window` | ساختمان‌ها و محل‌ها | `cas.attendance.site` | `list,form` | `views/attendance_site_views.xml` |
| `action_cas_attendance_device` | `ir.actions.act_window` | دستگاه‌های حضور | `cas.attendance.device` | `list,form` | `views/attendance_site_views.xml` |
| `action_cas_attendance_outage` | `ir.actions.act_window` | خرابی دستگاه | `cas.attendance.outage` | `list,form` | `views/attendance_site_views.xml` |

## Cron و Sequence

Cron یا sequence اختصاصی در XML ندارد.

## Assetهای رابط کاربری

Asset اختصاصی ندارد.

## داده‌های بارگذاری‌شده از manifest

- `security/cas_attendance_security.xml`
- `security/ir.model.access.csv`
- `views/attendance_site_views.xml`
- `views/attendance_event_views.xml`
- `views/attendance_day_views.xml`
- `views/attendance_menus.xml`

## آزمون‌های موجود

- `tests/test_attendance_core.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
