# سند تصمیم صفحه تقویم

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-EMP-CAL-001` |
| خط مبنا | نسخه ۴ |
| نسخه هدف | نسخه ۷ |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Needs Review` |
| نقش‌ها | همه کاربران دارای `calendar.use` |

## تغییر نسبت به نسخه ۴

نسخه ۴ صفحه و Route عمومی مستقل تقویم نداشت. نسخه ۷ Route مستقل `calendar`، Capability مستقل `calendar.use`، Widget تقویم در میزکار و سه نمای روز، هفته و ماه را اضافه کرده است.

## تصمیمات

- `PAGE-EMP-CAL-DEC-001`: تقویم یک قابلیت سطح اول Workspace است.
- `PAGE-EMP-CAL-DEC-002`: صفحه کامل و Widget میزکار باید از یک سرویس داده استفاده کنند.
- `PAGE-EMP-CAL-DEC-003`: سه نمای روز، هفته و ماه الزامی‌اند.
- `PAGE-EMP-CAL-DEC-004`: نمای ماه شامل عنوان ماه و سال شمسی، سربرگ شنبه تا جمعه، روز جاری، روزهای دارای رویداد و ناوبری ماه قبل/بعد است.
- `PAGE-EMP-CAL-DEC-005`: ذخیره تاریخ در Odoo استاندارد و UTC باقی می‌ماند؛ جلالی فقط لایه نمایش و ورودی است.
- `PAGE-EMP-CAL-DEC-006`: ساخت رویداد از Modal انجام می‌شود و در Production باید به Calendar واقعی یا Adapter رسمی متصل شود.
- `PAGE-EMP-CAL-DEC-007`: رویدادها می‌توانند از جلسات، Taskها، Workflow Deadlineها، شیفت‌ها و مکاتبات موعددار تجمیع شوند؛ مالکیت رکورد در ماژول منبع باقی می‌ماند.

## Actionها

`calendar-view`، `calendar-next`، `calendar-prev`، `calendar-today`، `new-calendar-event`، `calendar-event-detail`، `open-calendar-day`، `home-calendar-view`، `home-calendar-month-next` و `home-calendar-month-prev`.

## اثر ماژولی

| ماژول | اثر |
|---|---|
| `cas_workspace` | Route، Widget، View State و Adapter تجمیع |
| `cas_shift_management` | ارائه شیفت‌ها به تقویم |
| `cas_action_hub` | ارائه موعد اقدام‌ها |
| `cas_correspondence` | ارائه موعد نامه و ارجاع |
| `cas_workflow_core` | ارائه Deadline مرحله‌ها |
| Calendar Integration | ایجاد و ویرایش رویداد واقعی |
| Jalali Suite | نمایش و فیلتر تاریخ شمسی |

## معیارهای پذیرش

- تغییر View بدون خروج از صفحه انجام شود.
- صفحه کامل و Widget رفتار یکسان داشته باشند.
- روز جاری و رویدادها در نمای ماه قابل تشخیص باشند.
- اختلاف Timezone و تبدیل جلالی سبب تغییر مقدار ذخیره‌شده نشود.
- نبود ماژول منبع موجب Crash پوسته نشود و `unavailable` کنترل‌شده برگردد.
