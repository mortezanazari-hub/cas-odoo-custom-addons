from datetime import timedelta

from odoo import fields
from odoo.exceptions import AccessError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCasDocumentCore(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        company = cls.env.company
        base = cls.env.ref("base.group_user")
        doc_user = cls.env.ref("cas_document_core.group_cas_document_user")
        doc_manager = cls.env.ref("cas_document_core.group_cas_document_manager")

        def make_user(role, groups):
            return cls.env["res.users"].with_context(no_reset_password=True).create(
                {
                    "name": f"Document {role}",
                    "login": f"document.{role}",
                    "company_id": company.id,
                    "company_ids": [(6, 0, company.ids)],
                    "group_ids": [(6, 0, [base.id] + [group.id for group in groups])],
                }
            )

        cls.owner = make_user("owner", [doc_user])
        cls.reader = make_user("reader", [doc_user])
        cls.outsider = make_user("outsider", [doc_user])
        cls.manager = make_user("manager", [doc_manager])
        cls.backend = cls.env["cas.document.storage.backend"].create(
            {
                "name": "Test Database",
                "company_id": company.id,
                "backend_type": "database",
                "is_default": True,
            }
        )
        cls.folder = cls.env["cas.document.folder"].create(
            {
                "name": "Test Folder",
                "code": "test-folder",
                "company_id": company.id,
                "manager_user_id": cls.manager.id,
            }
        )
        cls.document = cls.env["cas.document"].with_user(cls.owner).create(
            {
                "name": "Versioned Test Document",
                "company_id": company.id,
                "folder_id": cls.folder.id,
                "owner_user_id": cls.owner.id,
                "authorized_user_ids": [(6, 0, [cls.reader.id])],
                "storage_backend_id": cls.backend.id,
            }
        )

    def test_version_checksum_lifecycle_and_audit(self):
        version = self.document.with_user(self.owner).add_version(
            "test.txt", b"CAS document version one", "text/plain", "Initial"
        )
        self.assertEqual(version.version_number, 1)
        self.assertEqual(len(version.sha256), 64)
        self.assertEqual(version.content(), b"CAS document version one")
        self.assertEqual(self.document.current_version_id, version)
        self.document.with_user(self.owner).action_activate()
        self.assertEqual(self.document.state, "active")
        self.assertEqual(
            set(self.document.event_ids.mapped("event_type")),
            {"created", "version_added", "activated"},
        )

    def test_duplicate_and_immutable_version(self):
        version = self.document.with_user(self.owner).add_version("same.txt", b"same")
        with self.assertRaises(ValidationError):
            self.document.with_user(self.owner).add_version("same-again.txt", b"same")
        with self.assertRaises(ValidationError):
            version.write({"filename": "changed.txt"})
        with self.assertRaises(ValidationError):
            version.unlink()

    def test_security_owner_reader_outsider_manager(self):
        self.assertTrue(self.document.with_user(self.owner).has_access("read"))
        self.assertTrue(self.document.with_user(self.reader).has_access("read"))
        self.assertFalse(self.document.with_user(self.outsider).has_access("read"))
        self.assertTrue(self.document.with_user(self.manager).has_access("read"))
        with self.assertRaises(AccessError):
            self.document.with_user(self.outsider).add_version("forbidden.txt", b"no")

    def test_retention_and_legal_hold(self):
        self.document.with_context(cas_document_engine=True).write(
            {"retention_until": fields.Date.context_today(self.env.user) - timedelta(days=1), "legal_hold": True}
        )
        with self.assertRaises(ValidationError):
            self.document.with_user(self.manager).action_destroy()
        self.document.with_user(self.manager).write({"legal_hold": False})
        self.document.with_user(self.manager).action_destroy()
        self.assertEqual(self.document.state, "destroyed")

    def test_manual_ocr_review_is_bound_to_version(self):
        version = self.document.with_user(self.owner).add_version("scan.txt", b"scan")
        provider = self.env["cas.document.ocr.provider"].create(
            {"name": "Manual", "company_id": self.env.company.id, "provider_type": "manual"}
        )
        job = self.env["cas.document.ocr.job"].with_user(self.reader).create(
            {"version_id": version.id, "provider_id": provider.id}
        )
        job.with_user(self.reader).action_submit_review()
        job.with_user(self.reader).write({"extracted_text": "متن بازبینی‌شده"})
        job.with_user(self.reader).action_confirm_text()
        self.assertEqual(job.state, "done")
        self.assertEqual(version.ocr_text, "متن بازبینی‌شده")
        self.assertIn("ocr_completed", self.document.event_ids.mapped("event_type"))

    def test_nextcloud_requires_explicit_contract(self):
        with self.assertRaises(ValidationError):
            self.env["cas.document.storage.backend"].create(
                {
                    "name": "Incomplete Nextcloud",
                    "company_id": self.env.company.id,
                    "backend_type": "nextcloud",
                }
            )
