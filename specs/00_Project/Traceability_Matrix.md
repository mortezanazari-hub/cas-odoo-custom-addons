---
document_id: REG-TRACE-001
title: UI Review to Implementation Traceability Matrix
document_type: Traceability Matrix
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Product, Architecture & QA Governance
domain_owner: Traceability Governance
created_at: N/A
updated_at: 2026-07-22
canonical: true
supersedes: []
superseded_by: []
related_decisions: []
related_modules: []
related_pages: []
related_capabilities: []
---

# ماتریس ردیابی چرخه UI تا پیاده‌سازی

## Registryهای مکمل

- [Decision Registry](Decision_Registry.md)
- [Capability Registry](Capability_Registry.md)
- [Page Registry](Page_Registry.md)
- [Module Registry](Module_Registry.md)
- [Implementation Gap Registry](Implementation_Gap_Registry.md)
- [Open Item Registry](Open_Item_Registry.md)

آخرین چرخه فعال: `CAS UI Review Cycle 10 — Through Iteration 13`.

## مسیر اجباری

```text
UI Observation
→ Decision
→ Page Specification
→ Module Impact
→ Backend Requirement
→ Architecture/Security
→ Implementation
→ Test Evidence
→ UI Revalidation
→ Accepted / Reopened
```

## ستون‌های اجباری

| ستون | توضیح |
|---|---|
| Observation ID | مشاهده منبع |
| UI Review Cycle | Cycle و Iteration |
| Page / Role / Scenario | محل کشف |
| Decision ID | تصمیم حاصل |
| Page Spec | سند UI |
| Module Owner | مالک Domain |
| Affected Modules | ماژول‌های متأثر |
| Backend Requirement | تغییر دقیق |
| Security Reference | امنیت |
| Change Set | بسته تغییر |
| Implementation Status | وضعیت اجرا |
| Implementation Evidence | PR/Commit/Ticket |
| Test Evidence | شواهد آزمون |
| Revalidation Cycle | Cycle بازآزمایی |
| Revalidation Result | نتیجه |
| Final Status | Accepted/Reopened |
| Supersedes | تصمیم قبلی |

## Cycle 9 Traceability

