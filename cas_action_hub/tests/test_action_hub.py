from odoo import fields
from odoo.exceptions import AccessError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCasActionHub(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env["res.users"].create(
            {
                "name": "Action Hub User",
                "login": "action.hub.user",
                "group_ids": [(6, 0, [cls.env.ref("base.group_user").id])],
                "company_ids": [(6, 0, [cls.env.company.id])],
                "company_id": cls.env.company.id,
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Action Hub Source"})
        cls.activity = cls.env["mail.activity"].create(
            {
                "activity_type_id": cls.env.ref("mail.mail_activity_data_todo").id,
                "res_model_id": cls.env["ir.model"]._get_id("res.partner"),
                "res_id": cls.partner.id,
                "user_id": cls.user.id,
                "summary": "Review action hub source",
                "date_deadline": fields.Date.context_today(cls.env.user),
            }
        )

    def test_activity_sync_projection_and_open(self):
        result = self.env["cas.action.item"]._sync_all()
        self.assertGreaterEqual(result["odoo_activity"], 1)
        item = self.env["cas.action.item"].sudo().search(
            [("action_key", "=", f"activity:{self.activity.id}")], limit=1
        )
        self.assertTrue(item)
        self.assertEqual(item.assignee_user_id, self.user)
        self.assertEqual(item.source_model, "mail.activity")
        action = item.with_user(self.user).action_open_source()
        self.assertEqual(action["res_model"], "res.partner")
        self.assertEqual(action["res_id"], self.partner.id)

    def test_projection_is_engine_owned(self):
        with self.assertRaises(AccessError):
            self.env["cas.action.item"].create(
                {
                    "source_model": "res.partner",
                    "source_record_id": self.partner.id,
                    "action_key": "forged",
                    "source_adapter": "test",
                    "action_type": "action",
                    "title": "Forged",
                    "assignee_user_id": self.user.id,
                    "company_id": self.env.company.id,
                    "last_synced_at": fields.Datetime.now(),
                }
            )

    def test_projection_history_cannot_be_deleted(self):
        self.env["cas.action.item"]._sync_all()
        item = self.env["cas.action.item"].sudo().search(
            [("action_key", "=", f"activity:{self.activity.id}")], limit=1
        )
        with self.assertRaises(ValidationError):
            item.unlink()

    def test_stale_activity_is_completed(self):
        self.env["cas.action.item"]._sync_all()
        item = self.env["cas.action.item"].sudo().search(
            [("action_key", "=", f"activity:{self.activity.id}")], limit=1
        )
        self.activity.unlink()
        self.env["cas.action.item"]._sync_all()
        self.assertEqual(item.status, "completed")
        self.assertTrue(item.completed_at)
