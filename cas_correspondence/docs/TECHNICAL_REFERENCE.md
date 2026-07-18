# مرجع فنی استخراج‌شده از کد: CAS Internal Correspondence

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_correspondence` |
| نسخه | `19.0.1.1.0` |
| عنوان | CAS Internal Correspondence |
| خلاصه | Secure, auditable internal organizational correspondence |
| دسته | Productivity |
| نوع برنامه | Application |
| نصب خودکار | — |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `cas_core`, `mail`, `hr` |
| Python خارجی | — |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 6 | مدل و منطق دامنه |
| `wizard/` | 5 | عملیات موقت/مرحله‌ای |
| `views/` | 4 | نما، action و menu |
| `security/` | 2 | گروه، ACL و record rule |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `cas.correspondence.audit` — کلاس `CasCorrespondenceAudit`

- منبع: `models/audit.py:7`
- inherits: —
- توضیح فنی: CAS Correspondence Immutable Audit

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `letter_id` | `Many2one` | — | `cas.correspondence.letter` | — | True | — | — | — |
| `delegation_id` | `Many2one` | — | `cas.correspondence.secretariat.delegation` | — | True | — | — | — |
| `company_id` | `Many2one` | — | `res.company` | True | True | — | — | — |
| `event_type` | `Selection` | — | — | True | True | — | — | — |
| `actor_user_id` | `Many2one` | — | `res.users` | True | True | — | — | — |
| `event_at` | `Datetime` | — | — | True | True | — | `fields.Datetime.now` | — |
| `reason` | `Text` | — | — | — | True | — | — | — |
| `payload` | `Json` | — | — | — | True | — | — | — |
| `visible_to_current_user` | `Boolean` | — | — | — | — | — | — | _compute_visible_to_current_user / — |

**مقادیر Selection/State**

- `event_type`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_compute_visible_to_current_user()` | `api.depends_context('uid', 'allowed_company_ids')` | 57 |
| `_search_visible_to_current_user()` | — | 68 |
| `create()` | `api.model_create_multi` | 82 |
| `write()` | — | 90 |
| `unlink()` | — | 93 |

### `افزونه مدل` — کلاس `ResCompany`

- منبع: `models/company.py:5`
- inherits: `res.company`
- توضیح فنی: —

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `cas_correspondence_ceo_user_id` | `Many2one` | مدیرعامل مکاتبات | `res.users` | — | — | — | — | — |
| `cas_correspondence_sequence_id` | `Many2one` | شماره‌گذار مکاتبات داخلی | `ir.sequence` | — | True | — | — | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_check_correspondence_ceo()` | `api.constrains('cas_correspondence_ceo_user_id')` | 23 |
| `_cas_correspondence_sequence()` | — | 31 |

Constraints سمت سرور: `_check_correspondence_ceo()`

### `cas.correspondence.secretariat.delegation` — کلاس `CasCorrespondenceSecretariatDelegation`

- منبع: `models/delegation.py:7`
- inherits: `mail.thread`
- توضیح فنی: CAS Secretariat Delegation

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `company_id` | `Many2one` | — | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `delegator_user_id` | `Many2one` | — | `res.users` | True | True | — | — | — |
| `delegate_user_id` | `Many2one` | — | `res.users` | True | — | True | — | — |
| `date_from` | `Date` | — | — | True | — | True | `fields.Date.context_today` | — |
| `date_to` | `Date` | — | — | — | — | True | — | — |
| `reason` | `Text` | — | — | True | — | True | — | — |
| `active` | `Boolean` | — | — | — | True | True | `True` | — |
| `revoked_at` | `Datetime` | — | — | — | True | — | — | — |
| `revoked_by_id` | `Many2one` | — | `res.users` | — | True | — | — | — |
| `revocation_reason` | `Text` | — | — | — | True | — | — | — |
| `audit_ids` | `One2many` | تاریخچه رسمی | `cas.correspondence.audit` | — | — | — | — | — |
| `visible_to_current_user` | `Boolean` | — | — | — | — | — | — | _compute_visible_to_current_user / — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_require_ceo()` | `api.model` | 50 |
| `_user_can_read()` | — | 57 |
| `_is_valid()` | — | 67 |
| `_compute_visible_to_current_user()` | `api.depends_context('uid', 'allowed_company_ids')` | 80 |
| `_search_visible_to_current_user()` | — | 84 |
| `_check_contract()` | `api.constrains('date_from', 'date_to', 'delegate_user_id', 'company_id')` | 104 |
| `_check_overlap()` | `api.constrains('delegate_user_id', 'company_id', 'date_from', 'date_to', 'active')` | 115 |
| `create()` | `api.model_create_multi` | 133 |
| `write()` | — | 153 |
| `unlink()` | — | 158 |
| `_audit()` | — | 161 |
| `action_revoke()` | — | 183 |
| `action_open_revoke_wizard()` | — | 201 |

