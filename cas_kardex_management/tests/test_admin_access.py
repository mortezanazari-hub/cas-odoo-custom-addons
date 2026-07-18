from odoo.tests.common import TransactionCase


class TestCasKardexSystemAdmin(TransactionCase):
    def test_system_admin_inherits_ceo_role(self):
        administrator = self.env.ref("base.user_admin")
        self.assertTrue(
            administrator.has_group("cas_kardex_management.group_cas_kardex_ceo")
        )
        self.assertTrue(
            administrator.has_group(
                "cas_kardex_management.group_cas_kardex_manager"
            )
        )
