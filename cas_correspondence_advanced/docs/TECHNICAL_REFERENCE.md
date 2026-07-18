# مرجع فنی استخراج‌شده از کد: CAS Advanced Correspondence

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_correspondence_advanced` |
| نسخه | `19.0.1.0.0` |
| عنوان | CAS Advanced Correspondence |
| خلاصه | Official templates, inbound/outbound registry, immutable PDFs and auditable signatures |
| دسته | Productivity |
| نوع برنامه | Technical/Extension |
| نصب خودکار | — |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `cas_correspondence`, `cas_document_core` |
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

### `افزونه مدل` — کلاس `CasCorrespondenceAuditAdvanced`

- منبع: `models/letter.py:8`
- inherits: `cas.correspondence.audit`
- توضیح فنی: —

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `event_type` | `Selection` | — | — | — | — | — | — | — |

**مقادیر Selection/State**

- `event_type`: —

### `افزونه مدل` — کلاس `CasCorrespondenceLetterAdvanced`

- منبع: `models/letter.py:17`
- inherits: `cas.correspondence.letter`
- توضیح فنی: —

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `template_id` | `Many2one` | قالب رسمی | `cas.correspondence.template` | — | — | — | — | — |
| `document_id` | `Many2one` | سند نسخه‌دار | `cas.document` | — | True | — | — | — |
| `official_pdf_attachment_id` | `Many2one` | PDF رسمی | `ir.attachment` | — | True | — | — | — |
| `official_pdf_sha256` | `Char` | SHA-256 نسخه رسمی | — | — | True | — | — | — |
| `official_pdf_generated_at` | `Datetime` | زمان تولید PDF | — | — | True | — | — | — |
| `advanced_signature_ids` | `One2many` | امضاهای پیشرفته | `cas.correspondence.signature` | — | — | — | — | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_advanced_folder()` | — | 27 |
| `action_apply_template()` | — | 41 |
| `_store_official_pdf()` | — | 53 |
| `action_generate_official_pdf()` | — | 82 |
| `action_download_official_pdf()` | — | 92 |
| `action_send()` | — | 98 |

### `cas.correspondence.register` — کلاس `CasCorrespondenceRegister`

- منبع: `models/register.py:8`
- inherits: `mail.thread`، `mail.activity.mixin`
- توضیح فنی: CAS Inbound Outbound Correspondence Register

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `number` | `Char` | شماره ثبت | — | — | True | — | `New` | — |
| `direction` | `Selection` | — | — | True | — | True | — | — |
| `subject` | `Char` | موضوع | — | True | — | True | — | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `owner_user_id` | `Many2one` | مسئول | `res.users` | True | — | — | `lambda self: self.env.user` | — |
| `counterparty` | `Char` | فرستنده/گیرنده بیرونی | — | True | — | — | — | — |
| `external_number` | `Char` | شماره بیرونی | — | — | — | — | — | — |
| `external_date` | `Date` | تاریخ بیرونی | — | — | — | — | — | — |
| `channel` | `Selection` | — | — | True | — | — | `physical` | — |
| `confidentiality` | `Selection` | — | — | True | — | True | `normal` | — |
| `note` | `Html` | شرح | — | — | — | — | — | — |
| `attachment_id` | `Many2one` | فایل اصلی | `ir.attachment` | — | — | — | — | — |
| `file_data` | `Binary` | بارگذاری فایل | — | — | — | — | — | — |
| `file_name` | `Char` | نام فایل | — | — | — | — | — | — |
| `document_folder_id` | `Many2one` | پوشه اسناد | `cas.document.folder` | — | — | — | — | — |
| `document_id` | `Many2one` | سند نسخه‌دار | `cas.document` | — | True | — | — | — |
| `current_sha256` | `Char` | — | — | — | True | — | — | — |
| `state` | `Selection` | — | — | True | True | True | `draft` | — |
| `registered_at` | `Datetime` | — | — | — | True | — | — | — |
| `closed_at` | `Datetime` | — | — | — | True | — | — | — |
| `signature_ids` | `One2many` | امضاها | `cas.correspondence.signature` | — | — | — | — | — |
| `event_ids` | `One2many` | تاریخچه | `cas.correspondence.register.event` | — | — | — | — | — |

**مقادیر Selection/State**