Constraints سمت سرور: `_check_contract()`, `_check_overlap()`

### `cas.correspondence.letter` — کلاس `CasCorrespondenceLetter`

- منبع: `models/letter.py:28`
- inherits: `mail.thread`، `mail.activity.mixin`
- توضیح فنی: CAS Internal Correspondence Letter

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `number` | `Char` | شماره ثبت | — | — | True | — | — | — |
| `subject` | `Char` | موضوع | — | True | — | True | — | — |
| `body` | `Html` | متن نامه | — | True | — | — | — | — |
| `company_id` | `Many2one` | — | `res.company` | True | — | — | `lambda self: self.env.company` | — |
| `sender_user_id` | `Many2one` | فرستنده | `res.users` | True | True | — | `lambda self: self.env.user` | — |
| `sender_employee_id` | `Many2one` | شخصیت سازمانی فرستنده | `hr.employee` | True | True | — | — | — |
| `sender_department_id` | `Many2one` | واحد فرستنده | `hr.department` | True | True | — | — | — |
| `confidentiality` | `Selection` | CONFIDENTIALITY | — | True | — | True | `normal` | — |
| `priority` | `Selection` | PRIORITY | — | True | — | True | `normal` | — |
| `default_deadline` | `Datetime` | مهلت پیش‌فرض | — | — | — | True | — | — |
| `state` | `Selection` | وضعیت | — | True | True | True | `draft` | — |
| `sent_at` | `Datetime` | زمان ارسال | — | — | True | — | — | — |
| `delivered_at` | `Datetime` | زمان تحویل | — | — | True | — | — | — |
| `first_viewed_at` | `Datetime` | زمان نخستین مشاهده | — | — | True | — | — | — |
| `replied_at` | `Datetime` | زمان پاسخ | — | — | True | — | — | — |
| `closed_at` | `Datetime` | زمان اختتام | — | — | True | — | — | — |
| `signed_by_user_id` | `Many2one` | امضاکننده | `res.users` | — | True | — | — | — |
| `signature_name` | `Char` | نام امضاکننده | — | — | True | — | — | — |
| `signature_job_title` | `Char` | سمت امضاکننده | — | — | True | — | — | — |
| `signed_at` | `Datetime` | زمان امضا | — | — | True | — | — | — |
| `recipient_ids` | `One2many` | گیرندگان و رونوشت‌ها | `cas.correspondence.recipient` | — | — | — | — | — |
| `referral_ids` | `One2many` | ارجاع‌ها | `cas.correspondence.referral` | — | — | — | — | — |
| `receipt_ids` | `One2many` | رسیدهای مشاهده | `cas.correspondence.view.receipt` | — | — | — | — | — |
| `audit_ids` | `One2many` | تاریخچه رسمی | `cas.correspondence.audit` | — | — | — | — | — |
| `outgoing_relation_ids` | `One2many` | روابط نامه | `cas.correspondence.relation` | — | — | — | — | — |
| `incoming_relation_ids` | `One2many` | روابط ورودی | `cas.correspondence.relation` | — | — | — | — | — |
| `reply_to_id` | `Many2one` | پاسخ به نامه | `cas.correspondence.letter` | — | — | — | — | — |
| `thread_root_id` | `Many2one` | ریشه زنجیره | `cas.correspondence.letter` | — | True | — | — | — |
| `correction_of_id` | `Many2one` | اصلاح‌کننده نامه | `cas.correspondence.letter` | — | — | — | — | — |
| `replacement_letter_id` | `Many2one` | نامه جایگزین | `cas.correspondence.letter` | — | True | — | — | — |
| `correction_reason` | `Text` | دلیل اصلاح | — | — | — | — | — | — |
| `attachment_ids` | `Many2many` | پیوست‌ها | `ir.attachment` | — | — | — | — | — |
| `authorized_user_ids` | `Many2many` | کاربران مجاز مستقیم | `res.users` | — | True | — | — | — |
| `scope_department_ids` | `Many2many` | واحدهای درگیر | `hr.department` | — | True | — | — | — |
| `has_secretariat_access` | `Boolean` | — | — | — | — | — | — | _compute_has_secretariat_access / — |
| `in_manager_scope` | `Boolean` | — | — | — | — | — | — | _compute_in_manager_scope / — |

