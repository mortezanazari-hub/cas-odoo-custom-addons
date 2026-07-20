# ارزیابی اثر معماری پویا بر `cas_work_report`

| مشخصه | مقدار |
|---|---|
| وضعیت | `Needs Review` |
| نسخه مبنا | Workspace v7 |
| نسخه هدف | Workspace v8 Iteration 12 |
| تصمیم مرجع | `../../04_Decisions/DEC-017-Work-Report-Domain-Uses-Form-Engine.md` |
| معماری مرجع | `../../05_Architecture/Work_Report_Form_Engine_Architecture.md` |

## جمع‌بندی
`cas_work_report` حذف نمی‌شود. این ماژول از فرم ثابت روزانه به دامنه تخصصی مدیریت گزارش کار تبدیل می‌شود و برای Schema، Version، Validation و Submission از Form Engine استفاده می‌کند.

## مسئولیت‌های قطعی ماژول
- Daily/Shift Report Identity
- Employee، Assignment، Date و Shift Context
- Profile Resolution
- Deadline و Missing/Overdue State
- Draft، Submitted، Returned، Approved و Locked
- Attendance Reconciliation
- Reviewer/Approval Reference
- Duplicate Prevention
- Snapshot Reference
- Reporting Projection
- Team Review و Management Aggregation

## مسئولیت‌هایی که منتقل می‌شوند
### به Form Engine
- Section و Field Definition
- Validation و Conditional Logic
- Form Version
- Submission و Answer Storage
- Runtime Schema

### به Workflow/Approval
- Decision، Return، Escalation و Delegation

### به Workspace
- Dynamic Page Shell
- Navigation و Renderer
- Profile Explanation

## مدل‌های موردنیاز
- `cas.work.report`
- `cas.work.report.profile`
- `cas.work.report.projection`
- Deadline/Attendance/Evidence Policy در صورت نیاز

## Profile Resolution
Profile براساس Company، Assignment، Position، Job، Department، Role، Shift Type، Effective Date و Priority انتخاب می‌شود. انتخاب Client معتبر نیست و Backend باید Resolve را تکرار کند.

## چندوظیفه‌ای
- Profile اصلی
- چند گزارش مستقل
- فرم ترکیبی با Sectionهای پویا

Policy پیشنهادی: فرم ترکیبی فقط در صورت یکسان‌بودن Reviewer و محرمانگی.

## APIهای پیشنهادی
- `get_or_create_daily_report(employee_id, report_date)`
- `resolve_work_report_profile(employee_id, report_date, shift_id)`
- `get_work_report_render_contract(report_id)`
- `submit_work_report(report_id, submission_revision)`
- `return_work_report(report_id, reason)`
- `approve_work_report(report_id, decision)`
- `reopen_work_report(report_id, reason)`
- `get_team_work_reports(filters)`

نام نهایی APIها هنوز تصویب نشده است.

## امنیت
- بدون `sudo()` برای مسیرهای کاربرمحور
- کنترل مجدد employee، assignment، profile و form version
- Record Rule مستقل Report و Submission
- Reviewer Scope مؤثر و تاریخ‌دار
- Multi-company
- Audit برای Submit، Return، Approve، Reopen و Lock

## Migration
فرم ثابت موجود باید به Form Definition نسخه‌دار و Profile پیش‌فرض تبدیل شود. رکوردهای قبلی باید شناسه، تاریخچه و Snapshot خود را حفظ کنند.

## تست‌ها
- Resolver و Conflict
- Assignment هم‌زمان
- فرم‌های تخصصی نگهبانی، IT و عملیات
- Snapshot تاریخی
- Attendance mismatch
- Reviewer delegation
- Security tampering
- Migration فرم ثابت
- Analytics Projection

## وضعیت
این سند Impact Assessment است و هنوز `Implementation Ready` نیست. مدل نهایی Profile، قرارداد Submission/Snapshot، Reporting Projection، Migration و Security Specification باید تصویب شوند.
