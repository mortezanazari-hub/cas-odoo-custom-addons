# Page Specification — Recent History داخل Command Palette

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-EMP-HISTORY-001` |
| نسخه هدف | `CAS UI Workspace v8 — Through Iteration 12` |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Consolidated` |
| نوع تجربه | قابلیت داخلی Command Palette؛ بدون صفحه مستقل |
| مالک Reference فنی | `cas_workspace` |
| مالک Resource | Provider منبع |

## تصمیم نهایی نسخه ۸

صفحه، Navigation Item و Route مستقل `recent-history` حذف شده‌اند. Recent History یک ابزار سبک Navigation در Query خالی Command Palette است و Audit Log محسوب نمی‌شود.

ماژول مستقل `cas_recent_history` در v8 ساخته نمی‌شود.

## هدف

بازگشت سریع کاربر به Resourceهایی که واقعاً و با مجوز باز کرده است، بدون ایجاد مقصد کاری اضافه یا انتقال مالکیت داده به Workspace.

## موارد قابل نمایش

- Resourceهای اخیراً بازشده
- Quick Actionهای پرتکرار مجاز
- Searchهای اخیر، در صورت Retention Policy مصوب
- Pinها، در صورت Provider معتبر

## Resource Reference

Workspace فقط Reference حداقلی نگه می‌دارد:

```text
provider_key
resource_type
resource_id
display_label_snapshot
deep_link
last_opened_at
company_id
```

`display_label_snapshot` فقط Fallback نمایشی است و Source of Truth نیست.

## قواعد ثبت

- فقط Open موفق و مجاز ثبت می‌شود.
- Hover، Preview یا Result بدون Open ثبت نمی‌شود.
- Reference به‌صورت User-scoped و Server-side نگهداری می‌شود.
- Retention محدود و قابل تنظیم است.
- Route و Resourceهای حساس قابل Exclusion هستند.
- حذف History فقط Reference کاربر را حذف می‌کند.
- حذف History هیچ رکورد کسب‌وکاری را تغییر نمی‌دهد.

## Revalidation

هنگام نمایش و Open مجدد:

1. Provider نصب و سازگار باشد.
2. Resource هنوز وجود داشته باشد.
3. Company Context معتبر باشد.
4. ACL، Record Rule و Domain Permission دوباره بررسی شوند.
5. Deep Link فعلی Resolve شود.

Resource حذف‌شده، غیرمجاز یا غیرفعال نمایش داده نمی‌شود. عنوان Snapshot پس از سلب دسترسی نباید افشا شود.

## Privacy و Security

- Capability مستقل `history.read` وجود ندارد.
- Permission هر Resource مرجع است.
- محتوای Document، Message، Correspondence یا Work Report در History Cache نمی‌شود.
- Count و Label نباید وجود Resource ممنوع را افشا کنند.
- Workspace برای Revalidation از broad `sudo` استفاده نمی‌کند.
- Company Switch نتیجه را invalidate می‌کند.
- History جایگزین Audit Log نیست.

## Storage

Production Storage باید:

- Server-side
- User-scoped
- Multi-device
- Retention-aware
- قابل پاک‌سازی توسط کاربر در محدوده Policy
- قابل Exclusion براساس Classification

باشد. Local Storage فقط برای Prototype یا Cache غیرمرجع کوتاه‌عمر قابل استفاده است.

## Stateها

- Loading
- Empty
- Ready
- Provider Unavailable
- Invalid Reference Removed
- Partial Failure
- Error

## معیارهای پذیرش

1. `recent-history` در Router و Navigation وجود نداشته باشد.
2. Recent Items فقط در Query خالی Palette نمایش داده شوند.
3. ماژول مستقل History ساخته نشود.
4. Permission هنگام نمایش و Open مجدد بررسی شود.
5. Resource غیرمجاز Label یا Count افشا نکند.
6. پاک‌کردن History Source Record را تغییر ندهد.
7. Production History روی دستگاه‌های مختلف قابل بازیابی باشد.
8. Routeهای حساس قابل Exclusion باشند.

## اسناد مرتبط

- `../../04_Decisions/DEC-016-Search-And-Recent-History-Consolidation.md`
- `../../05_Architecture/V8-Search-History-And-Scroll-Contracts.md`
- `../../03_Modules/V8_Provider_Registry.md`
- `../../00_Project/V8_Canonical_Baseline.md`