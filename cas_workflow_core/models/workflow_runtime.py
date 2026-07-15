"""Runtime workflow instance and append-only audit history."""

from __future__ import annotations

from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CasWorkflowInstance(models.Model):
    _name = "cas.workflow.instance"
    _description = "CAS Workflow Instance"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc, id desc"
    _rec_name = "number"

    number = fields.Char(default="New", readonly=True, copy=False, index=True)
    definition_id = fields.Many2one(
        "cas.workflow.definition", required=True, ondelete="restrict", index=True
    )
    version_id = fields.Many2one(
        "cas.workflow.version", required=True, ondelete="restrict", index=True
    )
    company_id = fields.Many2one(related="version_id.company_id", store=True, index=True)
    resource_model = fields.Char(string="مدل رکورد", required=True, readonly=True, index=True)
    resource_id = fields.Integer(string="شناسه رکورد", required=True, readonly=True, index=True)
    resource_display_name = fields.Char(string="عنوان رکورد", required=True, readonly=True)
    current_state_id = fields.Many2one(
        "cas.workflow.state", required=True, ondelete="restrict", index=True, tracking=True
    )
    status = fields.Selection(
        [("running", "در جریان"), ("completed", "تکمیل‌شده"), ("cancelled", "لغوشده")],
        required=True,
        default="running",
        readonly=True,
        index=True,
        tracking=True,
    )
    responsible_user_id = fields.Many2one(
        "res.users", string="مسئول جاری", required=True, index=True, tracking=True
    )
    started_by_id = fields.Many2one("res.users", required=True, readonly=True)
    started_at = fields.Datetime(required=True, readonly=True)
    state_entered_at = fields.Datetime(required=True, readonly=True)
    state_deadline = fields.Datetime(string="مهلت مرحله", readonly=True, index=True)
    completed_at = fields.Datetime(readonly=True)
    history_ids = fields.One2many("cas.workflow.history", "instance_id", copy=False)

    _number_uniq = models.Constraint("UNIQUE(number)", "شماره گردش‌کار باید یکتا باشد.")
    _resource_positive = models.Constraint(
        "CHECK(resource_id > 0)", "شناسه رکورد مقصد باید مثبت باشد."
    )

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.is_superuser():
            raise AccessError(_("نمونه گردش‌کار فقط از عملیات شروع رسمی ساخته می‌شود."))
        return super().create(vals_list)

    def write(self, vals):
        protected = {
            "number",
            "definition_id",
            "version_id",
            "company_id",
            "resource_model",
            "resource_id",
            "resource_display_name",
            "current_state_id",
            "status",
            "responsible_user_id",
            "started_by_id",
            "started_at",
            "state_entered_at",
            "state_deadline",
            "completed_at",
        }
        if protected.intersection(vals):
            raise ValidationError(_("فیلدهای اجرایی فقط از طریق انتقال رسمی تغییر می‌کنند."))
        return super().write(vals)

    def unlink(self):
        raise ValidationError(_("سابقه گردش‌کار قابل حذف نیست."))

    @api.model
    def _deadline_for_state(self, state, entered_at):
        if not state.sla_hours:
            return False
        return entered_at + timedelta(hours=state.sla_hours)

    @api.model
    def _start_instance(self, version, resource, responsible_user_id=False):
        """Private entry point; public callers use definition.action_start()."""
        version.ensure_one()
        resource.ensure_one()
        if version.state != "published" or version.definition_id.current_version_id != version:
            raise ValidationError(_("فقط نسخه فعال منتشرشده قابل اجرا است."))
        expected_model = version.definition_id.target_model_id.model
        if resource._name != expected_model:
            raise ValidationError(_("مدل رکورد با مدل مقصد گردش‌کار یکسان نیست."))
        duplicate = self.sudo().search_count(
            [
                ("definition_id", "=", version.definition_id.id),
                ("resource_model", "=", resource._name),
                ("resource_id", "=", resource.id),
                ("status", "=", "running"),
            ]
        )
        if duplicate:
            raise ValidationError(_("برای این رکورد یک گردش‌کار در جریان وجود دارد."))
        responsible = self.env["res.users"].browse(
            int(responsible_user_id or self.env.user.id)
        ).exists()
        if not responsible or not responsible.active:
            raise ValidationError(_("مسئول جاری معتبر و فعال نیست."))
        delegated_assignment = bool(
            responsible != self.env.user
            and hasattr(resource, "_cas_workflow_authorize_responsible_assignment")
            and resource._cas_workflow_authorize_responsible_assignment(responsible)
        )
        if (
            responsible != self.env.user
            and not self.env.is_superuser()
            and not self.env.user.has_group("cas_workflow_core.group_cas_workflow_manager")
            and not delegated_assignment
        ):
            raise AccessError(_("تعیین مسئول دیگر فقط برای مدیر گردش‌کار مجاز است."))
        if responsible.company_id not in self.env.companies:
            raise AccessError(_("مسئول انتخاب‌شده خارج از شرکت‌های مجاز است."))
        initial = version.state_ids.filtered(lambda state: state.kind == "initial")
        if len(initial) != 1:
            raise ValidationError(_("نسخه گردش‌کار وضعیت آغازین معتبر ندارد."))
        now = fields.Datetime.now()
        instance = self.sudo().create(
            {
                "number": self.env["ir.sequence"].next_by_code("cas.workflow.instance") or "New",
                "definition_id": version.definition_id.id,
                "version_id": version.id,
                "resource_model": resource._name,
                "resource_id": resource.id,
                "resource_display_name": resource.display_name,
                "current_state_id": initial.id,
                "status": "running",
                "responsible_user_id": responsible.id,
                "started_by_id": self.env.user.id,
                "started_at": now,
                "state_entered_at": now,
                "state_deadline": self._deadline_for_state(initial, now),
            }
        )
        self.env["cas.workflow.history"]._append_event(
            instance,
            event_type="started",
            to_state=initial,
            actor=self.env.user,
            note=_("گردش‌کار آغاز شد."),
        )
        instance._sync_responsible_activity()
        return {
            "instance_id": instance.id,
            "number": instance.number,
            "state": initial.code,
            "responsible_user_id": responsible.id,
        }

    def _user_can_execute(self, transition):
        self.ensure_one()
        if self.env.is_superuser() or self.env.user.has_group(
            "cas_workflow_core.group_cas_workflow_manager"
        ):
            return True
        if self.responsible_user_id != self.env.user:
            resource = self.env[self.resource_model].browse(self.resource_id).exists()
            delegated_execution = bool(
                resource
                and hasattr(resource, "_cas_workflow_user_can_execute_transition")
                and resource._cas_workflow_user_can_execute_transition(
                    self, transition, self.env.user
                )
            )
            if not delegated_execution:
                return False
        if not transition.allowed_group_ids:
            return True
        return bool(transition.allowed_group_ids & self.env.user.all_group_ids)

    def _available_transitions(self):
        self.ensure_one()
        if self.status != "running":
            return self.env["cas.workflow.transition"]
        candidates = self.version_id.transition_ids.filtered(
            lambda item: item.from_state_id == self.current_state_id
        )
        return candidates.filtered(lambda item: self._user_can_execute(item))

    def action_get_available_transitions(self):
        self.ensure_one()
        self.check_access("read")
        return [
            {
                "id": transition.id,
                "code": transition.code,
                "name": transition.name,
                "to_state": transition.to_state_id.code,
                "note_required": transition.note_required,
            }
            for transition in self._available_transitions()
        ]

    def action_execute_transition(self, transition_id, note=False):
        self.ensure_one()
        self.check_access("write")
        transition = self.env["cas.workflow.transition"].browse(int(transition_id)).exists()
        if not transition or transition.version_id != self.version_id:
            raise ValidationError(_("انتقال متعلق به نسخه جاری گردش‌کار نیست."))
        if transition.from_state_id != self.current_state_id or self.status != "running":
            raise ValidationError(_("انتقال از وضعیت جاری قابل اجرا نیست."))
        if not self._user_can_execute(transition):
            raise AccessError(_("شما مجوز اجرای این انتقال را ندارید."))
        transition._validate_definition()
        if transition.note_required and not str(note or "").strip():
            raise ValidationError(_("ثبت یادداشت برای این انتقال الزامی است."))

        actor = self.env.user
        previous = self.current_state_id
        target = transition.to_state_id
        now = fields.Datetime.now()
        status = "running"
        completed_at = False
        if target.kind == "final":
            status = "completed"
            completed_at = now
        elif target.kind == "cancelled":
            status = "cancelled"
            completed_at = now
        responsible = actor if transition.responsible_mode == "actor" else self.responsible_user_id
        super(CasWorkflowInstance, self.sudo()).write(
            {
                "current_state_id": target.id,
                "status": status,
                "responsible_user_id": responsible.id,
                "state_entered_at": now,
                "state_deadline": self._deadline_for_state(target, now) if status == "running" else False,
                "completed_at": completed_at,
            }
        )
        self.env["cas.workflow.history"]._append_event(
            self,
            event_type="transition",
            transition=transition,
            from_state=previous,
            to_state=target,
            actor=actor,
            note=note,
        )
        self._sync_responsible_activity()
        return {
            "instance_id": self.id,
            "number": self.number,
            "state": target.code,
            "status": status,
            "responsible_user_id": responsible.id,
        }

    def _sync_responsible_activity(self):
        model_id = self.env["ir.model"]._get_id(self._name)
        todo = self.env.ref("mail.mail_activity_data_todo")
        for instance in self:
            existing = self.env["mail.activity"].sudo().search(
                [
                    ("res_model_id", "=", model_id),
                    ("res_id", "=", instance.id),
                    ("activity_type_id", "=", todo.id),
                ]
            )
            existing.unlink()
            if instance.status != "running":
                continue
            self.env["mail.activity"].sudo().create(
                {
                    "activity_type_id": todo.id,
                    "res_model_id": model_id,
                    "res_id": instance.id,
                    "user_id": instance.responsible_user_id.id,
                    "summary": _("اقدام لازم: %s", instance.current_state_id.name),
                    "note": _("گردش‌کار %s برای رکورد %s", instance.number, instance.resource_display_name),
                    "date_deadline": fields.Date.to_date(instance.state_deadline)
                    if instance.state_deadline
                    else fields.Date.context_today(instance),
                }
            )


