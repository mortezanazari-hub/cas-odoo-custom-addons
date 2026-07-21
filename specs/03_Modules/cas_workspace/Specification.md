# Module Specification — `cas_workspace`

| مشخصه | مقدار |
|---|---|
| وضعیت محصول | `Agreed` |
| وضعیت اجرا | `Needs API/Security/Migration/Test Completion` |
| نسخه هدف | `v8 through iteration 12` |
| مالک دامنه | Workspace Experience |

## مسئولیت

`cas_workspace` پوسته و تجربه مشترک CAS را ارائه می‌کند و فقط مالک تنظیمات ظاهری، Layout، Preference و Dashboard Governance است.

## مسئولیت‌های مجاز

- Workspace Shell
- Router Adapter و Navigation Resolution
- Command Palette UI و Orchestration
- Theme، Density و Sidebar Preference
- Widget Layout و User Order
- Dashboard Configuration، Versioning و Publish
- Overlay Coordination بر پایه Odoo UI Services
- Recent Resource Reference
- Provider Health Presentation
- Notification Center View Composition

## مسئولیت‌های ممنوع

- ذخیره Personal Task، Action، Event، Report، Message یا Document
- اعمال Business Rule Providerها
- کپی Permission Logic دامنه‌ها
- ساخت Notification Delivery موازی
- ساخت Message Model موازی
- استفاده از `sudo` برای جمع‌آوری داده غیرمجاز

## مدل‌های مفهومی

### Workspace Preference

- user
- company
- theme
- density
- font scale
- sidebar state
- widget order
- configuration version source

### Dashboard Configuration

- name
- company scope
- role/profile scope
- version
- status
- effective date
- published snapshot
- change reason

### Dashboard Widget Placement

- configuration
- provider key
- widget key
- position
- size
- required
- draggable
- locked
- settings JSON validated against Provider Schema

### Recent Resource Reference

- user
- company
- provider key
- resource type/id
- deep link
- display fallback
- last opened at
- retention metadata

## سرویس‌ها

- `resolve_navigation(user, company)`
- `resolve_dashboard(user, company, role_profile)`
- `resolve_preferences(user, company)`
- `search_palette(query, cursor, context)`
- `record_recent_resource(reference)`
- `publish_dashboard_configuration(configuration, reason)`
- `rollback_dashboard_configuration(version, reason)`
- `reset_user_preferences(scope)`

نام نهایی API در سند API مستقل تثبیت می‌شود.

## Preference Resolution

```text
System Default
→ Company Policy
→ Role/Profile Default
→ User Preference
```

Lock سازمانی باید در Backend enforce شود.

## امنیت

گروه‌های مفهومی:

- Workspace User
- Workspace Administrator
- Dashboard Publisher
- Dashboard Auditor

Publish، Rollback و Bulk Reset نیازمند Method Check و Audit هستند.

## Integration

- `cas_workspace_contract`
- Odoo Web Services و Registries
- Odoo Dialog/Command Services
- Provider Bridgeها
- Mail/Discuss/Bus برای Conversation و Notification

## Migration

Migration باید حداقل پوشش دهد:

- تبدیل Routeهای v7 به Routeهای v8
- حذف ارجاع مستقل Search و History
- تبدیل Preferenceهای Layout قدیمی
- حفظ User Preferenceهای قابل نگاشت
- تعیین Default برای تنظیمات نامعتبر
- ثبت نسخه Dashboard اولیه

## Test Strategy

- Python: Resolution، Lock، ACL و Publish
- JS/HOOT: Router، Command Palette، Overlay و Scroll
- Tour: Admin Publish تا User Resolution
- Security: Direct RPC، Cross-company و Provider Failure
- Accessibility: Keyboard، Focus و RTL

## معیار پذیرش

- حذف Workspace باعث حذف داده Domainها نشود.
- Provider Failure محلی باشد.
- Search Permission منبع را رعایت کند.
- Dashboard Policy قابل Version و Rollback باشد.
- User Preference Company Lock را دور نزند.
- Routeهای مستقل Search/History وجود نداشته باشند.