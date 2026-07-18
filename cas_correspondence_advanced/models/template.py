from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CasCorrespondenceTemplate(models.Model):
    _name = "cas.correspondence.template"
    _description = "CAS Official Correspondence Template"
    _order = "company_id, sequence, name"

    sequence = fields.Integer(default=10)
    name = fields.Char(string="عنوان", required=True)
    code = fields.Char(string="کد", required=True, index=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one("res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True)
    subject_pattern = fields.Char(string="الگوی موضوع")
    header_html = fields.Html(string="سربرگ", sanitize=True)
    body_html = fields.Html(string="متن پایه", required=True, sanitize=True)
    footer_html = fields.Html(string="پابرگ", sanitize=True)
    document_folder_id = fields.Many2one("cas.document.folder", string="پوشه اسناد", ondelete="restrict")

    _code_company_uniq = models.Constraint(
        "UNIQUE(code, company_id)", "کد قالب در هر شرکت باید یکتا باشد."
    )

    @api.constrains("company_id", "document_folder_id")
    def _check_company(self):
        for template in self:
            if template.document_folder_id and template.document_folder_id.company_id != template.company_id:
                raise ValidationError("پوشه اسناد و قالب باید متعلق به یک شرکت باشند.")
