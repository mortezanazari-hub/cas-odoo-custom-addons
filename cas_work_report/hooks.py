from odoo import SUPERUSER_ID, api


WORKFLOW_CODE = "cas_daily_work_report"


def post_init_hook(env):
    env = api.Environment(env.cr, SUPERUSER_ID, {})
    Definition = env["cas.workflow.definition"]
    existing = Definition.search(
        [("code", "=", WORKFLOW_CODE), ("company_id", "=", env.company.id)], limit=1
    )
    if existing:
        return

    target_model = env["ir.model"]._get("cas.work.report")
    definition = Definition.create(
        {
            "name": "گردش تأیید گزارش کار روزانه",
            "code": WORKFLOW_CODE,
            "company_id": env.company.id,
            "owner_user_id": SUPERUSER_ID,
            "target_model_id": target_model.id,
        }
    )
    version = env["cas.workflow.version"].create(
        {
            "definition_id": definition.id,
            "name": "نسخه ۱",
            "revision": 1,
            "notes": "پیکربندی پایه گزارش کار روزانه",
        }
    )
    draft = env["cas.workflow.state"].create(
        {"version_id": version.id, "name": "پیش‌نویس", "code": "draft", "kind": "initial", "sequence": 10}
    )
    pending = env["cas.workflow.state"].create(
        {"version_id": version.id, "name": "در انتظار تأیید", "code": "pending", "kind": "normal", "sequence": 20, "sla_hours": 12}
    )
    approved = env["cas.workflow.state"].create(
        {"version_id": version.id, "name": "تأییدشده", "code": "approved", "kind": "final", "sequence": 30}
    )
    rejected = env["cas.workflow.state"].create(
        {"version_id": version.id, "name": "ردشده", "code": "rejected", "kind": "cancelled", "sequence": 40}
    )
    submit = env["cas.workflow.transition"].create(
        {"version_id": version.id, "name": "ارسال برای تأیید", "code": "submit", "from_state_id": draft.id, "to_state_id": pending.id, "sequence": 10}
    )
    approve = env["cas.workflow.transition"].create(
        {"version_id": version.id, "name": "تأیید نهایی", "code": "approve", "from_state_id": pending.id, "to_state_id": approved.id, "sequence": 20}
    )
    reject = env["cas.workflow.transition"].create(
        {"version_id": version.id, "name": "رد گزارش", "code": "reject", "from_state_id": pending.id, "to_state_id": rejected.id, "sequence": 30, "note_required": True}
    )
    policy = env["cas.approval.policy"].create(
        {
            "version_id": version.id,
            "name": "تأیید سرپرست گزارش کار",
            "code": "supervisor_approval",
            "state_id": pending.id,
            "approve_transition_id": approve.id,
            "reject_transition_id": reject.id,
            "execution_mode": "parallel",
            "decision_rule": "all",
            "quorum_count": 1,
        }
    )
    env["cas.approval.step"].create(
        {
            "policy_id": policy.id,
            "name": "تأیید سرپرست شیفت یا خط",
            "role_label": "سرپرست کار",
            "approver_type": "workflow_responsible",
            "sequence": 10,
            "deadline_hours": 12,
        }
    )
    version.action_publish()
