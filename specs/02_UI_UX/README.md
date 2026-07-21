# 02 — UI & UX

این بخش Page Specificationهای `CAS UI Workspace v8 — Through Iteration 12` را نگهداری می‌کند.

## قاعده مرجعیت

- [Workspace Home نسخه ۸](Employee/Workspace_V8.md) مرجع فعال میزکار است.
- [Workspace Shell نسخه ۸](Shared/Workspace_Shell_V8.md) مرجع فعال پوسته مشترک است.
- فایل‌های قدیمی `Workspace.md` و `Workspace_Shell.md` Historical Reference نسخه ۷ هستند.
- سایر صفحه‌های Employee که صریحاً v8 را ثبت کرده‌اند، در کنار Baseline و Decisionهای نسخه ۸ خوانده می‌شوند.

## صفحات کاربر عادی

- [میزکار نسخه ۸](Employee/Workspace_V8.md)
- [کارهای شخصی](Employee/Personal_Tasks.md)
- [تقویم](Employee/Calendar.md)
- [گفت‌وگوها](Employee/Conversations.md)
- [Command Palette و جست‌وجوی سازمانی](Employee/Global_Search.md)
- [مرکز اعلان‌ها](Employee/Notifications_Center.md)
- [Recent History داخل Command Palette](Employee/Recent_History.md)
- [گزارش کار پویا و شیفت‌محور](Employee/Dynamic_Work_Report.md)

## صفحات ادمین

- [مرکز مدیریت داشبورد](Admin/Dashboard_Management_Center.md)

## مشترک همه نقش‌ها

- [پوسته مشترک Workspace v8](Shared/Workspace_Shell_V8.md)

## دامنه قطعی نسخه ۸

- Workspace عملیاتی و Action-First
- Widgetهای Provider-based و قابل جابه‌جایی
- Dashboard Governance برای ادمین
- Personal Task با مالک مستقل
- Calendar با Attendee Selector مقیاس‌پذیر
- تفکیک Invitation، Self Task و Assigned Action
- Conversation مبتنی بر Odoo Mail/Discuss/Bus
- Command Palette مشترک Search و Recent History
- Native Scroll برای Routeهای عادی
- Scroll مستقل Conversation List و Message Body
- Overlay و Focus هماهنگ با Odoo UI Services
- Notification Center مستقل با Reuse زیرساخت Odoo
- Work Report براساس Shift Occurrence
- یک گزارش ترکیبی با Sectionهای چند Assignment
- Applicability قابل Required، Optional یا Disabled
- دسترسی تفویض‌شده مستقل از زیردستی

## الزامات مشترک هر صفحه

هر Page Specification باید این موارد را تعیین کند:

- هدف و نقش‌ها
- Route و Entry Point
- Capability و Permission Expectations
- Stateهای Loading، Empty، Forbidden، Unavailable، Error و Ready
- Primary و Secondary Actions
- Keyboard، Focus، RTL و Responsive Behavior
- Provider و Domain Owner
- Acceptance Criteria
- Decisionها و Architecture Contractهای مرتبط

## وضعیت

تصمیم‌های محصولی نسخه ۸ تجمیع شده‌اند. آمادگی اجرای هر صفحه تابع آماده‌شدن Module Specification، API، Security، Migration و Test Strategy ماژول‌های مالک است.