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
| `PAGE-EMP-DESK-DEC-016` | میزکار کاربر | `cas_workspace` | UI / Composition | Hero سه‌ردیفه و منظم | Collected |
| `PAGE-EMP-DESK-DEC-017` | میزکار کاربر | `cas_workspace`, Mail/Bus | Navigation / Communication | گفتگو قابلیت سطح اول | Needs Review |
| `PAGE-EMP-DESK-DEC-018` | میزکار کاربر | `cas_workspace` | Iconography | آیکن دو حباب گفتگو | Collected |
| `PAGE-EMP-DESK-DEC-019` | میزکار کاربر | `cas_workspace`, Mail/Bus | UI / Drawer | جزئیات گفتگو در Drawer | Needs Review |
| `PAGE-EMP-DESK-DEC-020` | میزکار کاربر | `cas_workspace`, Calendar | UI / Integration | تقویم روز، هفته و ماه در میزکار | Needs Review |
| `PAGE-EMP-DESK-DEC-021` | میزکار کاربر | Calendar, Jalali | UI / Date | نمای ماهانه شمسی کامل | Needs Review |
| `PAGE-EMP-DESK-DEC-022` | میزکار کاربر | `cas_workspace` | Widget / Layout | ارتفاع ثابت Widgetها | Collected |
| `PAGE-EMP-DESK-DEC-023` | میزکار کاربر | `cas_workspace` | Widget / Empty State | ظرفیت ثابت و ردیف خالی غیرفعال | Collected |
| `PAGE-EMP-DESK-DEC-024` | میزکار کاربر | `cas_workspace`, User Preference | Preference / DnD | Drag & Drop Widgetها | Needs Review |
| `PAGE-EMP-DESK-DEC-025` | میزکار کاربر | `cas_workspace` | Accessibility / Typography | سه حالت خوانایی | Collected |
| `PAGE-EMP-DESK-DEC-026` | میزکار کاربر | `cas_workspace` | Theme / Design System | Accent سراسری و Light/Dark Mode | Needs Review |
| `PAGE-EMP-DESK-DEC-027` | میزکار کاربر | `cas_workspace` | Shell / Navigation | Sidebar جمع‌شونده و پایدار | Collected |
| `PAGE-EMP-DESK-DEC-028` | میزکار کاربر | `cas_workspace`, `cas_work_report` | UI / Consolidation | ادغام ثبت و مرور فعالیت | Collected |
| `PAGE-EMP-DESK-DEC-029` | میزکار کاربر | `cas_workspace` | UI / Consolidation | ادغام میانبرها در نوار عملیات | Collected |
| `PAGE-EMP-DESK-DEC-030` | میزکار کاربر | `cas_workspace` | Accessibility | حداقل متن کاربردی ۱۲ پیکسل | Collected |

## Decision Recordهای مشترک

| شناسه | دامنه | خلاصه | وضعیت |
|---|---|---|---|
| `DEC-004` | Workspace / Preference | سیستم Widget با ارتفاع ثابت، Scroll داخلی و Drag | Agreed |
| `DEC-005` | Communication | گفتگو قابلیت سطح اول Workspace است | Agreed |
| `DEC-006` | Design System | خوانایی، Accent و Dark Mode سراسری | Agreed |
| `DEC-007` | Shell / Navigation | Sidebar جمع‌شونده و پایدار | Agreed |
| `DEC-008` | Calendar | تقویم تعاملی داخل میزکار | Agreed |

## نمای ماژول‌محور فعلی

### `cas_workspace`

- میزکار عملیاتی و Hero روزانه
- Action Strip و جست‌وجوی سراسری
- Widget Registry و Layout
- ارتفاع ثابت، Scroll داخلی و Empty Row
- Drag & Drop و User Preference
- Theme، Accent، Density و Typography
- Sidebar جمع‌شونده
- Quick Conversations و Drawer
- Calendar Widget و Adapterهای نمایشی
- تجربه فارسی، RTL و Responsive

وضعیت: `Needs Review` تا بررسی Workspace نقش‌های دیگر، Settings و قرارداد Preference.

### `cas_work_report`

- گزارش چندفعالیتی
- ثبت تدریجی و ثبت سریع
- ادغام ثبت و مرور فعالیت در میزکار
- Snapshot تاریخی
- مجموع زمان و اختلاف حضور

وضعیت: `Needs Review` تا بررسی صفحه کامل گزارش کار و فرایند تأیید.

### `cas_action_hub`

- برنامه امروز و اقدام‌های قابل انجام
- برچسب‌های کاربرپسند موعد
- منبع Widget «نیازمند اقدام»

وضعیت: `Needs Review` تا بررسی صفحه کارتابل و SLA Adapter.

### Mail/Bus و `cas_correspondence`

- منبع گفتگوها، Badge خوانده‌نشده و کانال‌ها
- ارتباط گفتگو با رکورد منبع
- Drawer اعضا و فایل‌ها

وضعیت: `Needs Review` تا بررسی صفحه کامل گفتگو و Permission Model.

### Calendar و Jalali

- منبع واحد رویدادهای روز، هفته و ماه
- ناوبری ماهانه شمسی
- Timezone و Date Conversion

وضعیت: `Needs Review` تا تعیین Adapter و Source Aggregation.

### User Preference

- اندازه متن
- Density
- Accent و Theme
- وضعیت Sidebar
- ترتیب Widgetها

وضعیت: `Needs Review`؛ مدل سمت سرور و Scope ذخیره‌سازی نهایی نشده است.

### فرهنگ فعالیت

- فعالیت استاندارد، دسته، Alias و دامنه انتشار
- پیشنهاد فعالیت و استانداردسازی
- حفظ عنوان اولیه و نگاشت

وضعیت: `Needs Review`؛ مرز ماژول نهایی نیست.

### `cas_attendance_core` و `cas_shift_management`

- خلاصه حضور و شیفت
- مغایرت و مسیر اقدام
- رویدادهای برنامه مرتبط با تقویم

وضعیت: `Needs Review` تا بررسی صفحات حضور، شیفت و نگهبانی.

## قاعده به‌روزرسانی

پس از هر جلسه بررسی صفحه:

1. تصمیمات صفحه با شناسه یکتا ثبت شوند.
2. ردیف‌های ماژول‌های متأثر به این فایل اضافه شوند.
3. تعارض‌ها و وابستگی‌ها مشخص شوند.
4. تصمیم مشترک در `04_Decisions` ثبت شود.
5. پس از پایان بررسی صفحات، ردیف‌ها ماژول‌به‌ماژول Consolidate شوند.
6. تنها Specification تجمیع‌شده و تأییدشده مبنای پیاده‌سازی قرار گیرد.