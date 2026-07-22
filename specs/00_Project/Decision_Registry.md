---
document_id: REG-DEC-001
title: CAS Decision Registry
document_type: Decision Registry
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Product & Architecture Governance
domain_owner: Decision Governance
created_at: 2026-07-22
updated_at: 2026-07-22
canonical: true
supersedes: []
superseded_by: []
related_decisions: []
related_modules: []
related_pages: []
related_capabilities: []
---

# رجیستری مرکزی تصمیم‌های CAS

این Registry نقطه ورود به تصمیم‌هاست و جایگزین Decision Document تفصیلی نیست. در تعارض، Source Document و سلسله‌مراتب `specs/README.md` مرجع‌اند.

## ۱. تصمیم‌های پایه و Workspace

| Canonical Registry Key | عنوان/Capability | Domain Owner | Source Cycle | Source Document | Decision Status | Implementation | UI Validation | Supersedes / Notes | Current Canonical Reference |
|---|---|---|---|---|---|---|---|---|---|
| `DEC-BASE-001-WORKSPACE-OPERATIONAL` | Workspace عملیاتی و Action-First | Workspace | Early baseline | [`DEC-001`](../04_Decisions/DEC-001-Workspace-Is-Operational.md) | Agreed | Not Assessed | Pending Revalidation | تصمیم پایه | Source + [UX Principles](../01_Product/UX_Principles.md) |
| `DEC-BASE-002-NO-SLA-EMPLOYEE-UI` | عدم نمایش SLA فنی در UI کاربر | Cross-domain UX | Early baseline | [`DEC-002`](../04_Decisions/DEC-002-No-SLA-In-Employee-UI.md) | Agreed | Not Assessed | Pending Revalidation | Labelهای انسانی جایگزین SLA فنی | Source |
| `DEC-BASE-003-ACTIVITY-STANDARDIZATION` | Activity Catalog و Snapshot | Activity Catalog | Early baseline | [`DEC-003`](../04_Decisions/DEC-003-Activity-Standardization.md) | Agreed | Gap Identified | Pending Revalidation | در Cycle 9 با Proposal تکمیل شد | Source + `DEC-UIR09-010-CONSOLIDATED` |
| `DEC-V7-004-WIDGET-SYSTEM` | سیستم Widget میزکار | Workspace | Cycle 7 | [`DEC-004`](../04_Decisions/DEC-004-Workspace-Widget-System.md) | Agreed | Gap Identified | Pending Revalidation | Dashboard Governance جدید مکمل آن است | Source + `DEC-V8-018-DASHBOARD-GOVERNANCE` |
| `DEC-V7-005-CONVERSATIONS-FIRST-CLASS` | گفتگو قابلیت سطح اول | Odoo Mail/Discuss + Workspace | Cycle 7 | [`DEC-005`](../04_Decisions/DEC-005-Conversations-Are-First-Class.md) | Agreed | Not Assessed | Pending Revalidation | Odoo reuse الزامی | Source + `DEC-V8-014-DISCUSS-REUSE` |
| `DEC-V7-006-THEME-READABILITY` | Theme و خوانایی | Workspace | Cycle 7 | [`DEC-006`](../04_Decisions/DEC-006-Workspace-Theme-And-Readability.md) | Agreed | Gap Identified | Pending Revalidation | CSS Contract مکمل است | [CSS Contract](../05_Architecture/Workspace_CSS_And_Design_System_Contract.md) |
| `DEC-V7-007-COLLAPSIBLE-SIDEBAR` | Sidebar جمع‌شونده | Workspace | Cycle 7 | [`DEC-007`](../04_Decisions/DEC-007-Collapsible-Sidebar.md) | Agreed | Gap Identified | Pending Revalidation | Navigation Cycle 9 بر آن سوار می‌شود | Source + Cycle 9 Decision |
| `DEC-V7-008-EMBEDDED-CALENDAR` | تقویم تعاملی | Calendar Domain | Cycle 7 | [`DEC-008`](../04_Decisions/DEC-008-Embedded-Calendar.md) | Agreed | Gap Identified | Pending Revalidation | Authorization در DEC-013 تکمیل شد | Source + `DEC-V8-013-CALENDAR-AUTH` |
| `DEC-V7-009-ROUTE-CAPABILITY` | Route و Capability عمومی | Workspace/Security | Cycle 7 | [`DEC-009`](../04_Decisions/DEC-009-Workspace-Route-And-Capability-Expansion.md) | Active | Gap Identified | Pending Revalidation | Partially Superseded: Route مستقل Search/History و `history.read` | `DEC-V8-016-SEARCH-HISTORY` + Cycle 9 Navigation |
| `DEC-V7-010-PROVIDER-REGISTRY` | Registry مشترک Providerها | Workspace Contract | Cycle 7 | [`DEC-010`](../04_Decisions/DEC-010-Global-Provider-Registries.md) | Under Review | Gap Identified | Pending Revalidation | Legacy metadata=`Needs Review`؛ اصل معماری در Registry v8 تثبیت شده | [Provider Registry](../03_Modules/V8_Provider_Registry.md) |
| `DEC-V7-011-DOMAIN-SEPARATION` | تفکیک Task، Action، Notification و History | Multiple | Cycle 7/8 | [`DEC-011`](../04_Decisions/DEC-011-Separate-Task-Action-Notification-History.md) | Agreed | Gap Identified | Pending Revalidation | مالکیت‌های مستقل | [Module Ownership](../03_Modules/V8_Module_Ownership_Map.md) |

