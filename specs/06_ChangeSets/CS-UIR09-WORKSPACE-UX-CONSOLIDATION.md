# Change Set — UI Review Cycle 9 Workspace UX Consolidation

| مشخصه | مقدار |
|---|---|
| Document ID | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` |
| Document Type | Change Set |
| Title | CAS UI Review Cycle 9 — Through Iteration 13 |
| Status | `Active` |
| Document Version | `1.0` |
| Created At | `2026-07-21` |
| Updated At | `2026-07-21` |
| Owner | Product & Architecture Governance |
| Source UI Review Cycle | `CAS UI Review Cycle 9` |
| Source Iteration | `Through Iteration 13` |
| Effective From | `2026-07-21` |
| Supersedes | بخش‌های صریح در `REG-UIR09` |
| Domain Owner | Multiple |
| Affected Modules | Workspace, Attendance, Shift, Overtime, Work Report, Activity Catalog, Form Engine, Approval/Delegation |
| Implementation Status | `Gap Identified` |
| UI Validation Status | `Pending Revalidation` |
| Related Decisions | `DEC-010-UIR09-CONSOLIDATED` |
| Related Observations | `REG-UIR09` |

## 1. Scope

تفاوت‌های پذیرفته‌شده Cycle 9 نسبت به Baseline فعال Cycle 8، شامل Navigation، Attendance correction، delegated audit، Overtime governance، Work Report quick entry، Form Builder providers، Dashboard personalization و layout است.

## 2. Added

- Navigation tree با Submenu، collapse state و parent-to-first-authorized-child.
- Clickable breadcrumb و deterministic parent route.
- Attendance correction request و Correction Ledger مستقل.
- Delegated random audit pool و CEO escalation.
- Overtime capability grant توسط Supervisor.
- Activity proposal برای عنوان خارج از Catalog.
- Searchable activity dropdown و custom duration.
- Form Builder field providers برای Activity Category و Recurring Activity.
- Dynamic Matrix field.
- Dashboard header settings icon.
- Widget visibility، Command Center visibility و shortcut customization.

## 3. Changed

- Notification Center زیر Dashboard group قرار می‌گیرد.
- Communications دومین گروه Navigation است.
- Employee discrepancy card فقط Missing Check-in/Check-out را نشان می‌دهد.
- Late arrival در جریان جدا و قابل اتصال به Leave/Mission قرار می‌گیرد.
- Dashboard personalization از control روی Widget به پنل مرکزی منتقل می‌شود.
- Quick Work Report تمام‌عرض و کم‌تراکم‌تر می‌شود.
- Workspace brand click به Dashboard home می‌رود.

## 4. Removed

- Flat-only navigation baseline.
- دکمه مستقل «فعالیت در فهرست نیست» خارج از selector.
- پیام آشکار درباره تعداد Widgetهای مخفی.
- Work Progress widget در Cycle 9 Dashboard baseline.

## 5. Superseded

فقط موارد زیر صریحاً Supersede می‌شوند:

1. Reorder-only user dashboard personalization در Cycle 8.
2. Flat navigation برای Workspace.
3. Work Progress widget baseline.
4. External standalone unknown-activity button.

## 6. Module Impacts

| Module/Domain | Change Type | Required Work |
|---|---|---|
| `cas_workspace` | UI + preference + provider contract | Tree navigation، header settings، widget visibility، shortcuts، home link |
| `cas_workspace_contract` | Contract | Navigation node schema، settings schema، capability filtering |
| Attendance domain | Model + workflow | correction request، correction ledger، audit source |
| Shift domain | Query/integration | shift occurrence context for attendance/work report |
| Overtime domain | Security/workflow | granular capabilities، supervisor grant، request approval |
| `cas_work_report` | UI/service | proposed activity، custom duration، submission independence |
| `cas_activity_catalog` | Model/service | standardization proposal، mapping history، original label retention |
| `cas_form_builder` / `cas_form_core` | Registry/schema | new reference fields and matrix schema |
| `cas_dynamic_form` | Renderer/storage | matrix renderer، pagination، answer validation |
| `cas_approval_core` | Workflow | supervisor approval، delegation، CEO escalation |

## 7. Security Impacts

- capability-aware navigation and direct-route checks.
- no metadata/count leakage.
- correction and overtime method checks.
- delegation expiry/revocation.
- matrix provider row/column filtering.
- multi-company and organization scope.
- immutable audit trail for attendance and activity mapping.

## 8. Migration

1. Workspace preferences schema migration with safe defaults.
2. Navigation state migration from flat keys to parent/child keys.
3. No destructive migration of raw attendance logs.
4. New correction and proposal records require forward migration and rollback plan.
5. Existing Work Report activities keep original labels and may be mapped later.

## 9. Tests

- Unit: node resolution، duration validation، proposal state.
- Integration: supervisor approval to correction ledger، audit escalation، work report submission.
- Security: forbidden route، count leakage، revoked delegation، overtime capability.
- Performance: matrix server-side pagination، searchable activity catalog.
- UI: RTL، Jalali، desktop/tablet/mobile، keyboard، focus، empty/error/forbidden.
- Regression: Cycle 8 active decisions not explicitly superseded.

## 10. Revalidation Plan

Revalidation MUST run against implemented Odoo modules, not only prototype ZIP. Evidence MUST include commit/PR، automated tests، screenshots or recordings، role matrix and direct URL security checks.

## 11. Open Questions

No blocking product question remains for Cycle 9 baseline. Advanced per-widget settings and remaining CSS polish are deferred to the next UI Review Cycle.

## 12. Risks

- hardcoded role names instead of capabilities.
- raw attendance mutation.
- client-side-only matrix filtering.
- preference scope collision between user/company/role.
- claiming implementation from prototype behavior.

## 13. Rollback

- Feature flags for tree navigation and dashboard preferences.
- migration backup for preference payloads.
- correction ledger is additive and must never roll back by mutating raw logs.
- provider registry can fall back to Cycle 8 nodes during controlled rollback.
