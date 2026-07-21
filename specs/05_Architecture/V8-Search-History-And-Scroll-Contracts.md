# قراردادهای معماری Search، Recent History و Scroll — Workspace v8

| مشخصه | مقدار |
|---|---|
| وضعیت | `Consolidated` |
| نسخه | `CAS UI Workspace v8 — Through Iteration 12` |
| Decision | `DEC-016` |
| Provider Contract | `../03_Modules/V8_Provider_Registry.md` |

## ۱. Command Palette

Triggerهای Topbar، Hero، Mobile و Keyboard باید یک Command Palette مشترک را باز کنند. Route مستقل Search وجود ندارد.

### Capability

`search.use` فقط اجازه استفاده از Palette را می‌دهد. هر Provider مجوز Resourceهای خود را در Backend اعمال می‌کند.

### حالت‌ها

- Query خالی: Recent Items مجاز و Quick Actions
- Query غیرخالی: نتایج Group‌شده Providerها
- Loading
- Empty
- Partial Provider Failure
- Error
- Unavailable

Palette باید Keyboard Navigation، Autofocus، Escape، Focus Trap و Focus Restore داشته باشد و با Command Service استاندارد Odoo تعارض نکند.

## ۲. Search Provider Contract

### Request مفهومی

```json
{
  "query": "درخواست خرید",
  "resource_filter": "all",
  "cursor": null,
  "limit": 20,
  "company_context": 1,
  "active_route": "workspace-home"
}
```

### Response مفهومی

```json
{
  "items": [
    {
      "provider_key": "correspondence",
      "resource_type": "letter",
      "resource_id": 123,
      "label": "درخواست خرید مواد اولیه",
      "secondary_label": "مکاتبات",
      "deep_link": {"route": "correspondence.detail", "params": {"id": 123}},
      "rank": 0.92
    }
  ],
  "next_cursor": null,
  "partial_warning": null
}
```

### قواعد

- Server-side Query
- Provider Registry/Whitelist
- Debounce و Cancel Stale Request
- Cursor Pagination
- Stable Sort و Ranking
- ACL، Record Rule، Method Scope و Company Isolation
- حداقل Metadata لازم
- عدم افشای Count، Label یا Snippet غیرمجاز
- Provider-specific Timeout و Partial Failure

## ۳. Recent Resource Reference

Workspace فقط Reference فنی نگه می‌دارد:

```json
{
  "provider_key": "document",
  "resource_type": "document",
  "resource_id": 81,
  "display_label_snapshot": "دستورالعمل ایمنی",
  "deep_link": {"route": "documents.detail", "params": {"id": 81}},
  "last_opened_at": "2026-07-20T10:00:00Z",
  "company_id": 1
}
```

### قواعد

- ثبت فقط پس از Open موفق و مجاز
- User-scoped
- Retention محدود
- Permission Revalidation هنگام Query و Open
- حذف History بدون تغییر Source Record
- عدم Cache محتوای محرمانه
- امکان Exclusion Route/Resource حساس
- رکورد حذف‌شده یا Forbidden نمایش داده نمی‌شود
- ماژول مستقل `cas_recent_history` در v8 ساخته نمی‌شود

## ۴. Router و Capability Migration

- حذف `global-search-page`
- حذف `recent-history`
- حذف Navigation Itemهای متناظر
- حذف `history.read`
- استفاده از `search.use` برای Palette
- Permission هر Resource از Provider
- Deep Link قدیمی به Workspace/Palette یا Controlled Not Found هدایت شود
- صفحه منسوخ Render نشود

## ۵. Scroll عمومی Workspace

- Routeهای عادی Native Page Scroll دارند.
- `overflow:hidden` سراسری روی Main Content ممنوع است.
- Wheel، Keyboard، Touch و Auto-scroll مرورگر کار می‌کنند.
- Scroll Lock فقط در طول عمر Overlay و با Cleanup قطعی مجاز است.
- Widget Scroll داخلی فقط با Contract و محدودیت ارتفاع واقعی مجاز است.

## ۶. Scroll گفتگو

```text
Conversation Route: no page scroll
├── Conversation List: internal scroll
└── Active Conversation
    ├── Header
    ├── Message Body: internal scroll
    └── Composer outside message scroll
```

قواعد:

- `min-height: 0` در Grid/Flex chain
- List و Message Body مستقل
- Initial position در آخرین پیام
- پس از Send، اگر کاربر Near-bottom است انتها حفظ شود
- هنگام Load Older، Anchor حفظ شود
- اگر کاربر از انتها فاصله دارد، New Message Indicator نمایش داده شود
- Mobile Keyboard نباید Composer یا Message را غیرقابل دسترس کند

## ۷. Security

- Search هیچ Permission جدیدی ایجاد نمی‌کند.
- `sudo` عمومی ممنوع است.
- Recent Item Permission دوباره Validate می‌شود.
- Deep Link Backend Check دارد.
- Count و Group Header نباید وجود داده Forbidden را افشا کند.
- Company Switch نتیجه و Cache را invalidate می‌کند.

## ۸. Observability

- search latency/error/provider timeout
- provider partial failure
- unauthorized result filtered
- recent reference invalid/forbidden
- scroll lock leak
- conversation initial position failure
- anchor jump
- message while away from bottom

## ۹. تست‌ها

- Command Palette Keyboard/Screen Reader
- Shortcut integration با Odoo
- Search/History Permission و Count Leakage
- Browser Back/Forward بعد از حذف Routeها
- Deep Link قدیمی
- Native Scroll Routeهای بلند
- Conversation internal scroll
- Initial bottom و Send behavior
- Load Older anchor
- Mobile Keyboard
- RTL و Resize

## ۱۰. معیار پذیرش

- هیچ Route مستقل Search/History وجود نداشته باشد.
- Query خالی Recent Items مجاز را نشان دهد.
- Provider Failure سایر نتایج را حذف نکند.
- Search Result غیرمجاز در Metadata یا Count افشا نشود.
- Routeهای عادی Scroll بومی داشته باشند.
- Conversation Scroll و Anchor رفتار پایدار داشته باشند.