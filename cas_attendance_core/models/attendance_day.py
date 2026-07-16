from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CasAttendanceDay(models.Model):
    _name = "cas.attendance.day"
    _description = "CAS Reconciled Attendance Day"
    _inherit = ["mail.thread"]
    _order = "work_date desc, employee_id"

    employee_id = fields.Many2one("hr.employee", string="کارمند", required=True, ondelete="restrict", index=True)
    company_id = fields.Many2one(related="employee_id.company_id", string="شرکت", store=True, index=True)
    work_date = fields.Date(string="روز کاری", required=True, index=True)
    shift_day_id = fields.Many2one("cas.shift.day", string="برنامه شیفت", ondelete="restrict", index=True, readonly=True)
    attendance_mode = fields.Selection([("simple", "ساده"), ("advanced", "پیشرفته")], string="روش محاسبه", required=True, readonly=True, index=True)
    tolerance_minutes = fields.Integer(string="حد تطبیق منابع", readonly=True)
    event_ids = fields.One2many("cas.attendance.event", compute="_compute_events", string="رخدادهای خام")
    interval_ids = fields.One2many("cas.attendance.interval", "attendance_day_id", string="بازه‌های محاسباتی", readonly=True)
    guard_entry = fields.Datetime(string="ورود نگهبانی", readonly=True)
    guard_exit = fields.Datetime(string="خروج نگهبانی", readonly=True)
    device_entry = fields.Datetime(string="شروع کار دستگاه", readonly=True)
    device_exit = fields.Datetime(string="پایان کار دستگاه", readonly=True)
    effective_entry = fields.Datetime(string="ورود مؤثر", readonly=True)
    effective_exit = fields.Datetime(string="خروج مؤثر", readonly=True)
    state = fields.Selection([
        ("draft", "در انتظار رخداد"), ("normal", "تطبیق‌شده"), ("warning", "بسته‌شده با هشدار"),
        ("conflict", "نیازمند تصمیم سرپرست"), ("incomplete", "ناقص"), ("resolved", "حل‌شده توسط سرپرست"),
    ], string="وضعیت", required=True, default="draft", readonly=True, index=True, tracking=True)
    warning_code = fields.Selection([
        ("mixed", "تکمیل ترکیبی منابع"), ("guard_only", "فقط اطلاعات نگهبانی"),
        ("device_only", "فقط اطلاعات دستگاه"), ("outage", "جایگزینی به‌علت خرابی دستگاه"),
        ("advanced_incomplete", "زنجیره رخداد پیشرفته ناقص"),
    ], string="هشدار", readonly=True)
    resolution_entry_source = fields.Selection([("guard", "نگهبانی"), ("device", "دستگاه"), ("custom", "زمان اصلاحی")], string="مبنای ورود")
    resolution_exit_source = fields.Selection([("guard", "نگهبانی"), ("device", "دستگاه"), ("custom", "زمان اصلاحی")], string="مبنای خروج")
    custom_entry = fields.Datetime(string="ورود اصلاحی")
    custom_exit = fields.Datetime(string="خروج اصلاحی")
    resolution_reason = fields.Text(string="دلیل تصمیم سرپرست")
    resolved_by_id = fields.Many2one("res.users", string="تصمیم‌گیرنده", readonly=True)
    resolved_at = fields.Datetime(string="زمان تصمیم", readonly=True)

    _employee_date_uniq = models.Constraint("UNIQUE(employee_id, work_date)", "برای هر کارمند در هر روز فقط یک نتیجه حضور مجاز است.")

    @api.depends("employee_id", "work_date")
    def _compute_events(self):
        Event = self.env["cas.attendance.event"]
        for rec in self:
            rec.event_ids = Event.search([("employee_id", "=", rec.employee_id.id), ("work_date", "=", rec.work_date)])

    @api.model
    def _get_or_create(self, employee, work_date):
        rec = self.search([("employee_id", "=", employee.id), ("work_date", "=", work_date)], limit=1)
        if rec:
            return rec
        shift = self.env["cas.shift.day"].search([("employee_id", "=", employee.id), ("schedule_date", "=", work_date)], limit=1)
        return self.with_context(cas_attendance_engine=True).create({
            "employee_id": employee.id, "work_date": work_date, "shift_day_id": shift.id,
            "attendance_mode": shift.attendance_mode if shift else "simple",
            "tolerance_minutes": shift.source_tolerance_minutes if shift else 5,
        })

    @api.model_create_multi
    def create(self, vals_list):
        if not (self.env.is_superuser() or self.env.context.get("cas_attendance_engine")):
            raise AccessError(_("روز حضور فقط توسط موتور تطبیق ساخته می‌شود."))
        return super().create(vals_list)

    def unlink(self):
        raise AccessError(_("نتیجه روزانه حضور قابل حذف نیست."))

    def _events(self):
        self.ensure_one()
        return self.env["cas.attendance.event"].search([
            ("employee_id", "=", self.employee_id.id), ("work_date", "=", self.work_date), ("is_void", "=", False)
        ], order="occurred_at, id")

    def _has_outage(self):
        self.ensure_one()
        if not self.shift_day_id or not self.shift_day_id.planned_start:
            return False
        return bool(self.env["cas.attendance.outage"].search_count([
            ("company_id", "=", self.company_id.id), ("start_at", "<=", self.shift_day_id.planned_end),
            "|", ("end_at", "=", False), ("end_at", ">=", self.shift_day_id.planned_start),
        ]))

    def recompute(self):
        for rec in self:
            if rec.attendance_mode == "advanced":
                rec._recompute_advanced()
            else:
                rec._recompute_simple()
        return True

    def _recompute_simple(self):
        self.ensure_one()
        events = self._events()
        guard_in = events.filtered(lambda e: e.source == "guard" and e.event_kind == "guard_entry")[:1]
        guard_outs = events.filtered(lambda e: e.source == "guard" and e.event_kind == "guard_exit")
        device_in = events.filtered(lambda e: e.source == "device" and e.event_kind == "work_start")[:1]
        device_outs = events.filtered(lambda e: e.source == "device" and e.event_kind == "work_end")
        gi, go = (guard_in.occurred_at if guard_in else False), (guard_outs[-1:].occurred_at if guard_outs else False)
        di, do = (device_in.occurred_at if device_in else False), (device_outs[-1:].occurred_at if device_outs else False)
        conflict = ((gi and di and abs((gi - di).total_seconds()) > self.tolerance_minutes * 60) or
                    (go and do and abs((go - do).total_seconds()) > self.tolerance_minutes * 60))
        entry = max(gi, di) if gi and di else (gi or di)
        exit_ = min(go, do) if go and do else (go or do)
        state, warning = "normal", False
        if conflict:
            state = "conflict"
            entry = exit_ = False
        elif not entry or not exit_:
            state = "incomplete"
        elif not (gi and go and di and do):
            if self._has_outage() and gi and go:
                state, warning = "warning", "outage"
            elif (gi or go) and (di or do):
                state, warning = "warning", "mixed"
            elif gi or go:
                state, warning = "warning", "guard_only"
            else:
                state, warning = "warning", "device_only"
        self.with_context(cas_attendance_engine=True).write({
            "guard_entry": gi, "guard_exit": go, "device_entry": di, "device_exit": do,
            "effective_entry": entry, "effective_exit": exit_, "state": state, "warning_code": warning,
        })

    def _recompute_advanced(self):
        self.ensure_one()
        self.interval_ids.with_context(cas_attendance_engine=True).unlink()
        events = self._events()
        stack = {}
        pairs = {"work_start": ("work_end", "work"), "break_start": ("break_end", "break"),
                 "temporary_exit": ("temporary_return", "personal"), "mission_exit": ("mission_return", "mission"),
                 "leave_exit": ("leave_return", "leave")}
        reverse = {end: start for start, (end, _) in pairs.items()}
        incomplete = False
        for event in events:
            if event.event_kind in pairs:
                if event.event_kind in stack:
                    incomplete = True
                stack[event.event_kind] = event
            elif event.event_kind in reverse:
                start_kind = reverse[event.event_kind]
                start = stack.pop(start_kind, False)
                if not start or event.occurred_at <= start.occurred_at:
                    incomplete = True
                    continue
                self.env["cas.attendance.interval"].with_context(cas_attendance_engine=True).create({
                    "attendance_day_id": self.id, "interval_type": pairs[start_kind][1],
                    "start_event_id": start.id, "end_event_id": event.id,
                    "start_at": start.occurred_at, "end_at": event.occurred_at,
                })
        incomplete = incomplete or bool(stack)
        works = self.interval_ids.filtered(lambda i: i.interval_type == "work")
        self.with_context(cas_attendance_engine=True).write({
            "effective_entry": min(works.mapped("start_at")) if works else False,
            "effective_exit": max(works.mapped("end_at")) if works else False,
            "state": "incomplete" if incomplete or not works else "normal",
            "warning_code": "advanced_incomplete" if incomplete else False,
        })

    def write(self, vals):
        engine_fields = {"guard_entry", "guard_exit", "device_entry", "device_exit", "effective_entry", "effective_exit", "state", "warning_code"}
        if engine_fields.intersection(vals) and not self.env.context.get("cas_attendance_engine"):
            raise AccessError(_("نتیجه محاسباتی فقط از عملیات رسمی قابل تغییر است."))
        return super().write(vals)

    def action_resolve(self):
        for rec in self:
            if rec.state != "conflict":
                raise ValidationError(_("فقط اختلاف باز قابل تصمیم‌گیری است."))
            if not rec.resolution_reason or not rec.resolution_entry_source or not rec.resolution_exit_source:
                raise ValidationError(_("مبنای ورود، مبنای خروج و دلیل تصمیم الزامی است."))
            entry = {"guard": rec.guard_entry, "device": rec.device_entry, "custom": rec.custom_entry}[rec.resolution_entry_source]
            exit_ = {"guard": rec.guard_exit, "device": rec.device_exit, "custom": rec.custom_exit}[rec.resolution_exit_source]
            if not entry or not exit_ or exit_ <= entry:
                raise ValidationError(_("ورود و خروج انتخاب‌شده معتبر نیست."))
            rec.with_context(cas_attendance_engine=True).write({
                "effective_entry": entry, "effective_exit": exit_, "state": "resolved",
                "resolved_by_id": self.env.user.id, "resolved_at": fields.Datetime.now(), "warning_code": False,
            })


