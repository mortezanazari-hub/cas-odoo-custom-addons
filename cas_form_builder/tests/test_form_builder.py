from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCasVisualFormBuilder(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        company = cls.env.company
        base = cls.env.ref("base.group_user")
        publisher = cls.env.ref("cas_form_core.group_cas_form_publisher")
        cls.designer = cls.env["res.users"].with_context(no_reset_password=True).create({
            "name": "Form Builder Designer", "login": "form.builder.designer",
            "company_id": company.id, "company_ids": [(6, 0, company.ids)],
            "group_ids": [(6, 0, [base.id, publisher.id])],
        })
        cls.definition = cls.env["cas.form.definition"].with_user(cls.designer).create({
            "name": "Visual Form", "code": "visual_form", "company_id": company.id,
            "owner_user_id": cls.designer.id,
        })
        cls.version = cls.env["cas.form.version"].with_user(cls.designer).create({
            "definition_id": cls.definition.id, "name": "Version 1", "revision": 1,
        })

    def _payload(self):
        return {
            "sections": [{"key": "main", "title": "اطلاعات اصلی", "columns": 2}],
            "fields": [
                {"key": "subject", "label": "موضوع", "type": "short_text", "required": True,
                 "readonly": False, "reportable": True, "placeholder": "موضوع...", "help_text": "",
                 "allowed_model": "", "column_span": 2, "section_key": "main", "options": []},
                {"key": "priority", "label": "اولویت", "type": "dropdown", "required": True,
                 "readonly": False, "reportable": True, "placeholder": "", "help_text": "",
                 "allowed_model": "", "column_span": 1, "section_key": "main",
                 "options": [{"key": "normal", "label": "عادی"}, {"key": "urgent", "label": "فوری"}]},
            ],
        }

    def test_visual_save_builds_core_fields_nodes_and_options(self):
        schema = self.version.with_user(self.designer).designer_get_schema()
        saved = self.version.with_user(self.designer).designer_save_schema(self._payload(), schema["revision"])
        self.assertEqual(saved["revision"], 1)
        self.assertEqual(set(self.version.field_ids.mapped("technical_key")), {"subject", "priority"})
        self.assertEqual(len(self.version.node_ids.filtered(lambda node: node.node_type == "section")), 1)
        self.assertEqual(len(self.version.node_ids.filtered(lambda node: node.node_type == "field")), 2)
        self.assertEqual(self.version.field_ids.filtered(lambda field: field.technical_key == "priority").option_ids.mapped("technical_key"), ["normal", "urgent"])
        self.assertEqual(self.version.action_open_visual_designer()["tag"], "cas_form_builder.visual_designer")

    def test_concurrency_validation_and_published_lock(self):
        self.version.with_user(self.designer).designer_save_schema(self._payload(), 0)
        with self.assertRaises(ValidationError):
            self.version.with_user(self.designer).designer_save_schema(self._payload(), 0)
        self.version.with_user(self.designer).action_publish()
        with self.assertRaises(ValidationError):
            self.version.with_user(self.designer).designer_save_schema(self._payload(), 1)

    def test_rejects_duplicate_keys_and_optionless_select(self):
        payload = self._payload()
        payload["fields"][1]["key"] = "subject"
        with self.assertRaises(ValidationError):
            self.version.with_user(self.designer).designer_save_schema(payload, 0)
        payload = self._payload()
        payload["fields"][1]["options"] = []
        with self.assertRaises(ValidationError):
            self.version.with_user(self.designer).designer_save_schema(payload, 0)
