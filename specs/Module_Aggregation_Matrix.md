# ماتریس تجمیع تغییرات ماژول‌ها — Workspace v8

| مشخصه | مقدار |
|---|---|
| نسخه فعال | `CAS UI Workspace v8 — Through Iteration 12` |
| وضعیت | `Consolidated` |
| مرجع بالادستی | `00_Project/V8_Canonical_Baseline.md` |

این فایل نمای اجرایی اثر تصمیم‌های محصول بر ماژول‌هاست. وضعیت `Consolidated` به معنی هماهنگی معماری است، نه مجوز Production.

## وضعیت‌ها

- `Historical`: فقط سابقه نسخه قبلی
- `Agreed`: تصمیم محصولی تأییدشده
- `Consolidated`: مالکیت و معماری هماهنگ شده
- `Needs Implementation Detail`: API، Migration یا Test هنوز کامل نیست
- `Implementation Ready`: تمام اسناد اجرایی کامل و تصویب شده
- `Verified`: اجرا و Acceptance تأیید شده

## ماتریس تصمیم‌ها

| تصمیم / حوزه | مالک اصلی | Integration / Provider | اثر | وضعیت |
|---|---|---|---|---|
| Workspace Action-First / `DEC-001` | `cas_workspace` | تمام Providerها | Shell، Widget، Priority | Consolidated |
| SLA Presentation / `DEC-002` | Domain مالک Deadline | Workspace Renderer | UX Label | Consolidated |
| Activity Standardization / `DEC-003` | `cas_activity_catalog` | Work Report، KPI | Catalog، Snapshot، Proposal | Consolidated |
| Widget System / `DEC-004` | `cas_workspace` | Widget Providers | Registry، Layout | Consolidated |
| Conversations / `DEC-005`, `DEC-014` | Odoo Mail/Discuss/Bus | Discuss Adapter | Reuse، Realtime، UI | Needs Odoo Verification |
| Theme / `DEC-006` | `cas_workspace` | Company Policy | Tokens، Readability | Consolidated |
| Sidebar / `DEC-007` | `cas_workspace` | — | Persistent Preference | Consolidated |
| Calendar / `DEC-008`, `DEC-013` | Calendar Domain | Organization Core، Personal Task، Action Hub | Event، Attendee، Task Link | Needs Implementation Detail |
| Route/Capability / `DEC-009` | `cas_workspace` | Security Model | Partially Superseded | Historical + v8 Mapping |
| Provider Registry / `DEC-010` | `cas_workspace_contract` | Domain Providers | Protocol، Versioning | Consolidated |
| Domain Separation / `DEC-011` | Domain Owners | Workspace | Ownership | Consolidated |
| Personal Task Category / `DEC-012` | `cas_personal_task` | Workspace Provider | CRUD، Security | Consolidated |
| Overlay / `DEC-015` | Odoo UI Services + Workspace Shell | همه صفحات | Focus، Stack، Scroll Lock | Consolidated |
| Search/History / `DEC-016` | `cas_workspace` | Search Providers | Command Palette، History Ref | Consolidated |
| Dynamic Work Report / `DEC-017` | `cas_work_report` | Form، Workflow، Approval | Dynamic Sections، Snapshot | Needs Implementation Detail |
| Dashboard Governance / `DEC-018` | `cas_workspace` | Widget Providers | Admin Center، Versioning | Consolidated |
| Shift Applicability / `DEC-019` | `cas_work_report` | Shift، Organization، Form | Shift Report، Multi-assignment | Consolidated |
| Delegated Access / `DEC-020` | `cas_work_report` | Organization Core | Access Grant، Section Security | Consolidated |
| Notification Reuse | Odoo Mail/Discuss/Bus | CAS Notification Adapter | Gap-driven Extension | Needs Gap Verification |
| File Infrastructure Future | Odoo Attachment فعلی | Document Core | Evidence در v8؛ Redesign آینده | Out of Scope v8 |

## Route و Navigation Migration

| نسخه ۷ | نسخه ۸ | Migration |
|---|---|---|
| `global-search-page` | حذف | Triggerها به Command Palette نگاشت شوند |
| `recent-history` | حذف | Query خالی Palette Recent Items را نشان دهد |
| `history.read` | حذف | Permission منبع هر Resource مرجع است |
| Search Topbar و Hero جدا | یک Overlay مشترک | Entry Pointها به Command Service مشترک متصل شوند |
| Static Navigation | Capability/Provider Navigation | Configuration و Registry Migration |

