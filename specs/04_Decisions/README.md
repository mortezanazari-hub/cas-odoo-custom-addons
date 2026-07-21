# 04 — Decisions

این بخش Decision Recordهای مشترک پروژه را نگهداری می‌کند. مرجع فعال تصمیم‌ها `Workspace v8 through iteration 12` است.

## Decisionهای پایه

- [`DEC-001` — Workspace عملیاتی و Action-First است](DEC-001-Workspace-Is-Operational.md)
- [`DEC-002` — SLA فنی در UI کاربر عادی نمایش داده نمی‌شود](DEC-002-No-SLA-In-Employee-UI.md)
- [`DEC-003` — فرهنگ فعالیت و Snapshot استاندارد می‌شود](DEC-003-Activity-Standardization.md)

## Decisionهای منشأگرفته از v7 و معتبر در v8

- [`DEC-004` — سیستم Widget میزکار](DEC-004-Workspace-Widget-System.md)
- [`DEC-005` — گفتگو قابلیت سطح اول است](DEC-005-Conversations-Are-First-Class.md)
- [`DEC-006` — Theme و خوانایی](DEC-006-Workspace-Theme-And-Readability.md)
- [`DEC-007` — Sidebar جمع‌شونده](DEC-007-Collapsible-Sidebar.md)
- [`DEC-008` — تقویم تعاملی](DEC-008-Embedded-Calendar.md)
- [`DEC-009` — Route و Capability عمومی](DEC-009-Workspace-Route-And-Capability-Expansion.md) — `Partially Superseded by DEC-016`
- [`DEC-010` — Provider Registry مشترک](DEC-010-Global-Provider-Registries.md)
- [`DEC-011` — تفکیک Task، Action، Notification و History](DEC-011-Separate-Task-Action-Notification-History.md)

## Decisionهای Workspace v8

- [`DEC-012` — حاکمیت دسته‌های Personal Task](DEC-012-Personal-Task-Category-Governance.md)
- [`DEC-013` — Attendee و Assignment Authorization](DEC-013-Calendar-Attendee-Selection-And-Assignment-Authorization.md)
- [`DEC-014` — Reuse Discuss و تعامل پیام](DEC-014-Discuss-Reuse-And-Message-Interaction.md)
- [`DEC-015` — Overlay و Focus](DEC-015-Overlay-Layering-And-Focus-Management.md)
- [`DEC-016` — ادغام Search و Recent History](DEC-016-Search-And-Recent-History-Consolidation.md)
- [`DEC-017` — Work Report از Form Engine استفاده می‌کند](DEC-017-Work-Report-Domain-Uses-Form-Engine.md)
- [`DEC-018` — حاکمیت و مدیریت داشبورد](DEC-018-Dashboard-Administration-And-Governance.md)
- [`DEC-019` — گزارش کار Shift-based و Applicability](DEC-019-Work-Report-Applicability-And-Shift-Period.md)
- [`DEC-020` — دسترسی تفویض‌شده گزارش کار](DEC-020-Delegated-Work-Report-Access.md)

## قواعد

- Decision نسخه قبلی در صورت تعارض با Baseline v8 مرجع نیست.
- تصمیم محصولی با محدودیت کد موجود تضعیف نمی‌شود.
- Decision باید Context، تصمیم، گزینه‌های ردشده، اثر و پیامد را ثبت کند.
- وضعیت `Agreed` به‌تنهایی معادل `Implementation Ready` نیست.

## Decisionهای کلیدی Consolidation

- Workspace فقط مالک UI Configuration و Preference است.
- Personal Task در `cas_personal_task` است.
- Organization Scope در `cas_organization_core` است.
- Activity Catalog مستقل است.
- Notification زیرساخت Odoo را Reuse می‌کند.
- Search/History صفحه مستقل ندارند.
- Work Report براساس Shift Occurrence است.
- Multi-assignment یک گزارش ترکیبی می‌سازد.
- Report Access می‌تواند مستقل از زیردستی تفویض شود.
- Dashboard Management Center برای ادمین الزامی است.