"""Versioned workflow schema models."""

from __future__ import annotations

import hashlib
import json
import re

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


TECHNICAL_CODE_RE = re.compile(r"^[a-z][a-z0-9_]*$")


class CasWorkflowDefinition(models.Model):
    _name = "cas.workflow.definition"
    _description = "CAS Workflow Definition"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name, id"

    name = fields.Char(string="عنوان گردش‌کار", required=True, tracking=True)
    code = fields.Char(string="کد فنی", required=True, index=True, copy=False)
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
    target_model_id = fields.Many2one(
        "ir.model",
        string="مدل مقصد",
        required=True,
        ondelete="cascade",
        domain="[('transient', '=', False)]",
        help="نمونه‌های این گردش‌کار فقط به رکوردهای این مدل متصل می‌شوند.",
    )
    version_ids = fields.One2many(
        "cas.workflow.version", "definition_id", string="نسخه‌ها"
    )
    current_version_id = fields.Many2one(
        "cas.workflow.version",
        string="نسخه فعال",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )
    active = fields.Boolean(default=True, tracking=True)

    _code_company_uniq = models.Constraint(
        "UNIQUE(code, company_id)",
        "کد فنی گردش‌کار باید در هر شرکت یکتا باشد.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code"):
                vals["code"] = vals["code"].strip().lower()
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("code"):
            vals["code"] = vals["code"].strip().lower()
        if {"code", "company_id", "target_model_id"}.intersection(vals):
            locked = self.filtered(
                lambda item: any(
                    version.state in {"published", "archived"}
                    for version in item.version_ids
                )
            )
            if locked:
                raise ValidationError(
                    _("کد، شرکت و مدل مقصد پس از اولین انتشار قابل تغییر نیستند.")
                )
        return super().write(vals)

    def unlink(self):
        if any(
            version.state in {"published", "archived"}
            for definition in self
            for version in definition.version_ids
        ):
            raise ValidationError(
                _("گردش‌کاری که سابقه انتشار دارد قابل حذف نیست؛ آن را غیرفعال کنید.")
            )
        return super().unlink()

    @api.constrains("code")
    def _check_code(self):
        for record in self:
            if record.code and not TECHNICAL_CODE_RE.fullmatch(record.code):
                raise ValidationError(_("کد فنی گردش‌کار معتبر نیست."))

    def action_create_initial_version(self):
        self.ensure_one()
        if self.version_ids:
            raise ValidationError(_("این گردش‌کار از قبل دارای نسخه است."))
        version = self.env["cas.workflow.version"].create(
            {"definition_id": self.id, "name": _("نسخه ۱"), "revision": 1}
        )
        return {
            "type": "ir.actions.act_window",
            "res_model": "cas.workflow.version",
            "res_id": version.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_start(self, resource_id, responsible_user_id=False):
        """Start the published workflow for one existing target record."""
        self.ensure_one()
        self.check_access("read")
        version = self.current_version_id
        if not version or version.state != "published":
            raise ValidationError(_("این گردش‌کار نسخه فعال منتشرشده ندارد."))
        model_name = self.target_model_id.model
        resource = self.env[model_name].browse(int(resource_id)).exists()
        if not resource:
            raise ValidationError(_("رکورد مقصد وجود ندارد یا قابل دسترسی نیست."))
        resource.check_access("read")
        return self.env["cas.workflow.instance"]._start_instance(
            version,
            resource,
            responsible_user_id=responsible_user_id,
        )


class CasWorkflowVersion(models.Model):
    _name = "cas.workflow.version"
    _description = "CAS Workflow Version"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "definition_id, revision desc, id desc"

    definition_id = fields.Many2one(
        "cas.workflow.definition", required=True, ondelete="cascade", index=True
    )
    company_id = fields.Many2one(related="definition_id.company_id", store=True, index=True)
    name = fields.Char(string="عنوان نسخه", required=True)
    revision = fields.Integer(string="بازنگری", required=True, default=1)
    state = fields.Selection(
        [("draft", "پیش‌نویس"), ("published", "منتشرشده"), ("archived", "بایگانی‌شده")],
        default="draft",
        required=True,
        index=True,
        tracking=True,
        copy=False,
        string="وضعیت نسخه",
    )
    notes = fields.Text(string="یادداشت بازنگری")
    published_at = fields.Datetime(readonly=True, copy=False)
    published_by_id = fields.Many2one("res.users", readonly=True, copy=False)
    schema_hash = fields.Char(readonly=True, copy=False, index=True)
    state_ids = fields.One2many(
        "cas.workflow.state",
        "version_id",
        string="وضعیت‌های گردش‌کار",
        copy=False,
    )
    transition_ids = fields.One2many("cas.workflow.transition", "version_id", copy=False)

    _revision_uniq = models.Constraint(
        "UNIQUE(definition_id, revision)", "شماره بازنگری باید یکتا باشد."
    )
    _revision_positive = models.Constraint(
        "CHECK(revision > 0)", "شماره بازنگری باید مثبت باشد."
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.setdefault("state", "draft")
            if vals["state"] != "draft":
                raise ValidationError(_("نسخه جدید باید پیش‌نویس باشد."))
        return super().create(vals_list)

    def write(self, vals):
        if any(record.state != "draft" for record in self):
            raise ValidationError(_("نسخه منتشرشده گردش‌کار قابل ویرایش نیست."))
        if "state" in vals and vals["state"] != "draft":
            raise ValidationError(_("انتشار فقط از عملیات رسمی مجاز است."))
        return super().write(vals)

    def unlink(self):
        if any(record.state != "draft" for record in self):
            raise ValidationError(_("نسخه منتشرشده قابل حذف نیست."))
        return super().unlink()

    def _check_publish_access(self):
        if not (
            self.env.is_superuser()
            or self.env.user.has_group("cas_workflow_core.group_cas_workflow_publisher")
        ):
            raise AccessError(_("مجوز انتشار گردش‌کار را ندارید."))

    def _schema_payload(self):
        self.ensure_one()
        return {
            "workflow": self.definition_id.code,
            "target_model": self.definition_id.target_model_id.model,
            "revision": self.revision,
            "states": [state._schema_payload() for state in self.state_ids.sorted("sequence")],
            "transitions": [
                transition._schema_payload()
                for transition in self.transition_ids.sorted("sequence")
            ],
        }

    def _validate_publishable(self):
        self.ensure_one()
        if self.state != "draft":
            raise ValidationError(_("فقط نسخه پیش‌نویس قابل انتشار است."))
        initial = self.state_ids.filtered(lambda state: state.kind == "initial")
        if len(initial) != 1:
            raise ValidationError(_("گردش‌کار باید دقیقاً یک وضعیت آغازین داشته باشد."))
        if not self.state_ids.filtered(lambda state: state.kind in {"final", "cancelled"}):
            raise ValidationError(_("حداقل یک وضعیت پایانی یا لغوشده لازم است."))
        if not self.transition_ids:
            raise ValidationError(_("گردش‌کار باید حداقل یک انتقال داشته باشد."))
        for transition in self.transition_ids:
            transition._validate_definition()

    def action_publish(self):
        self.ensure_one()
        self._check_publish_access()
        self._validate_publishable()
        payload = self._schema_payload()
        digest = hashlib.sha256(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        previous = self.definition_id.current_version_id
        if previous and previous != self:
            super(CasWorkflowVersion, previous).write({"state": "archived"})
        super().write(
            {
                "state": "published",
                "published_at": fields.Datetime.now(),
                "published_by_id": self.env.user.id,
                "schema_hash": digest,
            }
        )
        self.definition_id.write({"current_version_id": self.id})
        return True

    def action_new_revision(self):
        self.ensure_one()
        next_revision = max(self.definition_id.version_ids.mapped("revision") or [0]) + 1
        clone = self.create(
            {
                "definition_id": self.definition_id.id,
                "name": _("نسخه %s", next_revision),
                "revision": next_revision,
                "notes": self.notes,
            }
        )
        state_map = {}
        for source in self.state_ids.sorted("sequence"):
            new_state = source.copy({"version_id": clone.id})
            state_map[source.id] = new_state.id
        for source in self.transition_ids.sorted("sequence"):
            source.copy(
                {
                    "version_id": clone.id,
                    "from_state_id": state_map[source.from_state_id.id],
                    "to_state_id": state_map[source.to_state_id.id],
                }
            )
        return {
            "type": "ir.actions.act_window",
            "res_model": "cas.workflow.version",
            "res_id": clone.id,
            "view_mode": "form",
            "target": "current",
        }


class CasWorkflowVersionedMixin(models.AbstractModel):
    _name = "cas.workflow.versioned.mixin"
    _description = "CAS Workflow Versioned Mixin"

    version_id = fields.Many2one("cas.workflow.version", required=True, ondelete="cascade", index=True)
    company_id = fields.Many2one(related="version_id.company_id", store=True, index=True)

    @api.model_create_multi
    def create(self, vals_list):
        versions = self.env["cas.workflow.version"].browse(
            {vals.get("version_id") for vals in vals_list if vals.get("version_id")}
        ).exists()
        if any(version.state != "draft" for version in versions):
            raise ValidationError(_("اجزای نسخه منتشرشده قابل تغییر نیستند."))
        return super().create(vals_list)

    def write(self, vals):
        if any(record.version_id.state != "draft" for record in self):
            raise ValidationError(_("اجزای نسخه منتشرشده قابل تغییر نیستند."))
        if "version_id" in vals:
            raise ValidationError(_("انتقال جزء بین نسخه‌ها مجاز نیست."))
        return super().write(vals)

    def unlink(self):
        if any(record.version_id.state != "draft" for record in self):
            raise ValidationError(_("اجزای نسخه منتشرشده قابل حذف نیستند."))
        return super().unlink()


class CasWorkflowState(models.Model):
    _name = "cas.workflow.state"
    _description = "CAS Workflow State"
    _inherit = "cas.workflow.versioned.mixin"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    name = fields.Char(string="عنوان وضعیت", required=True, translate=True)
    code = fields.Char(string="کد فنی", required=True, index=True)
    kind = fields.Selection(
        [("initial", "آغازین"), ("normal", "عادی"), ("final", "پایانی"), ("cancelled", "لغوشده")],
        required=True,
        default="normal",
        index=True,
    )
    sla_hours = fields.Float(string="مهلت مرحله (ساعت)", default=0)
    fold = fields.Boolean(string="جمع‌شده در کانبان")

    _code_version_uniq = models.Constraint(
        "UNIQUE(version_id, code)", "کد وضعیت باید در هر نسخه یکتا باشد."
    )
    _sla_nonnegative = models.Constraint(
        "CHECK(sla_hours >= 0)", "مهلت مرحله نمی‌تواند منفی باشد."
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code"):
                vals["code"] = vals["code"].strip().lower()
        return super().create(vals_list)

    @api.constrains("code")
    def _check_code(self):
        for record in self:
            if record.code and not TECHNICAL_CODE_RE.fullmatch(record.code):
                raise ValidationError(_("کد فنی وضعیت معتبر نیست."))

    def _schema_payload(self):
        self.ensure_one()
        return {
            "code": self.code,
            "name": self.name,
            "kind": self.kind,
            "sequence": self.sequence,
            "sla_hours": self.sla_hours,
        }


class CasWorkflowTransition(models.Model):
    _name = "cas.workflow.transition"
    _description = "CAS Workflow Transition"
    _inherit = "cas.workflow.versioned.mixin"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    name = fields.Char(string="عنوان انتقال", required=True, translate=True)
    code = fields.Char(string="کد فنی", required=True, index=True)
    from_state_id = fields.Many2one("cas.workflow.state", required=True, ondelete="cascade")
    to_state_id = fields.Many2one("cas.workflow.state", required=True, ondelete="cascade")
    allowed_group_ids = fields.Many2many(
        "res.groups",
        "cas_workflow_transition_group_rel",
        "transition_id",
        "group_id",
        string="گروه‌های مجاز",
    )
    responsible_mode = fields.Selection(
        [("keep", "حفظ مسئول جاری"), ("actor", "کاربر اجراکننده")],
        default="keep",
        required=True,
    )
    note_required = fields.Boolean(string="یادداشت اجباری")
    condition_config = fields.Json(string="شرط ساختاریافته", default=dict)

    _code_version_uniq = models.Constraint(
        "UNIQUE(version_id, code)", "کد انتقال باید در هر نسخه یکتا باشد."
    )
    _different_states = models.Constraint(
        "CHECK(from_state_id != to_state_id)", "مبدأ و مقصد انتقال باید متفاوت باشند."
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code"):
                vals["code"] = vals["code"].strip().lower()
        return super().create(vals_list)

    @api.constrains("code")
    def _check_code(self):
        for record in self:
            if record.code and not TECHNICAL_CODE_RE.fullmatch(record.code):
                raise ValidationError(_("کد فنی انتقال معتبر نیست."))

    @api.constrains("from_state_id", "to_state_id", "version_id")
    def _check_state_versions(self):
        for record in self:
            if (
                record.from_state_id.version_id != record.version_id
                or record.to_state_id.version_id != record.version_id
            ):
                raise ValidationError(_("وضعیت‌های انتقال باید متعلق به همان نسخه باشند."))

    def _validate_definition(self):
        self.ensure_one()
        config = self.condition_config or {}
        if not isinstance(config, dict) or set(config) - {"type"}:
            raise ValidationError(_("ساختار شرط انتقال در این نسخه پشتیبانی نمی‌شود."))
        if config.get("type") not in {None, "always"}:
            raise ValidationError(_("در نسخه نخست فقط شرط امن «همیشه» مجاز است."))

    def _schema_payload(self):
        self.ensure_one()
        return {
            "code": self.code,
            "name": self.name,
            "from": self.from_state_id.code,
            "to": self.to_state_id.code,
            "sequence": self.sequence,
            "group_ids": sorted(self.allowed_group_ids.ids),
            "responsible_mode": self.responsible_mode,
            "note_required": self.note_required,
            "condition": self.condition_config or {},
        }
