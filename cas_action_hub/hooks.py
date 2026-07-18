from odoo import SUPERUSER_ID, api


def post_init_hook(env):
    env = api.Environment(env.cr, SUPERUSER_ID, {})
    Rule = env["cas.action.sla.rule"]
    for company in env["res.company"].search([]):
        if not Rule.search_count([("company_id", "=", company.id)]):
            Rule.create(
                {
                    "name": "SLA پیش‌فرض کارتابل",
                    "company_id": company.id,
                    "reminder_interval_hours": 24,
                    "escalation_after_hours": 24,
                    "max_escalation_level": 3,
                }
            )
    env["cas.action.item"]._sync_all()
