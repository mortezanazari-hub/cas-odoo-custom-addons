from datetime import datetime

from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestCasAttendanceCore(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.employee = cls.env["hr.employee"].create({"name": "کارمند آزمون حضور"})
        cls.Event = cls.env["cas.attendance.event"].with_context(cas_attendance_supervisor=True)

    def _event(self, at, source, kind, work_date="2026-07-10", **extra):
        values = {
            "employee_id": self.employee.id, "occurred_at": at, "source": source,
            "event_kind": kind, "work_date": work_date,
        }
        values.update(extra)
        return self.Event.create(values)

    def test_01_minute_precision_and_immutable_raw_event(self):
        event = self._event(datetime(2026, 7, 10, 7, 30, 49), "guard", "guard_entry")
        self.assertEqual(event.occurred_at.second, 0)
        with self.assertRaises(AccessError):
            event.write({"occurred_at": datetime(2026, 7, 10, 7, 31)})
        with self.assertRaises(AccessError):
            event.unlink()
        event.write({"void_reason": "ثبت اشتباه آزمون"})
        event.action_void()
        self.assertTrue(event.is_void)
        self.assertTrue(event.voided_at)

    def test_02_within_tolerance_uses_later_entry_and_earlier_exit(self):
        self._event(datetime(2026, 7, 10, 7, 30), "guard", "guard_entry")
        self._event(datetime(2026, 7, 10, 7, 34), "device", "work_start")
        self._event(datetime(2026, 7, 10, 16, 0), "guard", "guard_exit")
        self._event(datetime(2026, 7, 10, 16, 3), "device", "work_end")
        day = self.env["cas.attendance.day"].search([("employee_id", "=", self.employee.id), ("work_date", "=", "2026-07-10")])
        self.assertEqual(day.state, "normal")
        self.assertEqual(day.effective_entry, datetime(2026, 7, 10, 7, 34))
        self.assertEqual(day.effective_exit, datetime(2026, 7, 10, 16, 0))

    def test_03_conflict_requires_and_records_supervisor_decision(self):
        date = "2026-07-11"
        self._event(datetime(2026, 7, 11, 7, 20), "guard", "guard_entry", date)
        self._event(datetime(2026, 7, 11, 7, 40), "device", "work_start", date)
        self._event(datetime(2026, 7, 11, 16, 0), "guard", "guard_exit", date)
        self._event(datetime(2026, 7, 11, 16, 0), "device", "work_end", date)
        day = self.env["cas.attendance.day"].search([("employee_id", "=", self.employee.id), ("work_date", "=", date)])
        self.assertEqual(day.state, "conflict")
        day.write({"resolution_entry_source": "device", "resolution_exit_source": "guard", "resolution_reason": "بررسی دوربین"})
        day.action_resolve()
        self.assertEqual(day.state, "resolved")
        self.assertEqual(day.effective_entry, datetime(2026, 7, 11, 7, 40))
        self.assertEqual(day.resolved_by_id, self.env.user)

    def test_04_mixed_sources_close_with_warning(self):
        date = "2026-07-12"
        self._event(datetime(2026, 7, 12, 7, 30), "device", "work_start", date)
        self._event(datetime(2026, 7, 12, 16, 0), "guard", "guard_exit", date)
        day = self.env["cas.attendance.day"].search([("employee_id", "=", self.employee.id), ("work_date", "=", date)])
        self.assertEqual(day.state, "warning")
        self.assertEqual(day.warning_code, "mixed")

    def test_05_automatic_work_date_fallback(self):
        event = self.Event.create({
            "employee_id": self.employee.id, "occurred_at": datetime(2026, 7, 13, 23, 30),
            "source": "device", "event_kind": "work_start",
        })
        self.assertEqual(str(event.work_date), "2026-07-13")
        self.assertEqual(event.attribution_method, "automatic")

    def test_06_advanced_events_build_typed_intervals(self):
        date = "2026-07-14"
        day = self.env["cas.attendance.day"].with_context(cas_attendance_engine=True).create({
            "employee_id": self.employee.id, "work_date": date, "attendance_mode": "advanced", "tolerance_minutes": 5,
        })
        self._event(datetime(2026, 7, 14, 7, 30), "device", "work_start", date)
        self.assertEqual(day.state, "incomplete")
        self._event(datetime(2026, 7, 14, 16, 0), "device", "work_end", date)
        self.assertEqual(day.state, "normal")
        self.assertEqual(len(day.interval_ids), 1)
        self.assertEqual(day.interval_ids.interval_type, "work")
        self.assertEqual(day.interval_ids.duration_minutes, 510)
