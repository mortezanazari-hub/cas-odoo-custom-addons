from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CasOvertimeAuthorization(models.Model):
    _name = "cas.overtime.authorization"
    _description = "CAS CEO Overtime Auto Approval Authorization"
    _inherit = ["mail.thread", "cas.kardex.approval.mixin"]
    _order = "effective_from desc, id desc"

    employee_id = fields.Many2one("hr.employee", string="کارمند", required=True, ondelete="restrict", index=True, tracking=True)
    company_id = fields.Many2one(related="employee_id.company_id", store=True, index=True)
    grant_scope = fields.Selection([("month_start", "از ابتدای ماه جاری"), ("grant_date", "از روز صدور")], string="شروع اثر", required=True, default="grant_date")
    effective_from = fields.Date(string="تاریخ شروع اثر", required=True, readonly=True, index=True)
    date_to = fields.Date(string="تاریخ پایان", index=True, tracking=True)
    reason = fields.Text(string="دلیل مجوز", required=True)
    active = fields.Boolean(default=True, readonly=True, tracking=True)
    granted_by_id = fields.Many2one("res.users", string="صادرکننده", readonly=True)
    granted_at = fields.Datetime(string="زمان صدور", readonly=True)
    revoked_by_id = fields.Many2one("res.users", string="لغوکننده", readonly=True)
    revoked_at = fields.Datetime(string="زمان لغو", readonly=True)
    revoke_reason = fields.Text(string="دلیل لغو")
    review_rejected_cases = fields.Boolean(string="بازبینی موارد قبلاً ردشده", default=False, help="ردهای قبلی خودکار برنمی‌گردند؛ با این گزینه در فهرست بازبینی مدیرعامل قرار می‌گیرند.")

    @api.model_create_multi
    def create(self, vals_list):
        today = fields.Date.context_today(self)
        for vals in vals_list:
            employee = self.env["hr.employee"].browse(vals["employee_id"])
            self._cas_require_ceo(employee.company_id)
            scope = vals.get("grant_scope", "grant_date")
            vals["effective_from"] = today.replace(day=1) if scope == "month_start" else today
            vals["granted_by_id"] = self.env.user.id
            vals["granted_at"] = fields.Datetime.now()
        return super().create(vals_list)

    def write(self, vals):
        for rec in self:
            rec._cas_require_ceo(rec.company_id)
        protected = {"employee_id", "grant_scope", "effective_from", "granted_by_id", "granted_at"}
        if protected.intersection(vals):
            raise ValidationError(_("مشخصات صدور مجوز قابل تغییر نیست؛ مجوز را لغو و مورد جدید صادر کنید."))
        return super().write(vals)

    def unlink(self):
        raise ValidationError(_("مجوز اضافه‌کاری قابل حذف نیست؛ آن را با حفظ سابقه لغو کنید."))

    def action_revoke(self):
        for rec in self:
            rec._cas_require_ceo(rec.company_id)
            if not rec.active:
                continue
            if not rec.revoke_reason:
                raise ValidationError(_("ثبت دلیل لغو الزامی است."))
            rec.write({"active": False, "revoked_by_id": self.env.user.id, "revoked_at": fields.Datetime.now()})

    @api.model
    def authorization_for(self, employee, work_date):
        return self.sudo().search([
            ("employee_id", "=", employee.id), ("active", "=", True),
            ("effective_from", "<=", work_date), "|", ("date_to", "=", False), ("date_to", ">=", work_date),
        ], order="effective_from desc, id desc", limit=1)