## مالکیت ماژول‌ها

### `cas_workspace`

مالک:

- Shell
- Dashboard Configuration
- UI Preference
- Command Palette Orchestration
- Recent Resource Reference

مالک نیست:

- Personal Task
- Action
- Event
- Message
- Notification Delivery
- Work Report
- Document
- Organization Assignment

وضعیت: `Consolidated`; API/Migration/Test لازم است.

### `cas_workspace_contract`

- Provider Protocol
- Widget/Search/Action Metadata
- Resource Reference
- Contract Versioning

وضعیت: `Consolidated`; نام و API نهایی لازم است.

### `cas_personal_task`

- Personal Task و Category
- Self-task Calendar Integration
- Workspace Provider

وضعیت: `Consolidated`; Implementation Detail لازم است.

### `cas_action_hub`

- Action سازمانی برای دیگران
- Calendar Assigned Action
- Workspace/Search Provider

وضعیت: مرزبندی `Consolidated`; Specification اجرایی مستقل لازم است.

### `cas_organization_core`

- Effective Assignment
- Reporting Scope
- Delegation سازمانی
- Directory Purpose Scope

وضعیت: `Consolidated`; Domain/API/Security Detail لازم است.

### `cas_activity_catalog`

- Activity Definition
- Proposal
- Evidence Policy Reference
- KPI Mapping Reference

وضعیت: `Consolidated`; Implementation Detail لازم است.

### `cas_work_report`

- Report per Shift Occurrence
- Composite Sections
- Profile و Applicability
- Access Grant
- Evidence Relation
- Reporting Projection

وضعیت: `Consolidated`; Migration و Test Strategy کامل لازم است.

### Form Engine

نیازهای v8 Work Report:

- Form Version Pinning
- Conditional Logic
- Repeatable/Structured Sections، در صورت Profile
- File/Image/Evidence Field Contract
- Immutable Revision/Snapshot
- Typed Reporting Projection
- Reviewer-safe Answer Access

وضعیت: `Needs Implementation Detail`.

### Odoo Mail/Discuss/Bus

- Conversation و Message
- Notification Delivery
- Realtime Update

وضعیت: `Needs Odoo 19 Community Verification`; سیستم موازی ممنوع است.

## امنیت مشترک

- No broad `sudo`
- ACL + Record Rule + Method Check
- Provider Permission
- Multi-company Isolation
- Purpose-aware Organization Scope
- Section/Field Filtering
- Access Grant Expiry/Revocation
- Export Security
- Audit

## Migrationهای اجباری

- Route/Navigation v7 → v8
- Workspace Preference و Dashboard Version
- Personal Task Ownership، در صورت داده قبلی
- Static Work Report → Shift Report + Sections + Form Submission
- Form Snapshot Revision
- Reviewer Answer Access
- Search/History References
- Provider Keys و Deep Links

## تست‌های اجباری

### Workspace

- Command Palette و Shortcut Integration
- Search/History Permission
- Provider Partial Failure
- Dashboard Lock/Publish/Rollback
- Native Scroll و Conversation Scroll
- Overlay Parent/Child و Focus
- RTL و Accessibility

### Work Report

- Shift عبوری از نیمه‌شب
- Idempotent Draft
- Multi-assignment Sections
- Applicability Disabled
- Reviewer/Approver Resolution
- Delegated Access
- Section-level Visibility
- Export Leakage
- Form Version Immutability
- Migration Reconciliation

### Security

- Direct RPC و ID Tampering
- Cross-company
- Search/Count Leakage
- Attachment Leakage
- Expired/Revoked Grant
- Client Capability Tampering

## اسناد مرجع فعال

- `00_Project/V8_Canonical_Baseline.md`
- `00_Project/Traceability_Matrix.md`
- `03_Modules/V8_Module_Ownership_Map.md`
- `03_Modules/V8_Dependency_Map.md`
- `03_Modules/V8_Provider_Registry.md`
- `05_Architecture/Module_Boundaries.md`
- `05_Architecture/Capability_And_Security_Model.md`
- `05_Architecture/Assignment_Model.md`
- `03_Modules/cas_work_report/Specification.md`

## وضعیت نهایی

تصمیم‌های محصولی و مرزبندی معماری نسخه ۸ تا Iteration 12 تجمیع شده‌اند. هیچ ماژولی صرفاً با این ماتریس `Implementation Ready` نیست؛ تکمیل API، Security، Migration و Test Strategy همان ماژول همچنان الزامی است.