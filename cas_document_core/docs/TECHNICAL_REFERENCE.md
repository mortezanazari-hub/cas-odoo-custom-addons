# مرجع فنی استخراج‌شده از کد: CAS Document Core

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_document_core` |
| نسخه | `19.0.1.0.0` |
| عنوان | CAS Document Core |
| خلاصه | Secure, versioned organizational document foundation with pluggable storage |
| دسته | Productivity/Documents |
| نوع برنامه | Application |
| نصب خودکار | — |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `mail` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 6 | مدل و منطق دامنه |
| `wizard/` | 3 | عملیات موقت/مرحله‌ای |
| `views/` | 5 | نما، action و menu |
| `security/` | 2 | گروه، ACL و record rule |
| `data/` | 2 | داده پایه، sequence و cron |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `cas.document.tag` — کلاس `CasDocumentTag`

- منبع: `models/document.py:19`
- inherits: —
- توضیح فنی: CAS Document Tag

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `name` | `Char` | عنوان | — | True | — | — | — | — |
| `color` | `Integer` | — | — | — | — | — | — | — |

### `cas.document` — کلاس `CasDocument`

- منبع: `models/document.py:30`
- inherits: `mail.thread`، `mail.activity.mixin`
- توضیح فنی: CAS Versioned Document

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `number` | `Char` | شماره سند | — | — | True | — | `New` | — |
| `name` | `Char` | عنوان | — | True | — | True | — | — |
| `description` | `Text` | شرح | — | — | — | — | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `folder_id` | `Many2one` | پوشه | `cas.document.folder` | True | — | — | — | — |
| `owner_user_id` | `Many2one` | مالک | `res.users` | True | — | — | `lambda self: self.env.user` | — |
| `authorized_user_ids` | `Many2many` | کاربران مجاز | `res.users` | — | — | — | — | — |
| `confidentiality` | `Selection` | CONFIDENTIALITY | — | True | — | True | `normal` | — |
| `tag_ids` | `Many2many` | برچسب‌ها | `cas.document.tag` | — | — | — | — | — |
| `storage_backend_id` | `Many2one` | ذخیره‌ساز | `cas.document.storage.backend` | True | — | — | — | — |
| `state` | `Selection` | وضعیت | — | True | True | True | `draft` | — |
| `retention_until` | `Date` | نگهداری تا | — | — | — | — | — | — |
| `legal_hold` | `Boolean` | توقف حقوقی امحا | — | — | — | True | — | — |
| `current_version_id` | `Many2one` | نسخه جاری | `cas.document.version` | — | True | — | — | — |
| `version_ids` | `One2many` | نسخه‌ها | `cas.document.version` | — | — | — | — | — |
| `version_count` | `Integer` | تعداد نسخه | — | — | — | — | — | _compute_version_count / — |
| `current_sha256` | `Char` | SHA-256 نسخه جاری | — | — | True | — | — | — |
| `link_ids` | `One2many` | پیوندهای کسب‌وکار | `cas.document.link` | — | — | — | — | — |
| `event_ids` | `One2many` | تاریخچه رسمی | `cas.document.event` | — | — | — | — | — |

**مقادیر Selection/State**

- `confidentiality`: —
- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 82 |
| `write()` | — | 101 |
| `unlink()` | — | 112 |
| `_compute_version_count()` | `api.depends('version_ids')` | 116 |
| `_check_company_contract()` | `api.constrains('company_id', 'folder_id', 'owner_user_id', 'authorized_user_ids', 'storage_backend_id')` | 121 |
| `_require_editor()` | — | 131 |
| `_append_event()` | — | 143 |
| `action_activate()` | — | 157 |
| `action_archive()` | — | 166 |
| `action_destroy()` | — | 175 |
| `action_open_upload_version()` | — | 188 |
| `add_version()` | — | 200 |

Constraints سمت سرور: `_check_company_contract()`

### `cas.document.version` — کلاس `CasDocumentVersion`

- منبع: `models/document.py:255`
- inherits: —
- توضیح فنی: CAS Immutable Document Version

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `document_id` | `Many2one` | سند | `cas.document` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `version_number` | `Integer` | نسخه | — | True | True | — | — | — |
| `filename` | `Char` | نام فایل | — | True | True | — | — | — |
| `mimetype` | `Char` | نوع فایل | — | True | True | — | — | — |
| `size_bytes` | `Integer` | حجم (بایت) | — | True | True | — | — | — |
| `sha256` | `Char` | SHA-256 | — | True | True | — | — | — |
| `attachment_id` | `Many2one` | فایل Odoo | `ir.attachment` | — | True | — | — | — |
| `external_path` | `Char` | مسیر خارجی | — | — | True | — | — | — |
| `created_by_user_id` | `Many2one` | ثبت‌کننده | `res.users` | True | True | — | — | — |
| `created_at` | `Datetime` | زمان ثبت | — | True | True | — | `fields.Datetime.now` | — |
| `note` | `Text` | شرح نسخه | — | — | True | — | — | — |
| `ocr_text` | `Text` | متن OCR | — | — | True | — | — | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 284 |
| `write()` | — | 289 |
| `unlink()` | — | 295 |
| `content()` | — | 298 |
| `action_download()` | — | 305 |

### `cas.document.link` — کلاس `CasDocumentLink`

- منبع: `models/document.py:322`
- inherits: —
- توضیح فنی: CAS Document Business Link

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `document_id` | `Many2one` | سند | `cas.document` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `source_model` | `Char` | مدل منبع | — | True | — | — | — | — |
| `source_record_id` | `Integer` | شناسه منبع | — | True | — | — | — | — |
| `source_title` | `Char` | عنوان منبع | — | True | — | — | — | — |
| `relation_type` | `Selection` | نوع ارتباط | — | True | — | — | `reference` | — |

**مقادیر Selection/State**

- `relation_type`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 346 |
| `write()` | — | 355 |
| `unlink()` | — | 358 |

### `cas.document.event` — کلاس `CasDocumentEvent`

- منبع: `models/document_event.py:5`
- inherits: —
- توضیح فنی: CAS Document Append-only Event

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `document_id` | `Many2one` | سند | `cas.document` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `version_id` | `Many2one` | نسخه | `cas.document.version` | — | — | — | — | — |
| `event_type` | `Selection` | رویداد | — | True | True | — | — | — |
| `actor_user_id` | `Many2one` | اقدام‌کننده | `res.users` | True | True | — | — | — |
| `event_at` | `Datetime` | زمان | — | True | True | — | `fields.Datetime.now` | — |
| `note` | `Text` | توضیح | — | — | True | — | — | — |

**مقادیر Selection/State**

- `event_type`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 34 |
| `write()` | — | 39 |
| `unlink()` | — | 42 |

### `cas.document.folder` — کلاس `CasDocumentFolder`

- منبع: `models/document_folder.py:12`
- inherits: —
- توضیح فنی: CAS Document Folder

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `name` | `Char` | عنوان | — | True | — | — | — | — |
| `code` | `Char` | کد | — | True | — | — | — | — |
| `active` | `Boolean` | — | — | — | — | — | `True` | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `parent_id` | `Many2one` | پوشه بالادست | `cas.document.folder` | — | — | — | — | — |
| `parent_path` | `Char` | — | — | — | — | — | — | — |
| `child_ids` | `One2many` | زیرپوشه‌ها | `cas.document.folder` | — | — | — | — | — |
| `complete_name` | `Char` | مسیر کامل | — | — | — | — | — | _compute_complete_name / True |
| `manager_user_id` | `Many2one` | مدیر پوشه | `res.users` | — | — | — | — | — |
| `confidentiality` | `Selection` | CONFIDENTIALITY | — | True | — | — | `normal` | — |
| `document_ids` | `One2many` | اسناد | `cas.document` | — | — | — | — | — |

**مقادیر Selection/State**

- `confidentiality`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_compute_complete_name()` | `api.depends('name', 'parent_id.complete_name')` | 39 |
| `_check_contract()` | `api.constrains('parent_id', 'company_id', 'manager_user_id')` | 44 |

