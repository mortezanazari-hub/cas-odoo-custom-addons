from datetime import timedelta

from odoo import fields
from odoo.exceptions import AccessError, ValidationError
from odoo.tests.common import TransactionCase


class TestCasCorrespondence(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.user_group = cls.env.ref("cas_correspondence.group_cas_correspondence_user")
        internal_group = cls.env.ref("base.group_user")

        def make_user(login):
            return cls.env["res.users"].with_context(no_reset_password=True).create(
                {
                    "name": login.replace("_", " ").title(),
                    "login": login,
                    "company_id": cls.company.id,
                    "company_ids": [(6, 0, [cls.company.id])],
                    "group_ids": [(6, 0, [internal_group.id, cls.user_group.id])],
                }
            )

        cls.sender = make_user("cas_letter_sender")
        cls.receiver = make_user("cas_letter_receiver")
        cls.manager = make_user("cas_letter_manager")
        cls.outsider = make_user("cas_letter_outsider")
        cls.secretary = make_user("cas_letter_secretary")
        cls.ceo = make_user("cas_letter_ceo")

        cls.manager_department = cls.env["hr.department"].create(
            {"name": "CAS Management", "company_id": cls.company.id}
        )
        cls.sender_department = cls.env["hr.department"].create(
            {
                "name": "CAS Sender Unit",
                "company_id": cls.company.id,
                "parent_id": cls.manager_department.id,
            }
        )
        cls.receiver_department = cls.env["hr.department"].create(
            {"name": "CAS Receiver Unit", "company_id": cls.company.id}
        )
        cls.manager_employee = cls.env["hr.employee"].create(
            {
                "name": "CAS Manager Employee",
                "user_id": cls.manager.id,
                "company_id": cls.company.id,
                "department_id": cls.manager_department.id,
            }
        )
        cls.sender_employee = cls.env["hr.employee"].create(
            {
                "name": "CAS Sender Employee",
                "user_id": cls.sender.id,
                "company_id": cls.company.id,
                "department_id": cls.sender_department.id,
                "parent_id": cls.manager_employee.id,
                "job_title": "کارشناس فرستنده",
            }
        )
        cls.receiver_employee = cls.env["hr.employee"].create(
            {
                "name": "CAS Receiver Employee",
                "user_id": cls.receiver.id,
                "company_id": cls.company.id,
                "department_id": cls.receiver_department.id,
                "job_title": "کارشناس گیرنده",
            }
        )
        cls.outsider_employee = cls.env["hr.employee"].create(
            {
                "name": "CAS Outsider Employee",
                "user_id": cls.outsider.id,
                "company_id": cls.company.id,
                "department_id": cls.receiver_department.id,
            }
        )
        cls.secretary_employee = cls.env["hr.employee"].create(
            {
                "name": "CAS Secretary Employee",
                "user_id": cls.secretary.id,
                "company_id": cls.company.id,
                "department_id": cls.manager_department.id,
            }
        )
        cls.ceo_employee = cls.env["hr.employee"].create(
            {
                "name": "CAS CEO Employee",
                "user_id": cls.ceo.id,
                "company_id": cls.company.id,
                "department_id": cls.manager_department.id,
            }
        )
        cls.manager_department.manager_id = cls.manager_employee
        cls.receiver_department.manager_id = cls.receiver_employee
        cls.company.cas_correspondence_ceo_user_id = cls.ceo

    def _draft(self, sender=None, reply_to=None, correction_of=None):
        sender = sender or self.sender
        vals = {
            "subject": "نامه آزمایشی CAS",
            "body": "<p>متن رسمی آزمایش</p>",
            "company_id": self.company.id,
        }
        if reply_to:
            vals["reply_to_id"] = reply_to.id
        if correction_of:
            vals.update(
                {"correction_of_id": correction_of.id, "correction_reason": "اصلاح رسمی"}
            )
        return self.env["cas.correspondence.letter"].with_user(sender).create(vals)

    def _add_recipient(self, letter, user, expectation="information", role="to"):
        return self.env["cas.correspondence.recipient"].with_user(
            letter.sender_user_id
        ).create(
            {
                "letter_id": letter.id,
                "role": role,
                "target_kind": "user",
                "recipient_user_id": user.id,
                "expectation": expectation,
                "deadline": fields.Datetime.now() + timedelta(days=1),
            }
        )

    def _send(self, expectation="information"):
        letter = self._draft()
        line = self._add_recipient(letter, self.receiver, expectation)
        letter.with_user(self.sender).action_send()
        return letter, line

    def test_send_assigns_company_sequence_and_signature(self):
        first, first_line = self._send()
        second = self._draft()
        self._add_recipient(second, self.receiver)
        second.with_user(self.sender).action_send()
        self.assertTrue(first.number)
        self.assertNotEqual(first.number, second.number)
        self.assertEqual(first.state, "delivered")
        self.assertEqual(first.signed_by_user_id, self.sender)
        self.assertEqual(first.signature_job_title, "کارشناس فرستنده")
        self.assertEqual(first_line.status, "delivered")
        self.assertTrue(first_line.activity_id)
        self.assertEqual(set(first.audit_ids.mapped("event_type")), {"created", "sent", "delivered"})

    def test_information_receipt_completes_item(self):
        letter, line = self._send("information")
        line.with_user(self.receiver).action_mark_viewed()
        self.assertEqual(line.status, "completed")
        self.assertEqual(letter.state, "viewed")
        self.assertEqual(len(letter.receipt_ids), 1)
        line.with_user(self.receiver).action_mark_viewed()
        self.assertEqual(len(letter.receipt_ids), 1)

    def test_action_requires_responsible_and_result(self):
        letter, line = self._send("action")
        with self.assertRaises(AccessError):
            line.with_user(self.outsider).action_start()
        line.with_user(self.receiver).action_mark_viewed()
        line.with_user(self.receiver).action_start()
        with self.assertRaises(ValidationError):
            line.with_user(self.receiver).action_complete("")
        line.with_user(self.receiver).action_complete("اقدام انجام شد")
        self.assertEqual(line.status, "completed")
        self.assertEqual(line.action_result, "اقدام انجام شد")

    def test_formal_reply_is_independent_numbered_letter(self):
        original, line = self._send("reply")
        reply = self._draft(sender=self.receiver, reply_to=original)
        self._add_recipient(reply, self.sender, "information")
        reply.with_user(self.receiver).action_send()
        self.assertTrue(reply.number)
        self.assertNotEqual(original.number, reply.number)
        self.assertEqual(line.status, "replied")
        self.assertEqual(line.reply_letter_id, reply)
        self.assertEqual(original.state, "replied")
        self.assertEqual(reply.thread_root_id, original)

    def test_sent_letter_and_audit_are_immutable(self):
        letter, _line = self._send()
        with self.assertRaises(ValidationError):
            letter.with_user(self.sender).write({"subject": "تغییر غیرمجاز"})
        with self.assertRaises(ValidationError):
            letter.with_user(self.sender).unlink()
        with self.assertRaises(AccessError):
            letter.audit_ids[:1].write({"reason": "tamper"})

    def test_structural_manager_and_outsider_security(self):
        letter, _line = self._send()
        manager_visible = self.env["cas.correspondence.letter"].with_user(self.manager).search(
            [("id", "=", letter.id)]
        )
        outsider_visible = self.env["cas.correspondence.letter"].with_user(self.outsider).search(
            [("id", "=", letter.id)]
        )
        self.assertEqual(manager_visible, letter)
        self.assertFalse(outsider_visible)

    def test_secretariat_delegation_grants_and_revoke_removes_access(self):
        letter, _line = self._send()
        self.assertFalse(
            self.env["cas.correspondence.letter"].with_user(self.secretary).search(
                [("id", "=", letter.id)]
            )
        )
        delegation = self.env["cas.correspondence.secretariat.delegation"].with_user(
            self.ceo
        ).create(
            {
                "company_id": self.company.id,
                "delegate_user_id": self.secretary.id,
                "date_from": fields.Date.context_today(self.env.user),
                "reason": "تفویض آزمون",
            }
        )
        self.assertTrue(
            self.env["cas.correspondence.letter"].with_user(self.secretary).search(
                [("id", "=", letter.id)]
            )
        )
        delegation.with_user(self.ceo).action_revoke("پایان آزمون")
        self.assertFalse(
            self.env["cas.correspondence.letter"].with_user(self.secretary).search(
                [("id", "=", letter.id)]
            )
        )

    def test_correction_preserves_relationship_and_cancels_original(self):
        original, _line = self._send()
        correction = self._draft(correction_of=original)
        self._add_recipient(correction, self.receiver)
        correction.with_user(self.sender).action_send()
        self.assertEqual(original.state, "cancelled")
        self.assertEqual(original.replacement_letter_id, correction)
        self.assertEqual(correction.outgoing_relation_ids.relation_type, "corrects")

    def test_department_recipient_resolves_only_configured_manager(self):
        letter = self._draft()
        line = self.env["cas.correspondence.recipient"].with_user(self.sender).create(
            {
                "letter_id": letter.id,
                "target_kind": "department",
                "department_id": self.receiver_department.id,
                "expectation": "information",
            }
        )
        letter.with_user(self.sender).action_send()
        self.assertEqual(line.responsible_user_id, self.receiver)

    def test_referral_preserves_referrer_and_action_hub_descriptor(self):
        letter, _line = self._send("information")
        wizard = self.env["cas.correspondence.referral.wizard"].with_user(self.sender).create(
            {
                "letter_id": letter.id,
                "target_kind": "user",
                "recipient_user_id": self.outsider.id,
                "expectation": "action",
                "priority": "urgent",
                "note": "اقدام ارجاعی آزمایشی",
            }
        )
        wizard.action_confirm()
        referral = letter.referral_ids
        self.assertEqual(referral.referrer_user_id, self.sender)
        self.assertEqual(referral.responsible_user_id, self.outsider)
        descriptor = letter.with_user(self.sender)._cas_action_descriptors()
        self.assertIn(f"referral:{referral.id}", [item["action_key"] for item in descriptor])
        referral.with_user(self.outsider).action_mark_viewed()
        referral.with_user(self.outsider).action_start()
        referral.with_user(self.outsider).action_complete("ارجاع انجام شد")
        self.assertEqual(referral.status, "completed")

    def test_inactive_recipient_is_rejected_at_send(self):
        letter = self._draft()
        self._add_recipient(letter, self.receiver)
        self.receiver.active = False
        with self.assertRaises(ValidationError):
            letter.with_user(self.sender).action_send()

    def test_cross_company_recipient_is_rejected(self):
        other_company = self.env["res.company"].create({"name": "CAS Other Company"})
        other_user = self.env["res.users"].with_context(no_reset_password=True).create(
            {
                "name": "CAS Other User",
                "login": "cas_letter_other_company",
                "company_id": other_company.id,
                "company_ids": [(6, 0, [other_company.id])],
                "group_ids": [
                    (
                        6,
                        0,
                        [
                            self.env.ref("base.group_user").id,
                            self.user_group.id,
                        ],
                    )
                ],
            }
        )
        letter = self._draft()
        self._add_recipient(letter, other_user)
        with self.assertRaises(ValidationError):
            letter.with_user(self.sender).action_send()

    def test_action_close_waits_for_all_recipient_expectations(self):
        letter, line = self._send("action")
        with self.assertRaises(ValidationError):
            letter.with_user(self.sender).action_close()
        line.with_user(self.receiver).action_mark_viewed()
        line.with_user(self.receiver).action_start()
        line.with_user(self.receiver).action_complete("انجام شد")
        letter.with_user(self.sender).action_close()
        self.assertEqual(letter.state, "closed")
