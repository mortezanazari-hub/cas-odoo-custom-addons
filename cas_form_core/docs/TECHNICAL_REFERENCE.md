# مرجع فنی استخراج‌شده از کد: CAS Form Core

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_form_core` |
| نسخه | `19.0.1.1.0` |
| عنوان | CAS Form Core |
| خلاصه | Versioned and secure form-definition foundation |
| دسته | Technical |
| نوع برنامه | Application |
| نصب خودکار | — |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `cas_core`, `mail`, `web` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 7 | مدل و منطق دامنه |
| `views/` | 4 | نما، action و menu |
| `security/` | 2 | گروه، ACL و record rule |
| `data/` | 1 | داده پایه، sequence و cron |
| `tests/` | 3 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `cas.form.answer` — کلاس `CasFormAnswer`

- منبع: `models/form_answer.py:27`
- inherits: —
- توضیح فنی: CAS Form Typed Answer

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `submission_id` | `Many2one` | ثبت فرم | `cas.form.submission` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `field_id` | `Many2one` | فیلد | `cas.form.field` | True | — | — | — | — |
| `field_sequence` | `Integer` | — | — | — | — | — | — | — / True |
| `field_type` | `Selection` | — | — | — | — | — | — | — / True |
| `field_key` | `Char` | — | — | — | — | — | — | — / True |
| `value_char` | `Char` | مقدار متنی کوتاه | — | — | — | — | — | — |
| `value_text` | `Text` | مقدار متنی بلند | — | — | — | — | — | — |
| `value_integer` | `Integer` | مقدار عدد صحیح | — | — | — | — | — | — |
| `value_float` | `Float` | مقدار عدد اعشاری | — | — | — | — | — | — |
| `value_boolean` | `Boolean` | مقدار بله/خیر | — | — | — | — | — | — |
| `value_date` | `Date` | مقدار تاریخ | — | — | — | — | — | — |
| `value_datetime` | `Datetime` | مقدار تاریخ و ساعت | — | — | — | — | — | — |
| `value_time_seconds` | `Integer` | مقدار ساعت به ثانیه | — | — | — | — | — | — |
| `value_monetary` | `Monetary` | مقدار مبلغ | — | — | — | — | — | — |
| `currency_id` | `Many2one` | ارز | `res.currency` | — | — | — | — | — |
| `value_option_id` | `Many2one` | گزینه انتخابی | `cas.form.field.option` | — | — | — | — | — |
| `value_option_ids` | `Many2many` | گزینه‌های انتخابی | `cas.form.field.option` | — | — | — | — | — |
| `value_reference_model` | `Char` | مدل رکورد مرتبط | — | — | — | — | — | — |
| `value_reference_id` | `Integer` | شناسه رکورد مرتبط | — | — | — | — | — | — |
| `value_reference_name` | `Char` | عنوان ثبت‌شده رکورد مرتبط | — | — | — | — | — | — |
| `value_json` | `Json` | مقدار ساختاریافته | — | — | — | — | — | — |

**مقادیر Selection/State**

- `field_type`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_check_field_version()` | `api.constrains('submission_id', 'field_id')` | 91 |
| `create()` | `api.model_create_multi` | 99 |
| `write()` | — | 108 |
| `unlink()` | — | 115 |
| `_empty_value_dict()` | `staticmethod` | 121 |
| `_decimal_value()` | `staticmethod` | 142 |
| `_validate_numeric_config()` | `staticmethod` | 153 |
| `_validate_text_config()` | `staticmethod` | 176 |
| `_parse_time_seconds()` | `staticmethod` | 205 |
| `_normalized_values()` | `api.model` | 225 |
| `_is_empty()` | — | 345 |
| `_export_value()` | — | 364 |

Constraints سمت سرور: `_check_field_version()`

### `cas.form.definition` — کلاس `CasFormDefinition`