Constraints سمت سرور: `_check_contract()`

### `cas.document.ocr.provider` — کلاس `CasDocumentOcrProvider`

- منبع: `models/document_ocr.py:5`
- inherits: —
- توضیح فنی: CAS OCR Provider

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `sequence` | `Integer` | — | — | — | — | — | `10` | — |
| `name` | `Char` | عنوان | — | True | — | — | — | — |
| `active` | `Boolean` | — | — | — | — | — | `True` | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `provider_type` | `Selection` | نوع سرویس | — | True | — | — | `manual` | — |
| `endpoint_url` | `Char` | نشانی سرویس | — | — | — | — | — | — |
| `secret_parameter_key` | `Char` | کلید توکن در تنظیمات سیستم | — | — | — | — | — | — |
| `timeout_seconds` | `Integer` | مهلت (ثانیه) | — | — | — | — | `60` | — |

**مقادیر Selection/State**

- `provider_type`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_check_contract()` | `api.constrains('provider_type', 'endpoint_url', 'timeout_seconds')` | 25 |

Constraints سمت سرور: `_check_contract()`

### `cas.document.ocr.job` — کلاس `CasDocumentOcrJob`

- منبع: `models/document_ocr.py:33`
- inherits: `mail.thread`، `mail.activity.mixin`
- توضیح فنی: CAS OCR Review Job

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `version_id` | `Many2one` | نسخه سند | `cas.document.version` | True | — | — | — | — |
| `document_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `provider_id` | `Many2one` | سرویس | `cas.document.ocr.provider` | True | — | — | — | — |
| `state` | `Selection` | وضعیت | — | True | True | True | `queued` | — |
| `extracted_text` | `Text` | متن استخراج‌شده | — | — | — | — | — | — |
| `reviewer_user_id` | `Many2one` | بازبین | `res.users` | — | — | — | — | — |
| `attempt_count` | `Integer` | تعداد تلاش | — | — | True | — | — | — |
| `error_message` | `Text` | خطا | — | — | True | — | — | — |
| `completed_at` | `Datetime` | زمان تکمیل | — | — | True | — | — | — |

