# مرجع فنی استخراج‌شده از کد: CAS Attendance Operations

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_attendance_operations` |
| نسخه | `19.0.1.0.0` |
| عنوان | CAS Attendance Operations |
| خلاصه | Offline Excel imports and rapid guard attendance entry |
| دسته | Human Resources |
| نوع برنامه | Technical/Extension |
| نصب خودکار | — |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `cas_kardex_management` |
| Python خارجی | openpyxl |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 4 | مدل و منطق دامنه |
| `views/` | 4 | نما، action و menu |
| `security/` | 2 | گروه، ACL و record rule |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `cas.attendance.identity` — کلاس `CasAttendanceIdentity`

- منبع: `models/attendance_identity.py:4`
- inherits: `mail.thread`
- توضیح فنی: CAS External Attendance Identity

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `source_type` | `Selection` | منبع شناسه | — | True | — | — | — | — |
| `external_key` | `Char` | شناسه خارجی / نام شیت | — | True | — | True | — | — |
| `employee_id` | `Many2one` | کارمند | `hr.employee` | True | — | True | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `active` | `Boolean` | — | — | — | — | True | `True` | — |
| `note` | `Text` | توضیحات | — | — | — | — | — | — |

**مقادیر Selection/State**

- `source_type`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 20 |
| `write()` | — | 25 |
| `employee_for()` | `api.model` | 31 |

### `cas.attendance.import` — کلاس `CasAttendanceImport`

- منبع: `models/attendance_import.py:35`
- inherits: `mail.thread`
- توضیح فنی: CAS Audited Attendance Import Batch

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `name` | `Char` | عنوان ورود | — | True | — | True | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `import_type` | `Selection` | قالب ورودی | — | True | — | True | `device_punches` | — |
| `device_id` | `Many2one` | دستگاه | `cas.attendance.device` | — | — | — | — | — |
| `site_id` | `Many2one` | محل | `cas.attendance.site` | True | — | — | — | — |
| `data_file` | `Binary` | فایل | — | True | — | — | — | — |
| `filename` | `Char` | نام فایل | — | True | — | — | — | — |
| `state` | `Selection` | وضعیت | — | True | True | True | `draft` | — |
| `line_ids` | `One2many` | ردیف‌ها | `cas.attendance.import.line` | — | — | — | — | — |
| `total_count` | `Integer` | — | — | — | — | — | — | _compute_counts / — |
| `ready_count` | `Integer` | — | — | — | — | — | — | _compute_counts / — |
| `unmatched_count` | `Integer` | — | — | — | — | — | — | _compute_counts / — |
| `imported_count` | `Integer` | — | — | — | — | — | — | _compute_counts / — |
| `skipped_count` | `Integer` | — | — | — | — | — | — | _compute_counts / — |
| `parsed_at` | `Datetime` | — | — | — | True | — | — | — |
| `imported_at` | `Datetime` | — | — | — | True | — | — | — |
| `imported_by_id` | `Many2one` | — | `res.users` | — | True | — | — | — |

**مقادیر Selection/State**

- `import_type`: —
- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_compute_counts()` | `api.depends('line_ids.status')` | 64 |
| `write()` | — | 72 |
| `unlink()` | — | 81 |
| `_parse_datetime()` | `api.model` | 87 |
| `_parse_date()` | `api.model` | 109 |
| `_add_line()` | — | 115 |
| `action_parse()` | — | 128 |
| `_workbook()` | — | 139 |
| `_parse_guard_xlsx()` | — | 143 |
| `_rows_from_file()` | — | 158 |
| `_parse_paired()` | — | 168 |
| `_parse_device()` | — | 176 |
| `action_import_ready()` | — | 195 |

### `cas.attendance.import.line` — کلاس `CasAttendanceImportLine`

- منبع: `models/attendance_import.py:215`
- inherits: —
- توضیح فنی: CAS Attendance Import Staging Line

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `batch_id` | `Many2one` | — | `cas.attendance.import` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `row_number` | `Integer` | ردیف فایل | — | — | True | — | — | — |
| `external_key` | `Char` | شناسه خارجی | — | — | True | — | — | — |
| `employee_id` | `Many2one` | کارمند | `hr.employee` | — | — | — | — | — |
| `occurred_at` | `Datetime` | زمان رخداد | — | — | True | — | — | — |
| `event_kind` | `Selection` | نوع رخداد | — | — | — | — | — | — |
| `external_uid` | `Char` | — | — | — | True | — | — | — |
| `status` | `Selection` | — | — | True | True | — | — | — |
| `event_id` | `Many2one` | رخداد ساخته‌شده | `cas.attendance.event` | — | True | — | — | — |
| `note` | `Text` | یادداشت | — | — | True | — | — | — |
| `error_message` | `Text` | خطا | — | — | True | — | — | — |

**مقادیر Selection/State**

- `event_kind`: `lambda self: self.env['cas.attendance.event']._fields['event_kind'].selection`
- `status`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `write()` | — | 233 |
| `unlink()` | — | 245 |
| `action_skip()` | — | 249 |

### `cas.guard.batch` — کلاس `CasGuardBatch`

- منبع: `models/guard_batch.py:5`
- inherits: `mail.thread`
- توضیح فنی: CAS Rapid Guard Attendance Batch

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `name` | `Char` | عنوان نوبت ثبت | — | True | — | — | `lambda self: _('ثبت تردد نگهبانی')` | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `site_id` | `Many2one` | درب / محل | `cas.attendance.site` | True | — | — | — | — |
| `default_occurred_at` | `Datetime` | زمان پیش‌فرض | — | True | — | — | `fields.Datetime.now` | — |
| `line_ids` | `One2many` | افراد | `cas.guard.batch.line` | — | — | — | — | — |
| `state` | `Selection` | وضعیت | — | True | True | True | `draft` | — |
| `confirmed_at` | `Datetime` | — | — | — | True | — | — | — |
| `confirmed_by_id` | `Many2one` | — | `res.users` | — | True | — | — | — |

