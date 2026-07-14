from datetime import date, datetime

from odoo.tests.common import TransactionCase

from ..tools.jalali import (
    format_jalali_date,
    format_jalali_datetime,
    format_jalali_date_long,
    format_jalali_datetime_long,
    format_jalali_time,
    from_jalali,
    is_jalali_leap,
    parse_jalali_date,
    to_jalali,
)


class TestJalaliConversion(TransactionCase):
    def test_known_conversion_2026(self):
        self.assertEqual(
            to_jalali(date(2026, 7, 14)),
            type(to_jalali(date(2026, 7, 14)))(1405, 4, 23),
        )
        self.assertEqual(from_jalali(1405, 4, 23), date(2026, 7, 14))

    def test_nowruz_boundaries(self):
        self.assertEqual(
            (to_jalali(date(2025, 3, 20)).year,
             to_jalali(date(2025, 3, 20)).month,
             to_jalali(date(2025, 3, 20)).day),
            (1403, 12, 30),
        )
        self.assertEqual(
            (to_jalali(date(2025, 3, 21)).year,
             to_jalali(date(2025, 3, 21)).month,
             to_jalali(date(2025, 3, 21)).day),
            (1404, 1, 1),
        )

    def test_input_digits(self):
        expected = date(2026, 7, 14)
        self.assertEqual(parse_jalali_date("1405/04/23"), expected)
        self.assertEqual(parse_jalali_date("۱۴۰۵/۰۴/۲۳"), expected)
        self.assertEqual(parse_jalali_date("١٤٠٥/٠٤/٢٣"), expected)

    def test_formatting(self):
        self.assertEqual(format_jalali_date(date(2026, 7, 14)), "۱۴۰۵/۰۴/۲۳")
        self.assertEqual(
            format_jalali_datetime(datetime(2026, 7, 14, 9, 5)),
            "۱۴۰۵/۰۴/۲۳ ۰۹:۰۵",
        )

    def test_leap_year(self):
        self.assertTrue(is_jalali_leap(1403))
        self.assertFalse(is_jalali_leap(1404))


    def test_long_formatting(self):
        value = datetime(2026, 7, 14, 9, 5)
        self.assertEqual(
            format_jalali_date_long(value),
            "۲۳ تیر ۱۴۰۵",
        )
        self.assertEqual(
            format_jalali_time(value),
            "۰۹:۰۵",
        )
        self.assertEqual(
            format_jalali_datetime_long(value),
            "۲۳ تیر ۱۴۰۵، ۰۹:۰۵",
        )
