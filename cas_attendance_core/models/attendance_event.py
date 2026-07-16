from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


EVENT_KINDS = [
    ("guard_entry", "ورود اولیه نگهبانی"), ("guard_exit", "خروج نهایی نگهبانی"),
    ("work_start", "شروع کار دستگاه"), ("work_end", "پایان کار دستگاه"),
    ("break_start", "شروع استراحت"), ("break_end", "پایان استراحت"),
    ("temporary_exit", "خروج موقت شخصی"), ("temporary_return", "بازگشت خروج موقت"),
    ("mission_exit", "خروج مأموریت"), ("mission_return", "بازگشت مأموریت"),
    ("leave_exit", "خروج مرخصی ساعتی"), ("leave_return", "بازگشت مرخصی ساعتی"),
    ("unknown_entry", "ورود نامشخص"), ("unknown_exit", "خروج نامشخص"),
]

ENTRY_KINDS = {"guard_entry", "work_start", "break_end", "temporary_return", "mission_return", "leave_return", "unknown_entry"}
EXIT_KINDS = {"guard_exit", "work_end", "break_start", "temporary_exit", "mission_exit", "leave_exit", "unknown_exit"}


class CasAttendanceEvent(models.Model):
    _name = "cas.attendance.event"
    _description = "CAS Immutable Attendance Event"
    _inherit = ["mail.thread"]
    _order = "occurred_at desc, id desc"

    employee_id = fields.Many2one("hr.employee", string="کارمند", required=True, ondelete="restrict", index=True)
    company_id = fields.Many2one(related="employee_id.company_id", string="شرکت", store=True, index=True)
    occurred_at = fields.Datetime(string="زمان واقعی رخداد", required=True, index=True, readonly=True)
    registered_at = fields.Datetime(string="زمان ثبت در سامانه", required=True, default=fields.Datetime.now, readonly=True)
    source = fields.Selection([("guard", "نگهبانی"), ("device", "دستگاه"), ("manual", "ثبت اصلاحی سرپرست"), ("import", "ورودی سامانه")], string="منبع", required=True, index=True, readonly=True)
    event_kind = fields.Selection(EVENT_KINDS, string="نوع تردد", required=True, index=True, readonly=True)
    direction = fields.Selection([("in", "ورود"), ("out", "خروج")], string="جهت", compute="_compute_direction", store=True, index=True)
    site_id = fields.Many2one("cas.attendance.site", string="محل", ondelete="restrict", index=True, readonly=True)
    device_id = fields.Many2one("cas.attendance.device", string="دستگاه", ondelete="restrict", index=True, readonly=True)
    work_date = fields.Date(string="روز کاری منتسب", required=True, index=True, readonly=True)
    attribution_method = fields.Selection([("automatic", "خودکار از برنامه"), ("guard", "انتخاب نگهبان"), ("supervisor", "اصلاح سرپرست"), ("import", "ورودی سامانه")], string="روش انتساب روز", required=True, readonly=True)
    external_uid = fields.Char(string="شناسه یکتای منبع", index=True, readonly=True)
    note = fields.Text(string="توضیحات", readonly=True)
    is_void = fields.Boolean(string="باطل شده", default=False, readonly=True, index=True)
    voided_at = fields.Datetime(string="زمان ابطال", readonly=True)
    voided_by_id = fields.Many2one("res.users", string="ابطال‌کننده", readonly=True)
    void_reason = fields.Text(string="علت ابطال")
    replacement_event_id = fields.Many2one("cas.attendance.event", string="رکورد جایگزین", readonly=True, ondelete="restrict")

    _source_uid_uniq = models.Constraint("UNIQUE(source, external_uid, company_id)", "این رخداد قبلاً از منبع دریافت شده است.")

    @api.depends("event_kind")
    def _compute_direction(self):
        for rec in self:
            rec.direction = "in" if rec.event_kind in ENTRY_KINDS else "out"

    @api.model
    def _minute(self, value):
        value = fields.Datetime.to_datetime(value)
        return value.replace(second=0, microsecond=0)

    @api.model
    def _resolve_work_date(self, employee, occurred_at):
        start = occurred_at - timedelta(hours=18)
        end = occurred_at + timedelta(hours=18)
        days = self.env["cas.shift.day"].search([
            ("employee_id", "=", employee.id), ("state", "=", "planned"),
            ("planned_start", "<=", end), ("planned_end", ">=", start),
        ])
        containing = days.filtered(lambda d: d.planned_start <= occurred_at <= d.planned_end)
        day = containing[:1] or days.sorted(key=lambda d: abs((d.planned_start - occurred_at).total_seconds()))[:1]
        return day.schedule_date if day else occurred_at.date()

    @api.model_create_multi
    def create(self, vals_list):
        prepared = []
        for incoming in vals_list:
            vals = dict(incoming)
            occurred = self._minute(vals.get("occurred_at"))
            vals["occurred_at"] = occurred
            vals["registered_at"] = self._minute(vals.get("registered_at") or fields.Datetime.now())
            employee = self.env["hr.employee"].browse(vals["employee_id"])
            explicit_date = vals.get("work_date")
            if explicit_date:
                day = self.env["cas.shift.day"].search([("employee_id", "=", employee.id), ("schedule_date", "=", explicit_date)], limit=1)
                allowed = bool(day and day.policy_id.allow_guard_work_date_choice)
                if vals.get("source") == "guard" and not allowed and not self.env.context.get("cas_attendance_supervisor"):
                    raise ValidationError(_("انتخاب دستی روز کاری برای سیاست این کارمند مجاز نیست."))
                vals["attribution_method"] = vals.get("attribution_method") or ("guard" if vals.get("source") == "guard" else "import")
            else:
                vals["work_date"] = self._resolve_work_date(employee, occurred)
                vals["attribution_method"] = "automatic"
            prepared.append(vals)
        records = super().create(prepared)
        records._recompute_days()
        return records

    def write(self, vals):
        allowed = {"is_void", "voided_at", "voided_by_id", "void_reason", "replacement_event_id"}
        reason_only = set(vals) <= {"void_reason"} and not self.filtered("is_void")
        if set(vals) - allowed or (not reason_only and not self.env.context.get("cas_attendance_void")):
            raise AccessError(_("رخداد خام قابل ویرایش نیست؛ آن را با ذکر علت باطل و رکورد صحیح را ثبت کنید."))
        result = super().write(vals)
        self._recompute_days()
        return result

    def unlink(self):
        raise AccessError(_("رخداد خام حضور و غیاب قابل حذف نیست."))

    def action_void(self):
        for rec in self:
            if rec.is_void:
                continue
            if not rec.void_reason:
                raise ValidationError(_("پیش از ابطال، علت ابطال را ثبت کنید."))
            rec.with_context(cas_attendance_void=True).write({"is_void": True, "voided_at": fields.Datetime.now(), "voided_by_id": self.env.user.id})

    def _recompute_days(self):
        for employee, work_date in {(r.employee_id, r.work_date) for r in self}:
            day = self.env["cas.attendance.day"].sudo()._get_or_create(employee, work_date)
            day.recompute()
