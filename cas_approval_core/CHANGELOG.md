# CAS Approval Core changelog

## 19.0.1.0.2 — Foundation RC3

- add date-bounded, company-scoped and optional policy-scoped delegation;
- route activities to the substitute while preserving assigned and actual users;
- freeze used delegation records for audit integrity;
- reject overlapping delegation ranges;
- resolve direct/higher employee managers with department-manager fallback;
- add HR-backed security, views and transactional regression tests.

## 19.0.1.0.1 — Foundation RC2

- execute private request aggregation and activity synchronization with controlled
  engine privileges after the acting user's decision permission is validated;
- preserve per-approver record rules while allowing quorum completion to cancel
  remaining decision lines and activities safely.

## 19.0.1.0.0 — Foundation RC1

- introduce versioned approval policies and approver steps;
- add parallel/sequential and all/quorum runtime decisions;
- create explicit decision lines, activities and immutable audit history;
- protect workflow transitions from approval bypass;
- clone approval schemas with workflow revisions;
- add company security, backend views and transactional tests.
