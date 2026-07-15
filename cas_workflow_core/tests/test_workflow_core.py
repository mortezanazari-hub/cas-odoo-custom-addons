from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCasWorkflowCore(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.responsible_user = cls.env["res.users"].with_context(
            no_reset_password=True
        ).create(
            {
                "name": "CAS Workflow Test Responsible",
                "login": "cas_workflow_core_test_responsible",
                "active": True,
                "company_id": cls.env.company.id,
                "company_ids": [(6, 0, cls.env.companies.ids)],
                "group_ids": [(6, 0, [cls.env.ref("base.group_user").id])],
            }
        )
        cls.inactive_user = cls.responsible_user.copy(
            {
                "name": "CAS Workflow Inactive Test Responsible",
                "login": "cas_workflow_core_test_inactive",
                "active": False,
            }
        )
        partner_model = cls.env["ir.model"]._get("res.partner")
        cls.definition = cls.env["cas.workflow.definition"].create(
            {
                "name": "گردش‌کار آزمایشی",
                "code": "workflow_core_test",
                "company_id": cls.env.company.id,
                "owner_user_id": cls.env.user.id,
                "target_model_id": partner_model.id,
            }
        )
        cls.version = cls.env["cas.workflow.version"].create(
            {
                "definition_id": cls.definition.id,
                "name": "نسخه ۱",
                "revision": 1,
            }
        )
        cls.initial = cls.env["cas.workflow.state"].create(
            {
                "version_id": cls.version.id,
                "name": "در انتظار بررسی",
                "code": "waiting",
                "kind": "initial",
                "sequence": 10,
                "sla_hours": 12,
            }
        )
        cls.final = cls.env["cas.workflow.state"].create(
            {
                "version_id": cls.version.id,
                "name": "تکمیل‌شده",
                "code": "done",
                "kind": "final",
                "sequence": 20,
            }
        )
        cls.finish = cls.env["cas.workflow.transition"].create(
            {
                "version_id": cls.version.id,
                "name": "تکمیل",
                "code": "finish",
                "from_state_id": cls.initial.id,
                "to_state_id": cls.final.id,
                "note_required": True,
                "responsible_mode": "actor",
                "condition_config": {"type": "always"},
            }
        )
        cls.version.action_publish()
        cls.partner = cls.env["res.partner"].create({"name": "رکورد آزمایشی Workflow"})

    def _start(self):
        payload = self.definition.action_start(
            self.partner.id,
            responsible_user_id=self.responsible_user.id,
        )
        return self.env["cas.workflow.instance"].browse(payload["instance_id"])

    def test_start_pins_version_creates_history_activity_and_sla(self):
        instance = self._start()

        self.assertEqual(instance.version_id, self.version)
        self.assertEqual(instance.current_state_id, self.initial)
        self.assertEqual(instance.responsible_user_id, self.responsible_user)
        self.assertEqual(instance.status, "running")
        self.assertTrue(instance.state_deadline)
        self.assertEqual(len(instance.history_ids), 1)
        self.assertEqual(instance.history_ids.event_type, "started")
        activities = self.env["mail.activity"].search(
            [("res_model", "=", "cas.workflow.instance"), ("res_id", "=", instance.id)]
        )
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities.user_id, self.responsible_user)

    def test_transition_is_guarded_and_history_is_append_only(self):
        instance = self._start()

        with self.assertRaises(ValidationError):
            instance.action_execute_transition(self.finish.id, note=False)
        result = instance.action_execute_transition(self.finish.id, note="بررسی انجام شد")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(instance.current_state_id, self.final)
        self.assertEqual(instance.status, "completed")
        self.assertTrue(instance.completed_at)
        self.assertEqual(len(instance.history_ids), 2)
        event = instance.history_ids.filtered(lambda item: item.event_type == "transition")
        self.assertEqual(len(event), 1)
        self.assertEqual(event.transition_id, self.finish)
        self.assertEqual(event.from_state_id, self.initial)
        self.assertEqual(event.to_state_id, self.final)
        self.assertEqual(event.actor_user_id, self.env.user)
        self.assertEqual(event.note, "بررسی انجام شد")
        self.assertFalse(
            self.env["mail.activity"].search_count(
                [("res_model", "=", "cas.workflow.instance"), ("res_id", "=", instance.id)]
            )
        )
        with self.assertRaises(ValidationError):
            event.write({"note": "دست‌کاری"})
        with self.assertRaises(ValidationError):
            event.unlink()

    def test_duplicate_running_instance_is_rejected(self):
        self._start()
        with self.assertRaises(ValidationError):
            self.definition.action_start(
                self.partner.id,
                responsible_user_id=self.responsible_user.id,
            )

    def test_inactive_or_invalid_responsible_is_rejected(self):
        inactive_partner = self.env["res.partner"].create(
            {"name": "Inactive Responsible Workflow Target"}
        )
        with self.assertRaises(ValidationError):
            self.definition.action_start(
                inactive_partner.id,
                responsible_user_id=self.inactive_user.id,
            )

        invalid_partner = self.env["res.partner"].create(
            {"name": "Invalid Responsible Workflow Target"}
        )
        invalid_user_id = self.env["res.users"].sudo().search([], order="id desc", limit=1).id + 100000
        with self.assertRaises(ValidationError):
            self.definition.action_start(
                invalid_partner.id,
                responsible_user_id=invalid_user_id,
            )

    def test_published_schema_is_locked_and_revision_preserves_codes(self):
        with self.assertRaises(ValidationError):
            self.initial.write({"name": "تغییر غیرمجاز"})
        action = self.version.action_new_revision()
        revision = self.env["cas.workflow.version"].browse(action["res_id"])
        self.assertEqual(revision.revision, 2)
        self.assertEqual(set(revision.state_ids.mapped("code")), {"waiting", "done"})
        self.assertEqual(revision.transition_ids.code, "finish")
        self.assertEqual(revision.transition_ids.from_state_id.code, "waiting")
        self.assertEqual(revision.transition_ids.to_state_id.code, "done")

    def test_unsafe_condition_is_rejected(self):
        definition = self.env["cas.workflow.definition"].create(
            {
                "name": "گردش‌کار شرط ناامن",
                "code": "workflow_unsafe_test",
                "target_model_id": self.env["ir.model"]._get("res.partner").id,
            }
        )
        version = self.env["cas.workflow.version"].create(
            {"definition_id": definition.id, "name": "نسخه ۱", "revision": 1}
        )
        start = self.env["cas.workflow.state"].create(
            {"version_id": version.id, "name": "شروع", "code": "start", "kind": "initial"}
        )
        end = self.env["cas.workflow.state"].create(
            {"version_id": version.id, "name": "پایان", "code": "end", "kind": "final"}
        )
        self.env["cas.workflow.transition"].create(
            {
                "version_id": version.id,
                "name": "اجرای ناامن",
                "code": "unsafe",
                "from_state_id": start.id,
                "to_state_id": end.id,
                "condition_config": {"type": "python", "code": "env.cr.execute('DROP')"},
            }
        )
        with self.assertRaises(ValidationError):
            version.action_publish()
