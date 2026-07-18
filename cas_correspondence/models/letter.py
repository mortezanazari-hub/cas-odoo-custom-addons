from __future__ import annotations

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


CONFIDENTIALITY = [
    ("normal", "عادی"),
    ("confidential", "محرمانه"),
    ("highly_confidential", "خیلی محرمانه"),
]

PRIORITY = [("normal", "عادی"), ("urgent", "فوری"), ("immediate", "آنی")]


def _search_wants_true(operator, value):
    if operator in ("=", "=="):
        return bool(value)
    if operator == "!=":
        return not bool(value)
    if operator == "in":
        return True in value
    if operator == "not in":
        return True not in value
    raise NotImplementedError(f"Unsupported boolean operator: {operator}")


class CasCorrespondenceLetter(models.Model):
    _name = "cas.correspondence.letter"
    _description = "CAS Internal Correspondence Letter"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sent_at desc, id desc"
    _rec_name = "subject"

    number = fields.Char(string="شماره ثبت", readonly=True, copy=False, index=True)
    subject = fields.Char(string="موضوع", required=True, tracking=True, index=True)
    body = fields.Html(string="متن نامه", required=True, sanitize=True)
    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
        ondelete="restrict",
        index=True,
    )
    sender_user_id = fields.Many2one(
        "res.users",
        string="فرستنده",
        required=True,
        default=lambda self: self.env.user,
        ondelete="restrict",
        readonly=True,
        index=True,
    )
    sender_employee_id = fields.Many2one(
        "hr.employee",
        string="شخصیت سازمانی فرستنده",
        required=True,
        ondelete="restrict",
        readonly=True,
        index=True,
    )
    sender_department_id = fields.Many2one(
        "hr.department",
        string="واحد فرستنده",
        required=True,
        ondelete="restrict",
        readonly=True,
        index=True,
    )
    confidentiality = fields.Selection(
        CONFIDENTIALITY,
        string="محرمانگی",
        required=True,
        default="normal",
        tracking=True,
        index=True,
    )
    priority = fields.Selection(
        PRIORITY,
        string="اولویت",
        required=True,
        default="normal",
        tracking=True,
        index=True,
    )
    default_deadline = fields.Datetime(string="مهلت پیش‌فرض", tracking=True, index=True)
    state = fields.Selection(
        [
            ("draft", "پیش‌نویس"),
            ("sent", "ارسال‌شده"),
            ("delivered", "تحویل‌شده"),
            ("viewed", "مشاهده‌شده"),
            ("in_progress", "در حال اقدام"),
            ("replied", "پاسخ‌داده‌شده"),
            ("closed", "مختومه"),
            ("cancelled", "باطل‌شده با فرایند اصلاحی"),
        ],
        string="وضعیت",
        required=True,
        default="draft",
        readonly=True,
        tracking=True,
        index=True,
    )
    sent_at = fields.Datetime(string="زمان ارسال", readonly=True, index=True)
    delivered_at = fields.Datetime(string="زمان تحویل", readonly=True, index=True)
    first_viewed_at = fields.Datetime(string="زمان نخستین مشاهده", readonly=True, index=True)
    replied_at = fields.Datetime(string="زمان پاسخ", readonly=True, index=True)
    closed_at = fields.Datetime(string="زمان اختتام", readonly=True, index=True)
    signed_by_user_id = fields.Many2one(
        "res.users", string="امضاکننده", readonly=True, ondelete="restrict"
    )
    signature_name = fields.Char(string="نام امضاکننده", readonly=True)
    signature_job_title = fields.Char(string="سمت امضاکننده", readonly=True)
    signed_at = fields.Datetime(string="زمان امضا", readonly=True)
    recipient_ids = fields.One2many(
        "cas.correspondence.recipient", "letter_id", string="گیرندگان و رونوشت‌ها", copy=True
    )
    referral_ids = fields.One2many(
        "cas.correspondence.referral", "letter_id", string="ارجاع‌ها", copy=False
    )
    receipt_ids = fields.One2many(
        "cas.correspondence.view.receipt", "letter_id", string="رسیدهای مشاهده", copy=False
    )
    audit_ids = fields.One2many(
        "cas.correspondence.audit", "letter_id", string="تاریخچه رسمی", copy=False
    )
    outgoing_relation_ids = fields.One2many(
        "cas.correspondence.relation", "letter_id", string="روابط نامه", copy=False
    )
    incoming_relation_ids = fields.One2many(
        "cas.correspondence.relation", "related_letter_id", string="روابط ورودی", copy=False
    )
    reply_to_id = fields.Many2one(
        "cas.correspondence.letter",
        string="پاسخ به نامه",
        ondelete="restrict",
        copy=False,
        index=True,
    )
    thread_root_id = fields.Many2one(
        "cas.correspondence.letter",
        string="ریشه زنجیره",
        readonly=True,
        copy=False,
        ondelete="restrict",
        index=True,
    )
    correction_of_id = fields.Many2one(
        "cas.correspondence.letter",
        string="اصلاح‌کننده نامه",
        ondelete="restrict",
        copy=False,
        index=True,
    )
    replacement_letter_id = fields.Many2one(
        "cas.correspondence.letter",
        string="نامه جایگزین",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )
    correction_reason = fields.Text(string="دلیل اصلاح", copy=False)
    attachment_ids = fields.Many2many(
        "ir.attachment",
        "cas_correspondence_letter_attachment_rel",
        "letter_id",
        "attachment_id",
        string="پیوست‌ها",
        copy=True,
    )
    authorized_user_ids = fields.Many2many(
        "res.users",
        "cas_correspondence_letter_authorized_user_rel",
        "letter_id",
        "user_id",
        string="کاربران مجاز مستقیم",
        readonly=True,
        copy=False,
    )
    scope_department_ids = fields.Many2many(
        "hr.department",
        "cas_correspondence_letter_scope_department_rel",
        "letter_id",
        "department_id",
        string="واحدهای درگیر",
        readonly=True,
        copy=False,
    )
    has_secretariat_access = fields.Boolean(
        compute="_compute_has_secretariat_access",
        search="_search_has_secretariat_access",
    )
    in_manager_scope = fields.Boolean(
        compute="_compute_in_manager_scope", search="_search_in_manager_scope"
    )

    _number_company_unique = models.Constraint(
        "UNIQUE(number, company_id)", "شماره نامه باید در هر شرکت یکتا باشد."
    )
    _not_self_reply = models.Constraint(
        "CHECK(reply_to_id IS NULL OR reply_to_id != id)",
        "نامه نمی‌تواند پاسخ به خودش باشد.",
    )
    _not_self_correction = models.Constraint(
        "CHECK(correction_of_id IS NULL OR correction_of_id != id)",
        "نامه نمی‌تواند اصلاح‌کننده خودش باشد.",
    )

    @api.model
    def _employee_for_user(self, user, company):
        employees = user.sudo().employee_ids.with_context(active_test=False).filtered(
            lambda employee: employee.active
            and employee.company_id == company
            and employee.department_id
        )
        if len(employees) != 1:
            raise ValidationError(
                _(
                    "کاربر فرستنده باید دقیقاً یک پرونده کارمند فعال و دارای واحد در شرکت نامه داشته باشد."
                )
            )
        return employees

    @api.model_create_multi
    def create(self, vals_list):
        records = self.browse()
        for original in vals_list:
            vals = dict(original)
            company = self.env["res.company"].browse(
                vals.get("company_id") or self.env.company.id
            ).exists()
            sender = self.env["res.users"].browse(
                vals.get("sender_user_id") or self.env.user.id
            ).with_context(active_test=False).exists()
            if sender != self.env.user and not self.env.is_superuser():
                raise AccessError(_("ایجاد پیش‌نویس به نام کاربر دیگر مجاز نیست."))
            if not sender or not sender.active or sender.share or company not in sender.company_ids:
                raise ValidationError(_("فرستنده باید کاربر داخلی و فعال همان شرکت باشد."))
            employee = self._employee_for_user(sender, company)
            vals.update(
                {
                    "company_id": company.id,
                    "sender_user_id": sender.id,
                    "sender_employee_id": employee.id,
                    "sender_department_id": employee.department_id.id,
                    "number": False,
                    "state": "draft",
                    "thread_root_id": False,
                }
            )
            reply_to = self.browse(vals.get("reply_to_id")).exists()
            correction_of = self.browse(vals.get("correction_of_id")).exists()
            if reply_to and reply_to.company_id != company:
                raise ValidationError(_("نامه پاسخ و نامه مرجع باید متعلق به یک شرکت باشند."))
            if correction_of:
                correction_of._check_corrective_access()
                if correction_of.company_id != company or correction_of.state in ("draft", "cancelled"):
                    raise ValidationError(_("نامه مرجع اصلاح معتبر نیست."))
                if not str(vals.get("correction_reason") or "").strip():
                    raise ValidationError(_("برای نامه اصلاحی درج دلیل الزامی است."))
            record = super(CasCorrespondenceLetter, self).create(vals)
            record.with_context(cas_correspondence_engine=True).write(
                {"thread_root_id": (reply_to.thread_root_id or reply_to or record).id}
            )
            record._sync_access_index()
            record._audit("created", payload={"subject": record.subject})
            records |= record
        return records

    def write(self, vals):
        if not self.env.context.get("cas_correspondence_engine"):
            protected = {
                "number",
                "company_id",
                "sender_user_id",
                "sender_employee_id",
                "sender_department_id",
                "state",
                "sent_at",
                "delivered_at",
                "first_viewed_at",
                "replied_at",
                "closed_at",
                "signed_by_user_id",
                "signature_name",
                "signature_job_title",
                "signed_at",
                "thread_root_id",
                "replacement_letter_id",
                "authorized_user_ids",
                "scope_department_ids",
            }
            if protected.intersection(vals):
                raise ValidationError(_("فیلدهای سیستمی نامه قابل ویرایش مستقیم نیستند."))
            if any(letter.state != "draft" for letter in self):
                raise ValidationError(_("نامه ارسال‌شده قابل ویرایش مستقیم نیست."))
            if any(letter.sender_user_id != self.env.user for letter in self):
                raise AccessError(_("فقط فرستنده می‌تواند پیش‌نویس خود را ویرایش کند."))
        result = super().write(vals)
        if {"reply_to_id", "correction_of_id"}.intersection(vals):
            self._sync_access_index()
        return result

    def unlink(self):
        raise ValidationError(
            _("نامه و سابقه آن حذف نمی‌شود؛ پیش‌نویس بلااستفاده را بایگانی کنید.")
        )

    def copy(self, default=None):
        self.ensure_one()
        defaults = dict(default or {})
        defaults.update(
            {
                "number": False,
                "state": "draft",
                "reply_to_id": False,
                "correction_of_id": False,
                "correction_reason": False,
            }
        )
        return super().copy(defaults)

    @api.constrains("company_id", "attachment_ids")
    def _check_attachment_company(self):
        for letter in self:
            invalid = letter.attachment_ids.filtered(
                lambda attachment: attachment.company_id
                and attachment.company_id != letter.company_id
            )
            if invalid:
                raise ValidationError(_("پیوست نامه باید متعلق به همان شرکت باشد."))

    def _audit(self, event_type, reason=False, payload=False):
        self.ensure_one()
        return (
            self.env["cas.correspondence.audit"]
            .sudo()
            .with_context(cas_correspondence_audit_engine=True)
            .create(
                {
                    "letter_id": self.id,
                    "company_id": self.company_id.id,
                    "event_type": event_type,
                    "actor_user_id": self.env.user.id,
                    "reason": reason,
                    "payload": payload or {},
                }
            )
        )

    @api.model
    def _active_internal_user(self, user, company):
        user = user.with_context(active_test=False)
        return bool(user and user.active and not user.share and company in user.company_ids)

    def _manager_users_for_employee(self, employee):
        users = self.env["res.users"]
        manager = employee.sudo().parent_id
        visited = set()
        while manager and manager.id not in visited:
            visited.add(manager.id)
            if self._active_internal_user(manager.user_id, employee.company_id):
                users |= manager.user_id
            manager = manager.parent_id
        department = employee.sudo().department_id
        visited = set()
        while department and department.id not in visited:
            visited.add(department.id)
            if self._active_internal_user(department.manager_id.user_id, employee.company_id):
                users |= department.manager_id.user_id
            department = department.parent_id
        return users

    def _sync_access_index(self):
        for letter in self:
            users = letter.sender_user_id | letter._manager_users_for_employee(
                letter.sender_employee_id
            )
            departments = letter.sender_department_id
            for recipient in letter.recipient_ids:
                users |= recipient.recipient_user_id | recipient.responsible_user_id
                departments |= recipient.department_id
                employee = recipient.responsible_user_id.sudo().employee_ids.filtered(
                    lambda item: item.active and item.company_id == letter.company_id
                )[:1]
                if employee:
                    users |= letter._manager_users_for_employee(employee)
            for referral in letter.referral_ids:
                users |= (
                    referral.referrer_user_id
                    | referral.recipient_user_id
                    | referral.responsible_user_id
                )
                departments |= referral.department_id
            users = users.filtered(
                lambda user: letter._active_internal_user(user, letter.company_id)
            )
            letter.with_context(cas_correspondence_engine=True).write(
                {
                    "authorized_user_ids": [(6, 0, users.ids)],
                    "scope_department_ids": [(6, 0, departments.ids)],
                }
            )

    @api.model
    def _secretariat_company_ids(self, user=None):
        user = user or self.env.user
        companies = self.env["res.company"].sudo().search(
            [("id", "in", self.env.companies.ids)]
        )
        ceo_companies = companies.filtered(
            lambda company: company.cas_correspondence_ceo_user_id == user
        )
        today = fields.Date.context_today(self)
        delegations = self.env["cas.correspondence.secretariat.delegation"].sudo().search(
            [
                ("company_id", "in", companies.ids),
                ("delegate_user_id", "=", user.id),
                ("active", "=", True),
                ("date_from", "<=", today),
                "|",
                ("date_to", "=", False),
                ("date_to", ">=", today),
            ]
        )
        return ceo_companies | delegations.company_id

    @api.depends_context("uid", "allowed_company_ids")
    def _compute_has_secretariat_access(self):
        companies = self._secretariat_company_ids()
        for letter in self:
            letter.has_secretariat_access = letter.company_id in companies

    def _search_has_secretariat_access(self, operator, value):
        expected = _search_wants_true(operator, value)
        domain = [("company_id", "in", self._secretariat_company_ids().ids)]
        return domain if expected else [("company_id", "not in", self._secretariat_company_ids().ids)]

    @api.model
    def _manager_scope_domain(self, user=None):
        user = user or self.env.user
        employees = user.sudo().employee_ids.with_context(active_test=False).filtered(
            lambda employee: employee.active and employee.company_id in self.env.companies
        )
        managed_departments = self.env["hr.department"].sudo().search(
            [
                ("company_id", "in", self.env.companies.ids),
                ("manager_id", "in", employees.ids),
            ]
        )
        domains = []
        if employees:
            domains.append(("sender_employee_id", "child_of", employees.ids))
        if managed_departments:
            domains.append(("scope_department_ids", "child_of", managed_departments.ids))
        if not domains:
            return [("id", "=", 0)]
        return domains if len(domains) == 1 else ["|", *domains]

    @api.depends_context("uid", "allowed_company_ids")
    def _compute_in_manager_scope(self):
        visible = self.sudo().search(self._manager_scope_domain())
        for letter in self:
            letter.in_manager_scope = letter in visible

    def _search_in_manager_scope(self, operator, value):
        expected = _search_wants_true(operator, value)
        domain = self._manager_scope_domain()
        return domain if expected else ["!", *domain]

    def _check_corrective_access(self):
        self.ensure_one()
        if (
            self.env.is_superuser()
            or self.sender_user_id == self.env.user
            or self.company_id in self._secretariat_company_ids()
            or self.env.user.has_group("cas_correspondence.group_cas_correspondence_manager")
        ):
            return True
        raise AccessError(_("مجوز اصلاح این نامه را ندارید."))

    def action_send(self):
        self.ensure_one()
        self.check_access("write")
        if self.state != "draft" or self.sender_user_id != self.env.user:
            raise AccessError(_("فقط فرستنده می‌تواند پیش‌نویس خود را ارسال کند."))
        if not self.recipient_ids:
            raise ValidationError(_("حداقل یک گیرنده یا رونوشت لازم است."))
        if self.reply_to_id and self.reply_to_id.state in ("draft", "cancelled"):
            raise ValidationError(_("نامه مرجع پاسخ در وضعیت معتبر نیست."))
        if self.correction_of_id:
            self.correction_of_id._check_corrective_access()
        for recipient in self.recipient_ids:
            recipient._prepare_for_delivery()
        now = fields.Datetime.now()
        employee = self.sender_employee_id.sudo()
        job_title = employee.job_title or employee.job_id.name or ""
        sequence = self.company_id._cas_correspondence_sequence()
        number = sequence.next_by_id()
        self.with_context(cas_correspondence_engine=True).write(
            {
                "number": number,
                "state": "sent",
                "sent_at": now,
                "signed_by_user_id": self.env.user.id,
                "signature_name": employee.name,
                "signature_job_title": job_title,
                "signed_at": now,
            }
        )
        self._audit("sent", payload={"number": number})
        self.recipient_ids._deliver(now)
        self.with_context(cas_correspondence_engine=True).write(
            {"state": "delivered", "delivered_at": now}
        )
        self._audit("delivered", payload={"recipient_count": len(self.recipient_ids)})
        self._sync_access_index()
        self.message_post(body=_("نامه داخلی با شماره %s ارسال شد.", number))
        if self.reply_to_id:
            self.reply_to_id._register_formal_reply(self)
            self.env["cas.correspondence.relation"].sudo().with_context(
                cas_correspondence_relation_engine=True
            ).create(
                {
                    "letter_id": self.id,
                    "related_letter_id": self.reply_to_id.id,
                    "relation_type": "reply",
                }
            )
        if self.correction_of_id:
            original = self.correction_of_id
            original.with_context(cas_correspondence_engine=True).write(
                {"state": "cancelled", "replacement_letter_id": self.id}
            )
            self.env["cas.correspondence.relation"].sudo().with_context(
                cas_correspondence_relation_engine=True
            ).create(
                {
                    "letter_id": self.id,
                    "related_letter_id": original.id,
                    "relation_type": "corrects",
                }
            )
            original._audit("corrected", reason=self.correction_reason, payload={"replacement_id": self.id})
        return True

    def _register_formal_reply(self, reply):
        self.ensure_one()
        matching_recipients = self.recipient_ids.filtered(
            lambda line: line.expectation == "reply"
            and line.responsible_user_id == reply.sender_user_id
            and line.status not in ("replied", "cancelled")
        )
        matching_referrals = self.referral_ids.filtered(
            lambda line: line.expectation == "reply"
            and line.responsible_user_id == reply.sender_user_id
            and line.status not in ("replied", "cancelled")
        )
        if not matching_recipients and not matching_referrals:
            raise ValidationError(
                _("فرستنده پاسخ، مخاطب پاسخ‌گوی نامه مرجع نیست.")
            )
        matching_recipients._mark_replied(reply)
        matching_referrals._mark_replied(reply)
        now = fields.Datetime.now()
        self.with_context(cas_correspondence_engine=True).write({"replied_at": now})
        self._audit("replied", payload={"reply_letter_id": reply.id})
        self._refresh_state()

    def _refresh_state(self):
        for letter in self.filtered(lambda item: item.state not in ("draft", "closed", "cancelled")):
            lines = letter.recipient_ids.filtered(lambda item: item.status != "cancelled")
            referrals = letter.referral_ids.filtered(lambda item: item.status != "cancelled")
            all_actions = list(lines) + list(referrals)
            reply_actions = [item for item in all_actions if item.expectation == "reply"]
            new_state = "delivered"
            if reply_actions and all(item.status == "replied" for item in reply_actions) and all(
                item.status in ("completed", "replied") for item in all_actions
            ):
                new_state = "replied"
            elif all_actions and all(
                item.status == "completed" for item in all_actions
            ) and all(item.expectation == "information" for item in all_actions):
                new_state = "viewed"
            elif any(
                item.status in ("viewed", "in_progress", "completed", "replied")
                for item in all_actions
            ):
                new_state = "in_progress"
            if new_state != letter.state:
                letter.with_context(cas_correspondence_engine=True).write({"state": new_state})

    def action_close(self):
        for letter in self:
            letter.check_access("write")
            letter._check_corrective_access()
            if letter.state in ("draft", "closed", "cancelled"):
                raise ValidationError(_("این نامه در وضعیت قابل اختتام نیست."))
            if any(
                line.status not in ("completed", "replied", "cancelled")
                for line in letter.recipient_ids
            ) or any(
                referral.status not in ("completed", "replied", "cancelled")
                for referral in letter.referral_ids
            ):
                raise ValidationError(_("تا تکمیل انتظار همه مخاطبان، نامه مختومه نمی‌شود."))
            now = fields.Datetime.now()
            letter.with_context(cas_correspondence_engine=True).write(
                {"state": "closed", "closed_at": now}
            )
            letter._audit("closed")
        return True

    def action_create_reply(self):
        self.ensure_one()
        self.check_access("read")
        if self.state in ("draft", "cancelled"):
            raise ValidationError(_("برای این نامه امکان ثبت پاسخ رسمی وجود ندارد."))
        return {
            "type": "ir.actions.act_window",
            "name": _("پاسخ رسمی"),
            "res_model": "cas.correspondence.letter",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_reply_to_id": self.id,
                "default_subject": _("پاسخ: %s", self.subject),
                "default_company_id": self.company_id.id,
            },
        }

    def action_create_correction(self):
        self.ensure_one()
        self._check_corrective_access()
        if self.state in ("draft", "cancelled"):
            raise ValidationError(_("این نامه قابل اصلاح رسمی نیست."))
        return {
            "type": "ir.actions.act_window",
            "name": _("نامه اصلاحی"),
            "res_model": "cas.correspondence.letter",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_correction_of_id": self.id,
                "default_subject": _("اصلاحیه: %s", self.subject),
                "default_company_id": self.company_id.id,
            },
        }

    def action_open_referral_wizard(self):
        self.ensure_one()
        self.check_access("read")
        if self.state in ("draft", "cancelled", "closed"):
            raise ValidationError(_("این نامه در وضعیت قابل ارجاع نیست."))
        return {
            "type": "ir.actions.act_window",
            "name": _("ارجاع نامه"),
            "res_model": "cas.correspondence.referral.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_letter_id": self.id},
        }

    def _cas_action_descriptors(self):
        self.ensure_one()
        self.check_access("read")
        descriptors = []
        for sources in (self.recipient_ids, self.referral_ids):
            for source in sources:
                if source.status in ("completed", "replied", "cancelled"):
                    continue
                descriptors.append(source._cas_action_descriptor())
        return descriptors

    def _cas_action_check_access(self, action_key, user=None):
        self.ensure_one()
        user = user or self.env.user
        prefix, _, raw_id = str(action_key).partition(":")
        model = {
            "recipient": "cas.correspondence.recipient",
            "referral": "cas.correspondence.referral",
        }.get(prefix)
        source = self.env[model].browse(int(raw_id)).exists() if model and raw_id.isdigit() else False
        return bool(source and source.letter_id == self and source.responsible_user_id == user)


