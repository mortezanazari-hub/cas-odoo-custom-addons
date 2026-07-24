# ایستگاه سریع ثبت تردد نگهبانی

| مشخصه | مقدار |
|---|---|
| Document ID | `PAGE-GUARD-ATTENDANCE-STATION` |
| Document Type | Page Specification |
| Status | `Active` |
| Document Version | `2.0` |
| Created At | `2026-07-22` |
| Updated At | `2026-07-24` |
| Owner | Attendance Operations |
| Source UI Review Cycle | `CAS UI Review Cycle 10–11` |
| Source Iteration | `Cycle 10 I11–I12؛ Cycle 11 I1–I7` |
| Domain Owner | Attendance Operations |
| Affected Modules | `cas_attendance_operations`, `cas_attendance_core`, `cas_workspace`, Task/Action/Approval providers |
| Implementation Status | `Gap Identified` |
| UI Validation Status | `Design Approved` |
| Related Decisions | `DEC-016-UIR10-CONSOLIDATED`, `DEC-UIR11-GUARD-ATTENDANCE-001` |
| Related Observations | `OBS-UIR10-GUARD-001` |
| Related Registers | `REG-UIR10`, `REG-UIR11` |

## 1. Route and Goal

Route: `/workspace/guard/attendance`.

هدف صفحه ثبت سریع، کم‌خطا و گروهی ورود/خروج و ثبت مغایرت «تردد اعلام‌نشده» توسط نگهبان است. این صفحه گزارش مدیریتی کامل نیست.

## 2. Backend Ownership

ثبت عادی MUST روی مدل‌ها و عملیات موجود زیر ساخته شود:

- `cas.guard.batch`؛
- `cas.guard.batch.line`؛
- `cas.attendance.event`؛
- `cas.attendance.site`؛
- `action_confirm`.

Workspace فقط orchestration و presentation را مالک است و مدل Attendance موازی ایجاد نمی‌کند. جریان مغایرت باید با Attendance و Providerهای Task/Action/Approval یکپارچه شود.

## 3. Layout

- ساعت زنده، تاریخ جاری و محل/درب فعال در بالای صفحه؛
- حالت‌های مستقل «ثبت ورود»، «ثبت خروج» و «تردد اعلام‌نشده»؛
- جست‌وجوی نام، کد پرسنلی و سمت؛
- فیلتر واحد، شیفت و وضعیت داخل/خارج؛
- انتخاب تکی و چندگانه؛
- انتخاب همه نتایج فیلترشده؛
- Chipهای افراد انتخاب‌شده؛
- کارت انتخاب‌شده با پس‌زمینه متمایز، Border ضخیم، سایه/حلقه و نشان متنی «انتخاب شد»؛
- CTA متناسب با حالت؛
- آخرین ثبت‌ها در پایین صفحه.

## 4. Selection Rules

انتخاب چندگانه تجمعی است. حذف Chip باید کارت، Checkbox، شمارنده و CTA را هم‌زمان اصلاح کند. شناسه‌ها در Client normalized می‌شوند. عملیات بدون فرد غیرفعال است.

افراد دارای وضعیت «داخل مجموعه» و «خارج مجموعه» نباید در یک Batch هم‌زمان انتخاب شوند. اولین فرد انتخاب‌شده وضعیت مجاز Batch را تعیین می‌کند. در انتخاب همه نتایج ترکیبی، ابتدا باید فیلتر وضعیت مشخص شود.

برای هر فرد یک `cas.guard.batch.line` مستقل ایجاد می‌شود و همه Lineها به یک Batch مشترک تعلق دارند.

## 5. Normal Entry/Exit

- زمان فعلی پیش‌فرض است؛
- نگهبان مجاز می‌تواند ساعت و دقیقه را تغییر دهد؛
- تغییر زمان فقط با دلیل اجباری ممکن است؛
- ورود مجدد فردی که داخل ثبت شده ممنوع است؛
- خروج مجدد فردی که خارج ثبت شده ممنوع است؛
- کنترل Conflict هم در UI و هم در Backend الزامی است؛
- در ثبت گروهی، افراد متعارض باید از افراد قابل ثبت تفکیک شوند.

در تغییر دستی MUST موارد زیر نگهداری شوند:

- زمان واقعی ثبت سیستم؛
- زمان رخداد اعلام‌شده؛
- ثبت‌کننده؛
- دلیل اصلاح؛
- اختلاف زمانی؛
- Batch و Line مرتبط.