**مقادیر Selection/State**

- `confidentiality`: —
- `priority`: —
- `state`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_employee_for_user()` | `api.model` | 211 |
| `create()` | `api.model_create_multi` | 226 |
| `write()` | — | 271 |
| `unlink()` | — | 305 |
| `copy()` | — | 310 |
| `_check_attachment_company()` | `api.constrains('company_id', 'attachment_ids')` | 325 |
| `_audit()` | — | 334 |
| `_active_internal_user()` | `api.model` | 353 |
| `_manager_users_for_employee()` | — | 357 |
| `_sync_access_index()` | — | 375 |
| `_secretariat_company_ids()` | `api.model` | 407 |
| `_compute_has_secretariat_access()` | `api.depends_context('uid', 'allowed_company_ids')` | 430 |
| `_search_has_secretariat_access()` | — | 435 |
| `_manager_scope_domain()` | `api.model` | 441 |
| `_compute_in_manager_scope()` | `api.depends_context('uid', 'allowed_company_ids')` | 462 |
| `_search_in_manager_scope()` | — | 467 |
| `_check_corrective_access()` | — | 472 |
| `action_send()` | — | 483 |
| `_register_formal_reply()` | — | 548 |
| `_refresh_state()` | — | 571 |
| `action_close()` | — | 594 |
| `action_create_reply()` | — | 615 |
| `action_create_correction()` | — | 633 |
| `action_open_referral_wizard()` | — | 651 |
| `_cas_action_descriptors()` | — | 665 |
| `_cas_action_check_access()` | — | 676 |

Constraints سمت سرور: `_check_attachment_company()`

### `cas.correspondence.relation` — کلاس `CasCorrespondenceRelation`

- منبع: `models/letter.py:688`
- inherits: —
- توضیح فنی: CAS Correspondence Letter Relation

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `letter_id` | `Many2one` | — | `cas.correspondence.letter` | True | — | — | — | — |
| `related_letter_id` | `Many2one` | — | `cas.correspondence.letter` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | True | — | — | — / True |
| `relation_type` | `Selection` | — | — | True | — | — | — | — |
| `created_by_id` | `Many2one` | — | `res.users` | True | True | — | `lambda self: self.env.user` | — |
| `visible_to_current_user` | `Boolean` | — | — | — | — | — | — | _compute_visible_to_current_user / — |

**مقادیر Selection/State**

- `relation_type`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_compute_visible_to_current_user()` | `api.depends_context('uid', 'allowed_company_ids')` | 729 |
| `_search_visible_to_current_user()` | — | 736 |
| `create()` | `api.model_create_multi` | 746 |
| `write()` | — | 760 |
| `unlink()` | — | 763 |

### `cas.correspondence.visibility.mixin` — کلاس `CasCorrespondenceVisibilityMixin`

