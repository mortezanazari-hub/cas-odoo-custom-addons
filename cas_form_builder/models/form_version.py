import re

from odoo import _, fields, models
from odoo.exceptions import AccessError, ValidationError


TECHNICAL_KEY_RE = re.compile(r"^[a-z][a-z0-9_]*$")
FIELD_TYPES = {
    "short_text", "long_text", "rich_text", "integer", "decimal", "percentage", "monetary",
    "boolean", "single_select", "multi_select", "radio", "dropdown", "tag", "date", "datetime",
    "time", "file", "image", "user", "employee", "department", "company", "record_reference",
    "computed", "display",
}
OPTION_TYPES = {"single_select", "multi_select", "radio", "dropdown", "tag"}


class CasFormVersionVisualBuilder(models.Model):
    _inherit = "cas.form.version"

    designer_revision = fields.Integer(default=0, readonly=True, copy=False)

    def _require_designer(self):
        if not (self.env.is_superuser() or self.env.user.has_group("cas_form_core.group_cas_form_designer")):
            raise AccessError(_("مجوز طراحی فرم را ندارید."))

    def action_open_visual_designer(self):
        self.ensure_one()
        self._require_designer()
        return {
            "type": "ir.actions.client",
            "tag": "cas_form_builder.visual_designer",
            "name": _("طراح بصری فرم"),
            "context": {"active_id": self.id, "active_model": self._name},
        }

    def designer_get_schema(self):
        self.ensure_one()
        self.check_access("read")
        self._require_designer()
        roots = self.node_ids.filtered(lambda node: not node.parent_id and node.node_type == "section").sorted(
            key=lambda node: (node.sequence, node.id)
        )
        sections = [
            {"key": node.technical_key, "title": node.title or _("بخش"), "columns": node.column_count}
            for node in roots
        ]
        if not sections:
            sections = [{"key": "main", "title": _("اطلاعات اصلی"), "columns": 2}]
        section_keys = {section["key"] for section in sections}
        field_nodes = {
            node.field_id.id: node for node in self.node_ids.filtered(lambda node: node.node_type == "field" and node.field_id)
        }
        payload_fields = []
        for form_field in self.field_ids.sorted(key=lambda item: (item.sequence, item.id)):
            node = field_nodes.get(form_field.id)
            section_key = node.parent_id.technical_key if node and node.parent_id else sections[0]["key"]
            if section_key not in section_keys:
                section_key = sections[0]["key"]
            payload_fields.append({
                "id": form_field.id,
                "key": form_field.technical_key,
                "label": form_field.label,
                "type": form_field.field_type,
                "required": form_field.required,
                "readonly": form_field.readonly,
                "reportable": form_field.reportable,
                "placeholder": form_field.placeholder or "",
                "help_text": form_field.help_text or "",
                "allowed_model": form_field.allowed_model or "",
                "column_span": node.column_span if node else 1,
                "section_key": section_key,
                "options": [
                    {"key": option.technical_key, "label": option.label}
                    for option in form_field.option_ids.sorted(key=lambda item: (item.sequence, item.id))
                    if option.active
                ],
            })
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "revision": self.designer_revision,
            "sections": sections,
            "fields": payload_fields,
        }

    def _validate_designer_payload(self, payload):
        if not isinstance(payload, dict):
            raise ValidationError(_("ساختار طراح فرم معتبر نیست."))
        sections = payload.get("sections") or []
        form_fields = payload.get("fields") or []
        if not isinstance(sections, list) or not isinstance(form_fields, list):
            raise ValidationError(_("بخش‌ها و فیلدهای طراح باید فهرست باشند."))
        if len(sections) > 50 or len(form_fields) > 300:
            raise ValidationError(_("تعداد اجزای فرم از سقف امن بیشتر است."))
        if not sections:
            raise ValidationError(_("فرم باید حداقل یک بخش داشته باشد."))
        section_keys = []
        for section in sections:
            key = str(section.get("key") or "").strip().lower()
            columns = int(section.get("columns") or 1)
            if not TECHNICAL_KEY_RE.fullmatch(key) or not 1 <= columns <= 12:
                raise ValidationError(_("کلید یا تعداد ستون بخش معتبر نیست."))
            section["key"] = key
            section["columns"] = columns
            section_keys.append(key)
        if len(section_keys) != len(set(section_keys)):
            raise ValidationError(_("کلید بخش‌ها باید یکتا باشد."))
        keys = []
        for item in form_fields:
            key = str(item.get("key") or "").strip().lower()
            field_type = item.get("type")
            span = int(item.get("column_span") or 1)
            if not TECHNICAL_KEY_RE.fullmatch(key) or field_type not in FIELD_TYPES:
                raise ValidationError(_("کلید یا نوع یکی از فیلدها معتبر نیست."))
            if item.get("section_key") not in section_keys or not 1 <= span <= 12:
                raise ValidationError(_("محل یا عرض یکی از فیلدها معتبر نیست."))
            if not str(item.get("label") or "").strip():
                raise ValidationError(_("عنوان همه فیلدها الزامی است."))
            options = item.get("options") or []
            if field_type in OPTION_TYPES and not options:
                raise ValidationError(_("فیلد انتخابی «%s» باید گزینه داشته باشد.", item.get("label")))
            if field_type not in OPTION_TYPES and options:
                raise ValidationError(_("گزینه فقط برای فیلدهای انتخابی مجاز است."))
            option_keys = []
            for option in options:
                option_key = str(option.get("key") or "").strip().lower()
                if not TECHNICAL_KEY_RE.fullmatch(option_key) or not str(option.get("label") or "").strip():
                    raise ValidationError(_("کلید یا عنوان گزینه معتبر نیست."))
                option["key"] = option_key
                option_keys.append(option_key)
            if len(option_keys) != len(set(option_keys)):
                raise ValidationError(_("کلید گزینه‌های هر فیلد باید یکتا باشد."))
            item["key"] = key
            item["column_span"] = span
            keys.append(key)
        if len(keys) != len(set(keys)):
            raise ValidationError(_("کلید فنی فیلدها باید یکتا باشد."))
        return sections, form_fields

    def designer_save_schema(self, payload, expected_revision):
        self.ensure_one()
        self.check_access("write")
        self._require_designer()
        if self.state != "draft":
            raise ValidationError(_("فقط نسخه پیش‌نویس در طراح قابل ذخیره است."))
        if int(expected_revision) != self.designer_revision:
            raise ValidationError(_("فرم توسط کاربر دیگری تغییر کرده است؛ صفحه را تازه‌سازی کنید."))
        sections, items = self._validate_designer_payload(payload)
        existing = {record.id: record for record in self.field_ids}
        requested_ids = {int(item["id"]) for item in items if item.get("id")}
        if requested_ids - set(existing):
            raise ValidationError(_("یکی از فیلدهای ارسالی متعلق به این نسخه نیست."))
        self.node_ids.unlink()
        kept = self.env["cas.form.field"]
        field_by_key = {}
        for index, item in enumerate(items, 1):
            values = {
                "sequence": index * 10,
                "technical_key": item["key"],
                "label": str(item["label"]).strip(),
                "field_type": item["type"],
                "required": bool(item.get("required")),
                "readonly": bool(item.get("readonly")),
                "reportable": bool(item.get("reportable", True)),
                "placeholder": item.get("placeholder") or False,
                "help_text": item.get("help_text") or False,
                "allowed_model": item.get("allowed_model") or False,
            }
            record = existing.get(int(item.get("id") or 0))
            if record:
                record.write(values)
            else:
                record = self.env["cas.form.field"].create({"version_id": self.id, **values})
            record.option_ids.unlink()
            for option_index, option in enumerate(item.get("options") or [], 1):
                self.env["cas.form.field.option"].create({
                    "field_id": record.id, "sequence": option_index * 10,
                    "technical_key": option["key"], "label": str(option["label"]).strip(),
                })
            kept |= record
            field_by_key[item["key"]] = record
        (self.field_ids - kept).unlink()
        section_nodes = {}
        for index, section in enumerate(sections, 1):
            section_nodes[section["key"]] = self.env["cas.form.node"].create({
                "version_id": self.id, "sequence": index * 1000, "technical_key": section["key"],
                "node_type": "section", "title": str(section.get("title") or _("بخش")).strip(),
                "column_count": section["columns"], "column_span": 12,
            })
        for index, item in enumerate(items, 1):
            self.env["cas.form.node"].create({
                "version_id": self.id, "sequence": index * 10, "technical_key": f"field_{item['key']}",
                "node_type": "field", "parent_id": section_nodes[item["section_key"]].id,
                "field_id": field_by_key[item["key"]].id, "column_count": 1,
                "column_span": item["column_span"],
            })
        self.write({"designer_revision": self.designer_revision + 1})
        return self.designer_get_schema()
