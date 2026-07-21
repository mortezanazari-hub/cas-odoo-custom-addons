# Dashboard Configuration Architecture

| مشخصه | مقدار |
|---|---|
| وضعیت | `Consolidated` |
| Decision | `DEC-018` |
| مالک | `cas_workspace` |

## هدف

Dashboard Configuration باید UI را در سطح System، Company، Role/Profile و User کنترل کند، بدون اینکه داده Widgetها را به Workspace منتقل کند.

## مدل Resolution

```text
System Default
→ Company Policy
→ Role/Profile Default
→ User Preference
```

هر Property همراه این Metadata Resolve می‌شود:

- value
- source level
- source record/version
- locked
- reason

## Configuration Version

هر Publish یک Snapshot غیرقابل‌ویرایش ایجاد می‌کند:

- version number
- effective date
- scope
- placements
- locks
- provider contract versions
- publisher
- reason
- published at

ویرایش فقط روی Draft جدید انجام می‌شود.

## Scope

- Global/System
- Company
- Role/Profile
- User Preference

در صورت چند Role/Profile، Conflict Policy باید Deterministic و Explainable باشد.

## Widget Placement

- provider key
- widget key
- row/column or logical order
- supported size
- required
- draggable
- locked
- configuration values

Grid باید Responsive باشد و Position منطقی به Breakpointها نگاشت شود.

## Provider Validation

در Publish:

- Provider وجود داشته باشد.
- Contract Version پشتیبانی شود.
- Widget Key معتبر باشد.
- Size پشتیبانی شود.
- Configuration با Schema سازگار باشد.
- Capability و Dependencyها معتبر باشند.

## User Reorder

در v8:

- فقط Widget مجاز و Draggable جابه‌جا می‌شود.
- Required یا Locked حذف نمی‌شود.
- User Order فقط Layer نهایی است.
- با تغییر نسخه Published، Mapping تا حد ممکن حفظ و Conflictها Resolve می‌شوند.

## Preview

Preview باید بتواند Result را برای:

- Company
- Role/Profile
- User نمونه
- Desktop/Tablet/Mobile

نمایش دهد و Source هر Rule را توضیح دهد.

## Publish و Rollback

- Publish Atomic است.
- Version Conflict بررسی می‌شود.
- Rollback حذف تاریخچه نیست؛ Snapshot قبلی را به Version جدید تبدیل می‌کند.
- Cache Resolution پس از Publish invalidate می‌شود.

## Reset

- Reset User
- Reset Role/Profile Scope
- Reset Company Scope

Bulk Reset نیازمند Impact Preview، Confirmation و Audit است.

## Security

- Edit Draft
- Validate
- Publish
- Rollback
- Bulk Reset
- Audit Read

هر Operation Capability و Method Check مستقل دارد.

## Observability

- resolution latency
- invalid provider configuration
- publish conflict
- user preference migration conflict
- provider unavailable count

## Migration

- Layoutهای قدیمی به Logical Placement نگاشت شوند.
- Unknown Widget به Disabled Reference با Warning تبدیل شود.
- User Preference نامعتبر حذف نشود مگر با Migration Log.
- Initial Published Version ساخته شود.

## معیار پذیرش

- Result هر کاربر Explainable باشد.
- Company Lock قابل دورزدن نباشد.
- Publish و Rollback Audit شوند.
- Provider Missing کل Dashboard را خراب نکند.
- User Reorder پس از Upgrade تا حد ممکن حفظ شود.