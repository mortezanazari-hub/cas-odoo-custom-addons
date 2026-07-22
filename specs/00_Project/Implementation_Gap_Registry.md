---
document_id: REG-GAP-001
title: CAS Implementation Gap Registry
document_type: Implementation Gap Registry
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Architecture & Delivery Governance
domain_owner: Implementation Governance
created_at: 2026-07-22
updated_at: 2026-07-22
canonical: true
supersedes: []
superseded_by: []
related_decisions: [DEC-UIR09-010-CONSOLIDATED, DEC-UIR10-016-CONSOLIDATED]
related_modules: []
related_pages: []
related_capabilities: []
---

# رجیستری مرکزی Gapهای اجرا

Gap اختلاف میان Requirement/Decision فعال و وضعیت فعلی کد یا UI است. Gap دلیل تضعیف Requirement نیست.

## ۱. Gapهای Cycle 8 و پایه معماری

| Gap ID | Requirement/Decision | نوع | رفتار/وضعیت فعلی مستند | رفتار مورد انتظار | Owner Module/Domain | شدت | وابستگی | معیار پذیرش خلاصه | Implementation | Revalidation |
|---|---|---|---|---|---|---|---|---|---|---|
| `GAP-WORKSPACE-CONTRACT-001` | Provider-based Workspace | Architecture/API | Contract مفهومی Consolidated؛ نام/API نهایی باز | Contract versioned مستقل از UI runtime | Workspace Contract | High | `OPEN-TECH-001/002` | Provider بدون import مستقیم Domain، permission-aware و failure-isolated | Gap Identified | Pending Revalidation |
| `GAP-PERSONAL-TASK-001` | `DEC-V8-012` | Module/Model | مالکیت مصوب؛ presence/implementation کامل تأیید نشده | Personal Task/Category مستقل با provider | `cas_personal_task` | Medium | Workspace contract | CRUD و security و Calendar self-task pass | Gap Identified | Pending Revalidation |
| `GAP-ORG-SCOPE-001` | Organization Scope shared resolver | Model/Security | Specification موجود؛ integration evidence کامل نیست | effective-dated scope مشترک، purpose-aware و fail-closed | `cas_organization_core` | Critical | HR/employee | cross-company و direct RPC tests pass | Gap Identified | Pending Revalidation |
| `GAP-WORK-REPORT-DYNAMIC-001` | `DEC-017/019/020` | Model/Workflow/Data | ماژول موجود ولی Dynamic/Shift/Profile/Section/Grant target کامل نیست | report per Shift Occurrence با composite sections و form version pinning | `cas_work_report` | Critical | Form/Workflow/Approval/Shift/Org | migration، section security، overnight shift و grant tests pass | Gap Identified | Pending Revalidation |
| `GAP-NOTIFICATION-001` | Odoo notification reuse | Integration | Gap Odoo 19 هنوز verify نشده | reuse Mail/Discuss/Bus و extension فقط برای Gap واقعی | Odoo adapter/Workspace | High | `OPEN-TECH-004` | no parallel message/bus؛ deep link and permission tests | Not Assessed | Pending Revalidation |
| `GAP-CSS-DS-001` | CSS/Design System Contract | UI/Test | Contract فعال؛ implementation evidence همه addonها موجود نیست | tokens، namespace، shared primitives، visual regression | UI addon owners | Medium | Real Odoo build | RTL/responsive/zoom/visual regression pass | Gap Identified | Pending Revalidation |

## ۲. Gapهای Cycle 9

| Gap ID | Observation/Decision | نوع | Current | Expected | Owner | شدت | Acceptance | Status |
|---|---|---|---|---|---|---|---|---|
| `GAP-WORKSPACE-NAV-001` | `OBS-UIR09-NAV-001` | UI/API/Migration | baseline تخت یا اسناد/Preferenceهای قدیمی | Navigation tree، parent resolution، breadcrumb و capability filtering | `cas_workspace` / contract | High | direct route forbidden، parent opens first allowed child، preference migration | Gap Identified |
| `GAP-ATT-CORRECTION-001` | `OBS-UIR09-ATT-001/002` | Model/Workflow/Audit | correction flow و Page Spec کامل نشده | Employee request → supervisor approval → correction ledger؛ raw log immutable | Attendance/Kardex | Critical | no raw log rewrite؛ audit and recalculation evidence | Gap Identified |
| `GAP-ATT-RANDOM-AUDIT-001` | `OBS-UIR09-ATT-003` | Security/Workflow | delegated random audit implementation evidence ندارد | time-bound capability/grant، random/manual sample، CEO escalation | Attendance/Security | Critical | revoke immediate؛ mismatch creates CEO route | Gap Identified |
| `GAP-OVERTIME-CAP-001` | `OBS-UIR09-OT-001` | Security/UI | access ممکن است role/menu-oriented باشد | four independent capabilities + method checks + no leakage | Overtime/Kardex | Critical | menu/search/count/direct route protected | Gap Identified |
| `GAP-WR-ACTIVITY-PROPOSAL-001` | `OBS-UIR09-WR-001` | Model/UI/Audit | unknown activity flow target کامل نیست | submit continues، original label و mapping history محفوظ | Work Report + Activity Catalog | High | proposal does not block submission; audit preserved | Gap Identified |
| `GAP-FORM-PROVIDERS-001` | `OBS-UIR09-FORM-001` | Form/API/Performance | Field types target در Decision ثبت شده | activity refs و dynamic matrix با provider/pagination/snapshot/security | Form Builder/Core/Dynamic Form | High | large dataset server-side؛ row/column/cell filtering | Gap Identified |
| `GAP-DASH-PREF-001` | `OBS-UIR09-DASH-001..004` | UI/Preference/Migration | v8 reorder-only baseline و UIهای قدیمی | header settings، visibility، shortcuts، command center toggle، home link | `cas_workspace` | Medium | user/company scope و company lock pass | Gap Identified |
| `GAP-DASH-LAYOUT-001` | `OBS-UIR09-LAYOUT-001` | UI | Work Progress/width baselineهای قدیمی | remove Work Progress؛ Quick Report full-width | Workspace + Work Report | Low | target layout pass at supported breakpoints | Gap Identified |

