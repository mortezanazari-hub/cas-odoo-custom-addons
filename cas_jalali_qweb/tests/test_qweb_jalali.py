from datetime import date, datetime

from odoo.tests.common import TransactionCase


class TestJalaliQWebConverters(TransactionCase):
    def test_date_converter(self):
        converter = self.env["ir.qweb.field.date"]
        self.assertEqual(
            converter.value_to_html(date(2026, 7, 14), {}),
            "۱۴۰۵/۰۴/۲۳",
        )
        self.assertEqual(
            converter.value_to_html(
                date(2026, 7, 14),
                {"cas_long": True},
            ),
            "۲۳ تیر ۱۴۰۵",
        )

    def test_datetime_converter(self):
        converter = self.env["ir.qweb.field.datetime"].with_context(
            tz="Asia/Tehran"
        )
        result = converter.value_to_html(
            datetime(2026, 7, 14, 5, 0, 0),
            {"hide_seconds": True},
        )
        self.assertTrue(result.startswith("۱۴۰۵/۰۴/۲۳ "))
        self.assertNotIn(":۰۰:۰۰", result)

    def test_qweb_helpers_are_injected(self):
        values = {}
        self.env["ir.qweb"]._prepare_environment(values)
        self.assertIn("format_jalali_date", values)
        self.assertIn("format_jalali_datetime", values)
        self.assertEqual(
            values["format_jalali_date"](date(2026, 7, 14)),
            "۱۴۰۵/۰۴/۲۳",
        )
