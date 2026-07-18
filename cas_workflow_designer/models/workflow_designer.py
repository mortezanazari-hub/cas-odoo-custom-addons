import re

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


TECHNICAL_KEY_RE = re.compile(r"^[a-z][a-z0-9_]*$")
NODE_KINDS = {"initial", "normal", "final", "cancelled"}
RESPONSIBLE_MODES = {"keep", "actor"}


class CasWorkflowDefinitionFormBinding(models.Model):
    _inherit = "cas.workflow.definition"

    form_definition_id = fields.Many2one(
        "cas.form.definition",
        string="فرم متصل",
        ondelete="restrict",
        domain="[('company_id', '=', company_id)]",
        help="در صورت انتخاب، گردش‌کار فقط برای ثبت ارسال‌شده همین فرم آغاز می‌شود.",
    )

    @api.constrains("form_definition_id", "target_model_id")
    def _check_form_target_model(self):
        for definition in self:
            if definition.form_definition_id and definition.target_model_id.model != "cas.form.submission":
                raise ValidationError(_("مدل مقصد گردش‌کار متصل به فرم باید «ثبت فرم» باشد."))

    def write(self, vals):
        if "form_definition_id" in vals:
            locked = self.filtered(
                lambda item: any(version.state in {"published", "archived"} for version in item.version_ids)
            )
            if locked:
                raise ValidationError(_("فرم متصل پس از اولین انتشار گردش‌کار قابل تغییر نیست."))
        return super().write(vals)

    def action_start(self, resource_id, responsible_user_id=False):
        self.ensure_one()
        if self.form_definition_id:
            submission = self.env["cas.form.submission"].browse(int(resource_id)).exists()
            if not submission or submission.definition_id != self.form_definition_id:
                raise ValidationError(_("ثبت انتخاب‌شده متعلق به فرم متصل این گردش‌کار نیست."))
            submission.check_access("read")
            if submission.state != "submitted":
                raise ValidationError(_("گردش‌کار فقط برای فرم ارسال‌شده قابل آغاز است."))
        return super().action_start(resource_id, responsible_user_id=responsible_user_id)

    def action_start_submission(self, submission_id, responsible_user_id):
        self.ensure_one()
        if not self.form_definition_id:
            raise ValidationError(_("این گردش‌کار به فرم متصل نشده است."))
        if not responsible_user_id:
            raise ValidationError(_("تعیین مسئول فعال برای آغاز گردش‌کار الزامی است."))
        return self.action_start(submission_id, responsible_user_id=responsible_user_id)


