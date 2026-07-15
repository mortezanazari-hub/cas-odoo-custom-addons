from datetime import timedelta

from odoo import fields
from odoo.exceptions import AccessError, ValidationError
from odoo.tests.common import TransactionCase


class TestCasWorkReport(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_group = cls.env.ref("cas_work_report.group_cas_work_report_user")
        cls.manager_group = cls.env.ref("cas_work_report.group_cas_work_report_manager")
        cls.department = cls.env["hr.department"].create(
            {"name": "واحد تست گزارش کار", "company_id": cls.env.company.id}
        )
        cls.supervisor_user = cls._make_user("supervisor")
        cls.reporter_user = cls._make_user("reporter")
        cls.representative_user = cls._make_user("representative")
        cls.outsider_user = cls._make_user("outsider")
        cls.supervisor_employee = cls.env["hr.employee"].create(
            {
                "name": "سرپرست تست",
                "user_id": cls.supervisor_user.id,
                "department_id": cls.department.id,
                "company_id": cls.env.company.id,
            }
        )
        cls.reporter_employee = cls.env["hr.employee"].create(
            {
                "name": "کارمند گزارش‌دهنده",
                "user_id": cls.reporter_user.id,
                "department_id": cls.department.id,
                "parent_id": cls.supervisor_employee.id,
                "company_id": cls.env.company.id,
            }
        )
        cls.no_user_employee = cls.env["hr.employee"].create(
            {
                "name": "کارمند بدون کاربر",
                "department_id": cls.department.id,
                "parent_id": cls.supervisor_employee.id,
                "company_id": cls.env.company.id,
            }
        )
        cls.department.manager_id = cls.supervisor_employee
        cls.station = cls.env["cas.work.station"].create(
            {
                "name": "ایستگاه بسته‌بندی تست",
                "code": "test_packaging",
                "company_id": cls.env.company.id,
                "department_id": cls.department.id,
                "supervisor_user_id": cls.supervisor_user.id,
                "normal_shift_hours": 8,
            }
        )

    @classmethod
    def _make_user(cls, suffix):
        return cls.env["res.users"].with_context(no_reset_password=True).create(
            {
                "name": f"Work Report {suffix}",
                "login": f"cas_work_report_{suffix}",
                "company_id": cls.env.company.id,
                "company_ids": [(6, 0, cls.env.companies.ids)],
                "group_ids": [(6, 0, [cls.env.ref("base.group_user").id, cls.user_group.id])],
            }
        )

    def _values(self, employee=None, start=None, end=None):
        start = start or fields.Datetime.now() - timedelta(hours=8)
        end = end or fields.Datetime.now() - timedelta(minutes=10)
        return {
            "work_date": fields.Date.context_today(self.env.user),
            "employee_id": (employee or self.reporter_employee).id,
            "work_station_id": self.station.id,
            "shift_start": start,
            "shift_end": end,
            "task_title": "فعالیت تست خودکار",
            "description": "شرح کامل فعالیت تست خودکار",
            "result": "خروجی تست",
        }

    def test_self_report_routes_to_supervisor_and_approves(self):
        report = self.env["cas.work.report"].with_user(self.reporter_user).create(self._values())
        self.assertEqual(report.state_code, "draft")
        self.assertEqual(report.workflow_instance_id.started_by_id, self.reporter_user)
        self.assertEqual(report.workflow_instance_id.responsible_user_id, self.supervisor_user)
        self.assertAlmostEqual(report.duration_hours, 7.833333, places=3)
        report.action_submit()
        self.assertEqual(report.state_code, "pending")
        request = report.approval_request_id
        self.assertEqual(request.line_ids.approver_user_id, self.supervisor_user)
        request.line_ids.with_user(self.supervisor_user).action_approve("تأیید تست")
        self.assertEqual(report.state_code, "approved")
        self.assertTrue(report.submitted_at)

    def test_representation_requires_permission(self):
        with self.assertRaises(AccessError):
            self.env["cas.work.report"].with_user(self.representative_user).create(
                self._values(employee=self.no_user_employee)
            )
        delegation = self.env["cas.work.report.delegation"].create(
            {
                "representative_user_id": self.representative_user.id,
                "company_id": self.env.company.id,
                "scope": "departments",
                "department_ids": [(6, 0, [self.department.id])],
                "date_from": fields.Date.context_today(self.env.user),
                "reason": "پوشش ثبت کارکنان بدون کاربر",
            }
        )
        report = self.env["cas.work.report"].with_user(self.representative_user).create(
            self._values(employee=self.no_user_employee)
        )
        self.assertTrue(report.is_representative_entry)
        self.assertEqual(report.representation_delegation_id, delegation)

    def test_direct_manager_entry_is_formally_auto_approved(self):
        report = self.env["cas.work.report"].with_user(self.supervisor_user).create(
            self._values(employee=self.reporter_employee)
        )
        report.action_submit()
        self.assertEqual(report.state_code, "approved")
        self.assertEqual(report.approval_request_id.status, "approved")
        self.assertEqual(report.approval_request_id.line_ids.decision_user_id, self.supervisor_user)

    def test_late_submission_is_blocked_for_normal_user(self):
        start = fields.Datetime.now() - timedelta(hours=30)
        end = fields.Datetime.now() - timedelta(hours=20)
        report = self.env["cas.work.report"].with_user(self.reporter_user).create(
            self._values(start=start, end=end)
        )
        with self.assertRaises(ValidationError):
            report.action_submit()

    def test_excel_payload_and_immutable_history(self):
        report = self.env["cas.work.report"].with_user(self.reporter_user).create(self._values())
        payload = self.env["cas.work.report"]._xlsx_bytes(report)
        self.assertTrue(payload.startswith(b"PK"))
        self.assertGreater(len(payload), 1000)
        with self.assertRaises(ValidationError):
            report.unlink()