- منبع: `models/recipient.py:24`
- inherits: —
- توضیح فنی: CAS Correspondence Child Visibility

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `visible_to_current_user` | `Boolean` | — | — | — | — | — | — | _compute_visible_to_current_user / — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_compute_visible_to_current_user()` | `api.depends_context('uid', 'allowed_company_ids')` | 34 |
| `_search_visible_to_current_user()` | — | 39 |
| `_validate_target_user()` | — | 45 |
| `_resolve_target()` | — | 51 |
| `_create_activity()` | — | 67 |
| `_complete_activity()` | — | 83 |
| `_require_responsible()` | — | 88 |
| `_cas_action_descriptor()` | — | 94 |
| `_sync_action_hub()` | — | 119 |

### `cas.correspondence.recipient` — کلاس `CasCorrespondenceRecipient`

- منبع: `models/recipient.py:136`
- inherits: `cas.correspondence.visibility.mixin`
- توضیح فنی: CAS Correspondence Recipient

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `letter_id` | `Many2one` | — | `cas.correspondence.letter` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | True | — | — | — / True |
| `role` | `Selection` | — | — | True | — | — | `to` | — |
| `target_kind` | `Selection` | — | — | True | — | — | `user` | — |
| `recipient_user_id` | `Many2one` | مخاطب | `res.users` | — | — | — | — | — |
| `department_id` | `Many2one` | واحد مخاطب | `hr.department` | — | — | — | — | — |
| `responsible_user_id` | `Many2one` | مسئول نهایی | `res.users` | — | True | — | — | — |
| `expectation` | `Selection` | EXPECTATION | — | True | — | — | `information` | — |
| `priority` | `Selection` | PRIORITY | — | True | — | — | `normal` | — |
| `deadline` | `Datetime` | — | — | — | — | — | — | — |
| `note` | `Text` | توضیح مخاطب | — | — | — | — | — | — |
| `status` | `Selection` | ACTION_STATUS | — | True | True | — | `pending` | — |
| `delivered_at` | `Datetime` | — | — | — | True | — | — | — |
| `viewed_at` | `Datetime` | — | — | — | True | — | — | — |
| `started_at` | `Datetime` | — | — | — | True | — | — | — |
| `completed_at` | `Datetime` | — | — | — | True | — | — | — |
| `action_result` | `Text` | — | — | — | True | — | — | — |
| `reply_letter_id` | `Many2one` | — | `cas.correspondence.letter` | — | True | — | — | — |
| `activity_id` | `Many2one` | — | `mail.activity` | — | True | — | — | — |

**مقادیر Selection/State**

- `role`: —
- `target_kind`: —
- `expectation`: —
- `priority`: —
- `status`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_check_recipient_contract()` | `api.constrains('target_kind', 'recipient_user_id', 'department_id', 'role', 'letter_id')` | 197 |
| `create()` | `api.model_create_multi` | 215 |
| `write()` | — | 234 |
| `unlink()` | — | 258 |
| `_prepare_for_delivery()` | — | 266 |
| `_deliver()` | — | 275 |
| `_activity_summary()` | — | 283 |
| `action_mark_viewed()` | — | 291 |
| `action_start()` | — | 323 |
| `action_complete()` | — | 335 |
| `action_open_complete_wizard()` | — | 355 |
| `_mark_replied()` | — | 370 |

Constraints سمت سرور: `_check_recipient_contract()`

### `cas.correspondence.referral` — کلاس `CasCorrespondenceReferral`

- منبع: `models/recipient.py:383`
- inherits: `cas.correspondence.visibility.mixin`
- توضیح فنی: CAS Correspondence Referral

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `letter_id` | `Many2one` | — | `cas.correspondence.letter` | True | — | — | — | — |
| `company_id` | `Many2one` | — | — | — | True | — | — | — / True |
| `referrer_user_id` | `Many2one` | — | `res.users` | True | True | — | — | — |
| `target_kind` | `Selection` | — | — | True | — | — | `user` | — |
| `recipient_user_id` | `Many2one` | مخاطب | `res.users` | — | — | — | — | — |
| `department_id` | `Many2one` | واحد مخاطب | `hr.department` | — | — | — | — | — |
| `responsible_user_id` | `Many2one` | مسئول نهایی | `res.users` | True | True | — | — | — |
| `expectation` | `Selection` | EXPECTATION | — | True | — | — | `action` | — |
| `priority` | `Selection` | PRIORITY | — | True | — | — | `normal` | — |
| `deadline` | `Datetime` | — | — | — | — | — | — | — |
| `note` | `Text` | — | — | True | — | — | — | — |
| `status` | `Selection` | ACTION_STATUS | — | True | True | — | `delivered` | — |
| `delivered_at` | `Datetime` | — | — | True | True | — | — | — |
| `viewed_at` | `Datetime` | — | — | — | True | — | — | — |
| `started_at` | `Datetime` | — | — | — | True | — | — | — |
| `completed_at` | `Datetime` | — | — | — | True | — | — | — |
| `action_result` | `Text` | — | — | — | True | — | — | — |
| `reply_letter_id` | `Many2one` | — | `cas.correspondence.letter` | — | True | — | — | — |
| `activity_id` | `Many2one` | — | `mail.activity` | — | True | — | — | — |

