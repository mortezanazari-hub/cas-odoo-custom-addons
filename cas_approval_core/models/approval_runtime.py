"""Runtime approval requests, decisions, activities and immutable audit events."""

from __future__ import annotations

from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CasApprovalRequest(models.Model):
    _name = "cas.approval.request"
    _description = "CAS Approval Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc, id desc"
    _rec_name = "number"

    number = fields.Char(default="New", readonly=True, copy=False, index=True)
    instance_id = fields.Many2one(
        "cas.workflow.instance", required=True, ondelete="restrict", index=True
    )
    policy_id = fields.Many2one(
        "cas.approval.policy", required=True, ondelete="restrict", index=True
    )
    state_id = fields.Many2one(
        "cas.workflow.state", required=True, ondelete="restrict", index=True
    )
    company_id = fields.Many2one(
        related="instance_id.company_id", store=True, index=True, readonly=True
    )
    status = fields.Selection(
        [
            ("pending", "در انتظار تصمیم"),
            ("approved", "تأییدشده"),
            ("rejected", "ردشده"),
            ("cancelled", "لغوشده"),
        ],
        required=True,
        default="pending",
        readonly=True,
        tracking=True,
        index=True,
    )
    execution_mode = fields.Selection(
        [("parallel", "موازی"), ("sequential", "ترتیبی")],
        required=True,
        readonly=True,
    )
    decision_rule = fields.Selection(
        [("all", "تأیید همه"), ("quorum", "حد نصاب")],
        required=True,
        readonly=True,
    )
    quorum_count = fields.Integer(readonly=True)
    requested_at = fields.Datetime(required=True, readonly=True, index=True)
    completed_at = fields.Datetime(readonly=True, index=True)
    outcome_transition_id = fields.Many2one(
        "cas.workflow.transition", readonly=True, ondelete="restrict"
    )
    line_ids = fields.One2many("cas.approval.line", "request_id", copy=False)
    history_ids = fields.One2many("cas.approval.history", "request_id", copy=False)

    _number_uniq = models.Constraint(
        "UNIQUE(number)", "شماره درخواست تأیید باید یکتا باشد."
    )

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.is_superuser():
            raise AccessError(_("درخواست تأیید فقط توسط موتور تأیید ساخته می‌شود."))
        return super().create(vals_list)

    def write(self, vals):
        if not self.env.context.get("cas_approval_engine"):
            raise ValidationError(_("درخواست تأیید فقط توسط عملیات رسمی تغییر می‌کند."))
        return super().write(vals)

    def unlink(self):
        raise ValidationError(_("درخواست و سابقه تأیید قابل حذف نیست."))

    @api.model
    def _start_for_instance(self, instance, policy):
        instance.ensure_one()
        policy.ensure_one()
        if instance.status != "running" or instance.current_state_id != policy.state_id:
            raise ValidationError(_("سیاست تأیید با مرحله جاری گردش‌کار منطبق نیست."))
        existing = self.sudo().search(
            [
                ("instance_id", "=", instance.id),
                ("policy_id", "=", policy.id),
                ("state_id", "=", instance.current_state_id.id),
                ("status", "=", "pending"),
            ],
            limit=1,
        )
        if existing:
            return existing

        resolved = []
        for step in policy.step_ids.sorted(lambda item: (item.sequence, item.id)):
            users = self._resolve_step_users(instance, step)
            if not users:
                raise ValidationError(
                    _("برای گام تأیید «%s» تأییدکننده فعال پیدا نشد.", step.name)
                )
            for user in users:
                resolved.append((step, user))
        if not resolved:
            raise ValidationError(_("سیاست تأیید هیچ تأییدکننده فعالی ندارد."))
        if policy.decision_rule == "quorum" and policy.quorum_count > len(resolved):
            raise ValidationError(_("حد نصاب از تعداد تأییدکنندگان واقعی بیشتر است."))

        now = fields.Datetime.now()
        request = self.sudo().create(
            {
                "number": self.env["ir.sequence"].next_by_code("cas.approval.request")
                or "New",
                "instance_id": instance.id,
                "policy_id": policy.id,
                "state_id": instance.current_state_id.id,
                "status": "pending",
                "execution_mode": policy.execution_mode,
                "decision_rule": policy.decision_rule,
                "quorum_count": policy.quorum_count,
                "requested_at": now,
            }
        )
        first_sequence = min(step.sequence for step, _user in resolved)
        line_values = []
        for step, user in resolved:
            pending = policy.execution_mode == "parallel" or step.sequence == first_sequence
            assigned_at = now if pending else False
            deadline = (
                now + timedelta(hours=step.deadline_hours)
                if pending and step.deadline_hours
                else False
            )
            line_values.append(
                {
                    "request_id": request.id,
                    "step_id": step.id,
                    "sequence": step.sequence,
                    "role_label": step.role_label,
                    "approver_user_id": user.id,
                    "status": "pending" if pending else "waiting",
                    "assigned_at": assigned_at,
                    "deadline": deadline,
                }
            )
        self.env["cas.approval.line"].sudo().create(line_values)
        self.env["cas.approval.history"]._append_event(
            request,
            event_type="requested",
            actor=self.env.user,
            note=_("درخواست تأیید برای مرحله %s ساخته شد.", instance.current_state_id.name),
        )
        request._sync_activities()
        return request

    @api.model
    def _resolve_step_users(self, instance, step):
        Users = self.env["res.users"].sudo().with_context(active_test=False)
        if step.approver_type == "user":
            users = step.approver_user_id
        elif step.approver_type == "workflow_responsible":
            users = instance.responsible_user_id
        elif step.approver_type == "instance_starter":
            users = instance.started_by_id
        else:
            users = Users.search(
                [
                    ("active", "=", True),
                    ("share", "=", False),
                    ("all_group_ids", "in", step.approver_group_id.id),
                    ("company_ids", "in", instance.company_id.id),
                ],
                order="id",
            )
        users = users.with_context(active_test=False).exists().filtered(
            lambda user: user.active
            and not user.share
            and instance.company_id in user.company_ids
        )
        return users

    def _activate_next_sequence(self):
        self.ensure_one()
        self = self.sudo()
        waiting = self.line_ids.filtered(lambda line: line.status == "waiting")
        if not waiting:
            return False
        next_sequence = min(waiting.mapped("sequence"))
        now = fields.Datetime.now()
        for line in waiting.filtered(lambda item: item.sequence == next_sequence):
            deadline = (
                now + timedelta(hours=line.step_id.deadline_hours)
                if line.step_id.deadline_hours
                else False
            )
            line.with_context(cas_approval_engine=True).sudo().write(
                {"status": "pending", "assigned_at": now, "deadline": deadline}
            )
        self._sync_activities()
        return True

    def _evaluate(self):
        self.ensure_one()
        self = self.sudo()
        if self.status != "pending":
            return
        approved = self.line_ids.filtered(lambda line: line.status == "approved")
        rejected = self.line_ids.filtered(lambda line: line.status == "rejected")
        undecided = self.line_ids.filtered(lambda line: line.status in {"pending", "waiting"})

        if self.decision_rule == "all":
            if rejected:
                self._complete("rejected")
                return
            if not undecided:
                self._complete("approved")
                return
        else:
            if len(approved) >= self.quorum_count:
                self._complete("approved")
                return
            if len(approved) + len(undecided) < self.quorum_count:
                self._complete("rejected")
                return

        pending = self.line_ids.filtered(lambda line: line.status == "pending")
        if self.execution_mode == "sequential" and not pending:
            self._activate_next_sequence()

    def _complete(self, outcome):
        self.ensure_one()
        self = self.sudo()
        if outcome not in {"approved", "rejected"} or self.status != "pending":
            raise ValidationError(_("نتیجه نهایی درخواست تأیید معتبر نیست."))
        transition = (
            self.policy_id.approve_transition_id
            if outcome == "approved"
            else self.policy_id.reject_transition_id
        )
        now = fields.Datetime.now()
        undecided = self.line_ids.filtered(lambda line: line.status in {"pending", "waiting"})
        if undecided:
            undecided.with_context(cas_approval_engine=True).sudo().write(
                {"status": "cancelled"}
            )
        self.with_context(cas_approval_engine=True).sudo().write(
            {
                "status": outcome,
                "completed_at": now,
                "outcome_transition_id": transition.id if transition else False,
            }
        )
        self._sync_activities()
        actor = self.env.user
        self.env["cas.approval.history"]._append_event(
            self,
            event_type="request_approved" if outcome == "approved" else "request_rejected",
            actor=actor,
            note=_("نتیجه نهایی درخواست: %s", dict(self._fields["status"].selection)[outcome]),
        )
        if transition:
            self.instance_id.sudo().with_context(
                cas_approval_authorized_request_id=self.id
            ).action_execute_transition(
                transition.id,
                note=_("انتقال خودکار بر اساس نتیجه درخواست تأیید %s", self.number),
            )

    def _sync_activities(self):
        for request in self.sudo():
            for line in request.line_ids.sudo():
                line._sync_activity()


