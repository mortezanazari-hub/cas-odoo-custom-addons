# ماتریس ردیابی چرخه UI تا پیاده‌سازی

| مشخصه | مقدار |
|---|---|
| وضعیت | `Active` |
| هدف | ردیابی کامل Observation تا UI Revalidation |
| مرجع | `UI_Review_Lifecycle.md` |
| آخرین چرخه فعال | `CAS UI Review Cycle 10 — Through Iteration 13` |

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
| `OBS-UIR09-NAV-001` | UIR09 I1–I3 | Workspace / all roles / navigation | `DEC-010-UIR09-CONSOLIDATED` | `UI_Review_Cycle_9_Register.md` | Workspace | `cas_workspace`, `cas_workspace_contract` | tree navigation، parent resolution، breadcrumb، preference migration | Capability model + direct route check | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` | Gap Identified | N/A | Pending | Pending Revalidation | Flat navigation baseline |
| `OBS-UIR09-ATT-001..003` | UIR09 I4 | Attendance / employee-supervisor-auditor | `DEC-010-UIR09-CONSOLIDATED` | `UI_Review_Cycle_9_Register.md` | Attendance domain | attendance، approval/delegation | correction request/ledger، random audit، CEO escalation | ACL/Record Rule/Method/Delegation/Audit | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` | Gap Identified | N/A | Pending | Pending Revalidation | N/A |
| `OBS-UIR09-OT-001` | UIR09 I4 | Overtime / employee-supervisor | `DEC-010-UIR09-CONSOLIDATED` | `UI_Review_Cycle_9_Register.md` | Overtime domain | overtime، approval | granular capability grants and request workflow | no metadata/count leakage | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` | Gap Identified | N/A | Pending | Pending Revalidation | implicit role-only access |
| `OBS-UIR09-WR-001..002` | UIR09 I5–I7,I12–I13 | Dashboard work report / employee | `DEC-010-UIR09-CONSOLIDATED` | `UI_Review_Cycle_9_Register.md` | Work Report + Activity Catalog | `cas_work_report`, `cas_activity_catalog` | proposed activity، original label، searchable selector، custom duration | record ownership، method validation، audit | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` | Gap Identified | N/A | Pending | Pending Revalidation | standalone unknown-activity button |
| `OBS-UIR09-FORM-001` | UIR09 I7,I9 | Form Builder / form designer | `DEC-010-UIR09-CONSOLIDATED` | `UI_Review_Cycle_9_Register.md` | Form Engine | `cas_form_core`, `cas_form_builder`, `cas_dynamic_form` | activity reference fields، dynamic matrix provider/rendering | field/row/cell security، server-side pagination | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` | Gap Identified | N/A | Pending | Pending Revalidation | N/A |
| `OBS-UIR09-DASH-001..004` | UIR09 I7–I11 | Dashboard / user | `DEC-010-UIR09-CONSOLIDATED` | `UI_Review_Cycle_9_Register.md` | Workspace | `cas_workspace` | header settings، visibility، shortcuts، command center، home link | user/company scope، policy lock، capability filter | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` | Gap Identified | N/A | Pending | Pending Revalidation | Reorder-only personalization |
| `OBS-UIR09-LAYOUT-001` | UIR09 I13 | Dashboard / employee | `DEC-010-UIR09-CONSOLIDATED` | `UI_Review_Cycle_9_Register.md` | Workspace + Work Report | `cas_workspace`, `cas_work_report` | remove progress widget، full-width quick report، spacing | `ARCH-CSS-DS-001` + existing access controls | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` | Gap Identified | N/A | Pending | Pending Revalidation | Work Progress widget baseline |
| `OBS-UIR09-CSS-001` | UIR09 documentation hardening | All UI surfaces / maintainability | `DEC-010-UIR09-CONSOLIDATED` | `UI_Review_Cycle_9_Register.md` + CSS contract | Workspace Design System | all UI-producing addons | token registry، shared primitives، asset layering، lint and visual regression | `ARCH-CSS-DS-001` | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` | Gap Identified | Documentation commits | Pending | Pending Revalidation | implicit CSS practices |

## Cycle 10 Traceability

