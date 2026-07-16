from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CasAttendancePolicy(models.Model):
    _name = "cas.attendance.policy"
    _description = "CAS Attendance Policy"
    _inherit = ["mail.thread"]
    _order = "company_id, name, id"

    name = fields.Char(string="عنوان سیاست", required=True, tracking=True)
    code = fields.Char(string="کد", required=True, index=True)
    company_id = fields.Many2one(
        "res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True
    )
    attendance_mode = fields.Selection(
        [("simple", "ساده"), ("advanced", "پیشرفته")],
        string="حالت حضور و غیاب", required=True, default="simple", tracking=True,
    )
    source_tolerance_minutes = fields.Integer(
        string="حد تطبیق دستگاه و نگهبانی (دقیقه)", required=True, default=5
    )
    normal_work_minutes = fields.Integer(string="موظفی روز عادی", required=True, default=480)
    normal_break_minutes = fields.Integer(string="استراحت روز عادی", required=True, default=30)
    short_work_minutes = fields.Integer(string="موظفی روز کوتاه", required=True, default=330)
    short_day_extended_break_minutes = fields.Integer(
        string="استراحت در صورت ادامه کار روز کوتاه", required=True, default=30,
        help="اگر فرد در پایان برنامه کوتاه نرود و کار را ادامه دهد، این مقدار از حضور کسر می‌شود.",
    )
    allow_guard_work_date_choice = fields.Boolean(
        string="اجازه انتخاب روز کاری توسط نگهبان", default=False,
        help="زمان واقعی رخداد تغییر نمی‌کند؛ فقط انتساب روز کاری قابل انتخاب می‌شود.",
    )
    auto_close_mixed_sources = fields.Boolean(
        string="بستن ساده با ترکیب منابع", default=True,
        help="ورود از یک منبع و خروج از منبع دیگر می‌تواند روز ساده را با هشدار ببندد.",
    )
    active = fields.Boolean(default=True, tracking=True)

    _code_company_uniq = models.Constraint(
        "UNIQUE(code, company_id)", "کد سیاست در هر شرکت باید یکتا باشد."
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code"):
                vals["code"] = vals["code"].strip().lower()
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("code"):
            vals["code"] = vals["code"].strip().lower()
        return super().write(vals)

    @api.constrains(
        "source_tolerance_minutes", "normal_work_minutes", "normal_break_minutes",
        "short_work_minutes", "short_day_extended_break_minutes",
    )
    def _check_minutes(self):
        for policy in self:
            if not 0 <= policy.source_tolerance_minutes <= 120:
                raise ValidationError(_("حد تطبیق منابع باید بین صفر و ۱۲۰ دقیقه باشد."))
            values = [
                policy.normal_work_minutes, policy.normal_break_minutes,
                policy.short_work_minutes, policy.short_day_extended_break_minutes,
            ]
            if any(value < 0 or value > 1440 for value in values):
                raise ValidationError(_("مقادیر زمانی سیاست باید بین صفر و ۱۴۴۰ دقیقه باشند."))
            if not policy.normal_work_minutes or not policy.short_work_minutes:
                raise ValidationError(_("موظفی روز عادی و روز کوتاه باید مثبت باشد."))