class CasApprovalLine(models.Model):
    _name = "cas.approval.line"
    _description = "CAS Approval Decision Line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "request_id, sequence, id"

    request_id = fields.Many2one(
        "cas.approval.request", required=True, ondelete="restrict", index=True
    )
    step_id = fields.Many2one(
        "cas.approval.step", required=True, ondelete="restrict", index=True
    )
    instance_id = fields.Many2one(
        related="request_id.instance_id", store=True, index=True, readonly=True
    )
    state_id = fields.Many2one(
        related="request_id.state_id", store=True, index=True, readonly=True
    )
    company_id = fields.Many2one(
        related="request_id.company_id", store=True, index=True, readonly=True
    )
    sequence = fields.Integer(required=True, readonly=True)
    role_label = fields.Char(string="نقش تأیید", required=True, readonly=True)
    approver_user_id = fields.Many2one(
        "res.users", string="تأییدکننده منصوب", required=True, ondelete="restrict", index=True
    )
    delegate_user_id = fields.Many2one(
        "res.users", string="جانشین", readonly=True, ondelete="restrict"
    )
    decision_user_id = fields.Many2one(
        "res.users", string="تصمیم‌گیرنده واقعی", readonly=True, ondelete="restrict", index=True
    )
    status = fields.Selection(
        [
            ("waiting", "در انتظار نوبت"),
            ("pending", "در انتظار تصمیم"),
            ("approved", "تأییدشده"),
            ("rejected", "ردشده"),
            ("cancelled", "لغوشده"),
        ],
        required=True,
        readonly=True,
        index=True,
        tracking=True,
    )
    assigned_at = fields.Datetime(readonly=True, index=True)
    decided_at = fields.Datetime(readonly=True, index=True)
    deadline = fields.Datetime(readonly=True, index=True)
    delay_hours = fields.Float(string="تأخیر تصمیم (ساعت)", readonly=True)
    comment = fields.Text(string="نظر تصمیم‌گیرنده", readonly=True)
    rejection_reason = fields.Text(string="دلیل رد", readonly=True)

    _request_step_user_uniq = models.Constraint(
        "UNIQUE(request_id, step_id, approver_user_id)",
        "برای هر گام، تأییدکننده واقعی باید یکتا باشد.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.is_superuser():
            raise AccessError(_("خط تصمیم فقط توسط موتور تأیید ساخته می‌شود."))
        return super().create(vals_list)

    def write(self, vals):
        if not self.env.context.get("cas_approval_engine"):
            raise ValidationError(_("خط تصمیم فقط از عملیات رسمی قابل تغییر است."))
        return super().write(vals)

    def unlink(self):
        raise ValidationError(_("خط تصمیم و سابقه آن قابل حذف نیست."))

    def _check_decision_access(self):
        self.ensure_one()
        if self.status != "pending" or self.request_id.status != "pending":
            raise ValidationError(_("این تصمیم دیگر در انتظار اقدام نیست."))
        if not (
            self.env.is_superuser()
            or self.approver_user_id == self.env.user
            or self.delegate_user_id == self.env.user
            or self.env.user.has_group("cas_approval_core.group_cas_approval_manager")
        ):
            raise AccessError(_("شما تأییدکننده این تصمیم نیستید."))

    def action_approve(self, comment=False):
        self.ensure_one()
        self.check_access("read")
        self._check_decision_access()
        self._record_decision("approved", comment=comment)
        return True

    def action_open_reject_wizard(self):
        self.ensure_one()
        self.check_access("read")
        self._check_decision_access()
        return {
            "type": "ir.actions.act_window",
            "name": _("رد درخواست تأیید"),
            "res_model": "cas.approval.reject.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_line_id": self.id},
        }

    def action_reject(self, reason, comment=False):
        self.ensure_one()
        self.check_access("read")
        self._check_decision_access()
        if not str(reason or "").strip():
            raise ValidationError(_("ثبت دلیل رد الزامی است."))
        self._record_decision("rejected", comment=comment, rejection_reason=reason)
        return True

    def _record_decision(self, outcome, comment=False, rejection_reason=False):
        self.ensure_one()
        now = fields.Datetime.now()
        delay_hours = 0.0
        if self.deadline and now > self.deadline:
            delay_hours = (now - self.deadline).total_seconds() / 3600.0
        self.with_context(cas_approval_engine=True).sudo().write(
            {
                "status": outcome,
                "decision_user_id": self.env.user.id,
                "decided_at": now,
                "delay_hours": delay_hours,
                "comment": str(comment or "").strip() or False,
                "rejection_reason": str(rejection_reason or "").strip() or False,
            }
        )
        self.env["cas.approval.history"]._append_event(
            self.request_id,
            event_type="line_approved" if outcome == "approved" else "line_rejected",
            actor=self.env.user,
            line=self,
            note=self.rejection_reason or self.comment or False,
        )
        self._sync_activity()
        self.request_id._evaluate()

    def _sync_activity(self):
        self.ensure_one()
        self = self.sudo()
        existing = self.env["mail.activity"].sudo().search(
            [
                ("res_model", "=", self._name),
                ("res_id", "=", self.id),
                ("activity_type_id", "=", self.env.ref("mail.mail_activity_data_todo").id),
            ]
        )
        existing.unlink()
        if self.status != "pending" or self.request_id.status != "pending":
            return
        model_id = self.env["ir.model"]._get_id(self._name)
        self.env["mail.activity"].sudo().create(
            {
                "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
                "res_model_id": model_id,
                "res_id": self.id,
                "user_id": self.approver_user_id.id,
                "summary": _("تصمیم لازم: %s", self.role_label),
                "note": _(
                    "درخواست %s برای گردش‌کار %s در مرحله %s",
                    self.request_id.number,
                    self.instance_id.number,
                    self.state_id.name,
                ),
                "date_deadline": fields.Date.to_date(self.deadline)
                if self.deadline
                else fields.Date.context_today(self),
            }
        )


