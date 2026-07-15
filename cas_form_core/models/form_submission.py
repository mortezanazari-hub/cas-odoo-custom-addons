"""Version-pinned CAS form submissions with server-side validation."""

from __future__ import annotations

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CasFormSubmission(models.Model):
    _name = "cas.form.submission"
    _description = "CAS Form Submission"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc, id desc"
    _rec_name = "number"

    number = fields.Char(
        string="شماره رهگیری",
        required=True,
        default="New",
        copy=False,
        readonly=True,
        index=True,
        tracking=True,
    )
    version_id = fields.Many2one(
        "cas.form.version",
        string="نسخه فرم",
        required=True,
        ondelete="restrict",
        index=True,
        tracking=True,
        domain="[('state', '=', 'published')]",
    )
    definition_id = fields.Many2one(
        related="version_id.definition_id",
        string="فرم",
        store=True,
        index=True,
    )
    company_id = fields.Many2one(
        related="version_id.company_id",
        store=True,
        index=True,
    )
    owner_user_id = fields.Many2one(
        "res.users",
        string="مالک ثبت",
        required=True,
        default=lambda self: self.env.user,
        index=True,
        tracking=True,
    )
    state = fields.Selection(
        [
            ("draft", "پیش‌نویس"),
            ("submitted", "ارسال‌شده"),
            ("cancelled", "لغوشده"),
        ],
        string="وضعیت",
        required=True,
        default="draft",
        copy=False,
        index=True,
        tracking=True,
    )
    answer_ids = fields.One2many(
        "cas.form.answer",
        "submission_id",
        string="پاسخ‌ها",
        copy=False,
    )
    submitted_at = fields.Datetime(string="زمان ارسال", readonly=True, copy=False)
    submitted_by_id = fields.Many2one(
        "res.users",
        string="ارسال‌کننده",
        readonly=True,
        copy=False,
    )
    snapshot_json = fields.Json(
        string="Snapshot نهایی",
        readonly=True,
        copy=False,
    )
    reopen_count = fields.Integer(string="تعداد بازگشایی", readonly=True, copy=False)

    _number_uniq = models.Constraint(
        "UNIQUE(number)",
        "شماره رهگیری باید یکتا باشد.",
    )

    def _can_manage_owners(self):
        return self.env.is_superuser() or self.env.user.has_group(
            "cas_form_core.group_cas_form_manager"
        )

    def _sudo_answers(self):
        """Return answers without exposing a direct answer ACL to form users."""
        self.ensure_one()
        return self.env["cas.form.answer"].sudo().search(
            [("submission_id", "=", self.id)],
            order="field_sequence, id",
        )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            version = self.env["cas.form.version"].browse(vals.get("version_id")).exists()
            if not version or version.state != "published":
                raise ValidationError(_("ثبت جدید فقط از نسخه فعال و منتشرشده مجاز است."))
            if version.definition_id.current_version_id != version:
                raise ValidationError(_("نسخه انتخاب‌شده، نسخه فعال فرم نیست."))
            if vals.get("number", "New") == "New":
                vals["number"] = self.env["ir.sequence"].next_by_code(
                    "cas.form.submission"
                ) or "New"
            vals.setdefault("owner_user_id", self.env.user.id)
            if (
                not self._can_manage_owners()
                and vals["owner_user_id"] != self.env.user.id
            ):
                raise AccessError(_("کاربر عادی فقط می‌تواند ثبت را به نام خود ایجاد کند."))
            vals["state"] = "draft"
        return super().create(vals_list)

    def write(self, vals):
        locked = self.filtered(lambda submission: submission.state == "submitted")
        if locked:
            raise ValidationError(
                _("فرم ارسال‌شده قابل ویرایش نیست؛ ابتدا باید با مجوز بازگشایی شود.")
            )
        protected = {
            "number",
            "version_id",
            "definition_id",
            "company_id",
            "submitted_at",
            "submitted_by_id",
            "snapshot_json",
            "reopen_count",
        }
        if protected.intersection(vals):
            raise ValidationError(_("فیلدهای سیستمی ثبت فرم قابل ویرایش مستقیم نیستند."))
        if "state" in vals:
            raise ValidationError(_("تغییر وضعیت فقط از طریق عملیات رسمی مجاز است."))
        if (
            "owner_user_id" in vals
            and not self._can_manage_owners()
            and vals["owner_user_id"] != self.env.user.id
        ):
            raise AccessError(_("تغییر مالک ثبت به کاربر دیگر مجاز نیست."))
        return super().write(vals)

    def unlink(self):
        if any(submission.state != "draft" for submission in self):
            raise ValidationError(_("فقط پیش‌نویس قابل حذف است."))
        return super().unlink()

    def _check_draft_and_access(self):
        self.ensure_one()
        self.check_access("write")
        if self.state != "draft":
            raise ValidationError(_("فقط پیش‌نویس قابل ویرایش است."))

    def action_save_answers(self, values):
        """Validate and persist a mapping of ``technical_key -> value``.

        Ordinary users have no direct ACL on ``cas.form.answer``. This method
        validates the submission and schema under the caller, then performs the
        minimal answer mutation with elevated rights.
        """
        self._check_draft_and_access()
        if not isinstance(values, dict):
            raise ValidationError(_("پاسخ‌ها باید به‌صورت مجموعه کلید و مقدار ارسال شوند."))

        fields_by_key = {
            form_field.technical_key: form_field for form_field in self.version_id.field_ids
        }
        unknown = set(values) - set(fields_by_key)
        if unknown:
            raise ValidationError(
                _("کلیدهای فیلد ناشناخته‌اند: %s", "، ".join(sorted(unknown)))
            )

        AnswerValidator = self.env["cas.form.answer"]
        AnswerWriter = AnswerValidator.sudo()
        existing_by_field = {
            answer.field_id.id: answer for answer in self._sudo_answers()
        }
        for technical_key, raw_value in values.items():
            form_field = fields_by_key[technical_key]
            existing = existing_by_field.get(form_field.id)
            if raw_value is None:
                if existing:
                    existing.unlink()
                continue

            # Normalize with the caller's environment so related-record ACLs
            # and record rules remain effective.
            normalized = AnswerValidator._normalized_values(form_field, raw_value)
            if existing:
                existing.write(normalized)
            else:
                normalized.update(
                    {
                        "submission_id": self.id,
                        "field_id": form_field.id,
                    }
                )
                AnswerWriter.create(normalized)
        return self.action_get_answers()

    def action_get_answers(self):
        self.ensure_one()
        self.check_access("read")
        return {
            answer.field_key: answer._export_value()
            for answer in self._sudo_answers()
        }

    def _validate_required_answers(self):
        self.ensure_one()
        answers_by_field = {
            answer.field_id.id: answer for answer in self._sudo_answers()
        }
        missing = []
        for form_field in self.version_id.field_ids.filtered("required"):
            answer = answers_by_field.get(form_field.id)
            if not answer or answer._is_empty():
                missing.append(form_field.label)
        if missing:
            raise ValidationError(
                _("تکمیل فیلدهای اجباری زیر الزامی است: %s", "، ".join(missing))
            )

    def _build_snapshot(self):
        self.ensure_one()
        answers = []
        for answer in self._sudo_answers():
            answers.append(
                {
                    "field_uuid": answer.field_id.field_uuid,
                    "technical_key": answer.field_key,
                    "label": answer.field_id.label,
                    "field_type": answer.field_type,
                    "value": answer._export_value(),
                }
            )
        return {
            "snapshot_version": 1,
            "submission_number": self.number,
            "form_code": self.definition_id.code,
            "form_name": self.definition_id.name,
            "form_revision": self.version_id.revision,
            "schema_hash": self.version_id.schema_hash,
            "schema": self.version_id._schema_payload(),
            "answers": answers,
            "owner_user_id": self.owner_user_id.id,
            "owner_user_name": self.owner_user_id.name,
        }

    def action_submit(self, values=None):
        self._check_draft_and_access()
        if values is not None:
            self.action_save_answers(values)
        self._validate_required_answers()
        snapshot = self._build_snapshot()
        super(CasFormSubmission, self).write(
            {
                "state": "submitted",
                "submitted_at": fields.Datetime.now(),
                "submitted_by_id": self.env.user.id,
                "snapshot_json": snapshot,
            }
        )
        return True

    def action_cancel(self):
        self._check_draft_and_access()
        super(CasFormSubmission, self).write({"state": "cancelled"})
        return True

    def action_reopen(self, reason):
        self.ensure_one()
        if self.state != "submitted":
            raise ValidationError(_("فقط فرم ارسال‌شده قابل بازگشایی است."))
        if not reason or not str(reason).strip():
            raise ValidationError(_("ثبت دلیل بازگشایی الزامی است."))
        if not (
            self.env.is_superuser()
            or self.env.user.has_group("cas_form_core.group_cas_form_manager")
        ):
            raise AccessError(_("شما مجوز بازگشایی فرم را ندارید."))
        super(CasFormSubmission, self).write(
            {
                "state": "draft",
                "snapshot_json": False,
                "submitted_at": False,
                "submitted_by_id": False,
                "reopen_count": self.reopen_count + 1,
            }
        )
        self.message_post(body=_("فرم با دلیل زیر بازگشایی شد: %s", reason))
        return True
