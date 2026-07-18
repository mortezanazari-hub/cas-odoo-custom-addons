from odoo.tests.common import TransactionCase


class TestCasWorkspace(TransactionCase):
    def test_workspace_payload_contract(self):
        payload = self.env["cas.workspace.dashboard"].get_workspace_data()
        self.assertEqual(payload["user"]["id"], self.env.user.id)
        self.assertIn("actions", payload)
        self.assertIn("letters", payload)
        self.assertIn("stats", payload)
        self.assertIn("progress", payload["stats"])
        self.assertGreaterEqual(payload["stats"]["progress"], 0)
        self.assertLessEqual(payload["stats"]["progress"], 100)

    def test_workspace_client_action_is_registered(self):
        action = self.env.ref("cas_workspace.action_cas_workspace")
        self.assertEqual(action.tag, "cas_workspace.organizational_workspace")
        self.assertEqual(action.type, "ir.actions.client")

    def test_navigation_contains_all_cas_workspaces(self):
        navigation = self.env["cas.workspace.dashboard"].get_navigation()
        keys = {item["key"] for item in navigation["items"]}
        self.assertTrue(
            {
                "dashboard", "urgent", "actions", "forms", "form_builder",
                "workflows", "workflow_builder", "letters", "documents",
                "approvals", "attendance", "attendance_ops", "shifts",
                "kardex", "work_reports", "settings",
            }.issubset(keys)
        )

    def test_action_page_uses_custom_payload(self):
        payload = self.env["cas.workspace.dashboard"].get_page_data("actions")
        self.assertTrue(payload["available"])
        self.assertEqual(payload["model"], "cas.action.item")
        self.assertIn("rows", payload)
        self.assertIn("columns", payload)

    def test_unknown_page_is_safe(self):
        payload = self.env["cas.workspace.dashboard"].get_page_data("not-a-route")
        self.assertFalse(payload["available"])
