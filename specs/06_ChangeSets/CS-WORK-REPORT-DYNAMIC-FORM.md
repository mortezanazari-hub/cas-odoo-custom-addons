# Change Set — گزارش کار پویا مبتنی بر فرم‌ساز

| مشخصه | مقدار |
|---|---|
| شناسه | `CS-WORK-REPORT-DYNAMIC-FORM` |
| نسخه | Workspace v8 Iteration 12 |
| وضعیت | `Collected` |
| مجوز Production | ندارد تا Specification نهایی تصویب شود |

## تغییر محصولی
- فرم ثابت عمومی گزارش روزانه کنار گذاشته می‌شود.
- `cas_work_report` حفظ و به دامنه Lifecycle گزارش تبدیل می‌شود.
- Form Engine ساختار تخصصی هر گزارش را ارائه می‌کند.
- فرم مناسب براساس Profile مؤثر کاربر انتخاب می‌شود.

## تغییر UI
- Banner پروفایل و نسخه فرم
- Context سازمانی فقط‌خواندنی
- Sectionهای تخصصی براساس شغل/واحد
- نمایش دلیل انتخاب فرم
- نمایش Deadline، Reviewer و Snapshot
- نمونه‌های نگهبانی، IT، دبیرخانه، عملیات و مدیریت

## اثر ماژولی
- `cas_work_report`: Profile، Lifecycle، Deadline، Review، Projection
- `cas_form_core`: Definition، Version، Validation، Submission
- `cas_workspace`: Dynamic Shell، Navigation، Renderer
- Workflow/Approval: Decision و Escalation
- HR/Organization/Shift/Attendance: Context Providers
- Document Core: Evidence
- Notification: Reminder و State Change

## Migration
- تبدیل فرم ثابت به Form Definition نسخه‌دار
- ساخت Profile پیش‌فرض
- نگاشت رکوردهای قبلی به Submission/Snapshot
- حذف Renderer ثابت پس از Dual-read کنترل‌شده

## ریسک‌ها
- تعارض Profile
- Assignmentهای هم‌زمان
- Snapshot ناسازگار
- گزارش‌گیری روی داده پویا
- Tampering روی Context و Profile

## تست
- Profile Resolver
- چندوظیفه‌ای
- فرم‌های تخصصی
- Snapshot تاریخی
- Multi-company و Permission
- Attendance mismatch
- Migration
- Reporting Projection

## مراجع
- `../04_Decisions/DEC-017-Work-Report-Domain-Uses-Form-Engine.md`
- `../05_Architecture/Work_Report_Form_Engine_Architecture.md`
- `../02_UI_UX/Employee/Dynamic_Work_Report.md`
- `../03_Modules/cas_work_report/V7_Impact_Assessment.md`
