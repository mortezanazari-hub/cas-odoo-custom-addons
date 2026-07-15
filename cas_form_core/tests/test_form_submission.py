from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCasFormSubmission(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.definition = cls.env["cas.form.definition"].create(
            {
                "name": "فرم آزمایش ثبت",
                "code": "submission_test_form",
            }
        )
        cls.version = cls.env["cas.form.version"].create(
            {
                "definition_id": cls.definition.id,
                "name": "نسخه ۱",
                "revision": 1,
            }
        )
        cls.summary_field = cls.env["cas.form.field"].create(
            {
                "version_id": cls.version.id,
                "technical_key": "work_summary",
                "label": "شرح فعالیت",
                "field_type": "short_text",
                "required": True,
                "validation_config": {
                    "min_length": 3,
                    "max_length": 80,
                    "regex": r"[^0-9]+",
                },
            }
        )
        cls.quantity_field = cls.env["cas.form.field"].create(
            {
                "version_id": cls.version.id,
                "technical_key": "quantity",
                "label": "تعداد",
                "field_type": "integer",
                "validation_config": {"min": 0, "max": 1000},
            }
        )
        cls.safe_field = cls.env["cas.form.field"].create(
            {
                "version_id": cls.version.id,
                "technical_key": "safe_operation",
                "label": "کار ایمن بود",
                "field_type": "boolean",
                "required": True,
            }
        )
        cls.status_field = cls.env["cas.form.field"].create(
            {
                "version_id": cls.version.id,
                "technical_key": "result_status",
                "label": "نتیجه",
                "field_type": "dropdown",
            }
        )
        cls.env["cas.form.field.option"].create(
            [
                {
                    "field_id": cls.status_field.id,
                    "technical_key": "done",
                    "label": "انجام شد",
                },
                {
                    "field_id": cls.status_field.id,
                    "technical_key": "pending",
                    "label": "در انتظار",
                },
            ]
        )
        for sequence, form_field in enumerate(
            (
                cls.summary_field,
                cls.quantity_field,
                cls.safe_field,
                cls.status_field,
            ),
            start=1,
        ):
            cls.env["cas.form.node"].create(
                {
                    "version_id": cls.version.id,
                    "technical_key": f"node_{form_field.technical_key}",
                    "node_type": "field",
                    "field_id": form_field.id,
                    "sequence": sequence * 10,
                }
            )
        cls.version.action_publish()

    def _new_submission(self):
        return self.env["cas.form.submission"].create(
            {"version_id": self.version.id}
        )

    def test_typed_answers_submit_and_snapshot(self):
        submission = self._new_submission()
        values = submission.action_save_answers(
            {
                "work_summary": "  تعمیر پمپ  ",
                "quantity": 12,
                "safe_operation": False,
                "result_status": "done",
            }
        )

        self.assertRegex(submission.number, r"^FRM/")
        self.assertEqual(values["work_summary"], "تعمیر پمپ")
        self.assertEqual(values["quantity"], 12)
        self.assertIs(values["safe_operation"], False)
        self.assertEqual(values["result_status"], "done")

        submission.action_submit()

        self.assertEqual(submission.state, "submitted")
        self.assertTrue(submission.submitted_at)
        self.assertEqual(submission.submitted_by_id, self.env.user)
        self.assertEqual(
            submission.snapshot_json["schema_hash"], self.version.schema_hash
        )
        self.assertEqual(submission.snapshot_json["form_revision"], 1)
        self.assertEqual(len(submission.snapshot_json["answers"]), 4)

    def test_required_and_server_validation(self):
        submission = self._new_submission()

        with self.assertRaises(ValidationError):
            submission.action_submit({"safe_operation": False})

        with self.assertRaises(ValidationError):
            submission.action_save_answers({"work_summary": "12"})

        with self.assertRaises(ValidationError):
            submission.action_save_answers({"quantity": 1001})

        with self.assertRaises(ValidationError):
            submission.action_save_answers({"result_status": "invalid"})

        with self.assertRaises(ValidationError):
            submission.action_save_answers({"unknown_key": "value"})

    def test_submitted_record_and_answers_are_locked(self):
        submission = self._new_submission()
        submission.action_submit(
            {"work_summary": "بازرسی خط", "safe_operation": True}
        )
        answer = self.env["cas.form.answer"].sudo().search(
            [
                ("submission_id", "=", submission.id),
                ("field_id", "=", self.summary_field.id),
            ]
        )

        with self.assertRaises(ValidationError):
            submission.write({"owner_user_id": self.env.user.id})
        with self.assertRaises(ValidationError):
            answer.write({"value_char": "تغییر غیرمجاز"})
        with self.assertRaises(ValidationError):
            answer.unlink()
        with self.assertRaises(ValidationError):
            submission.unlink()

    def test_manager_reopen_requires_reason(self):
        submission = self._new_submission()
        submission.action_submit(
            {"work_summary": "کنترل نهایی", "safe_operation": True}
        )

        with self.assertRaises(ValidationError):
            submission.action_reopen("")

        submission.action_reopen("اصلاح اشتباه ثبت‌شده")
        self.assertEqual(submission.state, "draft")
        self.assertFalse(submission.snapshot_json)
        self.assertEqual(submission.reopen_count, 1)

    def test_draft_keeps_its_original_revision(self):
        submission = self._new_submission()
        action = self.version.action_new_revision()
        revision_two = self.env["cas.form.version"].browse(action["res_id"])
        revision_two.action_publish()

        self.assertEqual(self.version.state, "archived")
        self.assertEqual(self.definition.current_version_id, revision_two)
        submission.action_submit(
            {"work_summary": "گزارش نسخه قبلی", "safe_operation": True}
        )
        self.assertEqual(submission.version_id, self.version)
        self.assertEqual(submission.snapshot_json["form_revision"], 1)

    def test_cancelled_submission_cannot_be_changed(self):
        submission = self._new_submission()
        submission.action_cancel()

        self.assertEqual(submission.state, "cancelled")
        with self.assertRaises(ValidationError):
            submission.action_save_answers({"work_summary": "نامجاز"})
        with self.assertRaises(ValidationError):
            submission.unlink()
