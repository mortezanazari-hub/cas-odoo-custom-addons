"""Secure backend API for the CAS dynamic form OWL runtime."""

from __future__ import annotations

from odoo import _, api, models
from odoo.exceptions import AccessError, ValidationError


REFERENCE_TYPE_MODELS = {
    "user": "res.users",
    "employee": "hr.employee",
    "department": "hr.department",
    "company": "res.company",
}


class CasFormDefinitionRuntime(models.Model):
    _inherit = "cas.form.definition"

    def _runtime_action(self, submission_id=False):
        self.ensure_one()
        return {
            "type": "ir.actions.client",
            "name": self.name,
            "tag": "cas_dynamic_form.Runtime",
            "params": {
                "definition_id": self.id,
                "submission_id": submission_id or False,
            },
        }

    def action_open_dynamic_runtime(self):
        self.ensure_one()
        self.check_access("read")
        if (
            not self.active
            or not self.current_version_id
            or self.current_version_id.state != "published"
        ):
            raise ValidationError(_("این فرم نسخه فعال و منتشرشده ندارد."))
        return self._runtime_action()

    def runtime_start_submission(self):
        """Create a draft owned by the caller and return its runtime payload."""
        self.ensure_one()
        self.check_access("read")
        if (
            not self.active
            or not self.current_version_id
            or self.current_version_id.state != "published"
        ):
            raise ValidationError(_("امکان ثبت این فرم در حال حاضر وجود ندارد."))
        submission = self.env["cas.form.submission"].create(
            {
                "version_id": self.current_version_id.id,
                "owner_user_id": self.env.user.id,
            }
        )
        return submission.runtime_load()

    @api.model
    def runtime_catalog(self):
        if not self.env.user.has_group("cas_form_core.group_cas_form_user"):
            raise AccessError(_("شما مجوز استفاده از فرم‌های سازمانی را ندارید."))

        definitions = self.search(
            [
                ("active", "=", True),
                ("current_version_id", "!=", False),
                ("current_version_id.state", "=", "published"),
            ],
            order="name, id",
        )
        drafts = self.env["cas.form.submission"].search(
            [
                ("owner_user_id", "=", self.env.user.id),
                ("state", "=", "draft"),
            ],
            order="write_date desc, id desc",
            limit=50,
        )
        recent = self.env["cas.form.submission"].search(
            [
                ("owner_user_id", "=", self.env.user.id),
                ("state", "=", "submitted"),
            ],
            order="submitted_at desc, id desc",
            limit=10,
        )

        return {
            "forms": [
                {
                    "id": definition.id,
                    "name": definition.name,
                    "code": definition.code,
                    "description": definition.description or "",
                    "revision": definition.current_version_id.revision,
                }
                for definition in definitions
            ],
            "drafts": [submission._runtime_summary() for submission in drafts],
            "recent": [submission._runtime_summary() for submission in recent],
        }


