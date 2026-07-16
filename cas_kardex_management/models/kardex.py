from calendar import monthrange
from datetime import date, datetime, time, timedelta

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CasKardexPeriod(models.Model):
    _name = "cas.kardex.period"
    _description = "CAS Monthly Kardex Lock"
    _inherit = ["mail.thread", "cas.kardex.approval.mixin"]
    _order = "month_start desc, company_id"

    company_id = fields.Many2one("res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True)
    month_start = fields.Date(string="ماه", required=True, index=True, help="روز اول ماه میلادی متناظر در پایگاه داده")
    month_end = fields.Date(string="پایان ماه", compute="_compute_dates", store=True)
    lock_deadline = fields.Datetime(string="مهلت ویرایش", compute="_compute_dates", store=True)
    state = fields.Selection([("open", "باز"), ("locked", "قفل‌شده")], string="وضعیت", required=True, default="open", readonly=True, tracking=True)
    locked_at = fields.Datetime(readonly=True)
    locked_by_id = fields.Many2one("res.users", readonly=True)
    reopen_ids = fields.One2many("cas.kardex.reopen", "period_id", string="مجوزهای بازگشایی")

    _company_month_uniq = models.Constraint("UNIQUE(company_id, month_start)", "برای هر شرکت و ماه فقط یک دوره کاردکس مجاز است.")

    @api.depends("month_start", "company_id.cas_kardex_lock_day")
    def _compute_dates(self):
        for rec in self:
            if not rec.month_start:
                rec.month_end = rec.lock_deadline = False
                continue
            start = rec.month_start.replace(day=1)
            rec.month_end = start + relativedelta(months=1, days=-1)
            next_month = start + relativedelta(months=1)
            lock_day = rec.company_id.cas_kardex_lock_day or 4
            rec.lock_deadline = datetime.combine(next_month.replace(day=lock_day), time.max).replace(microsecond=0)

    @api.constrains("month_start")
    def _check_month(self):
        for rec in self:
            if rec.month_start and rec.month_start.day != 1:
                raise ValidationError(_("تاریخ دوره باید روز اول ماه باشد."))

    @api.model
    def period_for(self, company, work_date, create=True):
        start = work_date.replace(day=1)
        rec = self.sudo().search([("company_id", "=", company.id), ("month_start", "=", start)], limit=1)
        if not rec and create:
            rec = self.sudo().create({"company_id": company.id, "month_start": start})
        return rec

    def action_lock(self):
        for rec in self:
            if rec.state == "locked":
                continue
            rec.write({"state": "locked", "locked_at": fields.Datetime.now(), "locked_by_id": self.env.user.id})

    @api.model
    def _cron_lock_due_periods(self):
        now = fields.Datetime.now()
        periods = self.sudo().search([("state", "=", "open"), ("lock_deadline", "<", now)])
        periods.action_lock()
        return len(periods)

    def allows_edit(self, employee, work_date):
        self.ensure_one()
        if self.state == "open":
            return True
        return bool(self.reopen_ids.filtered(lambda r: r.active and r.date_from <= work_date <= r.date_to and (r.scope == "all" or employee in r.employee_ids)))


class CasKardexReopen(models.Model):
    _name = "cas.kardex.reopen"
    _description = "CAS Scoped Kardex Reopening"
    _inherit = ["mail.thread", "cas.kardex.approval.mixin"]
    _order = "create_date desc, id desc"

    period_id = fields.Many2one("cas.kardex.period", string="دوره قفل‌شده", required=True, ondelete="restrict", index=True)
    company_id = fields.Many2one(related="period_id.company_id", store=True, index=True)
    scope = fields.Selection([("all", "همه کارکنان شرکت"), ("employees", "کارکنان مشخص")], string="محدوده", required=True, default="employees")
    employee_ids = fields.Many2many("hr.employee", "cas_kardex_reopen_employee_rel", "reopen_id", "employee_id", string="کارکنان")
    date_from = fields.Date(string="از تاریخ", required=True)
    date_to = fields.Date(string="تا تاریخ", required=True)
    reason = fields.Text(string="دستور و دلیل مدیرعامل", required=True)
    active = fields.Boolean(default=True, readonly=True, tracking=True)
    opened_by_id = fields.Many2one("res.users", readonly=True)
    opened_at = fields.Datetime(readonly=True)
    closed_by_id = fields.Many2one("res.users", readonly=True)
    closed_at = fields.Datetime(readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            period = self.env["cas.kardex.period"].browse(vals["period_id"])
            self._cas_require_ceo(period.company_id)
            vals.update({"opened_by_id": self.env.user.id, "opened_at": fields.Datetime.now()})
        return super().create(vals_list)

    @api.constrains("period_id", "date_from", "date_to", "scope", "employee_ids")
    def _check_scope(self):
        for rec in self:
            if rec.period_id.state != "locked":
                raise ValidationError(_("بازگشایی فقط برای دوره قفل‌شده صادر می‌شود."))
            if rec.date_from < rec.period_id.month_start or rec.date_to > rec.period_id.month_end or rec.date_to < rec.date_from:
                raise ValidationError(_("بازه بازگشایی باید داخل همان ماه باشد."))
            if rec.scope == "employees" and not rec.employee_ids:
                raise ValidationError(_("برای بازگشایی محدود، انتخاب کارمند الزامی است."))

    def action_close(self):
        for rec in self:
            rec._cas_require_ceo(rec.company_id)
            rec.write({"active": False, "closed_by_id": self.env.user.id, "closed_at": fields.Datetime.now()})

    def unlink(self):
        raise ValidationError(_("سابقه بازگشایی قابل حذف نیست."))


class CasKardexDay(models.Model):
    _name = "cas.kardex.day"
    _description = "CAS Minute Accurate Daily Kardex"
    _inherit = ["mail.thread"]
    _order = "work_date desc, employee_id"

    employee_id = fields.Many2one("hr.employee", string="کارمند", required=True, ondelete="restrict", index=True)
    company_id = fields.Many2one(related="employee_id.company_id", store=True, index=True)
    work_date = fields.Date(string="روز کاردکس", required=True, index=True)
    attendance_day_id = fields.Many2one("cas.attendance.day", string="نتیجه حضور", required=True, ondelete="restrict", index=True)
    shift_day_id = fields.Many2one(related="attendance_day_id.shift_day_id", string="برنامه شیفت", store=True, readonly=True)
    period_id = fields.Many2one("cas.kardex.period", string="دوره", required=True, ondelete="restrict", index=True)
    day_kind = fields.Selection(related="shift_day_id.day_kind", string="نوع روز", store=True, readonly=True)
    planned_base_minutes = fields.Integer(string="موظفی برنامه", readonly=True)
    planned_break_minutes = fields.Integer(string="استراحت برنامه", readonly=True)
    planned_presence_minutes = fields.Integer(string="حضور برنامه", readonly=True)
    presence_minutes = fields.Integer(string="حضور واقعی", readonly=True)
    deducted_break_minutes = fields.Integer(string="استراحت کسرشده", readonly=True)
    net_work_minutes = fields.Integer(string="کار خالص واقعی", readonly=True)
    leave_minutes = fields.Integer(string="مرخصی تأییدشده", readonly=True)
    mission_minutes = fields.Integer(string="مأموریت تأییدشده", readonly=True)
    credited_base_minutes = fields.Integer(string="موظفی پوشش‌داده‌شده", readonly=True)
    absence_minutes = fields.Integer(string="کسری / غیبت", readonly=True)
    tardy_minutes = fields.Integer(string="تأخیر ورود", readonly=True)
    early_exit_minutes = fields.Integer(string="تعجیل خروج", readonly=True)
    mandatory_overtime_minutes = fields.Integer(string="اضافه‌کاری اجباری برنامه", readonly=True, groups="cas_kardex_management.group_cas_kardex_supervisor")
    discretionary_overtime_minutes = fields.Integer(string="اضافه‌کاری نیازمند مجوز", readonly=True, groups="cas_kardex_management.group_cas_kardex_supervisor")
    approved_overtime_minutes = fields.Integer(string="اضافه‌کاری اختیاری نهایی", readonly=True, groups="cas_kardex_management.group_cas_kardex_supervisor")
    holiday_work_minutes = fields.Integer(string="کار در روز تعطیل", readonly=True, groups="cas_kardex_management.group_cas_kardex_supervisor")
    break_waiver_state = fields.Selection([("none", "نیاز ندارد"), ("pending", "نیازمند تصمیم سرپرست"), ("approved", "عدم استفاده مجاز از استراحت"), ("rejected", "نیم‌ساعت کسری ثبت شود")], string="تصمیم استراحت", default="none", readonly=True, tracking=True)
    break_waiver_reason = fields.Text(string="دلیل تصمیم استراحت")
    break_waiver_by_id = fields.Many2one("res.users", readonly=True)
    break_waiver_at = fields.Datetime(readonly=True)
    state = fields.Selection([("draft", "در انتظار حضور معتبر"), ("warning", "نیازمند رسیدگی"), ("final", "محاسبه‌شده")], string="وضعیت", required=True, default="draft", readonly=True, index=True)

    _employee_date_uniq = models.Constraint("UNIQUE(employee_id, work_date)", "برای هر کارمند در هر روز فقط یک کاردکس مجاز است.")

    @api.model
    def _get_or_create(self, attendance_day):
        rec = self.sudo().search([("attendance_day_id", "=", attendance_day.id)], limit=1)
        if rec:
            return rec
        period = self.env["cas.kardex.period"].period_for(attendance_day.company_id, attendance_day.work_date)
        return self.sudo().with_context(cas_kardex_engine=True).create({
            "employee_id": attendance_day.employee_id.id, "work_date": attendance_day.work_date,
            "attendance_day_id": attendance_day.id, "period_id": period.id,
        })

    @api.model_create_multi
    def create(self, vals_list):
        if not (self.env.is_superuser() or self.env.context.get("cas_kardex_engine")):
            raise AccessError(_("روز کاردکس فقط توسط موتور محاسبه ساخته می‌شود."))
        return super().create(vals_list)

    def _check_editable(self):
        for rec in self:
            if not rec.period_id.allows_edit(rec.employee_id, rec.work_date):
                raise AccessError(_("کاردکس این روز قفل است و مجوز بازگشایی مدیرعامل ندارد."))

    def write(self, vals):
        engine_fields = set(self._fields) - {"break_waiver_reason", "message_follower_ids", "message_partner_ids", "message_ids", "activity_ids"}
        if engine_fields.intersection(vals):
            if not self.env.context.get("cas_kardex_engine"):
                raise AccessError(_("اعداد کاردکس فقط توسط موتور رسمی تغییر می‌کنند."))
            self._check_editable()
        return super().write(vals)

    def unlink(self):
        raise ValidationError(_("روز کاردکس و سابقه آن قابل حذف نیست."))

    def _approved_coverage(self, request_type, base_minutes):
        self.ensure_one()
        requests = self.env["cas.attendance.request"].sudo().search([
            ("employee_id", "=", self.employee_id.id), ("request_type", "=", request_type),
            ("state", "=", "approved"), ("date_from", "<=", self.work_date), ("date_to", ">=", self.work_date),
        ])
        total = 0
        for req in requests:
            if req.duration_type == "hourly":
                start = max(req.datetime_from, self.shift_day_id.planned_start) if self.shift_day_id.planned_start else req.datetime_from
                end = min(req.datetime_to, self.shift_day_id.planned_end) if self.shift_day_id.planned_end else req.datetime_to
                total += max(int((end - start).total_seconds() // 60), 0)
            else:
                total += base_minutes
        return min(total, base_minutes)

    def recompute(self):
        for rec in self:
            rec._check_editable()
            attendance = rec.attendance_day_id
            shift = attendance.shift_day_id
            presence = 0
            if attendance.effective_entry and attendance.effective_exit:
                presence = max(int((attendance.effective_exit - attendance.effective_entry).total_seconds() // 60), 0)
            base = shift.base_work_minutes if shift else 0
            scheduled_break = shift.break_minutes if shift else 0
            required_presence = shift.required_presence_minutes if shift else 0
            if attendance.attendance_mode == "advanced":
                actual_break = sum(attendance.interval_ids.filtered(lambda i: i.interval_type == "break").mapped("duration_minutes"))
                deducted_break = actual_break
            else:
                deducted_break = scheduled_break
                if shift and shift.rule_is_short_day and presence > base:
                    deducted_break = shift.policy_id.short_day_extended_break_minutes
                if rec.break_waiver_state == "approved":
                    deducted_break = 0
            net = max(presence - deducted_break, 0)
            leave = rec._approved_coverage("leave", base) if base else 0
            mission = rec._approved_coverage("mission", base) if base else 0
            covered = min(base, net + leave + mission)
            absence = max(base - covered, 0)
            tardy = max(int((attendance.effective_entry - shift.planned_start).total_seconds() // 60), 0) if shift and attendance.effective_entry else 0
            early = max(int((shift.planned_end - attendance.effective_exit).total_seconds() // 60), 0) if shift and attendance.effective_exit else 0
            mandatory = min(max(net - base, 0), shift.mandatory_overtime_minutes) if shift else 0
            discretionary = max(net - base - mandatory, 0) if base else net
            overtime = self.env["cas.overtime.request"].sudo().search([("kardex_day_id", "=", rec.id), ("state", "=", "approved")], limit=1)
            pending_break = bool(base and scheduled_break and attendance.attendance_mode == "simple" and base <= presence < required_presence and rec.break_waiver_state not in {"approved", "rejected"})
            waiver_state = "pending" if pending_break else rec.break_waiver_state
            if not pending_break and rec.break_waiver_state == "pending":
                waiver_state = "none"
            valid_attendance = attendance.state in {"normal", "warning", "resolved"}
            state = "draft" if not valid_attendance else ("warning" if waiver_state == "pending" else "final")
            rec.with_context(cas_kardex_engine=True).write({
                "planned_base_minutes": base, "planned_break_minutes": scheduled_break, "planned_presence_minutes": required_presence,
                "presence_minutes": presence, "deducted_break_minutes": deducted_break, "net_work_minutes": net,
                "leave_minutes": leave, "mission_minutes": mission, "credited_base_minutes": covered, "absence_minutes": absence,
                "tardy_minutes": tardy, "early_exit_minutes": early, "mandatory_overtime_minutes": mandatory,
                "discretionary_overtime_minutes": discretionary, "approved_overtime_minutes": overtime.final_approved_minutes if overtime else 0,
                "holiday_work_minutes": net if shift and shift.day_kind != "work" else 0,
                "break_waiver_state": waiver_state, "state": state,
            })
        return True

    @api.model
    def recompute_range(self, employees, date_from, date_to):
        attendance_days = self.env["cas.attendance.day"].sudo().search([
            ("employee_id", "in", employees.ids), ("work_date", ">=", date_from), ("work_date", "<=", date_to),
        ])
        for attendance in attendance_days:
            self._get_or_create(attendance).recompute()
        return len(attendance_days)

    def action_approve_break_waiver(self):
        for rec in self:
            if rec.break_waiver_state != "pending":
                raise ValidationError(_("این روز در انتظار تصمیم استراحت نیست."))
            if not rec.break_waiver_reason:
                raise ValidationError(_("ثبت دلیل تصمیم الزامی است."))
            rec.with_context(cas_kardex_engine=True).write({"break_waiver_state": "approved", "break_waiver_by_id": self.env.user.id, "break_waiver_at": fields.Datetime.now()})
            rec.recompute()

    def action_reject_break_waiver(self):
        for rec in self:
            if rec.break_waiver_state != "pending" or not rec.break_waiver_reason:
                raise ValidationError(_("روز باید در انتظار تصمیم باشد و دلیل ثبت شود."))
            rec.with_context(cas_kardex_engine=True).write({"break_waiver_state": "rejected", "break_waiver_by_id": self.env.user.id, "break_waiver_at": fields.Datetime.now()})
            rec.recompute()


class CasAttendanceDay(models.Model):
    _inherit = "cas.attendance.day"

    kardex_day_id = fields.One2many("cas.kardex.day", "attendance_day_id", string="کاردکس", readonly=True)

    def recompute(self):
        result = super().recompute()
        if "cas.kardex.day" in self.env:
            for attendance in self:
                self.env["cas.kardex.day"].sudo()._get_or_create(attendance).recompute()
        return result

    def action_new_attendance_request(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window", "name": _("درخواست مرخصی یا مأموریت"),
            "res_model": "cas.attendance.request", "view_mode": "form", "target": "current",
            "context": {
                "default_employee_id": self.employee_id.id, "default_date_from": self.work_date,
                "default_date_to": self.work_date, "default_source_attendance_day_id": self.id,
            },
        }
