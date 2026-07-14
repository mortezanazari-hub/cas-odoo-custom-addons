from datetime import date, datetime

from odoo.tests.common import TransactionCase


class TestJalaliTrackingValue(TransactionCase):
    def setUp(self):
        super().setUp()
        self.tracking_model = self.env["mail.tracking.value"]

    def test_date_display_helper(self):
        self.assertEqual(
            self.tracking_model._cas_jalali_format_tracking_value(
                "2026-07-14",
                "date",
            ),
            "۱۴۰۵/۰۴/۲۳",
        )

    def test_datetime_display_helper(self):
        result = self.tracking_model.with_context(
            tz="Asia/Tehran"
        )._cas_jalali_format_tracking_value(
            "2026-07-14 05:00:00Z",
            "datetime",
        )
        self.assertTrue(result.startswith("۱۴۰۵/۰۴/۲۳ "))
