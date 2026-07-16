from datetime import datetime, time, timedelta

import pytz

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


WEEKDAY_SELECTION = [
    ("none", "بدون تعطیل هفتگی ثابت"), ("0", "دوشنبه"), ("1", "سه‌شنبه"),
    ("2", "چهارشنبه"), ("3", "پنجشنبه"), ("4", "جمعه"),
    ("5", "شنبه"), ("6", "یکشنبه"),
]


class CasShiftAssignment(models.Model):
    _name = "cas.shift.assignment"
    _description = "CAS Effective-Dated Shift Assignment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_from desc, id desc"
    _rec_name = "number"

    number = fields.Char(string="شماره انتساب", default="New", readonly=True, copy=False, index=True)
    name = fields.Char(string="عنوان انتساب", required=True, tracking=True)
    company_id = fields.Many2one(
        "res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True
    )
    employee_ids = fields.Many2many(
        "hr.employee", "cas_shift_assignment_employee_rel", "assignment_id", "employee_id",
        string="کارکنان", required=True,
    )
    department_id = fields.Many2one("hr.department", string="واحد برنامه‌ریز", ondelete="restrict", index=True)
    supervisor_user_id = fields.Many2one(
        "res.users", string="مسئول برنامه", required=True, ondelete="restrict", index=True,
        domain="[('active', '=', True), ('share', '=', False)]",
    )
    policy_id = fields.Many2one(
        "cas.attendance.policy", string="سیاست حضور و غیاب", required=True, ondelete="restrict", tracking=True
    )
    pattern_id = fields.Many2one(
        "cas.shift.pattern", string="الگوی شیفت", required=True, ondelete="restrict", tracking=True
    )
    anchor_date = fields.Date(
        string="روز اول چرخه", required=True,
        help="این تاریخ روز شماره یک الگوی گردشی است.",
    )
    date_from = fields.Date(string="از تاریخ", required=True, index=True, tracking=True)
    date_to = fields.Date(string="تا تاریخ", required=True, index=True, tracking=True)
    weekly_rest_day = fields.Selection(
        WEEKDAY_SELECTION, string="تعطیل هفتگی قراردادی", required=True, default="4", tracking=True
    )
    roster_respects_weekly_rest = fields.Boolean(
        string="تعطیل هفتگی نوبت را تعطیل می‌کند", default=True,
        help="برای نگهبانان خاموش است؛ نوبت گردشی حتی در جمعه یا شنبه ادامه دارد.",
    )
    short_day_enabled = fields.Boolean(string="روز قبل از تعطیل، کوتاه است", default=True)
    short_day_template_id = fields.Many2one(
        "cas.shift.template", string="شیفت مخصوص روز کوتاه", ondelete="restrict",
        help="اگر خالی باشد همان شیفت چرخه حفظ می‌شود و فقط موظفی روز کوتاه اعمال می‌شود.",
    )
    roster_respects_official_holiday = fields.Boolean(
        string="تعطیل رسمی نوبت را تعطیل می‌کند", default=True
    )
    state = fields.Selection(
        [("draft", "پیش‌نویس"), ("published", "منتشرشده"), ("closed", "بسته‌شده"), ("cancelled", "لغوشده")],
        default="draft", required=True, readonly=True, tracking=True, index=True,
    )
    published_at = fields.Datetime(string="زمان انتشار", readonly=True)
    published_by_id = fields.Many2one("res.users", string="منتشرکننده", readonly=True)
    day_ids = fields.One2many("cas.shift.day", "assignment_id", string="برنامه‌های روزانه", copy=False)
    day_count = fields.Integer(compute="_compute_day_count")
    note = fields.Text(string="توضیحات")

    _number_uniq = models.Constraint("UNIQUE(number)", "شماره انتساب باید یکتا باشد.")

    @api.depends("day_ids")
    def _compute_day_count(self):
        for assignment in self:
            assignment.day_count = len(assignment.day_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["number"] = self.env["ir.sequence"].next_by_code("cas.shift.assignment") or "New"
            vals["state"] = "draft"
        return super().create(vals_list)

    def write(self, vals):
        protected = {
            "company_id", "employee_ids", "department_id", "supervisor_user_id", "policy_id",
            "pattern_id", "anchor_date", "date_from", "date_to", "weekly_rest_day",
            "roster_respects_weekly_rest", "short_day_enabled", "short_day_template_id",
            "roster_respects_official_holiday",
        }
        if protected.intersection(vals) and any(item.state != "draft" for item in self):
            raise ValidationError(_("ساختار انتساب منتشرشده قابل تغییر نیست؛ انتساب تاریخ‌دار جدید بسازید."))
        if "state" in vals and not self.env.context.get("cas_shift_engine"):
            raise ValidationError(_("وضعیت فقط از عملیات رسمی تغییر می‌کند."))
        return super().write(vals)

    def unlink(self):
        if any(item.state != "draft" or item.day_ids for item in self):
            raise ValidationError(_("انتساب منتشرشده یا دارای سابقه قابل حذف نیست."))
        return super().unlink()

    @api.constrains(
        "date_from", "date_to", "anchor_date", "employee_ids", "company_id", "policy_id",
        "pattern_id", "short_day_template_id", "supervisor_user_id",
    )
    def _check_contract(self):
        for item in self:
            if item.date_to < item.date_from:
                raise ValidationError(_("تاریخ پایان نمی‌تواند قبل از تاریخ شروع باشد."))
            if (item.date_to - item.date_from).days > 366:
                raise ValidationError(_("هر انتساب حداکثر ۳۶۷ روز را پوشش می‌دهد."))
            if not item.employee_ids:
                raise ValidationError(_("حداقل یک کارمند انتخاب کنید."))
            if item.policy_id.company_id != item.company_id or item.pattern_id.company_id != item.company_id:
                raise ValidationError(_("سیاست، الگو و انتساب باید متعلق به یک شرکت باشند."))
            if item.short_day_template_id and item.short_day_template_id.company_id != item.company_id:
                raise ValidationError(_("شیفت روز کوتاه خارج از شرکت انتساب است."))
            if any(employee.company_id != item.company_id for employee in item.employee_ids.sudo()):
                raise ValidationError(_("همه کارکنان باید متعلق به شرکت انتساب باشند."))
            supervisor = item.supervisor_user_id.with_context(active_test=False)
            if not supervisor.active or supervisor.share or item.company_id not in supervisor.company_ids:
                raise ValidationError(_("مسئول برنامه باید کاربر داخلی و فعال همان شرکت باشد."))
            if not item.pattern_id.line_ids:
                raise ValidationError(_("الگوی شیفت باید تمام روزهای چرخه را داشته باشد."))

    def _check_publish_access(self):
        if not (self.env.is_superuser() or self.env.user.has_group("cas_shift_management.group_cas_shift_planner")):
            raise AccessError(_("مجوز انتشار برنامه شیفت را ندارید."))

    @staticmethod
    def _local_datetime(template, schedule_date, hour_value):
        total_minutes = int(round(hour_value * 60))
        naive = datetime.combine(schedule_date, time((total_minutes // 60) % 24, total_minutes % 60))
        timezone = pytz.timezone(template.timezone)
        try:
            localized = timezone.localize(naive, is_dst=None)
        except pytz.NonExistentTimeError:
            localized = timezone.localize(naive + timedelta(hours=1), is_dst=True)
        except pytz.AmbiguousTimeError:
            localized = timezone.localize(naive, is_dst=False)
        return localized.astimezone(pytz.UTC).replace(tzinfo=None)

    def _pattern_line_for(self, schedule_date):
        self.ensure_one()
        cycle_day = ((schedule_date - self.anchor_date).days % self.pattern_id.cycle_length) + 1
        return self.pattern_id.line_ids.filtered(lambda line: line.cycle_day == cycle_day)[:1]

    def _day_values(self, employee, schedule_date, official_dates):
        self.ensure_one()
        line = self._pattern_line_for(schedule_date)
        if not line:
            raise ValidationError(_("روز متناظر در الگوی شیفت پیدا نشد."))
        policy = self.policy_id
        weekday = schedule_date.weekday()
        rest_weekday = int(self.weekly_rest_day) if self.weekly_rest_day != "none" else None
        weekly_rule = rest_weekday is not None and weekday == rest_weekday
        short_rule = (
            self.short_day_enabled and rest_weekday is not None
            and weekday == ((rest_weekday - 1) % 7)
        )
        official_rule = schedule_date in official_dates
        day_kind = line.day_kind
        if day_kind == "off":
            day_kind = "off_cycle"
        elif weekly_rule and self.roster_respects_weekly_rest:
            day_kind = "off_weekly"
        elif official_rule and self.roster_respects_official_holiday:
            day_kind = "off_official"
        else:
            day_kind = "work"

        template = line.template_id
        if day_kind == "work" and short_rule and self.short_day_template_id:
            template = self.short_day_template_id
        base_minutes = policy.short_work_minutes if short_rule else policy.normal_work_minutes
        if day_kind != "work":
            template = self.env["cas.shift.template"]
            base_minutes = 0
            break_minutes = 0
            presence_minutes = 0
            planned_start = planned_end = False
        else:
            presence_minutes = template.presence_minutes
            break_minutes = template.default_break_minutes
            if short_rule:
                break_minutes = 0 if presence_minutes <= base_minutes else policy.short_day_extended_break_minutes
            planned_start = self._local_datetime(template, schedule_date, template.start_hour)
            end_date = schedule_date + timedelta(days=1 if template.crosses_midnight else 0)
            planned_end = self._local_datetime(template, end_date, template.end_hour)
        net_planned = max(presence_minutes - break_minutes, 0)
        return {
            "assignment_id": self.id, "company_id": self.company_id.id,
            "employee_id": employee.id, "schedule_date": schedule_date,
            "policy_id": policy.id, "attendance_mode": policy.attendance_mode,
            "source_tolerance_minutes": policy.source_tolerance_minutes,
            "template_id": template.id, "day_kind": day_kind,
            "planned_start": planned_start, "planned_end": planned_end,
            "base_work_minutes": base_minutes, "break_minutes": break_minutes,
            "required_presence_minutes": presence_minutes,
            "mandatory_overtime_minutes": max(net_planned - base_minutes, 0) if template.shift_kind == "guard" else 0,
            "calendar_date_is_official_holiday": official_rule,
            "rule_is_official_holiday": official_rule,
            "rule_is_weekly_rest": weekly_rule,
            "rule_is_short_day": short_rule,
            "rule_origin_date": schedule_date,
        }

    def action_publish(self):
        for item in self:
            item._check_publish_access()
            if item.state != "draft":
                raise ValidationError(_("فقط انتساب پیش‌نویس قابل انتشار است."))
            indexes = set(item.pattern_id.line_ids.mapped("cycle_day"))
            if indexes != set(range(1, item.pattern_id.cycle_length + 1)):
                raise ValidationError(_("برای تمام روزهای چرخه باید دقیقاً یک سطر تعریف شود."))
            existing = self.env["cas.shift.day"].sudo().search_count([
                ("employee_id", "in", item.employee_ids.ids),
                ("schedule_date", ">=", item.date_from), ("schedule_date", "<=", item.date_to),
                ("state", "!=", "cancelled"),
            ], limit=1)
            if existing:
                raise ValidationError(_("برای حداقل یکی از کارکنان در این بازه برنامه روزانه موجود است."))
            holidays = self.env["cas.official.holiday"].sudo().search([
                ("company_id", "=", item.company_id.id),
                ("date", ">=", item.date_from), ("date", "<=", item.date_to),
                ("active", "=", True),
            ])
            official_dates = set(holidays.mapped("date"))
            values = []
            current = item.date_from
            while current <= item.date_to:
                for employee in item.employee_ids.sudo():
                    values.append(item._day_values(employee, current, official_dates))
                current += timedelta(days=1)
            self.env["cas.shift.day"].with_context(cas_shift_engine=True).sudo().create(values)
            item.with_context(cas_shift_engine=True).write({
                "state": "published", "published_at": fields.Datetime.now(), "published_by_id": self.env.user.id,
            })
        return True

    def action_close(self):
        for item in self:
            if item.state != "published":
                raise ValidationError(_("فقط انتساب منتشرشده قابل بستن است."))
            item.with_context(cas_shift_engine=True).write({"state": "closed"})
        return True

    def action_cancel(self):
        for item in self:
            if item.state not in {"draft", "published"}:
                raise ValidationError(_("این انتساب قابل لغو نیست."))
            item.day_ids.with_context(cas_shift_engine=True).write({"state": "cancelled"})
            item.with_context(cas_shift_engine=True).write({"state": "cancelled"})
        return True

    def action_open_days(self):
        self.ensure_one()
        action = self.env.ref("cas_shift_management.action_cas_shift_day").read()[0]
        action["domain"] = [("assignment_id", "=", self.id)]
        return action
