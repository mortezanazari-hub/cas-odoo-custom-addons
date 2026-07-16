from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CasOfficialHoliday(models.Model):
    _name = "cas.official.holiday"
    _description = "CAS Official Holiday"
    _inherit = ["mail.thread"]
    _order = "date desc, id desc"

    name = fields.Char(string="عنوان تعطیل", required=True, tracking=True)
    date = fields.Date(string="تاریخ", required=True, index=True, tracking=True)
    company_id = fields.Many2one(
        "res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True
    )
    active = fields.Boolean(default=True, tracking=True)
    note = fields.Text(string="توضیحات")

    _date_company_uniq = models.Constraint(
        "UNIQUE(date, company_id)", "برای هر شرکت در هر تاریخ فقط یک تعطیل رسمی قابل تعریف است."
    )


class CasShiftDay(models.Model):
    _name = "cas.shift.day"
    _description = "CAS Effective Daily Schedule"
    _inherit = ["mail.thread"]
    _order = "schedule_date desc, employee_id, id"

    assignment_id = fields.Many2one(
        "cas.shift.assignment", string="انتساب مبدأ", required=True, ondelete="restrict", index=True
    )
    company_id = fields.Many2one("res.company", string="شرکت", required=True, index=True)
    employee_id = fields.Many2one("hr.employee", string="کارمند", required=True, ondelete="restrict", index=True)
    department_id = fields.Many2one(related="employee_id.department_id", store=True, index=True)
    schedule_date = fields.Date(string="تاریخ واقعی", required=True, index=True)
    rule_origin_date = fields.Date(string="مبدأ قانون روز", required=True, index=True)
    policy_id = fields.Many2one("cas.attendance.policy", string="سیاست حضور", required=True, ondelete="restrict", index=True)
    attendance_mode = fields.Selection(
        [("simple", "ساده"), ("advanced", "پیشرفته")], string="حالت حضور", required=True, readonly=True, index=True
    )
    source_tolerance_minutes = fields.Integer(string="حد تطبیق منابع", required=True, readonly=True)
    template_id = fields.Many2one("cas.shift.template", string="شیفت مؤثر", ondelete="restrict", index=True)
    day_kind = fields.Selection(
        [("work", "کاری"), ("off_cycle", "تعطیل چرخه"), ("off_weekly", "تعطیل هفتگی"),
         ("off_official", "تعطیل رسمی")],
        string="نوع روز مؤثر", required=True, readonly=True, index=True,
    )
    planned_start = fields.Datetime(string="شروع برنامه", index=True, readonly=True)
    planned_end = fields.Datetime(string="پایان برنامه", index=True, readonly=True)
    base_work_minutes = fields.Integer(string="موظفی", readonly=True)
    break_minutes = fields.Integer(string="استراحت", readonly=True)
    required_presence_minutes = fields.Integer(string="حضور الزامی", readonly=True)
    mandatory_overtime_minutes = fields.Integer(string="اضافه‌کاری اجباری برنامه", readonly=True)
    calendar_date_is_official_holiday = fields.Boolean(string="تاریخ واقعی تعطیل رسمی است", readonly=True)
    rule_is_official_holiday = fields.Boolean(string="قانون منتقل‌شده تعطیل رسمی", readonly=True)
    rule_is_weekly_rest = fields.Boolean(string="قانون منتقل‌شده تعطیل هفتگی", readonly=True)
    rule_is_short_day = fields.Boolean(string="قانون منتقل‌شده روز کوتاه", readonly=True)
    swapped_by_id = fields.Many2one("cas.shift.swap", string="آخرین جابه‌جایی", readonly=True, index=True)
    state = fields.Selection(
        [("planned", "برنامه‌ریزی‌شده"), ("cancelled", "لغوشده")],
        string="وضعیت", required=True, default="planned", readonly=True, index=True,
    )

    _employee_date_uniq = models.Constraint(
        "UNIQUE(employee_id, schedule_date)", "برای هر کارمند در هر تاریخ فقط یک برنامه مؤثر مجاز است."
    )

    @api.model_create_multi
    def create(self, vals_list):
        if not (self.env.is_superuser() or self.env.context.get("cas_shift_engine")):
            raise AccessError(_("برنامه روزانه فقط از انتشار رسمی ساخته می‌شود."))
        return super().create(vals_list)

    def write(self, vals):
        structural = set(self._fields) - {"message_follower_ids", "message_partner_ids", "message_ids", "activity_ids"}
        if structural.intersection(vals) and not self.env.context.get("cas_shift_engine"):
            raise ValidationError(_("برنامه مؤثر فقط از عملیات رسمی قابل تغییر است."))
        return super().write(vals)

    def unlink(self):
        raise ValidationError(_("برنامه روزانه و سابقه آن قابل حذف نیست."))

    @api.constrains(
        "day_kind", "template_id", "planned_start", "planned_end", "base_work_minutes",
        "break_minutes", "required_presence_minutes", "mandatory_overtime_minutes",
    )
    def _check_contract(self):
        for day in self:
            values = [day.base_work_minutes, day.break_minutes, day.required_presence_minutes, day.mandatory_overtime_minutes]
            if any(value < 0 or value > 1440 for value in values):
                raise ValidationError(_("مقادیر برنامه روزانه معتبر نیستند."))
            if day.day_kind == "work":
                if not day.template_id or not day.planned_start or not day.planned_end:
                    raise ValidationError(_("روز کاری باید شیفت و زمان شروع و پایان داشته باشد."))
                if day.planned_end <= day.planned_start:
                    raise ValidationError(_("پایان برنامه باید بعد از شروع باشد."))
            elif day.template_id or day.planned_start or day.planned_end or day.base_work_minutes:
                raise ValidationError(_("روز تعطیل نباید برنامه کاری یا موظفی داشته باشد."))

    def _snapshot(self):
        self.ensure_one()
        return {
            "template_id": self.template_id.id, "day_kind": self.day_kind,
            "base_work_minutes": self.base_work_minutes, "break_minutes": self.break_minutes,
            "required_presence_minutes": self.required_presence_minutes,
            "mandatory_overtime_minutes": self.mandatory_overtime_minutes,
            "rule_is_official_holiday": self.rule_is_official_holiday,
            "rule_is_weekly_rest": self.rule_is_weekly_rest,
            "rule_is_short_day": self.rule_is_short_day,
            "rule_origin_date": self.rule_origin_date,
        }

    def _values_from_snapshot(self, snapshot, target_date, swap):
        self.ensure_one()
        template = self.env["cas.shift.template"].browse(snapshot["template_id"])
        values = dict(snapshot)
        values["swapped_by_id"] = swap.id
        if snapshot["day_kind"] == "work":
            values["planned_start"] = self.assignment_id._local_datetime(template, target_date, template.start_hour)
            end_date = target_date + timedelta(days=1 if template.crosses_midnight else 0)
            values["planned_end"] = self.assignment_id._local_datetime(template, end_date, template.end_hour)
        else:
            values.update({"template_id": False, "planned_start": False, "planned_end": False})
        return values
