# ماتریس تجمیع تغییرات ماژول‌ها

این فایل مرجع مرکزی اثر تصمیمات صفحه‌ای بر ماژول‌های پروژه است. ثبت ردیف در این ماتریس مجوز پیاده‌سازی نیست.

## وضعیت‌ها

- `Collected`: تصمیم ثبت شده ولی هنوز تجمیع ماژولی نشده است.
- `Needs Review`: نیازمند بررسی صفحات، نقش‌ها یا مرز مالکیت است.
- `Conflict`: تعارض حل‌نشده دارد.
- `Consolidated`: در Specification ماژول تجمیع شده است.
- `Implementation Ready`: آماده تبدیل به دستور اجرایی است.

## خط نسخه‌بندی فعال

```text
CAS UI Prototype v4 → CAS UI Workspace v7
```

نسخه‌های ۵ و ۶ Release رسمی مستقل نیستند.

## تغییرات صفحه میزکار

| شناسه تصمیم | ماژول/دامنه | نوع اثر | خلاصه | وضعیت |
|---|---|---|---|---|
| `PAGE-EMP-DESK-DEC-001..015` | `cas_workspace`, `cas_work_report`, `cas_action_hub`, Attendance, Activity Catalog | Product/Data/UI | تصمیمات پایه میزکار عملیاتی، ثبت تدریجی فعالیت و شخصی‌سازی | Needs Review |
| `PAGE-EMP-DESK-DEC-016` | `cas_workspace` | UI/Composition | Hero سه‌ردیفه | Collected |
| `PAGE-EMP-DESK-DEC-017` | `cas_workspace` | UI/Layout | چهار Status Card هم‌اندازه | Collected |
| `PAGE-EMP-DESK-DEC-018` | `cas_workspace`, Search Registry | UI/Navigation | Command Launcher تمام‌عرض | Needs Review |
| `PAGE-EMP-DESK-DEC-019` | `cas_workspace`, `cas_action_hub` | Domain/UI | جداسازی Task شخصی از Action رسمی | Needs Review |
| `PAGE-EMP-DESK-DEC-020` | `cas_workspace`, Calendar Providers | Widget/Integration | تقویم روز، هفته و ماه در میزکار | Needs Review |
| `PAGE-EMP-DESK-DEC-021` | `cas_workspace`, Mail/Bus | Widget/Communication | گفتگوهای اخیر | Needs Review |
| `PAGE-EMP-DESK-DEC-022` | `cas_workspace`, `cas_work_report` | UI/Consolidation | ادغام ثبت و مرور فعالیت | Collected |
| `PAGE-EMP-DESK-DEC-023` | `cas_workspace` | Widget/Layout | ارتفاع ثابت Widgetها | Collected |
| `PAGE-EMP-DESK-DEC-024` | `cas_workspace` | Widget/Empty State | ظرفیت بصری ثابت و Placeholder | Collected |
| `PAGE-EMP-DESK-DEC-025` | `cas_workspace`, User Preference | Preference/DnD | Drag & Drop و ذخیره ترتیب | Needs Review |
| `PAGE-EMP-DESK-DEC-026` | `cas_workspace`, User Preference | Preference | ذخیره تنظیمات | Needs Review |
| `PAGE-EMP-DESK-DEC-027` | `cas_workspace` | Theme/Accessibility | Theme و خوانایی سراسری | Needs Review |
| `PAGE-EMP-DESK-DEC-028` | `cas_workspace` | Accessibility | حداقل متن ۱۲ پیکسل | Collected |
| `PAGE-EMP-DESK-DEC-029` | `cas_workspace` | Drawer/UI | انتقال اطلاعات جانبی به Drawer | Collected |
| `PAGE-EMP-DESK-DEC-030` | `cas_workspace`, همه Providerها | Route/Action | اتصال همه CTAها به Route رسمی | Needs Review |

## صفحه کارهای شخصی

| شناسه | ماژول/دامنه | نوع اثر | خلاصه | وضعیت |
|---|---|---|---|---|
| `PAGE-EMP-TASK-DEC-001` | `cas_workspace`, `cas_action_hub` | Domain Boundary | جداسازی Task شخصی از Action سازمانی | Needs Review |
| `PAGE-EMP-TASK-DEC-002` | Access Resolver | Security/Capability | Capability جدید `personal.tasks` | Collected |
| `PAGE-EMP-TASK-DEC-003..005` | Personal Task Store, `cas_workspace` | Data/UI | ثبت سریع، تکمیل، انتقال و زمان‌بندی | Needs Review |
| `PAGE-EMP-TASK-DEC-006` | `cas_work_report` | Adapter | تبدیل اختیاری Task به فعالیت | Needs Review |
| `PAGE-EMP-TASK-DEC-007` | `cas_workspace` | Widget/Page | منبع مشترک Widget و صفحه کامل | Collected |

