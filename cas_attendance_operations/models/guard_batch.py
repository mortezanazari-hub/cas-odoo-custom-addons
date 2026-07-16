from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CasGuardBatch(models.Model):
    _name = "cas.guard.batch"
    _description = "CAS Rapid Guard Attendance Batch"
    _inherit = ["mail.thread"]
    _order = "create_date desc, id desc"

    name = fields.Char(string="عنوان نوبت ثبت", required=True, default=lambda self: _("ثبت تردد نگهبانی"))
    company_id = fields.Many2one("res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True)
    site_id = fields.Many2one("cas.attendance.site", string="درب / محل", required=True, ondelete="restrict", index=True)
    default_occurred_at = fields.Datetime(string="زمان پیش‌فرض", required=True, default=fields.Datetime.now)
    line_ids = fields.One2many("cas.guard.batch.line", "batch_id", string="افراد", copy=False)
    state = fields.Selection([("draft", "در حال ثبت"), ("confirmed", "ثبت نهایی‌شده")], string="وضعیت", required=True, default="draft", readonly=True, tracking=True)
    confirmed_at = fields.Datetime(readonly=True)
    confirmed_by_id = fields.Many2one("res.users", readonly=True)

    def write(self, vals):
        structural = {"site_id", "default_occurred_at", "line_ids"}
        if structural.intersection(vals) and any(rec.state != "draft" for rec in self):
            raise ValidationError(_("بچ نهایی‌شده نگهبانی قابل تغییر نیست."))
        engine = {"state", "confirmed_at", "confirmed_by_id"}
        if engine.intersection(vals) and not self.env.context.get("cas_guard_engine"):
            raise AccessError(_("وضعیت بچ فقط با عملیات ثبت نهایی تغییر می‌کند."))
        return super().write(vals)

    def unlink(self):
        if any(rec.state != "draft" for rec in self): raise ValidationError(_("بچ نهایی‌شده قابل حذف نیست."))
        return super().unlink()

    def action_confirm(self):
        for batch in self:
            if batch.state != "draft" or not batch.line_ids: raise ValidationError(_("بچ خالی یا قبلاً نهایی‌شده است."))
            if any(not line.employee_id or not line.occurred_at or not line.event_kind for line in batch.line_ids):
                raise ValidationError(_("کارمند، زمان و نوع تردد همه ردیف‌ها الزامی است."))
            for line in batch.line_ids:
                event = self.env["cas.attendance.event"].with_context(cas_attendance_supervisor=True).create({
                    "employee_id": line.employee_id.id, "occurred_at": line.occurred_at,
                    "work_date": line.work_date or False, "source": "guard", "event_kind": line.event_kind,
                    "site_id": batch.site_id.id, "note": line.note or _("ثبت گروهی نگهبانی: %s", batch.name),
                })
                line.with_context(cas_guard_engine=True).write({"event_id": event.id})
            batch.with_context(cas_guard_engine=True).write({"state": "confirmed", "confirmed_at": fields.Datetime.now(), "confirmed_by_id": self.env.user.id})


class CasGuardBatchLine(models.Model):
    _name = "cas.guard.batch.line"
    _description = "CAS Rapid Guard Attendance Batch Line"
    _order = "batch_id, id"

    batch_id = fields.Many2one("cas.guard.batch", required=True, ondelete="cascade", index=True)
    company_id = fields.Many2one(related="batch_id.company_id", store=True, index=True)
    employee_id = fields.Many2one("hr.employee", string="کارمند", required=True, ondelete="restrict", index=True)
    occurred_at = fields.Datetime(string="زمان واقعی", required=True, default=lambda self: self.env.context.get("default_occurred_at") or fields.Datetime.now())
    event_kind = fields.Selection([
        ("guard_entry", "ورود اولیه"), ("guard_exit", "خروج نهایی"),
        ("temporary_exit", "خروج موقت شخصی"), ("temporary_return", "بازگشت خروج موقت"),
        ("mission_exit", "خروج مأموریت"), ("mission_return", "بازگشت مأموریت"),
        ("leave_exit", "خروج مرخصی ساعتی"), ("leave_return", "بازگشت مرخصی ساعتی"),
        ("unknown_entry", "ورود نامشخص"), ("unknown_exit", "خروج نامشخص"),
    ], string="نوع تردد", required=True, default="guard_entry")
    work_date = fields.Date(string="روز کاری اختیاری", help="در حالت عادی خالی بماند تا از برنامه شیفت تعیین شود.")
    note = fields.Char(string="توضیح")
    event_id = fields.Many2one("cas.attendance.event", string="رخداد ثبت‌شده", readonly=True, ondelete="restrict")

    @api.onchange("batch_id")
    def _onchange_batch(self):
        if self.batch_id and not self.occurred_at: self.occurred_at = self.batch_id.default_occurred_at

    def write(self, vals):
        if self.env.context.get("cas_guard_engine"): return super().write(vals)
        if any(line.batch_id.state != "draft" for line in self): raise ValidationError(_("ردیف نهایی‌شده قابل تغییر نیست."))
        return super().write(vals)

    def unlink(self):
        if any(line.batch_id.state != "draft" for line in self): raise ValidationError(_("ردیف نهایی‌شده قابل حذف نیست."))
        return super().unlink()
