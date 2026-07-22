---
document_id: REG-OPEN-001
title: CAS Open Item Registry
document_type: Open Item Registry
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Product & Architecture Governance
domain_owner: Open Item Governance
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

# رجیستری مرکزی Observation، سؤال باز، تعارض، ریسک و Deferred Item

وجود Entry در این فایل به معنی تصویب پیشنهاد نیست. Item فقط زمانی بسته می‌شود که Decision، Architecture Contract، Specification یا Validation Evidence رسمی آن را تعیین تکلیف کند.

## Statusهای Registry

`Open`, `Triaged`, `Decision Required`, `Deferred`, `Blocked`, `Resolved`, `Rejected`, `Carried Forward`

## ۱. موارد فنی Carry Forward از Cycle 8

| Open ID | Type | موضوع | اطلاعات/تصمیم لازم | Owner/Decision Authority | Related Docs | Status |
|---|---|---|---|---|---|---|
| `OPEN-TECH-001` | Open Question | نام نهایی ماژول قرارداد Workspace | تثبیت نام، package boundary و migration path برای `cas_workspace_contract` | Architecture Governance | [Legacy Open Questions](Open_Questions.md)، [Provider Registry](../03_Modules/V8_Provider_Registry.md) | Carried Forward |
| `OPEN-TECH-002` | Open Question | API دقیق Providerها | Schema نهایی Widget/Search/Action/History/Dashboard/Deep Link | Architecture + Provider Owners | Provider Registry | Carried Forward |
| `OPEN-TECH-003` | Open Question | ذخیره Recent History | Preference model یا lightweight technical model، retention و cleanup | Workspace Architecture + Security | Search/History Contract | Carried Forward |
| `OPEN-TECH-004` | Open Question | Gap دقیق Notification در Odoo 19 Community | Verify read/unread، aggregation، severity، actions، deep link، snooze و policy | Odoo Integration Owner | [Notification Gap Analysis](../05_Architecture/Odoo_Notification_Gap_Analysis.md) | Carried Forward |
| `OPEN-TECH-005` | Open Question | نام و مدل Calendar Integration | Extension در Calendar یا Bridge مستقل | Calendar Architecture | Legacy Open Questions | Carried Forward |
| `OPEN-TECH-006` | Open Question | Policy دقیق Section Reviewer | تعداد Reviewer، approval level و رفتار Return یک Section | Work Report Product Owner | Work Report Specification/Security | Decision Required |
| `OPEN-TECH-007` | Open Question | Formula و Reporting Projection گزارش پویا | reportable fields، index strategy و projection refresh | Work Report/Data Architecture | Work Report Architecture | Open |
| `OPEN-TECH-008` | Open Question | Migration گزارش ثابت به پویا | Mapping، dual read، validation و rollback | Work Report Migration Owner | Work Report Architecture | Open |
| `OPEN-TECH-009` | Deferred Item | Widget Resize و Hide/Show پیشرفته | interaction، policy و governance جداگانه | Workspace Product Owner | `DEC-V8-018` و Cycle 9 | Deferred |
| `OPEN-TECH-010` | Deferred Item | File/Document Infrastructure Redesign | versioning، retention، archive، signature، Nextcloud و storage policy | Product + Integration Architecture | Alpha Out of Scope | Deferred |
| `OPEN-TECH-011` | Open Question | Delegation Approval Authority | نقش مجاز create/extend/revoke/audit برای هر Grant type | Security/Product Governance | Delegation Spec | Decision Required |
| `OPEN-TECH-012` | Open Question | Data Retention | Recent History، Notification، Audit و Work Report Evidence | Security/Compliance | Security docs | Decision Required |

## ۲. موارد باز Cycle 9

