from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CasAttendanceSite(models.Model):
    _name = "cas.attendance.site"
    _description = "CAS Attendance Site"
    _inherit = ["mail.thread"]
    _order = "company_id, name"

    name = fields.Char(string="ساختمان / محل", required=True, tracking=True)
    code = fields.Char(string="کد", required=True, index=True)
    company_id = fields.Many2one("res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True)
    active = fields.Boolean(default=True, tracking=True)

    _code_company_uniq = models.Constraint("UNIQUE(code, company_id)", "کد محل در هر شرکت باید یکتا باشد.")


class CasAttendanceDevice(models.Model):
    _name = "cas.attendance.device"
    _description = "CAS Attendance Device"
    _inherit = ["mail.thread"]
    _order = "company_id, name"

    name = fields.Char(string="نام دستگاه", required=True, tracking=True)
    code = fields.Char(string="شناسه دستگاه", required=True, index=True)
    company_id = fields.Many2one("res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True)
    site_id = fields.Many2one("cas.attendance.site", string="محل", required=True, ondelete="restrict", index=True)
    active = fields.Boolean(default=True, tracking=True)
    note = fields.Text(string="توضیحات")

    _code_company_uniq = models.Constraint("UNIQUE(code, company_id)", "شناسه دستگاه در هر شرکت باید یکتا باشد.")


class CasAttendanceOutage(models.Model):
    _name = "cas.attendance.outage"
    _description = "CAS Attendance Device Outage"
    _inherit = ["mail.thread"]
    _order = "start_at desc, id desc"

    name = fields.Char(string="عنوان خرابی", required=True, tracking=True)
    company_id = fields.Many2one("res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True)
    device_id = fields.Many2one("cas.attendance.device", string="دستگاه", ondelete="restrict", index=True, tracking=True)
    site_id = fields.Many2one("cas.attendance.site", string="محل", required=True, ondelete="restrict", index=True, tracking=True)
    start_at = fields.Datetime(string="شروع خرابی", required=True, index=True, tracking=True)
    end_at = fields.Datetime(string="پایان خرابی", index=True, tracking=True)
    state = fields.Selection([("open", "در حال خرابی"), ("recovered", "رفع شده")], string="وضعیت", required=True, default="open", tracking=True)
    reason = fields.Text(string="شرح خرابی", required=True)
    reporter_id = fields.Many2one("res.users", string="گزارش‌دهنده", required=True, default=lambda self: self.env.user, readonly=True)

    @api.constrains("start_at", "end_at", "state")
    def _check_dates(self):
        for rec in self:
            if rec.end_at and rec.end_at <= rec.start_at:
                raise ValidationError(_("پایان خرابی باید بعد از شروع آن باشد."))
            if rec.state == "recovered" and not rec.end_at:
                raise ValidationError(_("برای خرابی رفع‌شده، زمان پایان الزامی است."))

    def action_recover(self):
        self.write({"state": "recovered", "end_at": fields.Datetime.now()})

