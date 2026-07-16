from odoo import api, fields, models


class CasAttendanceIdentity(models.Model):
    _name = "cas.attendance.identity"
    _description = "CAS External Attendance Identity"
    _inherit = ["mail.thread"]
    _order = "source_type, external_key"

    source_type = fields.Selection([("device", "دستگاه"), ("guard", "گزارش نگهبانی")], string="منبع شناسه", required=True, index=True)
    external_key = fields.Char(string="شناسه خارجی / نام شیت", required=True, index=True, tracking=True)
    employee_id = fields.Many2one("hr.employee", string="کارمند", required=True, ondelete="restrict", index=True, tracking=True)
    company_id = fields.Many2one(related="employee_id.company_id", store=True, index=True)
    active = fields.Boolean(default=True, tracking=True)
    note = fields.Text(string="توضیحات")

    _key_company_uniq = models.Constraint("UNIQUE(source_type, external_key, company_id)", "این شناسه خارجی قبلاً برای شرکت تعریف شده است.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["external_key"] = str(vals.get("external_key") or "").strip()
        return super().create(vals_list)

    def write(self, vals):
        if "external_key" in vals:
            vals["external_key"] = str(vals["external_key"] or "").strip()
        return super().write(vals)

    @api.model
    def employee_for(self, source_type, external_key, company):
        key = str(external_key or "").strip()
        identity = self.sudo().search([
            ("source_type", "=", source_type), ("external_key", "=", key),
            ("company_id", "=", company.id), ("active", "=", True),
        ], limit=1)
        return identity.employee_id

