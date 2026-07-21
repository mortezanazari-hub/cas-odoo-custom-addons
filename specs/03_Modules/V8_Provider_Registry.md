# Registry و قرارداد Providerهای Workspace v8

| مشخصه | مقدار |
|---|---|
| شناسه | `PROVIDER-REGISTRY-V8` |
| وضعیت | `Consolidated` |
| مالک قرارداد | `cas_workspace_contract` |
| مصرف‌کننده اصلی | `cas_workspace` |

## هدف

Provider Contract اجازه می‌دهد Workspace داده و Action ماژول‌ها را نمایش دهد، بدون اینکه به مدل داخلی آن‌ها وابسته یا مالک داده آن‌ها شود.

## اصول

- Provider مالک داده خود باقی می‌ماند.
- Provider Permission را در Backend اعمال می‌کند.
- Workspace فقط Contract را می‌شناسد.
- Contract باید Versioned باشد.
- Failure یک Provider نباید کل Workspace را متوقف کند.
- خروجی Provider حداقل داده لازم برای UI است.
- `sudo` برای دورزدن Permission ممنوع است.

## انواع Provider

### Navigation Provider

Route و Navigation Item قابل استفاده را عرضه می‌کند.

### Widget Provider

Widget Metadata، Data Fetch و Actionها را عرضه می‌کند.

### Search Provider

نتایج مجاز Search را با Pagination و Ranking عرضه می‌کند.

### Quick Action Provider

Actionهای قابل اجرا از Command Palette یا Workspace را عرضه می‌کند.

### Badge Provider

Badge یا Count محدود و امن برای Navigation ارائه می‌دهد.

### Resource Resolver

Deep Link و Recent Resource Reference را به رکورد فعلی Resolve می‌کند.

### Dashboard Configuration Provider

Schema تنظیمات مجاز Widget را اعلام می‌کند؛ مالک Configuration همچنان Workspace است.

## Metadata مشترک

```text
provider_key
contract_version
display_name
module_name
resource_types
required_capabilities
company_aware
supports_pagination
supports_search
supports_deep_link
health_state
```

## Widget Contract

```text
widget_key
provider_key
title
icon
supported_sizes
default_size
required_capability
configuration_schema
data_sensitivity
refresh_policy
primary_action
empty_state
unavailable_state
```

## Search Contract

Request:

```text
query
limit
cursor
company_context
active_route
user_locale
```

Response:

```text
items[]
  resource_type
  resource_id
  label
  secondary_label
  icon
  deep_link
  rank
  provider_key
next_cursor
partial_warning
```

Provider باید قبل از بازگرداندن Item، Permission رکورد را بررسی کند.

## Recent Resource Reference

Workspace فقط این Reference فنی را ذخیره می‌کند:

```text
provider_key
resource_type
resource_id
display_label_snapshot
deep_link
last_opened_at
company_id
```

هنگام نمایش، Resource Resolver باید وجود و دسترسی فعلی را دوباره بررسی کند. Snapshot Label صرفاً Fallback UI است و مرجع داده نیست.

## Action Contract

هر Action باید مشخص کند:

- Action Key
- Label و Icon
- Capability
- Input Schema
- Confirmation Policy
- Idempotency Key Support
- Result Deep Link
- Error Contract

Workspace Action را مستقیماً با دستکاری Model اجرا نمی‌کند؛ Service رسمی Provider فراخوانی می‌شود.

## خطاها

کدهای مفهومی:

- `provider_unavailable`
- `forbidden`
- `not_found`
- `validation_error`
- `conflict`
- `partial_failure`
- `unsupported_contract_version`

خطای یک Provider باید محلی نمایش داده شود.

## Versioning

- Contract Version در Provider Metadata اجباری است.
- Breaking Change نیازمند Major Version جدید است.
- Workspace باید Provider ناسازگار را Unavailable نشان دهد، نه اینکه Crash کند.
- Deprecation Window در Module Specification ثبت می‌شود.

## Security

- Server-side Permission الزامی است.
- Search Result نباید اطلاعات رکورد Forbidden را در Label یا Count افشا کند.
- Badge Count باید از همان Scope رکوردها استفاده کند.
- Company Context از Client به‌تنهایی قابل اعتماد نیست.
- Deep Link مجوز را دوباره بررسی می‌کند.

## Performance

- Pagination برای Search و List Providerها الزامی است.
- N+1 Query ممنوع است.
- Countهای سنگین باید Cache یا Projection مناسب داشته باشند.
- Timeout Provider نباید Request کلی Workspace را نامحدود نگه دارد.

## Providerهای اولیه

- Personal Task
- Action Hub
- Calendar
- Conversations
- Notifications
- Work Report
- Correspondence
- Documents
- Attendance / Shift
- Announcements

## معیار پذیرش

1. Workspace بدون import مستقیم Modelهای Domain کار کند.
2. Providerها بدون وابستگی به UI Runtime ثبت شوند.
3. Permission در Provider enforce شود.
4. Search و Widget Failure مستقل باشند.
5. Contract Version ناسازگار قابل تشخیص باشد.
6. Recent History داده کسب‌وکاری را کپی نکند.