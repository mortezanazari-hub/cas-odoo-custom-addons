# ماتریس تجمیع تغییرات ماژول‌ها

این فایل مرجع مرکزی اثر تصمیمات صفحه‌ای بر ماژول‌های پروژه است. ثبت یک ردیف در این ماتریس به معنی دستور پیاده‌سازی نیست.

## وضعیت‌ها

- `Collected`: تصمیم ثبت شده ولی هنوز با سایر صفحات تجمیع نشده است.
- `Needs Review`: نیازمند بررسی صفحات یا نقش‌های دیگر است.
- `Conflict`: با تصمیم دیگری تعارض دارد.
- `Consolidated`: در Specification نهایی ماژول تجمیع شده است.
- `Implementation Ready`: آماده تبدیل به دستور اجرایی است.

## تصمیمات صفحه میزکار کاربر عادی

| شناسه تصمیم | صفحه | ماژول یا دامنه | نوع اثر | خلاصه | وضعیت |
|---|---|---|---|---|---|
| `PAGE-EMP-DESK-DEC-001` | میزکار کاربر | `cas_workspace` | UI / Product | تبدیل داشبورد به میزکار عملیاتی | Collected |
| `PAGE-EMP-DESK-DEC-002` | میزکار کاربر | `cas_workspace`, `cas_attendance_core` | UI / API | خلاصه حضور و تبدیل مغایرت به اقدام | Collected |
| `PAGE-EMP-DESK-DEC-003` | میزکار کاربر | `cas_workspace`, `cas_action_hub` | UI / Action | برنامه امروز به‌عنوان صف اقدام | Needs Review |
| `PAGE-EMP-DESK-DEC-004` | میزکار کاربر | `cas_workspace`, `cas_action_hub` | Terminology | حذف SLA از UI کاربر عادی | Collected |
| `PAGE-EMP-DESK-DEC-005` | میزکار کاربر | `cas_workspace`, `cas_work_report` | UI / API | ثبت سریع فعالیت | Collected |
| `PAGE-EMP-DESK-DEC-006` | میزکار کاربر | `cas_work_report` | Domain / Data | ساخت تدریجی گزارش روزانه | Collected |
| `PAGE-EMP-DESK-DEC-007` | میزکار کاربر | فرهنگ فعالیت، `cas_work_report` | Domain / Data | انتخاب فعالیت استاندارد | Needs Review |
| `PAGE-EMP-DESK-DEC-008` | میزکار کاربر | فرهنگ فعالیت، `cas_work_report` | Workflow / Data | ثبت فعالیت ناموجود و ایجاد پیشنهاد | Collected |
| `PAGE-EMP-DESK-DEC-009` | میزکار کاربر | `cas_work_report` | Rule | عدم توقف گزارش برای استانداردسازی | Collected |
| `PAGE-EMP-DESK-DEC-010` | میزکار کاربر | `cas_work_report`, فرهنگ فعالیت | Audit / Data | حفظ Snapshot اولیه | Collected |
| `PAGE-EMP-DESK-DEC-011` | میزکار کاربر | `cas_work_report`, `cas_workspace` | UI / Reporting | فعالیت‌های امروز و مجموع زمان | Collected |
| `PAGE-EMP-DESK-DEC-012` | میزکار کاربر | `cas_work_report`, `cas_attendance_core` | Validation / Policy | هشدار غیرمسدودکننده اختلاف زمان | Needs Review |
| `PAGE-EMP-DESK-DEC-013` | میزکار کاربر | `cas_workspace` | Preference | میانبرهای شخصی | Collected |
| `PAGE-EMP-DESK-DEC-014` | میزکار کاربر | `cas_workspace` | Preference / UI | شخصی‌سازی چیدمان | Collected |
| `PAGE-EMP-DESK-DEC-015` | میزکار کاربر | `cas_workspace` | Responsive UX | اولویت ثبت سریع در موبایل | Collected |

## نمای ماژول‌محور فعلی

### `cas_workspace`

- تبدیل صفحه اصلی به میزکار عملیاتی
- برنامه امروز و کارهای نیازمند اقدام
- ثبت سریع فعالیت به‌عنوان مصرف‌کننده سرویس گزارش کار
- فعالیت‌های امروز و مجموع زمان
- خلاصه حضور و مغایرت قابل اقدام
- میانبرهای شخصی و شخصی‌سازی Layout
- تجربه فارسی، RTL و Mobile-first

وضعیت: `Needs Review` تا بررسی سایر میزکارها و نقش‌ها.

### `cas_work_report`

- پشتیبانی محصولی از چند فعالیت در یک گزارش روزانه
- ثبت تدریجی و ثبت سریع
- فعالیت پیشنهادی و وضعیت استانداردسازی
- حفظ Snapshot تاریخی
- محاسبه مجموع زمان و هشدار اختلاف با حضور

وضعیت: `Needs Review` تا بررسی صفحه کامل گزارش کار، سرپرست و فرایند تأیید.

### `cas_action_hub`

- تأمین برنامه امروز و کارهای اقدام‌پذیر
- برچسب‌های کاربرپسند موعد به‌جای SLA در UI
- احتمال ایجاد اقدام بررسی پیشنهاد فعالیت

وضعیت: `Needs Review` تا بررسی صفحه کارتابل.

### فرهنگ فعالیت

- فعالیت استاندارد، دسته، Alias و دامنه انتشار
- پیشنهاد فعالیت جدید و فرایند استانداردسازی
- حفظ عنوان اولیه و نگاشت به فعالیت استاندارد

وضعیت: `Needs Review`؛ مرز ماژول هنوز نهایی نیست.

### `cas_attendance_core` و `cas_shift_management`

- ارائه خلاصه حضور و شیفت امروز
- اعلام مغایرت و مسیر اقدام

وضعیت: `Needs Review` تا بررسی صفحات حضور، شیفت و نگهبانی.

## قاعده به‌روزرسانی

پس از هر جلسه بررسی صفحه:

1. تصمیمات صفحه با شناسه یکتا ثبت شوند.
2. ردیف‌های مربوط به ماژول‌های متأثر به این فایل اضافه شوند.
3. تعارض‌ها و وابستگی‌ها مشخص شوند.
4. پس از پایان بررسی صفحات، ردیف‌ها ماژول‌به‌ماژول Consolidate شوند.
5. تنها Specification تجمیع‌شده و تأییدشده مبنای پیاده‌سازی قرار گیرد.
