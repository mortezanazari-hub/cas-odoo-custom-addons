# ایستگاه سریع ثبت تردد نگهبانی

| مشخصه | مقدار |
|---|---|
| Document ID | `PAGE-GUARD-ATTENDANCE-STATION` |
| Document Type | Page Specification |
| Status | `Active` |
| Document Version | `1.0` |
| Created At | `2026-07-22` |
| Updated At | `2026-07-22` |
| Owner | Attendance Operations |
| Source UI Review Cycle | `CAS UI Review Cycle 10` |
| Source Iteration | `11–12` |
| Domain Owner | Attendance Operations |
| Affected Modules | `cas_attendance_operations`, `cas_attendance_core`, `cas_workspace` |
| Implementation Status | `Gap Identified` |
| UI Validation Status | `Pending Revalidation` |
| Related Decisions | `DEC-016-UIR10-CONSOLIDATED` |
| Related Observations | `OBS-UIR10-GUARD-001` |
| Related Change Sets | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` |

## 1. Route and Goal

Route: `/workspace/guard/attendance`.

هدف صفحه ثبت سریع، کم‌خطا و گروهی رخداد ورود/خروج توسط نگهبان است. صفحه گزارش مدیریتی یا ویرایش مستقیم سابقه رسمی نیست.

## 2. Backend Ownership

رابط MUST روی مدل‌های موجود زیر ساخته شود:

- `cas.guard.batch`؛
- `cas.guard.batch.line`؛
- `cas.attendance.event`؛
- `cas.attendance.site`؛
- `action_confirm`.

Workspace فقط orchestration و presentation را مالک است و مدل Attendance موازی ایجاد نمی‌کند.

## 3. Layout

- ساعت زنده، تاریخ و محل/درب فعال در بالای صفحه؛
- انتخاب واضح نوع عملیات: ورود یا خروج؛
- جست‌وجوی نام، کد پرسنلی و سمت؛
- فیلتر واحد، شیفت و وضعیت داخل/خارج؛
- انتخاب تکی و چندگانه؛
- انتخاب همه نتایج فیلترشده؛
- Chipهای افراد انتخاب‌شده؛
- کنترل زمان رخداد؛
- CTA واضح «ثبت تردد N نفر»؛
- آخرین ثبت‌ها در پایین صفحه.

## 4. Selection Rules

انتخاب چندگانه تجمعی است. حذف Chip باید کارت، Checkbox، شمارنده و CTA را هم‌زمان اصلاح کند. شناسه‌ها در Client normalized می‌شوند. ثبت بدون فرد غیرفعال است.

برای هر فرد یک `cas.guard.batch.line` مستقل ایجاد می‌شود و همه Lineها به یک Batch مشترک تعلق دارند. Batch نباید به یک رخداد مبهم گروهی تبدیل شود.

## 5. Time Rules

`default_occurred_at` به‌صورت پیش‌فرض زمان فعلی است. نگهبان مجاز می‌تواند ساعت و دقیقه را تغییر دهد.

در تغییر دستی MUST موارد زیر نگهداری شوند:

- زمان واقعی ثبت سیستم؛
- زمان رخداد اعلام‌شده؛
- ثبت‌کننده؛
- دلیل اصلاح؛
- اختلاف زمانی؛
- Batch و Line مرتبط.

عبور از آستانه اختلاف قابل تنظیم باید هشدار یا approval requirement ایجاد کند. تاریخ گذشته یا آینده خارج از محدوده مجاز باید رد شود یا نیازمند Capability بالاتر باشد.

## 6. Person Status and Conflicts

هر نتیجه باید وضعیت فعلی، آخرین ورود و آخرین خروج را نشان دهد. ورود مجدد فردی که داخل ثبت شده یا خروج فردی که خارج ثبت شده Conflict است. ادامه فقط با دلیل و مجوز مناسب ممکن است.

## 7. Confirmation and Audit

تأیید نهایی Batch همان `action_confirm` را فراخوانی می‌کند. پس از تأیید، رخداد رسمی append-only است. ویرایش/حذف عادی ممنوع و اصلاح فقط از مسیر void/replacement/reopen مجاز است.

Audit حداقل actor، site، batch، lines، event kind، occurred_at، recorded_at، manual_time، reason و outcome را ثبت می‌کند.

## 8. Recent Log

آخرین ثبت‌ها نام، واحد، ورود/خروج، زمان رخداد، زمان واقعی ثبت، محل، ثبت‌کننده، منبع، دستی/خودکار و Batch را نشان می‌دهند. این Log جای گزارش کامل Attendance را نمی‌گیرد.

## 9. Security

نگهبان فقط Scope مجاز شرکت/سایت/کارمند را می‌بیند. UI hiding جای ACL، Record Rule و Method Check را نمی‌گیرد. Cross-company و ID tampering باید رد شوند.

## 10. Acceptance Criteria

- انتخاب تکی و چندگانه عملیاتی باشد؛
- حذف Chip کار کند؛
- ثبت بدون فرد ممکن نباشد؛
- زمان فعلی پیش‌فرض و زمان دستی با دلیل مجاز باشد؛
- هر فرد Line مستقل و Batch مشترک داشته باشد؛
- Conflict ورود/خروج دیده و Audit شود؛
- رخداد تأییدشده قابل ویرایش/حذف عادی نباشد؛
- صفحه روی مدل‌ها و Action موجود کار کند.
