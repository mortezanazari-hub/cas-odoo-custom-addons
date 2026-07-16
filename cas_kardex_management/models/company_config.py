from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    cas_ceo_user_id = fields.Many2one(
        "res.users", string="مدیرعامل برای تأییدهای کاردکس", ondelete="restrict",
        domain="[('active','=',True),('share','=',False)]",
    )
    cas_kardex_lock_day = fields.Integer(string="روز قفل کاردکس ماه قبل", default=4)

    @api.constrains("cas_kardex_lock_day", "cas_ceo_user_id")
    def _check_cas_kardex_config(self):
        for company in self:
            if not 1 <= company.cas_kardex_lock_day <= 28:
                raise ValidationError(_("روز قفل کاردکس باید بین ۱ و ۲۸ باشد."))
            user = company.cas_ceo_user_id.with_context(active_test=False)
            if user and (not user.active or user.share or company not in user.company_ids):
                raise ValidationError(_("مدیرعامل باید کاربر داخلی، فعال و عضو همان شرکت باشد."))


class CasKardexApprovalMixin(models.AbstractModel):
    _name = "cas.kardex.approval.mixin"
    _description = "CAS Kardex Approval Routing"

    @api.model
    def _cas_manager_or_ceo(self, employee):
        employee = employee.sudo()
        company = employee.company_id
        visited = set()
        manager = employee.parent_id
        while manager and manager.id not in visited:
            visited.add(manager.id)
            user = manager.user_id.with_context(active_test=False)
            if user and user.active and not user.share and company in user.company_ids:
                return user, "manager"
            manager = manager.parent_id
        department = employee.department_id
        visited = set()
        while department and department.id not in visited:
            visited.add(department.id)
            user = department.manager_id.user_id.with_context(active_test=False)
            if user and user.active and not user.share and company in user.company_ids and user != employee.user_id:
                return user, "manager"
            department = department.parent_id
        if company.cas_ceo_user_id:
            return company.cas_ceo_user_id, "ceo"
        raise ValidationError(_("برای این کارمند مدیر معتبر پیدا نشد و مدیرعامل شرکت نیز تنظیم نشده است."))

    def _cas_require_ceo(self, company):
        if not (self.env.is_superuser() or company.cas_ceo_user_id == self.env.user):
            raise AccessError(_("این عملیات فقط در اختیار مدیرعامل تعیین‌شده است."))

