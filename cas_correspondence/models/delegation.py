from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError

from .letter import _search_wants_true


class CasCorrespondenceSecretariatDelegation(models.Model):
    _name = "cas.correspondence.secretariat.delegation"
    _description = "CAS Secretariat Delegation"
    _inherit = ["mail.thread"]
    _order = "date_from desc, id desc"
    _rec_name = "delegate_user_id"

    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
        ondelete="restrict",
        index=True,
    )
    delegator_user_id = fields.Many2one(
        "res.users", required=True, readonly=True, ondelete="restrict", index=True
    )
    delegate_user_id = fields.Many2one(
        "res.users",
        required=True,
        ondelete="restrict",
        index=True,
        domain="[('active', '=', True), ('share', '=', False)]",
        tracking=True,
    )
    date_from = fields.Date(
        required=True, default=fields.Date.context_today, index=True, tracking=True
    )
    date_to = fields.Date(index=True, tracking=True)
    reason = fields.Text(required=True, tracking=True)
    active = fields.Boolean(default=True, readonly=True, tracking=True, index=True)
    revoked_at = fields.Datetime(readonly=True, index=True)
    revoked_by_id = fields.Many2one("res.users", readonly=True, ondelete="restrict")
    revocation_reason = fields.Text(readonly=True)
    audit_ids = fields.One2many(
        "cas.correspondence.audit", "delegation_id", string="تاریخچه رسمی", copy=False
    )
    visible_to_current_user = fields.Boolean(
        compute="_compute_visible_to_current_user",
        search="_search_visible_to_current_user",
    )

    @api.model
    def _require_ceo(self, company):
        if self.env.is_superuser() or self.env.user.has_group("base.group_system"):
            return True
        if company.cas_correspondence_ceo_user_id == self.env.user:
            return True
        raise AccessError(_("فقط مدیرعامل تعیین‌شده می‌تواند دسترسی دبیرخانه را تفویض کند."))

    def _user_can_read(self, user):
        self.ensure_one()
        return bool(
            self.env.is_superuser()
            or user.has_group("base.group_system")
            or self.delegate_user_id == user
            or self.delegator_user_id == user
            or self.company_id.cas_correspondence_ceo_user_id == user
        )

    def _is_valid(self, on_date=None):
        self.ensure_one()
        on_date = on_date or fields.Date.context_today(self)
        return bool(
            self.active
            and self.date_from <= on_date
            and (not self.date_to or self.date_to >= on_date)
            and self.delegate_user_id.active
            and not self.delegate_user_id.share
            and self.company_id in self.delegate_user_id.company_ids
        )

    @api.depends_context("uid", "allowed_company_ids")
    def _compute_visible_to_current_user(self):
        for delegation in self:
            delegation.visible_to_current_user = delegation._user_can_read(self.env.user)

    def _search_visible_to_current_user(self, operator, value):
        expected = _search_wants_true(operator, value)
        companies = self.env["res.company"].sudo().search(
            [
                ("id", "in", self.env.companies.ids),
                ("cas_correspondence_ceo_user_id", "=", self.env.user.id),
            ]
        )
        domain = [
            "|",
            "|",
            ("delegate_user_id", "=", self.env.user.id),
            ("delegator_user_id", "=", self.env.user.id),
            ("company_id", "in", companies.ids),
        ]
        if self.env.is_superuser() or self.env.user.has_group("base.group_system"):
            domain = [("company_id", "in", self.env.companies.ids)]
        return domain if expected else ["!", *domain]

    @api.constrains("date_from", "date_to", "delegate_user_id", "company_id")
    def _check_contract(self):
        for delegation in self:
            if delegation.date_to and delegation.date_to < delegation.date_from:
                raise ValidationError(_("تاریخ پایان نمی‌تواند قبل از تاریخ شروع باشد."))
            user = delegation.delegate_user_id.with_context(active_test=False)
            if not user.active or user.share or delegation.company_id not in user.company_ids:
                raise ValidationError(_("جانشین دبیرخانه باید کاربر داخلی و فعال همان شرکت باشد."))
            if user == delegation.company_id.cas_correspondence_ceo_user_id:
                raise ValidationError(_("مدیرعامل از ابتدا دسترسی دبیرخانه دارد و نیاز به تفویض ندارد."))

    @api.constrains("delegate_user_id", "company_id", "date_from", "date_to", "active")
    def _check_overlap(self):
        for delegation in self.filtered("active"):
            domain = [
                ("id", "!=", delegation.id),
                ("active", "=", True),
                ("company_id", "=", delegation.company_id.id),
                ("delegate_user_id", "=", delegation.delegate_user_id.id),
                "|",
                ("date_to", "=", False),
                ("date_to", ">=", delegation.date_from),
            ]
            overlaps = self.search(domain).filtered(
                lambda item: not delegation.date_to or item.date_from <= delegation.date_to
            )
            if overlaps:
                raise ValidationError(_("برای این کاربر تفویض دبیرخانه هم‌پوشان وجود دارد."))

    @api.model_create_multi
    def create(self, vals_list):
        records = self.browse()
        for original in vals_list:
            vals = dict(original)
            company = self.env["res.company"].browse(
                vals.get("company_id") or self.env.company.id
            ).exists()
            self._require_ceo(company)
            vals.update(
                {
                    "company_id": company.id,
                    "delegator_user_id": self.env.user.id,
                    "active": True,
                }
            )
            delegation = super(CasCorrespondenceSecretariatDelegation, self).create(vals)
            delegation._audit("delegated", delegation.reason)
            records |= delegation
        return records

    def write(self, vals):
        if not self.env.context.get("cas_correspondence_delegation_engine"):
            raise ValidationError(_("تفویض ثبت‌شده قابل ویرایش مستقیم نیست؛ آن را لغو کنید."))
        return super().write(vals)

    def unlink(self):
        raise ValidationError(_("تفویض دبیرخانه و سابقه آن قابل حذف نیست."))

    def _audit(self, event_type, reason=False):
        self.ensure_one()
        return (
            self.env["cas.correspondence.audit"]
            .sudo()
            .with_context(cas_correspondence_audit_engine=True)
            .create(
                {
                    "delegation_id": self.id,
                    "company_id": self.company_id.id,
                    "event_type": event_type,
                    "actor_user_id": self.env.user.id,
                    "reason": reason,
                    "payload": {
                        "delegate_user_id": self.delegate_user_id.id,
                        "date_from": fields.Date.to_string(self.date_from),
                        "date_to": fields.Date.to_string(self.date_to) if self.date_to else False,
                    },
                }
            )
        )

    def action_revoke(self, reason=False):
        for delegation in self:
            delegation._require_ceo(delegation.company_id)
            if not delegation.active:
                raise ValidationError(_("این تفویض قبلاً لغو شده است."))
            if not str(reason or "").strip():
                raise ValidationError(_("درج دلیل لغو تفویض الزامی است."))
            delegation.with_context(cas_correspondence_delegation_engine=True).write(
                {
                    "active": False,
                    "revoked_at": fields.Datetime.now(),
                    "revoked_by_id": self.env.user.id,
                    "revocation_reason": reason,
                }
            )
            delegation._audit("revoked", reason)
        return True

    def action_open_revoke_wizard(self):
        self.ensure_one()
        self._require_ceo(self.company_id)
        return {
            "type": "ir.actions.act_window",
            "name": _("لغو تفویض دبیرخانه"),
            "res_model": "cas.correspondence.delegation.revoke.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_delegation_id": self.id},
        }