| Observation ID | Cycle/Iteration | Page / Role / Scenario | Decision ID | Page Spec / Register | Module Owner | Affected Modules | Backend Requirement | Security / Architecture Reference | Change Set | Implementation | Evidence | Revalidation | Final Status | Supersedes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `OBS-UIR09-NAV-001` | UIR09 I1–I3 | Workspace / all roles / navigation | `DEC-UIR09-010-CONSOLIDATED` | Cycle 9 Register | Workspace | `cas_workspace`, workspace contract | tree navigation، parent resolution، breadcrumb، preference migration | Capability model + direct route check | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` | Gap Identified | N/A | Pending | Pending Revalidation | Flat navigation baseline |
| `OBS-UIR09-ATT-001..003` | UIR09 I4 | Attendance / employee-supervisor-auditor | `DEC-UIR09-010-CONSOLIDATED` | Cycle 9 Register؛ Page Specs pending | Attendance domain | attendance، approval/delegation | correction request/ledger، random audit، CEO escalation | ACL/Record Rule/Method/Delegation/Audit | همان | Gap Identified | N/A | Pending | Pending Revalidation | N/A |
| `OBS-UIR09-OT-001` | UIR09 I4 | Overtime / employee-supervisor | `DEC-UIR09-010-CONSOLIDATED` | Page Spec pending | Overtime domain | overtime، approval | granular capabilities and request workflow | no metadata/count leakage | همان | Gap Identified | N/A | Pending | Pending Revalidation | implicit role-only access |
| `OBS-UIR09-WR-001..002` | UIR09 I5–I7,I12–I13 | Dashboard work report / employee | `DEC-UIR09-010-CONSOLIDATED` | `Dynamic_Work_Report.md` | Work Report + Activity Catalog | `cas_work_report`, activity catalog | proposed activity، original label، searchable selector، custom duration | ownership، method validation، audit | همان | Gap Identified | N/A | Pending | Pending Revalidation | standalone unknown-activity button |
| `OBS-UIR09-FORM-001` | UIR09 I7,I9 | Form Builder / designer | `DEC-UIR09-010-CONSOLIDATED` | Page Spec pending | Form Engine | form core/builder/dynamic form | activity reference fields، dynamic matrix | field/row/cell security، server-side pagination | همان | Gap Identified | N/A | Pending | Pending Revalidation | N/A |
| `OBS-UIR09-DASH-001..004` | UIR09 I7–I11 | Dashboard / user | `DEC-UIR09-010-CONSOLIDATED` | Workspace/Dashboard specs | Workspace | `cas_workspace` | header settings، visibility، shortcuts، command center، home link | user/company scope، policy lock، capability filter | همان | Gap Identified | N/A | Pending | Pending Revalidation | Reorder-only personalization |
| `OBS-UIR09-LAYOUT-001` | UIR09 I13 | Dashboard / employee | `DEC-UIR09-010-CONSOLIDATED` | Workspace/Work Report | Workspace + Work Report | workspace/work report | remove progress widget، full-width quick report، spacing | CSS contract + access controls | همان | Gap Identified | N/A | Pending | Pending Revalidation | Work Progress baseline |
| `OBS-UIR09-CSS-001` | UIR09 hardening | All UI surfaces | `DEC-UIR09-010-CONSOLIDATED` | CSS contract | Workspace Design System | all UI addons | tokens، primitives، asset layering، lint/visual regression | `ARCH-CSS-DS-001` | همان | Gap Identified | Documentation commits only | Pending | Pending Revalidation | implicit CSS practices |

## Cycle 10 Traceability

| Observation ID | Cycle/Iteration | Page / Role / Scenario | Decision ID | Page Spec / Register | Module Owner | Affected Modules | Backend Requirement | Security / Architecture Reference | Change Set | Implementation | Evidence | Revalidation | Final Status | Supersedes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `OBS-UIR10-CORR-001` | UIR10 I1–I2 | Correspondence / delegated send/action request | `DEC-UIR10-016-CONSOLIDATED` | Cycle 10 Register؛ detailed backlinks pending | Correspondence | correspondence/delegation/tasks/workspace | official sender/actor، action request، receiver task decision، print/PDF | principal/actor audit، delegation check، export security | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` | Gap Identified | Prototype only | Post-implementation | Pending Revalidation | conflicting prototype behavior only |
| `OBS-UIR10-DELEG-001` | UIR10 I3–I8 | Delegation / user-admin | `DEC-UIR10-016-CONSOLIDATED` | `Employee/Delegation.md` | Delegation domain | delegation providers + consumers | principal fixed، admin scope، capabilities، validity، decree، revocation | ACL/Record Rule/Method/Scope/Audit/Impersonation | همان | Gap Identified | N/A | Post-implementation | Pending Revalidation | generic mixed form |
| `OBS-UIR10-PEOPLE-001` | UIR10 I4,I12 | Shared picker / consumers | `DEC-UIR10-016-CONSOLIDATED` | `Common/Shared_People_Picker.md` | Shared components | workspace + HR/org providers | shared contract، normalized IDs، cumulative selection، chip removal، filtering | search/count/metadata leakage، ID tampering، scoped cache | همان | Gap Identified | Prototype interaction only | Post-implementation | Pending Revalidation | duplicated selectors |
| `OBS-UIR10-ADMIN-001` | UIR10 I9 | Admin center | `DEC-UIR10-016-CONSOLIDATED` | Page Specs pending | Security governance | groups/workspace | granular admin groups + composite admin | least privilege، SoD، audit viewer read-only | همان | Gap Identified | N/A | Post-implementation | Pending Revalidation | absolute admin concept |
| `OBS-UIR10-SEC-001` | UIR10 I10 | Secretariat / administrative specialist | `DEC-UIR10-016-CONSOLIDATED` | `Administrative/Secretariat.md` | Secretariat Registry | correspondence/secretariat/workspace/attachments | incoming/outgoing، sequences، delivery، reports | sequence authorization، export/attachment security، append-only correction | همان | Gap Identified | N/A | Post-implementation | Pending Revalidation | title/manual numbering baselines |
| `OBS-UIR10-GUARD-001` | UIR10 I11–I12 | Guard attendance / rapid batch | `DEC-UIR10-016-CONSOLIDATED` | `Security/Guard_Attendance_Station.md` | Attendance Operations | attendance operations/core/workspace | UX over batch/event، manual time audit، conflicts، recent log | site/company scope، direct RPC، append-only، duplicate control | همان | Partially Implemented / Gap Identified | Existing models + prototype; no final implementation evidence | Post-implementation | Pending Revalidation | list-oriented UI |
| `OBS-UIR10-SCOPE-001` | UIR10 I10–I13 | Alpha scope | `DEC-UIR10-016-CONSOLIDATED` | `V10_Alpha_Out_Of_Scope.md` | Product Governance | workspace/document references | remove OCR/DMS product surfaces; retain attachment | attachment access؛ no parallel repository | همان | Planned Removal / Gap Identified | N/A | Post-implementation | Pending Revalidation | OCR/DMS alpha presence |

## Documentation Governance Traceability

| Change | Source | Decision | Scope | Evidence | Status |
|---|---|---|---|---|---|
| Registry and navigation unification | Documentation Audit | No new product decision | `specs` only | branch commits + `CS-SPECS-GOVERNANCE-UNIFICATION` | In Development / review required |
| ID collision handling | Audit `DEC-010/016` | No Rename decision | Registry keys + migration map | Metadata Standard | Triaged |
| Index alignment to Cycle 10 | Constitution/Version History | Existing Cycle 10 authority | Section indexes | branch diff | In Development |

## قواعد

1. ردیف بدون Observation برای تغییر UI ناقص است.
2. ردیف بدون Module Owner برای Backend ناقص است.
3. `Implemented` بدون Evidence مجاز نیست.
4. `Accepted in Production` بدون UI Revalidation مجاز نیست.
5. Cycle جدید ردیف‌های قبلی را حذف نمی‌کند.
6. تصمیم تغییرکرده باید Supersede صریح داشته باشد.
7. Prototype شواهد تصمیم‌سازی است، نه Implementation Evidence.
8. Registryها Index هستند و Source Document مرجع تفصیلی باقی می‌ماند.
