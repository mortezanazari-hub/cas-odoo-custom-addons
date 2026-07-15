"""Typed values stored for CAS dynamic form submissions."""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


TEXT_TYPES = {"short_text", "long_text", "rich_text"}
INTEGER_TYPES = {"integer"}
FLOAT_TYPES = {"decimal", "percentage"}
OPTION_TYPES = {"single_select", "radio", "dropdown", "tag"}
MULTI_OPTION_TYPES = {"multi_select"}
REFERENCE_TYPE_MODELS = {
    "user": "res.users",
    "employee": "hr.employee",
    "department": "hr.department",
    "company": "res.company",
}
UNSUPPORTED_RUNTIME_TYPES = {"file", "image"}
NON_INPUT_TYPES = {"computed", "display"}


class CasFormAnswer(models.Model):
    _name = "cas.form.answer"
    _description = "CAS Form Typed Answer"
    _order = "field_sequence, id"

    submission_id = fields.Many2one(
        "cas.form.submission",
        string="ثبت فرم",
        required=True,
        ondelete="cascade",
        index=True,
    )
    company_id = fields.Many2one(
        related="submission_id.company_id",
        store=True,
        index=True,
    )
    field_id = fields.Many2one(
        "cas.form.field",
        string="فیلد",
        required=True,
        ondelete="restrict",
        index=True,
    )
    field_sequence = fields.Integer(related="field_id.sequence", store=True)
    field_type = fields.Selection(related="field_id.field_type", store=True, index=True)
    field_key = fields.Char(related="field_id.technical_key", store=True, index=True)

    value_char = fields.Char(string="مقدار متنی کوتاه")
    value_text = fields.Text(string="مقدار متنی بلند")
    value_integer = fields.Integer(string="مقدار عدد صحیح")
    value_float = fields.Float(string="مقدار عدد اعشاری", digits=(16, 6))
    value_boolean = fields.Boolean(string="مقدار بله/خیر")
    value_date = fields.Date(string="مقدار تاریخ")
    value_datetime = fields.Datetime(string="مقدار تاریخ و ساعت")
    value_time_seconds = fields.Integer(string="مقدار ساعت به ثانیه")
    value_monetary = fields.Monetary(
        string="مقدار مبلغ",
        currency_field="currency_id",
    )
    currency_id = fields.Many2one("res.currency", string="ارز")
    value_option_id = fields.Many2one(
        "cas.form.field.option",
        string="گزینه انتخابی",
        ondelete="restrict",
    )
    value_option_ids = fields.Many2many(
        "cas.form.field.option",
        "cas_form_answer_option_rel",
        "answer_id",
        "option_id",
        string="گزینه‌های انتخابی",
    )
    value_reference_model = fields.Char(string="مدل رکورد مرتبط", index=True)
    value_reference_id = fields.Integer(string="شناسه رکورد مرتبط", index=True)
    value_reference_name = fields.Char(string="عنوان ثبت‌شده رکورد مرتبط")
    value_json = fields.Json(string="مقدار ساختاریافته")

    _submission_field_uniq = models.Constraint(
        "UNIQUE(submission_id, field_id)",
        "برای هر فیلد در هر ثبت فقط یک پاسخ مجاز است.",
    )

    @api.constrains("submission_id", "field_id")
    def _check_field_version(self):
        for answer in self:
            if answer.field_id.version_id != answer.submission_id.version_id:
                raise ValidationError(
                    _("فیلد پاسخ باید متعلق به نسخه ثبت‌شده فرم باشد.")
                )

    @api.model_create_multi
    def create(self, vals_list):
        submission_ids = {
            vals.get("submission_id") for vals in vals_list if vals.get("submission_id")
        }
        submissions = self.env["cas.form.submission"].browse(submission_ids).exists()
        if any(submission.state != "draft" for submission in submissions):
            raise ValidationError(_("پاسخ‌های فرم ارسال‌شده قابل تغییر نیستند."))
        return super().create(vals_list)

    def write(self, vals):
        if any(answer.submission_id.state != "draft" for answer in self):
            raise ValidationError(_("پاسخ‌های فرم ارسال‌شده قابل تغییر نیستند."))
        if {"submission_id", "field_id"}.intersection(vals):
            raise ValidationError(_("انتقال پاسخ بین فرم یا فیلد مجاز نیست."))
        return super().write(vals)

    def unlink(self):
        if any(answer.submission_id.state != "draft" for answer in self):
            raise ValidationError(_("پاسخ‌های فرم ارسال‌شده قابل حذف نیستند."))
        return super().unlink()

    @staticmethod
    def _empty_value_dict():
        return {
            "value_char": False,
            "value_text": False,
            "value_integer": 0,
            "value_float": 0.0,
            "value_boolean": False,
            "value_date": False,
            "value_datetime": False,
            "value_time_seconds": 0,
            "value_monetary": 0.0,
            "currency_id": False,
            "value_option_id": False,
            "value_option_ids": [(5, 0, 0)],
            "value_reference_model": False,
            "value_reference_id": 0,
            "value_reference_name": False,
            "value_json": False,
        }

    @staticmethod
    def _decimal_value(value, label):
        if isinstance(value, bool):
            raise ValidationError(_("مقدار فیلد «%s» باید عدد باشد.", label))
        try:
            return Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError) as error:
            raise ValidationError(
                _("مقدار فیلد «%s» باید عدد معتبر باشد.", label)
            ) from error

    @staticmethod
    def _validate_numeric_config(form_field, value):
        config = form_field.validation_config or {}
        if config.get("min") is not None and value < Decimal(str(config["min"])):
            raise ValidationError(
                _("مقدار فیلد «%s» کمتر از حداقل مجاز است.", form_field.label)
            )
        if config.get("max") is not None and value > Decimal(str(config["max"])):
            raise ValidationError(
                _("مقدار فیلد «%s» بیشتر از حداکثر مجاز است.", form_field.label)
            )
        decimal_places = config.get("decimal_places")
        if decimal_places is not None:
            actual_places = max(0, -value.as_tuple().exponent)
            if actual_places > int(decimal_places):
                raise ValidationError(
                    _(
                        "مقدار فیلد «%s» حداکثر می‌تواند %s رقم اعشار داشته باشد.",
                        form_field.label,
                        decimal_places,
                    )
                )

    @staticmethod
    def _validate_text_config(form_field, value):
        config = form_field.validation_config or {}
        if config.get("min_length") is not None and len(value) < int(
            config["min_length"]
        ):
            raise ValidationError(
                _("مقدار فیلد «%s» کوتاه‌تر از حد مجاز است.", form_field.label)
            )
        if config.get("max_length") is not None and len(value) > int(
            config["max_length"]
        ):
            raise ValidationError(
                _("مقدار فیلد «%s» بلندتر از حد مجاز است.", form_field.label)
            )
        pattern = config.get("regex")
        if pattern:
            try:
                matched = re.fullmatch(pattern, value)
            except re.error as error:
                raise ValidationError(
                    _("عبارت منظم فیلد «%s» معتبر نیست.", form_field.label)
                ) from error
            if not matched:
                raise ValidationError(
                    config.get("error_message")
                    or _("فرمت مقدار فیلد «%s» معتبر نیست.", form_field.label)
                )

    @staticmethod
    def _parse_time_seconds(value, label):
        if isinstance(value, int) and not isinstance(value, bool):
            seconds = value
        elif isinstance(value, str):
            matched = re.fullmatch(r"(\d{1,2}):(\d{2})(?::(\d{2}))?", value.strip())
            if not matched:
                raise ValidationError(
                    _("ساعت فیلد «%s» باید به‌شکل HH:MM یا HH:MM:SS باشد.", label)
                )
            hours, minutes, seconds_part = matched.groups()
            if int(hours) > 23 or int(minutes) > 59 or int(seconds_part or 0) > 59:
                raise ValidationError(_("ساعت فیلد «%s» معتبر نیست.", label))
            seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds_part or 0)
        else:
            raise ValidationError(_("ساعت فیلد «%s» معتبر نیست.", label))
        if seconds < 0 or seconds >= 86400:
            raise ValidationError(_("ساعت فیلد «%s» معتبر نیست.", label))
        return seconds

    @api.model
    def _normalized_values(self, form_field, value):
        values = self._empty_value_dict()
        field_type = form_field.field_type

        if field_type in NON_INPUT_TYPES:
            raise ValidationError(_("فیلد «%s» قابل ورود توسط کاربر نیست.", form_field.label))
        if field_type in UNSUPPORTED_RUNTIME_TYPES:
            raise ValidationError(
                _("ذخیره نوع فیلد «%s» در برش بعدی فعال می‌شود.", form_field.label)
            )

        if field_type in TEXT_TYPES:
            if not isinstance(value, str):
                raise ValidationError(_("مقدار فیلد «%s» باید متن باشد.", form_field.label))
            config = form_field.validation_config or {}
            if config.get("trim", True):
                value = value.strip()
            self._validate_text_config(form_field, value)
            target = "value_char" if field_type == "short_text" else "value_text"
            values[target] = value
        elif field_type in INTEGER_TYPES:
            if not isinstance(value, int) or isinstance(value, bool):
                raise ValidationError(
                    _("مقدار فیلد «%s» باید عدد صحیح باشد.", form_field.label)
                )
            decimal_value = Decimal(value)
            self._validate_numeric_config(form_field, decimal_value)
            values["value_integer"] = value
        elif field_type in FLOAT_TYPES:
            decimal_value = self._decimal_value(value, form_field.label)
            self._validate_numeric_config(form_field, decimal_value)
            if field_type == "percentage" and not (Decimal("0") <= decimal_value <= Decimal("100")):
                raise ValidationError(_("درصد باید بین صفر و صد باشد."))
            values["value_float"] = float(decimal_value)
        elif field_type == "monetary":
            payload = value if isinstance(value, dict) else {"amount": value}
            decimal_value = self._decimal_value(payload.get("amount"), form_field.label)
            self._validate_numeric_config(form_field, decimal_value)
            currency = self.env["res.currency"].browse(
                payload.get("currency_id") or self.env.company.currency_id.id
            ).exists()
            if not currency:
                raise ValidationError(_("ارز فیلد «%s» معتبر نیست.", form_field.label))
            values.update(
                {
                    "value_monetary": float(decimal_value),
                    "currency_id": currency.id,
                }
            )
        elif field_type == "boolean":
            if not isinstance(value, bool):
                raise ValidationError(_("مقدار فیلد «%s» باید بله/خیر باشد.", form_field.label))
            values["value_boolean"] = value
        elif field_type == "date":
            try:
                values["value_date"] = fields.Date.to_date(value)
            except (TypeError, ValueError) as error:
                raise ValidationError(_("تاریخ فیلد «%s» معتبر نیست.", form_field.label)) from error
        elif field_type == "datetime":
            try:
                values["value_datetime"] = fields.Datetime.to_datetime(value)
            except (TypeError, ValueError) as error:
                raise ValidationError(
                    _("تاریخ و ساعت فیلد «%s» معتبر نیست.", form_field.label)
                ) from error
        elif field_type == "time":
            values["value_time_seconds"] = self._parse_time_seconds(
                value, form_field.label
            )
        elif field_type in OPTION_TYPES:
            option = form_field.option_ids.filtered(
                lambda item: item.active and item.technical_key == value
            )
            if len(option) != 1:
                raise ValidationError(_("گزینه فیلد «%s» معتبر نیست.", form_field.label))
            values["value_option_id"] = option.id
        elif field_type in MULTI_OPTION_TYPES:
            if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                raise ValidationError(
                    _("مقدار فیلد «%s» باید فهرستی از گزینه‌ها باشد.", form_field.label)
                )
            option_keys = set(value)
            options = form_field.option_ids.filtered(
                lambda item: item.active and item.technical_key in option_keys
            )
            if set(options.mapped("technical_key")) != option_keys:
                raise ValidationError(_("یکی از گزینه‌های فیلد «%s» معتبر نیست.", form_field.label))
            values["value_option_ids"] = [(6, 0, options.ids)]
        elif field_type in REFERENCE_TYPE_MODELS or field_type == "record_reference":
            model_name = (
                REFERENCE_TYPE_MODELS.get(field_type) or form_field.allowed_model
            )
            if (
                field_type == "record_reference"
                and model_name not in form_field._get_allowed_reference_models()
            ):
                raise ValidationError(_("مدل مرتبط «%s» مجاز نیست.", model_name))
            if model_name not in self.env.registry:
                raise ValidationError(_("مدل مرتبط «%s» در سیستم نصب نیست.", model_name))
            if not isinstance(value, int) or isinstance(value, bool):
                raise ValidationError(_("شناسه رکورد مرتبط باید عدد صحیح باشد."))
            record = self.env[model_name].browse(value).exists()
            if not record:
                raise ValidationError(_("رکورد مرتبط یافت نشد."))
            record.check_access("read")
            if field_type == "company" and record not in self.env.companies:
                raise ValidationError(_("شرکت انتخاب‌شده در محدوده دسترسی کاربر نیست."))
            values.update(
                {
                    "value_reference_model": model_name,
                    "value_reference_id": record.id,
                    "value_reference_name": record.display_name,
                }
            )
        else:
            raise ValidationError(
                _("نوع فیلد «%s» هنوز توسط ذخیره‌ساز پشتیبانی نمی‌شود.", field_type)
            )
        return values

    def _is_empty(self):
        self.ensure_one()
        field_type = self.field_type
        if field_type in TEXT_TYPES:
            return not (self.value_char or self.value_text)
        if field_type in MULTI_OPTION_TYPES:
            return not self.value_option_ids
        if field_type in OPTION_TYPES:
            return not self.value_option_id
        if field_type in REFERENCE_TYPE_MODELS or field_type == "record_reference":
            return not (self.value_reference_model and self.value_reference_id)
        if field_type == "date":
            return not self.value_date
        if field_type == "datetime":
            return not self.value_datetime
        if field_type == "monetary":
            return not self.currency_id
        return False

    def _export_value(self):
        self.ensure_one()
        field_type = self.field_type
        if field_type == "short_text":
            return self.value_char
        if field_type in {"long_text", "rich_text"}:
            return self.value_text
        if field_type == "integer":
            return self.value_integer
        if field_type in FLOAT_TYPES:
            return self.value_float
        if field_type == "monetary":
            return {
                "amount": self.value_monetary,
                "currency_id": self.currency_id.id,
                "currency": self.currency_id.name,
            }
        if field_type == "boolean":
            return self.value_boolean
        if field_type == "date":
            return fields.Date.to_string(self.value_date)
        if field_type == "datetime":
            return fields.Datetime.to_string(self.value_datetime)
        if field_type == "time":
            return self.value_time_seconds
        if field_type in OPTION_TYPES:
            return self.value_option_id.technical_key
        if field_type in MULTI_OPTION_TYPES:
            return self.value_option_ids.sorted(
                key=lambda option: (option.sequence, option.id)
            ).mapped("technical_key")
        if field_type in REFERENCE_TYPE_MODELS or field_type == "record_reference":
            return {
                "model": self.value_reference_model,
                "id": self.value_reference_id,
                "display_name": self.value_reference_name,
            }
        return self.value_json
