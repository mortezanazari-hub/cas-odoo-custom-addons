# ارزیابی اثر بین‌ماژولی UI Review Cycle 9

| مشخصه | مقدار |
|---|---|
| Document ID | `MOD-IMPACT-UIR09` |
| Document Type | Cross-module Impact Assessment |
| Title | UI Review Cycle 9 Cross-module Impact |
| Status | `Active` |
| Document Version | `1.1` |
| Created At | `2026-07-21` |
| Updated At | `2026-07-21` |
| Owner | Architecture Governance |
| Source UI Review Cycle | `CAS UI Review Cycle 9` |
| Source Iteration | `Through Iteration 13` |
| Effective From | `2026-07-21` |
| Supersedes | `N/A` |
| Domain Owner | Multiple |
| Implementation Status | `Gap Identified` |
| UI Validation Status | `Pending Revalidation` |
| Related Decisions | `DEC-010-UIR09-CONSOLIDATED` |
| Related Change Sets | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` |
| Related Architecture | `ARCH-CSS-DS-001` |

## 1. اصل مالکیت

Workspace مالک Business Data نیست. `cas_workspace` فقط Shell، Navigation، Provider registry، UI preference، widget settings، transient state و Design System مشترک را مالک است.

هر Business Module مالک رفتار و Componentهای Domain خود است، اما Styleهای آن MUST از Tokenها، Primitiveها، Breakpointها و قراردادهای مشترک Workspace تبعیت کند.

## 2. Impact Matrix

| Domain | Owner | Create/Update Owner | Workspace Role | Models/Services Required | Migration | Tests |
|---|---|---|---|---|---|---|
| Navigation | `cas_workspace_contract` | `cas_workspace` config/admin services | Read/render | tree node registry، capability filter، parent resolution | preference key migration | route/capability/RTL |
| Dashboard preference | `cas_workspace` | current user within policy | Read/write preference | widget visibility، shortcut order، command center visibility | defaults and schema version | user/company lock/regression |
| Shared CSS/Design System | `cas_workspace` | architecture-governed shared assets | token/primitive consumer | token registry، shared components، asset layering، lint rules | staged stylesheet migration | lint/visual/RTL/responsive |
| UI module styles | each business module | module owner | scoped consumer | namespaced component styles based on shared primitives | remove hardcoded/legacy styles | visual regression/no leakage |
| Attendance correction | Attendance domain | employee request; supervisor approval | provider consumer | correction request، correction ledger، immutable source refs | additive schema | audit/security/workflow |
| Random audit | Attendance governance + approval | delegated reviewer | provider consumer | audit pool، sample command، CEO escalation event | additive schema | revoke/expiry/escalation |
| Shift context | Shift domain | shift planner/system | read-only consumer | occurrence query، assignment resolution | none or index | crossing-midnight/multi-assignment |
| Overtime | Overtime domain | employee/supervisor/approver | capability-aware consumer | grant، request workflow، granular capabilities | grant backfill policy | leakage/method checks |
| Work Report | `cas_work_report` | employee/reviewer | quick-entry consumer | proposed activity ref، custom duration validation | schema/index | submission/regression/layout |
| Activity Catalog | `cas_activity_catalog` | catalog steward | reference provider | proposal، mapping history، original label snapshot | additive schema | dedup/audit/concurrency |
| Form Builder | `cas_form_builder` / `cas_form_core` | authorized form designer | route consumer | field registry، provider binding، matrix schema | form revision migration | schema/security/versioning/layout |
| Dynamic Form | `cas_dynamic_form` | submission owner | renderer | matrix answer storage، validation، pagination | answer compatibility | load/field security/responsive |
| Approval/Delegation | `cas_approval_core` | authorized manager/admin | action provider | supervisor approval، grants، escalation | state migration if reused | ACL/record rule/audit |

## 3. New or Extended Entities

### 3.1 Attendance

- `attendance.correction.request`
- `attendance.correction.entry`
- `attendance.correction.audit`

Required fields include employee، occurrence/date، missing direction، proposed timestamp، requester، supervisor decision، correction entry reference، source evidence metadata، audit status and escalation reference.

### 3.2 Activity Catalog

- `activity.catalog.proposal`
- mapping history or immutable mapping event

Original label MUST remain queryable after mapping.

### 3.3 Workspace Preference

Preference payload MUST be versioned and scoped by user with optional company/role policy overlay. Company lock MUST take precedence over user preference.

### 3.4 Dynamic Matrix

Schema MUST include row provider key، row domain، column definitions، cell field type، required/readonly rules، pagination size، snapshot policy and export policy.

### 3.5 Design System Assets

`cas_workspace` MUST expose shared tokens and primitives through Odoo asset bundles. Business modules MUST declare dependency rather than importing unrelated files directly.

No Business Model is created for CSS tokens. Theme and density values MAY be persisted only as UI preferences.

## 4. Provider Contracts

Required provider keys:

- `workspace.navigation.tree`
- `workspace.dashboard.preferences`
- `attendance.employee.exceptions`
- `attendance.correction.actions`
- `attendance.correction.audit_queue`
- `overtime.self_service`
- `work_report.activity_catalog`
- `form_builder.activity_categories`
- `form_builder.recurring_activities`
- `form_builder.matrix_rows`

Each provider MUST return only authorized records and MUST NOT expose forbidden counts or labels.

## 5. CSS and Asset Contracts

All UI-producing addons MUST:

- consume `ARCH-CSS-DS-001` Design Tokenها؛
- scope selectors under CAS namespace؛
- avoid fixed inline styles and static JavaScript style mutation؛
- use shared breakpoints and logical properties؛
- avoid undocumented `!important` and broad Odoo overrides؛
- use shared primitives for fields، buttons، cards، dialogs، states and tables؛
- provide lint and visual regression evidence before conformant status.

CSS hiding is not an authorization mechanism. ACL، Record Rule and method checks remain mandatory.

## 6. Events

- `attendance.correction.requested`
- `attendance.correction.approved`
- `attendance.correction.rejected`
- `attendance.correction.audited`
- `attendance.correction.discrepancy_found`
- `attendance.correction.escalated_to_ceo`
- `activity.catalog.proposal_created`
- `activity.catalog.proposal_mapped`
- `workspace.preference_changed`

Events MUST be idempotent where they trigger external actions.

## 7. Security

- capability + ACL + Record Rule + method check.
- purpose-aware organization scope.
- no broad `sudo()`.
- delegation expiry and revocation checked at command time.
- matrix serialization after permission filtering.
- attachment access inherited from owning business record.
- secure export and audit retention.
- hidden UI does not weaken direct-route or RPC security.

## 8. Performance

- searchable Activity Catalog MUST use server-side search and limit.
- Matrix MUST use pagination/virtualization; full employee dataset client-side loading is prohibited.
- navigation provider may cache only permission-safe results and MUST invalidate on role/capability/company change.
- shared CSS MUST avoid duplicate component implementations and costly broad selectors.
- Odoo asset load order MUST prevent layout shift and uncontrolled cascade leakage.

## 9. Failure Modes

- unavailable provider → explicit `Unavailable` state, no fabricated data.
- partial provider failure → remaining widgets render with scoped error.
- revoked delegation during open page → command denied and UI refreshed.
- concurrent activity mapping → deterministic conflict handling and preserved original proposal.
- approval event retry → idempotency key prevents duplicate correction entries.
- missing shared token/primitive → asset build or lint failure; module must not silently hardcode fallback values.
- Odoo upgrade breaks override → regression test fails and override remains blocked until reviewed.

## 10. Migration Sequence for CSS Compliance

1. inventory current CSS/SCSS/XML inline styles and JavaScript style mutations؛
2. identify duplicate visual primitives and hardcoded tokens؛
3. create shared tokens/foundation/components in `cas_workspace`؛
4. migrate Workspace surfaces without visual redesign؛
5. migrate each business module incrementally؛
6. retain deprecated classes only for a documented transition window؛
7. remove legacy selectors after visual regression and downstream verification.

## 11. Acceptance

This assessment becomes implementation-ready only after module-level APIs، model constraints، migration scripts، test plans and CSS compliance plans are added to each affected module specification. Current status remains `Gap Identified`.
