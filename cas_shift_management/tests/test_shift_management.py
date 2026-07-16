from datetime import date

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCasShiftManagement(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.supervisor = cls.env["res.users"].create({
            "name": "CAS Shift Test Supervisor",
            "login": "cas_shift_test_supervisor",
            "company_id": cls.company.id,
            "company_ids": [(6, 0, cls.company.ids)],
            "group_ids": [(6, 0, [cls.env.ref("base.group_user").id])],
        })
        cls.employee_1 = cls.env["hr.employee"].create({
            "name": "CAS Shift Test Employee 1", "company_id": cls.company.id,
        })
        cls.employee_2 = cls.env["hr.employee"].create({
            "name": "CAS Shift Test Employee 2", "company_id": cls.company.id,
        })
        cls.simple_policy = cls.env["cas.attendance.policy"].create({
            "name": "Simple Test", "code": "simple_test", "company_id": cls.company.id,
            "attendance_mode": "simple",
        })
        cls.advanced_policy = cls.env["cas.attendance.policy"].create({
            "name": "Advanced Test", "code": "advanced_test", "company_id": cls.company.id,
            "attendance_mode": "advanced",
        })
        cls.morning = cls.env["cas.shift.template"].create({
            "name": "Morning Test", "code": "morning_test", "company_id": cls.company.id,
            "start_hour": 7.5, "end_hour": 16.0, "default_break_minutes": 30,
        })
        cls.short = cls.env["cas.shift.template"].create({
            "name": "Short Test", "code": "short_test", "company_id": cls.company.id,
            "start_hour": 7.5, "end_hour": 13.0, "default_break_minutes": 0,
        })
        cls.guard = cls.env["cas.shift.template"].create({
            "name": "Guard Day Test", "code": "guard_test", "company_id": cls.company.id,
            "shift_kind": "guard", "start_hour": 7.5, "end_hour": 19.5,
            "default_break_minutes": 30,
        })
        cls.regular_pattern = cls.env["cas.shift.pattern"].create({
            "name": "Every Day Morning", "code": "every_day_morning", "company_id": cls.company.id,
            "cycle_length": 1,
            "line_ids": [(0, 0, {"cycle_day": 1, "day_kind": "work", "template_id": cls.morning.id})],
        })
        cls.guard_pattern = cls.env["cas.shift.pattern"].create({
            "name": "Every Day Guard", "code": "every_day_guard", "company_id": cls.company.id,
            "cycle_length": 1,
            "line_ids": [(0, 0, {"cycle_day": 1, "day_kind": "work", "template_id": cls.guard.id})],
        })

    def _assignment(self, employee, policy, pattern, date_from, date_to, **extra):
        values = {
            "name": "Test Assignment", "company_id": self.company.id,
            "employee_ids": [(6, 0, employee.ids)], "supervisor_user_id": self.supervisor.id,
            "policy_id": policy.id, "pattern_id": pattern.id,
            "anchor_date": date_from, "date_from": date_from, "date_to": date_to,
        }
        values.update(extra)
        return self.env["cas.shift.assignment"].create(values)

    def test_effective_dated_mode_is_snapshotted(self):
        first = self._assignment(
            self.employee_1, self.simple_policy, self.regular_pattern,
            date(2026, 7, 1), date(2026, 7, 15), weekly_rest_day="none", short_day_enabled=False,
        )
        second = self._assignment(
            self.employee_1, self.advanced_policy, self.regular_pattern,
            date(2026, 7, 16), date(2026, 7, 31), weekly_rest_day="none", short_day_enabled=False,
        )
        first.action_publish()
        second.action_publish()
        day_15 = self.env["cas.shift.day"].search([
            ("employee_id", "=", self.employee_1.id), ("schedule_date", "=", date(2026, 7, 15))
        ])
        day_16 = self.env["cas.shift.day"].search([
            ("employee_id", "=", self.employee_1.id), ("schedule_date", "=", date(2026, 7, 16))
        ])
        self.assertEqual(day_15.attendance_mode, "simple")
        self.assertEqual(day_16.attendance_mode, "advanced")

    def test_short_day_and_guard_mandatory_overtime(self):
        assignment = self._assignment(
            self.employee_1, self.simple_policy, self.guard_pattern,
            date(2026, 7, 17), date(2026, 7, 17),
            weekly_rest_day="5", roster_respects_weekly_rest=False,
            roster_respects_official_holiday=False,
        )
        assignment.action_publish()
        day = assignment.day_ids
        self.assertTrue(day.rule_is_short_day)
        self.assertEqual(day.base_work_minutes, 330)
        self.assertEqual(day.required_presence_minutes, 720)
        self.assertEqual(day.break_minutes, 30)
        self.assertEqual(day.mandatory_overtime_minutes, 360)

    def test_swap_moves_each_employees_complete_rule(self):
        first = self._assignment(
            self.employee_1, self.simple_policy, self.regular_pattern,
            date(2026, 7, 15), date(2026, 7, 17),
            weekly_rest_day="5", short_day_template_id=self.short.id,
        )
        second = self._assignment(
            self.employee_2, self.simple_policy, self.regular_pattern,
            date(2026, 7, 15), date(2026, 7, 17),
            weekly_rest_day="4", short_day_template_id=self.short.id,
        )
        first.action_publish()
        second.action_publish()
        swap = self.env["cas.shift.swap"].create({
            "name": "Wednesday Friday Test", "company_id": self.company.id,
            "date_a": date(2026, 7, 15), "date_b": date(2026, 7, 17),
            "scope": "employees", "employee_ids": [(6, 0, (self.employee_1 | self.employee_2).ids)],
            "reason": "Automated test",
        })
        swap.action_apply()
        employee_1_wednesday = self.env["cas.shift.day"].search([
            ("employee_id", "=", self.employee_1.id), ("schedule_date", "=", date(2026, 7, 15))
        ])
        employee_2_wednesday = self.env["cas.shift.day"].search([
            ("employee_id", "=", self.employee_2.id), ("schedule_date", "=", date(2026, 7, 15))
        ])
        self.assertEqual(employee_1_wednesday.base_work_minutes, 330)
        self.assertEqual(employee_1_wednesday.template_id, self.short)
        self.assertTrue(employee_1_wednesday.rule_is_short_day)
        self.assertEqual(employee_1_wednesday.rule_origin_date, date(2026, 7, 17))
        self.assertEqual(employee_2_wednesday.day_kind, "off_weekly")
        self.assertTrue(employee_2_wednesday.rule_is_weekly_rest)
        self.assertEqual(swap.affected_count, 2)

    def test_incomplete_pattern_and_overlap_are_rejected(self):
        incomplete = self.env["cas.shift.pattern"].create({
            "name": "Incomplete", "code": "incomplete", "company_id": self.company.id,
            "cycle_length": 2,
            "line_ids": [(0, 0, {"cycle_day": 1, "day_kind": "work", "template_id": self.morning.id})],
        })
        assignment = self._assignment(
            self.employee_1, self.simple_policy, incomplete,
            date(2026, 8, 1), date(2026, 8, 2), weekly_rest_day="none", short_day_enabled=False,
        )
        with self.assertRaises(ValidationError):
            assignment.action_publish()

        valid = self._assignment(
            self.employee_1, self.simple_policy, self.regular_pattern,
            date(2026, 8, 1), date(2026, 8, 2), weekly_rest_day="none", short_day_enabled=False,
        )
        valid.action_publish()
        overlapping = self._assignment(
            self.employee_1, self.simple_policy, self.regular_pattern,
            date(2026, 8, 2), date(2026, 8, 3), weekly_rest_day="none", short_day_enabled=False,
        )
        with self.assertRaises(ValidationError):
            overlapping.action_publish()

    def test_generated_days_are_append_only(self):
        assignment = self._assignment(
            self.employee_1, self.simple_policy, self.regular_pattern,
            date(2026, 9, 1), date(2026, 9, 1), weekly_rest_day="none", short_day_enabled=False,
        )
        assignment.action_publish()
        with self.assertRaises(ValidationError):
            assignment.day_ids.unlink()
