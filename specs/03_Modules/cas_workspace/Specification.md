# Module Specification — `cas_workspace`

| مشخصه | مقدار |
|---|---|
| Document ID | `MOD-CAS-WORKSPACE-SPEC` |
| Document Type | Module Specification |
| Title | `cas_workspace` Module Specification |
| Status | `Active` |
| Document Version | `1.1` |
| Created At | `N/A` |
| Updated At | `2026-07-21` |
| Owner | Workspace Experience |
| Reviewers | Architecture Governance, Product Design, Security |
| Source UI Review Cycle | `CAS UI Review Cycle 9` |
| Source Iteration | `Through Iteration 13` |
| Effective From | `2026-07-21` |
| Supersedes | بخش‌های متعارض نسخه قبلی همین سند |
| Superseded By | `N/A` |
| Domain Owner | Workspace Experience |
| Affected Modules | `cas_workspace`, `cas_workspace_contract`, all UI-producing custom addons as consumers |
| Implementation Status | `Gap Identified` |
| UI Validation Status | `Pending Revalidation` |
| Related Decisions | `DEC-010-UIR09-CONSOLIDATED` |
| Related Observations | `OBS-UIR09-NAV-001`, `OBS-UIR09-DASH-001..004`, `OBS-UIR09-LAYOUT-001`, `OBS-UIR09-CSS-001` |
| Related Change Sets | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` |
| Related Architecture | `ARCH-CSS-DS-001` |

## 1. Purpose

`cas_workspace` پوسته و تجربه مشترک CAS را ارائه می‌کند و فقط مالک تنظیمات ظاهری، Layout، Preference، Dashboard Governance و Design System مشترک است.

## 2. In Scope

- Workspace Shell
- Router Adapter و Navigation Resolution
- Tree Navigation، Parent Resolution و Breadcrumb
- Command Palette UI و Orchestration
- Theme، Density و Sidebar Preference
- Widget Layout، Visibility، User Order و Settings
- Shortcut Customization
- Dashboard Configuration، Versioning و Publish
- Overlay Coordination بر پایه Odoo UI Services
- Recent Resource Reference
- Provider Health Presentation
- Notification Center View Composition
- Shared Design Tokens، CSS foundation، layout primitives و shared UI components
- Odoo asset ordering contract برای UIهای CAS

## 3. Out of Scope

- ذخیره Personal Task، Action، Event، Report، Message یا Document
- اعمال Business Rule Providerها
- کپی Permission Logic دامنه‌ها
- ساخت Notification Delivery موازی
- ساخت Message Model موازی
- استفاده از `sudo` برای جمع‌آوری داده غیرمجاز
- ذخیره Business Data در Theme، Widget settings یا Workspace preferences
- ایجاد Styleهای Domain-specific بدون مالکیت ماژول مربوطه

## 4. Domain Ownership

`cas_workspace` مالک موارد زیر است:

- Shell و Navigation presentation؛
- UI preferences؛
- Dashboard layout/settings؛
- Shared Design Tokens و Primitiveها؛
- Asset layering و CSS architecture governance.

هر Business Module مالک Componentهای Domain خود است، اما MUST از `ARCH-CSS-DS-001` تبعیت کند.

## 5. Dependencies

- `cas_workspace_contract`
- Odoo Web Services و Registries
- Odoo Dialog/Command Services
- Provider Bridgeها
- Mail/Discuss/Bus برای Conversation و Notification
- UI modules به‌عنوان مصرف‌کننده shared assets

## 6. Entities and Models

### 6.1 Workspace Preference

- user
- company
- theme
- density
- font scale
- sidebar state
- navigation collapse state
- widget visibility
- widget order
- shortcut order
- widget settings
- command center visibility
- configuration version source

Preference payload MUST versioned باشد و Company Policy lock را دور نزند.

### 6.2 Dashboard Configuration

- name
- company scope
- role/profile scope
- version
- status
- effective date
- published snapshot
- change reason

### 6.3 Dashboard Widget Placement

- configuration
- provider key
- widget key
- position
- size
- required
- draggable
- locked
- settings JSON validated against Provider Schema

### 6.4 Recent Resource Reference

- user
- company
- provider key
- resource type/id
- deep link
- display fallback
- last opened at
- retention metadata

### 6.5 Design Token Registry

Design Tokenها Business Model ایجاد نمی‌کنند. Source of truth باید در shared CSS/SCSS assets باشد. فقط Theme/Density preference در Workspace persistence ذخیره می‌شود.

## 7. State Machines

Dashboard Configuration lifecycle:

```text
Draft → Published → Superseded/Rolled Back
```

Preference schema lifecycle:

```text
Current Version → Migrated Version → Validated Defaults
```

## 8. Services and Commands

- `resolve_navigation(user, company)`
- `resolve_dashboard(user, company, role_profile)`
- `resolve_preferences(user, company)`
- `search_palette(query, cursor, context)`
- `record_recent_resource(reference)`
- `publish_dashboard_configuration(configuration, reason)`
- `rollback_dashboard_configuration(version, reason)`
- `reset_user_preferences(scope)`
- `resolve_widget_settings(widget_key, user, company, role_profile)`

نام نهایی API در سند API مستقل تثبیت می‌شود.

## 9. Queries

- authorized navigation tree
- resolved dashboard configuration
- resolved user/company/role preference overlay
- provider health summary without unauthorized metadata
- recent resources filtered by provider permission

## 10. Events

- `workspace.preference_changed`
- `workspace.dashboard.published`
- `workspace.dashboard.rolled_back`
- `workspace.navigation.changed`

## 11. Provider Interfaces

Providerها MUST schema تنظیمات، capability requirement، data query و empty/error state را اعلام کنند. Workspace فقط orchestration و rendering contract را مالک است.

## 12. ACL

گروه‌های مفهومی:

- Workspace User
- Workspace Administrator
- Dashboard Publisher
- Dashboard Auditor

## 13. Record Rules

Preference فقط برای مالک رکورد یا Administrator مجاز است. Company-scoped configuration باید multi-company isolation را رعایت کند.

## 14. Method Checks

Publish، Rollback، Bulk Reset، Company Lock و administrative preference override نیازمند Method Check و Audit هستند.

## 15. Field/Section Security

Widget، shortcut، navigation node، title، count و metadata فقط پس از capability/provider filtering render می‌شوند. مخفی‌کردن CSS یا route absence کنترل امنیتی محسوب نمی‌شود.

## 16. Multi-company

Resolution order:

```text
System Default
→ Company Policy
→ Role/Profile Default
→ User Preference
```

Company Lock در Backend enforce می‌شود و Cross-company cache isolation الزامی است.

## 17. Audit

Publish، Rollback، policy lock، bulk reset و administrative override باید actor، timestamp، scope، reason و old/new version را ثبت کنند.

## 18. CSS and Design System Contract

تمام Styleهای `cas_workspace` و مصرف‌کنندگان آن MUST با `specs/05_Architecture/Workspace_CSS_And_Design_System_Contract.md` منطبق باشند.

الزام‌های اصلی:

- shared tokens برای color، spacing، radius، shadow، typography، controls، z-index و breakpoints؛
- CAS namespace برای selectorها؛
- ممنوعیت inline style ثابت و static JS style mutation؛
- ممنوعیت `!important` بدون Exception Record؛
- shared primitives برای Widget، Form field، Button، Table، Dialog، State و Searchable Select؛
- Odoo asset bundle order صریح؛
- logical properties برای RTL؛
- visual regression و lint evidence.

## 19. Migration

Migration باید حداقل پوشش دهد:

- تبدیل Routeهای Cycle 7 به Routeهای Cycle 8/9؛
- حذف ارجاع مستقل Search و History؛
- تبدیل Preferenceهای Layout قدیمی؛
- migration کلیدهای navigation flat به tree؛
- migration widget visibility، shortcuts و settings schema؛
- حفظ User Preferenceهای قابل نگاشت؛
- تعیین Default برای تنظیمات نامعتبر؛
- ثبت نسخه Dashboard اولیه؛
- inventory و migration مرحله‌ای CSS legacy، hardcoded values، inline styles، `!important` و Odoo overrides؛
- deprecation window برای legacy classes.

## 20. Performance

- permission-safe caching با invalidation روی user/company/capability change؛
- split asset bundles و جلوگیری از stylesheet monolithic؛
- جلوگیری از duplicate shared component CSS؛
- no global costly selectors؛
- جلوگیری از layout shift در Asset load.

## 21. Observability

- provider failure telemetry؛
- dashboard resolution errors؛
- asset build/lint failures؛
- visual regression reports؛
- deprecated selector usage تا پایان migration.

## 22. Failure Modes

- invalid preference → validated default؛
- unavailable provider → scoped unavailable state؛
- revoked capability → route/action denied and refreshed؛
- missing token/shared asset → build/lint failure، نه hardcoded silent fallback؛
- Odoo upgrade breaks override → regression failure and blocked release.

## 23. Test Strategy

- Python: Resolution، Lock، ACL و Publish
- JS/HOOT: Router، Command Palette، Overlay، Widget settings و Scroll
- Tour: Admin Publish تا User Resolution
- Security: Direct RPC، Cross-company و Provider Failure
- Accessibility: Keyboard، Focus، Zoom 200%، Long Persian Text و RTL
- CSS lint: namespace، selector depth، forbidden IDs، inline styles، undocumented `!important`
- Visual regression: Desktop، Tablet، Mobile و shared components
- Asset: Odoo bundle build، dependency order و cache invalidation

## 24. Acceptance Criteria

- حذف Workspace باعث حذف داده Domainها نشود.
- Provider Failure محلی باشد.
- Search Permission منبع را رعایت کند.
- Dashboard Policy قابل Version و Rollback باشد.
- User Preference Company Lock را دور نزند.
- Routeهای مستقل Search/History وجود نداشته باشند.
- Navigation tree capability-aware باشد.
- Widget visibility و shortcut customization فقط UI preference را تغییر دهند.
- تغییر spacing/radius/theme با Token و بدون تغییر Business Model ممکن باشد.
- هیچ selector اختصاصی CAS خارج از Namespace به Odoo leak نکند.
- CSS hiding هرگز جای ACL/Record Rule/Method Check را نگیرد.

## 25. UI Review Sources

- CAS UI Review Cycle 8 — Through Iteration 12
- CAS UI Review Cycle 9 — Through Iteration 13
- `REG-UIR09`
- `ARCH-CSS-DS-001`

## 26. Revalidation Plan

پس از پیاده‌سازی، Workspace باید روی Dashboard، Navigation، Attendance، Work Report، Form Builder، Calendar، Conversations و Mobile/Tablet/Desktop بازآزمایی شود. Evidence باید شامل Commit/PR، tests، lint report، visual regression و role-based screenshots باشد.

تا زمان وجود این شواهد وضعیت اجرا `Gap Identified` و UI Validation برابر `Pending Revalidation` باقی می‌ماند.
