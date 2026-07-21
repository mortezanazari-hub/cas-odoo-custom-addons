# Capability and Security Model — CAS Workspace v8

| مشخصه | مقدار |
|---|---|
| وضعیت | `Consolidated` |
| اصل | `UI is not a security boundary` |

## لایه‌های امنیت

```text
Capability / Navigation
→ Group Membership
→ ACL
→ Record Rule
→ Domain Scope Resolver
→ Method Check
→ Field/Section Filtering
→ Audit
```

هر لایه نقش متفاوت دارد و حذف یکی با وجود دیگری مجاز نیست.

## Capability

Capability برای این موارد است:

- نمایش Navigation
- فعال‌کردن Action در UI
- تعیین Provider قابل استفاده
- بهبود UX Forbidden/Unavailable

Capability به‌تنهایی مجوز خواندن یا تغییر رکورد نیست.

## Capabilityهای پایه پیشنهادی

### Workspace

- `workspace.use`
- `workspace.manage_dashboard`
- `workspace.publish_dashboard`
- `workspace.audit_dashboard`

### Search

- `search.use`

`search.use` فقط Palette را باز می‌کند؛ هر Provider Permission منبع را اعمال می‌کند.

### Personal Task

- `personal_task.use`
- `personal_task.manage_categories`

### Calendar

- `calendar.use`
- `calendar.invite`
- `calendar.assign_action`

### Conversations

- `conversation.use`
- Operationهای پیام مطابق Odoo و Policy CAS

### Notifications

- `notifications.use`

### Work Report

Capabilityهای تفصیلی در `cas_work_report/Security.md` ثبت شده‌اند.

## Navigation Resolution

Navigation Item فقط زمانی نمایش داده می‌شود که:

- Capability مجاز باشد.
- Provider/Module فعال باشد.
- Company Context مجاز باشد.
- Route برای نقش یا Profile منتشر شده باشد.

Deep Link مستقیم همچنان Backend Permission را بررسی می‌کند.

## Search Security

- Provider Search در Backend اجرا می‌شود.
- Result Count نیز Permission-aware است.
- Label یا Snippet نباید داده Forbidden را افشا کند.
- Recent Resource هنگام نمایش دوباره Validate می‌شود.

## Organization Scope

Organization Core Scope پایه را می‌دهد، اما Domain Owner Permission نهایی را اعمال می‌کند.

مثال:

- فرد در Directory دیده می‌شود، ولی Report او قابل مشاهده نیست.
- فرد قابل دعوت است، ولی Action قابل تخصیص نیست.

## Section و Field Security

برای Form و Work Report:

- Read کل Record به معنی Read همه Section/Fieldها نیست.
- Backend Serializer یا Service باید Fieldهای غیرمجاز را حذف کند.
- Export و Aggregate نیز همان فیلتر را اعمال می‌کنند.
- Client نباید Field مخفی را دریافت کند و فقط CSS آن را پنهان کند.

## Multi-company

- Company Context Server-side Validate می‌شود.
- Record Ruleهای Company اجباری‌اند.
- Cross-company Role مجوز صریح و Scope محدود دارد.
- Company Switch Cacheهای Scope و Dashboard را invalidate می‌کند.

## Method Check

Methodهای حساس باید Actor، Operation، Scope و State را بررسی کنند:

- Create/Assign
- Submit/Return/Approve
- Publish/Rollback
- Export
- Grant/Revoke Access
- Bulk Reset
- Rebuild Projection

## `sudo`

استفاده از `sudo` فقط در Serviceهای محدود و مستند برای عملیات سیستمی ممکن است؛ نتیجه باید دوباره براساس User Scope Filter شود. `sudo` عمومی در Workspace، Search و Reporting ممنوع است.

## Audit

Audit برای این موارد الزامی است:

- تغییر Security Configuration
- Dashboard Publish/Rollback
- Access Grant Lifecycle
- Approval Decision
- Export حساس
- Unauthorized Attempts
- Cross-company Operations

## Fail-closed

در نبود Rule، Resolver، Provider یا Configuration معتبر:

- دسترسی رد می‌شود.
- سیستم Scope وسیع‌تر فرض نمی‌کند.
- UI پیام Forbidden یا Unavailable مناسب نشان می‌دهد.

## تست‌های اجباری

- Direct RPC
- Guessed IDs
- Cross-company
- Revoked/Expired Delegation
- Search leakage
- Count leakage
- Export leakage
- Attachment leakage
- Section/Field leakage
- Client-side capability tampering
- Cache invalidation after role/company change