## صفحه تقویم

| شناسه | ماژول/دامنه | نوع اثر | خلاصه | وضعیت |
|---|---|---|---|---|
| `PAGE-EMP-CAL-DEC-001..003` | `cas_workspace`, Calendar Aggregator | Route/Widget | Route سطح اول و سه نمای روز/هفته/ماه | Needs Review |
| `PAGE-EMP-CAL-DEC-004` | Jalali Suite | Date/UI | نمای ماهانه شمسی کامل | Needs Review |
| `PAGE-EMP-CAL-DEC-005` | Jalali Suite, Odoo ORM | Data Contract | ذخیره استاندارد و نمایش جلالی | Collected |
| `PAGE-EMP-CAL-DEC-006` | Calendar Integration | CRUD | ساخت رویداد واقعی | Needs Review |
| `PAGE-EMP-CAL-DEC-007` | Shift, Action, Correspondence, Workflow | Provider Aggregation | تجمیع رویدادهای چندمنبعی | Needs Review |

## صفحه گفت‌وگوها

| شناسه | ماژول/دامنه | نوع اثر | خلاصه | وضعیت |
|---|---|---|---|---|
| `PAGE-EMP-CONV-DEC-001` | `cas_workspace` | Navigation | Route سطح اول `messages` | Collected |
| `PAGE-EMP-CONV-DEC-002` | Mail/Discuss, `cas_correspondence` | Domain Boundary | جداسازی گفتگو از مکاتبه رسمی | Needs Review |
| `PAGE-EMP-CONV-DEC-003..005` | `cas_workspace` | Widget/Drawer/Topbar | سه نقطه دسترسی و Drawer جزئیات | Collected |
| `PAGE-EMP-CONV-DEC-006` | Mail/Bus | Realtime/State | همگام‌سازی Unread | Needs Review |
| `PAGE-EMP-CONV-DEC-007` | Mail/Discuss/Bus Adapter | Integration | Workspace مالک Message نیست | Needs Review |
| `PAGE-EMP-CONV-DEC-008` | Search | Search Boundary | جست‌وجوی پیام مستقل از Global Search | Collected |

## صفحه جست‌وجوی سراسری

| شناسه | ماژول/دامنه | نوع اثر | خلاصه | وضعیت |
|---|---|---|---|---|
| `PAGE-EMP-SEARCH-DEC-001..002` | `cas_workspace` | Route/Command | Route مستقل و Command Launcher | Collected |
| `PAGE-EMP-SEARCH-DEC-003` | همه ماژول‌های منبع | Provider Registry | جست‌وجوی فرم، اقدام، شخص، سند، نامه و فرایند | Needs Review |
| `PAGE-EMP-SEARCH-DEC-004..005` | Access Resolver, Providerها | Security | Whitelist و جلوگیری از نشت نتیجه | Needs Review |
| `PAGE-EMP-SEARCH-DEC-006` | `cas_workspace` | UX | تجربه واحد برای Route و Data Search | Collected |
| `PAGE-EMP-SEARCH-DEC-007` | `cas_jalali_search` | Date Parsing | تبدیل Query شمسی | Needs Review |

## مرکز اعلان‌ها

| شناسه | ماژول/دامنه | نوع اثر | خلاصه | وضعیت |
|---|---|---|---|---|
| `PAGE-EMP-NOTIF-DEC-001` | Notification Service, `cas_action_hub` | Domain Boundary | اعلان با Action یکی نیست | Needs Review |
| `PAGE-EMP-NOTIF-DEC-002..004` | `cas_workspace`, Notification Service | Data/UI | نوع، منبع، مقصد، Read State و Count | Needs Review |
| `PAGE-EMP-NOTIF-DEC-005` | همه ماژول‌های منبع | Provider Registry | Adapter اعلان | Needs Review |
| `PAGE-EMP-NOTIF-DEC-006` | Mail/Bus/Cron | Delivery | Realtime با fallback | Needs Review |

## تاریخچه اخیر

| شناسه | ماژول/دامنه | نوع اثر | خلاصه | وضعیت |
|---|---|---|---|---|
| `PAGE-EMP-HISTORY-DEC-001` | `cas_workspace`, Audit | Domain Boundary | History مرور با Audit Log متفاوت است | Collected |
| `PAGE-EMP-HISTORY-DEC-002` | Access Resolver | Security | بازبینی مجوز هنگام نمایش | Needs Review |
| `PAGE-EMP-HISTORY-DEC-003..004` | History Service | Data/Preference | Resource Reference و حذف فقط از History | Needs Review |
| `PAGE-EMP-HISTORY-DEC-005` | Security Policy | Privacy | استثنای Routeهای حساس | Needs Review |
| `PAGE-EMP-HISTORY-DEC-006` | User Preference | Persistence | ذخیره سمت سرور در Production | Needs Review |

