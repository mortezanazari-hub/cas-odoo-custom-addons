---
document_id: REG-MOD-001
title: CAS Module and Ownership Registry
document_type: Module Registry
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Architecture Governance
domain_owner: Module Ownership Governance
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

# رجیستری مرکزی ماژول‌ها و مالکیت CAS

این Registry وضعیت Repository را از وضعیت Specification جدا می‌کند. وجود پوشه ماژول به معنی تکمیل Requirementهای Active یا `Implementation Ready` بودن نیست.

## ۱. ماژول‌های موجود Repository

| Module ID | ماژول | مسئولیت اصلی و داده تحت مالکیت | Provider/Consumer | وابستگی و مرز مهم | صفحات/Capabilityهای مرتبط | وضعیت اجرا نسبت به اسناد | Canonical References |
|---|---|---|---|---|---|---|---|
| `MOD-CAS-CORE-001` | `cas_core` | پایه فنی مشترک؛ نباید Business Domain جدید جذب کند | مصرف‌شونده توسط خانواده CAS | Foundation؛ بدون وابستگی به Workspace | غیرمستقیم | Not Assessed | [`README`](../../cas_core/README.md)، [`MODULES`](../../MODULES.md) |
| `MOD-JALALI-001` | `cas_jalali` | ورود/نمایش جلالی؛ مالک تاریخ ذخیره‌شده نیست | همه UIها | تاریخ استاندارد Odoo حفظ می‌شود | همه صفحات تاریخ‌دار | Not Assessed | [`README`](../../cas_jalali/README.md) |
| `MOD-JALALI-HR-001` | `cas_jalali_hr` | Bridge نمایش HR | HR consumer | به Jalali Core متکی | صفحات کارکنان | Not Assessed | [`README`](../../cas_jalali_hr/README.md) |
| `MOD-JALALI-MAIL-001` | `cas_jalali_mail` | Bridge Chatter/Tracking | Odoo Mail consumer | مدل Message موازی ممنوع | Conversations/Chatter | Not Assessed | [`README`](../../cas_jalali_mail/README.md) |
| `MOD-JALALI-SEARCH-001` | `cas_jalali_search` | Parse و Filter تاریخ شمسی | Search Providers | Permission منبع را تغییر نمی‌دهد | Command Palette/Search | Not Assessed | [`README`](../../cas_jalali_search/README.md) |
| `MOD-JALALI-QWEB-001` | `cas_jalali_qweb` | نمایش QWeb/PDF/Email | Report consumers | فقط presentation | Print/PDF | Not Assessed | [`README`](../../cas_jalali_qweb/README.md) |
| `MOD-JALALI-SUITE-001` | `cas_jalali_suite` | نصب تجمیعی خانواده جلالی | Installer | مالک Business Data نیست | N/A | Not Assessed | [`README`](../../cas_jalali_suite/README.md) |
| `MOD-FORM-CORE-001` | `cas_form_core` | Form Definition/Version/Field/Submission/Answer/Snapshot فنی | Work Report و فرم‌های دامنه‌ای | نباید Work Report Lifecycle را مالک شود | Dynamic Work Report، Form Runtime | Gap Identified | [`README`](../../cas_form_core/README.md)، [Work Report Architecture](../05_Architecture/Work_Report_Form_Engine_Architecture.md) |
| `MOD-FORM-BUILDER-001` | `cas_form_builder` | طراح پیش‌نویس Form Schema | Form Core | Runtime یا Domain lifecycle را کپی نمی‌کند | Form Builder؛ Activity/Matrix fields | Gap Identified | [`README`](../../cas_form_builder/README.md)، Cycle 9 Decision |
| `MOD-DYNAMIC-FORM-001` | `cas_dynamic_form` | اجرای Form منتشرشده | Form Core consumers | نسخه منتشرشده immutable | فرم‌های Runtime و Work Report | Gap Identified | [`README`](../../cas_dynamic_form/README.md) |
| `MOD-WORKFLOW-CORE-001` | `cas_workflow_core` | Process State، Transition، Instance و History | Domain modules | Approval Decision را کپی نمی‌کند | Workflow surfaces | Not Assessed | [`README`](../../cas_workflow_core/README.md)، [Module Boundaries](../05_Architecture/Module_Boundaries.md) |
| `MOD-WORKFLOW-DESIGNER-001` | `cas_workflow_designer` | طراح نسخه پیش‌نویس Workflow | Workflow Core | Runtime مالک نیست | Workflow Designer | Not Assessed | [`README`](../../cas_workflow_designer/README.md) |
| `MOD-APPROVAL-001` | `cas_approval_core` | Approval Request/Decision/Delegation موجود | Workflow و Domains | Workflow Definition را کپی نمی‌کند | Approval/Request، Delegation Provider | Gap Identified | [`README`](../../cas_approval_core/README.md) |
| `MOD-ACTION-HUB-001` | `cas_action_hub` | اقدام سازمانی و Lifecycle تخصیص؛ نه Personal Task | Workspace/Calendar consumers | نباید به Workspace برای کارکرد اصلی وابسته باشد | Action Hub، Calendar assigned action | Gap Identified | [`README`](../../cas_action_hub/README.md)، Module Boundaries |
| `MOD-DOCUMENT-001` | `cas_document_core` | سند نسخه‌دار، Binary/Storage linkage و OCR موجود | Correspondence/Attachments | Alpha Scope: OCR و DMS داخلی در Navigation خارج از محدوده؛ Attachment مجاز باقی می‌ماند | اسناد خارج از Alpha؛ Attachment consumers | Planned Removal from Alpha surfaces / Existing module | [`README`](../../cas_document_core/README.md)، [Alpha Out of Scope](../07_Out_Of_Scope/V10_Alpha_Out_Of_Scope.md) |
| `MOD-CORRESPONDENCE-001` | `cas_correspondence` | نامه رسمی، گیرنده، ارجاع و Audit | Workspace، Delegation، Secretariat | Conversation نیست | صفحات مکاتبات | Gap Identified | [`README`](../../cas_correspondence/README.md)، Cycle 10 Decision |
| `MOD-CORRESPONDENCE-ADV-001` | `cas_correspondence_advanced` | قابلیت‌های پیشرفته مکاتبات/ثبت/PDF/امضا در کد فعلی | Correspondence + Document | ownership نهایی Secretariat باید روشن شود؛ DMS داخلی آلفا ممنوع | Secretariat/Outgoing/PDF | Gap Identified | [`README`](../../cas_correspondence_advanced/README.md)، [Secretariat Spec](../02_UI_UX/Administrative/Secretariat.md) |
| `MOD-SHIFT-001` | `cas_shift_management` | سیاست، قالب و برنامه شیفت | Attendance/Work Report | Shift Occurrence contract لازم | Work Report/Attendance | Not Assessed | [`README`](../../cas_shift_management/README.md) |
| `MOD-ATTENDANCE-CORE-001` | `cas_attendance_core` | `cas.attendance.event`، attribution، reconciliation، conflict، void/replacement و append-only history | Operations/Kardex/Workspace | UI نباید منطق را کپی کند | Attendance، Guard Station | Partially Implemented / Gap Identified | [`README`](../../cas_attendance_core/README.md)، [Guard Spec](../02_UI_UX/Security/Guard_Attendance_Station.md) |
| `MOD-ATTENDANCE-OPS-001` | `cas_attendance_operations` | Excel/Staging و `cas.guard.batch` / lines / confirm | Attendance Core/Workspace | هر فرد line مستقل؛ event رسمی در Core | Guard Attendance Station | Partially Implemented / Gap Identified | [`README`](../../cas_attendance_operations/README.md)، [Cycle 10 Impact](../03_Modules/V10_Module_Impact_Assessment.md) |
| `MOD-KARDEX-001` | `cas_kardex_management` | کاردکس دقیقه‌ای، درخواست‌ها و قفل دوره | Attendance/Workflow | raw event بازنویسی نمی‌شود | Attendance correction/Overtime surfaces | Gap Identified | [`README`](../../cas_kardex_management/README.md)، Cycle 9 Decision |
| `MOD-KARDEX-REPORT-001` | `cas_kardex_report` | گزارش Excel کاردکس | Kardex consumer | Export Security الزامی | Kardex reports | Not Assessed | [`README`](../../cas_kardex_report/README.md) |
| `MOD-WORK-REPORT-001` | `cas_work_report` | Report، Section، Profile، Applicability، Access Grant، Evidence Relation و Projection | Organization/Form/Workflow/Approval/Activity/Shift | به Workspace وابسته نمی‌شود؛ Form Schema را کپی نمی‌کند | Dynamic Work Report | Gap Identified | [Specification](../03_Modules/cas_work_report/Specification.md)، [Security](../03_Modules/cas_work_report/Security.md) |
| `MOD-WORKSPACE-001` | `cas_workspace` | Shell، Route، Dashboard Configuration، UI Preference، Command Palette و Recent Resource Reference | همه Domain Providers | مالک Business Data و Permission منبع نیست | تمام Workspace pages | Gap Identified | [Specification](../03_Modules/cas_workspace/Specification.md)، [Provider Registry](../03_Modules/V8_Provider_Registry.md) |