- `direction`: —
- `channel`: —
- `confidentiality`: —
- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_check_contract()` | `api.constrains('company_id', 'owner_user_id', 'document_folder_id', 'attachment_id')` | 50 |
| `write()` | — | 59 |
| `unlink()` | — | 65 |
| `_folder()` | — | 70 |
| `_append_event()` | — | 84 |
| `action_register()` | — | 92 |
| `action_close()` | — | 124 |

Constraints سمت سرور: `_check_contract()`

### `cas.correspondence.register.event` — کلاس `CasCorrespondenceRegisterEvent`

- منبع: `models/register.py:133`
- inherits: —
- توضیح فنی: CAS Immutable Correspondence Register Event

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `register_id` | `Many2one` | — | `cas.correspondence.register` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | — | — | — | — / True |
| `event_type` | `Selection` | — | — | True | — | — | — | — |
| `actor_user_id` | `Many2one` | — | `res.users` | True | — | — | — | — |
| `event_at` | `Datetime` | — | — | True | True | — | `fields.Datetime.now` | — |
| `note` | `Text` | — | — | — | True | — | — | — |
| `digest` | `Char` | — | — | — | True | — | — | — |

**مقادیر Selection/State**

- `event_type`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 147 |
| `write()` | — | 152 |
| `unlink()` | — | 155 |

### `cas.correspondence.signature` — کلاس `CasCorrespondenceSignature`

- منبع: `models/signature.py:7`
- inherits: —
- توضیح فنی: CAS Auditable Correspondence Signature

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `letter_id` | `Many2one` | نامه داخلی | `cas.correspondence.letter` | — | — | — | — | — |
| `register_id` | `Many2one` | ثبت وارده/صادره | `cas.correspondence.register` | — | — | — | — | — |
| `company_id` | `Many2one` | — | `res.company` | — | — | — | — | _compute_company / True |
| `signer_user_id` | `Many2one` | امضاکننده | `res.users` | True | — | — | `lambda self: self.env.user` | — |
| `method` | `Selection` | — | — | True | True | — | `organizational` | — |
| `state` | `Selection` | — | — | True | True | — | `pending` | — |
| `source_digest` | `Char` | هش محتوای امضاشده | — | — | True | — | — | — |
| `provider_reference` | `Char` | شناسه سرویس امضا | — | — | True | — | — | — |
| `certificate_serial` | `Char` | شماره گواهی | — | — | True | — | — | — |
| `provider_signature_digest` | `Char` | هش امضای سرویس | — | — | True | — | — | — |
| `signed_at` | `Datetime` | — | — | — | True | — | — | — |
| `revoked_at` | `Datetime` | — | — | — | True | — | — | — |
| `revoke_reason` | `Text` | — | — | — | True | — | — | — |

**مقادیر Selection/State**

- `method`: —
- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_compute_company()` | `api.depends('letter_id.company_id', 'register_id.company_id')` | 30 |
| `_check_contract()` | `api.constrains('letter_id', 'register_id', 'signer_user_id')` | 35 |
| `create()` | `api.model_create_multi` | 43 |
| `write()` | — | 49 |
| `unlink()` | — | 54 |
| `_current_source_digest()` | — | 59 |
| `action_sign_organizational()` | — | 66 |
| `record_external_signature()` | — | 80 |
| `action_revoke()` | — | 99 |

Constraints سمت سرور: `_check_contract()`

### `cas.correspondence.template` — کلاس `CasCorrespondenceTemplate`

