# CAS Workflow Core

Versioned, secure and auditable workflow foundation for Odoo 19 Community.

Current module version: `19.0.1.0.2` (Foundation RC3).

## Version 1.0 scope

- stable workflow definition and immutable published revisions;
- initial, normal, final and cancelled states;
- guarded transitions with group-based permission;
- safe structured condition placeholder without Python or JavaScript code;
- generic binding through an allowed `ir.model` and numeric resource id;
- version-pinned runtime instances;
- current responsible user and state deadline;
- explicit active responsibility for technical/test execution paths;
- append-only transition history with actor, time and note;
- company isolation, manager visibility and personal runtime visibility;
- backend tests and deployment verification.

## Deferred to extensions

- parallel, unanimous and quorum approvals (`cas_approval_core`);
- delegation, absence and substitutes;
- conditional expression builder and automatic transitions;
- notification/action engine and scheduled escalation;
- graphical workflow designer;
- work-report-specific supervisor resolution.

Published workflow schemas never execute arbitrary Python, JavaScript, SQL or
unrestricted domains.

Runtime validation rejects missing, nonexistent or inactive responsible users.
Interactive callers may omit the responsible user only when the current Odoo
user is a real active user; technical execution must always pass it explicitly.