class CasOvertimeRequest(models.Model):
    _name = "cas.overtime.request"
    _description = "CAS Post Work Overtime Request"
    _inherit = ["mail.thread", "mail.activity.mixin", "cas.kardex.approval.mixin"]
    _order = "work_date desc, id desc"
    _rec_name = "number"

    number = fields.Char(string="شماره", default="New", readonly=True, copy=False, index=True)
    employee_id = fields.Many2one("hr.employee", string="کارمند", required=True, ondelete="restrict", index=True)
    company_id = fields.Many2one(related="employee_id.company_id", store=True, index=True)
    kardex_day_id = fields.Many2one("cas.kardex.day", string="روز کاردکس", required=True, ondelete="restrict", index=True)
    work_date = fields.Date(related="kardex_day_id.work_date", string="روز کار", store=True, index=True)
    actual_minutes = fields.Integer(string="اضافه‌کاری واقعی قابل درخواست", required=True, readonly=True)
    manager_approved_minutes = fields.Integer(string="دقایق تأیید مدیر", readonly=True)
    ceo_approved_minutes = fields.Integer(string="دقایق تأیید نهایی مدیرعامل", readonly=True)
    final_approved_minutes = fields.Integer(string="دقایق نهایی", readonly=True)
    manager_user_id = fields.Many2one("res.users", string="مدیر رسیدگی‌کننده", readonly=True)
    authorization_id = fields.Many2one("cas.overtime.authorization", string="مجوز خودکار مدیرعامل", readonly=True, ondelete="restrict")
    reason = fields.Text(string="شرح اضافه‌کاری", required=True)
    manager_note = fields.Text(string="توضیح مدیر")
    ceo_note = fields.Text(string="توضیح مدیرعامل")
    state = fields.Selection([
        ("draft", "پیش‌نویس"), ("pending_manager", "در انتظار مدیر"), ("pending_ceo", "در انتظار مدیرعامل"),
        ("approved", "تأیید نهایی"), ("rejected", "بدون اثر در کاردکس"), ("cancelled", "لغوشده"),
    ], string="وضعیت", required=True, default="draft", readonly=True, tracking=True, index=True)
    submitted_at = fields.Datetime(readonly=True)
    finalized_at = fields.Datetime(readonly=True)

    _number_uniq = models.Constraint("UNIQUE(number)", "شماره درخواست اضافه‌کاری باید یکتا باشد.")
    _day_uniq = models.Constraint("UNIQUE(kardex_day_id)", "برای هر روز کاردکس فقط یک درخواست اضافه‌کاری مجاز است.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            day = self.env["cas.kardex.day"].browse(vals["kardex_day_id"])
            vals["employee_id"] = day.employee_id.id
            vals["actual_minutes"] = day.discretionary_overtime_minutes
            if vals.get("number", "New") == "New":
                vals["number"] = self.env["ir.sequence"].next_by_code("cas.overtime.request") or "New"
            if vals["actual_minutes"] <= 0:
                raise ValidationError(_("برای این روز اضافه‌کاری اختیاری واقعی وجود ندارد."))
        return super().create(vals_list)

    @api.constrains("manager_approved_minutes", "ceo_approved_minutes", "final_approved_minutes", "actual_minutes")
    def _check_minutes(self):
        for rec in self:
            if not 0 <= rec.manager_approved_minutes <= rec.actual_minutes:
                raise ValidationError(_("تأیید مدیر نمی‌تواند از اضافه‌کاری واقعی بیشتر باشد."))
            if not 0 <= rec.ceo_approved_minutes <= rec.manager_approved_minutes:
                raise ValidationError(_("تأیید مدیرعامل نمی‌تواند از مقدار عبورکرده از مدیر بیشتر باشد."))
            if not 0 <= rec.final_approved_minutes <= rec.actual_minutes:
                raise ValidationError(_("اضافه‌کاری نهایی معتبر نیست."))

    def write(self, vals):
        editable = {"reason"} if all(rec.state == "draft" for rec in self) else set()
        decision_fields = {"manager_approved_minutes", "manager_note", "ceo_approved_minutes", "ceo_note"}
        if set(vals).intersection(decision_fields) and self.env.context.get("cas_overtime_decision"):
            return super().write(vals)
        if set(vals) <= {"manager_approved_minutes", "manager_note"} and all(
            rec.state == "pending_manager" and (self.env.is_superuser() or rec.manager_user_id == self.env.user) for rec in self
        ):
            return super().write(vals)
        if set(vals) <= {"ceo_approved_minutes", "ceo_note"} and all(
            rec.state == "pending_ceo" and (self.env.is_superuser() or rec.company_id.cas_ceo_user_id == self.env.user) for rec in self
        ):
            return super().write(vals)
        engine = {"state", "manager_user_id", "authorization_id", "final_approved_minutes", "submitted_at", "finalized_at"}
        if set(vals) - editable - engine or (set(vals).intersection(engine) and not self.env.context.get("cas_overtime_engine")):
            raise ValidationError(_("درخواست اضافه‌کاری فقط از عملیات رسمی تغییر می‌کند."))
        return super().write(vals)

    def unlink(self):
        if any(rec.state != "draft" for rec in self):
            raise ValidationError(_("درخواست ارسال‌شده قابل حذف نیست."))
        return super().unlink()

    def action_submit(self):
        for rec in self:
            if rec.state != "draft":
                raise ValidationError(_("فقط پیش‌نویس قابل ارسال است."))
            if rec.kardex_day_id.attendance_day_id.state not in {"normal", "warning", "resolved"}:
                raise ValidationError(_("اضافه‌کاری فقط پس از بسته‌شدن معتبر روز حضور قابل ارسال است."))
            authorization = self.env["cas.overtime.authorization"].authorization_for(rec.employee_id, rec.work_date)
            values = {"submitted_at": fields.Datetime.now()}
            if authorization:
                values.update({"state": "approved", "authorization_id": authorization.id, "manager_approved_minutes": rec.actual_minutes, "ceo_approved_minutes": rec.actual_minutes, "final_approved_minutes": rec.actual_minutes, "finalized_at": fields.Datetime.now()})
            else:
                manager, role = rec._cas_manager_or_ceo(rec.employee_id)
                if role == "ceo":
                    values.update({"state": "pending_ceo", "manager_user_id": manager.id, "manager_approved_minutes": rec.actual_minutes})
                else:
                    values.update({"state": "pending_manager", "manager_user_id": manager.id})
            rec.with_context(cas_overtime_engine=True, cas_overtime_decision=True).write(values)
            if rec.state == "approved":
                rec.kardex_day_id.recompute()
            else:
                target = rec.company_id.cas_ceo_user_id if rec.state == "pending_ceo" else rec.manager_user_id
                rec.activity_schedule("mail.mail_activity_data_todo", user_id=target.id, summary=_("رسیدگی به اضافه‌کاری %s", rec.number))

    def action_manager_approve(self):
        for rec in self:
            if rec.state != "pending_manager" or not (self.env.is_superuser() or rec.manager_user_id == self.env.user):
                raise AccessError(_("این درخواست در اختیار شما نیست."))
            minutes = rec.manager_approved_minutes
            if not 0 <= minutes <= rec.actual_minutes:
                raise ValidationError(_("مقدار تأیید مدیر معتبر نیست."))
            rec.activity_ids.action_done()
            if minutes == 0:
                rec.with_context(cas_overtime_engine=True).write({"state": "rejected", "finalized_at": fields.Datetime.now()})
            else:
                ceo = rec.company_id.cas_ceo_user_id
                if not ceo:
                    raise ValidationError(_("مدیرعامل شرکت برای مرحله نهایی تنظیم نشده است."))
                rec.with_context(cas_overtime_engine=True).write({"state": "pending_ceo"})
                rec.activity_schedule("mail.mail_activity_data_todo", user_id=ceo.id, summary=_("تصمیم نهایی اضافه‌کاری %s", rec.number))

    def action_ceo_finalize(self):
        for rec in self:
            rec._cas_require_ceo(rec.company_id)
            if rec.state != "pending_ceo":
                raise ValidationError(_("درخواست در مرحله تصمیم مدیرعامل نیست."))
            minutes = rec.ceo_approved_minutes
            if not 0 <= minutes <= rec.manager_approved_minutes:
                raise ValidationError(_("مقدار نهایی مدیرعامل معتبر نیست."))
            rec.activity_ids.action_done()
            rec.with_context(cas_overtime_engine=True).write({
                "state": "approved" if minutes else "rejected", "final_approved_minutes": minutes,
                "finalized_at": fields.Datetime.now(),
            })
            rec.kardex_day_id.recompute()
