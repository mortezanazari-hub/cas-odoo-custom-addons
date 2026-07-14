"""Shared Jalali formatting helpers inside the QWeb environment."""

from __future__ import annotations

from odoo import api, fields, models
from odoo.addons.cas_jalali.tools.jalali import (
    format_jalali_date,
    format_jalali_date_long,
    format_jalali_datetime,
    format_jalali_datetime_long,
)


class IrQWeb(models.AbstractModel):
    _inherit = "ir.qweb"

    @api.model
    def _cas_qweb_format_date(
        self,
        value,
        long=False,
        weekday=False,
        latin_digits=False,
    ):
        if not value:
            return ""
        if isinstance(value, str):
            value = fields.Date.from_string(value)
        if long or weekday:
            return format_jalali_date_long(
                value,
                persian_digits=not latin_digits,
                include_weekday=weekday,
            )
        return format_jalali_date(
            value,
            persian_digits=not latin_digits,
        )

    @api.model
    def _cas_qweb_format_datetime(
        self,
        value,
        long=False,
        weekday=False,
        hide_seconds=True,
        latin_digits=False,
        tz_name=None,
    ):
        if not value:
            return ""
        if isinstance(value, str):
            value = fields.Datetime.from_string(value)

        formatter = self.with_context(tz=tz_name) if tz_name else self
        localized = fields.Datetime.context_timestamp(formatter, value)

        if long or weekday:
            return format_jalali_datetime_long(
                localized,
                persian_digits=not latin_digits,
                include_weekday=weekday,
                show_seconds=not hide_seconds,
            )
        return format_jalali_datetime(
            localized,
            persian_digits=not latin_digits,
            show_seconds=not hide_seconds,
        )

    @api.model
    def _prepare_environment(self, values):
        result = super()._prepare_environment(values)
        values.setdefault("format_jalali_date", self._cas_qweb_format_date)
        values.setdefault(
            "format_jalali_datetime",
            self._cas_qweb_format_datetime,
        )
        return result
