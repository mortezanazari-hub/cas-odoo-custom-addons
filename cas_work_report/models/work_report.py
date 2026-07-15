from __future__ import annotations

from datetime import timedelta
from io import BytesIO

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
import xlsxwriter

from ..hooks import WORKFLOW_CODE


class CasWorkStation(models.Model):
    _name = "cas.work.station"
    _description = "CAS Work Station"
    _inherit = ["mail.thread"]
    _order = "department_id, sequence, name"

    sequence = fields.Integer(default=10)
    name = fields.Char(string="ایستگاه کاری", required=True, tracking=True)
    code = fields.Char(string="کد فنی", required=True, index=True)
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company, index=True
    )
    department_id = fields.Many2one(
        "hr.department", string="واحد میزبان", required=True, ondelete="restrict", index=True
    )
    supervisor_user_id = fields.Many2one(
        "res.users",
        string="سرپرست پیش‌فرض",
        required=True,
        ondelete="restrict",
        domain="[('active', '=', True), ('share', '=', False)]",
        tracking=True,
    )
    normal_shift_hours = fields.Float(string="ساعات عادی شیفت", default=8.0)
    active = fields.Boolean(default=True, tracking=True)

    _code_company_uniq = models.Constraint(
        "UNIQUE(code, company_id)", "کد ایستگاه کاری باید در هر شرکت یکتا باشد."
    )
    _shift_positive = models.Constraint(
        "CHECK(normal_shift_hours > 0)", "ساعات عادی شیفت باید بیشتر از صفر باشد."
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
        return super().write(vals)

    @api.constrains("company_id", "department_id", "supervisor_user_id")
    def _check_company_contract(self):
        for station in self:
            if station.department_id.company_id and station.department_id.company_id != station.company_id:
                raise ValidationError(_("واحد و ایستگاه کاری باید متعلق به یک شرکت باشند."))
            user = station.supervisor_user_id.with_context(active_test=False)
            if not user.active or user.share or station.company_id not in user.company_ids:
                raise ValidationError(_("سرپرست ایستگاه باید کاربر داخلی، فعال و عضو شرکت باشد."))


class CasWorkReportDelegation(models.Model):
    _name = "cas.work.report.delegation"
    _description = "CAS Work Report Representation Permission"
    _inherit = ["mail.thread"]
    _order = "date_from desc, id desc"
    _rec_name = "representative_user_id"

    representative_user_id = fields.Many2one(
        "res.users", string="نماینده ثبت", required=True, ondelete="restrict", index=True
    )
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company, index=True
    )
    scope = fields.Selection(
        [("all", "همه کارکنان شرکت"), ("departments", "واحدهای مشخص")],
        string="محدوده نمایندگی",
        required=True,
        default="departments",
    )
    department_ids = fields.Many2many(
        "hr.department", "cas_work_report_delegation_department_rel", "delegation_id", "department_id", string="واحدهای مجاز"
    )
    date_from = fields.Date(string="از تاریخ", required=True, default=fields.Date.context_today, index=True)
    date_to = fields.Date(string="تا تاریخ", index=True)
    reason = fields.Text(string="دلیل نمایندگی", required=True)
    active = fields.Boolean(default=True, tracking=True)

    @api.constrains("date_from", "date_to", "scope", "department_ids", "company_id")
    def _check_contract(self):
        for delegation in self:
            if delegation.date_to and delegation.date_to < delegation.date_from:
                raise ValidationError(_("تاریخ پایان نمایندگی نمی‌تواند قبل از تاریخ شروع باشد."))
            if delegation.scope == "departments" and not delegation.department_ids:
                raise ValidationError(_("برای نمایندگی محدود باید حداقل یک واحد انتخاب شود."))
            if any(dep.company_id and dep.company_id != delegation.company_id for dep in delegation.department_ids):
                raise ValidationError(_("همه واحدهای نمایندگی باید متعلق به همان شرکت باشند."))

    def allows(self, employee, report_date):
        self.ensure_one()
        employee = employee.sudo()
        return bool(
            self.active
            and self.company_id == employee.company_id
            and self.date_from <= report_date
            and (not self.date_to or self.date_to >= report_date)
            and (self.scope == "all" or employee.department_id in self.department_ids)
        )