- منبع: `models/form_definition.py:14`
- inherits: `mail.thread`، `mail.activity.mixin`
- توضیح فنی: CAS Form Definition

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `name` | `Char` | عنوان فرم | — | True | — | True | — | — |
| `code` | `Char` | کد فنی | — | True | — | True | — | — |
| `description` | `Text` | توضیحات | — | — | — | — | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `owner_user_id` | `Many2one` | مالک فرایند | `res.users` | — | — | True | `lambda self: self.env.user` | — |
| `version_ids` | `One2many` | نسخه‌ها | `cas.form.version` | — | — | — | — | — |
| `current_version_id` | `Many2one` | نسخه فعال | `cas.form.version` | — | True | True | — | — |
| `active` | `Boolean` | — | — | — | — | True | `True` | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_check_code()` | `api.constrains('code')` | 64 |
| `create()` | `api.model_create_multi` | 75 |
| `write()` | — | 81 |
| `unlink()` | — | 97 |
| `action_create_initial_version()` | — | 110 |

Constraints سمت سرور: `_check_code()`

### `cas.form.versioned.mixin` — کلاس `CasFormVersionedMixin`

- منبع: `models/form_field.py:28`
- inherits: —
- توضیح فنی: CAS Form Versioned Record Mixin

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `version_id` | `Many2one` | نسخه فرم | `cas.form.version` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 46 |
| `write()` | — | 55 |
| `unlink()` | — | 64 |

### `cas.form.field` — کلاس `CasFormField`

- منبع: `models/form_field.py:72`
- inherits: `cas.form.versioned.mixin`
- توضیح فنی: CAS Form Field

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `sequence` | `Integer` | — | — | — | — | — | `10` | — |
| `field_uuid` | `Char` | شناسه پایدار | — | True | True | — | `lambda self: str(uuid.uuid4())` | — |
| `technical_key` | `Char` | کلید فنی | — | True | — | — | — | — |
| `label` | `Char` | عنوان | — | True | — | — | — | — |
| `field_type` | `Selection` | نوع فیلد | — | True | — | — | `short_text` | — |
| `required` | `Boolean` | اجباری | — | — | — | — | — | — |
| `readonly` | `Boolean` | فقط خواندنی | — | — | — | — | — | — |
| `reportable` | `Boolean` | قابل گزارش | — | — | — | — | `True` | — |
| `placeholder` | `Char` | متن نمونه | — | — | — | — | — | — |
| `help_text` | `Text` | راهنما | — | — | — | — | — | — |
| `default_value` | `Json` | مقدار پیش‌فرض | — | — | — | — | — | — |
| `validation_config` | `Json` | تنظیمات اعتبارسنجی | — | — | — | — | `dict` | — |
| `allowed_model` | `Char` | مدل مجاز | — | — | — | — | — | — |
| `option_ids` | `One2many` | گزینه‌ها | `cas.form.field.option` | — | — | — | — | — |

**مقادیر Selection/State**

- `field_type`: `short_text` = متن کوتاه، `long_text` = متن بلند، `rich_text` = متن قالب‌دار، `integer` = عدد صحیح، `decimal` = عدد اعشاری، `percentage` = درصد، `monetary` = مبلغ، `boolean` = بله/خیر، `single_select` = انتخاب تکی، `multi_select` = انتخاب چندگانه، `radio` = رادیویی، `dropdown` = فهرست کشویی، `tag` = برچسب، `date` = تاریخ، `datetime` = تاریخ و ساعت، `time` = ساعت، `file` = فایل، `image` = تصویر، `user` = کاربر، `employee` = کارکن، `department` = دپارتمان، `company` = شرکت، `record_reference` = رکورد مرتبط، `computed` = محاسبه‌شده، `display` = فقط نمایشی

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 158 |
| `write()` | — | 164 |
| `_get_allowed_reference_models()` | `api.model` | 172 |
| `_check_technical_key()` | `api.constrains('technical_key')` | 177 |
| `_check_allowed_model_usage()` | `api.constrains('allowed_model', 'field_type')` | 190 |
| `_validate_definition()` | — | 205 |

Constraints سمت سرور: `_check_technical_key()`, `_check_allowed_model_usage()`

### `cas.form.field.option` — کلاس `CasFormFieldOption`

- منبع: `models/form_field.py:218`
- inherits: —
- توضیح فنی: CAS Form Field Option

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `field_id` | `Many2one` | فیلد | `cas.form.field` | True | — | — | — | — |
| `version_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `sequence` | `Integer` | — | — | — | — | — | `10` | — |
| `technical_key` | `Char` | کلید فنی | — | True | — | — | — | — |
| `label` | `Char` | عنوان | — | True | — | — | — | — |
| `active` | `Boolean` | — | — | — | — | — | `True` | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 251 |
| `write()` | — | 261 |
| `unlink()` | — | 270 |
| `_check_technical_key()` | `api.constrains('technical_key')` | 276 |