## ۲. تصمیم‌های Cycle 8

| Canonical Registry Key | عنوان/Capability | Domain Owner | Source Iteration | Source Document | Decision Status | Implementation | UI Validation | Affected Modules/Pages | Current Canonical Reference |
|---|---|---|---|---|---|---|---|---|---|
| `DEC-V8-012-PERSONAL-TASK-CATEGORIES` | حاکمیت دسته‌های Personal Task | `cas_personal_task` | Cycle 8 I1–I4 | [`DEC-012`](../04_Decisions/DEC-012-Personal-Task-Category-Governance.md) | Agreed | Gap Identified | Pending Revalidation | Personal Tasks | Source |
| `DEC-V8-013-CALENDAR-AUTH` | Attendee Selection و Assignment Authorization | Calendar/Organization | Cycle 8 I1–I4 | [`DEC-013`](../04_Decisions/DEC-013-Calendar-Attendee-Selection-And-Assignment-Authorization.md) | Agreed | Gap Identified | Pending Revalidation | Calendar, People selection | Source |
| `DEC-V8-014-DISCUSS-REUSE` | Reuse Odoo Discuss و تعامل پیام | Odoo Mail/Discuss | Cycle 8 I1–I4 | [`DEC-014`](../04_Decisions/DEC-014-Discuss-Reuse-And-Message-Interaction.md) | Agreed | Not Assessed | Pending Revalidation | Conversations, Notifications | Source |
| `DEC-V8-015-OVERLAY-FOCUS` | Overlay، Layering و Focus | Workspace/Odoo UI Services | Cycle 8 I1–I4 | [`DEC-015`](../04_Decisions/DEC-015-Overlay-Layering-And-Focus-Management.md) | Agreed | Gap Identified | Pending Revalidation | همه Modal/Picker/Paletteها | Source |
| `DEC-V8-016-SEARCH-HISTORY` | ادغام Search و Recent History | Workspace | Cycle 8 I5–I11 | [`DEC-016`](../04_Decisions/DEC-016-Search-And-Recent-History-Consolidation.md) | Agreed | Gap Identified | Pending Revalidation | Command Palette؛ حذف Routeهای مستقل | Source + [Search Contract](../05_Architecture/V8-Search-History-And-Scroll-Contracts.md) |
| `DEC-V8-017-WORK-REPORT-FORM-ENGINE` | Work Report از Form Engine استفاده می‌کند | Work Report/Form Engine | Cycle 8 I12 | [`DEC-017`](../04_Decisions/DEC-017-Work-Report-Domain-Uses-Form-Engine.md) | Agreed | Gap Identified | Pending Revalidation | Dynamic Work Report | [Work Report Architecture](../05_Architecture/Work_Report_Form_Engine_Architecture.md) |
| `DEC-V8-018-DASHBOARD-GOVERNANCE` | مدیریت و حاکمیت Dashboard | Workspace | Cycle 8 | [`DEC-018`](../04_Decisions/DEC-018-Dashboard-Administration-And-Governance.md) | Agreed | Gap Identified | Pending Revalidation | Dashboard Admin Center | Source + Cycle 9 personalization changes |
| `DEC-V8-019-SHIFT-APPLICABILITY` | Work Report براساس Shift Occurrence و Applicability | Work Report | Cycle 8 I12 | [`DEC-019`](../04_Decisions/DEC-019-Work-Report-Applicability-And-Shift-Period.md) | Agreed | Gap Identified | Pending Revalidation | Dynamic Work Report | Source |
| `DEC-V8-020-DELEGATED-WORK-REPORT` | دسترسی تفویض‌شده گزارش کار | Work Report | Cycle 8 I12 | [`DEC-020`](../04_Decisions/DEC-020-Delegated-Work-Report-Access.md) | Agreed | Gap Identified | Pending Revalidation | Work Report security | [Work Report Security](../03_Modules/cas_work_report/Security.md) |

