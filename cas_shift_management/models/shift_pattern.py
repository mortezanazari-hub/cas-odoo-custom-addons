from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CasShiftPattern(models.Model):
    _name = "cas.shift.pattern"
    _description = "CAS Shift Pattern"
    _inherit = ["mail.thread"]
    _order = "company_id, name, id"

    name = fields.Char(string="عنوان الگو", required=True, tracking=True)
    code = fields.Char(string="کد", required=True, index=True)
    company_id = fields.Many2one(
        "res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True
    )
    cycle_length = fields.Integer(string="طول چرخه (روز)", required=True, default=7, tracking=True)
    line_ids = fields.One2many("cas.shift.pattern.line", "pattern_id", string="روزهای چرخه", copy=True)
    active = fields.Boolean(default=True, tracking=True)

    _code_company_uniq = models.Constraint(
        "UNIQUE(code, company_id)", "کد الگو در هر شرکت باید یکتا باشد."
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
        if {"cycle_length", "line_ids"}.intersection(vals):
            published = self.env["cas.shift.assignment"].sudo().search_count([
                ("pattern_id", "in", self.ids), ("state", "in", ["published", "closed"])
            ], limit=1)
            if published:
                raise ValidationError(_("الگوی استفاده‌شده در برنامه منتشرشده قابل تغییر نیست؛ الگوی جدید بسازید."))
        return super().write(vals)

    @api.constrains("cycle_length", "line_ids")
    def _check_cycle(self):
        for pattern in self:
            if not 1 <= pattern.cycle_length <= 60:
                raise ValidationError(_("طول چرخه باید بین ۱ و ۶۰ روز باشد."))
            indexes = pattern.line_ids.mapped("cycle_day")
            if len(indexes) != len(set(indexes)) or any(index < 1 or index > pattern.cycle_length for index in indexes):
                raise ValidationError(_("شماره روزهای چرخه باید یکتا و داخل طول چرخه باشد."))


class CasShiftPatternLine(models.Model):
    _name = "cas.shift.pattern.line"
    _description = "CAS Shift Pattern Day"
    _order = "pattern_id, cycle_day, id"

    pattern_id = fields.Many2one("cas.shift.pattern", required=True, ondelete="cascade", index=True)
    company_id = fields.Many2one(related="pattern_id.company_id", store=True, index=True)
    cycle_day = fields.Integer(string="روز چرخه", required=True)
    day_kind = fields.Selection(
        [("work", "کاری"), ("off", "تعطیل چرخه")], string="نوع روز", required=True, default="work"
    )
    template_id = fields.Many2one("cas.shift.template", string="شیفت", ondelete="restrict")

    _pattern_day_uniq = models.Constraint(
        "UNIQUE(pattern_id, cycle_day)", "هر روز چرخه فقط یک‌بار قابل تعریف است."
    )

    def write(self, vals):
        published = self.env["cas.shift.assignment"].sudo().search_count([
            ("pattern_id", "in", self.mapped("pattern_id").ids),
            ("state", "in", ["published", "closed"]),
        ], limit=1)
        if published:
            raise ValidationError(_("روزهای الگوی استفاده‌شده در برنامه منتشرشده قابل تغییر نیستند."))
        return super().write(vals)

    def unlink(self):
        published = self.env["cas.shift.assignment"].sudo().search_count([
            ("pattern_id", "in", self.mapped("pattern_id").ids),
            ("state", "in", ["published", "closed"]),
        ], limit=1)
        if published:
            raise ValidationError(_("روزهای الگوی استفاده‌شده در برنامه منتشرشده قابل حذف نیستند."))
        return super().unlink()

    @api.constrains("day_kind", "template_id", "pattern_id")
    def _check_line(self):
        for line in self:
            if line.day_kind == "work" and not line.template_id:
                raise ValidationError(_("برای روز کاری باید شیفت انتخاب شود."))
            if line.day_kind == "off" and line.template_id:
                raise ValidationError(_("روز تعطیل چرخه نباید شیفت داشته باشد."))
            if line.template_id and line.template_id.company_id != line.pattern_id.company_id:
                raise ValidationError(_("الگو و شیفت باید متعلق به یک شرکت باشند."))