## ۲. ماژول‌ها/دامنه‌های مشخص‌شده در Specification اما خارج از فهرست ۲۴ ماژول موجود

| Module/Domain Registry Key | نام فعلی | مسئولیت مصوب/پیشنهادی | وضعیت | تصمیم یا سؤال باز | Canonical Reference |
|---|---|---|---|---|---|
| `MOD-WORKSPACE-CONTRACT-001` | `cas_workspace_contract` | Provider Protocol، Resource Reference، Metadata و Contract Versioning بدون UI Runtime | Specified / Not confirmed in repository module list | نام و API نهایی باز است | [Provider Registry](../03_Modules/V8_Provider_Registry.md)، [Open Items](Open_Item_Registry.md) |
| `MOD-PERSONAL-TASK-001` | `cas_personal_task` | Personal Task و Category مستقل | Specified / module presence not confirmed | Implementation detail لازم | [Personal Task Spec](../03_Modules/cas_personal_task/Specification.md) |
| `MOD-ORGANIZATION-CORE-001` | `cas_organization_core` | Effective Assignment و Organization Scope پایه | Specified / module presence not confirmed | API/Security detail لازم | [Organization Spec](../03_Modules/cas_organization_core/Specification.md) |
| `MOD-ACTIVITY-CATALOG-001` | `cas_activity_catalog` | Activity Definition، Proposal و Standardization | Specified / module presence not confirmed | Implementation detail لازم | [Activity Catalog Spec](../03_Modules/cas_activity_catalog/Specification.md) |
| `MOD-DELEGATION-DOMAIN-001` | نام نهایی تعیین نشده | principal/agent/domain/capability/validity/decree/state/audit و Provider delegation | Gap Identified | reuse/extension Approval/Organization یا ماژول مستقل نیازمند تصمیم معماری | [Delegation Spec](../02_UI_UX/Employee/Delegation.md)، [Cycle 10 Impact](../03_Modules/V10_Module_Impact_Assessment.md) |
| `MOD-SECRETARIAT-REGISTRY-001` | نام نهایی تعیین نشده | incoming/outgoing registry، sequence، routing، delivery، report و correction ledger | Gap Identified | ownership و نام نهایی Open | [Secretariat Spec](../02_UI_UX/Administrative/Secretariat.md) |
| `MOD-PEOPLE-PICKER-001` | داخل `cas_workspace` یا ماژول فنی مستقل | Shared person-selection contract و UI component | Gap Identified | محل فنی نهایی Open | [People Picker](../02_UI_UX/Common/Shared_People_Picker.md) |

