---
document_id: STD-DOCS-001
title: CAS Metadata, Status and Identifier Standard
document_type: Documentation Standard
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Product & Architecture Governance
domain_owner: Documentation Governance
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

# استاندارد Metadata، Status و شناسه‌های مستندات CAS

این سند استاندارد موجود در `specs/README.md` را توسعه می‌دهد و استاندارد موازی ایجاد نمی‌کند. اسناد قدیمی تا زمان Migration موضوعی تغییر نام یا حذف نمی‌شوند.

## ۱. Metadata پایه

اسناد مهم باید در ابتدای فایل Front Matter زیر را متناسب با نوع خود داشته باشند:

```yaml
---
document_id: <stable-id>
title: <title>
document_type: <official-type>
document_status: Draft | Under Review | Agreed | Active | Superseded | Historical | Rejected | Archived
implementation_status: Not Assessed | Gap Identified | Planned | In Development | Implemented | Partially Implemented | Blocked | Deprecated | N/A
ui_validation_status: Not Validated | Pending Revalidation | Validated | Accepted | Reopened | Failed Validation | N/A
source_ui_review_cycle: <cycle-or-N/A>
source_iteration: <iteration-or-N/A>
owner: <document-owner>
domain_owner: <domain-owner>
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
effective_from: YYYY-MM-DD | N/A
canonical: true | false
supersedes: []
superseded_by: []
related_decisions: []
related_observations: []
related_change_sets: []
related_modules: []
related_pages: []
related_capabilities: []
---
```

فیلد نامرتبط باید `N/A` یا آرایه خالی باشد؛ حذف فیلد بدون دلیل مجاز نیست.

## ۲. مدل رسمی Status

### Document Status

`Draft`, `Under Review`, `Agreed`, `Active`, `Superseded`, `Historical`, `Rejected`, `Archived`

### Implementation Status

`Not Assessed`, `Gap Identified`, `Planned`, `In Development`, `Implemented`, `Partially Implemented`, `Blocked`, `Deprecated`, `N/A`

### UI Validation Status

`Not Validated`, `Pending Revalidation`, `Validated`, `Accepted`, `Reopened`, `Failed Validation`, `N/A`

سه محور مستقل‌اند. Prototype Acceptance با Production Acceptance یکی نیست و در Notes یا Evidence Context جدا ثبت می‌شود.

## ۳. نگاشت Statusهای قدیمی

| مقدار قدیمی | رفتار Migration |
|---|---|
| `Consolidated` | به‌عنوان توضیح بلوغ/هماهنگی در Notes حفظ شود؛ یک Document Status رسمی جدا تعیین شود. |
| `Needs Review` | در صورت نبود تصمیم جدید به `Under Review` نگاشت شود. |
| `Active Review Source` | وضعیت خود Cycle از اعتبار Decisionهای درون آن جدا شود؛ Cycle قدیمی معمولاً `Historical` است، اما Decisionهای بدون Supersede می‌توانند Active بمانند. |
| `Accepted as Review Baseline; Pending Implementation Revalidation` | به دو Context تفکیک شود: Prototype=`Accepted` و Production=`Pending Revalidation`. |
| `Planned Removal / Not In Alpha` | Implementation=`Planned` و Scope=`Out of Scope for Alpha`. |
| `Verified` یا `Implementation Ready` | Status رسمی نیستند؛ فقط با Evidence و معیارهای تعریف‌شده در Governance به‌عنوان readiness/outcome ثبت شوند. |

هیچ نگاشت خودکار بدون خواندن Source Document انجام نمی‌شود.

## ۴. الگوی شناسه‌ها

| نوع | الگو |
|---|---|
| Decision | `DEC-<DOMAIN>-NNN` یا شناسه موجود تثبیت‌شده |
| Architecture Decision | `ADR-<DOMAIN>-NNN` |
| Security Decision | `SEC-<DOMAIN>-NNN` |
| Capability | `CAP-<DOMAIN>-NNN` |
| Page | `PAGE-<DOMAIN>-NNN` یا Page ID موجود |
| Module Registry Entry | `MOD-<MODULE>-NNN` |
| Observation | `OBS-UIR<cycle>-<DOMAIN>-NNN` |
| Gap | `GAP-<MODULE>-NNN` |
| Change Set | `CS-UIR<cycle>-<SCOPE>` |
| Validation | `VAL-UIR<cycle>-NNN` |
| Open Item | `OPEN-<TYPE>-NNN` |
| Documentation Standard/Map | `STD-DOCS-NNN`, `MAP-DOCS-NNN` |

شناسه منتشرشده Reuse یا بی‌دلیل Rename نمی‌شود.

## ۵. Migration Map شناسه‌های متعارض

برای جلوگیری از شکستن لینک‌ها، فایل‌ها فعلاً Rename نمی‌شوند. Registryها از `Canonical Registry Key` برای تفکیک استفاده می‌کنند.

| Legacy/Visible ID | Canonical Registry Key | Source | وضعیت |
|---|---|---|---|
| `DEC-010` | `DEC-V7-010-PROVIDER-REGISTRY` | `../04_Decisions/DEC-010-Global-Provider-Registries.md` | Legacy ID collision؛ Source metadata=`Needs Review` |
| `DEC-010-UIR09-CONSOLIDATED` | `DEC-UIR09-010-CONSOLIDATED` | `../04_Decisions/DEC-010-UIR09-Consolidated-Workspace-And-Operational-UX.md` | Active |
| `DEC-016` | `DEC-V8-016-SEARCH-HISTORY` | `../04_Decisions/DEC-016-Search-And-Recent-History-Consolidation.md` | Agreed |
| `DEC-016-UIR10-CONSOLIDATED` | `DEC-UIR10-016-CONSOLIDATED` | `../04_Decisions/DEC-016-UIR10-Consolidated-Alpha-Workspace-Refinement.md` | Agreed |

هر تعارض جدید باید قبل از ایجاد سند تازه در این جدول و [Open Item Registry](Open_Item_Registry.md) ثبت شود.

## ۶. قواعد Canonical Reference

- `canonical: true` فقط برای مرجع معتبر فعلی همان Scope استفاده می‌شود.
- یک Scope می‌تواند چند سند Active مکمل داشته باشد، اما نباید دو مرجع متناقض بدون Conflict Record داشته باشد.
- Registry مرجع تفصیلی نیست؛ Source Document مرجع حقیقت است.
- Prototype، Screenshot، ZIP، Commit Message و Conversation به‌تنهایی Canonical نیستند.
- کد فعلی Evidence وضعیت اجراست و Decision Active را خودکار باطل نمی‌کند.

## ۷. Banner اسناد Superseded یا Historical

```text
Status: Superseded | Historical
Superseded By: <relative-link-or-N/A>
Historical Purpose: <why-this-document-is-retained>
Current Canonical Reference: <relative-link>
```

## ۸. سیاست Migration

Migration Metadata به‌صورت تدریجی و در Change Setهای موضوعی انجام می‌شود:

1. Registry و ID Map؛
2. اسناد Active و Agreed؛
3. اسناد Superseded/Historical؛
4. Indexها و Backlinkها؛
5. Validation لینک و Duplicate ID؛
6. عدم Rename فیزیکی تا آماده‌شدن Link Migration Map.
