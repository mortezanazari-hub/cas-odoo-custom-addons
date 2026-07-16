from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CasAttendanceRequest(models.Model):
    _name = "cas.attendance.request"
    _description = "CAS Leave or Mission Request"
    _inherit = ["mail.thread", "mail.activity.mixin", "cas.kardex.approval.mixin"]
    _order = "date_from desc, id desc"
    _rec_name = "number"

    number = fields.Char(string="شماره", default="New", readonly=True, copy=False, index=True)
    employee_id = fields.Many2one("hr.employee", string="کارمند", required=True, ondelete="restrict", index=True, tracking=True)
    company_id = fields.Many2one(related="employee_id.company_id", store=True, index=True)
    request_type = fields.Selection([("leave", "مرخصی"), ("mission", "مأموریت خارج از شرکت")], string="نوع درخواست", required=True, tracking=True)
    duration_type = fields.Selection([("hourly", "ساعتی"), ("daily", "روزانه"), ("multi", "چندروزه")], string="نوع مدت", required=True, default="hourly")
    date_from = fields.Date(string="از روز", required=True, index=True)
    date_to = fields.Date(string="تا روز", required=True, index=True)
    datetime_from = fields.Datetime(string="از ساعت")
    datetime_to = fields.Datetime(string="تا ساعت")
    requested_minutes = fields.Integer(string="دقایق پوشش تعهد", compute="_compute_requested_minutes", store=True)
    reason = fields.Text(string="دلیل / شرح", required=True)
    source_attendance_day_id = fields.Many2one("cas.attendance.day", string="روز حضور مبدأ", ondelete="restrict")
    approver_user_id = fields.Many2one("res.users", string="تأییدکننده", readonly=True, ondelete="restrict", index=True)
    approver_role = fields.Selection([("manager", "مدیر واحد یا بالادست"), ("ceo", "مدیرعامل")], string="مسیر تأیید", readonly=True)
    state = fields.Selection([("draft", "پیش‌نویس"), ("pending", "در انتظار تأیید"), ("approved", "تأییدشده"), ("rejected", "ردشده"), ("cancelled", "لغوشده")], string="وضعیت", required=True, default="draft", readonly=True, tracking=True, index=True)
    submitted_at = fields.Datetime(readonly=True)
    decided_at = fields.Datetime(readonly=True)
    decision_user_id = fields.Many2one("res.users", readonly=True)
    decision_note = fields.Text(string="توضیح تصمیم")

    _number_uniq = models.Constraint("UNIQUE(number)", "شماره درخواست باید یکتا باشد.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("number", "New") == "New":
                vals["number"] = self.env["ir.sequence"].next_by_code("cas.attendance.request") or "New"
        return super().create(vals_list)

    @api.depends("duration_type", "date_from", "date_to", "datetime_from", "datetime_to", "employee_id")
    def _compute_requested_minutes(self):
        Shift = self.env["cas.shift.day"]
        for rec in self:
            minutes = 0
            if rec.duration_type == "hourly" and rec.datetime_from and rec.datetime_to:
                minutes = max(int((rec.datetime_to - rec.datetime_from).total_seconds() // 60), 0)
            elif rec.employee_id and rec.date_from and rec.date_to and rec.date_to >= rec.date_from:
                days = Shift.search([("employee_id", "=", rec.employee_id.id), ("schedule_date", ">=", rec.date_from), ("schedule_date", "<=", rec.date_to), ("day_kind", "=", "work")])
                minutes = sum(days.mapped("base_work_minutes"))
            rec.requested_minutes = minutes

    @api.constrains("date_from", "date_to", "duration_type", "datetime_from", "datetime_to", "employee_id")
    def _check_request_range(self):
        for rec in self:
            if rec.date_to < rec.date_from:
                raise ValidationError(_("پایان درخواست نمی‌تواند قبل از شروع آن باشد."))
            if rec.duration_type == "hourly":
                if not rec.datetime_from or not rec.datetime_to or rec.datetime_to <= rec.datetime_from:
                    raise ValidationError(_("برای درخواست ساعتی، بازه ساعت معتبر الزامی است."))
                if rec.datetime_from.date() != rec.date_from or rec.datetime_to.date() not in {rec.date_from, rec.date_from + timedelta(days=1)}:
                    raise ValidationError(_("ساعت درخواست ساعتی باید با روز درخواست منطبق باشد."))
                shift = self.env["cas.shift.day"].search([("employee_id", "=", rec.employee_id.id), ("schedule_date", "=", rec.date_from), ("day_kind", "=", "work")], limit=1)
                if not shift:
                    raise ValidationError(_("روز تعطیل تعهد کاری ندارد و برای آن مرخصی یا مأموریت لازم نیست."))
            if rec.requested_minutes <= 0:
                raise ValidationError(_("روز تعطیل تعهد کاری ندارد و برای آن مرخصی یا مأموریت لازم نیست."))

    def write(self, vals):
        protected = {"employee_id", "request_type", "duration_type", "date_from", "date_to", "datetime_from", "datetime_to", "reason"}
        if protected.intersection(vals) and any(rec.state != "draft" for rec in self):
            raise ValidationError(_("درخواست پس از ارسال قابل ویرایش نیست."))
        engine = {"state", "approver_user_id", "approver_role", "submitted_at", "decided_at", "decision_user_id"}
        if engine.intersection(vals) and not self.env.context.get("cas_request_engine"):
            raise AccessError(_("وضعیت درخواست فقط از عملیات رسمی تغییر می‌کند."))
        if set(vals) <= {"decision_note"} and all(
            rec.state == "pending" and (self.env.is_superuser() or rec.approver_user_id == self.env.user) for rec in self
        ):
            return super().write(vals)
        return super().write(vals)

    def unlink(self):
        if any(rec.state != "draft" for rec in self):
            raise ValidationError(_("درخواست ارسال‌شده قابل حذف نیست."))
        return super().unlink()

    def action_submit(self):
        for rec in self:
            if rec.state != "draft":
                raise ValidationError(_("فقط پیش‌نویس قابل ارسال است."))
            approver, role = rec._cas_manager_or_ceo(rec.employee_id)
            rec.with_context(cas_request_engine=True).write({"state": "pending", "approver_user_id": approver.id, "approver_role": role, "submitted_at": fields.Datetime.now()})
            rec.activity_schedule("mail.mail_activity_data_todo", user_id=approver.id, summary=_("رسیدگی به %s", rec.number))

    def _check_approver(self):
        for rec in self:
            if rec.state != "pending":
                raise ValidationError(_("این درخواست در انتظار تصمیم نیست."))
            if not (self.env.is_superuser() or rec.approver_user_id == self.env.user):
                raise AccessError(_("شما تأییدکننده این درخواست نیستید."))

    def action_approve(self):
        self._check_approver()
        self.with_context(cas_request_engine=True).write({"state": "approved", "decided_at": fields.Datetime.now(), "decision_user_id": self.env.user.id})
        self.activity_ids.action_done()
        self.env["cas.kardex.day"].sudo().recompute_range(self.mapped("employee_id"), min(self.mapped("date_from")), max(self.mapped("date_to")))

    def action_reject(self):
        self._check_approver()
        if any(not rec.decision_note for rec in self):
            raise ValidationError(_("برای رد درخواست، توضیح تصمیم الزامی است."))
        self.with_context(cas_request_engine=True).write({"state": "rejected", "decided_at": fields.Datetime.now(), "decision_user_id": self.env.user.id})
        self.activity_ids.action_done()

    def action_cancel(self):
        for rec in self:
            if rec.state not in {"draft", "pending"}:
                raise ValidationError(_("این درخواست قابل لغو نیست."))
            if not (self.env.is_superuser() or rec.employee_id.user_id == self.env.user):
                raise AccessError(_("فقط درخواست‌کننده می‌تواند درخواست را لغو کند."))
            rec.with_context(cas_request_engine=True).write({"state": "cancelled"})
            rec.activity_ids.unlink()
