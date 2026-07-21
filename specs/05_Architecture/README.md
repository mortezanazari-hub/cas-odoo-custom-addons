# 05 — Architecture

این بخش Architecture Contractهای فعال CAS را نگهداری می‌کند. آخرین چرخه فعال بازنگری UI برابر `CAS UI Review Cycle 9 — Through Iteration 13` است؛ بااین‌حال تصمیم‌ها و قراردادهای Active چرخه‌های قبلی تا زمان Supersede صریح معتبر می‌مانند.

## معماری‌های پایه

- [System Context](System_Context.md)
- [Domain Model](Domain_Model.md)
- [Module Boundaries](Module_Boundaries.md)
- [Data Flow](Data_Flow.md)
- [Integration Map](Integration_Map.md)
- [Assignment Model](Assignment_Model.md)
- [Capability and Security Model](Capability_And_Security_Model.md)
- [Provider Architecture](Provider_Architecture.md)
- [Dashboard Configuration Architecture](Dashboard_Configuration_Architecture.md)
- [Odoo Notification Gap Analysis](Odoo_Notification_Gap_Analysis.md)
- [Workspace CSS and Design System Contract](Workspace_CSS_And_Design_System_Contract.md)

## قراردادهای تخصصی Cycle 8 که همچنان Active هستند

- [Interaction و Integration Contracts](V8-Interaction-And-Integration-Contracts.md)
- [Search، Recent History و Scroll Contracts](V8-Search-History-And-Scroll-Contracts.md)
- [معماری Work Report مبتنی بر Form Engine](Work_Report_Form_Engine_Architecture.md)

## قرارداد فعال CSS و Design System

`Workspace_CSS_And_Design_System_Contract.md` برای تمام Custom Addonهایی که UI تولید می‌کنند الزام‌آور است و Design Token، Namespace، Asset layering، Responsive، RTL، Shared Components، Odoo override، `!important`، Inline Style، Visual Regression و Definition of Done را تعیین می‌کند.

## سند تاریخی

- `Workspace_UI_Integration_Notes.md` مرجع تاریخی Cycle 7 است و در تعارض با معماری‌های Active مرجع اجرا نیست.

## اصول

- No Core Edit
- Domain Ownership صریح
- Reuse Odoo before Rebuild
- Provider-based Integration
- Fail-closed Security
- Effective-dated Organization Scope
- Shift-based Work Report
- Immutable Historical Snapshot
- Idempotent Cross-domain Commands
- Multi-company Isolation
- Token-driven and namespaced CSS
- Shared UI primitives before module-specific styling

## آمادگی اجرا

Architecture Contract مسیر طراحی را تثبیت می‌کند، اما هر Module برای `Implementation Ready` شدن به API، Security، Migration، Test Strategy و شواهد انطباق CSS مستقل نیاز دارد.
