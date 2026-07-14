"""Immutable revisions for CAS form definitions."""

from __future__ import annotations

import hashlib
import json

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CasFormVersion(models.Model):
    _name = "cas.form.version"
    _description = "CAS Form Version"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "definition_id, revision desc, id desc"

    definition_id = fields.Many2one(
        "cas.form.definition",
        string="فرم",
        required=True,
        ondelete="cascade",
        index=True,
    )
    company_id = fields.Many2one(
        related="definition_id.company_id",
        store=True,
        index=True,
    )
    name = fields.Char(string="عنوان نسخه", required=True)
    revision = fields.Integer(string="شماره بازنگری", required=True, default=1)
    state = fields.Selection(
        [
            ("draft", "پیش‌نویس"),
            ("published", "منتشرشده"),
            ("archived", "بایگانی‌شده"),
        ],
        string="وضعیت",
        required=True,
        default="draft",
        index=True,
        tracking=True,
        copy=False,
    )
    notes = fields.Text(string="یادداشت بازنگری")
    effective_from = fields.Datetime(string="شروع اعتبار")
    published_at = fields.Datetime(string="زمان انتشار", readonly=True, copy=False)
    published_by_id = fields.Many2one(
        "res.users",
        string="منتشرکننده",
        readonly=True,
        copy=False,
    )
    schema_hash = fields.Char(
        string="اثر انگشت ساختار",
        readonly=True,
        copy=False,
        index=True,
    )
    field_ids = fields.One2many(
        "cas.form.field",
        "version_id",
        string="فیلدها",
        copy=False,
    )
    node_ids = fields.One2many(
        "cas.form.node",
        "version_id",
        string="ساختار فرم",
        copy=False,
    )

    _revision_uniq = models.Constraint(
        "UNIQUE(definition_id, revision)",
        "شماره بازنگری باید برای هر فرم یکتا باشد.",
    )
    _revision_positive = models.Constraint(
        "CHECK(revision > 0)",
        "شماره بازنگری باید بزرگ‌تر از صفر باشد.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.setdefault("state", "draft")
            if vals["state"] != "draft":
                raise ValidationError(_("نسخه جدید باید ابتدا به‌صورت پیش‌نویس ایجاد شود."))
        return super().create(vals_list)

    def write(self, vals):
        immutable = self.filtered(lambda version: version.state != "draft")
        if immutable:
            raise ValidationError(
                _("نسخه منتشرشده یا بایگانی‌شده قابل ویرایش نیست.")
            )
        if "state" in vals and vals["state"] != "draft":
            raise ValidationError(
                _("تغییر وضعیت نسخه فقط از طریق عملیات انتشار مجاز است.")
            )
        return super().write(vals)

    def unlink(self):
        if any(version.state != "draft" for version in self):
            raise ValidationError(
                _("نسخه منتشرشده یا بایگانی‌شده قابل حذف نیست.")
            )
        return super().unlink()

    def _check_publish_access(self):
        if self.env.is_superuser():
            return
        if not self.env.user.has_group("cas_form_core.group_cas_form_publisher"):
            raise AccessError(_("شما مجوز انتشار فرم را ندارید."))

    def _schema_payload(self):
        self.ensure_one()
        fields_payload = []
        for field in self.field_ids.sorted(key=lambda item: (item.sequence, item.id)):
            fields_payload.append(
                {
                    "uuid": field.field_uuid,
                    "key": field.technical_key,
                    "label": field.label,
                    "type": field.field_type,
                    "required": field.required,
                    "readonly": field.readonly,
                    "reportable": field.reportable,
                    "config": field.validation_config or {},
                    "options": [
                        {
                            "key": option.technical_key,
                            "label": option.label,
                            "sequence": option.sequence,
                        }
                        for option in field.option_ids.sorted(
                            key=lambda item: (item.sequence, item.id)
                        )
                    ],
                }
            )
        nodes_payload = []
        for node in self.node_ids.sorted(key=lambda item: (item.sequence, item.id)):
            nodes_payload.append(
                {
                    "key": node.technical_key,
                    "type": node.node_type,
                    "parent": node.parent_id.technical_key or None,
                    "field": node.field_id.field_uuid or None,
                    "sequence": node.sequence,
                    "columns": node.column_count,
                    "span": node.column_span,
                }
            )
        return {
            "form": self.definition_id.code,
            "revision": self.revision,
            "fields": fields_payload,
            "nodes": nodes_payload,
        }

    def _compute_schema_hash(self):
        self.ensure_one()
        serialized = json.dumps(
            self._schema_payload(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def _validate_publishable(self):
        self.ensure_one()
        if self.state != "draft":
            raise ValidationError(_("فقط نسخه پیش‌نویس قابل انتشار است."))
        if not self.field_ids:
            raise ValidationError(_("فرم باید حداقل یک فیلد داشته باشد."))
        if not self.node_ids.filtered(lambda node: node.node_type == "field"):
            raise ValidationError(
                _("حداقل یک فیلد باید در ساختار نمایشی فرم قرار گرفته باشد.")
            )
        unplaced = self.field_ids.filtered(
            lambda field: not self.node_ids.filtered(
                lambda node: node.node_type == "field" and node.field_id == field
            )
        )
        if unplaced:
            raise ValidationError(
                _(
                    "فیلدهای زیر در ساختار فرم قرار نگرفته‌اند: %s",
                    "، ".join(unplaced.mapped("label")),
                )
            )
        for field in self.field_ids:
            field._validate_definition()

    def action_publish(self):
        self.ensure_one()
        self._check_publish_access()
        self._validate_publishable()

        previous = self.definition_id.current_version_id
        if previous and previous != self:
            super(CasFormVersion, previous).write({"state": "archived"})

        values = {
            "state": "published",
            "published_at": fields.Datetime.now(),
            "published_by_id": self.env.user.id,
            "schema_hash": self._compute_schema_hash(),
        }
        super(CasFormVersion, self).write(values)
        self.definition_id.write({"current_version_id": self.id})
        return True

    def action_archive(self):
        self.ensure_one()
        self._check_publish_access()
        if self.state != "published":
            raise ValidationError(_("فقط نسخه منتشرشده قابل بایگانی است."))
        super(CasFormVersion, self).write({"state": "archived"})
        if self.definition_id.current_version_id == self:
            self.definition_id.write({"current_version_id": False})
        return True

    def action_new_revision(self):
        self.ensure_one()
        next_revision = max(self.definition_id.version_ids.mapped("revision") or [0]) + 1
        clone = self.create(
            {
                "definition_id": self.definition_id.id,
                "revision": next_revision,
                "name": _("نسخه %s", next_revision),
                "notes": self.notes,
            }
        )

        field_map = {}
        for source_field in self.field_ids.sorted(key=lambda item: (item.sequence, item.id)):
            new_field = source_field.copy({"version_id": clone.id})
            field_map[source_field.id] = new_field.id

        def clone_node(source_node, new_parent=False):
            values = {
                "version_id": clone.id,
                "parent_id": new_parent.id if new_parent else False,
                "field_id": field_map.get(source_node.field_id.id),
            }
            new_node = source_node.copy(values)
            for child in source_node.child_ids.sorted(
                key=lambda item: (item.sequence, item.id)
            ):
                clone_node(child, new_node)

        roots = self.node_ids.filtered(lambda node: not node.parent_id)
        for root in roots.sorted(key=lambda item: (item.sequence, item.id)):
            clone_node(root)

        return {
            "type": "ir.actions.act_window",
            "res_model": "cas.form.version",
            "res_id": clone.id,
            "view_mode": "form",
            "target": "current",
        }
