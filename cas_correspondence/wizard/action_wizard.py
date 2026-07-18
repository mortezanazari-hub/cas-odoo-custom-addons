from odoo import _, fields, models
from odoo.exceptions import ValidationError


class CasCorrespondenceCompleteWizard(models.TransientModel):
    _name = "cas.correspondence.complete.wizard"
    _description = "Complete CAS Correspondence Action"

    source_model = fields.Selection(
        [
            ("cas.correspondence.recipient", "مخاطب نامه"),
            ("cas.correspondence.referral", "ارجاع نامه"),
        ],
        required=True,
        readonly=True,
    )
    source_id = fields.Integer(required=True, readonly=True)
    result = fields.Text(string="نتیجه اقدام", required=True)

    def action_confirm(self):
        self.ensure_one()
        if self.source_model not in (
            "cas.correspondence.recipient",
            "cas.correspondence.referral",
        ):
            raise ValidationError(_("منبع اقدام معتبر نیست."))
        source = self.env[self.source_model].browse(self.source_id).exists()
        if not source:
            raise ValidationError(_("اقدام موردنظر پیدا نشد."))
        source.action_complete(self.result)
        return {"type": "ir.actions.act_window_close"}


class CasCorrespondenceDelegationRevokeWizard(models.TransientModel):
    _name = "cas.correspondence.delegation.revoke.wizard"
    _description = "Revoke CAS Secretariat Delegation"

    delegation_id = fields.Many2one(
        "cas.correspondence.secretariat.delegation",
        required=True,
        readonly=True,
        ondelete="cascade",
    )
    reason = fields.Text(string="دلیل لغو", required=True)

    def action_confirm(self):
        self.ensure_one()
        self.delegation_id.action_revoke(self.reason)
        return {"type": "ir.actions.act_window_close"}
