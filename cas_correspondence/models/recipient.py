from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError

from .letter import PRIORITY, _search_wants_true


EXPECTATION = [
    ("information", "صرفاً جهت اطلاع"),
    ("action", "جهت اقدام"),
    ("reply", "نیازمند پاسخ"),
]

ACTION_STATUS = [
    ("pending", "در انتظار ارسال"),
    ("delivered", "تحویل‌شده"),
    ("viewed", "مشاهده‌شده"),
    ("in_progress", "در حال اقدام"),
    ("completed", "انجام‌شده"),
    ("replied", "پاسخ‌داده‌شده"),
    ("cancelled", "لغوشده"),
]


class CasCorrespondenceVisibilityMixin(models.AbstractModel):
    _name = "cas.correspondence.visibility.mixin"
    _description = "CAS Correspondence Child Visibility"

    visible_to_current_user = fields.Boolean(
        compute="_compute_visible_to_current_user",
        search="_search_visible_to_current_user",
    )

    @api.depends_context("uid", "allowed_company_ids")
    def _compute_visible_to_current_user(self):
        visible = self.env["cas.correspondence.letter"].search([])
        for record in self:
            record.visible_to_current_user = record.letter_id in visible

    def _search_visible_to_current_user(self, operator, value):
        expected = _search_wants_true(operator, value)
        visible = self.env["cas.correspondence.letter"].search([])
        domain = [("letter_id", "in", visible.ids)]
        return domain if expected else [("letter_id", "not in", visible.ids)]

    def _validate_target_user(self, user, company):
        user = user.with_context(active_test=False)
        if not user or not user.active or user.share or company not in user.company_ids:
            raise ValidationError(_("مسئول مخاطب باید کاربر داخلی و فعال همان شرکت باشد."))
        return user

    def _resolve_target(self):
        self.ensure_one()
        if self.target_kind == "user":
            if not self.recipient_user_id or self.department_id:
                raise ValidationError(_("برای مخاطب شخصی فقط انتخاب کاربر الزامی است."))
            return self._validate_target_user(self.recipient_user_id, self.company_id)
        if self.target_kind == "department":
            if not self.department_id or self.recipient_user_id:
                raise ValidationError(_("برای مخاطب واحدی فقط انتخاب واحد الزامی است."))
            if self.department_id.company_id and self.department_id.company_id != self.company_id:
                raise ValidationError(_("واحد مخاطب باید متعلق به شرکت نامه باشد."))
            return self._validate_target_user(
                self.department_id.manager_id.user_id, self.company_id
            )
        raise ValidationError(_("نوع مخاطب معتبر نیست."))

    def _create_activity(self):
        self.ensure_one()
        deadline = fields.Date.to_date(self.deadline) if self.deadline else fields.Date.context_today(self)
        activity = self.env["mail.activity"].sudo().create(
            {
                "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
                "res_model_id": self.env["ir.model"]._get_id("cas.correspondence.letter"),
                "res_id": self.letter_id.id,
                "user_id": self.responsible_user_id.id,
                "summary": self._activity_summary(),
                "note": self.note or self.letter_id.subject,
                "date_deadline": deadline,
            }
        )
        self.with_context(cas_correspondence_engine=True).write({"activity_id": activity.id})

    def _complete_activity(self, feedback):
        for record in self.filtered("activity_id"):
            record.activity_id.sudo().action_feedback(feedback=feedback)
            record.with_context(cas_correspondence_engine=True).write({"activity_id": False})

    def _require_responsible(self):
        for record in self:
            record.letter_id.check_access("read")
            if record.responsible_user_id != self.env.user and not self.env.is_superuser():
                raise AccessError(_("این اقدام به شما واگذار نشده است."))

    def _cas_action_descriptor(self):
        self.ensure_one()
        prefix = "recipient" if self._name == "cas.correspondence.recipient" else "referral"
        return {
            "source_model": self._name,
            "source_record_id": self.id,
            "action_key": f"{prefix}:{self.id}",
            "action_type": self.expectation,
            "title": self.letter_id.subject,
            "responsible_user_id": self.responsible_user_id.id,
            "original_responsible_user_id": self.responsible_user_id.id,
            "delegate_user_id": False,
            "priority": self.priority,
            "deadline": fields.Datetime.to_string(self.deadline) if self.deadline else False,
            "company_id": self.company_id.id,
            "status": self.status,
            "destination": {
                "type": "ir.actions.act_window",
                "res_model": "cas.correspondence.letter",
                "res_id": self.letter_id.id,
                "views": [[False, "form"]],
            },
            "source_adapter": "cas_correspondence",
        }