class CasWorkflowVersionNodeDesigner(models.Model):
    _inherit = "cas.workflow.version"

    designer_revision = fields.Integer(default=0, readonly=True, copy=False)

    def _require_designer(self):
        if not (
            self.env.is_superuser()
            or self.env.user.has_group("cas_workflow_core.group_cas_workflow_designer")
        ):
            raise AccessError(_("مجوز طراحی گردش‌کار را ندارید."))

    def action_open_node_designer(self):
        self.ensure_one()
        self._require_designer()
        return {
            "type": "ir.actions.client",
            "tag": "cas_workflow_designer.node_designer",
            "name": _("طراح نودبیس گردش‌کار"),
            "context": {"active_id": self.id, "active_model": self._name},
        }

    def designer_get_graph(self):
        self.ensure_one()
        self.check_access("read")
        self._require_designer()
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "revision": self.designer_revision,
            "form_name": self.definition_id.form_definition_id.name or "",
            "nodes": [
                {
                    "key": state.code,
                    "name": state.name,
                    "kind": state.kind,
                    "x": state.designer_x,
                    "y": state.designer_y,
                    "color": state.designer_color,
                    "sla_hours": state.sla_hours,
                    "fold": state.fold,
                }
                for state in self.state_ids.sorted(key=lambda item: (item.sequence, item.id))
            ],
            "edges": [
                {
                    "key": transition.code,
                    "name": transition.name,
                    "from": transition.from_state_id.code,
                    "to": transition.to_state_id.code,
                    "responsible_mode": transition.responsible_mode,
                    "note_required": transition.note_required,
                }
                for transition in self.transition_ids.sorted(key=lambda item: (item.sequence, item.id))
            ],
        }

    def _validate_graph_payload(self, payload):
        if not isinstance(payload, dict):
            raise ValidationError(_("ساختار گراف معتبر نیست."))
        nodes = payload.get("nodes") or []
        edges = payload.get("edges") or []
        if not isinstance(nodes, list) or not isinstance(edges, list):
            raise ValidationError(_("نودها و اتصال‌ها باید فهرست باشند."))
        if not 2 <= len(nodes) <= 150 or len(edges) > 300:
            raise ValidationError(_("گراف باید ۲ تا ۱۵۰ نود و حداکثر ۳۰۰ اتصال داشته باشد."))

        node_keys = []
        for node in nodes:
            key = str(node.get("key") or "").strip().lower()
            name = str(node.get("name") or "").strip()
            kind = node.get("kind") or "normal"
            if not TECHNICAL_KEY_RE.fullmatch(key) or not name or kind not in NODE_KINDS:
                raise ValidationError(_("کلید، عنوان یا نوع یکی از نودها معتبر نیست."))
            try:
                x, y = int(node.get("x") or 0), int(node.get("y") or 0)
                sla = float(node.get("sla_hours") or 0)
            except (TypeError, ValueError):
                raise ValidationError(_("مختصات یا مهلت یکی از نودها معتبر نیست."))
            if not 0 <= x <= 5000 or not 0 <= y <= 5000 or sla < 0:
                raise ValidationError(_("مختصات یا مهلت یکی از نودها خارج از محدوده امن است."))
            node.update({"key": key, "name": name, "kind": kind, "x": x, "y": y, "sla_hours": sla})
            node_keys.append(key)
        if len(node_keys) != len(set(node_keys)):
            raise ValidationError(_("کلید نودها باید یکتا باشد."))
        if sum(node.get("kind") == "initial" for node in nodes) != 1:
            raise ValidationError(_("گراف باید دقیقاً یک نود آغازین داشته باشد."))
        if not any(node.get("kind") in {"final", "cancelled"} for node in nodes):
            raise ValidationError(_("گراف باید حداقل یک نود پایانی یا لغوشده داشته باشد."))

        edge_keys = []
        known = set(node_keys)
        for edge in edges:
            key = str(edge.get("key") or "").strip().lower()
            name = str(edge.get("name") or "").strip()
            source, target = edge.get("from"), edge.get("to")
            mode = edge.get("responsible_mode") or "keep"
            if not TECHNICAL_KEY_RE.fullmatch(key) or not name or mode not in RESPONSIBLE_MODES:
                raise ValidationError(_("کلید، عنوان یا نحوه مسئولیت یکی از اتصال‌ها معتبر نیست."))
            if source not in known or target not in known or source == target:
                raise ValidationError(_("مبدأ یا مقصد یکی از اتصال‌ها معتبر نیست."))
            edge.update({"key": key, "name": name, "responsible_mode": mode})
            edge_keys.append(key)
        if len(edge_keys) != len(set(edge_keys)):
            raise ValidationError(_("کلید اتصال‌ها باید یکتا باشد."))
        if not edges:
            raise ValidationError(_("گراف باید حداقل یک اتصال داشته باشد."))

        initial = next(node["key"] for node in nodes if node["kind"] == "initial")
        reached, pending = {initial}, [initial]
        adjacency = {}
        for edge in edges:
            adjacency.setdefault(edge["from"], []).append(edge["to"])
        while pending:
            for target in adjacency.get(pending.pop(), []):
                if target not in reached:
                    reached.add(target)
                    pending.append(target)
        missing = known - reached
        if missing:
            raise ValidationError(_("همه نودها باید از نود آغازین قابل دسترسی باشند: %s", "، ".join(sorted(missing))))
        return nodes, edges

    def designer_save_graph(self, payload, expected_revision):
        self.ensure_one()
        self.check_access("write")
        self._require_designer()
        self.env.cr.execute(
            "SELECT designer_revision FROM cas_workflow_version WHERE id = %s FOR UPDATE",
            [self.id],
        )
        current_revision = self.env.cr.fetchone()[0]
        if current_revision != int(expected_revision):
            raise ValidationError(_("گراف توسط کاربر دیگری تغییر کرده است؛ صفحه را تازه‌سازی کنید."))
        self.invalidate_recordset(["designer_revision", "state"])
        if self.state != "draft":
            raise ValidationError(_("نسخه منتشرشده یا بایگانی‌شده فقط قابل مشاهده است."))
        nodes, edges = self._validate_graph_payload(payload)

        existing_edges = {item.code: item for item in self.transition_ids}
        incoming_edge_keys = {item["key"] for item in edges}
        (self.transition_ids - self.transition_ids.filtered(lambda item: item.code in incoming_edge_keys)).unlink()

        existing_nodes = {item.code: item for item in self.state_ids}
        state_by_key = {}
        for sequence, node in enumerate(nodes, 1):
            values = {
                "sequence": sequence * 10,
                "name": node["name"],
                "code": node["key"],
                "kind": node["kind"],
                "sla_hours": node["sla_hours"],
                "fold": bool(node.get("fold")),
                "designer_x": node["x"],
                "designer_y": node["y"],
                "designer_color": str(node.get("color") or "blue")[:20],
            }
            record = existing_nodes.get(node["key"])
            if record:
                record.write(values)
            else:
                record = self.env["cas.workflow.state"].create({"version_id": self.id, **values})
            state_by_key[node["key"]] = record

        for sequence, edge in enumerate(edges, 1):
            values = {
                "sequence": sequence * 10,
                "name": edge["name"],
                "code": edge["key"],
                "from_state_id": state_by_key[edge["from"]].id,
                "to_state_id": state_by_key[edge["to"]].id,
                "responsible_mode": edge["responsible_mode"],
                "note_required": bool(edge.get("note_required")),
                "condition_config": {"type": "always"},
            }
            record = existing_edges.get(edge["key"])
            if record:
                record.write(values)
            else:
                self.env["cas.workflow.transition"].create({"version_id": self.id, **values})

        incoming_node_keys = set(state_by_key)
        obsolete = self.state_ids.filtered(lambda item: item.code not in incoming_node_keys)
        if obsolete:
            obsolete.unlink()
        super(CasWorkflowVersionNodeDesigner, self).write({"designer_revision": current_revision + 1})
        return self.designer_get_graph()


class CasWorkflowStateVisualPosition(models.Model):
    _inherit = "cas.workflow.state"

    designer_x = fields.Integer(default=80)
    designer_y = fields.Integer(default=80)
    designer_color = fields.Char(default="blue")