class CasCorrespondenceRelation(models.Model):
    _name = "cas.correspondence.relation"
    _description = "CAS Correspondence Letter Relation"
    _order = "create_date desc, id desc"

    letter_id = fields.Many2one(
        "cas.correspondence.letter", required=True, ondelete="restrict", index=True
    )
    related_letter_id = fields.Many2one(
        "cas.correspondence.letter", required=True, ondelete="restrict", index=True
    )
    company_id = fields.Many2one(
        related="letter_id.company_id", store=True, readonly=True, index=True
    )
    relation_type = fields.Selection(
        [
            ("reply", "پاسخ"),
            ("related", "مرتبط"),
            ("corrects", "اصلاح‌کننده"),
            ("replaces", "جایگزین"),
        ],
        required=True,
        index=True,
    )
    created_by_id = fields.Many2one(
        "res.users", required=True, default=lambda self: self.env.user, readonly=True
    )
    visible_to_current_user = fields.Boolean(
        compute="_compute_visible_to_current_user",
        search="_search_visible_to_current_user",
    )

    _relation_unique = models.Constraint(
        "UNIQUE(letter_id, related_letter_id, relation_type)",
        "این رابطه قبلاً ثبت شده است.",
    )
    _different_letters = models.Constraint(
        "CHECK(letter_id != related_letter_id)", "دو سوی رابطه باید متفاوت باشند."
    )

    @api.depends_context("uid", "allowed_company_ids")
    def _compute_visible_to_current_user(self):
        visible = self.env["cas.correspondence.letter"].search([])
        for relation in self:
            relation.visible_to_current_user = (
                relation.letter_id in visible and relation.related_letter_id in visible
            )

    def _search_visible_to_current_user(self, operator, value):
        expected = _search_wants_true(operator, value)
        visible = self.env["cas.correspondence.letter"].search([])
        domain = [
            ("letter_id", "in", visible.ids),
            ("related_letter_id", "in", visible.ids),
        ]
        return domain if expected else ["!", *domain]

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.context.get("cas_correspondence_relation_engine"):
            raise AccessError(_("رابطه نامه فقط توسط موتور مکاتبات ثبت می‌شود."))
        for vals in vals_list:
            letter = self.env["cas.correspondence.letter"].browse(vals.get("letter_id")).exists()
            related = self.env["cas.correspondence.letter"].browse(
                vals.get("related_letter_id")
            ).exists()
            if not letter or not related or letter.company_id != related.company_id:
                raise ValidationError(_("نامه‌های مرتبط باید معتبر و متعلق به یک شرکت باشند."))
            letter.check_access("read")
            related.check_access("read")
        return super().create(vals_list)

    def write(self, vals):
        raise ValidationError(_("رابطه رسمی نامه قابل ویرایش نیست."))

    def unlink(self):
        raise ValidationError(_("رابطه رسمی نامه قابل حذف نیست."))
