# ماتریس تجمیع تغییرات ماژول‌ها

این فایل مرجع مرکزی اثر تصمیمات صفحه‌ای بر ماژول‌های پروژه است. ثبت در این ماتریس به‌تنهایی مجوز پیاده‌سازی نیست.

## وضعیت‌ها

- `Collected`: ثبت شده ولی هنوز تجمیع اجرایی نشده است.
- `Needs Review`: مرز مالکیت، امنیت یا API نیازمند تصمیم است.
- `Consolidated`: در Specification ماژول تجمیع شده است.
- `Implementation Ready`: آماده اجرا است.

## خط نسخه‌بندی

```text
CAS UI Prototype v4 → CAS UI Workspace v7 → CAS UI Workspace v8 / Iteration 11
```

## ماتریس تصمیمات Workspace v8

| تصمیم/حوزه | ماژول یا سرویس | نوع اثر | وضعیت |
|---|---|---|---|
| دسته‌های Task شخصی / `DEC-012` | `cas_personal_task` پیشنهادی، `cas_workspace` | Data، CRUD، Ownership، Migration | Needs Review |
| Selector شرکت‌کنندگان / `DEC-013` | HR Directory، Organization Resolver، Calendar، `cas_workspace` | Search، Security، Event/Task | Needs Review |
| Discuss Reuse / `DEC-014` | Odoo Mail/Discuss/Bus، `cas_workspace` | Integration، Message، Realtime | Needs Review |
| Overlay Stack / `DEC-015` | `cas_workspace`، Design System | Modal، Drawer، Focus، Scroll Lock | Needs Review |
| Search/History Consolidation / `DEC-016` | `cas_workspace`، Search Registry، Preference | Router، Command Palette، History | Needs Review |
| Action Hub source chips | `cas_action_hub`، `cas_workspace` | Filter State، UI | Collected |
| Conversation compact rows | `cas_workspace`، Discuss Adapter | Layout، Density | Collected |
| Conversation internal scroll | `cas_workspace`، Discuss Adapter | Scroll Contract، Accessibility | Needs Review |
| Conversation bottom anchoring | Discuss Adapter، Message Pagination | Initial Position، Send، Pagination | Needs Review |
| Native browser autoscroll | Workspace Shell | Global Scroll Contract | Collected |
| Calendar RTL arrows | `cas_workspace`، Jalali UI | RTL Semantics | Collected |

## Route و Navigation Migration

| مورد نسخه ۷ | تصمیم نسخه ۸ | اثر |
|---|---|---|
| `global-search-page` | حذف Route و Navigation Item | Search از Command Palette باز می‌شود |
| `recent-history` | حذف Route و Navigation Item | Recent Items داخل Query خالی Search |
| `history.read` | حذف Capability مستقل | Permission هر Resource مرجع است |
| Search Topbar/Hero | حفظ و یکپارچه‌سازی | همه Triggerها یک Overlay مشترک |

## `cas_workspace` — اثر بسیار زیاد

مسئولیت‌ها:

- Shell، Router و Navigation
- Command Palette مشترک Search/History
- Search Provider Registry و Safe Result Navigation
- Recent History UI و Preference Adapter
- Overlay Manager و Focus Restore
- Scroll Contract سراسری
- Conversation Layout و Initial Scroll
- Calendar Attendee Selector
- Widget و Theme Preferences

نباید مالک این داده‌ها باشد:

- Message و Conversation
- Calendar Event و Invitation
- Task رسمی
- Employee/Hierarchy
- Document، Correspondence و Workflow Record

وضعیت: `Needs Review`.

## `cas_action_hub` — اثر زیاد

- حفظ مرزبندی Action رسمی از Task شخصی
- فیلتر زمانی تک‌انتخابی
- فیلتر منبع به‌صورت چیپ تک‌انتخابی
- Sort مستقل به‌صورت Dropdown
- Provider برای Search، Notification و Calendar Deadline

وضعیت: `Needs Review`.

## Search Provider Registry — اثر زیاد

- Query Server-side
- Provider Whitelist
- Cursor/Pagination
- ACL، Record Rule و Company Scope
- عدم افشای عنوان و Count غیرمجاز
- Safe Serializer و Deep Link

وضعیت: `Needs Review` تا تصویب API.

## Recent History / Preference Service — اثر متوسط

- Resource Reference حداقلی
- User-scoped Storage
- Retention محدود
- Permission Revalidation
- Exclusion مسیرهای حساس
- حذف History بدون تغییر رکورد منبع

تصمیم: فعلاً ماژول مستقل `cas_recent_history` ساخته نمی‌شود.

## Odoo Mail/Discuss/Bus — اثر زیاد

- Conversation، Message، Member و Unread
- Reply، Forward، Reaction، Pin، Mute و Archive
- Message Pagination و Realtime
- Initial Scroll به آخرین پیام
- حفظ Anchor هنگام Load Older Messages
- New-message Indicator زمانی که کاربر Near-bottom نیست

وضعیت: `Needs Review`؛ تطبیق دقیق با Odoo 19 Community لازم است.

## HR Directory و Organization Resolver — اثر زیاد

- Search Server-side شرکت‌کنندگان
- Company Scope و حداقل Metadata
- تعیین رابطه مدیریتی و Delegation
- مجوز دعوت و Task Assignment

وضعیت: `Needs Review`.

## Calendar/Event Integration — اثر زیاد

- Event، Attendee، Invitation و RSVP
- تفکیک Invitation از Task
- Event-to-Task Link
- Timezone و Jalali Adapter
- Partial Failure Policy

وضعیت: `Needs Review`.

## Jalali Suite — اثر متوسط

- Parse تاریخ شمسی Search
- ورودی و نمایش تقویم
- معنای صحیح ماه قبل/بعد در RTL
- حفظ ذخیره Date/Datetime استاندارد

وضعیت: `Needs Review`.

## قرارداد امنیت مشترک

- بدون `sudo()` برای Query کاربرمحور
- ACL، Record Rule، Company Scope و Method Check
- جلوگیری از ID Tampering
- Provider Whitelist
- Permission مستقل Attachment و Forward
- عدم نشت Search/History
- Audit برای عملیات حساس

## تست‌های اجباری

- نبود Routeهای حذف‌شده
- Command Palette و `Ctrl+K`
- Search/History Security
- Middle-click Auto-scroll در Routeهای عادی
- نبود Scroll کلی در Conversation Route
- Scroll مستقل List و Message Body
- ورود به انتهای گفتگو و حفظ انتها پس از Send
- حفظ Anchor هنگام Pagination معکوس
- Overlay Parent/Child، Escape و Focus Restore
- RTL ماه قبل/بعد
- چیپ منبع تک‌انتخابی Action Hub
- Responsive، Keyboard و Screen Reader

## اسناد مرجع

- `02_UI_UX/Employee/Global_Search.md`
- `02_UI_UX/Employee/Recent_History.md`
- `02_UI_UX/Employee/Conversations.md`
- `04_Decisions/DEC-016-Search-And-Recent-History-Consolidation.md`
- `05_Architecture/V8-Search-History-And-Scroll-Contracts.md`
- `06_ChangeSets/CS-WORKSPACE-V8.md`

## وضعیت نهایی

این ماتریس تا Prototype `ui-workspace-v8-iteration11.zip` به‌روزرسانی شده است. هیچ ردیفی هنوز `Implementation Ready` نیست مگر پس از تدوین Specification مستقل ماژول مربوط.
