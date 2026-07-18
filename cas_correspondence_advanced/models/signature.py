import hashlib

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CasCorrespondenceSignature(models.Model):
    _name = "cas.correspondence.signature"
    _description = "CAS Auditable Correspondence Signature"
    _order = "signed_at desc, id desc"

    letter_id = fields.Many2one("cas.correspondence.letter", string="نامه داخلی", ondelete="restrict", index=True)
    register_id = fields.Many2one("cas.correspondence.register", string="ثبت وارده/صادره", ondelete="restrict", index=True)
    company_id = fields.Many2one("res.company", compute="_compute_company", store=True, index=True)
    signer_user_id = fields.Many2one("res.users", string="امضاکننده", required=True, default=lambda self: self.env.user, ondelete="restrict")
    method = fields.Selection(
        [("organizational", "تأیید سازمانی"), ("external_digital", "امضای دیجیتال بیرونی")],
        required=True, default="organizational", readonly=True,
    )
    state = fields.Selection([("pending", "در انتظار"), ("signed", "امضاشده"), ("revoked", "ابطال‌شده")], required=True, default="pending", readonly=True)
    source_digest = fields.Char(string="هش محتوای امضاشده", readonly=True, index=True)
    provider_reference = fields.Char(string="شناسه سرویس امضا", readonly=True)
    certificate_serial = fields.Char(string="شماره گواهی", readonly=True)
    provider_signature_digest = fields.Char(string="هش امضای سرویس", readonly=True)
    signed_at = fields.Datetime(readonly=True)
    revoked_at = fields.Datetime(readonly=True)
    revoke_reason = fields.Text(readonly=True)

    @api.depends("letter_id.company_id", "register_id.company_id")
    def _compute_company(self):
        for signature in self:
            signature.company_id = signature.letter_id.company_id or signature.register_id.company_id

    @api.constrains("letter_id", "register_id", "signer_user_id")
    def _check_contract(self):
        for signature in self:
            if bool(signature.letter_id) == bool(signature.register_id):
                raise ValidationError("امضا باید دقیقاً به یک منبع متصل باشد.")
            if signature.company_id not in signature.signer_user_id.company_ids:
                raise ValidationError("امضاکننده باید عضو شرکت منبع باشد.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("state", "pending") != "pending" and not self.env.context.get("cas_correspondence_advanced_engine"):
                raise AccessError("ثبت امضای نهایی فقط از عملیات رسمی ممکن است.")
        return super().create(vals_list)

    def write(self, vals):
        if not self.env.context.get("cas_correspondence_advanced_engine"):
            raise ValidationError("رکورد امضا تغییرپذیر نیست؛ از عملیات رسمی استفاده کنید.")
        return super().write(vals)

    def unlink(self):
        if any(signature.state != "pending" for signature in self):
            raise ValidationError("امضای نهایی قابل حذف نیست.")
        return super().unlink()

    def _current_source_digest(self):
        self.ensure_one()
        digest = self.letter_id.official_pdf_sha256 or self.register_id.current_sha256
        if not digest:
            raise ValidationError("منبع هنوز نسخه رسمی قابل امضا ندارد.")
        return digest

    def action_sign_organizational(self):
        for signature in self:
            if signature.state != "pending" or signature.method != "organizational":
                raise ValidationError("این امضا قابل تأیید سازمانی نیست.")
            if signature.signer_user_id != self.env.user:
                raise AccessError("فقط امضاکننده تعیین‌شده مجاز است.")
            digest = signature._current_source_digest()
            signature.with_context(cas_correspondence_advanced_engine=True).write({
                "state": "signed", "source_digest": digest, "signed_at": fields.Datetime.now(),
            })
            if signature.register_id:
                signature.register_id._append_event("signed", digest=digest)
        return True

    def record_external_signature(self, provider_reference, certificate_serial, signature_bytes):
        self.ensure_one()
        if self.state != "pending" or self.method != "external_digital":
            raise ValidationError("درخواست امضای دیجیتال معتبر نیست.")
        if self.signer_user_id != self.env.user and not self.env.user.has_group("cas_correspondence.group_cas_correspondence_manager"):
            raise AccessError("مجوز ثبت پاسخ سرویس امضا را ندارید.")
        if not provider_reference or not certificate_serial or not signature_bytes:
            raise ValidationError("پاسخ سرویس امضا ناقص است.")
        digest = self._current_source_digest()
        signature_digest = hashlib.sha256(bytes(signature_bytes)).hexdigest()
        self.with_context(cas_correspondence_advanced_engine=True).write({
            "state": "signed", "source_digest": digest, "provider_reference": provider_reference,
            "certificate_serial": certificate_serial, "provider_signature_digest": signature_digest,
            "signed_at": fields.Datetime.now(),
        })
        if self.register_id:
            self.register_id._append_event("signed", note=provider_reference, digest=digest)
        return True

    def action_revoke(self, reason=False):
        if not self.env.user.has_group("cas_correspondence.group_cas_correspondence_manager"):
            raise AccessError("فقط مدیر مکاتبات مجاز به ثبت ابطال است.")
        for signature in self:
            if signature.state != "signed" or not str(reason or "").strip():
                raise ValidationError("دلیل ابطال امضای نهایی الزامی است.")
            signature.with_context(cas_correspondence_advanced_engine=True).write({
                "state": "revoked", "revoked_at": fields.Datetime.now(), "revoke_reason": reason,
            })
        return True
