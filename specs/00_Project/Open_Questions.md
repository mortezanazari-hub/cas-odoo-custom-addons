---
document_id: OPEN-CAS-V8
title: Legacy Open Questions from Cycle 8 Consolidation
document_type: Historical Open Question Register
document_status: Superseded
implementation_status: N/A
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 8
source_iteration: 12
owner: Product & Architecture Governance
domain_owner: Open Item Governance
created_at: N/A
updated_at: 2026-07-22
canonical: false
supersedes: []
superseded_by: [REG-OPEN-001]
related_decisions: []
related_modules: []
related_pages: []
related_capabilities: []
---

# سؤالات باز Cycle 8 — سند سازگاری تاریخی

> **Status: Superseded as central register**  
> **Superseded By:** [Open Item Registry](Open_Item_Registry.md)  
> **Historical Purpose:** حفظ شناسه‌ها، توضیحات و لینک‌های قدیمی Cycle 8.  
> پاسخ یا Item جدید باید فقط در Registry مرکزی ثبت شود.

## نتیجه تصمیم‌های محصولی Cycle 8

موارد زیر در Consolidation Cycle 8 تعیین تکلیف شده بودند:

- Iteration 12 جزو Cycle 8 است؛
- Cycle 7 Historical است؛
- Personal Task مالک مستقل دارد؛
- Self Task و Assigned Action تفکیک شده‌اند؛
- Odoo Notification Reuse می‌شود؛
- Recent History ماژول مستقل ندارد؛
- Provider Contract مشترک است؛
- Organization Scope مالک مستقل دارد؛
- Search Capability از Permission منابع جداست؛
- Notification Center Route مستقل دارد؛
- Overlay بر پایه Odoo UI Services هماهنگ می‌شود؛
- Preference Resolution تعیین شده است؛
- Dashboard Management Center لازم است؛
- Work Report چند Assignment یک گزارش ترکیبی است؛
- واحد گزارش Shift Occurrence است؛
- File Infrastructure در Cycle 8 بازطراحی نمی‌شود؛
- Activity Catalog مستقل است؛
- Applicability گزارش می‌تواند Disabled باشد؛
- Access Grant مستقل از زیردستی لازم است.

## سؤالات فنی منتقل‌شده به Registry مرکزی

| Legacy ID | موضوع | Central Open ID | وضعیت جاری |
|---|---|---|---|
| `Q-TECH-001` | نام نهایی ماژول قرارداد Workspace | `OPEN-TECH-001` | Carried Forward |
| `Q-TECH-002` | API دقیق Providerها | `OPEN-TECH-002` | Carried Forward |
| `Q-TECH-003` | ذخیره Recent History | `OPEN-TECH-003` | Carried Forward |
| `Q-TECH-004` | Gap Notification در Odoo 19 Community | `OPEN-TECH-004` | Carried Forward |
| `Q-TECH-005` | نام/مدل Calendar Integration | `OPEN-TECH-005` | Carried Forward |
| `Q-TECH-006` | Policy Section Reviewer | `OPEN-TECH-006` | Decision Required |
| `Q-TECH-007` | Formula و Reporting Projection | `OPEN-TECH-007` | Open |
| `Q-TECH-008` | Migration گزارش ثابت به پویا | `OPEN-TECH-008` | Open |
| `Q-TECH-009` | Widget Resize و Hide/Show پیشرفته | `OPEN-TECH-009` | Deferred |
| `Q-TECH-010` | File/Document Infrastructure Redesign | `OPEN-TECH-010` | Deferred |
| `Q-TECH-011` | Delegation Approval Authority | `OPEN-TECH-011` | Decision Required |
| `Q-TECH-012` | Data Retention | `OPEN-TECH-012` | Decision Required |

## جزئیات تاریخی

### `Q-TECH-001` — نام ماژول قرارداد Workspace

نام پیشنهادی `cas_workspace_contract` بود. معیارها: عدم وابستگی به UI Runtime، جلوگیری از Circular Dependency و امکان استفاده Providerها بدون وابستگی مستقیم به `cas_workspace`.

### `Q-TECH-002` — API Providerها

Widget، Search، Action، History Resource Reference، Dashboard Availability و Deep Link Resolver باید Schema نهایی داشته باشند.

### `Q-TECH-003` — Recent History

گزینه‌های فنی Preference Model یا مدل Lightweight با Retention محدود بودند. کپی Business Data در هر دو حالت ممنوع است.

### `Q-TECH-004` — Notification Gap

Read/Unread، aggregation، severity، action button، deep link، snooze و company policy باید در Odoo 19 Community Verify شوند.

### `Q-TECH-005` — Calendar Integration

Extension در Calendar موجود یا Bridge مستقل CAS باید بررسی شود؛ مالکیت Event نزد Calendar باقی می‌ماند.

### `Q-TECH-006` — Section Reviewer

تعداد Reviewer، سطح Approval و رفتار Return یک Section نسبت به سایر Sectionها نیازمند تصمیم است.

### `Q-TECH-007` — Projection

Fieldهای reportable، index strategy و projection refresh باید برای Answerهای پویا تعیین شوند.

### `Q-TECH-008` — Migration Work Report

Mapping، dual read، validation و rollback plan لازم است.

### `Q-TECH-009` — Widget Advanced Personalization

در Scope Cycle 8 فعال نبود و برای آینده به Decision جدا نیاز دارد.

### `Q-TECH-010` — Document Infrastructure

Versioning، retention، archive، advanced permissions، digital signature، Nextcloud integration و storage policy خارج از Cycle 8 بودند. Cycle 10 نیز OCR/DMS داخلی را از Alpha Scope خارج کرد.

### `Q-TECH-011` — Delegation Authority

برای هر Access Grant باید نقش مجاز create/extend/revoke/audit مشخص شود.

### `Q-TECH-012` — Data Retention

Recent History، Notification Aggregation، Audit و Work Report Evidence نیازمند Security/Compliance Specification هستند.

## قاعده برخورد

- این فایل دیگر Registry فعال نیست؛
- شناسه‌های قدیمی برای لینک و سابقه حفظ می‌شوند؛
- تصمیم جدید در Decision/Architecture Contract و Item متناظر در [Open Item Registry](Open_Item_Registry.md) ثبت می‌شود؛
- سؤال فنی نباید Baseline محصولی Active را تضعیف کند؛
- تا زمان تصمیم، رفتار fail-closed و حداقل دسترسی اعمال می‌شود.
