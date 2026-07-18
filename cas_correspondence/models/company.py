from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    cas_correspondence_ceo_user_id = fields.Many2one(
        "res.users",
        string="مدیرعامل مکاتبات",
        ondelete="restrict",
        domain="[('active', '=', True), ('share', '=', False)]",
    )
    cas_correspondence_sequence_id = fields.Many2one(
        "ir.sequence",
        string="شماره‌گذار مکاتبات داخلی",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )

    @api.constrains("cas_correspondence_ceo_user_id")
    def _check_correspondence_ceo(self):
        for company in self:
            user = company.cas_correspondence_ceo_user_id.with_context(active_test=False)
            if user and (not user.active or user.share or company not in user.company_ids):
                raise ValidationError(
                    _("مدیرعامل مکاتبات باید کاربر داخلی، فعال و عضو همان شرکت باشد.")
                )

    def _cas_correspondence_sequence(self):
        self.ensure_one()
        sequence = self.cas_correspondence_sequence_id
        if sequence:
            return sequence
        sequence = self.env["ir.sequence"].sudo().create(
            {
                "name": _("شماره نامه داخلی - %s", self.name),
                "code": f"cas.correspondence.letter.{self.id}",
                "prefix": f"CAS{self.id}/%(year)s/",
                "padding": 6,
                "company_id": self.id,
            }
        )
        self.sudo().write({"cas_correspondence_sequence_id": sequence.id})
        return sequence
