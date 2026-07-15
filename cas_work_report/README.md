# CAS Daily Work Reports

Typed daily work reports for Odoo 19 Community.

## Foundation scope

- Daily reports linked to real `hr.employee`, department and company records.
- Configurable work stations independent from the employee's organizational unit.
- Shift start/end, normal hours, overtime and a hard 12-hour submission deadline.
- Self-entry, managerial entry and explicit department/company representation permissions.
- Server-enforced visibility for the employee, submitter, station supervisor and every
  direct/indirect manager in the organizational chain.
- Formal supervisor approval through `cas_workflow_core` and `cas_approval_core`.
- Automatic, audited approval when the employee's direct manager creates the report.
- Filtered XLSX export that respects record rules.
- Permanent tracking number, chatter and immutable workflow/approval history.

Missing-report detection, a full shift-management module and PDF output are intentionally
outside this foundation release.
