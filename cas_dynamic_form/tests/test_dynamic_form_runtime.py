from odoo.tests.common import TransactionCase


class TestCasDynamicFormRuntime(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.definition = cls.env["cas.form.definition"].create(
            {
                "name": "فرم آزمایش Runtime",
                "code": "dynamic_runtime_test",
                "description": "فرم مخصوص آزمون رابط پویا",
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
                "technical_key": "summary",
                "label": "شرح فعالیت",
                "field_type": "long_text",
                "required": True,
                "placeholder": "شرح را وارد کنید",
                "validation_config": {"min_length": 3},
            }
        )
        cls.company_field = cls.env["cas.form.field"].create(
            {
                "version_id": cls.version.id,
                "technical_key": "company",
                "label": "شرکت",
                "field_type": "company",
            }
        )
        cls.time_field = cls.env["cas.form.field"].create(
            {
                "version_id": cls.version.id,
                "technical_key": "finish_time",
                "label": "ساعت پایان",
                "field_type": "time",
            }
        )
        section = cls.env["cas.form.node"].create(
            {
                "version_id": cls.version.id,
                "technical_key": "main_section",
                "node_type": "section",
                "title": "اطلاعات اصلی",
                "column_count": 2,
                "column_span": 2,
            }
        )
        for sequence, form_field in enumerate(
            (cls.summary_field, cls.company_field, cls.time_field), start=1
        ):
            cls.env["cas.form.node"].create(
                {
                    "version_id": cls.version.id,
                    "technical_key": f"node_{form_field.technical_key}",
                    "node_type": "field",
                    "parent_id": section.id,
                    "field_id": form_field.id,
                    "sequence": sequence * 10,
                }
            )
        cls.version.action_publish()

    def test_runtime_schema_contains_layout_and_safe_metadata(self):
        schema = self.version.runtime_schema()

        self.assertEqual(schema["form_code"], "dynamic_runtime_test")
        self.assertEqual(schema["revision"], 1)
        self.assertEqual(len(schema["fields"]), 3)
        self.assertEqual(schema["fields"][0]["id"], self.summary_field.id)
        self.assertEqual(schema["fields"][0]["validation"], {"min_length": 3})
        self.assertEqual(schema["layout"][0]["type"], "section")
        self.assertEqual(len(schema["layout"][0]["children"]), 3)

    def test_catalog_start_save_resume_and_submit(self):
        catalog = self.env["cas.form.definition"].runtime_catalog()
        self.assertIn(self.definition.id, [item["id"] for item in catalog["forms"]])

        payload = self.definition.runtime_start_submission()
        submission = self.env["cas.form.submission"].browse(
            payload["submission"]["id"]
        )
        self.assertEqual(submission.state, "draft")
        self.assertEqual(payload["answers"], {})

        saved = submission.runtime_save(
            {
                "summary": "کنترل Runtime",
                "company": self.env.company.id,
                "finish_time": "12:30",
            }
        )
        self.assertEqual(saved["answers"]["summary"], "کنترل Runtime")
        self.assertEqual(saved["answers"]["company"]["id"], self.env.company.id)
        self.assertEqual(saved["answers"]["finish_time"], "12:30")

        resumed = submission.runtime_load()
        self.assertEqual(resumed["submission"]["number"], submission.number)
        self.assertEqual(resumed["answers"], saved["answers"])

        final = submission.runtime_submit(
            {
                "summary": "کنترل نهایی Runtime",
                "company": self.env.company.id,
                "finish_time": "13:00",
            }
        )
        self.assertEqual(final["submission"]["state"], "submitted")
        self.assertEqual(submission.state, "submitted")

    def test_reference_options_respect_allowed_companies(self):
        options = self.company_field.runtime_reference_options()
        option_ids = {option["id"] for option in options}
        self.assertIn(self.env.company.id, option_ids)
        self.assertTrue(option_ids.issubset(set(self.env.companies.ids)))

    def test_runtime_actions_include_client_tag_and_ids(self):
        action = self.definition.action_open_dynamic_runtime()
        self.assertEqual(action["type"], "ir.actions.client")
        self.assertEqual(action["tag"], "cas_dynamic_form.Runtime")
        self.assertEqual(action["params"]["definition_id"], self.definition.id)

        payload = self.definition.runtime_start_submission()
        submission = self.env["cas.form.submission"].browse(
            payload["submission"]["id"]
        )
        submission_action = submission.action_open_dynamic_runtime()
        self.assertEqual(submission_action["params"]["submission_id"], submission.id)

    def test_archived_revision_remains_renderable_for_old_draft(self):
        payload = self.definition.runtime_start_submission()
        submission = self.env["cas.form.submission"].browse(
            payload["submission"]["id"]
        )
        revision_action = self.version.action_new_revision()
        revision_two = self.env["cas.form.version"].browse(revision_action["res_id"])
        revision_two.action_publish()

        self.assertEqual(self.version.state, "archived")
        old_payload = submission.runtime_load()
        self.assertEqual(old_payload["schema"]["revision"], 1)
        self.assertEqual(old_payload["submission"]["state"], "draft")
