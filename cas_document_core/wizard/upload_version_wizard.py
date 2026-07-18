import base64

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class CasDocumentUploadVersionWizard(models.TransientModel):
    _name = "cas.document.upload.version.wizard"
    _description = "CAS Upload Document Version"

    document_id = fields.Many2one("cas.document", string="سند", required=True, readonly=True)
    file_data = fields.Binary(string="فایل", required=True, attachment=False)
    filename = fields.Char(string="نام فایل", required=True)
    note = fields.Text(string="شرح نسخه")

    def action_confirm(self):
        self.ensure_one()
        if not self.file_data:
            raise ValidationError(_("انتخاب فایل الزامی است."))
        self.document_id.add_version(self.filename, base64.b64decode(self.file_data), note=self.note)
        return {"type": "ir.actions.act_window_close"}
