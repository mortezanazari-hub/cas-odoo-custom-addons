# DEC-004 — سیستم Widget میزکار

| مشخصه | مقدار |
|---|---|
| شناسه | `DEC-004` |
| وضعیت | `Agreed` |
| دامنه | Workspace / Dashboard / User Preference |
| اسناد مرتبط | `../02_UI_UX/Employee/Workspace.md` |

## زمینه

در نسخه ۴، اجزای میزکار ارتفاع، تراکم و وزن بصری هماهنگ نداشتند. برخی کارت‌ها با داده کم کوتاه و برخی با داده بیشتر بسیار بلند می‌شدند. این وضعیت نظم Grid را از بین می‌برد و شخصی‌سازی را دشوار می‌کرد.

## تصمیم

Workspace از سیستم Widget با قواعد زیر استفاده می‌کند:

1. Widgetهای هم‌ردیف ارتفاع ثابت دارند.
2. Header، Tab و Footer ثابت می‌مانند.
3. فقط Body Widget Scroll می‌شود.
4. فهرست‌های کم‌داده با ردیف خالی غیرفعال تا ظرفیت بصری تعریف‌شده تکمیل می‌شوند.
5. ردیف خالی Loading State نیست.
6. Widgetها با Drag & Drop قابل جابه‌جایی‌اند.
7. در Prototype ترتیب در Local Storage و در Production در Preference سمت سرور ذخیره می‌شود.
8. Drag از Header انجام می‌شود تا Body همچنان Scroll و Interaction عادی داشته باشد.

## گزینه‌های ردشده

- ارتفاع خودکار برای هر Widget
- Masonry Layout بدون ردیف مشخص
- Scroll کل صفحه به‌جای Scroll داخلی Widget
- Skeleton دائمی برای پرکردن فضای خالی
- ذخیره ترتیب فقط در Frontend Production

## پیامدها

### مثبت

- Grid منظم و قابل پیش‌بینی
- کاهش پرش Layout
- سازگاری بهتر با Drag & Drop
- امکان تعریف Widget Registry
- تجربه یکنواخت در نقش‌های مختلف

### منفی یا هزینه

- نیاز به تعریف ظرفیت و Height Token
- نیاز به مدیریت Overflow برای انواع محتوا
- نیاز به مدل Preference در Production

## وضعیت پیاده‌سازی

این تصمیم محصولی مورد توافق است، اما طراحی نهایی Widget Registry، مدل Preference و API هنوز `Needs Review` است.