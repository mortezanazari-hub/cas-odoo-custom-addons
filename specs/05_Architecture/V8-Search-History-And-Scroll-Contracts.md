# قراردادهای معماری Search، Recent History و Scroll — Workspace v8

| مشخصه | مقدار |
|---|---|
| وضعیت | `Needs Review` |
| نسخه | `CAS UI Workspace v8` |
| Change Set | `../06_ChangeSets/CS-WORKSPACE-V8.md` |

## ۱. Command Palette Contract

Triggerهای Topbar، Hero، Mobile Search و `Ctrl+K` باید یک Overlay مشترک را باز کنند. Route مستقل Search وجود ندارد.

حالت‌ها:

- Query خالی: Recent Items، Search History، Pinها و Commandهای مجاز
- Query غیرخالی: نتایج گروه‌بندی‌شده Providerها
- Loading، Empty، Error و Unavailable

Overlay باید Autofocus، Escape، Outside Click، Focus Trap و Focus Restore داشته باشد.

## ۲. Search Provider Contract

ورودی مفهومی:

```json
{
  "query": "درخواست خرید",
  "type": "all",
  "cursor": null,
  "limit": 20,
  "company_id": 1
}
```

خروجی حداقلی:

```json
{
  "items": [
    {
      "provider": "correspondence",
      "resource_type": "letter",
      "resource_id": 123,
      "title": "درخواست خرید مواد اولیه",
      "subtitle": "مکاتبات",
      "route": "correspondence.detail",
      "route_params": {"id": 123}
    }
  ],
  "next_cursor": null,
  "has_more": false
}
```

قواعد:

- Server-side Query
- Debounce و Cancel Request
- Provider Whitelist
- Stable Sort و Pagination/Cursor
- ACL، Record Rule و Company Scope
- عدم افشای Count یا Metadata غیرمجاز

## ۳. Recent History Contract

Resource Reference حداقلی:

```json
{
  "provider": "document",
  "resource_type": "document",
  "resource_id": 81,
  "safe_title": "دستورالعمل ایمنی",
  "route": "documents.detail",
  "last_opened_at": "2026-07-20T10:00:00Z"
}
```

قواعد:

- ثبت فقط پس از Open موفق
- User-scoped و سمت سرور در Production
- Retention محدود
- Revalidation مجوز هنگام نمایش و Open
- حذف History بدون تغییر رکورد منبع
- عدم Cache محتوای محرمانه
- امکان Exclusion مسیرهای حساس

## ۴. Router و Capability Migration

- حذف `global-search-page`
- حذف `recent-history`
- حذف Navigation Itemهای متناظر
- حذف Capability مستقل `history.read`
- حفظ Capability یا Operation مجاز Search در سطح Shell
- Deep Linkهای قدیمی باید به Workspace اصلی Redirect یا Controlled Not Found شوند؛ نباید صفحه منسوخ را Render کنند.

## ۵. Scroll Contract عمومی Workspace

- Routeهای عادی Scroll بومی مرورگر را حفظ می‌کنند.
- `overflow:hidden` سراسری روی `.main-content` ممنوع است.
- Auto-scroll دکمه وسط موس، Wheel، Keyboard و Touch باید کار کنند.
- Scroll Lock فقط در طول عمر Overlay و با Cleanup قطعی مجاز است.

## ۶. Scroll Contract گفتگو

ساختار:

```text
Conversation Route: no page scroll
├── Conversation List: overflow:auto
└── Active Conversation
    ├── Header: fixed in container
    ├── Message Body: overflow:auto
    └── Composer: fixed in container
```

قواعد:

- `min-height:0` در Grid/Flex chain
- List و Message Body Scroll مستقل
- پشتیبانی Auto-scroll مرورگر در هر دو Container
- Initial scroll بعد از Render به انتهای Message Body
- پس از Send، Scroll به انتها
- هنگام Load Older Messages حفظ Anchor
- اگر کاربر Near-bottom نیست، پیام جدید با Indicator اعلام شود و Scroll اجباری انجام نشود.

## ۷. Observability و تست

رویدادهای قابل پایش:

- Search latency/error/provider timeout
- Recent Item permission rejection
- Scroll Lock leak
- Conversation initial-scroll failure
- Anchor jump هنگام Load Older
- Bus message received while user is away from bottom

تست‌ها:

- Keyboard و Screen Reader Command Palette
- Search/History Security
- Browser Back/Forward بعد از حذف Routeها
- Middle-click Auto-scroll روی Routeهای بلند
- Conversation internal auto-scroll
- Resize، Mobile Keyboard و RTL
