# Change Set جامع — CAS UI Workspace v8

| مشخصه | مقدار |
|---|---|
| شناسه | `CS-WORKSPACE-V8` |
| خط مبنا تاریخی | `CAS UI Workspace v7` |
| نسخه هدف | `CAS UI Workspace v8 — Through Iteration 12` |
| وضعیت | `Consolidated` |
| مجوز Production | فقط پس از تکمیل Specification اجرایی هر ماژول |
| مرجع بالادستی | `../00_Project/V8_Canonical_Baseline.md` |

## دامنه نسخه ۸

1. Workspace عملیاتی و Action-First
2. Widget System و Dashboard Governance
3. Personal Task با مالک مستقل
4. Calendar و Attendee Selector مقیاس‌پذیر
5. تفکیک Invitation، Self Task و Assigned Action
6. Conversation مبتنی بر Odoo Mail/Discuss/Bus
7. Overlay و Focus هماهنگ با Odoo UI Services
8. Command Palette مشترک Search و Recent History
9. Native Scroll در Routeهای عادی
10. Scroll مستقل Conversation List و Message Body
11. Notification Center مستقل با Reuse Odoo
12. Dynamic Work Report مبتنی بر Form Engine
13. Shift-based Reporting
14. Multi-assignment Composite Sections
15. Applicability قابل Required/Optional/Disabled
16. Delegated Work Report Access
17. Activity Catalog مستقل

## تاریخچه Iterationها

- Iteration 1–4: دسته‌ها، Attendee، Discuss Interaction و Overlay/Focus
- Iteration 5: تراکم Conversation و RTL Calendar Navigation
- Iteration 6: Action Hub Source Chip
- Iteration 7: حذف Search/History Route و Command Palette
- Iteration 8: Native Scroll Routeهای عادی
- Iteration 9: Conversation Internal Scroll
- Iteration 10: داده و سناریوی Scroll طولانی
- Iteration 11: Initial Bottom و Send Anchoring در Conversation
- Iteration 12: Dynamic Shift-based Work Report و Form Engine Integration

## Personal Task

- مالک قطعی: `cas_personal_task`
- Workspace مالک داده نیست.
- Category سیستمی Backend-protected است.
- Category شخصی CRUD و Reorder دارد.
- حذف Category Taskها را منتقل می‌کند.
- Self Task از Calendar به Personal Task Service می‌رود.

## Calendar

- Directory Server-side و Purpose-aware است.
- Invitation و Assignment Permission جدا هستند.
- Self Task در Personal Task ایجاد می‌شود.
- Task برای دیگری در Action Hub ایجاد می‌شود.
- Command UUID و Idempotency لازم است.
- Partial Failure باید تفصیلی باشد.
- Timezone و Jalali صحیح و استاندارد Odoo باقی می‌ماند.

## Conversations

- Message Model موازی ساخته نمی‌شود.
- Odoo Mail/Discuss/Bus Reuse می‌شود.
- Route Scroll کلی ندارد.
- List و Message Body Scroll مستقل دارند.
- Initial Position در آخرین پیام است.
- Send در Near-bottom انتها را حفظ می‌کند.
- Extension فقط برای Gap تأییدشده است.

## Search و Recent History

- Routeهای `global-search-page` و `recent-history` حذف‌اند.
- `history.read` حذف است.
- Capability ابزار: `search.use`.
- Query خالی Recent Resourceهای مجاز را نشان می‌دهد.
- Provider Permission منبع را enforce می‌کند.
- ماژول مستقل `cas_recent_history` ساخته نمی‌شود.

## Notifications

- `notifications-center` Route مستقل است.
- Odoo Mail/Discuss/Activity/Bus زیرساخت Delivery است.
- `cas_notification_core` کامل تصویب نشده است.
- CAS فقط Deep Link، Severity، Action Metadata یا Aggregation Gap واقعی را Extend می‌کند.
- Gap Analysis اجباری است.

## Dashboard Administration

- Dashboard Management Center برای ادمین الزامی است.
- Configuration در Scope System، Company و Role/Profile نسخه‌بندی می‌شود.
- Preview، Publish، Rollback و Reset دارد.
- Company Policy می‌تواند Lock کند.
- کاربر عادی در v8 فقط Reorder مجاز دارد.

## Work Report — Iteration 12

- هر شخص و Shift Occurrence حداکثر یک Report دارد.
- Shift عبوری از نیمه‌شب یک Report است.
- چند Assignment یک Report ترکیبی با Sectionهای مستقل می‌سازد.
- Applicability: Required/Optional/Disabled.
- Disabled هیچ Form، Draft یا Reminder شخصی ندارد.
- Access می‌تواند مستقل از زیردستی تفویض شود.
- Activity Catalog مستقل است.
- Form Engine ساختار و Answer را مالک است؛ Work Report Lifecycle را مالک نیست.

## مالکیت‌های قطعی

| دامنه | مالک |
|---|---|
| Workspace UI/Preferences | `cas_workspace` |
| Provider Contract | `cas_workspace_contract` |
| Personal Task | `cas_personal_task` |
| Organization Scope | `cas_organization_core` |
| Activity Catalog | `cas_activity_catalog` |
| Work Report | `cas_work_report` |
| Conversation/Notification Delivery | Odoo Mail/Discuss/Bus |

## امنیت

- No broad `sudo`
- Capability + ACL + Record Rule + Method Check
- Purpose-aware Organization Scope
- Provider Permission
- Multi-company isolation
- Section/Field filtering
- Access Grant expiry/revocation
- Secure Export و Attachment
- Audit

## Migrationهای لازم

- Route/Navigation v7 → v8
- Dashboard Preference/Version
- Personal Task Ownership
- Search/History References
- Static Work Report → Shift Report + Sections + Form Submission
- Form Snapshot Revision
- Reviewer Answer Access
- Provider Keys و Deep Links

## تست‌های Regression

- نبود Routeهای حذف‌شده
- Command Palette و Odoo Shortcut Integration
- Search/History leakage
- Provider Partial Failure
- Dashboard Publish/Lock/Rollback
- Native Scroll و Conversation Scroll
- Overlay Focus/Escape
- Calendar Idempotency و Permission
- Shift crossing midnight
- Multi-assignment Report
- Disabled Applicability
- Delegated Section Access
- Notification Odoo Reuse
- RTL، Timezone، Mobile و Accessibility

## شرط `Implementation Ready`

1. API Contract هر ماژول
2. Security کامل
3. Migration و Rollback
4. Test Strategy و Acceptance Criteria
5. Odoo 19 Verification برای Discuss/Notification
6. Performance و Observability
7. تطبیق Traceability Matrix

تصمیم‌های محصولی و مالکیت‌ها Consolidated هستند؛ جزئیات اجرایی باز نباید Baseline v8 را کاهش دهند.