"""Jalali formatting bridge for chatter tracking values."""

from __future__ import annotations

from odoo import fields, models

from odoo.addons.cas_jalali.tools.jalali import (
    format_jalali_date,
    format_jalali_datetime,
)


class MailTrackingValue(models.Model):
    _inherit = "mail.tracking.value"

    def _cas_jalali_format_tracking_value(self, value, field_type):
        """Convert a serialized Odoo tracking value for human display only."""
        if not value:
            return value

        if field_type == "date":
            parsed = fields.Date.from_string(value)
            return format_jalali_date(parsed)

        if field_type == "datetime":
            serialized = str(value)
            if serialized.endswith("Z"):
                serialized = serialized[:-1]
            parsed_utc = fields.Datetime.from_string(serialized)
            localized = fields.Datetime.context_timestamp(self, parsed_utc)
            return format_jalali_datetime(localized)

        return value

    def _tracking_value_format_model(self, model):
        """Return Jalali strings and mark them as text for the mail frontend.

        Odoo normally sends ISO date/datetime strings together with fieldType
        ``date`` or ``datetime``. The mail frontend then formats those values
        independently from normal field widgets. We convert the final
        serialized payload and change its presentation type to ``char`` so it
        is displayed verbatim and never reparsed as Gregorian.
        """
        formatted = super()._tracking_value_format_model(model)

        for item in formatted:
            field_info = item.get("fieldInfo") or {}
            source_type = field_info.get("fieldType")
            if source_type not in {"date", "datetime"}:
                continue

            item["oldValue"] = self._cas_jalali_format_tracking_value(
                item.get("oldValue"),
                source_type,
            )
            item["newValue"] = self._cas_jalali_format_tracking_value(
                item.get("newValue"),
                source_type,
            )
            item["fieldInfo"] = {
                **field_info,
                "fieldType": "char",
                "jalaliSourceType": source_type,
            }

        return formatted