class CasApprovalHistory(models.Model):
    _name = "cas.approval.history"
    _description = "CAS Approval Immutable History"
    _order = "event_at desc, id desc"

    request_id = fields.Many2one(
        "cas.approval.request", required=True, ondelete="restrict", index=True
    )
    line_id = fields.Many2one("cas.approval.line", ondelete="restrict", index=True)
    instance_id = fields.Many2one(
        related="request_id.instance_id", store=True, index=True, readonly=True
    )
    company_id = fields.Many2one(
        related="request_id.company_id", store=True, index=True, readonly=True
    )
    event_type = fields.Selection(
        [
            ("requested", "ایجاد درخواست"),
            ("line_approved", "تأیید خط"),
            ("line_rejected", "رد خط"),
            ("request_approved", "تأیید نهایی درخواست"),
            ("request_rejected", "رد نهایی درخواست"),
        ],
        required=True,
        index=True,
    )
    actor_user_id = fields.Many2one(
        "res.users", required=True, ondelete="restrict", index=True
    )
    event_at = fields.Datetime(required=True, default=fields.Datetime.now, index=True)
    note = fields.Text()

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.is_superuser():
            raise AccessError(_("تاریخچه تأیید فقط توسط موتور ثبت می‌شود."))
        return super().create(vals_list)

    def write(self, vals):
        raise ValidationError(_("تاریخچه تأیید قابل ویرایش نیست."))

    def unlink(self):
        raise ValidationError(_("تاریخچه تأیید قابل حذف نیست."))

    @api.model
    def _append_event(self, request, event_type, actor, line=False, note=False):
        return self.sudo().create(
            {
                "request_id": request.id,
                "line_id": line.id if line else False,
                "event_type": event_type,
                "actor_user_id": actor.id,
                "event_at": fields.Datetime.now(),
                "note": note or False,
            }
        )


