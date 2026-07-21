# Page Specification — میزکار کاربر در Workspace v8

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-WORKSPACE-HOME-V8` |
| نسخه | `v8 through iteration 12` |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Consolidated` |
| Route | `workspace-home` |
| مالک UI | `cas_workspace` |
| مالک داده | Providerهای دامنه |
| جایگزین مرجع فعال | `Employee/Workspace.md` نسخه ۷ |

## هدف

میزکار نقطه ورود عملیاتی کاربر است و باید پاسخ دهد:

- اکنون چه کاری مهم‌تر است؟
- برنامه و شیفت فعلی چیست؟
- کدام گزارش، Action یا پیام نیازمند توجه است؟
- سریع‌ترین مسیر برای اقدام بعدی چیست؟

میزکار نباید به مجموعه‌ای از نمودارها یا کپی منوهای Odoo تبدیل شود.

## نقش‌ها

تمام کاربران داخلی دارای Workspace. محتوا و Widgetها براساس Company Policy، Role/Profile، Capability و Provider Availability متفاوت‌اند.

## ساختار صفحه

### ۱. Hero

- خوش‌آمدگویی و تاریخ
- وضعیت شیفت یا حضور
- موارد نیازمند اقدام
- جلسه یا رویداد بعدی
- وضعیت گزارش شیفت
- ورودی Command Palette

### ۲. نوار عملیات پرتکرار

عملیات فقط در صورت وجود Capability و Provider مجاز نمایش داده می‌شوند؛ مانند:

- ثبت درخواست
- Personal Task جدید
- Action سازمانی جدید
- Event جدید
- ثبت Activity
- نامه رسمی جدید
- شروع Conversation
- مشاهده حضور و شیفت

### ۳. Grid Widgetها

Widgetهای نمونه:

- Personal Tasks
- Action Hub
- Calendar
- Conversations
- Work Report Status
- Shift/Attendance Summary
- Announcements
- Recent Operational Items

فهرست قطعی Widgetها از Dashboard Configuration و Provider Registry Resolve می‌شود.

## مالکیت داده

Workspace فقط Layout، ترتیب، Theme، Density و Preference را نگه می‌دارد. تمام Cardها و Actionها باید از Provider مالک Domain دریافت شوند.

## Dashboard Resolution

```text
System Default
→ Company Policy
→ Role/Profile Default
→ User Preference
```

- Company Policy می‌تواند Widget یا تنظیم را Lock کند.
- کاربر عادی در v8 فقط Widgetهای مجاز را Reorder می‌کند.
- Hide/Show و Resize آزاد در v8 فعال نیست.
- ادمین از Dashboard Management Center پیکربندی را Publish می‌کند.

## رفتار Widget

هر Widget Contract باید شامل موارد زیر باشد:

- `provider_key`
- `widget_key`
- عنوان و Icon
- Capability لازم
- Supported Sizes
- Data Fetch Contract
- Primary Action
- Empty/Unavailable/Error State
- Refresh Policy
- Deep Link
- Company/Role Scope

## Work Report Status

- گزارش براساس Shift Occurrence است.
- اگر Applicability شخص `Disabled` باشد، Widget ثبت گزارش نمایش داده نمی‌شود.
- اگر شخص فقط دسترسی مشاهده گزارش دیگران داشته باشد، Widget Review/Monitoring نمایش داده می‌شود.
- چند Assignment در یک شیفت به یک گزارش ترکیبی منتهی می‌شود.

## Search

- Search صفحه مستقل ندارد.
- Hero و Topbar یک Command Palette مشترک را باز می‌کنند.
- Query خالی Recent Items مجاز را نشان می‌دهد.
- Search Permission هر Provider در Backend اعمال می‌شود.

## Stateها

### Loading

Skeleton سطح Shell و Widgetها مستقل است. کندی یک Provider نباید کل صفحه را متوقف کند.

### Partial Failure

Widget Provider شکست‌خورده Unavailable/Error محلی نشان می‌دهد و سایر Widgetها فعال می‌مانند.

### Empty

Empty State باید اقدام بعدی معنادار داشته باشد و صرفاً «داده‌ای نیست» نباشد.

### Forbidden

Widget یا Action غیرمجاز نمایش داده نمی‌شود؛ Route مستقیم نیز در Backend Forbidden است.

### Provider Unavailable

پیام وضعیت و امکان Retry یا مراجعه به ادمین نمایش داده می‌شود.

## Responsive و RTL

- RTL واقعی
- Navigation و Drag Handle متناسب با RTL
- Mobile First برای اقدام‌های پرتکرار
- حداقل اندازه متن کاربردی ۱۲ پیکسل
- Touch Target مناسب
- Native Page Scroll

## دسترس‌پذیری

- Drag and Drop جایگزین Keyboard دارد.
- Focus Order منطقی است.
- Command Palette Focus Trap و Restore دارد.
- Icon-only Action دارای Accessible Label است.

## امنیت

- Workspace داده را با `sudo` تجمیع نمی‌کند.
- Provider فقط رکوردهای مجاز را برمی‌گرداند.
- Capability فقط Navigation را کنترل می‌کند.
- تغییر Preference حق تغییر Company Policy Lock‌شده را ندارد.

## معیار پذیرش

1. Workspace بدون مالکیت داده Domainها کار کند.
2. خرابی یک Provider کل صفحه را از کار نیندازد.
3. Search و History Route مستقل نداشته باشند.
4. Widgetهای کاربر مطابق Policy Resolve شوند.
5. کاربر فقط Widgetهای مجاز را جابه‌جا کند.
6. Work Report UI با Applicability و Shift فعلی سازگار باشد.
7. تمام حالت‌های Loading، Empty، Error، Forbidden و Unavailable پوشش داده شوند.
8. RTL، Keyboard و Focus در تمام Interactionها صحیح باشند.