**مقادیر Selection/State**

- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `write()` | — | 20 |
| `unlink()` | — | 29 |
| `action_confirm()` | — | 33 |

### `cas.guard.batch.line` — کلاس `CasGuardBatchLine`

- منبع: `models/guard_batch.py:48`
- inherits: —
- توضیح فنی: CAS Rapid Guard Attendance Batch Line

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `batch_id` | `Many2one` | — | `cas.guard.batch` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `employee_id` | `Many2one` | کارمند | `hr.employee` | True | — | — | — | — |
| `occurred_at` | `Datetime` | زمان واقعی | — | True | — | — | `lambda self: self.env.context.get('default_occurred_at') or fields.Datetime.now()` | — |
| `event_kind` | `Selection` | نوع تردد | — | True | — | — | `guard_entry` | — |
| `work_date` | `Date` | روز کاری اختیاری | — | — | — | — | — | — |
| `note` | `Char` | توضیح | — | — | — | — | — | — |
| `event_id` | `Many2one` | رخداد ثبت‌شده | `cas.attendance.event` | — | True | — | — | — |

**مقادیر Selection/State**

- `event_kind`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_onchange_batch()` | `api.onchange('batch_id')` | 69 |
| `write()` | — | 72 |
| `unlink()` | — | 77 |

## گروه‌های امنیتی

گروه اختصاصی در XML این ماژول تعریف نشده است.

## ماتریس ACL

| ACL | مدل | گروه | Read | Write | Create | Unlink |
|---|---|---|---:|---:|---:|---:|
| `access_cas_attendance_identity_manager` | `model_cas_attendance_identity` | `cas_attendance_core.group_cas_attendance_manager` | 1 | 1 | 1 | 0 |
| `access_cas_attendance_import_supervisor` | `model_cas_attendance_import` | `cas_attendance_core.group_cas_attendance_supervisor` | 1 | 1 | 1 | 1 |
| `access_cas_attendance_import_line_supervisor` | `model_cas_attendance_import_line` | `cas_attendance_core.group_cas_attendance_supervisor` | 1 | 1 | 1 | 0 |
| `access_cas_guard_batch_guard` | `model_cas_guard_batch` | `cas_attendance_core.group_cas_attendance_guard` | 1 | 1 | 1 | 1 |
| `access_cas_guard_batch_line_guard` | `model_cas_guard_batch_line` | `cas_attendance_core.group_cas_attendance_guard` | 1 | 1 | 1 | 1 |

## Record Ruleها

| XML ID | عنوان | مدل | گروه‌ها | Domain |
|---|---|---|---|---|
| `rule_cas_attendance_identity_company` | شناسه‌های حضور شرکت‌های مجاز | `model_cas_attendance_identity` | — | `[('company_id','in',company_ids)]` |
| `rule_cas_attendance_import_company` | ورودی‌های حضور شرکت‌های مجاز | `model_cas_attendance_import` | — | `[('company_id','in',company_ids)]` |
| `rule_cas_attendance_import_line_company` | ردیف‌های ورودی شرکت‌های مجاز | `model_cas_attendance_import_line` | — | `[('company_id','in',company_ids)]` |
| `rule_cas_guard_batch_company` | بچ‌های نگهبانی شرکت‌های مجاز | `model_cas_guard_batch` | — | `[('company_id','in',company_ids)]` |
| `rule_cas_guard_batch_line_company` | ردیف‌های نگهبانی شرکت‌های مجاز | `model_cas_guard_batch_line` | — | `[('company_id','in',company_ids)]` |

## منوها

| XML ID | عنوان | والد | action | گروه |
|---|---|---|---|---|
| `menu_cas_guard_batch` | ثبت گروهی نگهبانی | `cas_attendance_core.menu_cas_attendance_operations` | `action_cas_guard_batch` | `cas_attendance_core.group_cas_attendance_guard` |
| `menu_cas_attendance_import` | ورود فایل دستگاه و نگهبانی | `cas_attendance_core.menu_cas_attendance_operations` | `action_cas_attendance_import` | `cas_attendance_core.group_cas_attendance_supervisor` |
| `menu_cas_attendance_identity` | نگاشت شناسه‌های خارجی | `cas_shift_management.menu_cas_shift_config` | `action_cas_attendance_identity` | `cas_attendance_core.group_cas_attendance_manager` |

## Actionها

| XML ID | نوع | عنوان | مدل/تگ | view mode | فایل |
|---|---|---|---|---|---|
| `action_cas_guard_batch` | `ir.actions.act_window` | ثبت گروهی نگهبانی | `cas.guard.batch` | `list,form` | `views/guard_batch_views.xml` |
| `action_cas_attendance_identity` | `ir.actions.act_window` | نگاشت شناسه‌های خارجی | `cas.attendance.identity` | `list,form` | `views/identity_views.xml` |
| `action_cas_attendance_import` | `ir.actions.act_window` | ورود فایل دستگاه و نگهبانی | `cas.attendance.import` | `list,form` | `views/import_views.xml` |

## Cron و Sequence

Cron یا sequence اختصاصی در XML ندارد.

## Assetهای رابط کاربری

Asset اختصاصی ندارد.

## داده‌های بارگذاری‌شده از manifest

- `security/cas_attendance_operations_security.xml`
- `security/ir.model.access.csv`
- `views/identity_views.xml`
- `views/import_views.xml`
- `views/guard_batch_views.xml`
- `views/operations_menus.xml`

## آزمون‌های موجود

- `tests/test_attendance_operations.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
