"""Typed metadata for fields contained in a form revision."""

from __future__ import annotations

import re
import uuid

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


TECHNICAL_KEY_RE = re.compile(r"^[a-z][a-z0-9_]*$")
OPTION_FIELD_TYPES = {"single_select", "multi_select", "radio", "dropdown", "tag"}
BASE_ALLOWED_REFERENCE_MODELS = {
    "res.users",
    "res.company",
    "res.partner",
    "hr.employee",
    "hr.department",
    "hr.job",
    "product.product",
    "stock.warehouse",
    "project.project",
    "account.analytic.account",
}


class CasFormVersionedMixin(models.AbstractModel):
    _name = "cas.form.versioned.mixin"
    _description = "CAS Form Versioned Record Mixin"

    version_id = fields.Many2one(
        "cas.form.version",
        string="نسخه فرم",
        required=True,
        ondelete="cascade",
        index=True,
    )
    company_id = fields.Many2one(
        related="version_id.company_id",
        store=True,
        index=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        version_ids = {vals.get("version_id") for vals in vals_list if vals.get("version_id")}
        versions = self.env["cas.form.version"].browse(version_ids).exists()
        if any(version.state != "draft" for version in versions):
            raise ValidationError(
                _("ساختار نسخه منتشرشده یا بایگانی‌شده قابل تغییر نیست.")
            )
        return super().create(vals_list)

    def write(self, vals):
        if any(record.version_id.state != "draft" for record in self):
            raise ValidationError(
                _("ساختار نسخه منتشرشده یا بایگانی‌شده قابل تغییر نیست.")
            )
        if "version_id" in vals:
            raise ValidationError(_("انتقال اجزای فرم بین نسخه‌ها مجاز نیست."))
        return super().write(vals)

    def unlink(self):
        if any(record.version_id.state != "draft" for record in self):
            raise ValidationError(
                _("ساختار نسخه منتشرشده یا بایگانی‌شده قابل حذف نیست.")
            )
        return super().unlink()


class CasFormField(models.Model):
    _name = "cas.form.field"
    _description = "CAS Form Field"
    _inherit = "cas.form.versioned.mixin"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    field_uuid = fields.Char(
        string="شناسه پایدار",
        required=True,
        default=lambda self: str(uuid.uuid4()),
        index=True,
        copy=True,
        readonly=True,
    )
    technical_key = fields.Char(string="کلید فنی", required=True, index=True)
    label = fields.Char(string="عنوان", required=True, translate=True)
    field_type = fields.Selection(
        selection=[
            ("short_text", "متن کوتاه"),
            ("long_text", "متن بلند"),
            ("rich_text", "متن قالب‌دار"),
            ("integer", "عدد صحیح"),
            ("decimal", "عدد اعشاری"),
            ("percentage", "درصد"),
            ("monetary", "مبلغ"),
            ("boolean", "بله/خیر"),
            ("single_select", "انتخاب تکی"),
            ("multi_select", "انتخاب چندگانه"),
            ("radio", "رادیویی"),
            ("dropdown", "فهرست کشویی"),
            ("tag", "برچسب"),
            ("date", "تاریخ"),
            ("datetime", "تاریخ و ساعت"),
            ("time", "ساعت"),
            ("file", "فایل"),
            ("image", "تصویر"),
            ("user", "کاربر"),
            ("employee", "کارکن"),
            ("department", "دپارتمان"),
            ("company", "شرکت"),
            ("record_reference", "رکورد مرتبط"),
            ("computed", "محاسبه‌شده"),
            ("display", "فقط نمایشی"),
        ],
        string="نوع فیلد",
        required=True,
        default="short_text",
        index=True,
    )
    required = fields.Boolean(string="اجباری")
    readonly = fields.Boolean(string="فقط خواندنی")
    reportable = fields.Boolean(
        string="قابل گزارش",
        default=True,
        help="فقط فیلدهای علامت‌گذاری‌شده وارد گزارش‌گیری عمومی می‌شوند.",
    )
    placeholder = fields.Char(string="متن نمونه", translate=True)
    help_text = fields.Text(string="راهنما", translate=True)
    default_value = fields.Json(string="مقدار پیش‌فرض")
    validation_config = fields.Json(
        string="تنظیمات اعتبارسنجی",
        default=dict,
        help="تنظیمات ساختاریافته و بدون کد اجرایی.",
    )
    allowed_model = fields.Char(
        string="مدل مجاز",
        help="فقط برای نوع رکورد مرتبط و پس از کنترل فهرست مجاز استفاده می‌شود.",
    )
    option_ids = fields.One2many(
        "cas.form.field.option",
        "field_id",
        string="گزینه‌ها",
        copy=True,
    )

    _key_version_uniq = models.Constraint(
        "UNIQUE(version_id, technical_key)",
        "کلید فنی فیلد باید در هر نسخه یکتا باشد.",
    )
    _uuid_version_uniq = models.Constraint(
        "UNIQUE(version_id, field_uuid)",
        "شناسه پایدار فیلد باید در هر نسخه یکتا باشد.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("technical_key"):
                vals["technical_key"] = vals["technical_key"].strip().lower()
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("technical_key"):
            vals["technical_key"] = vals["technical_key"].strip().lower()
        if "field_uuid" in vals:
            raise ValidationError(_("شناسه پایدار فیلد قابل تغییر نیست."))
        return super().write(vals)

    @api.model
    def _get_allowed_reference_models(self):
        """Extension point for trusted business modules to add safe models."""
        return set(BASE_ALLOWED_REFERENCE_MODELS)

    @api.constrains("technical_key")
    def _check_technical_key(self):
        for record in self:
            if record.technical_key and not TECHNICAL_KEY_RE.fullmatch(
                record.technical_key
            ):
                raise ValidationError(
                    _(
                        "کلید فنی فیلد باید با حرف انگلیسی کوچک شروع شود و فقط "
                        "شامل حروف انگلیسی کوچک، عدد و زیرخط باشد."
                    )
                )

    @api.constrains("allowed_model", "field_type")
    def _check_allowed_model_usage(self):
        for record in self:
            if record.allowed_model and record.field_type != "record_reference":
                raise ValidationError(
                    _("مدل مجاز فقط برای فیلد «رکورد مرتبط» قابل تعیین است.")
                )
            if (
                record.field_type == "record_reference"
                and record.allowed_model
                and record.allowed_model not in record._get_allowed_reference_models()
            ):
                raise ValidationError(
                    _("مدل «%s» در فهرست مجاز فرم‌ها نیست.", record.allowed_model)
                )

    def _validate_definition(self):
        for record in self:
            if record.field_type in OPTION_FIELD_TYPES and not record.option_ids:
                raise ValidationError(
                    _("فیلد «%s» باید حداقل یک گزینه داشته باشد.", record.label)
                )
            if record.field_type == "record_reference" and not record.allowed_model:
                raise ValidationError(
                    _("برای فیلد «%s» باید مدل مجاز مشخص شود.", record.label)
                )
        return True


class CasFormFieldOption(models.Model):
    _name = "cas.form.field.option"
    _description = "CAS Form Field Option"
    _order = "sequence, id"

    field_id = fields.Many2one(
        "cas.form.field",
        string="فیلد",
        required=True,
        ondelete="cascade",
        index=True,
    )
    version_id = fields.Many2one(
        related="field_id.version_id",
        store=True,
        index=True,
    )
    company_id = fields.Many2one(
        related="field_id.company_id",
        store=True,
        index=True,
    )
    sequence = fields.Integer(default=10)
    technical_key = fields.Char(string="کلید فنی", required=True)
    label = fields.Char(string="عنوان", required=True, translate=True)
    active = fields.Boolean(default=True)

    _key_uniq = models.Constraint(
        "UNIQUE(field_id, technical_key)",
        "کلید فنی گزینه باید در هر فیلد یکتا باشد.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        field_ids = {vals.get("field_id") for vals in vals_list if vals.get("field_id")}
        form_fields = self.env["cas.form.field"].browse(field_ids).exists()
        if any(field.version_id.state != "draft" for field in form_fields):
            raise ValidationError(_("گزینه‌های نسخه منتشرشده قابل تغییر نیستند."))
        for vals in vals_list:
            if vals.get("technical_key"):
                vals["technical_key"] = vals["technical_key"].strip().lower()
        return super().create(vals_list)

    def write(self, vals):
        if any(option.version_id.state != "draft" for option in self):
            raise ValidationError(_("گزینه‌های نسخه منتشرشده قابل تغییر نیستند."))
        if "field_id" in vals:
            raise ValidationError(_("انتقال گزینه بین فیلدها مجاز نیست."))
        if vals.get("technical_key"):
            vals["technical_key"] = vals["technical_key"].strip().lower()
        return super().write(vals)

    def unlink(self):
        if any(option.version_id.state != "draft" for option in self):
            raise ValidationError(_("گزینه‌های نسخه منتشرشده قابل حذف نیستند."))
        return super().unlink()

    @api.constrains("technical_key")
    def _check_technical_key(self):
        for record in self:
            if record.technical_key and not TECHNICAL_KEY_RE.fullmatch(
                record.technical_key
            ):
                raise ValidationError(_("کلید فنی گزینه معتبر نیست."))
