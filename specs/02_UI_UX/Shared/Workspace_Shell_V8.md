# Shared Specification — Workspace Shell v8

| مشخصه | مقدار |
|---|---|
| شناسه | `SHARED-WORKSPACE-SHELL-V8` |
| نسخه | `v8 through iteration 12` |
| وضعیت | `Consolidated` |
| مالک | `cas_workspace` |
| جایگزین مرجع فعال | `Shared/Workspace_Shell.md` نسخه ۷ |

## هدف

Workspace Shell چارچوب مشترک تمام نقش‌ها و Routeهای CAS است. Shell باید تجربه‌ای اختصاصی، یکپارچه و غیرقابل‌اشتباه با Backend استاندارد Odoo فراهم کند، بدون تغییر Odoo Core.

## اجزا

- Collapsible Sidebar
- Topbar
- Breadcrumb / Context Title
- Route Outlet
- Command Palette
- Notification Entry
- User Menu
- Theme و Density Resolver
- Overlay Coordination
- Route-level Scroll Policy
- Global Error Boundary
- Provider Availability Indicator

## Navigation

Navigation از یک فهرست ثابت و بدون Permission ساخته نمی‌شود. هر Item باید شامل این موارد باشد:

- Route Key
- Label و Icon
- Capability
- Provider Availability
- Company/Role Scope
- Order
- Badge Provider اختیاری
- Deep Link Contract

### Routeهای اصلی v8

- Workspace Home
- Personal Tasks
- Calendar
- Conversations
- Notifications Center
- Work Report، براساس Applicability یا Access Scope
- Provider Routes
- Dashboard Management Center برای ادمین

### Routeهای حذف‌شده

- `global-search-page`
- `recent-history`

## Command Palette

Command Palette از این Entry Pointها باز می‌شود:

- Topbar
- Hero Workspace
- Keyboard Shortcut

Behavior:

- Query خالی: Recent Items مجاز و Quick Actions
- Query غیرخالی: نتایج Providerها
- Permission: Capability ابزار + Permission منبع
- Keyboard Navigation کامل
- Focus Trap و Focus Restore
- Grouping براساس Provider یا Resource Type
- Partial Failure مستقل هر Provider

میانبر صفحه‌کلید باید با Command System استاندارد Odoo هماهنگ شود و Listener سراسری متعارض ایجاد نکند.

## Scroll Contract

| Context | Scroll |
|---|---|
| Routeهای عادی | Native Page Scroll |
| Workspace Home | Native Page Scroll؛ Widget داخلی فقط در صورت Contract |
| Conversations | بدون Scroll کلی |
| Conversation List | Internal Scroll |
| Message Body | Internal Scroll و شروع از آخرین پیام |
| Modal / Dialog | Scroll داخلی کنترل‌شده |
| Command Palette | Results Scroll داخلی |

پس از Send در Conversation، انتهای Chat حفظ می‌شود مگر کاربر عمداً از انتها فاصله گرفته باشد.

## Overlay Contract

Primitiveها از Odoo UI Services Reuse می‌شوند. Workspace فقط Policy هماهنگی را اعمال می‌کند:

- Stack Order
- Parent/Child Overlay
- Focus Trap
- Focus Restore
- Escape فقط Overlay بالایی را می‌بندد
- Outside Click مطابق Contract همان Overlay
- Scroll Lock در Modalهای لازم
- عدم دسترسی Tab به محتوای پشت Modal
- Tooltip و Dropdown زیر Dialog پنهان نشوند

ماژول مستقل Overlay در v8 ایجاد نمی‌شود.

## Theme و Preference

Resolution:

```text
System Default
→ Company Policy
→ Role/Profile Default
→ User Preference
```

Preferenceهای مجاز:

- Theme
- Accent، در محدوده Policy
- Density
- Font Scale
- Sidebar State
- Widget Order

Company Policy می‌تواند هر مورد را Lock کند.

## Notifications

- Topbar Entry به Notification Center مستقل متصل است.
- داده از Odoo Mail/Discuss/Bus و Extensionهای Gap-driven دریافت می‌شود.
- Shell مالک Notification Record نیست.

## Provider Availability

در نبود Provider:

- Route در Navigation غیرفعال یا پنهان می‌شود.
- Deep Link باید Unavailable State قابل‌فهم نشان دهد.
- خطای Provider نباید Shell را Crash کند.
- Admin Diagnostic باید Provider Key و وضعیت را نمایش دهد.

## Security

- Navigation فقط UX است.
- Backend باید ACL، Record Rule و Method Check را enforce کند.
- Shell حق افزایش Scope ندارد.
- Search و Badge Providerها بدون `sudo` غیرمجاز اجرا می‌شوند.
- Multi-company Context باید در تمام Provider Callها منتقل شود.

## RTL و Accessibility

- Sidebar، Breadcrumb، Calendar Control و Pagination RTL واقعی دارند.
- Focus Visible اجباری است.
- تمام Shortcutها Alternative قابل کلیک دارند.
- Text کاربردی کمتر از ۱۲ پیکسل ممنوع است.
- Contrast با Theme Policy کنترل می‌شود.

## Observability

- Provider Latency
- Provider Error Rate
- Route Load Failure
- Search Partial Failure
- Overlay/Focus Error Diagnostics
- Invalid Deep Link

هیچ Logی نباید محتوای محرمانه رکوردها را بدون ضرورت ثبت کند.

## معیار پذیرش

1. Routeهای Search و History مستقل وجود نداشته باشند.
2. Navigation براساس Capability و Provider ساخته شود.
3. Shortcut با Odoo Command System تعارض نداشته باشد.
4. Routeهای عادی Native Scroll داشته باشند.
5. Conversation Scroll Contract رعایت شود.
6. Overlay Stack، Escape و Focus قابل پیش‌بینی باشند.
7. Preference Lock سازمانی قابل دورزدن از Client نباشد.
8. خرابی Provider Shell را از کار نیندازد.