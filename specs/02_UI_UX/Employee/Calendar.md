# سند تصمیم صفحه تقویم

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-EMP-CAL-001` |
| خط مبنا | نسخه ۴ |
| نسخه قبلی | نسخه ۷ |
| نسخه هدف | نسخه ۸ |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Needs Review` |
| وضعیت پیاده‌سازی | Prototype تأییدشده؛ Production پس از تصویب قراردادها |
| نقش‌ها | همه کاربران دارای `calendar.use` |

## هدف

تقویم، قابلیت سطح اول Workspace برای مشاهده رویدادها، ساخت جلسه، دریافت دعوت، مشاهده موعدها و در صورت مجازبودن تخصیص وظیفه به زیرمجموعه است.

## تغییر نسبت به نسخه ۷

نسخه ۷ Route مستقل، Widget و سه نمای روز/هفته/ماه را ایجاد کرد. نسخه ۸ Modal ساخت رویداد و انتخاب شرکت‌کنندگان را بازطراحی می‌کند:

- حذف فهرست کامل کارکنان از Modal
- Selector مستقل و جست‌وجومحور
- جست‌وجوی Server-side و صفحه‌بندی‌شده
- فیلتر واحد و محدوده سازمانی
- تفکیک دعوت از تخصیص وظیفه
- محدودکردن Task به زیرمجموعه مجاز
- نمایش انتخاب‌شده‌ها به‌صورت Chip
- حذف Scroll تودرتو و کنترل عمومی متناقض
- اصلاح Layering، Focus و بازگشت State بین Modal و Selector

## ساختار صفحه تقویم

1. Header و تغییر نمای روز/هفته/ماه
2. ناوبری قبل/بعد و امروز
3. Feed تجمیعی رویدادها
4. Modal ساخت/ویرایش رویداد
5. Selector مستقل شرکت‌کنندگان
6. Detail View رویداد
7. Loading، Empty، Forbidden، Error و Unavailable State

## Modal رویداد

فیلدهای حداقلی:

- عنوان رویداد
- تاریخ
- زمان شروع
- زمان پایان
- نوع رویداد
- شرکت‌کنندگان
- توضیحات

قواعد Layout:

- Header و Footer ثابت‌اند.
- فقط Body در صورت نیاز Scroll می‌خورد.
- Footer روی محتوا Overlay نمی‌شود.
- Scroll تودرتوی غیرضروری وجود ندارد.
- Modal در Viewportهای کوچک Responsive است.

## Selector شرکت‌کنندگان

### رفتار اولیه

- هیچ‌گاه همه کارکنان بارگذاری نمی‌شوند.
- حالت اولیه فقط افراد اخیر، پرتکرار و زیرمجموعه‌های مستقیم محدود را نشان می‌دهد.
- جست‌وجوی آزاد پس از حداقل دو نویسه اجرا می‌شود.
- هر درخواست حداکثر تعداد محدود، ترجیحاً ۲۰ نتیجه، برمی‌گرداند.
- نتایج Production باید Server-side، صفحه‌بندی‌شده یا Virtualized باشند.

### فیلترها

- واحد سازمانی
- محدوده سازمانی
- زیرمجموعه‌های من
- افراد اخیر
- همه افراد قابل دعوت

عبارت‌های مبهمی مانند «همه واحدهای مجاز» بدون توضیح Scope نباید استفاده شوند.

### اطلاعات هر نتیجه

- نام و آواتار
- عنوان شغلی
- واحد
- نوع رابطه سازمانی
- وضعیت مجوز: `زیرمجموعه مجاز` یا `فقط دعوت`

### انتخاب و نوع ارسال

کنترل روش ارسال فقط پس از انتخاب شخص ظاهر می‌شود.

برای زیرمجموعه مجاز:

- دعوت‌نامه تقویمی
- وظیفه در کارتابل
- دعوت‌نامه و وظیفه

برای فرد خارج از محدوده تخصیص:

- فقط دعوت‌نامه، به‌صورت Read-only

دلیل عدم امکان Task باید قابل مشاهده باشد.

### جمع‌بندی انتخاب‌ها

- افراد انتخاب‌شده به‌صورت Chip نمایش داده می‌شوند.
- حذف Chip انتخاب فرد را لغو می‌کند.
- دکمه «تأیید شرکت‌کنندگان» انتخاب‌ها را به Modal اصلی برمی‌گرداند.
- انصراف، تغییرات موقت Selector را کنار می‌گذارد.
- Modal اصلی بعد از تأیید باز می‌ماند.

## Layering و Focus

