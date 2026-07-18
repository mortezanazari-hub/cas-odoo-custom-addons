from odoo.tests.common import TransactionCase


class TestCasAttendanceSystemAdmin(TransactionCase):
    def test_system_admin_inherits_all_attendance_roles(self):
        administrator = self.env.ref("base.user_admin")
        self.assertTrue(
            administrator.has_group(
                "cas_attendance_core.group_cas_attendance_manager"
            )
        )
        self.assertTrue(
            administrator.has_group(
                "cas_attendance_core.group_cas_attendance_device_importer"
            )
        )
