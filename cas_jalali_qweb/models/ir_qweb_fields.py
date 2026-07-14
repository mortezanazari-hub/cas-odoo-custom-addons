"""Jalali QWeb field converters.

These converters affect human-facing ``t-field`` output only. Storage and ORM
values remain standard Gregorian/UTC.
"""

from __future__ import annotations

from odoo import api, fields, models, _
from odoo.addons.cas_jalali.tools.jalali import (
    format_jalali_date,
    format_jalali_date_long,
    format_jalali_datetime,
    format_jalali_datetime_long,
    format_jalali_time,
)


class IrQwebFieldDate(models.AbstractModel):
    _inherit = "ir.qweb.field.date"

    @api.model
    def get_available_options(self):
        options = super().get_available_options()
        options.update(
            cas_gregorian={
                "type": "boolean",
                "string": _("Keep Gregorian output"),
            },
            cas_long={
                "type": "boolean",
                "string": _("Use long Jalali date"),
            },
            cas_weekday={
                "type": "boolean",
                "string": _("Include weekday"),
            },
            cas_latin_digits={
                "type": "boolean",
                "string": _("Use Latin digits"),
            },
        )
        return options

    @api.model
    def value_to_html(self, value, options):
        if options.get("cas_gregorian"):
            return super().value_to_html(value, options)

        if not value:
            return ""
        if isinstance(value, str):
            value = fields.Date.from_string(value)

        persian_digits = not options.get("cas_latin_digits")
        if options.get("cas_long") or options.get("cas_weekday"):
            return format_jalali_date_long(
                value,
                persian_digits=persian_digits,
                include_weekday=bool(options.get("cas_weekday")),
            )
        return format_jalali_date(value, persian_digits=persian_digits)


class IrQwebFieldDatetime(models.AbstractModel):
    _inherit = "ir.qweb.field.datetime"

    @api.model
    def get_available_options(self):
        options = super().get_available_options()
        options.update(
            cas_gregorian={
                "type": "boolean",
                "string": _("Keep Gregorian output"),
            },
            cas_long={
                "type": "boolean",
                "string": _("Use long Jalali date"),
            },
            cas_weekday={
                "type": "boolean",
                "string": _("Include weekday"),
            },
            cas_latin_digits={
                "type": "boolean",
                "string": _("Use Latin digits"),
            },
        )
        return options

    @api.model
    def value_to_html(self, value, options):
        if options.get("cas_gregorian"):
            return super().value_to_html(value, options)
        if not value:
            return ""

        if isinstance(value, str):
            value = fields.Datetime.from_string(value)

        formatter = self
        if options.get("tz_name"):
            formatter = self.with_context(tz=options["tz_name"])
        localized = fields.Datetime.context_timestamp(formatter, value)

        persian_digits = not options.get("cas_latin_digits")
        show_seconds = not bool(options.get("hide_seconds"))

        if options.get("time_only"):
            return format_jalali_time(
                localized,
                persian_digits=persian_digits,
                show_seconds=show_seconds,
            )

        if options.get("date_only"):
            if options.get("cas_long") or options.get("cas_weekday"):
                return format_jalali_date_long(
                    localized,
                    persian_digits=persian_digits,
                    include_weekday=bool(options.get("cas_weekday")),
                )
            return format_jalali_date(
                localized,
                persian_digits=persian_digits,
            )

        if options.get("cas_long") or options.get("cas_weekday"):
            return format_jalali_datetime_long(
                localized,
                persian_digits=persian_digits,
                include_weekday=bool(options.get("cas_weekday")),
                show_seconds=show_seconds,
            )
        return format_jalali_datetime(
            localized,
            persian_digits=persian_digits,
            show_seconds=show_seconds,
        )