## ۳. Providerها و مصرف‌کنندگان کلیدی

| Provider Domain | Provider مالک | Consumerهای اصلی |
|---|---|---|
| Navigation/Widget/Search/Action contract | `cas_workspace_contract` | `cas_workspace` و Domain providers |
| Personal Tasks | `cas_personal_task` | Workspace، Calendar |
| Organizational Actions | `cas_action_hub` | Workspace، Calendar، Correspondence action requests |
| Organization Scope | `cas_organization_core` | Work Report، Calendar، Actions، Search، People Picker |
| Work Report | `cas_work_report` | Workspace، Reviewer، Reporting |
| Correspondence | Correspondence modules | Workspace، Delegation، Secretariat |
| Attendance/Shift | Attendance/Shift modules | Workspace، Kardex، Work Report |
| Conversation/Notification Delivery | Odoo Mail/Discuss/Bus | Workspace views |
| Attachment | Odoo Attachment / allowed document contract | Correspondence، Work Report، Form، Secretariat |

## ۴. وابستگی‌های ممنوع کلیدی

- Foundation و Domain Module به `cas_workspace` UI وابسته نمی‌شوند.
- Workspace Domain Modelها را مستقیم import یا با `sudo()` تجمیع نمی‌کند.
- Form Core به Work Report وابسته نمی‌شود.
- Organization Core به Work Report/Action/Workspace وابسته نمی‌شود.
- Activity Catalog به Work Report وابسته نمی‌شود.
- Conversation، Notification Delivery، Calendar Event و Attachment مدل موازی نمی‌گیرند مگر Gap و Decision رسمی.
- Secretariat در آلفا DMS یا OCR داخلی ایجاد نمی‌کند.

## ۵. قاعده نگهداری

هر Module Entry باید Presence در Repository، Domain Ownership، Provider/Consumer، allowed/forbidden dependencies، صفحات، Decisionها، وضعیت اجرا، Gapها و Canonical docs را جداگانه نگهدارد. مالکیت از روی نام UI یا کد فعلی حدس زده نمی‌شود.