## پوسته مشترک Workspace

| حوزه | ماژول/دامنه | اثر | وضعیت |
|---|---|---|---|
| Routeهای جدید | `cas_workspace`, Access Resolver | ثبت ۶ Route و ۶ Capability جدید | Needs Review |
| Sidebar | `cas_workspace` | Collapse/Expand، Tooltip و State | Collected |
| Topbar | `cas_workspace` | Search، Conversation، Notification، Appearance و Profile | Collected |
| Theme | `cas_workspace`, Preference | Accent، Dark Mode، Font Scale و Density | Needs Review |
| Widget Registry | `cas_workspace` | ID پایدار، DnD، Error Boundary و State | Needs Review |
| Drawer/Modal | `cas_workspace` | Focus، Escape، State Preservation | Needs Review |
| Router | `cas_workspace` | Deep Link، Browser History و Route State | Needs Review |

## نمای ماژول‌محور جامع

### `cas_workspace` — اثر بسیار زیاد

- Shell و Router
- Navigation و Capability Mapping
- Routeهای `personal-tasks`, `calendar`, `messages`, `global-search-page`, `notifications-center`, `recent-history`
- Dashboard/Hero/Widget Registry
- Drawer و Modal Infrastructure
- Theme و Preference
- Provider Registryهای Search، Calendar، Notification و History
- Topbar Quick Access

وضعیت: `Needs Review`؛ Specification نهایی هنوز تولید نشده است.

### `cas_action_hub` — اثر زیاد

- تغییر عنوان UI از «کارهای من» به «نیازمند اقدام»
- جداسازی Action رسمی از Task شخصی
- Provider اقدام‌های میزکار، Search، Calendar Deadline و Notification

وضعیت: `Needs Review`.

### `cas_work_report` — اثر زیاد

- ثبت سریع و تدریجی
- Widget ترکیبی فعالیت
- تبدیل اختیاری Task به Activity
- مجموع زمان و اختلاف حضور
- Search/History Provider

وضعیت: `Needs Review`.

### `cas_attendance_core` و `cas_attendance_operations` — اثر متوسط

- Hero Presence Provider
- مغایرت و Notification
- Search/History محدود
- Deep Link به ثبت نگهبانی؛ صفحه تخصصی نسخه ۴ حفظ می‌شود

وضعیت: `Needs Review` تا بررسی نقش نگهبان.

### `cas_shift_management` — اثر متوسط

- شیفت امروز
- Calendar Provider
- Notification جابه‌جایی/انتشار
- Search و History

وضعیت: `Needs Review`.

### `cas_correspondence` و `cas_correspondence_advanced` — اثر متوسط

- مرزبندی با Conversation
- Search Provider
- Calendar Deadline
- Notification و Recent History

وضعیت: `Needs Review`.

### `cas_document_core` — اثر متوسط

- Global Search
- Recent History
- فایل گفتگو و Permission Download
- Notification نسخه/OCR در صورت نیاز

وضعیت: `Needs Review`.

### Form/Workflow/Approval/Kardex — اثر متوسط یا کم

هرکدام باید Providerهای Search، Notification، Calendar Deadline و History متناسب با مجوز ارائه دهند. مالکیت داده و عملیات در ماژول اصلی باقی می‌ماند.

### Jalali Suite — اثر متوسط

- Calendar Month View
- Parse بازه شمسی در Search
- نمایش زمان History و Notification
- عدم تغییر مقدار استاندارد ذخیره‌شده

وضعیت: `Needs Review`.

### Odoo Mail/Discuss/Bus — اثر زیاد

- Conversation Source
- Unread Count
- Realtime Delivery
- Member/File Permission

وضعیت: `Needs Review`؛ Adapter نهایی تصویب نشده است.

## قواعد به‌روزرسانی

1. هر صفحه جدید سند مستقل دارد.
2. هر تصمیم با شناسه در این ماتریس ثبت می‌شود.
3. Decisionهای بین‌صفحه‌ای در `04_Decisions` ثبت می‌شوند.
4. Change Set جامع در `06_ChangeSets/CS-WORKSPACE-V7.md` مرجع Audit است.
5. پس از بررسی نقش‌ها و صفحات وابسته، آثار در `03_Modules` Consolidate می‌شوند.
6. فقط Specification ماژولی با وضعیت `Implementation Ready` مجوز اجرا دارد.
