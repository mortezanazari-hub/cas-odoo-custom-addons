# Provider Architecture — CAS Workspace v8

| مشخصه | مقدار |
|---|---|
| وضعیت | `Consolidated` |
| قرارداد پایه | `cas_workspace_contract` |

## هدف

Provider Architecture جداسازی Experience Layer از Domain Layer را تضمین می‌کند. Workspace داده را مصرف می‌کند، اما Business Model و Permission آن را مالک نمی‌شود.

## اجزا

```text
cas_workspace_contract
├── provider interfaces
├── metadata schemas
├── resource references
├── error model
└── contract versioning

Domain Provider / Bridge
├── registers metadata
├── implements queries/actions
├── enforces permission
└── resolves deep links

cas_workspace
├── discovers providers
├── orchestrates calls
├── renders partial states
└── stores UI-only preferences
```

## Registryها

- Navigation Registry
- Widget Registry
- Search Registry
- Quick Action Registry
- Badge Registry
- Resource Resolver Registry

Registry ممکن است یک مکانیزم مشترک با Typeهای مختلف باشد؛ جزئیات فنی در API Spec تثبیت می‌شود.

## Registration

Provider Registration باید:

- Declarative یا Service-based باشد.
- Contract Version داشته باشد.
- Duplicate Key را رد کند.
- Module Source را ثبت کند.
- Capability و Company Awareness را اعلام کند.
- Health Check اختیاری داشته باشد.

## Invocation

Workspace فقط Contract Method را فراخوانی می‌کند. Domain Provider مسئول:

- Input Validation
- Permission
- Record Rule
- Pagination
- Serialization امن
- Error Mapping
- Audit موردنیاز

## Aggregation

Aggregation باید:

- Timeout مستقل داشته باشد.
- Partial Failure را حفظ کند.
- Result Limit داشته باشد.
- Provider Rank را با Global Rank ترکیب کند.
- داده تکراری را با Resource Identity مدیریت کند.

## Circular Dependency Prevention

- Contract Module به Workspace یا Domain وابسته نیست.
- Domain Provider به Contract وابسته است.
- Workspace به Contract و Bridgeهای نصب‌شده وابسته یا Runtime-aware است.
- Domain Model هرگز برای ثبت Provider به UI Module وابسته نمی‌شود.

## Resource Identity

```text
provider_key + resource_type + resource_id + company_context
```

Deep Link باید Stable و Permission-aware باشد.

## Configuration Schema

Widget Provider Schema تنظیمات مجاز را اعلام می‌کند. Workspace مقدار را ذخیره می‌کند ولی:

- Schema را Validate می‌کند.
- Secret یا Domain Data ذخیره نمی‌کند.
- Provider Version Compatibility را بررسی می‌کند.

## Security

- Client Provider Key را قابل اعتماد نمی‌کند.
- Provider فعال و مجاز در Server Resolve می‌شود.
- Search و Badge از Scope یکسان استفاده می‌کنند.
- Provider Result حداقل داده لازم است.
- Error Message داده محرمانه افشا نمی‌کند.

## Performance

- Batch API برای Widgetهای هم‌Provider در صورت نیاز
- Pagination Cursor
- Cache Scope-aware
- Provider-specific timeout
- Metrics per provider

## Degradation

- Missing Provider: Unavailable
- Old Contract: Unsupported Version
- Timeout: Retryable Local Error
- Forbidden: Route/Widget hidden or explicit Forbidden on deep link
- Partial Data: Warning without losing valid results

## معیار پذیرش

- Domain Module بدون Workspace قابل نصب و استفاده باشد.
- Workspace بدون شناخت Model داخلی Provider کار کند.
- Duplicate Provider Key شناسایی شود.
- Permission leakage از Search/Badge رخ ندهد.
- Failure یک Provider کل Workspace را متوقف نکند.