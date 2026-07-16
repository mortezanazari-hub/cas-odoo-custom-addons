from datetime import date, datetime, timedelta

from odoo.exceptions import AccessError, ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCasKardexManagement(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        base_group = cls.env.ref("base.group_user")
        cls.manager_user = cls.env["res.users"].create({
            "name": "Kardex Test Manager", "login": "kardex_test_manager",
            "company_id": cls.company.id, "company_ids": [(6, 0, cls.company.ids)],
            "group_ids": [(6, 0, base_group.ids)],
        })
        cls.ceo_user = cls.env["res.users"].create({
            "name": "Kardex Test CEO", "login": "kardex_test_ceo",
            "company_id": cls.company.id, "company_ids": [(6, 0, cls.company.ids)],
            "group_ids": [(6, 0, base_group.ids)],
        })
        cls.company.write({"cas_ceo_user_id": cls.ceo_user.id, "cas_kardex_lock_day": 4})
        cls.manager_employee = cls.env["hr.employee"].create({
            "name": "Kardex Manager Employee", "company_id": cls.company.id, "user_id": cls.manager_user.id,
        })
        cls.employee = cls.env["hr.employee"].create({
            "name": "Kardex Test Employee", "company_id": cls.company.id, "parent_id": cls.manager_employee.id,
        })
        cls.off_employee = cls.env["hr.employee"].create({
            "name": "Kardex Off Test Employee", "company_id": cls.company.id, "parent_id": cls.manager_employee.id,
        })
        cls.auto_employee = cls.env["hr.employee"].create({
            "name": "Kardex Auto OT Employee", "company_id": cls.company.id, "parent_id": cls.manager_employee.id,
        })
        cls.policy = cls.env["cas.attendance.policy"].create({
            "name": "Kardex Simple Policy", "code": "kardex_simple_test", "company_id": cls.company.id,
            "attendance_mode": "simple",
        })
        cls.morning = cls.env["cas.shift.template"].create({
            "name": "Kardex Morning", "code": "kardex_morning_test", "company_id": cls.company.id,
            "start_hour": 7.5, "end_hour": 16.0, "default_break_minutes": 30,
        })
        cls.guard = cls.env["cas.shift.template"].create({
            "name": "Kardex Guard", "code": "kardex_guard_test", "company_id": cls.company.id,
            "shift_kind": "guard", "start_hour": 7.5, "end_hour": 19.5, "default_break_minutes": 30,
        })
        cls.work_pattern = cls.env["cas.shift.pattern"].create({
            "name": "Kardex Work", "code": "kardex_work_test", "company_id": cls.company.id, "cycle_length": 1,
            "line_ids": [(0, 0, {"cycle_day": 1, "day_kind": "work", "template_id": cls.morning.id})],
        })
        cls.guard_pattern = cls.env["cas.shift.pattern"].create({
            "name": "Kardex Guard Pattern", "code": "kardex_guard_pattern_test", "company_id": cls.company.id, "cycle_length": 1,
            "line_ids": [(0, 0, {"cycle_day": 1, "day_kind": "work", "template_id": cls.guard.id})],
        })
        cls.mixed_pattern = cls.env["cas.shift.pattern"].create({
            "name": "Kardex Work Off Work", "code": "kardex_mixed_test", "company_id": cls.company.id, "cycle_length": 3,
            "line_ids": [
                (0, 0, {"cycle_day": 1, "day_kind": "work", "template_id": cls.morning.id}),
                (0, 0, {"cycle_day": 2, "day_kind": "off"}),
                (0, 0, {"cycle_day": 3, "day_kind": "work", "template_id": cls.morning.id}),
            ],
        })
        cls._publish(cls.employee, cls.work_pattern, date(2026, 7, 1), date(2026, 7, 10))
        cls._publish(
            cls.employee, cls.guard_pattern, date(2026, 7, 17), date(2026, 7, 17),
            weekly_rest_day="5", roster_respects_weekly_rest=False, short_day_enabled=True,
        )
        cls._publish(cls.off_employee, cls.mixed_pattern, date(2026, 7, 1), date(2026, 7, 3))
        today = date.today()
        cls.auto_date = today
        cls._publish(cls.auto_employee, cls.work_pattern, today, today)

    @classmethod
    def _publish(cls, employee, pattern, date_from, date_to, **extra):
        values = {
            "name": "Kardex Test Assignment", "company_id": cls.company.id,
            "employee_ids": [(6, 0, employee.ids)], "supervisor_user_id": cls.manager_user.id,
            "policy_id": cls.policy.id, "pattern_id": pattern.id, "anchor_date": date_from,
            "date_from": date_from, "date_to": date_to, "weekly_rest_day": "none", "short_day_enabled": False,
        }
        values.update(extra)
        assignment = cls.env["cas.shift.assignment"].create(values)
        assignment.action_publish()
        return assignment

    def _event(self, employee, work_date, at, kind):
        return self.env["cas.attendance.event"].with_context(cas_attendance_supervisor=True).create({
            "employee_id": employee.id, "work_date": work_date, "occurred_at": at,
            "source": "guard", "event_kind": kind,
        })

    def _presence(self, employee, work_date, start, end):
        self._event(employee, work_date, start, "guard_entry")
        self._event(employee, work_date, end, "guard_exit")
        return self.env["cas.kardex.day"].search([("employee_id", "=", employee.id), ("work_date", "=", work_date)])

    def test_01_eight_hour_presence_requires_break_decision(self):
        day = self._presence(self.employee, date(2026, 7, 1), datetime(2026, 7, 1, 7, 30), datetime(2026, 7, 1, 15, 30))
        self.assertEqual(day.presence_minutes, 480)
        self.assertEqual(day.net_work_minutes, 450)
        self.assertEqual(day.absence_minutes, 30)
        self.assertEqual(day.break_waiver_state, "pending")
        day.write({"break_waiver_reason": "با تأیید سرپرست بدون استراحت کار کرده است"})
        day.action_approve_break_waiver()
        self.assertEqual(day.net_work_minutes, 480)
        self.assertEqual(day.absence_minutes, 0)
        self.assertEqual(day.state, "final")

    def test_02_guard_short_day_keeps_twelve_hours_and_mandatory_overtime(self):
        day = self._presence(self.employee, date(2026, 7, 17), datetime(2026, 7, 17, 7, 30), datetime(2026, 7, 17, 19, 30))
        self.assertEqual(day.planned_base_minutes, 330)
        self.assertEqual(day.presence_minutes, 720)
        self.assertEqual(day.deducted_break_minutes, 30)
        self.assertEqual(day.net_work_minutes, 690)
        self.assertEqual(day.mandatory_overtime_minutes, 360)
        self.assertEqual(day.discretionary_overtime_minutes, 0)

    def test_03_multiday_request_skips_off_day_and_off_only_is_rejected(self):
        request = self.env["cas.attendance.request"].create({
            "employee_id": self.off_employee.id, "request_type": "leave", "duration_type": "multi",
            "date_from": date(2026, 7, 1), "date_to": date(2026, 7, 3), "reason": "آزمون مرخصی چندروزه",
        })
        self.assertEqual(request.requested_minutes, 960)
        request.action_submit()
        self.assertEqual(request.approver_user_id, self.manager_user)
        request.action_approve()
        self.assertEqual(request.state, "approved")
        with self.assertRaises(ValidationError):
            self.env["cas.attendance.request"].create({
                "employee_id": self.off_employee.id, "request_type": "leave", "duration_type": "daily",
                "date_from": date(2026, 7, 2), "date_to": date(2026, 7, 2), "reason": "روز تعطیل",
            })

    def test_04_manager_and_ceo_can_approve_subsets(self):
        day = self._presence(self.employee, date(2026, 7, 4), datetime(2026, 7, 4, 7, 30), datetime(2026, 7, 4, 17, 30))
        self.assertEqual(day.discretionary_overtime_minutes, 90)
        request = self.env["cas.overtime.request"].create({"kardex_day_id": day.id, "reason": "کار واقعی پس از شیفت"})
        request.action_submit()
        self.assertEqual(request.state, "pending_manager")
        request.write({"manager_approved_minutes": 60, "manager_note": "شصت دقیقه قابل قبول"})
        request.action_manager_approve()
        self.assertEqual(request.state, "pending_ceo")
        request.write({"ceo_approved_minutes": 40, "ceo_note": "چهل دقیقه نهایی"})
        request.action_ceo_finalize()
        self.assertEqual(request.final_approved_minutes, 40)
        self.assertEqual(day.approved_overtime_minutes, 40)

    def test_05_ceo_authorization_removes_all_other_approvals(self):
        work_date = self.auto_date
        start = datetime.combine(work_date, datetime.min.time()).replace(hour=7, minute=30)
        day = self._presence(self.auto_employee, work_date, start, start + timedelta(hours=9, minutes=30))
        self.assertEqual(day.discretionary_overtime_minutes, 60)
        authorization = self.env["cas.overtime.authorization"].create({
            "employee_id": self.auto_employee.id, "grant_scope": "grant_date", "reason": "آزمون مجوز مستقیم مدیرعامل",
        })
        request = self.env["cas.overtime.request"].create({"kardex_day_id": day.id, "reason": "اضافه‌کاری دارای مجوز"})
        request.action_submit()
        self.assertEqual(request.state, "approved")
        self.assertEqual(request.authorization_id, authorization)
        self.assertEqual(request.final_approved_minutes, 60)

    def test_06_locked_period_needs_scoped_ceo_reopening(self):
        day = self._presence(self.employee, date(2026, 7, 6), datetime(2026, 7, 6, 7, 30), datetime(2026, 7, 6, 16, 0))
        period = day.period_id
        period.action_lock()
        with self.assertRaises(AccessError):
            day.recompute()
        reopen = self.env["cas.kardex.reopen"].create({
            "period_id": period.id, "scope": "employees", "employee_ids": [(6, 0, self.employee.ids)],
            "date_from": date(2026, 7, 6), "date_to": date(2026, 7, 6), "reason": "دستور آزمون مدیرعامل",
        })
        self.assertTrue(reopen.active)
        day.recompute()
        reopen.action_close()
        with self.assertRaises(AccessError):
            day.recompute()
