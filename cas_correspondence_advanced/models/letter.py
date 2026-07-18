import base64
import hashlib

from odoo import _, fields, models
from odoo.exceptions import AccessError, ValidationError


class CasCorrespondenceAuditAdvanced(models.Model):
    _inherit = "cas.correspondence.audit"

    event_type = fields.Selection(
        selection_add=[("official_pdf_generated", "تولید PDF رسمی")],
        ondelete={"official_pdf_generated": "cascade"},
    )


class CasCorrespondenceLetterAdvanced(models.Model):
    _inherit = "cas.correspondence.letter"

    template_id = fields.Many2one("cas.correspondence.template", string="قالب رسمی", ondelete="restrict")
    document_id = fields.Many2one("cas.document", string="سند نسخه‌دار", readonly=True, copy=False, ondelete="restrict")
    official_pdf_attachment_id = fields.Many2one("ir.attachment", string="PDF رسمی", readonly=True, copy=False, ondelete="restrict")
    official_pdf_sha256 = fields.Char(string="SHA-256 نسخه رسمی", readonly=True, copy=False)
    official_pdf_generated_at = fields.Datetime(string="زمان تولید PDF", readonly=True, copy=False)
    advanced_signature_ids = fields.One2many("cas.correspondence.signature", "letter_id", string="امضاهای پیشرفته", copy=False)

    def _advanced_folder(self):
        self.ensure_one()
        folder = self.template_id.document_folder_id
        if not folder:
            folder = self.env["cas.document.folder"].sudo().search(
                [("company_id", "=", self.company_id.id), ("code", "=", "CORRESPONDENCE")], limit=1
            )
        if not folder:
            folder = self.env["cas.document.folder"].sudo().create({
                "name": _("مکاتبات رسمی"), "code": "CORRESPONDENCE", "company_id": self.company_id.id,
                "manager_user_id": self.sender_user_id.id,
            })
        return folder

    def action_apply_template(self):
        for letter in self:
            if letter.state != "draft" or letter.sender_user_id != self.env.user:
                raise AccessError("فقط فرستنده می‌تواند قالب پیش‌نویس را اعمال کند.")
            if not letter.template_id:
                raise ValidationError("ابتدا قالب را انتخاب کنید.")
            values = {"body": letter.template_id.body_html}
            if letter.template_id.subject_pattern and not letter.subject:
                values["subject"] = letter.template_id.subject_pattern
            letter.write(values)
        return True

    def _store_official_pdf(self, pdf):
        self.ensure_one()
        digest = hashlib.sha256(pdf).hexdigest()
        if self.official_pdf_sha256 == digest and self.official_pdf_attachment_id:
            return self.official_pdf_attachment_id
        filename = f"letter-{self.number}.pdf"
        attachment = self.env["ir.attachment"].sudo().create({
            "name": filename, "datas": base64.b64encode(pdf), "mimetype": "application/pdf",
            "res_model": self._name, "res_id": self.id, "company_id": self.company_id.id,
        })
        document = self.document_id
        if not document:
            document = self.env["cas.document"].create({
                "name": self.subject, "company_id": self.company_id.id, "folder_id": self._advanced_folder().id,
                "owner_user_id": self.sender_user_id.id, "authorized_user_ids": [(6, 0, self.authorized_user_ids.ids)],
                "confidentiality": self.confidentiality,
            })
            self.env["cas.document.link"].create({
                "document_id": document.id, "source_model": self._name, "source_record_id": self.id,
                "source_title": self.subject, "relation_type": "primary",
            })
        document.add_version(filename, pdf, "application/pdf", _("نسخه رسمی نامه %s", self.number))
        self.with_context(cas_correspondence_engine=True).write({
            "document_id": document.id, "official_pdf_attachment_id": attachment.id,
            "official_pdf_sha256": digest, "official_pdf_generated_at": fields.Datetime.now(),
        })
        self._audit("official_pdf_generated", payload={"sha256": digest})
        return attachment

    def action_generate_official_pdf(self):
        for letter in self:
            if letter.state == "draft" or not letter.number:
                raise ValidationError("PDF رسمی پس از ثبت و شماره‌گذاری نامه تولید می‌شود.")
            pdf, _ = self.env["ir.actions.report"]._render_qweb_pdf(
                "cas_correspondence_advanced.action_report_correspondence_letter", res_ids=letter.ids
            )
            letter._store_official_pdf(pdf)
        return True

    def action_download_official_pdf(self):
        self.ensure_one()
        if not self.official_pdf_attachment_id:
            self.action_generate_official_pdf()
        return {"type": "ir.actions.act_url", "url": f"/web/content/{self.official_pdf_attachment_id.id}?download=1", "target": "self"}

    def action_send(self):
        result = super().action_send()
        self.action_generate_official_pdf()
        self.env["cas.correspondence.signature"].with_context(cas_correspondence_advanced_engine=True).create({
            "letter_id": self.id, "signer_user_id": self.signed_by_user_id.id, "method": "organizational",
            "state": "signed", "source_digest": self.official_pdf_sha256, "signed_at": self.signed_at,
        })
        return result
