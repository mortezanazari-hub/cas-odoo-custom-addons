# CAS Internal Correspondence

Foundation module for secure internal organizational correspondence on Odoo 19 Community.

## RC1 scope

- Company-wide letter numbering assigned only on formal send.
- Internal recipients and copies addressed to users or departments.
- Information, action and formal-reply expectations per recipient.
- System signature snapshot, confidentiality, priority and deadlines.
- Immutable sent letters, view receipts, referrals, relations and audit events.
- Formal replies as independently numbered letters with a preserved thread.
- Corrective replacement letters instead of hidden edits.
- Date-bounded, revocable secretariat delegation controlled by the configured CEO.
- Structural manager, participant, secretariat and multi-company access controls.
- Odoo activities for pending recipient and referral actions.
- Source-side descriptor contract for a future `cas_action_hub` connector.

External mail, incoming/outgoing physical mail, OCR, digital signature, PDF rendering,
Nextcloud and Action Hub projection are intentionally outside RC1.

## Operational setup

1. Assign the correspondence user group to internal users.
2. Configure one correspondence CEO on every participating company.
3. Complete employee/user/department mappings and department managers.
4. Review the automatically created company sequence after the first formal send.
5. Grant secretariat access only through dated delegation records.

No operational users, departments, letters or sample records are seeded by this module.