Constraints سمت سرور: `_check_technical_key()`

### `cas.form.node` — کلاس `CasFormNode`

- منبع: `models/form_node.py:11`
- inherits: `cas.form.versioned.mixin`
- توضیح فنی: CAS Form Layout Node

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `sequence` | `Integer` | — | — | — | — | — | `10` | — |
| `technical_key` | `Char` | کلید فنی | — | True | — | — | — | — |
| `node_type` | `Selection` | نوع | — | True | — | — | `field` | — |
| `title` | `Char` | عنوان | — | — | — | — | — | — |
| `help_text` | `Text` | توضیح | — | — | — | — | — | — |
| `parent_id` | `Many2one` | والد | `cas.form.node` | — | — | — | — | — |
| `parent_path` | `Char` | — | — | — | — | — | — | — |
| `child_ids` | `One2many` | اجزا | `cas.form.node` | — | — | — | — | — |
| `field_id` | `Many2one` | فیلد | `cas.form.field` | — | — | — | — | — |
| `column_count` | `Integer` | تعداد ستون | — | — | — | — | `1` | — |
| `column_span` | `Integer` | عرض ستونی | — | — | — | — | `1` | — |

**مقادیر Selection/State**

- `node_type`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 67 |
| `write()` | — | 73 |
| `_check_technical_key()` | `api.constrains('technical_key')` | 79 |
| `_check_parent_version()` | `api.constrains('parent_id', 'version_id')` | 87 |
| `_check_field_node()` | `api.constrains('node_type', 'field_id', 'version_id')` | 95 |

Constraints سمت سرور: `_check_technical_key()`, `_check_parent_version()`, `_check_field_node()`

### `cas.form.submission` — کلاس `CasFormSubmission`

- منبع: `models/form_submission.py:9`
- inherits: `mail.thread`، `mail.activity.mixin`
- توضیح فنی: CAS Form Submission

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `number` | `Char` | شماره رهگیری | — | True | True | True | `New` | — |
| `version_id` | `Many2one` | نسخه فرم | `cas.form.version` | True | — | True | — | — |
| `definition_id` | `Many2one` | فرم | — | — | — | — | — | — / True |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `owner_user_id` | `Many2one` | مالک ثبت | `res.users` | True | — | True | `lambda self: self.env.user` | — |
| `state` | `Selection` | وضعیت | — | True | — | True | `draft` | — |
| `answer_ids` | `One2many` | پاسخ‌ها | `cas.form.answer` | — | — | — | — | — |
| `submitted_at` | `Datetime` | زمان ارسال | — | — | True | — | — | — |
| `submitted_by_id` | `Many2one` | ارسال‌کننده | `res.users` | — | True | — | — | — |
| `snapshot_json` | `Json` | Snapshot نهایی | — | — | True | — | — | — |
| `reopen_count` | `Integer` | تعداد بازگشایی | — | — | True | — | — | — |

**مقادیر Selection/State**

- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_can_manage_owners()` | — | 91 |
| `_sudo_answers()` | — | 96 |
| `create()` | `api.model_create_multi` | 105 |
| `write()` | — | 125 |
| `unlink()` | — | 153 |
| `_check_draft_and_access()` | — | 158 |
| `action_save_answers()` | — | 164 |
| `action_get_answers()` | — | 212 |
| `_validate_required_answers()` | — | 220 |
| `_build_snapshot()` | — | 235 |
| `action_submit()` | — | 261 |
| `action_cancel()` | — | 277 |
| `action_reopen()` | — | 282 |

### `cas.form.version` — کلاس `CasFormVersion`

- منبع: `models/form_version.py:12`
- inherits: `mail.thread`، `mail.activity.mixin`
- توضیح فنی: CAS Form Version

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `definition_id` | `Many2one` | فرم | `cas.form.definition` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `name` | `Char` | عنوان نسخه | — | True | — | — | — | — |
| `revision` | `Integer` | شماره بازنگری | — | True | — | — | `1` | — |
| `state` | `Selection` | وضعیت | — | True | — | True | `draft` | — |
| `notes` | `Text` | یادداشت بازنگری | — | — | — | — | — | — |
| `effective_from` | `Datetime` | شروع اعتبار | — | — | — | — | — | — |
| `published_at` | `Datetime` | زمان انتشار | — | — | True | — | — | — |
| `published_by_id` | `Many2one` | منتشرکننده | `res.users` | — | True | — | — | — |
| `schema_hash` | `Char` | اثر انگشت ساختار | — | — | True | — | — | — |
| `field_ids` | `One2many` | فیلدها | `cas.form.field` | — | — | — | — | — |
| `node_ids` | `One2many` | ساختار فرم | `cas.form.node` | — | — | — | — | — |

**مقادیر Selection/State**

- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 83 |
| `write()` | — | 90 |
| `unlink()` | — | 102 |
| `_check_publish_access()` | — | 109 |
| `_schema_payload()` | — | 115 |
| `_compute_schema_hash()` | — | 161 |
| `_validate_publishable()` | — | 171 |
| `action_publish()` | — | 196 |
| `action_archive()` | — | 215 |
| `action_new_revision()` | — | 225 |

## گروه‌های امنیتی

| XML ID | عنوان | implied groups | فایل |
|---|---|---|---|
| `group_cas_form_user` | کاربر فرم‌های سازمانی | [(4, ref('base.group_user'))] | `security/cas_form_security.xml` |
| `group_cas_form_designer` | طراح فرم‌های سازمانی | [(4, ref('cas_form_core.group_cas_form_user'))] | `security/cas_form_security.xml` |
| `group_cas_form_publisher` | منتشرکننده فرم‌های سازمانی | [(4, ref('cas_form_core.group_cas_form_designer'))] | `security/cas_form_security.xml` |
| `group_cas_form_manager` | مدیر فنی فرم‌های سازمانی | [(4, ref('cas_form_core.group_cas_form_publisher'))] | `security/cas_form_security.xml` |
| `base.group_system` | — | [(4, ref('cas_form_core.group_cas_form_manager'))] | `security/cas_form_security.xml` |

## ماتریس ACL

| ACL | مدل | گروه | Read | Write | Create | Unlink |
|---|---|---|---:|---:|---:|---:|
| `access_cas_form_definition_user` | `model_cas_form_definition` | `group_cas_form_user` | 1 | 0 | 0 | 0 |
| `access_cas_form_version_user` | `model_cas_form_version` | `group_cas_form_user` | 1 | 0 | 0 | 0 |
| `access_cas_form_field_user` | `model_cas_form_field` | `group_cas_form_user` | 1 | 0 | 0 | 0 |
| `access_cas_form_field_option_user` | `model_cas_form_field_option` | `group_cas_form_user` | 1 | 0 | 0 | 0 |
| `access_cas_form_node_user` | `model_cas_form_node` | `group_cas_form_user` | 1 | 0 | 0 | 0 |
| `access_cas_form_definition_designer` | `model_cas_form_definition` | `group_cas_form_designer` | 1 | 1 | 1 | 0 |
| `access_cas_form_version_designer` | `model_cas_form_version` | `group_cas_form_designer` | 1 | 1 | 1 | 0 |
| `access_cas_form_field_designer` | `model_cas_form_field` | `group_cas_form_designer` | 1 | 1 | 1 | 1 |
| `access_cas_form_field_option_designer` | `model_cas_form_field_option` | `group_cas_form_designer` | 1 | 1 | 1 | 1 |
| `access_cas_form_node_designer` | `model_cas_form_node` | `group_cas_form_designer` | 1 | 1 | 1 | 1 |
| `access_cas_form_definition_manager` | `model_cas_form_definition` | `group_cas_form_manager` | 1 | 1 | 1 | 1 |
| `access_cas_form_version_manager` | `model_cas_form_version` | `group_cas_form_manager` | 1 | 1 | 1 | 1 |
| `access_cas_form_submission_user` | `model_cas_form_submission` | `group_cas_form_user` | 1 | 1 | 1 | 1 |
| `access_cas_form_submission_manager` | `model_cas_form_submission` | `group_cas_form_manager` | 1 | 1 | 1 | 1 |
| `access_cas_form_answer_manager` | `model_cas_form_answer` | `group_cas_form_manager` | 1 | 1 | 1 | 1 |

## Record Ruleها

| XML ID | عنوان | مدل | گروه‌ها | Domain |
|---|---|---|---|---|
| `rule_cas_form_definition_company` | فرم‌ها: محدوده شرکت | `model_cas_form_definition` | [(4, ref('cas_form_core.group_cas_form_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_cas_form_version_company` | نسخه فرم: محدوده شرکت | `model_cas_form_version` | [(4, ref('cas_form_core.group_cas_form_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_cas_form_field_company` | فیلد فرم: محدوده شرکت | `model_cas_form_field` | [(4, ref('cas_form_core.group_cas_form_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_cas_form_field_option_company` | گزینه فیلد: محدوده شرکت | `model_cas_form_field_option` | [(4, ref('cas_form_core.group_cas_form_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_cas_form_node_company` | ساختار فرم: محدوده شرکت | `model_cas_form_node` | [(4, ref('cas_form_core.group_cas_form_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_cas_form_submission_user_own` | ثبت فرم: مالک یا ایجادکننده | `model_cas_form_submission` | [(4, ref('cas_form_core.group_cas_form_user'))] | `['&', ('company_id', 'in', company_ids), '\|', ('owner_user_id', '=', user.id), ('create_uid', '=', user.id)]` |
| `rule_cas_form_submission_manager_company` | ثبت فرم: مدیر در محدوده شرکت | `model_cas_form_submission` | [(4, ref('cas_form_core.group_cas_form_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_cas_form_answer_manager_company` | پاسخ فرم: مدیر در محدوده شرکت | `model_cas_form_answer` | [(4, ref('cas_form_core.group_cas_form_manager'))] | `[('company_id', 'in', company_ids)]` |

## منوها

| XML ID | عنوان | والد | action | گروه |
|---|---|---|---|---|
| `menu_cas_forms_root` | فرم‌های سازمانی | — | — | `cas_form_core.group_cas_form_user` |
| `menu_cas_form_submissions` | ثبت‌های فرم | `menu_cas_forms_root` | `action_cas_form_submission` | `cas_form_core.group_cas_form_user` |
| `menu_cas_forms_configuration` | طراحی و پیکربندی | `menu_cas_forms_root` | — | `cas_form_core.group_cas_form_designer` |
| `menu_cas_form_definitions` | تعریف فرم‌ها | `menu_cas_forms_configuration` | `action_cas_form_definition` | — |
| `menu_cas_form_versions` | نسخه‌های فرم | `menu_cas_forms_configuration` | `action_cas_form_version` | — |

## Actionها

| XML ID | نوع | عنوان | مدل/تگ | view mode | فایل |
|---|---|---|---|---|---|
| `action_cas_form_definition` | `ir.actions.act_window` | فرم‌های سازمانی | `cas.form.definition` | `list,form` | `views/cas_form_definition_views.xml` |
| `action_cas_form_submission` | `ir.actions.act_window` | ثبت‌های فرم | `cas.form.submission` | `list,form` | `views/cas_form_submission_views.xml` |
| `action_cas_form_version` | `ir.actions.act_window` | نسخه‌های فرم | `cas.form.version` | `list,form` | `views/cas_form_version_views.xml` |

## Cron و Sequence

**Sequenceها**

| XML ID | عنوان | code | prefix |
|---|---|---|---|
| `seq_cas_form_submission` | شماره رهگیری ثبت فرم | `cas.form.submission` | `FRM/%(year)s/` |

## Assetهای رابط کاربری

Asset اختصاصی ندارد.

## داده‌های بارگذاری‌شده از manifest

- `security/cas_form_security.xml`
- `security/ir.model.access.csv`
- `data/cas_form_sequence.xml`
- `views/cas_form_definition_views.xml`
- `views/cas_form_version_views.xml`
- `views/cas_form_submission_views.xml`
- `views/cas_form_menus.xml`

## آزمون‌های موجود

- `tests/test_form_submission.py`
- `tests/test_form_versioning.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
