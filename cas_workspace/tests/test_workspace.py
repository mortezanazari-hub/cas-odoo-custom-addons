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
