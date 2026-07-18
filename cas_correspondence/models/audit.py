from odoo import api, fields, models
from odoo.exceptions import AccessError, ValidationError

from .letter import _search_wants_true


class CasCorrespondenceAudit(models.Model):
    _name = "cas.correspondence.audit"
    _description = "CAS Correspondence Immutable Audit"
    _order = "event_at desc, id desc"

    letter_id = fields.Many2one(
        "cas.correspondence.letter", ondelete="restrict", index=True, readonly=True
    )
    delegation_id = fields.Many2one(
        "cas.correspondence.secretariat.delegation",
        ondelete="restrict",
        index=True,
        readonly=True,
    )
    company_id = fields.Many2one(
        "res.company", required=True, ondelete="restrict", index=True, readonly=True
    )
    event_type = fields.Selection(
        [
            ("created", "ایجاد"),
            ("sent", "ارسال"),
            ("delivered", "تحویل"),
            ("viewed", "مشاهده"),
            ("started", "شروع اقدام"),
            ("completed", "تکمیل اقدام"),
            ("replied", "پاسخ رسمی"),
            ("referred", "ارجاع"),
            ("closed", "مختومه"),
            ("corrected", "اصلاح/جایگزینی"),
            ("delegated", "تفویض دبیرخانه"),
            ("revoked", "لغو تفویض"),
        ],
        required=True,
        readonly=True,
        index=True,
    )
    actor_user_id = fields.Many2one(
        "res.users", required=True, ondelete="restrict", readonly=True, index=True
    )
    event_at = fields.Datetime(
        required=True, default=fields.Datetime.now, readonly=True, index=True
    )
    reason = fields.Text(readonly=True)
    payload = fields.Json(readonly=True)
    visible_to_current_user = fields.Boolean(
        compute="_compute_visible_to_current_user",
        search="_search_visible_to_current_user",
    )

    @api.depends_context("uid", "allowed_company_ids")
    def _compute_visible_to_current_user(self):
        visible_letters = self.env["cas.correspondence.letter"].search([])
        for record in self:
            if record.letter_id:
                record.visible_to_current_user = record.letter_id in visible_letters
            else:
                record.visible_to_current_user = bool(
                    record.delegation_id
                    and record.delegation_id._user_can_read(self.env.user)
                )

    def _search_visible_to_current_user(self, operator, value):
        expected = _search_wants_true(operator, value)
        letters = self.env["cas.correspondence.letter"].search([])
        delegations = self.env["cas.correspondence.secretariat.delegation"].sudo().search(
            [("company_id", "in", self.env.companies.ids)]
        ).filtered(lambda item: item._user_can_read(self.env.user))
        domain = [
            "|",
            ("letter_id", "in", letters.ids),
            ("delegation_id", "in", delegations.ids),
        ]
        return domain if expected else ["!", *domain]

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.context.get("cas_correspondence_audit_engine"):
            raise AccessError("Audit records can only be created by the correspondence engine.")
        for vals in vals_list:
            if bool(vals.get("letter_id")) == bool(vals.get("delegation_id")):
                raise ValidationError("Audit must reference exactly one business record.")
        return super().create(vals_list)

    def write(self, vals):
        raise AccessError("Correspondence audit records are immutable.")

    def unlink(self):
        raise AccessError("Correspondence audit records cannot be deleted.")