**مقادیر Selection/State**

- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `write()` | — | 62 |
| `action_submit_review()` | — | 68 |
| `action_confirm_text()` | — | 75 |
| `_cron_process_webhooks()` | `api.model` | 94 |

### `cas.document.storage.backend` — کلاس `CasDocumentStorageBackend`

- منبع: `models/storage_backend.py:12`
- inherits: `mail.thread`
- توضیح فنی: CAS Document Storage Backend

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `sequence` | `Integer` | — | — | — | — | — | `10` | — |
| `name` | `Char` | عنوان | — | True | — | True | — | — |
| `active` | `Boolean` | — | — | — | — | True | `True` | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `backend_type` | `Selection` | نوع ذخیره‌سازی | — | True | — | True | `database` | — |
| `base_url` | `Char` | نشانی Nextcloud | — | — | — | — | — | — |
| `root_path` | `Char` | مسیر ریشه | — | — | — | — | `CAS` | — |
| `username` | `Char` | نام کاربری | — | — | — | — | — | — |
| `secret_parameter_key` | `Char` | کلید رمز در تنظیمات سیستم | — | — | — | — | — | — |
| `timeout_seconds` | `Integer` | مهلت اتصال (ثانیه) | — | — | — | — | `30` | — |
| `verify_ssl` | `Boolean` | اعتبارسنجی SSL | — | — | — | — | `True` | — |
| `is_default` | `Boolean` | پیش‌فرض شرکت | — | — | — | True | — | — |
| `document_ids` | `One2many` | اسناد | `cas.document` | — | True | — | — | — |

**مقادیر Selection/State**

