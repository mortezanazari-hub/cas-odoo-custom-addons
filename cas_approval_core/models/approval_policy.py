"""Versioned approval policy models attached to workflow states."""

from __future__ import annotations

import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


TECHNICAL_CODE_RE = re.compile(r"^[a-z][a-z0-9_]*$")


class CasApprovalPolicy(models.Model):
    _name = "cas.approval.policy"
    _description = "CAS Approval Policy"
    _inherit = "cas.workflow.versioned.mixin"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    name = fields.Char(string="عنوان سیاست تأیید", required=True, translate=True)
    code = fields.Char(string="کد فنی", required=True, index=True)
    state_id = fields.Many2one(
        "cas.workflow.state",
        string="مرحله گردش‌کار",
        required=True,
        ondelete="cascade",
        index=True,
    )
    approve_transition_id = fields.Many2one(
        "cas.workflow.transition",
        string="انتقال پس از تأیید",
        required=True,
        ondelete="restrict",
    )
    reject_transition_id = fields.Many2one(
        "cas.workflow.transition",
        string="انتقال پس از رد",
        ondelete="restrict",
    )
    execution_mode = fields.Selection(
        [("parallel", "موازی"), ("sequential", "ترتیبی")],
        string="روش اجرا",
        required=True,
        default="parallel",
    )
    decision_rule = fields.Selection(
        [("all", "تأیید همه"), ("quorum", "حد نصاب")],
        string="قاعده تصمیم",
        required=True,
        default="all",
    )
    quorum_count = fields.Integer(string="حد نصاب تأیید", default=1)
    step_ids = fields.One2many(
        "cas.approval.step", "policy_id", string="تأییدکنندگان", copy=False
    )

    _code_version_uniq = models.Constraint(
        "UNIQUE(version_id, code)", "کد سیاست تأیید باید در هر نسخه یکتا باشد."
    )
    _state_version_uniq = models.Constraint(
        "UNIQUE(version_id, state_id)", "برای هر مرحله فقط یک سیاست تأیید مجاز است."
    )
    _quorum_positive = models.Constraint(
        "CHECK(quorum_count > 0)", "حد نصاب تأیید باید مثبت باشد."
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
        return super().write(vals)

    @api.constrains(
        "code",
        "version_id",
        "state_id",
        "approve_transition_id",
        "reject_transition_id",
        "decision_rule",
        "quorum_count",
    )
    def _check_policy_contract(self):
        for policy in self:
            if policy.code and not TECHNICAL_CODE_RE.fullmatch(policy.code):
                raise ValidationError(_("کد فنی سیاست تأیید معتبر نیست."))
            policy._validate_definition(require_steps=False)

    def _validate_definition(self, require_steps=True):
        self.ensure_one()
        if self.state_id.version_id != self.version_id:
            raise ValidationError(_("مرحله تأیید باید متعلق به همان نسخه گردش‌کار باشد."))
        if self.state_id.kind in {"final", "cancelled"}:
            raise ValidationError(_("برای مرحله پایانی یا لغوشده نمی‌توان تأیید تعریف کرد."))
        transitions = self.approve_transition_id | self.reject_transition_id
        if any(item.version_id != self.version_id for item in transitions):
            raise ValidationError(_("انتقال‌های تأیید و رد باید متعلق به همان نسخه باشند."))
        if any(item.from_state_id != self.state_id for item in transitions):
            raise ValidationError(_("انتقال تأیید یا رد باید از مرحله سیاست آغاز شود."))
        if self.reject_transition_id and self.reject_transition_id == self.approve_transition_id:
            raise ValidationError(_("انتقال تأیید و رد نمی‌توانند یکسان باشند."))
        if self.decision_rule == "quorum" and self.quorum_count < 1:
            raise ValidationError(_("حد نصاب تأیید باید مثبت باشد."))
        if require_steps and not self.step_ids:
            raise ValidationError(_("سیاست تأیید باید حداقل یک تأییدکننده داشته باشد."))
        for step in self.step_ids:
            step._validate_definition()

    def _schema_payload(self):
        self.ensure_one()
        return {
            "code": self.code,
            "state": self.state_id.code,
            "approve_transition": self.approve_transition_id.code,
            "reject_transition": self.reject_transition_id.code or False,
            "execution_mode": self.execution_mode,
            "decision_rule": self.decision_rule,
            "quorum_count": self.quorum_count,
            "steps": [step._schema_payload() for step in self.step_ids.sorted("sequence")],
        }


class CasApprovalStep(models.Model):
    _name = "cas.approval.step"
    _description = "CAS Approval Step"
    _order = "sequence, id"

    policy_id = fields.Many2one(
        "cas.approval.policy", required=True, ondelete="cascade", index=True
    )
    version_id = fields.Many2one(
        related="policy_id.version_id", store=True, index=True, readonly=True
    )
    company_id = fields.Many2one(
        related="policy_id.company_id", store=True, index=True, readonly=True
    )
    sequence = fields.Integer(default=10)
    name = fields.Char(string="عنوان گام تأیید", required=True, translate=True)
    role_label = fields.Char(string="نقش سازمانی", required=True)
    approver_type = fields.Selection(
        [
            ("user", "کاربر مشخص"),
            ("group", "اعضای گروه"),
            ("workflow_responsible", "مسئول جاری گردش‌کار"),
            ("instance_starter", "آغازکننده گردش‌کار"),
        ],
        string="نوع تأییدکننده",
        required=True,
        default="user",
    )
    approver_user_id = fields.Many2one(
        "res.users",
        string="کاربر تأییدکننده",
        ondelete="restrict",
        domain="[('active', '=', True), ('share', '=', False)]",
    )
    approver_group_id = fields.Many2one(
        "res.groups", string="گروه تأییدکننده", ondelete="restrict"
    )
    deadline_hours = fields.Float(string="مهلت تصمیم (ساعت)", default=0)

    _deadline_nonnegative = models.Constraint(
        "CHECK(deadline_hours >= 0)", "مهلت تصمیم نمی‌تواند منفی باشد."
    )

    @api.model_create_multi
    def create(self, vals_list):
        policies = self.env["cas.approval.policy"].browse(
            {vals.get("policy_id") for vals in vals_list if vals.get("policy_id")}
        ).exists()
        if any(policy.version_id.state != "draft" for policy in policies):
            raise ValidationError(_("گام‌های سیاست منتشرشده قابل تغییر نیستند."))
        return super().create(vals_list)

    def write(self, vals):
        if any(step.policy_id.version_id.state != "draft" for step in self):
            raise ValidationError(_("گام‌های سیاست منتشرشده قابل تغییر نیستند."))
        if "policy_id" in vals:
            raise ValidationError(_("انتقال گام بین سیاست‌ها مجاز نیست."))
        return super().write(vals)

    def unlink(self):
        if any(step.policy_id.version_id.state != "draft" for step in self):
            raise ValidationError(_("گام‌های سیاست منتشرشده قابل حذف نیستند."))
        return super().unlink()

    @api.constrains("approver_type", "approver_user_id", "approver_group_id")
    def _check_approver_contract(self):
        for step in self:
            step._validate_definition()

    def _validate_definition(self):
        self.ensure_one()
        if self.approver_type == "user":
            user = self.approver_user_id.with_context(active_test=False)
            if not user or not user.active or user.share:
                raise ValidationError(_("کاربر تأییدکننده باید داخلی و فعال باشد."))
            if user.company_id != self.company_id and self.company_id not in user.company_ids:
                raise ValidationError(_("کاربر تأییدکننده خارج از شرکت سیاست است."))
            if self.approver_group_id:
                raise ValidationError(_("برای کاربر مشخص نباید گروه تعیین شود."))
        elif self.approver_type == "group":
            if not self.approver_group_id:
                raise ValidationError(_("برای تأیید گروهی باید گروه مشخص شود."))
            if self.approver_user_id:
                raise ValidationError(_("برای تأیید گروهی نباید کاربر ثابت تعیین شود."))
        elif self.approver_user_id or self.approver_group_id:
            raise ValidationError(_("برای نقش پویا نباید کاربر یا گروه ثابت تعیین شود."))

    def _schema_payload(self):
        self.ensure_one()
        return {
            "sequence": self.sequence,
            "name": self.name,
            "role": self.role_label,
            "approver_type": self.approver_type,
            "approver_user": self.approver_user_id.login or False,
            "approver_group": self.approver_group_id.get_external_id().get(
                self.approver_group_id.id, False
            )
            or self.approver_group_id.name
            or False,
            "deadline_hours": self.deadline_hours,
        }


class CasWorkflowVersion(models.Model):
    _inherit = "cas.workflow.version"

    approval_policy_ids = fields.One2many(
        "cas.approval.policy", "version_id", string="سیاست‌های تأیید", copy=False
    )

    def _schema_payload(self):
        payload = super()._schema_payload()
        payload["approval_policies"] = [
            policy._schema_payload() for policy in self.approval_policy_ids.sorted("sequence")
        ]
        return payload

    def _validate_publishable(self):
        result = super()._validate_publishable()
        for policy in self.approval_policy_ids:
            policy._validate_definition(require_steps=True)
        return result

    def action_new_revision(self):
        action = super().action_new_revision()
        clone = self.browse(action["res_id"])
        state_map = {state.code: state for state in clone.state_ids}
        transition_map = {transition.code: transition for transition in clone.transition_ids}
        for source in self.approval_policy_ids.sorted("sequence"):
            new_policy = source.copy(
                {
                    "version_id": clone.id,
                    "state_id": state_map[source.state_id.code].id,
                    "approve_transition_id": transition_map[
                        source.approve_transition_id.code
                    ].id,
                    "reject_transition_id": transition_map[
                        source.reject_transition_id.code
                    ].id
                    if source.reject_transition_id
                    else False,
                }
            )
            for step in source.step_ids.sorted("sequence"):
                step.copy({"policy_id": new_policy.id})
        return action