## 6. Correction of Existing Record

رخداد رسمی مستقیماً بازنویسی یا حذف عادی نمی‌شود. اصلاح فقط از مسیر ممیزی‌پذیر `void/replacement/reopen` یا معادل مصوب آن مجاز است.

Audit اصلاح حداقل شامل زمان قبلی، زمان جدید، دلیل، اصلاح‌کننده، زمان اصلاح، نوع رخداد و شناسه رکورد اصلی است.

## 7. Unreported Attendance

این حالت مغایرت ایجاد می‌کند و نباید مستقیماً رخداد رسمی Attendance بسازد.

نگهبان فقط موارد زیر را مشخص می‌کند:

- یک یا چند فرد؛
- نوع مشترک رکورد گمشده: «ورود ثبت نشده» یا «خروج ثبت نشده»؛
- تاریخ مشترک مربوط به مغایرت.

نگهبان در این مرحله ساعت، توضیح، دلیل یا منبع تشخیص وارد نمی‌کند.

### Date Picker

فیلد تاریخ دارای دکمه/آیکن تقویم و Modal تقویم جلالی است. انتخاب تاریخ صرفاً با ورودی متنی طراحی نهایی محسوب نمی‌شود. تاریخ انتخابی برای همه افراد Batch مشترک است.

### Follow-up Flow

1. نگهبان مغایرت را ثبت می‌کند؛
2. برای هر فرد Task/Action شخصی ایجاد می‌شود؛
3. فرد نوع ثبت‌شده، تاریخ، وضعیت درخواست و مهلت پیگیری را در پنل خود می‌بیند؛
4. فرد ساعت پیشنهادی و توضیح خود را ثبت می‌کند؛
5. سرپرست درخواست را تأیید یا رد می‌کند؛
6. فقط پس از تأیید سرپرست رکورد رسمی Attendance ایجاد می‌شود.

## 8. Confirmation and Audit

تأیید نهایی ثبت عادی Batch همان `action_confirm` را فراخوانی می‌کند. رخداد رسمی append-only است.

Audit حداقل actor، principal، site، batch، lines، event kind، occurred_at، recorded_at، manual_time، reason، target، approval و outcome را ثبت می‌کند.

## 9. Recent Log

آخرین ثبت‌ها نام، واحد، ورود/خروج، زمان رخداد، زمان واقعی ثبت، محل، ثبت‌کننده، منبع، دستی/خودکار و Batch را نشان می‌دهند. مغایرت‌های اعلام‌نشده باید از رخدادهای رسمی قابل تفکیک باشند.

## 10. Security

نگهبان فقط Scope مجاز شرکت/سایت/کارمند را می‌بیند. UI hiding جای ACL، Record Rule و Method Check را نمی‌گیرد. Cross-company، direct RPC و ID tampering باید رد شوند.

ایجاد رخداد رسمی از مسیر مغایرت فقط پس از Approval معتبر و server-side validation مجاز است.

## 11. Acceptance Criteria

- انتخاب تکی و چندگانه عملیاتی باشد؛
- حذف Chip تمام stateها را هماهنگ اصلاح کند؛
- انتخاب کارت روی نمایشگر کم‌کیفیت نیز واضح باشد؛
- افراد داخل و خارج در یک Batch قابل انتخاب نباشند؛
- ثبت بدون فرد ممکن نباشد؛
- ورود/خروج تکراری در UI و Backend رد شود؛
- زمان فعلی پیش‌فرض و زمان دستی با دلیل مجاز باشد؛
- اصلاح رکورد قبلی Audit کامل داشته باشد؛
- حالت اعلام‌نشده نوع و تاریخ مشترک داشته باشد؛
- تاریخ با Modal تقویم جلالی انتخاب شود؛
- نگهبان در حالت اعلام‌نشده ساعت یا توضیح وارد نکند؛
- برای هر فرد Task مستقل ایجاد شود؛
- رکورد رسمی فقط پس از تأیید سرپرست ساخته شود؛
- هر فرد Line مستقل و Batch مشترک داشته باشد؛
- رخداد تأییدشده قابل ویرایش/حذف عادی نباشد؛
- صفحه روی مدل‌ها و Actionهای موجود کار کند؛
- Desktop، Tablet، ACL، Record Rule، direct RPC و ID tampering بازآزمایی شوند.
