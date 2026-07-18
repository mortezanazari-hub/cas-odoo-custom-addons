import base64

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCasCorrespondenceAdvanced(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        base = cls.env.ref("base.group_user")
        correspondence = cls.env.ref("cas_correspondence.group_cas_correspondence_user")

        def make_user(login):
            return cls.env["res.users"].with_context(no_reset_password=True).create({
                "name": login, "login": login, "company_id": cls.company.id,
                "company_ids": [(6, 0, cls.company.ids)], "group_ids": [(6, 0, [base.id, correspondence.id])],
            })

        cls.sender = make_user("advanced.sender")
        cls.receiver = make_user("advanced.receiver")
        department = cls.env["hr.department"].create({"name": "Advanced Correspondence", "company_id": cls.company.id})
        cls.sender_employee = cls.env["hr.employee"].create({
            "name": "Advanced Sender", "user_id": cls.sender.id, "company_id": cls.company.id,
            "department_id": department.id, "job_title": "مدیر مکاتبات",
        })
        cls.receiver_employee = cls.env["hr.employee"].create({
            "name": "Advanced Receiver", "user_id": cls.receiver.id, "company_id": cls.company.id,
            "department_id": department.id,
        })
        department.manager_id = cls.sender_employee
        cls.folder = cls.env["cas.document.folder"].sudo().create({
            "name": "Advanced Letters", "code": "ADVANCED-LETTERS", "company_id": cls.company.id,
            "manager_user_id": cls.sender.id,
        })

    def test_register_versions_file_and_audits_signature(self):
        record = self.env["cas.correspondence.register"].with_user(self.sender).create({
            "direction": "inbound", "subject": "Inbound Test", "company_id": self.company.id,
            "owner_user_id": self.sender.id, "counterparty": "External Party",
            "file_data": base64.b64encode(b"official inbound"), "file_name": "inbound.txt",
            "document_folder_id": self.folder.id,
        })
        record.with_user(self.sender).action_register()
        self.assertEqual(record.state, "registered")
        self.assertTrue(record.number and record.document_id.current_version_id)
        self.assertEqual(record.document_id.current_version_id.content(), b"official inbound")
        self.assertEqual(record.event_ids.mapped("event_type"), ["registered"])
        signature = self.env["cas.correspondence.signature"].with_user(self.sender).create({
            "register_id": record.id, "signer_user_id": self.sender.id, "method": "organizational",
        })
        signature.with_user(self.sender).action_sign_organizational()
        self.assertEqual(signature.source_digest, record.current_sha256)
        with self.assertRaises(ValidationError):
            signature.write({"source_digest": "changed"})

    def test_template_send_creates_official_pdf_document_and_signature(self):
        template = self.env["cas.correspondence.template"].sudo().create({
            "name": "Official", "code": "OFFICIAL", "company_id": self.company.id,
            "body_html": "<p>Template body</p>", "document_folder_id": self.folder.id,
        })
        letter = self.env["cas.correspondence.letter"].with_user(self.sender).create({
            "subject": "Advanced PDF", "body": "<p>Body</p>", "company_id": self.company.id,
            "template_id": template.id,
        })
        self.env["cas.correspondence.recipient"].with_user(self.sender).create({
            "letter_id": letter.id, "target_kind": "user", "recipient_user_id": self.receiver.id,
            "expectation": "information",
        })
        letter.with_user(self.sender).action_send()
        self.assertTrue(letter.official_pdf_attachment_id)
        self.assertEqual(len(letter.official_pdf_sha256), 64)
        self.assertEqual(letter.document_id.current_sha256, letter.official_pdf_sha256)
        self.assertEqual(letter.advanced_signature_ids.state, "signed")
        self.assertEqual(letter.advanced_signature_ids.source_digest, letter.official_pdf_sha256)