class CasCorrespondenceRecipient(models.Model):
    _name = "cas.correspondence.recipient"
    _description = "CAS Correspondence Recipient"
    _inherit = ["cas.correspondence.visibility.mixin"]
    _order = "role, id"

    letter_id = fields.Many2one(
        "cas.correspondence.letter", required=True, ondelete="restrict", index=True
    )
    company_id = fields.Many2one(
        related="letter_id.company_id", store=True, readonly=True, index=True
    )
    role = fields.Selection(
        [("to", "گیرنده اصلی"), ("cc", "رونوشت")],
        required=True,
        default="to",
        index=True,
    )
    target_kind = fields.Selection(
        [("user", "شخص"), ("department", "واحد")],
        required=True,
        default="user",
    )
    recipient_user_id = fields.Many2one(
        "res.users",
        string="مخاطب",
        ondelete="restrict",
        index=True,
        domain="[('active', '=', True), ('share', '=', False)]",
    )
    department_id = fields.Many2one(
        "hr.department", string="واحد مخاطب", ondelete="restrict", index=True
    )
    responsible_user_id = fields.Many2one(
        "res.users", string="مسئول نهایی", readonly=True, ondelete="restrict", index=True
    )
    expectation = fields.Selection(
        EXPECTATION, required=True, default="information", index=True
    )
    priority = fields.Selection(PRIORITY, required=True, default="normal", index=True)
    deadline = fields.Datetime(index=True)
    note = fields.Text(string="توضیح مخاطب")
    status = fields.Selection(
        ACTION_STATUS, required=True, default="pending", readonly=True, index=True
    )
    delivered_at = fields.Datetime(readonly=True, index=True)
    viewed_at = fields.Datetime(readonly=True, index=True)
    started_at = fields.Datetime(readonly=True, index=True)
    completed_at = fields.Datetime(readonly=True, index=True)
    action_result = fields.Text(readonly=True)
    reply_letter_id = fields.Many2one(
        "cas.correspondence.letter", readonly=True, ondelete="restrict"
    )
    activity_id = fields.Many2one("mail.activity", readonly=True, ondelete="set null")

    _recipient_once = models.Constraint(
        "UNIQUE(letter_id, role, recipient_user_id, department_id)",
        "این مخاطب با همین نقش قبلاً افزوده شده است.",
    )

    @api.constrains("target_kind", "recipient_user_id", "department_id", "role", "letter_id")
    def _check_recipient_contract(self):
        for line in self:
            if line.target_kind == "user" and (not line.recipient_user_id or line.department_id):
                raise ValidationError(_("مخاطب شخصی باید فقط یک کاربر داشته باشد."))
            if line.target_kind == "department" and (not line.department_id or line.recipient_user_id):
                raise ValidationError(_("مخاطب واحدی باید فقط یک واحد داشته باشد."))
            target_field = "recipient_user_id" if line.target_kind == "user" else "department_id"
            if self.search_count(
                [
                    ("id", "!=", line.id),
                    ("letter_id", "=", line.letter_id.id),
                    ("role", "=", line.role),
                    (target_field, "=", line[target_field].id),
                ]
            ):
                raise ValidationError(_("این مخاطب با همین نقش قبلاً افزوده شده است."))

    @api.model_create_multi
    def create(self, vals_list):
        records = self.browse()
        for vals in vals_list:
            letter = self.env["cas.correspondence.letter"].browse(vals.get("letter_id")).exists()
            if not letter or letter.state != "draft" or letter.sender_user_id != self.env.user:
                raise AccessError(_("مخاطب فقط توسط فرستنده و در پیش‌نویس قابل افزودن است."))
            values = dict(vals)
            values.update(
                {
                    "responsible_user_id": False,
                    "status": "pending",
                    "priority": values.get("priority") or letter.priority,
                    "deadline": values.get("deadline") or letter.default_deadline,
                }
            )
            records |= super(CasCorrespondenceRecipient, self).create(values)
        records.mapped("letter_id")._sync_access_index()
        return records

    def write(self, vals):
        if not self.env.context.get("cas_correspondence_engine"):
            if any(line.letter_id.state != "draft" for line in self):
                raise ValidationError(_("مخاطب نامه ارسال‌شده قابل ویرایش نیست."))
            if any(line.letter_id.sender_user_id != self.env.user for line in self):
                raise AccessError(_("فقط فرستنده می‌تواند مخاطبان پیش‌نویس را ویرایش کند."))
            protected = {
                "responsible_user_id",
                "status",
                "delivered_at",
                "viewed_at",
                "started_at",
                "completed_at",
                "action_result",
                "reply_letter_id",
                "activity_id",
            }
            if protected.intersection(vals):
                raise ValidationError(_("فیلدهای اجرایی مخاطب قابل ویرایش مستقیم نیستند."))
        result = super().write(vals)
        self.mapped("letter_id")._sync_access_index()
        return result

    def unlink(self):
        letters = self.mapped("letter_id")
        if any(letter.state != "draft" or letter.sender_user_id != self.env.user for letter in letters):
            raise ValidationError(_("مخاطب نامه ارسال‌شده قابل حذف نیست."))
        result = super().unlink()
        letters._sync_access_index()
        return result

    def _prepare_for_delivery(self):
        for line in self:
            responsible = line._resolve_target()
            if responsible == line.letter_id.sender_user_id:
                raise ValidationError(_("فرستنده نمی‌تواند مخاطب همان نامه باشد."))
            line.with_context(cas_correspondence_engine=True).write(
                {"responsible_user_id": responsible.id}
            )

    def _deliver(self, delivered_at=None):
        delivered_at = delivered_at or fields.Datetime.now()
        for line in self:
            line.with_context(cas_correspondence_engine=True).write(
                {"status": "delivered", "delivered_at": delivered_at}
            )
            line._create_activity()

    def _activity_summary(self):
        self.ensure_one()
        return {
            "information": _("مشاهده نامه داخلی"),
            "action": _("اقدام روی نامه داخلی"),
            "reply": _("پاسخ رسمی به نامه داخلی"),
        }[self.expectation]

    def action_mark_viewed(self):
        self._require_responsible()
        now = fields.Datetime.now()
        for line in self:
            if line.status not in ("delivered", "viewed"):
                continue
            values = {"viewed_at": line.viewed_at or now}
            if line.expectation == "information":
                values.update({"status": "completed", "completed_at": now})
            else:
                values["status"] = "viewed"
            line.with_context(cas_correspondence_engine=True).write(values)
            self.env["cas.correspondence.view.receipt"].with_context(
                cas_correspondence_engine=True
            ).create(
                {
                    "letter_id": line.letter_id.id,
                    "recipient_id": line.id,
                    "viewer_user_id": self.env.user.id,
                    "viewed_at": now,
                }
            )
            if line.expectation == "information":
                line._complete_activity(_("نامه مشاهده شد."))
            if not line.letter_id.first_viewed_at:
                line.letter_id.with_context(cas_correspondence_engine=True).write(
                    {"first_viewed_at": now}
                )
            line.letter_id._audit("viewed", payload={"recipient_id": line.id})
            line.letter_id._refresh_state()
        return True

    def action_start(self):
        self._require_responsible()
        for line in self:
            if line.expectation == "information" or line.status not in ("delivered", "viewed"):
                raise ValidationError(_("این مخاطب در وضعیت قابل شروع اقدام نیست."))
            line.with_context(cas_correspondence_engine=True).write(
                {"status": "in_progress", "started_at": fields.Datetime.now()}
            )
            line.letter_id._audit("started", payload={"recipient_id": line.id})
            line.letter_id._refresh_state()
        return True

    def action_complete(self, result=False):
        self._require_responsible()
        for line in self:
            if line.expectation != "action":
                raise ValidationError(_("این مخاطب نیازمند ثبت نتیجه اقدام نیست."))
            if line.status not in ("viewed", "in_progress"):
                raise ValidationError(_("اقدام در وضعیت قابل تکمیل نیست."))
            if not str(result or "").strip():
                raise ValidationError(_("ثبت نتیجه اقدام الزامی است."))
            now = fields.Datetime.now()
            line.with_context(cas_correspondence_engine=True).write(
                {"status": "completed", "completed_at": now, "action_result": result}
            )
            line._complete_activity(result)
            line.letter_id._audit(
                "completed", reason=result, payload={"recipient_id": line.id}
            )
            line.letter_id._refresh_state()
        return True

    def action_open_complete_wizard(self):
        self.ensure_one()
        self._require_responsible()
        return {
            "type": "ir.actions.act_window",
            "name": _("ثبت نتیجه اقدام"),
            "res_model": "cas.correspondence.complete.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_source_model": self._name,
                "default_source_id": self.id,
            },
        }

    def _mark_replied(self, reply_letter):
        now = fields.Datetime.now()
        for line in self:
            line.with_context(cas_correspondence_engine=True).write(
                {
                    "status": "replied",
                    "completed_at": now,
                    "reply_letter_id": reply_letter.id,
                }
            )
            line._complete_activity(_("پاسخ رسمی ثبت شد."))