| Observation ID | Cycle/Iteration | Page / Role / Scenario | Decision ID | Page Spec / Register | Module Owner | Affected Modules | Backend Requirement | Security / Architecture Reference | Change Set | Implementation | Evidence | Revalidation | Final Status | Supersedes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `OBS-UIR10-CORR-001` | UIR10 I1–I2 | Correspondence / sender-recipient / delegated send and action request | `DEC-016-UIR10-CONSOLIDATED` | `UI_Review_Cycle_10_Register.md` | Correspondence | correspondence, delegation, tasks, workspace | official sender/actual actor، action request، receiver task decision، print/PDF access | principal/actor audit، delegation method check، export security | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` | Gap Identified | Prototype only; not implementation evidence | Cycle 10 post-implementation | Pending Revalidation | conflicting prototype behavior only |
| `OBS-UIR10-DELEG-001` | UIR10 I3–I8 | Delegation / user and admin | `DEC-016-UIR10-CONSOLIDATED` | `../02_UI_UX/Employee/Delegation.md` | Delegation domain | delegation providers, correspondence, tasks, approvals, work reports | principal fixed for public form، admin scope، domain capabilities، validity، decree، revocation | ACL/Record Rule/Method/Scope/Audit/Impersonation | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` | Gap Identified | N/A | Cycle 10 post-implementation | Pending Revalidation | generic mixed delegation form |
| `OBS-UIR10-PEOPLE-001` | UIR10 I4,I12 | Shared picker / all consumers / single-multiple selection | `DEC-016-UIR10-CONSOLIDATED` | `../02_UI_UX/Common/Shared_People_Picker.md` | Workspace shared components | workspace + HR/organization providers | shared provider contract، normalized IDs، cumulative selection، chip removal، filtering | search/count/metadata leakage، ID tampering، scoped cache | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` | Gap Identified | Prototype interaction evidence only | Cycle 10 post-implementation | Pending Revalidation | duplicated person selectors |
| `OBS-UIR10-ADMIN-001` | UIR10 I9 | Admin center / system administrators | `DEC-016-UIR10-CONSOLIDATED` | `UI_Review_Cycle_10_Register.md` | Security governance | security groups, workspace | granular admin groups and composite super-admin | least privilege، SoD، audit viewer read-only | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` | Gap Identified | N/A | Cycle 10 post-implementation | Pending Revalidation | absolute system-admin group concept |
| `OBS-UIR10-SEC-001` | UIR10 I10 | Secretariat / administrative specialist | `DEC-016-UIR10-CONSOLIDATED` | `../02_UI_UX/Administrative/Secretariat.md` | Secretariat Registry | correspondence, secretariat, workspace, attachments | incoming/outgoing models or extensions، sequences، delivery status، register reports | sequence authorization، export/attachment security، append-only corrections | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` | Gap Identified | N/A | Cycle 10 post-implementation | role-title secretariat and manual numbering baselines |
| `OBS-UIR10-GUARD-001` | UIR10 I11–I12 | Guard attendance / guard operator / rapid batch entry | `DEC-016-UIR10-CONSOLIDATED` | `../02_UI_UX/Security/Guard_Attendance_Station.md` | Attendance Operations | `cas_attendance_operations`, `cas_attendance_core`, workspace | UX over existing batch/event models، manual time audit، conflicts، recent log | site/company scope، direct RPC، append-only event، duplicate control | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` | Gap Identified | Existing model docs + prototype; no implementation evidence | Cycle 10 post-implementation | Pending Revalidation | list-oriented guard registration UI |
| `OBS-UIR10-SCOPE-001` | UIR10 I10–I13 | Alpha scope / all roles | `DEC-016-UIR10-CONSOLIDATED` | `../07_Out_Of_Scope/V10_Alpha_Out_Of_Scope.md` | Product Governance | workspace, OCR references, document management | remove OCR/DMS menu-route-product dependencies while retaining attachment | attachment access and no parallel repository | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` | Planned Removal / Gap Identified | N/A | Cycle 10 post-implementation | OCR/DMS alpha presence |

## قواعد

1. ردیف بدون Observation برای تغییر UI ناقص است.
2. ردیف بدون Module Owner برای Backend ناقص است.
3. `Implemented` بدون Evidence مجاز نیست.
4. `Accepted` در Production بدون UI Revalidation مجاز نیست.
5. Cycle جدید ردیف‌های قبلی را حذف نمی‌کند.
6. تصمیم تغییرکرده باید Supersede صریح داشته باشد.
7. Prototype شواهد تصمیم‌سازی است، نه Implementation Evidence.
8. Documentation commit فقط Evidence مستندسازی است.

## وضعیت فعلی

Cycle 10 آخرین Cycle فعال بازنگری UI است. Cycleهای 8 و 9 Historical Review Source باقی می‌مانند و تصمیم‌های Active آن‌ها فقط در موارد صریح Cycle 10 Supersede شده‌اند. تمام ردیف‌های Cycle 10 از نظر اجرا `Gap Identified` یا `Planned Removal` و از نظر UI Production برابر `Pending Revalidation` هستند.
