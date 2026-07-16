import base64
import io
from datetime import date, datetime

import openpyxl

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCasAttendanceOperations(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.employee = cls.env["hr.employee"].create({"name": "Operations Test Employee", "company_id": cls.company.id})
        cls.site = cls.env["cas.attendance.site"].create({"name": "Operations Test Site", "code": "operations_test_site", "company_id": cls.company.id})
        cls.device = cls.env["cas.attendance.device"].create({"name": "Operations Test Device", "code": "operations_test_device", "company_id": cls.company.id, "site_id": cls.site.id})
        cls.env["cas.attendance.identity"].create({"source_type": "device", "external_key": "1001", "employee_id": cls.employee.id})
        cls.env["cas.attendance.identity"].create({"source_type": "guard", "external_key": "کارمند تست", "employee_id": cls.employee.id})

    def _batch(self, import_type, content, filename, name="Operations Import"):
        return self.env["cas.attendance.import"].create({
            "name": name, "company_id": self.company.id, "import_type": import_type,
            "device_id": self.device.id if import_type != "guard_workbook" else False,
            "site_id": self.site.id, "data_file": base64.b64encode(content), "filename": filename,
        })

    def test_01_device_file_stages_first_last_and_middle_without_data_loss(self):
        content = (
            "EnNo,DateTime\n"
            "1001,2026-07-01 07:30:21\n"
            "1001,2026-07-01 12:00:00\n"
            "1001,2026-07-01 16:00:55\n"
        ).encode()
        batch = self._batch("device_punches", content, "device.csv")
        batch.action_parse()
        self.assertEqual(batch.state, "review")
        self.assertEqual(batch.total_count, 3)
        self.assertEqual(batch.unmatched_count, 0)
        self.assertEqual(set(batch.line_ids.mapped("event_kind")), {"work_start", "unknown_entry", "work_end"})
        self.assertTrue(all(line.occurred_at.second == 0 for line in batch.line_ids))
        batch.action_import_ready()
        self.assertEqual(batch.state, "imported")
        self.assertEqual(batch.imported_count, 3)
        self.assertEqual(self.env["cas.attendance.event"].search_count([("employee_id", "=", self.employee.id)]), 3)
        with self.assertRaises(ValidationError):
            batch.unlink()

    def test_02_same_file_is_detected_as_duplicate(self):
        content = "employee_id,check_in,check_out\n1001,2026-07-02 07:30,2026-07-02 16:00\n".encode()
        first = self._batch("paired_sessions", content, "paired.csv", "First")
        first.action_parse(); first.action_import_ready()
        second = self._batch("paired_sessions", content, "paired.csv", "Second")
        second.action_parse()
        self.assertEqual(second.skipped_count, 2)
        self.assertEqual(set(second.line_ids.mapped("status")), {"duplicate"})

    def test_03_guard_workbook_uses_sheet_identity_and_cross_midnight(self):
        wb = openpyxl.Workbook(); ws = wb.active; ws.title = "کارمند تست"
        ws.append([None] * 10); ws.append([None] * 10)
        ws.append([None] * 7 + ["1405/04/12", "23:30", "08:00"])
        stream = io.BytesIO(); wb.save(stream)
        batch = self._batch("guard_workbook", stream.getvalue(), "guard.xlsx")
        batch.action_parse()
        self.assertEqual(batch.ready_count, 2)
        entry = batch.line_ids.filtered(lambda l: l.event_kind == "guard_entry")
        exit_ = batch.line_ids.filtered(lambda l: l.event_kind == "guard_exit")
        self.assertGreater(exit_.occurred_at, entry.occurred_at)
        self.assertEqual((exit_.occurred_at - entry.occurred_at).total_seconds() // 3600, 8)

    def test_04_unknown_identity_blocks_import_until_reviewed(self):
        content = "employee_id,check_in,check_out\nUNKNOWN,2026-07-03 07:30,2026-07-03 16:00\n".encode()
        batch = self._batch("paired_sessions", content, "unknown.csv")
        batch.action_parse()
        self.assertEqual(batch.unmatched_count, 2)
        with self.assertRaises(ValidationError):
            batch.action_import_ready()
        batch.line_ids.write({"employee_id": self.employee.id})
        self.assertEqual(batch.unmatched_count, 0)
        batch.action_import_ready()
        self.assertEqual(batch.imported_count, 2)

    def test_05_guard_can_confirm_multiple_people_in_one_batch(self):
        second = self.env["hr.employee"].create({"name": "Operations Second Employee", "company_id": self.company.id})
        batch = self.env["cas.guard.batch"].create({
            "name": "Morning Gate", "company_id": self.company.id, "site_id": self.site.id,
            "default_occurred_at": datetime(2026, 7, 4, 7, 30),
            "line_ids": [
                (0, 0, {"employee_id": self.employee.id, "occurred_at": datetime(2026, 7, 4, 7, 30), "event_kind": "guard_entry"}),
                (0, 0, {"employee_id": second.id, "occurred_at": datetime(2026, 7, 4, 7, 32), "event_kind": "guard_entry"}),
            ],
        })
        batch.action_confirm()
        self.assertEqual(batch.state, "confirmed")
        self.assertEqual(len(batch.line_ids.mapped("event_id")), 2)
        with self.assertRaises(ValidationError):
            batch.unlink()