- `backend_type`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_check_contract()` | `api.constrains('backend_type', 'base_url', 'root_path', 'username', 'secret_parameter_key', 'timeout_seconds', 'is_default', 'company_id')` | 46 |
| `_credential()` | — | 62 |
| `_remote_url()` | — | 71 |
| `_request()` | — | 80 |
| `_ensure_remote_folder()` | — | 100 |
| `upload()` | — | 109 |
| `download()` | — | 118 |
| `action_test_connection()` | — | 124 |
| `default_for_company()` | `api.model` | 136 |

Constraints سمت سرور: `_check_contract()`

### `cas.document.upload.version.wizard` — کلاس `CasDocumentUploadVersionWizard`

- منبع: `wizard/upload_version_wizard.py:7`
- inherits: —
- توضیح فنی: CAS Upload Document Version

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `document_id` | `Many2one` | سند | `cas.document` | True | True | — | — | — |
| `file_data` | `Binary` | فایل | — | True | — | — | — | — |
| `filename` | `Char` | نام فایل | — | True | — | — | — | — |
| `note` | `Text` | شرح نسخه | — | — | — | — | — | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `action_confirm()` | — | 16 |

## گروه‌های امنیتی

| XML ID | عنوان | implied groups | فایل |
|---|---|---|---|
| `group_cas_document_user` | کاربر مدیریت اسناد | — | `security/cas_document_security.xml` |
| `group_cas_document_manager` | مدیر مدیریت اسناد | [(4, ref('group_cas_document_user'))] | `security/cas_document_security.xml` |
| `base.group_system` | — | [(4, ref('cas_document_core.group_cas_document_manager'))] | `security/cas_document_security.xml` |

## ماتریس ACL

| ACL | مدل | گروه | Read | Write | Create | Unlink |
|---|---|---|---:|---:|---:|---:|
| `access_document_user` | `model_cas_document` | `group_cas_document_user` | 1 | 1 | 1 | 0 |
| `access_document_manager` | `model_cas_document` | `group_cas_document_manager` | 1 | 1 | 1 | 0 |
| `access_document_folder_user` | `model_cas_document_folder` | `group_cas_document_user` | 1 | 0 | 0 | 0 |
| `access_document_folder_manager` | `model_cas_document_folder` | `group_cas_document_manager` | 1 | 1 | 1 | 1 |
| `access_document_backend_user` | `model_cas_document_storage_backend` | `group_cas_document_user` | 1 | 0 | 0 | 0 |
| `access_document_backend_manager` | `model_cas_document_storage_backend` | `group_cas_document_manager` | 1 | 1 | 1 | 1 |
| `access_document_version_user` | `model_cas_document_version` | `group_cas_document_user` | 1 | 0 | 0 | 0 |
| `access_document_version_manager` | `model_cas_document_version` | `group_cas_document_manager` | 1 | 0 | 0 | 0 |
| `access_document_tag_user` | `model_cas_document_tag` | `group_cas_document_user` | 1 | 0 | 0 | 0 |
| `access_document_tag_manager` | `model_cas_document_tag` | `group_cas_document_manager` | 1 | 1 | 1 | 1 |
| `access_document_link_user` | `model_cas_document_link` | `group_cas_document_user` | 1 | 0 | 1 | 0 |
| `access_document_link_manager` | `model_cas_document_link` | `group_cas_document_manager` | 1 | 0 | 1 | 1 |
| `access_document_event_user` | `model_cas_document_event` | `group_cas_document_user` | 1 | 0 | 0 | 0 |
| `access_document_event_manager` | `model_cas_document_event` | `group_cas_document_manager` | 1 | 0 | 0 | 0 |
| `access_document_ocr_provider_user` | `model_cas_document_ocr_provider` | `group_cas_document_user` | 1 | 0 | 0 | 0 |
| `access_document_ocr_provider_manager` | `model_cas_document_ocr_provider` | `group_cas_document_manager` | 1 | 1 | 1 | 1 |
| `access_document_ocr_job_user` | `model_cas_document_ocr_job` | `group_cas_document_user` | 1 | 1 | 1 | 0 |
| `access_document_ocr_job_manager` | `model_cas_document_ocr_job` | `group_cas_document_manager` | 1 | 1 | 1 | 0 |
| `access_document_upload_version_wizard` | `model_cas_document_upload_version_wizard` | `group_cas_document_user` | 1 | 1 | 1 | 1 |

## Record Ruleها

| XML ID | عنوان | مدل | گروه‌ها | Domain |
|---|---|---|---|---|
| `rule_document_user_scope` | سند: مالک، کاربر مجاز یا مدیر پوشه | `model_cas_document` | [(4, ref('group_cas_document_user'))] | `[('company_id', 'in', company_ids), '\|', '\|', ('owner_user_id', '=', user.id), ('authorized_user_ids', 'in', user.id), ('folder_id.manager_user_id', '=', user.id)]` |
| `rule_document_manager_company` | سند: مدیر در شرکت‌های مجاز | `model_cas_document` | [(4, ref('group_cas_document_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_document_folder_user` | پوشه: عادی یا تحت مدیریت کاربر | `model_cas_document_folder` | [(4, ref('group_cas_document_user'))] | `[('company_id', 'in', company_ids), '\|', ('confidentiality', '=', 'normal'), ('manager_user_id', '=', user.id)]` |
| `rule_document_folder_manager` | پوشه: مدیر در شرکت‌های مجاز | `model_cas_document_folder` | [(4, ref('group_cas_document_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_document_backend_company` | ذخیره‌ساز: شرکت‌های مجاز | `model_cas_document_storage_backend` | [(4, ref('group_cas_document_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_document_version_scope` | نسخه: سند قابل مشاهده | `model_cas_document_version` | [(4, ref('group_cas_document_user'))] | `[('company_id', 'in', company_ids), '\|', '\|', ('document_id.owner_user_id', '=', user.id), ('document_id.authorized_user_ids', 'in', user.id), ('document_id.folder_id.manager_user_id', '=', user.id)]` |
| `rule_document_link_scope` | پیوند: سند قابل مشاهده | `model_cas_document_link` | [(4, ref('group_cas_document_user'))] | `[('company_id', 'in', company_ids), '\|', '\|', ('document_id.owner_user_id', '=', user.id), ('document_id.authorized_user_ids', 'in', user.id), ('document_id.folder_id.manager_user_id', '=', user.id)]` |
| `rule_document_event_scope` | تاریخچه: سند قابل مشاهده | `model_cas_document_event` | [(4, ref('group_cas_document_user'))] | `[('company_id', 'in', company_ids), '\|', '\|', ('document_id.owner_user_id', '=', user.id), ('document_id.authorized_user_ids', 'in', user.id), ('document_id.folder_id.manager_user_id', '=', user.id)]` |
| `rule_document_ocr_job_scope` | OCR: سند قابل مشاهده | `model_cas_document_ocr_job` | [(4, ref('group_cas_document_user'))] | `[('company_id', 'in', company_ids), '\|', '\|', ('document_id.owner_user_id', '=', user.id), ('document_id.authorized_user_ids', 'in', user.id), ('document_id.folder_id.manager_user_id', '=', user.id)]` |
| `rule_document_ocr_provider_company` | سرویس OCR: شرکت‌های مجاز | `model_cas_document_ocr_provider` | [(4, ref('group_cas_document_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_document_version_manager` | نسخه: مدیر در شرکت‌های مجاز | `model_cas_document_version` | [(4, ref('group_cas_document_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_document_link_manager` | پیوند: مدیر در شرکت‌های مجاز | `model_cas_document_link` | [(4, ref('group_cas_document_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_document_event_manager` | تاریخچه: مدیر در شرکت‌های مجاز | `model_cas_document_event` | [(4, ref('group_cas_document_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_document_ocr_job_manager` | OCR: مدیر در شرکت‌های مجاز | `model_cas_document_ocr_job` | [(4, ref('group_cas_document_manager'))] | `[('company_id', 'in', company_ids)]` |

## منوها

| XML ID | عنوان | والد | action | گروه |
|---|---|---|---|---|
| `menu_document_root` | مدیریت اسناد | — | — | `group_cas_document_user` |
| `menu_documents` | اسناد | `menu_document_root` | `action_documents` | — |
| `menu_document_folders` | پوشه‌ها | `menu_document_root` | `action_document_folders` | — |
| `menu_document_ocr_jobs` | صف OCR | `menu_document_root` | `action_document_ocr_jobs` | — |
| `menu_document_config` | پیکربندی | `menu_document_root` | — | `group_cas_document_manager` |
| `menu_document_backends` | ذخیره‌سازها | `menu_document_config` | `action_document_backends` | — |
| `menu_document_ocr_providers` | سرویس‌های OCR | `menu_document_config` | `action_document_ocr_providers` | — |

## Actionها

| XML ID | نوع | عنوان | مدل/تگ | view mode | فایل |
|---|---|---|---|---|---|
| `action_document_backends` | `ir.actions.act_window` | ذخیره‌سازها | `cas.document.storage.backend` | `list,form` | `views/cas_document_backend_views.xml` |
| `action_document_folders` | `ir.actions.act_window` | پوشه‌ها | `cas.document.folder` | `list,form` | `views/cas_document_folder_views.xml` |
| `action_document_ocr_jobs` | `ir.actions.act_window` | صف OCR | `cas.document.ocr.job` | `list,form` | `views/cas_document_ocr_views.xml` |
| `action_document_ocr_providers` | `ir.actions.act_window` | سرویس‌های OCR | `cas.document.ocr.provider` | `list,form` | `views/cas_document_ocr_views.xml` |
| `action_documents` | `ir.actions.act_window` | اسناد | `cas.document` | `list,form` | `views/cas_document_views.xml` |

## Cron و Sequence

**Cronها**

| XML ID | عنوان | مدل/کد | تناوب |
|---|---|---|---|
| `ir_cron_cas_document_ocr` | CAS Documents: پردازش OCR | `model._cron_process_webhooks()` | 10 minutes |

**Sequenceها**

| XML ID | عنوان | code | prefix |
|---|---|---|---|
| `sequence_cas_document` | شماره سند CAS | `cas.document` | `DOC/%(year)s/` |

## Assetهای رابط کاربری

Asset اختصاصی ندارد.

## داده‌های بارگذاری‌شده از manifest

- `security/cas_document_security.xml`
- `security/ir.model.access.csv`
- `data/cas_document_sequence.xml`
- `data/cas_document_cron.xml`
- `views/cas_document_backend_views.xml`
- `views/cas_document_folder_views.xml`
- `views/cas_document_views.xml`
- `views/cas_document_ocr_views.xml`
- `wizard/upload_version_wizard_views.xml`
- `views/cas_document_menus.xml`

## آزمون‌های موجود

- `tests/test_document_core.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