| Open ID | Type | موضوع | وضعیت فعلی | نیاز برای بستن | Owner | Status |
|---|---|---|---|---|---|---|
| `OPEN-UIR09-001` | Deferred Item | تنظیمات پیشرفته اختصاصی هر Widget | Cycle 9 فقط visibility/shortcut محدود را پذیرفت | Decision و configuration schema | Workspace Product Owner | Deferred |
| `OPEN-UIR09-002` | Observation | CSS و Responsive polish باقی‌مانده | Contract فعال است؛ اجرای واقعی و visual regression لازم است | Implementation evidence + revalidation | Workspace/UI Addon Owners | Carried Forward |
| `OPEN-UIR09-003` | Validation Item | بازبینی تراکم، ارتفاع و breakpointها | Prototype کافی نیست | تست با Odoo و داده واقعی | UX/QA | Open |
| `OPEN-UIR09-004` | Documentation Gap | Page Spec اصلاح حضور و Correction Ledger | Decision و Traceability وجود دارد؛ Page Spec مستقل ندارد | Page ID، Route، states، security و acceptance | Attendance Product Owner | Open |
| `OPEN-UIR09-005` | Documentation Gap | Page Spec ممیزی تصادفی Attendance | Flow ثبت شده؛ صفحه/Entry رسمی ناقص است | Page Specification | Attendance/Security Owner | Open |
| `OPEN-UIR09-006` | Documentation Gap | Page Spec کامل Overtime | Capabilityها ثبت شده‌اند؛ Page mapping ناقص است | Page/Route/Role/Provider spec | Overtime Owner | Open |
| `OPEN-UIR09-007` | Documentation Gap | Page Spec Form Builder providers/matrix | Decision موجود است؛ Page ID و UI contract مرکزی ناقص | Page Spec + API contract | Form Builder Owner | Open |

## ۳. موارد باز Cycle 10

| Open ID | Type | موضوع | وضعیت فعلی | اطلاعات/تصمیم لازم | Owner | Status |
|---|---|---|---|---|---|---|
| `OPEN-UIR10-001` | Open Question | نام و ownership نهایی ماژول دبیرخانه | Secretariat Registry به‌عنوان Domain تعریف شده؛ module name باز است | reuse/extension `cas_correspondence_advanced` یا ماژول مستقل با rationale | Architecture + Correspondence Owner | Decision Required |
| `OPEN-UIR10-002` | Open Question | محل فنی Shared People Picker | Contract و Page Spec فعال؛ محل `cas_workspace` یا module فنی مستقل باز است | dependency analysis و reuse plan | Workspace Architecture | Decision Required |
| `OPEN-UIR10-003` | Open Question | threshold و approval policy زمان دستی Attendance | reason/audit قطعی است؛ آستانه و approver باز است | policy configurable، roles و edge cases | Attendance Product/Security | Decision Required |
| `OPEN-UIR10-004` | Deferred Item | Integration Contract با Nextcloud | OCR/DMS داخلی خارج از آلفاست | ownership، storage، permission، sync، audit و failure contract | Integration Architecture | Deferred |
| `OPEN-UIR10-005` | Documentation Gap | Pageهای تفصیلی Admin Center | گروه‌ها و SoD تصمیم‌گیری شده؛ Page/Routeها کامل نیستند | Page Specs برای user/access، organization، settings و audit | Security/UX Governance | Open |
| `OPEN-UIR10-006` | Documentation Gap | Backlink Cycle 10 در Page Specهای مکاتبات | Decision تجمیعی موجود است؛ همه صفحات جزئی Index نشده‌اند | inventory و backlink update | Correspondence Owner | Open |
| `OPEN-UIR10-007` | Open Question | Delegation domain implementation placement | Entity/Provider requirements روشن، placement نامشخص | extend Approval/Organization یا module مستقل | Architecture/Security | Decision Required |

## ۴. تعارض‌ها و مشکلات حاکمیت مستندات کشف‌شده در Audit