- منبع: `models/template.py:5`
- inherits: —
- توضیح فنی: CAS Official Correspondence Template

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `sequence` | `Integer` | — | — | — | — | — | `10` | — |
| `name` | `Char` | عنوان | — | True | — | — | — | — |
| `code` | `Char` | کد | — | True | — | — | — | — |
| `active` | `Boolean` | — | — | — | — | — | `True` | — |
| `company_id` | `Many2one` | شرکت | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `subject_pattern` | `Char` | الگوی موضوع | — | — | — | — | — | — |
| `header_html` | `Html` | سربرگ | — | — | — | — | — | — |
| `body_html` | `Html` | متن پایه | — | True | — | — | — | — |
| `footer_html` | `Html` | پابرگ | — | — | — | — | — | — |
| `document_folder_id` | `Many2one` | پوشه اسناد | `cas.document.folder` | — | — | — | — | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_check_company()` | `api.constrains('company_id', 'document_folder_id')` | 26 |

Constraints سمت سرور: `_check_company()`

## گروه‌های امنیتی

| XML ID | عنوان | implied groups | فایل |
|---|---|---|---|
| `cas_correspondence.group_cas_correspondence_user` | — | [(4, ref('cas_document_core.group_cas_document_user'))] | `security/cas_correspondence_advanced_security.xml` |
| `cas_correspondence.group_cas_correspondence_manager` | — | [(4, ref('cas_document_core.group_cas_document_manager'))] | `security/cas_correspondence_advanced_security.xml` |

## ماتریس ACL

| ACL | مدل | گروه | Read | Write | Create | Unlink |
|---|---|---|---:|---:|---:|---:|
| `access_correspondence_template_user` | `model_cas_correspondence_template` | `cas_correspondence.group_cas_correspondence_user` | 1 | 0 | 0 | 0 |
| `access_correspondence_template_manager` | `model_cas_correspondence_template` | `cas_correspondence.group_cas_correspondence_manager` | 1 | 1 | 1 | 1 |
| `access_correspondence_register_user` | `model_cas_correspondence_register` | `cas_correspondence.group_cas_correspondence_user` | 1 | 1 | 1 | 1 |
| `access_correspondence_register_manager` | `model_cas_correspondence_register` | `cas_correspondence.group_cas_correspondence_manager` | 1 | 1 | 1 | 1 |
| `access_correspondence_register_event_user` | `model_cas_correspondence_register_event` | `cas_correspondence.group_cas_correspondence_user` | 1 | 0 | 0 | 0 |
| `access_correspondence_signature_user` | `model_cas_correspondence_signature` | `cas_correspondence.group_cas_correspondence_user` | 1 | 1 | 1 | 1 |
| `access_correspondence_signature_manager` | `model_cas_correspondence_signature` | `cas_correspondence.group_cas_correspondence_manager` | 1 | 1 | 1 | 1 |

## Record Ruleها

| XML ID | عنوان | مدل | گروه‌ها | Domain |
|---|---|---|---|---|
| `rule_template_company` | قالب مکاتبات: شرکت‌های مجاز | `model_cas_correspondence_template` | [(4, ref('cas_correspondence.group_cas_correspondence_user'))] | `[('company_id', 'in', company_ids)]` |
| `rule_register_owner` | ثبت مکاتبات: مسئول رکورد | `model_cas_correspondence_register` | [(4, ref('cas_correspondence.group_cas_correspondence_user'))] | `[('company_id', 'in', company_ids), ('owner_user_id', '=', user.id)]` |
| `rule_register_manager` | ثبت مکاتبات: مدیر شرکت | `model_cas_correspondence_register` | [(4, ref('cas_correspondence.group_cas_correspondence_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_register_event_user` | رویداد ثبت: مسئول رکورد | `model_cas_correspondence_register_event` | [(4, ref('cas_correspondence.group_cas_correspondence_user'))] | `[('company_id', 'in', company_ids), ('register_id.owner_user_id', '=', user.id)]` |
| `rule_register_event_manager` | رویداد ثبت: مدیر شرکت | `model_cas_correspondence_register_event` | [(4, ref('cas_correspondence.group_cas_correspondence_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_signature_user` | امضا: امضاکننده یا ذی‌نفع منبع | `model_cas_correspondence_signature` | [(4, ref('cas_correspondence.group_cas_correspondence_user'))] | `[('company_id', 'in', company_ids), '\|', '\|', ('signer_user_id', '=', user.id), ('register_id.owner_user_id', '=', user.id), ('letter_id.authorized_user_ids', 'in', user.id)]` |
| `rule_signature_manager` | امضا: مدیر شرکت | `model_cas_correspondence_signature` | [(4, ref('cas_correspondence.group_cas_correspondence_manager'))] | `[('company_id', 'in', company_ids)]` |

## منوها

| XML ID | عنوان | والد | action | گروه |
|---|---|---|---|---|
| `menu_correspondence_registers` | دفتر وارده و صادره | `cas_correspondence.menu_correspondence_root` | `action_correspondence_registers` | — |
| `menu_correspondence_signatures` | دفتر امضاها | `cas_correspondence.menu_correspondence_root` | `action_correspondence_signatures` | — |
| `menu_correspondence_templates` | قالب‌های رسمی | `cas_correspondence.menu_correspondence_config` | `action_correspondence_templates` | `cas_correspondence.group_cas_correspondence_manager` |

## Actionها

| XML ID | نوع | عنوان | مدل/تگ | view mode | فایل |
|---|---|---|---|---|---|
| `action_report_correspondence_letter` | `cas.correspondence.letter` | نامه رسمی | `cas_correspondence_advanced.report_correspondence_letter` | — | `reports/correspondence_report.xml` |
| `action_correspondence_registers` | `ir.actions.act_window` | دفتر وارده و صادره | `cas.correspondence.register` | `list,form` | `views/correspondence_register_views.xml` |
| `action_correspondence_signatures` | `ir.actions.act_window` | دفتر امضاها | `cas.correspondence.signature` | `list` | `views/correspondence_signature_views.xml` |
| `action_correspondence_templates` | `ir.actions.act_window` | قالب‌های رسمی | `cas.correspondence.template` | `list,form` | `views/correspondence_template_views.xml` |

## Cron و Sequence

**Sequenceها**

| XML ID | عنوان | code | prefix |
|---|---|---|---|
| `sequence_correspondence_inbound` | CAS Inbound Correspondence | `cas.correspondence.inbound` | `IN/%(year)s/` |
| `sequence_correspondence_outbound` | CAS Outbound Correspondence | `cas.correspondence.outbound` | `OUT/%(year)s/` |

## Assetهای رابط کاربری

Asset اختصاصی ندارد.

## داده‌های بارگذاری‌شده از manifest

- `security/cas_correspondence_advanced_security.xml`
- `security/ir.model.access.csv`
- `data/cas_correspondence_advanced_sequence.xml`
- `reports/correspondence_report.xml`
- `views/correspondence_template_views.xml`
- `views/correspondence_register_views.xml`
- `views/correspondence_letter_views.xml`
- `views/correspondence_signature_views.xml`
- `views/correspondence_advanced_menus.xml`

## آزمون‌های موجود

- `tests/test_correspondence_advanced.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