**مقادیر Selection/State**

- `target_kind`: —
- `expectation`: —
- `priority`: —
- `status`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 430 |
| `write()` | — | 443 |
| `unlink()` | — | 450 |
| `_activity_summary()` | — | 453 |
| `action_mark_viewed()` | — | 461 |
| `action_start()` | — | 487 |
| `action_complete()` | — | 499 |
| `action_open_complete_wizard()` | — | 515 |
| `_mark_replied()` | — | 530 |

### `cas.correspondence.view.receipt` — کلاس `CasCorrespondenceViewReceipt`

- منبع: `models/recipient.py:543`
- inherits: `cas.correspondence.visibility.mixin`
- توضیح فنی: CAS Correspondence Immutable View Receipt

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `letter_id` | `Many2one` | — | `cas.correspondence.letter` | True | True | — | — | — |
| `company_id` | `Many2one` | — | — | — | True | — | — | — / True |
| `recipient_id` | `Many2one` | — | `cas.correspondence.recipient` | — | True | — | — | — |
| `referral_id` | `Many2one` | — | `cas.correspondence.referral` | — | True | — | — | — |
| `viewer_user_id` | `Many2one` | — | `res.users` | True | True | — | — | — |
| `viewed_at` | `Datetime` | — | — | True | True | — | `fields.Datetime.now` | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `create()` | `api.model_create_multi` | 576 |
| `write()` | — | 584 |
| `unlink()` | — | 587 |

### `cas.correspondence.complete.wizard` — کلاس `CasCorrespondenceCompleteWizard`

- منبع: `wizard/action_wizard.py:5`
- inherits: —
- توضیح فنی: Complete CAS Correspondence Action

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `source_model` | `Selection` | — | — | True | True | — | — | — |
| `source_id` | `Integer` | — | — | True | True | — | — | — |
| `result` | `Text` | نتیجه اقدام | — | True | — | — | — | — |

**مقادیر Selection/State**

- `source_model`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `action_confirm()` | — | 20 |

### `cas.correspondence.delegation.revoke.wizard` — کلاس `CasCorrespondenceDelegationRevokeWizard`

- منبع: `wizard/action_wizard.py:34`
- inherits: —
- توضیح فنی: Revoke CAS Secretariat Delegation

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `delegation_id` | `Many2one` | — | `cas.correspondence.secretariat.delegation` | True | True | — | — | — |
| `reason` | `Text` | دلیل لغو | — | True | — | — | — | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `action_confirm()` | — | 46 |

### `cas.correspondence.referral.wizard` — کلاس `CasCorrespondenceReferralWizard`

- منبع: `wizard/referral_wizard.py:8`
- inherits: —
- توضیح فنی: Refer CAS Correspondence Letter

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `letter_id` | `Many2one` | — | `cas.correspondence.letter` | True | True | — | — | — |
| `target_kind` | `Selection` | — | — | True | — | — | `user` | — |
| `recipient_user_id` | `Many2one` | مخاطب | `res.users` | — | — | — | — | — |
| `department_id` | `Many2one` | واحد مخاطب | `hr.department` | — | — | — | — | — |
| `expectation` | `Selection` | EXPECTATION | — | True | — | — | `action` | — |
| `priority` | `Selection` | PRIORITY | — | True | — | — | `normal` | — |
| `deadline` | `Datetime` | — | — | — | — | — | — | — |
| `note` | `Text` | توضیح ارجاع | — | True | — | — | — | — |

**مقادیر Selection/State**

- `target_kind`: —
- `expectation`: —
- `priority`: —

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `action_confirm()` | — | 27 |

## گروه‌های امنیتی

| XML ID | عنوان | implied groups | فایل |
|---|---|---|---|
| `group_cas_correspondence_user` | کاربر مکاتبات سازمانی | — | `security/cas_correspondence_security.xml` |
| `group_cas_correspondence_manager` | مدیر مکاتبات سازمانی | [(4, ref('group_cas_correspondence_user'))] | `security/cas_correspondence_security.xml` |
| `base.group_system` | — | [(4, ref('cas_correspondence.group_cas_correspondence_manager'))] | `security/cas_correspondence_security.xml` |

## ماتریس ACL