class CasWorkflowHistory(models.Model):
    _name = "cas.workflow.history"
    _description = "CAS Workflow History"
    _order = "event_at desc, id desc"

    instance_id = fields.Many2one(
        "cas.workflow.instance", required=True, ondelete="restrict", index=True
    )
    company_id = fields.Many2one(related="instance_id.company_id", store=True, index=True)
    event_type = fields.Selection(
        [("started", "آغاز"), ("transition", "انتقال")], required=True, index=True
    )
    transition_id = fields.Many2one("cas.workflow.transition", ondelete="restrict")
    from_state_id = fields.Many2one("cas.workflow.state", ondelete="restrict")
    to_state_id = fields.Many2one("cas.workflow.state", required=True, ondelete="restrict")
    actor_user_id = fields.Many2one("res.users", required=True, ondelete="restrict", index=True)
    event_at = fields.Datetime(required=True, default=fields.Datetime.now, index=True)
    note = fields.Text()

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.is_superuser():
            raise AccessError(_("تاریخچه فقط توسط موتور گردش‌کار ثبت می‌شود."))
        return super().create(vals_list)

    def write(self, vals):
        raise ValidationError(_("تاریخچه گردش‌کار قابل ویرایش نیست."))

    def unlink(self):
        raise ValidationError(_("تاریخچه گردش‌کار قابل حذف نیست."))

    @api.model
    def _append_event(
        self,
        instance,
        event_type,
        to_state,
        actor,
        transition=False,
        from_state=False,
        note=False,
    ):
        return self.sudo().create(
            {
                "instance_id": instance.id,
                "event_type": event_type,
                "transition_id": transition.id if transition else False,
                "from_state_id": from_state.id if from_state else False,
                "to_state_id": to_state.id,
                "actor_user_id": actor.id,
                "event_at": fields.Datetime.now(),
                "note": note or False,
            }
        )
