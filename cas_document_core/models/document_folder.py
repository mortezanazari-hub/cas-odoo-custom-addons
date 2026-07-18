from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


CONFIDENTIALITY = [
    ("normal", "عادی"),
    ("confidential", "محرمانه"),
    ("highly_confidential", "خیلی محرمانه"),
]


class CasDocumentFolder(models.Model):
    _name = "cas.document.folder"
    _description = "CAS Document Folder"
    _parent_name = "parent_id"
    _parent_store = True
    _order = "complete_name"
    _rec_name = "complete_name"

    name = fields.Char(string="عنوان", required=True)
    code = fields.Char(string="کد", required=True, index=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True
    )
    parent_id = fields.Many2one("cas.document.folder", string="پوشه بالادست", index=True, ondelete="restrict")
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many("cas.document.folder", "parent_id", string="زیرپوشه‌ها")
    complete_name = fields.Char(string="مسیر کامل", compute="_compute_complete_name", store=True, recursive=True)
    manager_user_id = fields.Many2one("res.users", string="مدیر پوشه", ondelete="restrict")
    confidentiality = fields.Selection(CONFIDENTIALITY, string="سطح محرمانگی", required=True, default="normal")
    document_ids = fields.One2many("cas.document", "folder_id", string="اسناد")

    _code_company_uniq = models.Constraint(
        "UNIQUE(code, company_id)", "کد پوشه باید در هر شرکت یکتا باشد."
    )

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for folder in self:
            folder.complete_name = f"{folder.parent_id.complete_name} / {folder.name}" if folder.parent_id else folder.name

    @api.constrains("parent_id", "company_id", "manager_user_id")
    def _check_contract(self):
        if self._has_cycle():
            raise ValidationError(_("ساختار پوشه نمی‌تواند حلقه داشته باشد."))
        for folder in self:
            if folder.parent_id and folder.parent_id.company_id != folder.company_id:
                raise ValidationError(_("پوشه بالادست باید متعلق به همان شرکت باشد."))
            if folder.manager_user_id and folder.company_id not in folder.manager_user_id.company_ids:
                raise ValidationError(_("مدیر پوشه باید عضو همان شرکت باشد."))
