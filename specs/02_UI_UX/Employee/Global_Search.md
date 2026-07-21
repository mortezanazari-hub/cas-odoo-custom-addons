# Page Specification — جست‌وجوی سازمانی در Command Palette

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-EMP-SEARCH-001` |
| نسخه هدف | `CAS UI Workspace v8 — Through Iteration 12` |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Consolidated` |
| نوع تجربه | Command Palette مشترک؛ بدون صفحه مستقل |
| Capability ابزار | `search.use` |
| مالک UI | `cas_workspace` |
| مالک نتایج | Providerهای منبع |

## تصمیم نهایی نسخه ۸

صفحه، Navigation Item و Route مستقل `global-search-page` حذف می‌شوند. Search یک ابزار عبور سریع و اجرای Command است که از Topbar، Hero، Mobile Trigger و میانبر هماهنگ با Command System استاندارد Odoo باز می‌شود.

Workspace نباید Listener سراسری متعارض با Odoo برای `Ctrl+K` ایجاد کند. Trigger صفحه‌کلید باید از Registry یا Service استاندارد Command استفاده کند.

## ساختار Palette

1. Header فشرده و Close
2. ورودی Autofocus
3. فیلتر تک‌انتخابی نوع Resource
4. نتایج Group‌شده Providerها
5. Recent Items و Quick Actions در Query خالی
6. Loading، Empty، Partial Failure، Error و Unavailable

## Query خالی

می‌تواند این موارد را نشان دهد:

- Recently opened Resourceهای مجاز
- Quick Actions مجاز
- Searchهای اخیر، در صورت Policy و Retention مصوب
- موارد Pin‌شده، در صورت Provider معتبر

با شروع Query، محتوای اولیه با نتایج Search جایگزین می‌شود.

## دامنه Providerها

- Personal Task
- Organizational Action
- اشخاص و ساختار سازمانی
- Calendar Event
- Work Report و Review Route
- Form و Submission، در محدوده مجاز
- Workflow و Approval
- Correspondence
- Document
- Conversation
- Routeها و Quick Actionهای مجاز
- سایر Providerهای نصب‌شده و سازگار

## رفتار تعامل

- همه Triggerها یک Palette و یک State مشترک را باز می‌کنند.
- Escape فقط Overlay بالایی را می‌بندد.
- Focus پس از Close به Trigger بازمی‌گردد.
- Keyboard Navigation کامل است.
- انتخاب Result، Deep Link امن را باز می‌کند.
- در Mobile به Sheet تمام‌عرض کنترل‌شده تبدیل می‌شود.
- Provider Timeout نتیجه سایر Providerها را حذف نمی‌کند.

## قرارداد داده و Performance

- Query کاملاً Server-side است.
- Provider Threshold می‌تواند براساس Resource متفاوت باشد.
- Requestها Debounce و Stale Requestها Cancel می‌شوند.
- Cursor/Pagination الزامی است.
- Provider Registry و Contract Version بررسی می‌شوند.
- Result Limit، Stable Sort و Ranking قابل پیش‌بینی است.
- Providerهای اختیاری `unavailable` یا Partial Error کنترل‌شده می‌دهند.

## امنیت

- `search.use` فقط Palette را فعال می‌کند.
- هر Provider ACL، Record Rule، Company Scope و Method Permission خود را اعمال می‌کند.
- Search هیچ Permission جدیدی ایجاد نمی‌کند.
- Label، Count، Snippet یا Metadata رکورد غیرمجاز افشا نمی‌شود.
- Workspace و Search Aggregator از broad `sudo` استفاده نمی‌کنند.
- Deep Link در مقصد Permission را دوباره بررسی می‌کند.
- Company Switch نتایج و Cache را invalidate می‌کند.

## Recent Resource

پس از بازشدن موفق و مجاز Resource، Workspace فقط Reference فنی حداقلی را ثبت می‌کند. داده کسب‌وکاری یا محتوای محرمانه در History کپی نمی‌شود.

## Jalali و تاریخ

Providerهای تاریخ‌محور می‌توانند Query شمسی را Parse و به Date/Datetime استاندارد Odoo تبدیل کنند. تاریخ شمسی به‌عنوان تاریخ اصلی ذخیره نمی‌شود.

## Stateها

- Loading
- Empty
- Ready
- Partial Provider Failure
- Provider Unavailable
- Forbidden Tool Access
- Error

## معیارهای پذیرش

1. `global-search-page` در Router و Navigation وجود نداشته باشد.
2. همه Triggerها یک Palette مشترک را باز کنند.
3. Shortcut با Command System استاندارد Odoo تعارض نداشته باشد.
4. Query خالی Recent Items مجاز را نمایش دهد.
5. Permission هر Provider در Backend اعمال شود.
6. داده غیرمجاز در Result، Count یا Metadata نشت نکند.
7. Failure یک Provider سایر نتایج را از بین نبرد.
8. Focus، Keyboard، RTL و Mobile کامل باشند.

## اسناد مرتبط

- `../../04_Decisions/DEC-016-Search-And-Recent-History-Consolidation.md`
- `../../05_Architecture/V8-Search-History-And-Scroll-Contracts.md`
- `../../03_Modules/V8_Provider_Registry.md`
- `../../05_Architecture/Capability_And_Security_Model.md`
- `../../00_Project/V8_Canonical_Baseline.md`