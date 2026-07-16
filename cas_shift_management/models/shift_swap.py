from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CasShiftSwap(models.Model):
    _name = "cas.shift.swap"
    _description = "CAS Bulk Day Rule Swap"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc, id desc"

    name = fields.Char(string="عنوان جابه‌جایی", required=True, tracking=True)
    company_id = fields.Many2one(
        "res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True
    )
    date_a = fields.Date(string="روز اول", required=True, tracking=True)
    date_b = fields.Date(string="روز دوم", required=True, tracking=True)
    scope = fields.Selection(
        [("company", "کل شرکت"), ("department", "واحد"), ("employees", "افراد منتخب")],
        string="دامنه", required=True, default="company", tracking=True,
    )
    department_id = fields.Many2one("hr.department", string="واحد", ondelete="restrict")
    employee_ids = fields.Many2many(
        "hr.employee", "cas_shift_swap_employee_rel", "swap_id", "employee_id", string="افراد منتخب"
    )
    reason = fields.Text(string="دلیل", required=True)
    state = fields.Selection(
        [("draft", "پیش‌نویس"), ("applied", "اعمال‌شده")], default="draft", required=True, readonly=True, tracking=True
    )
    applied_at = fields.Datetime(string="زمان اعمال", readonly=True)
    applied_by_id = fields.Many2one("res.users", string="اعمال‌کننده", readonly=True)
    affected_count = fields.Integer(string="تعداد افراد", readonly=True)

    @api.constrains("date_a", "date_b", "scope", "department_id", "employee_ids", "company_id")
    def _check_contract(self):
        for swap in self:
            if swap.date_a == swap.date_b:
                raise ValidationError(_("دو تاریخ جابه‌جایی باید متفاوت باشند."))
            if swap.scope == "department" and not swap.department_id:
                raise ValidationError(_("برای دامنه واحد باید واحد انتخاب شود."))
            if swap.scope == "employees" and not swap.employee_ids:
                raise ValidationError(_("برای دامنه افراد باید حداقل یک نفر انتخاب شود."))
            if swap.department_id and swap.department_id.company_id and swap.department_id.company_id != swap.company_id:
                raise ValidationError(_("واحد خارج از شرکت جابه‌جایی است."))
            if any(employee.company_id != swap.company_id for employee in swap.employee_ids.sudo()):
                raise ValidationError(_("همه افراد منتخب باید متعلق به شرکت باشند."))

    def write(self, vals):
        protected = {"company_id", "date_a", "date_b", "scope", "department_id", "employee_ids", "reason"}
        if protected.intersection(vals) and any(swap.state != "draft" for swap in self):
            raise ValidationError(_("جابه‌جایی اعمال‌شده قابل تغییر نیست."))
        if "state" in vals and not self.env.context.get("cas_shift_engine"):
            raise ValidationError(_("وضعیت فقط از عملیات رسمی تغییر می‌کند."))
        return super().write(vals)

    def unlink(self):
        if any(swap.state != "draft" for swap in self):
            raise ValidationError(_("جابه‌جایی اعمال‌شده قابل حذف نیست."))
        return super().unlink()

    def _target_employees(self):
        self.ensure_one()
        if self.scope == "employees":
            return self.employee_ids.sudo().filtered("active")
        days = self.env["cas.shift.day"].sudo().search([
            ("company_id", "=", self.company_id.id),
            ("schedule_date", "in", [self.date_a, self.date_b]),
            ("state", "=", "planned"),
        ])
        employees = days.mapped("employee_id").filtered("active")
        if self.scope == "department":
            department_ids = self.env["hr.department"].sudo().search([
                ("id", "child_of", self.department_id.id)
            ]).ids
            employees = employees.filtered(lambda employee: employee.department_id.id in department_ids)
        return employees

    def action_apply(self):
        for swap in self:
            if not (self.env.is_superuser() or self.env.user.has_group("cas_shift_management.group_cas_shift_manager")):
                raise AccessError(_("مجوز اعمال جابه‌جایی روزها را ندارید."))
            if swap.state != "draft":
                raise ValidationError(_("این جابه‌جایی قبلاً اعمال شده است."))
            employees = swap._target_employees()
            if not employees:
                raise ValidationError(_("هیچ کارمند فعالی در دامنه انتخابی وجود ندارد."))
            days = self.env["cas.shift.day"].sudo().search([
                ("employee_id", "in", employees.ids),
                ("schedule_date", "in", [swap.date_a, swap.date_b]),
                ("state", "=", "planned"),
            ])
            by_key = {(day.employee_id.id, day.schedule_date): day for day in days}
            missing = employees.filtered(
                lambda employee: (employee.id, swap.date_a) not in by_key or (employee.id, swap.date_b) not in by_key
            )
            if missing:
                raise ValidationError(_("برای %s نفر در یکی از دو تاریخ برنامه روزانه موجود نیست.") % len(missing))
            for employee in employees:
                first = by_key[(employee.id, swap.date_a)]
                second = by_key[(employee.id, swap.date_b)]
                first_snapshot, second_snapshot = first._snapshot(), second._snapshot()
                first.with_context(cas_shift_engine=True).write(
                    first._values_from_snapshot(second_snapshot, swap.date_a, swap)
                )
                second.with_context(cas_shift_engine=True).write(
                    second._values_from_snapshot(first_snapshot, swap.date_b, swap)
                )
            swap.with_context(cas_shift_engine=True).write({
                "state": "applied", "applied_at": fields.Datetime.now(),
                "applied_by_id": self.env.user.id, "affected_count": len(employees),
            })
        return True