class CasWorkReport(models.Model):
    _name = "cas.work.report"
    _description = "CAS Daily Work Report"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "work_date desc, id desc"
    _rec_name = "number"

    number = fields.Char(string="شماره رهگیری", default="New", readonly=True, copy=False, index=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, index=True)
    work_date = fields.Date(string="تاریخ کار", required=True, default=fields.Date.context_today, index=True, tracking=True)
    employee_id = fields.Many2one("hr.employee", string="کارمند", required=True, ondelete="restrict", index=True, tracking=True)
    employee_department_id = fields.Many2one("hr.department", string="واحد سازمانی کارمند", readonly=True, store=True, index=True)
    work_station_id = fields.Many2one("cas.work.station", string="ایستگاه کاری", required=True, ondelete="restrict", index=True, tracking=True)
    station_department_id = fields.Many2one(related="work_station_id.department_id", string="واحد محل کار", store=True, index=True)
    supervisor_user_id = fields.Many2one("res.users", string="سرپرست تأییدکننده", required=True, ondelete="restrict", index=True, tracking=True)
    submitted_by_id = fields.Many2one("res.users", string="ثبت‌کننده", readonly=True, index=True)
    representation_delegation_id = fields.Many2one("cas.work.report.delegation", string="مجوز نمایندگی", readonly=True, ondelete="restrict")
    is_representative_entry = fields.Boolean(string="ثبت به نمایندگی", readonly=True, index=True)
    shift_start = fields.Datetime(string="شروع کار/شیفت", required=True, tracking=True)
    shift_end = fields.Datetime(string="پایان کار/شیفت", required=True, tracking=True)
    duration_hours = fields.Float(string="مدت کار (ساعت)", compute="_compute_hours", store=True)
    normal_hours = fields.Float(string="ساعات عادی", compute="_compute_hours", store=True)
    overtime_hours = fields.Float(string="اضافه‌کاری", compute="_compute_hours", store=True)
    submission_deadline = fields.Datetime(string="مهلت ثبت", compute="_compute_deadline", store=True, index=True)
    submitted_at = fields.Datetime(string="زمان ارسال", readonly=True, index=True)
    is_late = fields.Boolean(string="ثبت با تأخیر", readonly=True, index=True)
    late_reason = fields.Text(string="دلیل ثبت با تأخیر")
    task_title = fields.Char(string="عنوان فعالیت", required=True, tracking=True)
    description = fields.Text(string="شرح فعالیت", required=True)
    result = fields.Text(string="نتیجه/خروجی")
    issues = fields.Text(string="مشکلات و موانع")
    workflow_instance_id = fields.Many2one("cas.workflow.instance", readonly=True, copy=False, ondelete="restrict")
    state_code = fields.Char(related="workflow_instance_id.current_state_id.code", string="وضعیت", store=True, readonly=True, index=True)
    state = fields.Selection(
        [("draft", "پیش‌نویس"), ("pending", "در انتظار تأیید"), ("approved", "تأییدشده"), ("rejected", "ردشده")],
        string="وضعیت گزارش",
        compute="_compute_state",
        store=True,
        readonly=True,
        index=True,
    )
    approval_request_id = fields.Many2one("cas.approval.request", compute="_compute_approval_request", string="درخواست تأیید")
    authorized_user_ids = fields.Many2many(
        "res.users", "cas_work_report_authorized_user_rel", "report_id", "user_id", string="کاربران مجاز", readonly=True
    )

    @api.depends("shift_start", "shift_end", "work_station_id.normal_shift_hours")
    def _compute_hours(self):
        for report in self:
            duration = 0.0
            if report.shift_start and report.shift_end and report.shift_end > report.shift_start:
                duration = (report.shift_end - report.shift_start).total_seconds() / 3600.0
            normal_limit = report.work_station_id.normal_shift_hours or 0.0
            report.duration_hours = duration
            report.normal_hours = min(duration, normal_limit) if normal_limit else duration
            report.overtime_hours = max(duration - normal_limit, 0.0) if normal_limit else 0.0

    @api.depends("shift_end")
    def _compute_deadline(self):
        for report in self:
            report.submission_deadline = report.shift_end + timedelta(hours=12) if report.shift_end else False

    @api.depends("workflow_instance_id.approval_request_ids", "workflow_instance_id.approval_request_ids.status")
    def _compute_approval_request(self):
        for report in self:
            requests = report.workflow_instance_id.approval_request_ids.sorted("id", reverse=True)
            report.approval_request_id = requests[:1]

    @api.depends("state_code")
    def _compute_state(self):
        for report in self:
            report.state = report.state_code if report.state_code in {"draft", "pending", "approved", "rejected"} else False

    @api.onchange("work_station_id")
    def _onchange_work_station_id(self):
        if self.work_station_id:
            self.supervisor_user_id = self.work_station_id.supervisor_user_id

    @api.constrains("shift_start", "shift_end")
    def _check_shift_range(self):
        for report in self:
            if report.shift_start and report.shift_end and report.shift_end <= report.shift_start:
                raise ValidationError(_("زمان پایان باید بعد از زمان شروع باشد."))

    @api.constrains("company_id", "employee_id", "work_station_id", "supervisor_user_id")
    def _check_company_contract(self):
        for report in self:
            employee = report.employee_id.sudo()
            if employee.company_id != report.company_id or report.work_station_id.company_id != report.company_id:
                raise ValidationError(_("کارمند، ایستگاه و گزارش باید متعلق به یک شرکت باشند."))
            supervisor = report.supervisor_user_id.with_context(active_test=False)
            if not supervisor.active or supervisor.share or report.company_id not in supervisor.company_ids:
                raise ValidationError(_("سرپرست تأییدکننده معتبر نیست."))

    @api.model
    def _active_actor_employees(self, user, company):
        return user.sudo().employee_ids.with_context(active_test=False).filtered(
            lambda emp: emp.active and emp.company_id == company
        )

    @api.model
    def _is_manager_of(self, user, employee, direct=False):
        employee = employee.sudo()
        actor_ids = set(self._active_actor_employees(user, employee.company_id).ids)
        manager = employee.parent_id
        while manager:
            if manager.id in actor_ids:
                return True
            if direct:
                return False
            manager = manager.parent_id
        return False

    @api.model
    def _find_representation(self, user, employee, report_date):
        employee = employee.sudo()
        delegations = self.env["cas.work.report.delegation"].sudo().search(
            [
                ("representative_user_id", "=", user.id),
                ("company_id", "=", employee.company_id.id),
                ("active", "=", True),
                ("date_from", "<=", report_date),
                "|",
                ("date_to", "=", False),
                ("date_to", ">=", report_date),
            ],
            order="date_from desc, id desc",
        )
        return delegations.filtered(lambda delegation: delegation.allows(employee, report_date))[:1]

    @api.model
    def _authorize_employee_entry(self, user, employee, report_date):
        employee = employee.sudo()
        if user.has_group("cas_work_report.group_cas_work_report_manager"):
            return False
        if employee in self._active_actor_employees(user, employee.company_id):
            return False
        if self._is_manager_of(user, employee):
            return False
        delegation = self._find_representation(user, employee, report_date)
        if delegation:
            return delegation
        raise AccessError(_("برای ثبت گزارش این کارمند مجوز نمایندگی یا مدیریت ندارید."))

    @api.model
    def _authorized_users_for(self, employee, submitter, supervisor):
        employee = employee.sudo()
        users = submitter | supervisor | employee.user_id
        manager = employee.parent_id
        while manager:
            users |= manager.user_id
            manager = manager.parent_id
        department = employee.department_id
        while department:
            users |= department.manager_id.user_id
            department = department.parent_id
        return users.filtered(lambda user: user.active and not user.share)

    @api.model_create_multi
    def create(self, vals_list):
        reports = self.browse()
        for original in vals_list:
            vals = dict(original)
            employee = self.env["hr.employee"].sudo().browse(vals.get("employee_id")).exists()
            station = self.env["cas.work.station"].browse(vals.get("work_station_id")).exists()
            report_date = fields.Date.to_date(vals.get("work_date") or fields.Date.context_today(self))
            if not employee or not station:
                raise ValidationError(_("کارمند و ایستگاه کاری معتبر الزامی است."))
            delegation = self._authorize_employee_entry(self.env.user, employee, report_date)
            supervisor = self.env["res.users"].browse(
                vals.get("supervisor_user_id") or station.supervisor_user_id.id
            ).exists()
            vals.update(
                {
                    "number": self.env["ir.sequence"].next_by_code("cas.work.report") or "New",
                    "company_id": employee.company_id.id,
                    "employee_department_id": employee.department_id.id,
                    "supervisor_user_id": supervisor.id,
                    "submitted_by_id": self.env.user.id,
                    "representation_delegation_id": delegation.id if delegation else False,
                    "is_representative_entry": employee not in self._active_actor_employees(self.env.user, employee.company_id),
                    "authorized_user_ids": [(6, 0, self._authorized_users_for(employee, self.env.user, supervisor).ids)],
                }
            )
            report = super(CasWorkReport, self).create(vals)
            definition = self.env["cas.workflow.definition"].search(
                [("code", "=", WORKFLOW_CODE), ("company_id", "=", report.company_id.id)], limit=1
            )
            if not definition or not definition.current_version_id:
                raise ValidationError(_("گردش‌کار فعال گزارش کار برای این شرکت پیکربندی نشده است."))
            started = definition.action_start(report.id, responsible_user_id=supervisor.id)
            report.with_context(cas_work_report_engine=True).write({"workflow_instance_id": started["instance_id"]})
            reports |= report
        return reports

    def write(self, vals):
        if not self.env.context.get("cas_work_report_engine"):
            protected = {"number", "company_id", "submitted_by_id", "representation_delegation_id", "is_representative_entry", "workflow_instance_id", "authorized_user_ids", "employee_department_id"}
            if protected.intersection(vals):
                raise ValidationError(_("فیلدهای سیستمی گزارش قابل ویرایش مستقیم نیستند."))
            if any(report.state_code != "draft" for report in self):
                raise ValidationError(_("فقط گزارش پیش‌نویس قابل ویرایش است."))
        return super().write(vals)

    def unlink(self):
        raise ValidationError(_("گزارش کار و سابقه آن قابل حذف نیست؛ در صورت نیاز آن را بایگانی کنید."))

    def _cas_workflow_authorize_responsible_assignment(self, responsible):
        self.ensure_one()
        return bool(
            responsible == self.supervisor_user_id
            and self.submitted_by_id == self.env.user
            and self.env.user in self.authorized_user_ids
        )

    def _cas_workflow_user_can_execute_transition(self, instance, transition, user):
        self.ensure_one()
        return bool(
            instance == self.workflow_instance_id
            and transition.code == "submit"
            and self.state_code == "draft"
            and user == self.submitted_by_id
            and user in self.authorized_user_ids
        )

    def action_submit(self):
        self.ensure_one()
        self.check_access("write")
        if self.state_code != "draft":
            raise ValidationError(_("فقط گزارش پیش‌نویس قابل ارسال است."))
        now = fields.Datetime.now()
        late = bool(self.submission_deadline and now > self.submission_deadline)
        if late and not (
            self.env.user.has_group("cas_work_report.group_cas_work_report_manager")
            and str(self.late_reason or "").strip()
        ):
            raise ValidationError(_("مهلت ثبت گزارش گذشته است؛ ثبت دیرهنگام فقط با مجوز مدیر و درج دلیل ممکن است."))
        transition = self.workflow_instance_id.version_id.transition_ids.filtered(
            lambda item: item.code == "submit" and item.from_state_id == self.workflow_instance_id.current_state_id
        )[:1]
        if not transition:
            raise ValidationError(_("انتقال ارسال گزارش در نسخه جاری پیدا نشد."))
        self.workflow_instance_id.action_execute_transition(transition.id, note=_("گزارش کار %s ارسال شد.", self.number))
        self.with_context(cas_work_report_engine=True).write({"submitted_at": now, "is_late": late})
        request = self.workflow_instance_id.approval_request_ids.filtered(lambda item: item.status == "pending")[:1]
        if self._is_manager_of(self.env.user, self.employee_id, direct=True) and request:
            own_line = request.line_ids.filtered(
                lambda line: line.status == "pending" and line.approver_user_id == self.env.user
            )[:1]
            if own_line:
                own_line.action_approve(comment=_("ثبت و تأیید مستقیم توسط مدیر مستقیم"))
        return True

    @api.model
    def _xlsx_bytes(self, reports):
        reports.check_access("read")
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        sheet = workbook.add_worksheet("Work Reports")
        header = workbook.add_format({"bold": True, "bg_color": "#D9EAD3", "border": 1})
        date_format = workbook.add_format({"num_format": "yyyy-mm-dd"})
        columns = [
            "شماره رهگیری", "تاریخ کار", "کارمند", "واحد سازمانی", "ایستگاه کاری",
            "واحد محل کار", "سرپرست", "ثبت‌کننده", "وضعیت", "عنوان فعالیت",
            "شرح فعالیت", "نتیجه", "مشکلات", "ساعت کار", "ساعت عادی", "اضافه‌کاری",
            "مهلت ثبت", "زمان ارسال", "ثبت با تأخیر",
        ]
        for col, title in enumerate(columns):
            sheet.write(0, col, title, header)
        for row, report in enumerate(reports, start=1):
            values = [
                report.number, report.work_date, report.employee_id.name, report.employee_department_id.name,
                report.work_station_id.name, report.station_department_id.name, report.supervisor_user_id.name,
                report.submitted_by_id.name, report.workflow_instance_id.current_state_id.name, report.task_title,
                report.description, report.result or "", report.issues or "", report.duration_hours,
                report.normal_hours, report.overtime_hours, report.submission_deadline, report.submitted_at,
                "بله" if report.is_late else "خیر",
            ]
            for col, value in enumerate(values):
                if col == 1 and value:
                    sheet.write_datetime(row, col, fields.Date.to_date(value), date_format)
                else:
                    sheet.write(row, col, value or "")
        sheet.freeze_panes(1, 0)
        sheet.autofilter(0, 0, max(len(reports), 1), len(columns) - 1)
        sheet.set_column(0, len(columns) - 1, 18)
        workbook.close()
        return output.getvalue()


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def write(self, vals):
        result = super().write(vals)
        if {"parent_id", "department_id", "user_id", "active"}.intersection(vals):
            reports = self.env["cas.work.report"].sudo().search([("employee_id", "child_of", self.ids)])
            for report in reports:
                users = report._authorized_users_for(report.employee_id, report.submitted_by_id, report.supervisor_user_id)
                report.with_context(cas_work_report_engine=True).write({"authorized_user_ids": [(6, 0, users.ids)]})
        return result