## ۳. Gapهای Cycle 10

| Gap ID | Observation | نوع | Current | Expected | Owner | شدت | وابستگی | Acceptance Reference | Status |
|---|---|---|---|---|---|---|---|---|---|
| `GAP-CORR-C10-001` | `OBS-UIR10-CORR-001` | Model/Security/UI | official sender/actor و action request flow کامل نیست | principal/actor audit، request action بدون auto-task، receiver decision، secure print/PDF | Correspondence | High | Delegation/People Picker | [Alpha Acceptance](../05_Acceptance/V10_Alpha_Acceptance_Criteria.md) | Gap Identified |
| `GAP-DELEGATION-C10-001` | `OBS-UIR10-DELEG-001` | Module/Model/Security | placement و provider contract نهایی نشده | principal/agent/domain/capability/validity/decree/state/revocation/audit | Delegation Domain | Critical | `OPEN-UIR10-007/OPEN-TECH-011` | Alpha Acceptance | Gap Identified |
| `GAP-PEOPLE-PICKER-C10-001` | `OBS-UIR10-PEOPLE-001` | Shared UI/API/Security | selectorهای پراکنده/محل فنی باز | shared single/multiple picker با normalized IDs، cumulative state و secure provider | Workspace Shared Components | High | `OPEN-UIR10-002` | Alpha Acceptance | Gap Identified |
| `GAP-ADMIN-GROUPS-C10-001` | `OBS-UIR10-ADMIN-001` | Security/Migration/UI | مفهوم مدیر سامانه ممکن است تجمیعی/عنوان‌محور باشد | granular groups + composite super-admin + read-only audit viewer | Security Governance | Critical | group mapping migration | Alpha Acceptance | Gap Identified |
| `GAP-SECRETARIAT-C10-001` | `OBS-UIR10-SEC-001` | Module/Model/Sequence/Security | ownership/module و sequence flow نهایی نیست | incoming/outgoing registry، atomic sequence، delivery، reports، correction ledger | Secretariat Registry | High | `OPEN-UIR10-001` | Alpha Acceptance | Gap Identified |
| `GAP-GUARD-STATION-C10-001` | `OBS-UIR10-GUARD-001` | UI/Model/Audit | batch/event models موجود؛ target station و metadata gaps باقی است | batch UI روی مدل‌های موجود، manual time reason، recorded_at، conflict and recent log | `cas_attendance_operations` + core | Critical | `OPEN-UIR10-003` | Alpha Acceptance | Partially Implemented / Gap Identified |
| `GAP-ALPHA-SCOPE-C10-001` | `OBS-UIR10-SCOPE-001` | UI/Dependency/Documentation | OCR/DMS module/code و برخی docs موجودند | هیچ menu/route/queue/setting/dependency محصولی OCR/DMS در Alpha؛ Attachment باقی | Workspace/Document/Correspondence | High | Nextcloud deferred | Alpha Acceptance | Planned Removal / Gap Identified |

## ۴. Gapهای مستندات و Traceability

| Gap ID | نوع | مشکل | Owner | شدت | Acceptance | Status |
|---|---|---|---|---|---|---|
| `GAP-DOC-INDEX-001` | Documentation | Indexهای پوشه با Cycle 10 همگام نبودند | Documentation Governance | High | همه Indexها Cycle 10 و Registryهای مرکزی را نشان دهند | In Development in this branch |
| `GAP-DOC-ID-001` | Documentation | Duplicate Decision IDs | Documentation Governance | High | migration map و registry key یکتا؛ no reuse in new docs | In Development in this branch |
| `GAP-DOC-METADATA-001` | Documentation | Metadata و Statusهای چندگانه/غیراستاندارد | Documentation Governance | Medium | standard منتشر و migration backlog ثبت شود | In Development in this branch |
| `GAP-DOC-PAGE-001` | Documentation | Page Specs/Routeهای ناقص برای چند surface | UX/Domain Owners | Medium | Page ID/Route/Role/Capability/owner/source/status ثبت شود | Gap Identified |
| `GAP-DOC-AUTOVAL-001` | Documentation/Test | validator خودکار لینک/ID/status وجود ندارد | Documentation/Tooling | Medium | CI/report قابل تکرار با approval جدا | Gap Identified |

## ۵. Priority

### P0 / Critical

Delegation security، Attendance correction/audit، Overtime leakage، Organization Scope، Dynamic Work Report security، Admin group separation، Guard append-only integration.

### P1 / High

Provider API، Correspondence actor model، Shared People Picker، Secretariat sequence/security، Form Matrix، Alpha OCR/DMS removal.

### P2 / Medium/Low

Dashboard personalization/layout، CSS polish، documentation metadata migration و automation.

## ۶. قاعده تغییر Status

- `Implemented` فقط با Commit/PR یا deployment evidence و tests؛
- `Accepted` فقط پس از UI revalidation در Context مشخص؛
- `Partially Implemented` باید بخش‌های اجراشده و باقی‌مانده را صریح کند؛
- بسته‌شدن Gap باید Traceability، Decision/Page/Module Registry و Test Evidence را به‌روزرسانی کند.
