from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCasFormVersioning(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.definition = cls.env["cas.form.definition"].create(
            {
                "name": "گزارش کار روزانه",
                "code": "daily_work_report",
            }
        )
        cls.version = cls.env["cas.form.version"].create(
            {
                "definition_id": cls.definition.id,
                "name": "نسخه ۱",
                "revision": 1,
            }
        )
        cls.form_field = cls.env["cas.form.field"].create(
            {
                "version_id": cls.version.id,
                "technical_key": "work_summary",
                "label": "خلاصه فعالیت",
                "field_type": "long_text",
                "required": True,
            }
        )
        cls.node = cls.env["cas.form.node"].create(
            {
                "version_id": cls.version.id,
                "technical_key": "work_summary_node",
                "node_type": "field",
                "field_id": cls.form_field.id,
            }
        )

    def test_publish_locks_schema(self):
        self.version.action_publish()

        self.assertEqual(self.version.state, "published")
        self.assertEqual(self.definition.current_version_id, self.version)
        self.assertEqual(len(self.version.schema_hash), 64)

        with self.assertRaises(ValidationError):
            self.form_field.write({"label": "عنوان تغییرکرده"})

        with self.assertRaises(ValidationError):
            self.version.write({"notes": "تغییر غیرمجاز"})

        with self.assertRaises(ValidationError):
            self.version.unlink()

    def test_new_revision_preserves_field_identity(self):
        self.version.action_publish()
        action = self.version.action_new_revision()
        clone = self.env["cas.form.version"].browse(action["res_id"])

        self.assertEqual(clone.state, "draft")
        self.assertEqual(clone.revision, 2)
        self.assertEqual(len(clone.field_ids), 1)
        self.assertEqual(clone.field_ids.field_uuid, self.form_field.field_uuid)
        self.assertEqual(clone.field_ids.technical_key, "work_summary")
        self.assertEqual(len(clone.node_ids), 1)
        self.assertEqual(clone.node_ids.field_id, clone.field_ids)

    def test_definition_code_is_stable_after_publish(self):
        self.version.action_publish()
        with self.assertRaises(ValidationError):
            self.definition.write({"code": "changed_code"})

    def test_option_field_requires_options(self):
        field = self.env["cas.form.field"].create(
            {
                "version_id": self.version.id,
                "technical_key": "status",
                "label": "وضعیت",
                "field_type": "dropdown",
            }
        )
        with self.assertRaises(ValidationError):
            field._validate_definition()

    def test_invalid_technical_key_is_rejected(self):
        with self.assertRaises(ValidationError):
            self.env["cas.form.field"].create(
                {
                    "version_id": self.version.id,
                    "technical_key": "Bad Key",
                    "label": "نامعتبر",
                    "field_type": "short_text",
                }
            )

    def test_system_administrators_imply_form_manager(self):
        system_group = self.env.ref("base.group_system")
        form_manager_group = self.env.ref("cas_form_core.group_cas_form_manager")
        self.assertIn(form_manager_group, system_group.implied_ids)