class CasFormVersionRuntime(models.Model):
    _inherit = "cas.form.version"

    def _runtime_field_payload(self, form_field):
        return {
            "id": form_field.id,
            "uuid": form_field.field_uuid,
            "key": form_field.technical_key,
            "label": form_field.label,
            "type": form_field.field_type,
            "required": form_field.required,
            "readonly": form_field.readonly,
            "placeholder": form_field.placeholder or "",
            "help_text": form_field.help_text or "",
            "default": form_field.default_value,
            "validation": form_field.validation_config or {},
            "allowed_model": form_field.allowed_model or False,
            "options": [
                {
                    "key": option.technical_key,
                    "label": option.label,
                }
                for option in form_field.option_ids.filtered("active").sorted(
                    key=lambda item: (item.sequence, item.id)
                )
            ],
        }

    def _runtime_layout_payload(self):
        self.ensure_one()
        children_by_parent = {}
        for node in self.node_ids.sorted(key=lambda item: (item.sequence, item.id)):
            children_by_parent.setdefault(node.parent_id.id or False, []).append(node)

        def serialize(node):
            return {
                "key": node.technical_key,
                "type": node.node_type,
                "title": node.title or "",
                "help_text": node.help_text or "",
                "columns": node.column_count,
                "span": node.column_span,
                "field_uuid": node.field_id.field_uuid or False,
                "children": [
                    serialize(child) for child in children_by_parent.get(node.id, [])
                ],
            }

        return [serialize(node) for node in children_by_parent.get(False, [])]

    def runtime_schema(self):
        self.ensure_one()
        self.check_access("read")
        if self.state not in {"published", "archived"}:
            raise ValidationError(_("نسخه پیش‌نویس قابل اجرا نیست."))
        return {
            "definition_id": self.definition_id.id,
            "form_name": self.definition_id.name,
            "form_code": self.definition_id.code,
            "description": self.definition_id.description or "",
            "version_id": self.id,
            "revision": self.revision,
            "schema_hash": self.schema_hash,
            "fields": [
                self._runtime_field_payload(form_field)
                for form_field in self.field_ids.sorted(
                    key=lambda item: (item.sequence, item.id)
                )
            ],
            "layout": self._runtime_layout_payload(),
        }


class CasFormSubmissionRuntime(models.Model):
    _inherit = "cas.form.submission"

    def _runtime_summary(self):
        self.ensure_one()
        return {
            "id": self.id,
            "number": self.number,
            "form_name": self.definition_id.name,
            "form_code": self.definition_id.code,
            "revision": self.version_id.revision,
            "state": self.state,
            "write_date": self.write_date,
            "submitted_at": self.submitted_at,
        }

    def action_open_dynamic_runtime(self):
        self.ensure_one()
        self.check_access("read")
        return self.definition_id._runtime_action(submission_id=self.id)

    def _runtime_answers(self):
        self.ensure_one()
        answers = self.action_get_answers()
        field_types = {
            form_field.technical_key: form_field.field_type
            for form_field in self.version_id.field_ids
        }
        for key, value in list(answers.items()):
            if field_types.get(key) == "time" and isinstance(value, int):
                hours, remainder = divmod(value, 3600)
                minutes, seconds = divmod(remainder, 60)
                answers[key] = (
                    f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                    if seconds
                    else f"{hours:02d}:{minutes:02d}"
                )
        return answers

    def runtime_load(self):
        self.ensure_one()
        self.check_access("read")
        return {
            "submission": self._runtime_summary(),
            "schema": self.version_id.runtime_schema(),
            "answers": self._runtime_answers(),
        }

    def runtime_save(self, values):
        self.ensure_one()
        self.action_save_answers(values)
        return self.runtime_load()

    def runtime_submit(self, values):
        self.ensure_one()
        self.action_submit(values)
        return self.runtime_load()


class CasFormFieldRuntime(models.Model):
    _inherit = "cas.form.field"

    def runtime_reference_options(self, query="", limit=50):
        """Return a bounded name-search result under the caller's real ACLs."""
        self.ensure_one()
        self.check_access("read")
        if self.field_type not in {
            "user",
            "employee",
            "department",
            "company",
            "record_reference",
        }:
            raise ValidationError(_("این فیلد از نوع رکورد مرتبط نیست."))

        model_name = REFERENCE_TYPE_MODELS.get(self.field_type) or self.allowed_model
        if (
            self.field_type == "record_reference"
            and model_name not in self._get_allowed_reference_models()
        ):
            raise AccessError(_("مدل مرتبط در فهرست مجاز قرار ندارد."))
        if not model_name or model_name not in self.env.registry:
            return []

        domain = []
        if self.field_type == "company":
            domain = [("id", "in", self.env.companies.ids)]
        safe_limit = min(max(int(limit or 50), 1), 100)
        return [
            {"id": record_id, "name": display_name}
            for record_id, display_name in self.env[model_name].name_search(
                name=str(query or "").strip(),
                domain=domain,
                operator="ilike",
                limit=safe_limit,
            )
        ]