class CasCorrespondenceReferral(models.Model):
    _name = "cas.correspondence.referral"
    _description = "CAS Correspondence Referral"
    _inherit = ["cas.correspondence.visibility.mixin"]
    _order = "create_date desc, id desc"

    letter_id = fields.Many2one(
        "cas.correspondence.letter", required=True, ondelete="restrict", index=True
    )
    company_id = fields.Many2one(
        related="letter_id.company_id", store=True, readonly=True, index=True
    )
    referrer_user_id = fields.Many2one(
        "res.users", required=True, readonly=True, ondelete="restrict", index=True
    )
    target_kind = fields.Selection(
        [("user", "شخص"), ("department", "واحد")], required=True, default="user"
    )
    recipient_user_id = fields.Many2one(
        "res.users", string="مخاطب", ondelete="restrict", index=True
    )
    department_id = fields.Many2one(
        "hr.department", string="واحد مخاطب", ondelete="restrict", index=True
    )
    responsible_user_id = fields.Many2one(
        "res.users", string="مسئول نهایی", required=True, readonly=True, ondelete="restrict", index=True
    )
    expectation = fields.Selection(
        EXPECTATION, required=True, default="action", index=True
    )
    priority = fields.Selection(PRIORITY, required=True, default="normal", index=True)
    deadline = fields.Datetime(index=True)
    note = fields.Text(required=True)
    status = fields.Selection(
        ACTION_STATUS, required=True, default="delivered", readonly=True, index=True
    )
    delivered_at = fields.Datetime(required=True, readonly=True, index=True)
    viewed_at = fields.Datetime(readonly=True, index=True)
    started_at = fields.Datetime(readonly=True, index=True)
    completed_at = fields.Datetime(readonly=True, index=True)
    action_result = fields.Text(readonly=True)
    reply_letter_id = fields.Many2one(
        "cas.correspondence.letter", readonly=True, ondelete="restrict"
    )
    activity_id = fields.Many2one("mail.activity", readonly=True, ondelete="set null")

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.context.get("cas_correspondence_referral_engine"):
            raise AccessError(_("ارجاع فقط از مسیر رسمی نامه قابل ایجاد است."))
        records = self.browse()
        for vals in vals_list:
            values = dict(vals)
            record = super(CasCorrespondenceReferral, self).create(values)
            records |= record
        records._create_activity()
        records.mapped("letter_id")._sync_access_index()
        return records

    def write(self, vals):
        if not self.env.context.get("cas_correspondence_engine"):
            raise ValidationError(_("ارجاع قابل ویرایش مستقیم نیست."))
        return super().write(vals)

    def unlink(self):
        raise ValidationError(_("ارجاع و سابقه آن قابل حذف نیست."))

    def _activity_summary(self):
        self.ensure_one()
        return {
            "information": _("مشاهده ارجاع نامه"),
            "action": _("اقدام ارجاع‌شده"),
            "reply": _("پاسخ به ارجاع نامه"),
        }[self.expectation]

    def action_mark_viewed(self):
        self._require_responsible()
        now = fields.Datetime.now()
        for referral in self:
            values = {"viewed_at": referral.viewed_at or now}
            if referral.expectation == "information":
                values.update({"status": "completed", "completed_at": now})
            elif referral.status == "delivered":
                values["status"] = "viewed"
            referral.with_context(cas_correspondence_engine=True).write(values)
            self.env["cas.correspondence.view.receipt"].with_context(
                cas_correspondence_engine=True
            ).create(
                {
                    "letter_id": referral.letter_id.id,
                    "referral_id": referral.id,
                    "viewer_user_id": self.env.user.id,
                    "viewed_at": now,
                }
            )
            if referral.expectation == "information":
                referral._complete_activity(_("ارجاع مشاهده شد."))
            referral.letter_id._audit("viewed", payload={"referral_id": referral.id})
            referral.letter_id._refresh_state()
        return True

    def action_start(self):
        self._require_responsible()
        for referral in self:
            if referral.expectation == "information" or referral.status not in ("delivered", "viewed"):
                raise ValidationError(_("این ارجاع در وضعیت قابل شروع نیست."))
            referral.with_context(cas_correspondence_engine=True).write(
                {"status": "in_progress", "started_at": fields.Datetime.now()}
            )
            referral.letter_id._audit("started", payload={"referral_id": referral.id})
            referral.letter_id._refresh_state()
        return True

    def action_complete(self, result=False):
        self._require_responsible()
        for referral in self:
            if referral.expectation != "action" or referral.status not in ("viewed", "in_progress"):
                raise ValidationError(_("این ارجاع در وضعیت قابل تکمیل اقدام نیست."))
            if not str(result or "").strip():
                raise ValidationError(_("ثبت نتیجه اقدام ارجاع الزامی است."))
            now = fields.Datetime.now()
            referral.with_context(cas_correspondence_engine=True).write(
                {"status": "completed", "completed_at": now, "action_result": result}
            )
            referral._complete_activity(result)
            referral.letter_id._audit("completed", reason=result, payload={"referral_id": referral.id})
            referral.letter_id._refresh_state()
        return True

    def action_open_complete_wizard(self):
        self.ensure_one()
        self._require_responsible()
        return {
            "type": "ir.actions.act_window",
            "name": _("ثبت نتیجه ارجاع"),
            "res_model": "cas.correspondence.complete.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_source_model": self._name,
                "default_source_id": self.id,
            },
        }

    def _mark_replied(self, reply_letter):
        now = fields.Datetime.now()
        for referral in self:
            referral.with_context(cas_correspondence_engine=True).write(
                {
                    "status": "replied",
                    "completed_at": now,
                    "reply_letter_id": reply_letter.id,
                }
            )
            referral._complete_activity(_("پاسخ رسمی ثبت شد."))