| ACL | مدل | گروه | Read | Write | Create | Unlink |
|---|---|---|---:|---:|---:|---:|
| `access_correspondence_letter_user` | `model_cas_correspondence_letter` | `group_cas_correspondence_user` | 1 | 1 | 1 | 0 |
| `access_correspondence_letter_manager` | `model_cas_correspondence_letter` | `group_cas_correspondence_manager` | 1 | 1 | 1 | 0 |
| `access_correspondence_recipient_user` | `model_cas_correspondence_recipient` | `group_cas_correspondence_user` | 1 | 1 | 1 | 1 |
| `access_correspondence_recipient_manager` | `model_cas_correspondence_recipient` | `group_cas_correspondence_manager` | 1 | 1 | 1 | 1 |
| `access_correspondence_referral_user` | `model_cas_correspondence_referral` | `group_cas_correspondence_user` | 1 | 1 | 1 | 0 |
| `access_correspondence_referral_manager` | `model_cas_correspondence_referral` | `group_cas_correspondence_manager` | 1 | 1 | 1 | 0 |
| `access_correspondence_receipt_user` | `model_cas_correspondence_view_receipt` | `group_cas_correspondence_user` | 1 | 0 | 1 | 0 |
| `access_correspondence_receipt_manager` | `model_cas_correspondence_view_receipt` | `group_cas_correspondence_manager` | 1 | 0 | 1 | 0 |
| `access_correspondence_relation_user` | `model_cas_correspondence_relation` | `group_cas_correspondence_user` | 1 | 0 | 1 | 0 |
| `access_correspondence_relation_manager` | `model_cas_correspondence_relation` | `group_cas_correspondence_manager` | 1 | 0 | 1 | 0 |
| `access_correspondence_delegation_user` | `model_cas_correspondence_secretariat_delegation` | `group_cas_correspondence_user` | 1 | 1 | 1 | 0 |
| `access_correspondence_delegation_manager` | `model_cas_correspondence_secretariat_delegation` | `group_cas_correspondence_manager` | 1 | 1 | 1 | 0 |
| `access_correspondence_audit_user` | `model_cas_correspondence_audit` | `group_cas_correspondence_user` | 1 | 0 | 0 | 0 |
| `access_correspondence_audit_manager` | `model_cas_correspondence_audit` | `group_cas_correspondence_manager` | 1 | 0 | 0 | 0 |
| `access_correspondence_referral_wizard` | `model_cas_correspondence_referral_wizard` | `group_cas_correspondence_user` | 1 | 1 | 1 | 1 |
| `access_correspondence_complete_wizard` | `model_cas_correspondence_complete_wizard` | `group_cas_correspondence_user` | 1 | 1 | 1 | 1 |
| `access_correspondence_revoke_wizard` | `model_cas_correspondence_delegation_revoke_wizard` | `group_cas_correspondence_user` | 1 | 1 | 1 | 1 |

## Record Ruleها