- Selector Child Overlay از Modal رویداد است و باید بالاتر از آن رندر شود.
- Modal زیرین هنگام بازبودن Selector Inert است.
- Escape ابتدا Selector را می‌بندد، نه Modal اصلی را.
- پس از بستن Selector، Focus به دکمه «انتخاب شرکت‌کنندگان» بازمی‌گردد.
- State واردشده در Modal اصلی حفظ می‌شود.

## تصمیمات قطعی

- `PAGE-EMP-CAL-DEC-001`: تقویم قابلیت سطح اول Workspace است.
- `PAGE-EMP-CAL-DEC-002`: صفحه و Widget از یک Feed استفاده می‌کنند.
- `PAGE-EMP-CAL-DEC-003`: سه نمای روز، هفته و ماه الزامی‌اند.
- `PAGE-EMP-CAL-DEC-004`: نمای ماه شمسی کامل است.
- `PAGE-EMP-CAL-DEC-005`: ذخیره تاریخ استاندارد Odoo و UTC باقی می‌ماند.
- `PAGE-EMP-CAL-DEC-006`: ایجاد رویداد به Calendar واقعی یا Adapter رسمی متصل می‌شود.
- `PAGE-EMP-CAL-DEC-007`: Feed از Providerهای چندماژولی تجمیع می‌شود.
- `PAGE-EMP-CAL-DEC-008`: انتخاب شرکت‌کننده جست‌وجومحور و Server-side است.
- `PAGE-EMP-CAL-DEC-009`: دعوت و تخصیص وظیفه Operationهای مستقل هستند.
- `PAGE-EMP-CAL-DEC-010`: Task فقط برای Scope سازمانی مجاز قابل ایجاد است.
- `PAGE-EMP-CAL-DEC-011`: نوع ارسال برای هر فرد مستقل تعیین می‌شود.
- `PAGE-EMP-CAL-DEC-012`: Overlay Stack و Focus باید قرارداد مشترک Workspace را رعایت کند.

## امنیت و مجوز

- Invitation Permission با Task Assignment Permission برابر نیست.
- Backend باید شرکت فعال، انتساب معتبر، رابطه مدیریتی، Capability، ACL و Record Rule را بررسی کند.
- نتیجه Directory Search نباید اطلاعات فرد غیرمجاز را افشا کند.
- تغییر شناسه فرد در Request نباید Rule تخصیص را دور بزند.
- ارسال دعوت و ساخت Task باید Transaction و خطای مستقل و قابل گزارش داشته باشند.

## اثر ماژولی

| ماژول/دامنه | اثر |
|---|---|
| `cas_workspace` | Route، Modal، Selector، Overlay Manager و State |
| Odoo Calendar/Event | ایجاد رویداد، Attendee و Invitation |
| HR/Employee Directory | جست‌وجوی کارکنان |
| Organization Hierarchy | محاسبه رابطه مدیریتی و Scope |
| `cas_action_hub` | ایجاد Action/Task رسمی در صورت انتخاب وظیفه |
| `cas_personal_task` | فقط در صورت تعریف Task شخصی برای خود کاربر |
| Mail/Notification | دعوت و اعلان |
| `cas_shift_management` | Calendar Provider |
| `cas_correspondence` | Deadline Provider |
| `cas_workflow_core` | Deadline Provider |
| Jalali Suite | نمایش و ورود شمسی |

## معیارهای پذیرش

- زمان بازشدن Modal به تعداد کل کارکنان وابسته نباشد.
- هیچ فهرست کامل Client-side از کارکنان ساخته نشود.
- جست‌وجو و فیلتر Server-side باشند.
- افراد خارج از Scope فقط دعوت دریافت کنند.
- RPC مستقیم نتواند Task غیرمجاز بسازد.
- Modal اصلی هنگام کار با Selector State خود را حفظ کند.
- Selector روی Modal و نه پشت آن باز شود.
- Focus و Escape در Stack لایه‌ها صحیح عمل کنند.
- Header/Footer ثابت و Scroll کنترل‌شده باشد.
- نبود Provider اختیاری موجب Crash نشود.

## اسناد مرتبط

- `04_Decisions/DEC-013-Calendar-Attendee-Selection-And-Assignment-Authorization.md`
- `04_Decisions/DEC-015-Overlay-Layering-And-Focus-Management.md`
- `05_Architecture/V8-Interaction-And-Integration-Contracts.md`
- `03_Modules/V8_Impact_Assessment.md`
- `06_ChangeSets/CS-WORKSPACE-V8.md`
