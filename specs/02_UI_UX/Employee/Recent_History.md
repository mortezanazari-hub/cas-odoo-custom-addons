# سند تصمیم تاریخچه اخیر

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-EMP-HISTORY-001` |
| نسخه هدف | `CAS UI Workspace v8` |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Needs Review` |
| نوع تجربه | قابلیت داخلی Command Palette؛ بدون صفحه مستقل |

## تصمیم نهایی نسخه ۸

صفحه، Navigation Item و Route مستقل `recent-history` حذف می‌شوند. تاریخچه اخیر به‌عنوان یک قابلیت سبک ناوبری در حالت خالی Modal جست‌وجوی سازمانی نمایش داده می‌شود.

## هدف

کمک به بازگشت سریع کاربر به رکوردها و مسیرهایی که واقعاً باز کرده است، بدون ایجاد یک مقصد کاری و صفحه اضافی در Sidebar.

## موارد قابل نمایش

- رکوردهای اخیراً مشاهده‌شده
- جست‌وجوهای اخیر
- موارد سنجاق‌شده
- عملیات پرتکرار مجاز

## قواعد ثبت

- فقط بازشدن واقعی Route یا Record ثبت می‌شود؛ Hover و Preview ثبت نمی‌شوند.
- هر آیتم شامل Resource Reference، نوع منبع، عنوان امن و زمان آخرین مشاهده است.
- تعداد نگهداری محدود و قابل پیکربندی است.
- Routeهای حساس می‌توانند از ثبت مستثنا شوند.
- حذف یک آیتم یا پاک‌کردن History فقط Preference کاربر را تغییر می‌دهد و به رکورد منبع دست نمی‌زند.

## امنیت و Privacy

- Permission هنگام ثبت، نمایش و بازکردن مجدد بررسی می‌شود.
- Snapshot عنوان پس از سلب دسترسی نباید نمایش داده شود.
- محتوای سند، پیام یا نامه در History Cache نمی‌شود.
- History جایگزین Audit Log نیست.
- Capability مستقل `history.read` حذف می‌شود؛ دسترسی هر مورد تابع Resource اصلی است.

## مالکیت و ذخیره‌سازی

- فعلاً ماژول مستقل `cas_recent_history` ساخته نمی‌شود.
- Service سبک می‌تواند در `cas_workspace` یا Preference Service قرار گیرد.
- Local Storage فقط برای Prototype مجاز است؛ Production باید User-scoped و سمت سرور باشد.

## تصمیمات

- `PAGE-EMP-HISTORY-DEC-001`: Recent History با Audit Log متفاوت است.
- `PAGE-EMP-HISTORY-DEC-002`: صفحه و Route مستقل حذف می‌شوند.
- `PAGE-EMP-HISTORY-DEC-003`: History در Query خالی Command Palette نمایش داده می‌شود.
- `PAGE-EMP-HISTORY-DEC-004`: حذف History اثری روی رکورد منبع ندارد.
- `PAGE-EMP-HISTORY-DEC-005`: مسیرهای حساس قابل استثنا هستند.
- `PAGE-EMP-HISTORY-DEC-006`: Production Storage سمت سرور و User-scoped است.
- `PAGE-EMP-HISTORY-DEC-007`: مجوز هر Resource در زمان نمایش مجدداً بررسی می‌شود.

## معیارهای پذیرش

- `recent-history` در Router و Navigation وجود نداشته باشد.
- Recent Items در Query خالی Modal جست‌وجو نمایش داده شوند.
- رکورد حذف‌شده یا غیرمجاز Mask یا حذف شود.
- پاک‌کردن History هیچ رکورد کسب‌وکاری را تغییر ندهد.
- تاریخچه روی دستگاه‌های مختلف در Production قابل بازیابی باشد.