| XML ID | عنوان | مدل | گروه‌ها | Domain |
|---|---|---|---|---|
| `rule_correspondence_letter_user` | نامه: ذی‌نفع، مدیر ساختاری یا دبیرخانه | `model_cas_correspondence_letter` | [(4, ref('group_cas_correspondence_user'))] | `['&', ('company_id', 'in', company_ids), '\|', '\|', ('authorized_user_ids', 'in', user.id), ('in_manager_scope', '=', True), ('has_secretariat_access', '=', True)]` |
| `rule_correspondence_letter_manager` | نامه: مدیر سامانه در شرکت‌های مجاز | `model_cas_correspondence_letter` | [(4, ref('group_cas_correspondence_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_correspondence_recipient_user` | مخاطب: نامه قابل مشاهده | `model_cas_correspondence_recipient` | [(4, ref('group_cas_correspondence_user'))] | `[('visible_to_current_user', '=', True)]` |
| `rule_correspondence_referral_user` | ارجاع: نامه قابل مشاهده | `model_cas_correspondence_referral` | [(4, ref('group_cas_correspondence_user'))] | `[('visible_to_current_user', '=', True)]` |
| `rule_correspondence_receipt_user` | رسید مشاهده: نامه قابل مشاهده | `model_cas_correspondence_view_receipt` | [(4, ref('group_cas_correspondence_user'))] | `[('visible_to_current_user', '=', True)]` |
| `rule_correspondence_relation_user` | رابطه: هر دو نامه قابل مشاهده | `model_cas_correspondence_relation` | [(4, ref('group_cas_correspondence_user'))] | `[('visible_to_current_user', '=', True)]` |
| `rule_correspondence_audit_user` | تاریخچه: رکورد منبع قابل مشاهده | `model_cas_correspondence_audit` | [(4, ref('group_cas_correspondence_user'))] | `[('visible_to_current_user', '=', True)]` |
| `rule_correspondence_delegation_user` | تفویض دبیرخانه: ذی‌نفع یا مدیرعامل | `model_cas_correspondence_secretariat_delegation` | [(4, ref('group_cas_correspondence_user'))] | `['&', ('company_id', 'in', company_ids), ('visible_to_current_user', '=', True)]` |
| `rule_correspondence_child_manager` | مخاطب: مدیر سامانه | `model_cas_correspondence_recipient` | [(4, ref('group_cas_correspondence_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_correspondence_referral_manager` | ارجاع: مدیر سامانه | `model_cas_correspondence_referral` | [(4, ref('group_cas_correspondence_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_correspondence_receipt_manager` | رسید: مدیر سامانه | `model_cas_correspondence_view_receipt` | [(4, ref('group_cas_correspondence_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_correspondence_relation_manager` | رابطه: مدیر سامانه | `model_cas_correspondence_relation` | [(4, ref('group_cas_correspondence_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_correspondence_audit_manager` | تاریخچه: مدیر سامانه | `model_cas_correspondence_audit` | [(4, ref('group_cas_correspondence_manager'))] | `[('company_id', 'in', company_ids)]` |
| `rule_correspondence_delegation_manager` | تفویض دبیرخانه: مدیر سامانه | `model_cas_correspondence_secretariat_delegation` | [(4, ref('group_cas_correspondence_manager'))] | `[('company_id', 'in', company_ids)]` |

## منوها

| XML ID | عنوان | والد | action | گروه |
|---|---|---|---|---|
| `menu_correspondence_root` | مکاتبات سازمانی | — | — | `group_cas_correspondence_user` |
| `menu_correspondence_letters` | نامه‌های داخلی | `menu_correspondence_root` | `action_correspondence_letters` | — |
| `menu_correspondence_drafts` | پیش‌نویس‌های من | `menu_correspondence_root` | `action_correspondence_drafts` | — |
| `menu_correspondence_secretariat` | دبیرخانه | `menu_correspondence_root` | `action_correspondence_secretariat` | — |
| `menu_correspondence_config` | پیکربندی | `menu_correspondence_root` | — | `group_cas_correspondence_manager` |
| `menu_secretariat_delegations` | تفویض‌های دبیرخانه | `menu_correspondence_config` | `action_secretariat_delegations` | — |

## Actionها

| XML ID | نوع | عنوان | مدل/تگ | view mode | فایل |
|---|---|---|---|---|---|
| `action_correspondence_letters` | `ir.actions.act_window` | نامه‌های داخلی | `cas.correspondence.letter` | `list,form` | `views/correspondence_letter_views.xml` |
| `action_correspondence_drafts` | `ir.actions.act_window` | پیش‌نویس‌های من | `cas.correspondence.letter` | `list,form` | `views/correspondence_letter_views.xml` |
| `action_correspondence_secretariat` | `ir.actions.act_window` | دبیرخانه | `cas.correspondence.letter` | `list,form` | `views/correspondence_letter_views.xml` |
| `action_secretariat_delegations` | `ir.actions.act_window` | تفویض‌های دبیرخانه | `cas.correspondence.secretariat.delegation` | `list,form` | `views/secretariat_delegation_views.xml` |

## Cron و Sequence

Cron یا sequence اختصاصی در XML ندارد.

## Assetهای رابط کاربری

Asset اختصاصی ندارد.

## داده‌های بارگذاری‌شده از manifest

- `security/cas_correspondence_security.xml`
- `security/ir.model.access.csv`
- `views/res_company_views.xml`
- `views/correspondence_letter_views.xml`
- `views/secretariat_delegation_views.xml`
- `wizard/referral_wizard_views.xml`
- `wizard/action_wizard_views.xml`
- `views/correspondence_menus.xml`

## آزمون‌های موجود

- `tests/test_correspondence.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
