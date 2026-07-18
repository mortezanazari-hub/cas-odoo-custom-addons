from odoo import _, fields, models
from odoo.exceptions import AccessError, ValidationError

from ..models.letter import PRIORITY
from ..models.recipient import EXPECTATION


class CasCorrespondenceReferralWizard(models.TransientModel):
    _name = "cas.correspondence.referral.wizard"
    _description = "Refer CAS Correspondence Letter"

    letter_id = fields.Many2one(
        "cas.correspondence.letter", required=True, readonly=True, ondelete="cascade"
    )
    target_kind = fields.Selection(
        [("user", "شخص"), ("department", "واحد")], required=True, default="user"
    )
    recipient_user_id = fields.Many2one(
        "res.users", string="مخاطب", domain="[('active', '=', True), ('share', '=', False)]"
    )
    department_id = fields.Many2one("hr.department", string="واحد مخاطب")
    expectation = fields.Selection(EXPECTATION, required=True, default="action")
    priority = fields.Selection(PRIORITY, required=True, default="normal")
    deadline = fields.Datetime()
    note = fields.Text(string="توضیح ارجاع", required=True)

    def action_confirm(self):
        self.ensure_one()
        letter = self.letter_id
        letter.check_access("read")
        if letter.state in ("draft", "closed", "cancelled"):
            raise ValidationError(_("نامه در وضعیت قابل ارجاع نیست."))
        if self.target_kind == "user":
            if not self.recipient_user_id or self.department_id:
                raise ValidationError(_("برای ارجاع شخصی فقط انتخاب مخاطب الزامی است."))
            responsible = self.recipient_user_id.with_context(active_test=False)
        elif self.target_kind == "department":
            if not self.department_id or self.recipient_user_id:
                raise ValidationError(_("برای ارجاع واحدی فقط انتخاب واحد الزامی است."))
            if self.department_id.company_id and self.department_id.company_id != letter.company_id:
                raise ValidationError(_("واحد ارجاع باید متعلق به شرکت نامه باشد."))
            responsible = self.department_id.manager_id.user_id.with_context(active_test=False)
        else:
            raise ValidationError(_("نوع مخاطب ارجاع معتبر نیست."))
        if not responsible or not responsible.active or responsible.share or letter.company_id not in responsible.company_ids:
            raise ValidationError(_("برای مخاطب ارجاع، کاربر مسئول فعال و معتبر پیدا نشد."))
        if responsible == self.env.user:
            raise ValidationError(_("ارجاع نامه به خود کاربر مجاز نیست."))
        referral = self.env["cas.correspondence.referral"].with_context(
            cas_correspondence_referral_engine=True
        ).create(
            {
                "letter_id": letter.id,
                "referrer_user_id": self.env.user.id,
                "target_kind": self.target_kind,
                "recipient_user_id": self.recipient_user_id.id,
                "department_id": self.department_id.id,
                "responsible_user_id": responsible.id,
                "expectation": self.expectation,
                "priority": self.priority,
                "deadline": self.deadline,
                "note": self.note,
                "status": "delivered",
                "delivered_at": fields.Datetime.now(),
            }
        )
        if not referral:
            raise AccessError(_("ارجاع ایجاد نشد."))
        letter._audit("referred", reason=self.note, payload={"referral_id": referral.id})
        letter._sync_access_index()
        return {"type": "ir.actions.act_window_close"}
