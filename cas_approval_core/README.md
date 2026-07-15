# CAS Approval Core

Versioned, secure and auditable approval foundation for Odoo 19 Community.

Current module version: `19.0.1.0.2` (Foundation RC3).

## Foundation RC1 scope

- approval policies pinned to workflow version and state;
- parallel and sequential approval execution;
- unanimous (`all`) and quorum decisions;
- fixed-user, group, workflow-responsible and instance-starter resolution;
- explicit active internal approvers within the workflow company;
- assigned approver, actual decision user, role, assignment/decision/deadline times;
- mandatory rejection reason, optional comment and decision delay;
- append-only request and decision history;
- per-approver Odoo activities;
- date-bounded, company-scoped and optionally policy-scoped delegation;
- immutable delegation snapshots on decision lines and activities routed to substitutes;
- responsible/starter manager resolution through direct management and department fallback;
- guarded approve/reject transitions that cannot bypass the approval engine;
- immutable policies after workflow publication and safe revision cloning;
- company record rules, backend views and automated tests.

## Deferred

- department/job-specific role resolvers beyond the manager chain;
- absence-calendar-driven automatic delegation creation;
- reminder/escalation cron jobs and SLA dashboards;
- multi-stage return-for-correction and reopen policies;
- email/SMS templates and document signatures.

No user-entered Python, JavaScript, SQL or unrestricted domain is executed.
