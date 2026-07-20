# سند تصمیم پوسته مشترک Workspace نسخه ۷

| مشخصه | مقدار |
|---|---|
| شناسه | `UI-SHELL-001` |
| خط مبنا | `CAS_UI_Prototype_V4` |
| نسخه هدف | `CAS UI Workspace v7` |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Needs Review` |
| نقش‌ها | همه نقش‌ها |

## دامنه

این سند تغییرات مشترکی را پوشش می‌دهد که فقط متعلق به صفحه میزکار کاربر عادی نیستند و بر تمام نقش‌ها، Routeها و صفحات Workspace اثر دارند.

## تغییرات نسبت به نسخه ۴

### Navigation و Capability

در نسخه ۷ Capabilityهای زیر به تمام نقش‌های مرتبط افزوده شده‌اند:

- `personal.tasks`
- `calendar.use`
- `discuss.use`
- `search.global`
- `notification.read`
- `history.read`

گروه «فضای کاری» از ساختار محدود نسخه ۴ به مجموعه زیر توسعه یافته است:

1. میزکار
2. کارهای من
3. تقویم
4. گفت‌وگوها
5. نیازمند اقدام
6. جست‌وجوی سازمان
7. مرکز اعلان‌ها
8. تاریخچه اخیر
9. ثبت درخواست
10. پیگیری درخواست‌ها
11. گزارش روزانه
12. حضور و شیفت
13. مکاتبات

### تفکیک مفهومی Routeها

- `home`: میزکار و مرکز فرمان شخصی
- `personal-tasks`: کارهای شخصی
- `my-actions`: اقدام‌های سازمانی منتظر انجام یا تصمیم
- `messages`: ارتباط سریع سازمانی
- `correspondence`: مکاتبه رسمی
- `notifications-center`: اطلاع‌رسانی
- `recent-history`: سابقه مرور کاربر
- `audit-log`: ممیزی رسمی سامانه

این مفاهیم نباید در Backend یا UI با هم ادغام شوند.

## Sidebar

- Sidebar واقعاً Collapse/Expand می‌شود.
- در حالت بسته، آیکن‌ها باقی می‌مانند و Labelها مخفی می‌شوند.
- کنترل بازکردن در هر دو وضعیت قابل دسترس است.
- Tooltip مسیرها در حالت جمع‌شده ضروری است.
- وضعیت کاربر ذخیره می‌شود.
- ساختار منو بر اساس Capability مؤثر ساخته می‌شود، نه عنوان نقش.

## Topbar و Quick Access

Topbar در نسخه ۷ فقط نوار عنوان نیست و دسترسی سریع به موارد زیر را فراهم می‌کند:

- جست‌وجوی سراسری
- گفت‌وگوهای سریع
- اعلان‌ها
- تنظیمات ظاهری
- پروفایل کاربر

Quick Access نباید Route یا مجوز جدیدی ایجاد کند؛ فقط میانبر همان Capability و Route رسمی است.

## Theme و خوانایی

- حداقل متن کاربردی ۱۲ پیکسل است.
- سه مقیاس خوانایی: فشرده، استاندارد و بزرگ.
- دو حالت تراکم: فشرده و راحت.
- Accent Color سراسری.
- Light Mode و Dark Mode.
- تغییر Theme نباید Contrast، وضعیت Focus، Badgeهای بحرانی یا هویت سازمانی را تخریب کند.
- تنظیمات Prototype در Local Storage و Production در Preference کاربر Odoo ذخیره می‌شوند.

## Widget System

- Widgetها دارای شناسه پایدار هستند.
- ترتیب Widgetهای مجاز با Drag & Drop تغییر می‌کند.
- ترتیب انتخابی کاربر ذخیره می‌شود.
- Header، Tab و Footer ثابت‌اند و فقط Body فهرست Scroll می‌شود.
- کارت‌های هم‌ردیف ارتفاع یکسان دارند.
- فهرست‌های کم‌داده برای حفظ ریتم بصری با ردیف خالی غیرفعال تکمیل می‌شوند.
- Widget باید حالت‌های `loading`, `empty`, `error`, `unavailable`, `forbidden`, `ready` را پوشش دهد.
- Widget مالک داده کسب‌وکاری نیست و از Adapter ماژول منبع استفاده می‌کند.

## Drawer و Modal

- اطلاعات جانبی، تنظیمات سبک و جزئیات غیرمحوری در Drawer باز می‌شوند.
- عملیات رسمی مانند تأیید، رد، ارسال و انتشار باید به متد دامنه ماژول منبع متصل شوند.
- بستن لایه نباید State اصلی Route را از بین ببرد.
- Focus Trap، Escape و بازگشت Focus برای دسترس‌پذیری الزامی است.

## State و Preferenceهای جدید

- وضعیت Sidebar
- Theme
- Accent Color
- Font Scale
- Density
- ترتیب Widgetها
- نمای آخر تقویم
- فیلترهای صفحه در صورت تصویب
- آخرین Route معتبر

## Actionهای مشترک جدید نسخه ۷

- `toggle-sidebar`
- `appearance-settings`
- `set-v7-setting`
- `quick-conversations`
- `notifications`
- `global-search`
- Actionهای Navigation و Drawer مربوط به صفحات جدید

## اثر بر معماری

| بخش | اثر |
|---|---|
| `cas_workspace` | Shell، Router، Registry، Widget، Drawer، Preferences و Action Dispatch |
| Access Resolver | Capabilityهای جدید و Routeهای جدید |
| Theme Service | Tokenها، Contrast و Preference |
| Search/Notification/History/Calendar/Discuss Adapters | سرویس‌های مشترک جدید |
| ماژول‌های منبع | Provider و Deep Link بدون انتقال مالکیت داده |

## معیارهای پذیرش

- تمام نقش‌ها فقط Routeهای مجاز خود را ببینند.
- تغییر ظاهر و Layout پس از Reload حفظ شود.
- Sidebar در هر دو حالت قابل استفاده باشد.
- هیچ Widget یا صفحه‌ای با نبود ماژول اختیاری Shell را Crash نکند.
- Theme و Font Scale در تمام صفحات، نه فقط میزکار، اعمال شوند.
- Routeهای جدید با Back/Forward مرورگر و Deep Link سازگار باشند.