class CasCorrespondenceViewReceipt(models.Model):
    _name = "cas.correspondence.view.receipt"
    _description = "CAS Correspondence Immutable View Receipt"
    _inherit = ["cas.correspondence.visibility.mixin"]
    _order = "viewed_at desc, id desc"

    letter_id = fields.Many2one(
        "cas.correspondence.letter", required=True, readonly=True, ondelete="restrict", index=True
    )
    company_id = fields.Many2one(
        related="letter_id.company_id", store=True, readonly=True, index=True
    )
    recipient_id = fields.Many2one(
        "cas.correspondence.recipient", readonly=True, ondelete="restrict", index=True
    )
    referral_id = fields.Many2one(
        "cas.correspondence.referral", readonly=True, ondelete="restrict", index=True
    )
    viewer_user_id = fields.Many2one(
        "res.users", required=True, readonly=True, ondelete="restrict", index=True
    )
    viewed_at = fields.Datetime(
        required=True, default=fields.Datetime.now, readonly=True, index=True
    )

    _recipient_receipt_unique = models.Constraint(
        "UNIQUE(recipient_id, viewer_user_id)", "رسید مشاهده مخاطب قبلاً ثبت شده است."
    )
    _referral_receipt_unique = models.Constraint(
        "UNIQUE(referral_id, viewer_user_id)", "رسید مشاهده ارجاع قبلاً ثبت شده است."
    )

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.context.get("cas_correspondence_engine"):
            raise AccessError(_("رسید مشاهده فقط توسط موتور مکاتبات ثبت می‌شود."))
        for vals in vals_list:
            if bool(vals.get("recipient_id")) == bool(vals.get("referral_id")):
                raise ValidationError(_("رسید باید دقیقاً به یک مخاطب یا ارجاع متصل باشد."))
        return super().create(vals_list)

    def write(self, vals):
        raise AccessError(_("رسید مشاهده تغییرناپذیر است."))

    def unlink(self):
        raise AccessError(_("رسید مشاهده قابل حذف نیست."))