| Open ID | Type | Conflict/Risk | Evidence | تصمیم/اصلاح لازم | Owner | Status |
|---|---|---|---|---|---|---|
| `OPEN-DOC-001` | Conflict | Indexهای `00_Project`, Product, UI, Modules, Decisions و Change Sets هنوز Baselineهای 8/9 را آخرین مرجع نشان می‌دهند، درحالی‌که Constitution و Version History Cycle 10 را فعال می‌دانند | Indexهای پوشه | همگام‌سازی Navigation بدون Supersede تصمیم‌های قدیمی | Documentation Governance | Triaged |
| `OPEN-DOC-002` | Conflict | `DEC-010` و `DEC-016` برای بیش از یک سند استفاده شده‌اند | Decision files | استفاده از Canonical Registry Key و Migration Map؛ Rename فقط در Change Set جدا | Documentation Governance | Triaged |
| `OPEN-DOC-003` | Conflict | Metadata تصمیم Cycle 9 Implementation=`Planned` ولی Register/Traceability=`Gap Identified` | Cycle 9 Decision/Register/Traceability | تعیین یک مقدار رسمی و اصلاح Metadata Source | Product & Architecture Governance | Decision Required |
| `OPEN-DOC-004` | Conflict | Statusهای غیراستاندارد مانند `Consolidated`, `Needs Review`, `Active Review Source` و ترکیب چند Context | اسناد v7/v8/v9 | Migration تدریجی براساس Metadata Standard | Documentation Governance | Triaged |
| `OPEN-DOC-005` | Conflict | `Open_Questions.md` هنوز خود را v8 معرفی می‌کند و موارد Cycle 9/10 در Change Setها پراکنده‌اند | Open Questions + Change Sets | این Registry مرجع مرکزی شود؛ فایل قدیمی Historical/compatibility index باقی بماند | Documentation Governance | Triaged |
| `OPEN-DOC-006` | Conflict | Root README قابلیت OCR/DMS را هدف عمومی معرفی می‌کند، اما Cycle 10 آن‌ها را از Alpha Scope خارج می‌کند | Root README + Alpha Out of Scope | چون مأموریت فعلی فقط `specs` است، اصلاح Root README نیازمند تأیید جداگانه است | Product Governance | Open |
| `OPEN-DOC-007` | Risk | فهرست ۲۴ ماژول موجود با module/domainهای مصوب ولی تأییدنشده در Repository متفاوت است | `MODULES.md` + Module Specs | Presence/Planned/Proposed به‌صورت جدا نگهداری شود | Architecture Governance | Triaged |
| `OPEN-DOC-008` | Risk | Page Specهای فعال Metadata YAML استاندارد ندارند یا Route در بعضی‌ها اعلام نشده | UI docs | Migration تدریجی Active pages و ثبت route=`N/A/Overlay/TBD` | UX/Documentation Governance | Open |
| `OPEN-DOC-009` | Validation Failure | نبود ابزار خودکار تأیید لینک، duplicate ID و enum status در Repository | Documentation audit | validator script/CI فقط با تأیید جداگانه خارج از docs یا در tooling scope | Documentation Governance | Open |

## ۵. Risks مشترک Product/Architecture

| Risk ID | ریسک | Mitigation موجود | Owner | Status |
|---|---|---|---|---|
| `OPEN-RISK-001` | privilege escalation از طریق Delegation | principal/actor audit، capability/scope checks، revocation | Security | Open until implemented |
| `OPEN-RISK-002` | metadata/search/count leakage در People Picker/Search/Reports | server-side filtering و fail-closed | Security/Providers | Open until tested |
| `OPEN-RISK-003` | sequence race در دبیرخانه | atomic backend sequence و unique constraints | Secretariat Owner | Open until implemented |
| `OPEN-RISK-004` | duplicate/conflicting attendance event | batch line، conflict validation، append-only event | Attendance Owner | Open until implemented |
| `OPEN-RISK-005` | DMS موازی با Nextcloud | OCR/DMS خارج از Alpha | Product/Integration | Mitigated for Alpha; deferred |
| `OPEN-RISK-006` | stale cache پس از revocation/company switch | scoped/revocation-aware cache | Security/Workspace | Open until tested |

## ۶. قاعده بستن Item

هر Item بسته‌شده باید `Resolved By`، تاریخ، Decision/Contract/PR/Test Evidence و اثر روی Registryهای Decision/Capability/Page/Module/Gap را ثبت کند. حذف ردیف ممنوع است؛ وضعیت به `Resolved` یا `Rejected` تغییر می‌کند.
