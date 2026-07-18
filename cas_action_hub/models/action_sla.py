from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CasActionSlaRule(models.Model):
    _name = "cas.action.sla.rule"
    _description = "CAS Action Hub SLA Rule"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    name = fields.Char(string="عنوان", required=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True
    )
    source_adapter = fields.Char(
        string="آداپتر منبع", help="در صورت خالی‌بودن برای همه منابع اعمال می‌شود."
    )
    action_type = fields.Selection(
        selection=lambda self: self.env["cas.action.item"]._fields["action_type"].selection,
        string="نوع اقدام",
        help="در صورت خالی‌بودن برای همه انواع اقدام اعمال می‌شود.",
    )
    reminder_interval_hours = fields.Float(
        string="فاصله یادآوری (ساعت)", required=True, default=24.0
    )
    escalation_after_hours = fields.Float(
        string="تصعید پس از سررسید (ساعت)", required=True, default=24.0
    )
    max_escalation_level = fields.Integer(string="حداکثر سطح تصعید", required=True, default=3)
    escalation_user_id = fields.Many2one(
        "res.users", string="مسئول تصعید ثابت", ondelete="restrict"
    )

    @api.constrains(
        "reminder_interval_hours", "escalation_after_hours", "max_escalation_level", "company_id", "escalation_user_id"
    )
    def _check_contract(self):
        for rule in self:
            if rule.reminder_interval_hours <= 0 or rule.escalation_after_hours < 0:
                raise ValidationError(_("فواصل SLA باید معتبر و نامنفی باشند."))
            if rule.max_escalation_level < 0:
                raise ValidationError(_("حداکثر سطح تصعید نمی‌تواند منفی باشد."))
            if rule.escalation_user_id and rule.company_id not in rule.escalation_user_id.company_ids:
                raise ValidationError(_("مسئول تصعید باید عضو شرکت قانون SLA باشد."))

    @api.model
    def _for_item(self, item):
        return self.sudo().search(
            [
                ("active", "=", True),
                ("company_id", "=", item.company_id.id),
                "|",
                ("source_adapter", "=", False),
                ("source_adapter", "=", item.source_adapter),
                "|",
                ("action_type", "=", False),
                ("action_type", "=", item.action_type),
            ],
            order="source_adapter desc, action_type desc, sequence, id",
            limit=1,
        )
