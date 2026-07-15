from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCasApprovalCore(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["ir.model"]._get("res.partner")
        cls.approval_group = cls.env.ref("cas_approval_core.group_cas_approval_user")
        cls.users = cls.env["res.users"]
        cls.approvers = []
        for index in range(1, 4):
            user = cls.users.with_context(no_reset_password=True).create(
                {
                    "name": f"CAS Approval Test User {index}",
                    "login": f"cas_approval_test_user_{index}",
                    "active": True,
                    "company_id": cls.env.company.id,
                    "company_ids": [(6, 0, cls.env.companies.ids)],
                    "group_ids": [
                        (6, 0, [cls.env.ref("base.group_user").id, cls.approval_group.id])
                    ],
                }
            )
            cls.approvers.append(user)

    def _build_and_start(
        self,
        suffix,
        execution_mode="parallel",
        decision_rule="all",
        quorum_count=1,
        sequences=None,
    ):
        sequences = sequences or [10, 10]
        definition = self.env["cas.workflow.definition"].create(
            {
                "name": f"Approval Workflow {suffix}",
                "code": f"approval_workflow_{suffix}",
                "company_id": self.env.company.id,
                "owner_user_id": self.env.user.id,
                "target_model_id": self.partner_model.id,
            }
        )
        version = self.env["cas.workflow.version"].create(
            {"definition_id": definition.id, "name": "نسخه ۱", "revision": 1}
        )
        initial = self.env["cas.workflow.state"].create(
            {
                "version_id": version.id,
                "name": "در انتظار تأیید",
                "code": "approval",
                "kind": "initial",
                "sla_hours": 12,
            }
        )
        approved = self.env["cas.workflow.state"].create(
            {
                "version_id": version.id,
                "name": "تأیید نهایی",
                "code": "approved",
                "kind": "final",
            }
        )
        rejected = self.env["cas.workflow.state"].create(
            {
                "version_id": version.id,
                "name": "رد نهایی",
                "code": "rejected",
                "kind": "cancelled",
            }
        )
        approve_transition = self.env["cas.workflow.transition"].create(
            {
                "version_id": version.id,
                "name": "تأیید",
                "code": "approve",
                "from_state_id": initial.id,
                "to_state_id": approved.id,
                "condition_config": {"type": "always"},
                "responsible_mode": "actor",
            }
        )
        reject_transition = self.env["cas.workflow.transition"].create(
            {
                "version_id": version.id,
                "name": "رد",
                "code": "reject",
                "from_state_id": initial.id,
                "to_state_id": rejected.id,
                "condition_config": {"type": "always"},
                "responsible_mode": "actor",
            }
        )
        policy = self.env["cas.approval.policy"].create(
            {
                "version_id": version.id,
                "state_id": initial.id,
                "name": "سیاست تأیید آزمایشی",
                "code": "main_approval",
                "approve_transition_id": approve_transition.id,
                "reject_transition_id": reject_transition.id,
                "execution_mode": execution_mode,
                "decision_rule": decision_rule,
                "quorum_count": quorum_count,
            }
        )
        for index, sequence in enumerate(sequences):
            self.env["cas.approval.step"].create(
                {
                    "policy_id": policy.id,
                    "sequence": sequence,
                    "name": f"گام {index + 1}",
                    "role_label": f"تأییدکننده {index + 1}",
                    "approver_type": "user",
                    "approver_user_id": self.approvers[index].id,
                    "deadline_hours": 4,
                }
            )
        version.action_publish()
        partner = self.env["res.partner"].create(
            {"name": f"Approval Target {suffix}"}
        )
        payload = definition.action_start(
            partner.id, responsible_user_id=self.approvers[0].id
        )
        instance = self.env["cas.workflow.instance"].browse(payload["instance_id"])
        request = instance.approval_request_ids
        self.assertEqual(len(request), 1)
        return {
            "definition": definition,
            "version": version,
            "initial": initial,
            "approved": approved,
            "rejected": rejected,
            "approve_transition": approve_transition,
            "reject_transition": reject_transition,
            "policy": policy,
            "instance": instance,
            "request": request,
        }

    def _line_for(self, request, user):
        line = request.line_ids.filtered(lambda item: item.approver_user_id == user)
        self.assertEqual(len(line), 1)
        return line

    def test_parallel_all_blocks_bypass_and_completes_transition(self):
        data = self._build_and_start("parallel_all")
        request = data["request"]
        self.assertEqual(set(request.line_ids.mapped("status")), {"pending"})
        self.assertTrue(all(line.activity_ids for line in request.line_ids))

        with self.assertRaises(ValidationError):
            data["instance"].action_execute_transition(data["approve_transition"].id)

        self._line_for(request, self.approvers[0]).with_user(
            self.approvers[0]
        ).action_approve("تأیید اول")
        self.assertEqual(request.status, "pending")
        self._line_for(request, self.approvers[1]).with_user(
            self.approvers[1]
        ).action_approve("تأیید دوم")

        self.assertEqual(request.status, "approved")
        self.assertEqual(data["instance"].status, "completed")
        self.assertEqual(data["instance"].current_state_id, data["approved"])
        self.assertFalse(request.line_ids.activity_ids)
        self.assertEqual(len(request.history_ids), 4)

    def test_sequential_activates_only_next_sequence(self):
        data = self._build_and_start(
            "sequential", execution_mode="sequential", sequences=[10, 20]
        )
        first = self._line_for(data["request"], self.approvers[0])
        second = self._line_for(data["request"], self.approvers[1])
        self.assertEqual(first.status, "pending")
        self.assertEqual(second.status, "waiting")
        self.assertTrue(first.activity_ids)
        self.assertFalse(second.activity_ids)

        first.with_user(self.approvers[0]).action_approve()
        self.assertEqual(second.status, "pending")
        self.assertTrue(second.assigned_at)
        self.assertTrue(second.activity_ids)
        second.with_user(self.approvers[1]).action_approve()
        self.assertEqual(data["request"].status, "approved")

    def test_parallel_quorum_cancels_remaining_decisions(self):
        data = self._build_and_start(
            "quorum",
            decision_rule="quorum",
            quorum_count=2,
            sequences=[10, 10, 10],
        )
        request = data["request"]
        self._line_for(request, self.approvers[0]).with_user(
            self.approvers[0]
        ).action_approve()
        self._line_for(request, self.approvers[1]).with_user(
            self.approvers[1]
        ).action_approve()
        self.assertEqual(request.status, "approved")
        self.assertEqual(
            self._line_for(request, self.approvers[2]).status, "cancelled"
        )

    def test_rejection_requires_reason_and_keeps_immutable_history(self):
        data = self._build_and_start("rejection")
        line = self._line_for(data["request"], self.approvers[0]).with_user(
            self.approvers[0]
        )
        with self.assertRaises(ValidationError):
            line.action_reject("")
        line.action_reject("مدارک کافی نیست", comment="نیازمند اصلاح")
        self.assertEqual(data["request"].status, "rejected")
        self.assertEqual(data["instance"].status, "cancelled")
        self.assertEqual(data["instance"].current_state_id, data["rejected"])
        event = data["request"].history_ids.filtered(
            lambda item: item.event_type == "line_rejected"
        )
        self.assertEqual(event.note, "مدارک کافی نیست")
        with self.assertRaises(ValidationError):
            event.write({"note": "دست‌کاری"})
        with self.assertRaises(ValidationError):
            event.unlink()

    def test_inactive_fixed_approver_is_rejected(self):
        inactive = self.approvers[0].copy(
            {
                "name": "Inactive Approval User",
                "login": "cas_approval_test_inactive",
                "active": False,
            }
        )
        definition = self.env["cas.workflow.definition"].create(
            {
                "name": "Inactive Approver Workflow",
                "code": "inactive_approver_workflow",
                "target_model_id": self.partner_model.id,
            }
        )
        version = self.env["cas.workflow.version"].create(
            {"definition_id": definition.id, "name": "نسخه ۱", "revision": 1}
        )
        initial = self.env["cas.workflow.state"].create(
            {"version_id": version.id, "name": "شروع", "code": "start", "kind": "initial"}
        )
        final = self.env["cas.workflow.state"].create(
            {"version_id": version.id, "name": "پایان", "code": "done", "kind": "final"}
        )
        transition = self.env["cas.workflow.transition"].create(
            {
                "version_id": version.id,
                "name": "پایان",
                "code": "done",
                "from_state_id": initial.id,
                "to_state_id": final.id,
                "condition_config": {"type": "always"},
            }
        )
        policy = self.env["cas.approval.policy"].create(
            {
                "version_id": version.id,
                "state_id": initial.id,
                "name": "سیاست نامعتبر",
                "code": "invalid_policy",
                "approve_transition_id": transition.id,
            }
        )
        with self.assertRaises(ValidationError):
            self.env["cas.approval.step"].create(
                {
                    "policy_id": policy.id,
                    "name": "کاربر غیرفعال",
                    "role_label": "تأییدکننده",
                    "approver_type": "user",
                    "approver_user_id": inactive.id,
                }
            )

    def test_revision_clones_locked_approval_schema(self):
        data = self._build_and_start("revision")
        policy = data["policy"]
        with self.assertRaises(ValidationError):
            policy.write({"name": "تغییر غیرمجاز"})
        action = data["version"].action_new_revision()
        revision = self.env["cas.workflow.version"].browse(action["res_id"])
        self.assertEqual(len(revision.approval_policy_ids), 1)
        cloned = revision.approval_policy_ids
        self.assertEqual(cloned.code, policy.code)
        self.assertEqual(cloned.state_id.code, policy.state_id.code)
        self.assertEqual(
            cloned.approve_transition_id.code, policy.approve_transition_id.code
        )
        self.assertEqual(len(cloned.step_ids), len(policy.step_ids))
