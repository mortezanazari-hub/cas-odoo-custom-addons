"""Versioned layout tree for CAS forms."""

from __future__ import annotations

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .form_field import TECHNICAL_KEY_RE


class CasFormNode(models.Model):
    _name = "cas.form.node"
    _description = "CAS Form Layout Node"
    _inherit = "cas.form.versioned.mixin"
    _order = "sequence, id"
    _parent_name = "parent_id"
    _parent_store = True

    sequence = fields.Integer(default=10)
    technical_key = fields.Char(string="کلید فنی", required=True, index=True)
    node_type = fields.Selection(
        [
            ("page", "صفحه/مرحله"),
            ("tab", "زبانه"),
            ("section", "بخش"),
            ("group", "گروه"),
            ("field", "فیلد"),
            ("separator", "جداکننده"),
            ("text", "متن راهنما"),
        ],
        string="نوع",
        required=True,
        default="field",
        index=True,
    )
    title = fields.Char(string="عنوان", translate=True)
    help_text = fields.Text(string="توضیح", translate=True)
    parent_id = fields.Many2one(
        "cas.form.node",
        string="والد",
        ondelete="cascade",
        index=True,
        domain="[('version_id', '=', version_id)]",
    )
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many("cas.form.node", "parent_id", string="اجزا")
    field_id = fields.Many2one(
        "cas.form.field",
        string="فیلد",
        ondelete="cascade",
        domain="[('version_id', '=', version_id)]",
    )
    column_count = fields.Integer(string="تعداد ستون", default=1)
    column_span = fields.Integer(string="عرض ستونی", default=1)

    _key_version_uniq = models.Constraint(
        "UNIQUE(version_id, technical_key)",
        "کلید فنی جزء فرم باید در هر نسخه یکتا باشد.",
    )
    _columns_range = models.Constraint(
        "CHECK(column_count >= 1 AND column_count <= 12 "
        "AND column_span >= 1 AND column_span <= 12)",
        "تعداد و عرض ستون باید بین ۱ تا ۱۲ باشد.",
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
        return super().write(vals)

    @api.constrains("technical_key")
    def _check_technical_key(self):
        for record in self:
            if record.technical_key and not TECHNICAL_KEY_RE.fullmatch(
                record.technical_key
            ):
                raise ValidationError(_("کلید فنی جزء فرم معتبر نیست."))

    @api.constrains("parent_id", "version_id")
    def _check_parent_version(self):
        if self._has_cycle():
            raise ValidationError(_("ساختار فرم نمی‌تواند دارای حلقه باشد."))
        for record in self:
            if record.parent_id and record.parent_id.version_id != record.version_id:
                raise ValidationError(_("والد و فرزند باید متعلق به یک نسخه باشند."))

    @api.constrains("node_type", "field_id", "version_id")
    def _check_field_node(self):
        for record in self:
            if record.node_type == "field" and not record.field_id:
                raise ValidationError(_("برای جزء از نوع فیلد باید یک فیلد انتخاب شود."))
            if record.node_type != "field" and record.field_id:
                raise ValidationError(_("فیلد فقط برای جزء از نوع فیلد قابل تعیین است."))
            if record.field_id and record.field_id.version_id != record.version_id:
                raise ValidationError(_("جزء نمایشی و فیلد باید متعلق به یک نسخه باشند."))
