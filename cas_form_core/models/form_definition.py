"""Stable identities for versioned CAS forms."""

from __future__ import annotations

import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


TECHNICAL_CODE_RE = re.compile(r"^[a-z][a-z0-9_]*$")


class CasFormDefinition(models.Model):
    _name = "cas.form.definition"
    _description = "CAS Form Definition"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name, id"

    name = fields.Char(string="عنوان فرم", required=True, tracking=True)
    code = fields.Char(
        string="کد فنی",
        required=True,
        index=True,
        copy=False,
        tracking=True,
        help="کلید پایدار فرم؛ پس از اولین انتشار قابل تغییر نیست.",
    )
    description = fields.Text(string="توضیحات")
    company_id = fields.Many2one(
        "res.company",
        string="شرکت",
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )
    owner_user_id = fields.Many2one(
        "res.users",
        string="مالک فرایند",
        default=lambda self: self.env.user,
        tracking=True,
    )
    version_ids = fields.One2many(
        "cas.form.version",
        "definition_id",
        string="نسخه‌ها",
    )
    current_version_id = fields.Many2one(
        "cas.form.version",
        string="نسخه فعال",
        copy=False,
        readonly=True,
        tracking=True,
        domain="[('definition_id', '=', id), ('state', '=', 'published')]",
    )
    active = fields.Boolean(default=True, tracking=True)

    _code_company_uniq = models.Constraint(
        "UNIQUE(code, company_id)",
        "کد فنی فرم باید در هر شرکت یکتا باشد.",
    )

    @api.constrains("code")
    def _check_code(self):
        for record in self:
            if record.code and not TECHNICAL_CODE_RE.fullmatch(record.code):
                raise ValidationError(
                    _(
                        "کد فنی باید با حرف انگلیسی کوچک شروع شود و فقط شامل "
                        "حروف انگلیسی کوچک، عدد و زیرخط باشد."
                    )
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code"):
                vals["code"] = vals["code"].strip().lower()
        return super().create(vals_list)

    def write(self, vals):
        if "code" in vals:
            vals["code"] = (vals["code"] or "").strip().lower()
        if {"code", "company_id"}.intersection(vals):
            locked = self.filtered(
                lambda definition: any(
                    version.state in {"published", "archived"}
                    for version in definition.version_ids
                )
            )
            if locked:
                raise ValidationError(
                    _("کد فنی و شرکت فرم پس از اولین انتشار قابل تغییر نیستند.")
                )
        return super().write(vals)

    def unlink(self):
        locked = self.filtered(
            lambda definition: any(
                version.state in {"published", "archived"}
                for version in definition.version_ids
            )
        )
        if locked:
            raise ValidationError(
                _("فرمی که سابقه انتشار دارد قابل حذف نیست؛ آن را بایگانی کنید.")
            )
        return super().unlink()

    def action_create_initial_version(self):
        self.ensure_one()
        if self.version_ids:
            raise ValidationError(_("این فرم از قبل دارای نسخه است."))
        version = self.env["cas.form.version"].create(
            {
                "definition_id": self.id,
                "revision": 1,
                "name": _("نسخه ۱"),
            }
        )
        return {
            "type": "ir.actions.act_window",
            "res_model": "cas.form.version",
            "res_id": version.id,
            "view_mode": "form",
            "target": "current",
        }
