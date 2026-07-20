# ارزیابی اثر نسخه ۷ بر ماژول `cas_workspace`

| مشخصه | مقدار |
|---|---|
| وضعیت | `Needs Review` |
| نوع سند | ارزیابی اثر؛ نه Specification اجرایی |
| Change Set | `../../06_ChangeSets/CS-WORKSPACE-V7.md` |

## جمع‌بندی

`cas_workspace` بیشترین تغییر را در گذار نسخه ۴ به ۷ دارد. این ماژول باید از یک Dashboard Shell محدود به پوسته سازمانی کامل با Router، Navigation، Widget، Preference و Adapter Registry تبدیل شود؛ بدون آن‌که مالک داده کسب‌وکاری ماژول‌های دیگر شود.

## مسئولیت‌های افزوده یا توسعه‌یافته

- Route Registry و Navigation مبتنی بر Capability
- Routeهای جدید کارهای شخصی، تقویم، گفتگو، جست‌وجو، اعلان و تاریخچه
- Hero و Dashboard Composition
- Widget Registry با ID پایدار
- Drag & Drop و ذخیره ترتیب
- Theme، Accent، Font Scale و Density
- Sidebar State
- Drawer و Modal Infrastructure
- Topbar Quick Access
- Search Provider Registry
- Calendar Aggregation Registry
- Notification Provider Registry
- Recent History Service Interface
- Conversation Adapter Interface
- Error Boundary و Stateهای Route/Widget

## مواردی که نباید مالک آن‌ها شود

- Message و Conversation Record
- Calendar Event کسب‌وکاری
- Action رسمی
- Work Report و Activity Line
- Attendance و Shift Record
- Correspondence و Document
- Workflow/Approval State

## APIهای موردنیاز برای بررسی آینده

- `get_navigation`
- `get_workspace_data`
- `get_page_data`
- `get_record_detail`
- `execute_route_action`
- `get_user_preferences`
- `save_user_preferences`
- `search_global`
- `get_calendar_feed`
- `get_notifications`
- `get_recent_history`

نام و امضای نهایی این APIها هنوز تصویب نشده است.

## امنیت

- Query بدون `sudo`
- Route و Operation مبتنی بر Capability
- Record Rule ماژول منبع مرجع نهایی
- Provider Whitelist
- جلوگیری از نشت عنوان در Search/History/Notification
- حذف Role Switch آزمایشی در Production

## تست‌های لازم

- تمام نقش‌ها و ترکیب نقش‌ها
- Deep Link و Back/Forward
- نبود Provider اختیاری
- Theme و Contrast
- Sidebar باز/بسته
- Widget Order و Preference
- Forbidden/Unavailable/Error State
- RTL و Responsive

## وضعیت

تا زمان تصویب مرز سرویس‌های Personal Task، Notification، History، Calendar و Conversation این سند `Needs Review` باقی می‌ماند.
