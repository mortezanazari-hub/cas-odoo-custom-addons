# DEC-010 — تصمیم تجمیعی Cycle 9 برای Workspace و جریان‌های عملیاتی

| مشخصه | مقدار |
|---|---|
| Document ID | `DEC-010-UIR09-CONSOLIDATED` |
| Document Type | Product / Architecture Decision |
| Title | Consolidated Workspace and Operational UX Decisions for UI Review Cycle 9 |
| Status | `Active` |
| Document Version | `1.0` |
| Created At | `2026-07-21` |
| Updated At | `2026-07-21` |
| Owner | Product Owner |
| Reviewers | Architecture, Security, UI/UX |
| Source UI Review Cycle | `CAS UI Review Cycle 9` |
| Source Iteration | `Through Iteration 13` |
| Effective From | `2026-07-21` |
| Supersedes | Navigation تخت Cycle 8؛ محدودیت Reorder-only برای User Dashboard؛ Work Progress widget baseline |
| Superseded By | `N/A` |
| Domain Owner | Multiple |
| Affected Modules | `cas_workspace`, `cas_work_report`, `cas_activity_catalog`, attendance/shift/overtime domains, form engine |
| Implementation Status | `Planned` |
| UI Validation Status | `Pending Revalidation` |
| Related Observations | `REG-UIR09` |
| Related Change Sets | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` |

## 1. Context

بازنگری Cycle 9 نشان داد ساختار منوی تخت، مسیرهای ناقص Attendance، ثبت فعالیت خارج از Catalog، تنظیمات Dashboard و Fieldهای تخصصی Form Builder برای سناریوهای واقعی سازمان کافی نیستند.

## 2. Problem

- کاربر در صفحات داخلی مسیر بازگشت و Navigation هم‌خانواده ندارد.
- مغایرت حضور برای Employee دامنه نامشخص دارد و اصلاح ممکن است با لاگ خام مخلوط شود.
- Overtime می‌تواند بدون Governance مناسب افشا شود.
- Work Report در نبود Activity Catalog item کاربر را به انتخاب نادرست سوق می‌دهد.
- Dashboard personalization روی خود Widget آشکار و مزاحم است.
- Form Builder منبع Activity و Matrix data را به‌صورت First-class Field ندارد.

## 3. Decision

### 3.1 Workspace Navigation

`cas_workspace` MUST Navigation tree را از Provider Registry دریافت کند. هر Node شامل `key`, `label`, `route`, `parent_key`, `order`, `capability`, `children` و optional badge provider است. Parent click اولین Child مجاز را باز می‌کند. Collapse state فقط UI Preference است.

### 3.2 Attendance Correction

Domain مالک Attendance MUST برای Missing Check-in/Check-out درخواست اصلاح مستقل ایجاد کند. Approval سرپرست MUST رکورد Correction Ledger بسازد و MUST NOT raw device log را تغییر دهد. تمام عملیات Audit می‌شوند.

### 3.3 Delegated Random Audit

دسترسی بازبینی با Capability و Grant زمان‌دار کنترل می‌شود. Reviewer MAY نمونه را دستی یا تصادفی انتخاب کند. مغایرت تأییدشده MUST مستقیماً به CEO workflow route شود. نبود بازبینی، Approval سرپرست را معلق نمی‌کند.

### 3.4 Overtime Governance

`overtime.view_own`, `overtime.request`, `overtime.view_history`, `overtime.cancel_request` مستقل‌اند. Supervisor grant دسترسی پایه را تعیین می‌کند و Approval هر درخواست همچنان Workflow مستقل دارد. Route و Method MUST capability check داشته باشند.

### 3.5 Work Report Activity Proposal

کاربر MAY Activity خارج از Catalog را ثبت کند. Submission MUST بدون انتظار برای Standardization ادامه یابد. Original label، creator، timestamp و mapping history MUST در Audit حفظ شوند. Standardization permission از Report approval جداست.

### 3.6 Form Builder Providers and Matrix

Form Builder MUST Field types زیر را ارائه کند:

- `activity_category_reference`
- `recurring_activity_reference`
- `dynamic_matrix`

`dynamic_matrix` MUST row provider، column schema، cell type، pagination، permission filtering و snapshot policy داشته باشد.

### 3.7 Dashboard Personalization

تنظیمات از آیکون Header Dashboard باز می‌شود. User MAY Widget visibility و shortcuts را تغییر دهد. Workspace MUST فقط Preference را ذخیره کند. هیچ پیام «ویجت مخفی شده» روی Dashboard نمایش داده نمی‌شود. Command Center نیز یک Widget قابل Disable است.

### 3.8 Cycle 9 Layout Baseline

Work Progress widget حذف و Quick Work Report تمام‌عرض می‌شود. Activity selector MUST searchable dropdown باشد. Custom duration input فقط پس از انتخاب Custom Duration نمایش داده می‌شود.

## 4. Rationale

این تصمیم Navigation، Governance، Audit و UX را بدون انتقال Business Ownership به Workspace یکپارچه می‌کند و از ساخت مدل موازی برای داده‌های Attendance، Activity، Overtime یا Form Submission جلوگیری می‌کند.

## 5. Consequences

- Navigation contract و preference schema تغییر می‌کند.
- Attendance correction و delegated audit نیازمند Model/Workflow جدید یا Extension مالک Domain هستند.
- Overtime باید Capability سطح Method داشته باشد.
- Form Builder registry و renderer توسعه می‌یابد.
- Migration برای preferenceهای Dashboard و navigation state لازم است.

## 6. Alternatives Rejected

1. Flat navigation با Back button محلی: مشکل کشف‌پذیری و deep link را حل نمی‌کند.
2. ویرایش raw attendance log: Audit و منشأ داده را مخدوش می‌کند.
3. Role-name hardcode برای Auditor: با Delegation و تغییر سازمان سازگار نیست.
4. جلوگیری از ارسال Report تا استانداردسازی Activity: جریان عملیاتی را متوقف می‌کند.
5. Hide button روی هر Widget: UI را شلوغ و وضعیت شخصی‌سازی را بیش از حد آشکار می‌کند.
6. Matrix به‌صورت Table ساده client-side: برای داده بزرگ و security filtering مناسب نیست.

## 7. Domain Ownership

| Domain | Owner |
|---|---|
| Workspace shell/preferences/navigation | `cas_workspace` / `cas_workspace_contract` |
| Work report lifecycle | `cas_work_report` |
| Activity catalog/standardization | `cas_activity_catalog` |
| Attendance raw and correction ledger | Attendance domain module |
| Shift occurrence | Shift domain module |
| Overtime | Overtime domain module |
| Form schema/rendering | `cas_form_core`, `cas_form_builder`, `cas_dynamic_form` |
| Approval/delegation | `cas_approval_core` and organization capability service |

## 8. Security Impact

- ACL، Record Rule، Method Check و Capability هم‌زمان لازم‌اند.
- Menu hiding کنترل امنیتی محسوب نمی‌شود.
- Provider MUST Count/Title/Metadata leakage را حذف کند.
- Delegation MUST expiry, revocation, scope و audit داشته باشد.
- Matrix row/column/cell MUST قبل از serialization فیلتر شوند.
- broad `sudo()` ممنوع است.

## 9. Migration Impact

- تبدیل navigation preference تخت به tree state.
- افزودن Widget visibility و shortcut preferences با default سازگار.
- backfill احتمالی correction source و audit metadata فقط با Migration plan جداگانه.
- هیچ raw attendance log بازنویسی نمی‌شود.

## 10. Test Impact

Unit، Integration، Security، Multi-company، Regression، RTL، Responsive، Accessibility، Audit و Revalidation اجباری‌اند. سناریوهای دقیق در `REG-UIR09` و Change Set ثبت شده‌اند.

## 11. Acceptance Criteria

1. Parent menu فقط Child مجاز را باز می‌کند و route غیرمجاز Forbidden است.
2. Missing attendance correction raw log را تغییر نمی‌دهد.
3. مغایرت random audit مستقیماً CEO action ایجاد می‌کند.
4. Overtime metadata برای کاربر فاقد Capability نشت نمی‌کند.
5. Activity پیشنهادی مانع Report submission نیست.
6. Matrix با dataset بزرگ server-side کار می‌کند.
7. Dashboard preference فقط در user scope مجاز اعمال می‌شود و company lock را نقض نمی‌کند.
8. Searchable Activity dropdown و Custom Duration بدون overlap در breakpointهای پشتیبانی‌شده کار می‌کنند.
