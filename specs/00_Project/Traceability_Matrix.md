# ماتریس ردیابی چرخه UI تا پیاده‌سازی

| مشخصه | مقدار |
|---|---|
| وضعیت | `Active` |
| هدف | ردیابی کامل Observation تا UI Revalidation |
| مرجع | `UI_Review_Lifecycle.md` |
| آخرین چرخه فعال | `CAS UI Review Cycle 9 — Through Iteration 13` |

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

| Observation ID | Cycle/Iteration | Page / Role / Scenario | Decision ID | Page Spec / Register | Module Owner | Affected Modules | Backend Requirement | Security Reference | Change Set | Implementation | Evidence | Revalidation | Final Status | Supersedes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `OBS-UIR09-NAV-001` | UIR09 I1–I3 | Workspace / all roles / navigation | `DEC-010-UIR09-CONSOLIDATED` | `UI_Review_Cycle_9_Register.md` | Workspace | `cas_workspace`, `cas_workspace_contract` | tree navigation، parent resolution، breadcrumb، preference migration | Capability model + direct route check | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` | Gap Identified | N/A | Pending | Pending Revalidation | Flat navigation baseline |
| `OBS-UIR09-ATT-001..003` | UIR09 I4 | Attendance / employee-supervisor-auditor | `DEC-010-UIR09-CONSOLIDATED` | `UI_Review_Cycle_9_Register.md` | Attendance domain | attendance، approval/delegation | correction request/ledger، random audit، CEO escalation | ACL/Record Rule/Method/Delegation/Audit | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` | Gap Identified | N/A | Pending | Pending Revalidation | N/A |
| `OBS-UIR09-OT-001` | UIR09 I4 | Overtime / employee-supervisor | `DEC-010-UIR09-CONSOLIDATED` | `UI_Review_Cycle_9_Register.md` | Overtime domain | overtime، approval | granular capability grants and request workflow | no metadata/count leakage | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` | Gap Identified | N/A | Pending | Pending Revalidation | implicit role-only access |
| `OBS-UIR09-WR-001..002` | UIR09 I5–I7,I12–I13 | Dashboard work report / employee | `DEC-010-UIR09-CONSOLIDATED` | `UI_Review_Cycle_9_Register.md` | Work Report + Activity Catalog | `cas_work_report`, `cas_activity_catalog` | proposed activity، original label، searchable selector، custom duration | record ownership، method validation، audit | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` | Gap Identified | N/A | Pending | Pending Revalidation | standalone unknown-activity button |
| `OBS-UIR09-FORM-001` | UIR09 I7,I9 | Form Builder / form designer | `DEC-010-UIR09-CONSOLIDATED` | `UI_Review_Cycle_9_Register.md` | Form Engine | `cas_form_core`, `cas_form_builder`, `cas_dynamic_form` | activity reference fields، dynamic matrix provider/rendering | field/row/cell security، server-side pagination | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` | Gap Identified | N/A | Pending | Pending Revalidation | N/A |
| `OBS-UIR09-DASH-001..004` | UIR09 I7–I11 | Dashboard / user | `DEC-010-UIR09-CONSOLIDATED` | `UI_Review_Cycle_9_Register.md` | Workspace | `cas_workspace` | header settings، visibility، shortcuts، command center، home link | user/company scope، policy lock، capability filter | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` | Gap Identified | N/A | Pending | Pending Revalidation | Reorder-only personalization |
| `OBS-UIR09-LAYOUT-001` | UIR09 I13 | Dashboard / employee | `DEC-010-UIR09-CONSOLIDATED` | `UI_Review_Cycle_9_Register.md` | Workspace + Work Report | `cas_workspace`, `cas_work_report` | remove progress widget، full-width quick report، spacing | N/A beyond existing access | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` | Gap Identified | N/A | Pending | Pending Revalidation | Work Progress widget baseline |

## قواعد

1. ردیف بدون Observation برای تغییر UI ناقص است.
2. ردیف بدون Module Owner برای Backend ناقص است.
3. `Implemented` بدون Evidence مجاز نیست.
4. `Accepted` در Production بدون UI Revalidation مجاز نیست.
5. Cycle جدید ردیف‌های قبلی را حذف نمی‌کند.
6. تصمیم تغییرکرده باید Supersede صریح داشته باشد.
7. یک Requirement می‌تواند در چند Cycle اعتبارسنجی شود.
8. Version نرم‌افزار فقط در صورت Release واقعی ثبت می‌شود.
9. Prototype Cycle 9 شواهد تصمیم‌سازی است، نه Implementation Evidence.

## وضعیت فعلی

Cycle 9 آخرین Cycle فعال بازنگری UI است. Cycle 8 Historical Review Source باقی می‌ماند و تصمیم‌های Active آن فقط در موارد صریح Cycle 9 Supersede شده‌اند. تمام ردیف‌های Cycle 9 از نظر اجرا `Gap Identified` و از نظر UI Production برابر `Pending Revalidation` هستند.