class CasAttendanceInterval(models.Model):
    _name = "cas.attendance.interval"
    _description = "CAS Attendance Computation Interval"
    _order = "start_at, id"

    attendance_day_id = fields.Many2one("cas.attendance.day", string="روز حضور", required=True, ondelete="cascade", index=True)
    employee_id = fields.Many2one(related="attendance_day_id.employee_id", store=True, index=True)
    company_id = fields.Many2one(related="attendance_day_id.company_id", store=True, index=True)
    interval_type = fields.Selection([("work", "کار"), ("break", "استراحت"), ("personal", "خروج شخصی"), ("mission", "مأموریت"), ("leave", "مرخصی")], string="نوع بازه", required=True)
    start_event_id = fields.Many2one("cas.attendance.event", string="رخداد شروع", required=True, ondelete="restrict")
    end_event_id = fields.Many2one("cas.attendance.event", string="رخداد پایان", required=True, ondelete="restrict")
    start_at = fields.Datetime(string="شروع", required=True, readonly=True)
    end_at = fields.Datetime(string="پایان", required=True, readonly=True)
    duration_minutes = fields.Integer(string="مدت (دقیقه)", compute="_compute_duration", store=True)

    @api.depends("start_at", "end_at")
    def _compute_duration(self):
        for rec in self:
            rec.duration_minutes = int((rec.end_at - rec.start_at).total_seconds() // 60) if rec.start_at and rec.end_at else 0

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.context.get("cas_attendance_engine"):
            raise AccessError(_("بازه محاسباتی فقط توسط موتور حضور ساخته می‌شود."))
        return super().create(vals_list)

    def write(self, vals):
        if not self.env.context.get("cas_attendance_engine"):
            raise AccessError(_("بازه محاسباتی قابل ویرایش مستقیم نیست."))
        return super().write(vals)

    def unlink(self):
        if not self.env.context.get("cas_attendance_engine"):
            raise AccessError(_("بازه محاسباتی قابل حذف مستقیم نیست."))
        return super().unlink()
