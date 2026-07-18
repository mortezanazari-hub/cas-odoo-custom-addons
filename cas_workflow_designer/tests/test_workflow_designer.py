from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCasWorkflowDesigner(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["ir.model"]._get("res.partner")
        cls.submission_model = cls.env["ir.model"]._get("cas.form.submission")
        cls.definition = cls.env["cas.workflow.definition"].create({
            "name": "Visual Workflow",
            "code": "visual_workflow",
            "target_model_id": cls.partner_model.id,
        })
        cls.version = cls.env["cas.workflow.version"].create({
            "definition_id": cls.definition.id,
            "name": "Version 1",
            "revision": 1,
        })

    def _graph(self):
        return {
            "nodes": [
                {"key": "start", "name": "Start", "kind": "initial", "x": 80, "y": 160, "color": "green", "sla_hours": 0, "fold": False},
                {"key": "review", "name": "Review", "kind": "normal", "x": 340, "y": 160, "color": "blue", "sla_hours": 8, "fold": False},
                {"key": "done", "name": "Done", "kind": "final", "x": 620, "y": 160, "color": "purple", "sla_hours": 0, "fold": True},
            ],
            "edges": [
                {"key": "send", "name": "Send", "from": "start", "to": "review", "responsible_mode": "keep", "note_required": False},
                {"key": "approve", "name": "Approve", "from": "review", "to": "done", "responsible_mode": "actor", "note_required": True},
            ],
        }

    def test_save_graph_builds_real_core_records(self):
        result = self.version.designer_save_graph(self._graph(), 0)
        self.assertEqual(result["revision"], 1)
        self.assertEqual(set(self.version.state_ids.mapped("code")), {"start", "review", "done"})
        self.assertEqual(set(self.version.transition_ids.mapped("code")), {"send", "approve"})
        review = self.version.state_ids.filtered(lambda item: item.code == "review")
        self.assertEqual((review.designer_x, review.designer_y, review.sla_hours), (340, 160, 8))
        self.assertEqual(self.version.action_open_node_designer()["tag"], "cas_workflow_designer.node_designer")

    def test_concurrency_reachability_and_published_lock(self):
        self.version.designer_save_graph(self._graph(), 0)
        with self.assertRaises(ValidationError):
            self.version.designer_save_graph(self._graph(), 0)
        invalid = self._graph()
        invalid["edges"] = invalid["edges"][:1]
        with self.assertRaises(ValidationError):
            self.version.designer_save_graph(invalid, 1)
        self.version.action_publish()
        with self.assertRaises(ValidationError):
            self.version.designer_save_graph(self._graph(), 1)

    def _published_form(self):
        definition = self.env["cas.form.definition"].create({"name": "Request", "code": "workflow_request"})
        version = self.env["cas.form.version"].create({"definition_id": definition.id, "name": "Version 1", "revision": 1})
        field = self.env["cas.form.field"].create({
            "version_id": version.id, "technical_key": "subject", "label": "Subject",
            "field_type": "short_text", "required": False, "sequence": 10,
        })
        section = self.env["cas.form.node"].create({
            "version_id": version.id, "technical_key": "main", "node_type": "section",
            "title": "Main", "sequence": 10, "column_count": 1, "column_span": 1,
        })
        self.env["cas.form.node"].create({
            "version_id": version.id, "technical_key": "field_subject", "node_type": "field",
            "parent_id": section.id, "field_id": field.id, "sequence": 20, "column_count": 1, "column_span": 1,
        })
        version.action_publish()
        return definition, version

    def test_form_binding_accepts_only_submitted_bound_form(self):
        form, form_version = self._published_form()
        definition = self.env["cas.workflow.definition"].create({
            "name": "Request Approval", "code": "request_approval",
            "target_model_id": self.submission_model.id, "form_definition_id": form.id,
        })
        version = self.env["cas.workflow.version"].create({
            "definition_id": definition.id, "name": "Version 1", "revision": 1,
        })
        version.designer_save_graph(self._graph(), 0)
        version.action_publish()
        submission = self.env["cas.form.submission"].create({"version_id": form_version.id})
        responsible = self.env.ref("base.user_admin")
        with self.assertRaises(ValidationError):
            definition.action_start_submission(submission.id, responsible.id)
        submission.action_submit()
        started = definition.action_start_submission(submission.id, responsible.id)
        self.assertEqual(started["state"], "start")
        self.assertEqual(started["responsible_user_id"], responsible.id)

    def test_form_binding_requires_submission_target(self):
        form, _version = self._published_form()
        with self.assertRaises(ValidationError):
            self.env["cas.workflow.definition"].create({
                "name": "Invalid", "code": "invalid_form_workflow",
                "target_model_id": self.partner_model.id, "form_definition_id": form.id,
            })
