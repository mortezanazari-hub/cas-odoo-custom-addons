import pytz

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CasShiftTemplate(models.Model):
    _name = "cas.shift.template"
    _description = "CAS Shift Template"
    _inherit = ["mail.thread"]
    _order = "sequence, name, id"

    sequence = fields.Integer(default=10)
    name = fields.Char(string="عنوان شیفت", required=True, tracking=True)
    code = fields.Char(string="کد", required=True, index=True)
    company_id = fields.Many2one(
        "res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True
    )
    shift_kind = fields.Selection(
        [("regular", "عادی"), ("guard", "نگهبانی"), ("flexible", "شناور")],
        string="نوع حضور", required=True, default="regular", tracking=True,
    )
    timezone = fields.Selection(
        selection=lambda self: [(tz, tz) for tz in pytz.common_timezones],
        string="منطقه زمانی", required=True, default=lambda self: self.env.user.tz or "Asia/Tehran",
    )
    start_hour = fields.Float(string="ساعت شروع", required=True, default=7.5, tracking=True)
    end_hour = fields.Float(string="ساعت پایان", required=True, default=16.0, tracking=True)
    crosses_midnight = fields.Boolean(compute="_compute_duration", store=True)
    presence_minutes = fields.Integer(string="مدت حضور برنامه (دقیقه)", compute="_compute_duration", store=True)
    default_break_minutes = fields.Integer(string="استراحت پیش‌فرض", required=True, default=30)
    work_date_rule = fields.Selection(
        [("start", "روز شروع"), ("end", "روز پایان")],
        string="روز کاری پیش‌فرض", required=True, default="start",
    )
    manual_work_date_allowed = fields.Boolean(
        string="اجازه انتخاب روز کاری توسط نگهبان", default=False
    )
    active = fields.Boolean(default=True, tracking=True)

    _code_company_uniq = models.Constraint(
        "UNIQUE(code, company_id)", "کد شیفت در هر شرکت باید یکتا باشد."
    )

    @api.depends("start_hour", "end_hour")
    def _compute_duration(self):
        for template in self:
            start = int(round((template.start_hour or 0.0) * 60))
            end = int(round((template.end_hour or 0.0) * 60))
            duration = end - start
            crosses = duration <= 0
            if crosses:
                duration += 1440
            template.crosses_midnight = crosses
            template.presence_minutes = duration if 0 < duration <= 1440 else 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code"):
                vals["code"] = vals["code"].strip().lower()
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("code"):
            vals["code"] = vals["code"].strip().lower()
        structural = {
            "shift_kind", "timezone", "start_hour", "end_hour", "default_break_minutes",
            "work_date_rule", "manual_work_date_allowed",
        }
        if structural.intersection(vals):
            published = self.env["cas.shift.day"].sudo().search_count([
                ("template_id", "in", self.ids), ("state", "=", "planned")
            ], limit=1)
            if published:
                raise ValidationError(_("شیفت استفاده‌شده در برنامه روزانه قابل تغییر نیست؛ شیفت جدید بسازید."))
        return super().write(vals)

    @api.constrains("start_hour", "end_hour", "default_break_minutes", "timezone")
    def _check_contract(self):
        for template in self:
            if not 0 <= template.start_hour < 24 or not 0 <= template.end_hour < 24:
                raise ValidationError(_("ساعت شروع و پایان باید بین صفر و کمتر از ۲۴ باشند."))
            if template.presence_minutes <= 0:
                raise ValidationError(_("مدت حضور شیفت معتبر نیست."))
            if not 0 <= template.default_break_minutes < template.presence_minutes:
                raise ValidationError(_("استراحت باید نامنفی و کمتر از مدت حضور باشد."))
            if template.timezone not in pytz.all_timezones_set:
                raise ValidationError(_("منطقه زمانی معتبر نیست."))
