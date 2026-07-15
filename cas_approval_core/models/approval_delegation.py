"""Date-bounded and auditable approval delegation."""

from __future__ import annotations

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CasApprovalDelegation(models.Model):
    _name = "cas.approval.delegation"
    _description = "CAS Approval Delegation"
    _inherit = ["mail.thread"]
    _order = "date_from desc, id desc"
    _rec_name = "delegator_user_id"

    delegator_user_id = fields.Many2one(
        "res.users",
        string="تفویض‌کننده",
        required=True,
        ondelete="restrict",
        tracking=True,
        domain="[('active', '=', True), ('share', '=', False)]",
        index=True,
    )
    delegate_user_id = fields.Many2one(
        "res.users",
        string="جانشین",
        required=True,
        ondelete="restrict",
        tracking=True,
        domain="[('active', '=', True), ('share', '=', False)]",
        index=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="شرکت",
        required=True,
        default=lambda self: self.env.company,
        ondelete="restrict",
        index=True,
    )
    date_from = fields.Date(
        string="از تاریخ", required=True, default=fields.Date.context_today, index=True
    )
    date_to = fields.Date(string="تا تاریخ", index=True)
    policy_ids = fields.Many2many(
        "cas.approval.policy",
        "cas_approval_delegation_policy_rel",
        "delegation_id",
        "policy_id",
        string="سیاست‌های محدودشده",
        help="اگر خالی باشد، جانشینی برای همه سیاست‌های تأیید این شرکت معتبر است.",
    )
    reason = fields.Text(string="دلیل جانشینی", required=True)
    active = fields.Boolean(default=True, tracking=True, index=True)
    decision_line_ids = fields.One2many(
        "cas.approval.line", "delegation_id", string="تصمیم‌های استفاده‌شده", readonly=True
    )

    @api.constrains(
        "delegator_user_id",
        "delegate_user_id",
        "company_id",
        "date_from",
        "date_to",
        "policy_ids",
        "active",
    )
    def _check_delegation_contract(self):
        for delegation in self:
            if delegation.delegator_user_id == delegation.delegate_user_id:
                raise ValidationError(_("تفویض‌کننده و جانشین نمی‌توانند یک نفر باشند."))
            if delegation.date_to and delegation.date_to < delegation.date_from:
                raise ValidationError(_("تاریخ پایان جانشینی نمی‌تواند پیش از شروع باشد."))
            for user in delegation.delegator_user_id | delegation.delegate_user_id:
                candidate = user.with_context(active_test=False)
                if not candidate.active or candidate.share:
                    raise ValidationError(_("تفویض‌کننده و جانشین باید کاربران داخلی فعال باشند."))
                if delegation.company_id not in candidate.company_ids:
                    raise ValidationError(_("کاربر جانشینی خارج از شرکت انتخاب‌شده است."))
            if any(policy.company_id != delegation.company_id for policy in delegation.policy_ids):
                raise ValidationError(_("سیاست‌های جانشینی باید متعلق به همان شرکت باشند."))
            if delegation.active:
                delegation._check_overlap()

    def _check_overlap(self):
        self.ensure_one()
        domain = [
            ("id", "!=", self.id),
            ("active", "=", True),
            ("company_id", "=", self.company_id.id),
            ("delegator_user_id", "=", self.delegator_user_id.id),
            "|",
            ("date_to", "=", False),
            ("date_to", ">=", self.date_from),
        ]
        if self.date_to:
            domain.append(("date_from", "<=", self.date_to))
        for other in self.sudo().search(domain):
            if not self.policy_ids or not other.policy_ids or self.policy_ids & other.policy_ids:
                raise ValidationError(
                    _("برای این کاربر در بازه و محدوده سیاست انتخاب‌شده جانشینی هم‌پوشان وجود دارد.")
                )

    def write(self, vals):
        protected = {
            "delegator_user_id",
            "delegate_user_id",
            "company_id",
            "date_from",
            "date_to",
            "policy_ids",
            "reason",
        }
        if protected.intersection(vals) and any(record.decision_line_ids for record in self):
            raise ValidationError(
                _("جانشینی استفاده‌شده قابل بازنویسی نیست؛ آن را غیرفعال کنید.")
            )
        return super().write(vals)

    def unlink(self):
        if any(record.decision_line_ids for record in self):
            raise ValidationError(_("جانشینی استفاده‌شده قابل حذف نیست."))
        return super().unlink()

    @api.model
    def _find_for(self, policy, delegator, on_date=None):
        on_date = on_date or fields.Date.context_today(self)
        candidates = self.sudo().search(
            [
                ("active", "=", True),
                ("company_id", "=", policy.company_id.id),
                ("delegator_user_id", "=", delegator.id),
                ("date_from", "<=", on_date),
                "|",
                ("date_to", "=", False),
                ("date_to", ">=", on_date),
            ],
            order="date_from desc, id desc",
        )
        matching = candidates.filtered(
            lambda item: not item.policy_ids or policy in item.policy_ids
        )
        if len(matching) > 1:
            raise ValidationError(_("بیش از یک جانشینی معتبر برای تأییدکننده پیدا شد."))
        return matching