class CasApprovalRejectWizard(models.TransientModel):
    _name = "cas.approval.reject.wizard"
    _description = "CAS Approval Rejection Wizard"

    line_id = fields.Many2one(
        "cas.approval.line", string="تصمیم تأیید", required=True, readonly=True
    )
    reason = fields.Text(string="دلیل رد", required=True)
    comment = fields.Text(string="توضیحات تکمیلی")

    def action_confirm(self):
        self.ensure_one()
        self.line_id.action_reject(self.reason, comment=self.comment)
        return {"type": "ir.actions.act_window_close"}


class CasWorkflowInstance(models.Model):
    _inherit = "cas.workflow.instance"

    approval_request_ids = fields.One2many(
        "cas.approval.request", "instance_id", string="درخواست‌های تأیید", copy=False
    )

    @api.model
    def _start_instance(self, version, resource, responsible_user_id=False):
        result = super()._start_instance(
            version, resource, responsible_user_id=responsible_user_id
        )
        instance = self.browse(result["instance_id"])
        instance._ensure_approval_for_current_state()
        return result

    def action_execute_transition(self, transition_id, note=False):
        self.ensure_one()
        transition = self.env["cas.workflow.transition"].browse(int(transition_id)).exists()
        policies = self.env["cas.approval.policy"].sudo().search(
            [
                ("version_id", "=", self.version_id.id),
                ("state_id", "=", self.current_state_id.id),
                "|",
                ("approve_transition_id", "=", transition.id),
                ("reject_transition_id", "=", transition.id),
            ]
        )
        if policies:
            authorized_id = int(
                self.env.context.get("cas_approval_authorized_request_id") or 0
            )
            request = self.env["cas.approval.request"].sudo().browse(authorized_id).exists()
            valid = bool(
                request
                and request.instance_id == self
                and request.policy_id in policies
                and (
                    (
                        transition == request.policy_id.approve_transition_id
                        and request.status == "approved"
                    )
                    or (
                        transition == request.policy_id.reject_transition_id
                        and request.status == "rejected"
                    )
                )
            )
            if not valid:
                raise ValidationError(
                    _("این انتقال فقط پس از تکمیل رسمی فرایند تأیید قابل اجرا است.")
                )
        result = super().action_execute_transition(transition_id, note=note)
        self._ensure_approval_for_current_state()
        return result

    def _ensure_approval_for_current_state(self):
        for instance in self:
            if instance.status != "running":
                continue
            policy = self.env["cas.approval.policy"].sudo().search(
                [
                    ("version_id", "=", instance.version_id.id),
                    ("state_id", "=", instance.current_state_id.id),
                ],
                limit=1,
            )
            if policy:
                self.env["cas.approval.request"]._start_for_instance(instance, policy)
