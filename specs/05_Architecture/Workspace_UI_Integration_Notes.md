# یادداشت معماری اتصال Workspace v7

| مشخصه | مقدار |
|---|---|
| وضعیت | `Needs Review` |
| دامنه | بین‌ماژولی / Workspace Integration |
| سند منبع | `../02_UI_UX/Employee/Workspace.md` |

## هدف

ثبت اثرهای معماری احتمالی تصمیم‌های v7 بدون تبدیل آن‌ها به دستور پیاده‌سازی.

## مرز مسئولیت Workspace

`cas_workspace` مسئول موارد زیر است:

- Shell و Navigation
- Route Resolution
- Widget Registry
- Layout و Preference
- Drawer و Modal
- Action Dispatch
- Theme و Design Token

Workspace مالک داده‌های زیر نیست:

- گزارش کار
- حضور و شیفت
- گفتگو و کانال
- رویداد تقویم
- مکاتبه و سند
- تصمیم تأیید

## سرویس‌های احتمالی

### Workspace Preference Service

- Font Scale
- Density
- Accent
- Theme
- Sidebar State
- Widget Order
- Widget Visibility

### Widget Registry

هر Widget احتمالاً نیازمند Metadata زیر است:

- شناسه
- نقش‌ها و Capabilityهای مجاز
- اندازه و ظرفیت
- منبع داده
- Route مقصد
- Empty State
- Refresh Policy
- قابلیت Drag یا Hide

### Conversation Adapter

- دریافت کانال‌ها و گفتگوها از Mail/Bus
- کنترل دسترسی کانال
- Badge خوانده‌نشده
- اتصال به رکورد منبع
- فایل‌ها و اعضا در Drawer

### Calendar Adapter

- تجمیع رویدادهای Calendar و Actionهای زمان‌دار
- تبدیل Jalali در لایه نمایش
- Timezone کاربر
- نمای روز، هفته و ماه

## قواعد امنیت

- Frontend فقط Route و Action مجاز را نمایش می‌دهد.
- Backend بدون `sudo` داده را خوانده و ACL/Record Rule را اعمال می‌کند.
- Preference کاربر نباید Scope دسترسی را تغییر دهد.
- Widget مخفی‌شده همچنان نباید از طریق RPC بدون مجوز قابل خواندن باشد.

## موارد باز

1. مدل نهایی Preference چیست؟
2. Widget Registry در Python، XML یا ترکیب هر دو تعریف می‌شود؟
3. Refresh و Cache Widgetها چگونه مدیریت می‌شود؟
4. Conversation و Calendar Adapter در `cas_workspace` قرار می‌گیرند یا ماژول Bridge مستقل دارند؟
5. ترتیب Widgetها در سطح User، Role یا Company ذخیره می‌شود؟

## محدودیت

این سند Architecture نهایی نیست و تا تجمیع صفحات نقش‌های دیگر نباید مبنای مستقیم Schema یا API قرار گیرد.