## ۳. تصمیم‌های تجمیعی Cycle 9 و Cycle 10

| Canonical Registry Key | عنوان | Source | Status | Implementation | UI Validation | Affected Modules | Supersedes | Current Canonical Reference |
|---|---|---|---|---|---|---|---|---|
| `DEC-UIR09-010-CONSOLIDATED` | Workspace Navigation، Attendance Correction/Audit، Overtime، Activity Proposal، Form Matrix و Dashboard Personalization | [Cycle 9 Decision](../04_Decisions/DEC-010-UIR09-Consolidated-Workspace-And-Operational-UX.md) | Active | Gap Identified | Pending Revalidation | Workspace، Work Report، Activity Catalog، Attendance، Overtime، Form Engine | Flat navigation؛ reorder-only dashboard؛ Work Progress baseline | Source + [Cycle 9 Register](UI_Review_Cycle_9_Register.md) |
| `DEC-UIR10-016-CONSOLIDATED` | اصلاح آلفا در مکاتبات، تفویض، People Picker، مدیریت سامانه، دبیرخانه، نگهبانی و حذف OCR/DMS | [Cycle 10 Decision](../04_Decisions/DEC-016-UIR10-Consolidated-Alpha-Workspace-Refinement.md) | Agreed | Gap Identified | Pending Revalidation | Workspace، Correspondence، Delegation، Secretariat، Attendance، Security | فقط baselineهای متعارض صریح | Source + [Cycle 10 Register](UI_Review_Cycle_10_Register.md) |

## ۴. تعارض‌ها و نکات حاکمیتی

1. شناسه‌های نمایشی `DEC-010` و `DEC-016` تکرار شده‌اند؛ کلیدهای Registry بالا برای رفع ابهام استفاده می‌شوند و فایل‌ها فعلاً Rename نمی‌شوند.
2. Metadata تصمیم Cycle 9 مقدار Implementation=`Planned` دارد، درحالی‌که Traceability و Cycle Register آن را `Gap Identified` اعلام می‌کنند. وضعیت Registry براساس Traceability=`Gap Identified` است و تعارض در [Open Item Registry](Open_Item_Registry.md) ثبت شده است.
3. `Agreed` یا `Active` به معنی `Implemented` یا `Accepted in Production` نیست.
4. Prototype و ZIP فقط Evidence بازنگری UI هستند.

## ۵. قاعده افزودن تصمیم

Decision جدید باید هم‌زمان در این Registry، Traceability، Module/Page Registryهای متأثر، Change Set و Open Item Registry به‌روزرسانی شود. در صورت Supersede، لینک دوطرفه اجباری است.
