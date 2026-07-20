# معماری جامع گزارش کار مبتنی بر Form Engine

| مشخصه | مقدار |
|---|---|
| وضعیت | `Needs Review` |
| تصمیم مرجع | `../04_Decisions/DEC-017-Work-Report-Domain-Uses-Form-Engine.md` |
| دامنه | `cas_work_report`, Form Engine, Workspace, Workflow, HR, Shift, Attendance |

## ۱. هدف
ایجاد یک دامنه واحد برای گزارش کار که Lifecycle، کنترل، تأیید و گزارش‌گیری را یکپارچه نگه دارد، در حالی‌که فرم ثبت هر واحد، شغل و Assignment بتواند ساختار تخصصی و نسخه‌دار داشته باشد.

## ۲. مرز مالکیت

### `cas_form_core`
- Form Definition و Form Version
- Section، Field، Rule، Validation و Conditional Logic
- Submission و Answer Storage
- Schema Snapshot
- Runtime Contract
- Attachment Reference

### `cas_work_report`
- هویت گزارش روزانه/شیفتی
- Profile Resolution
- Frequency و Deadline
- Draft/Submitted/Returned/Approved/Locked
- کنترل تکراری‌بودن گزارش
- ارتباط Employee، Assignment، Shift و Date
- Attendance Reconciliation
- Reviewer و Approval Reference
- Missing/Overdue/Incomplete Status
- Projectionهای گزارش‌گیری

### `cas_workspace`
- Navigation براساس Capability
- Routeهای «گزارش امروز»، «گزارش‌های من» و «گزارش‌های حوزه»
- Dynamic Report Shell
- Renderer Registry
- نمایش Context، Status و Profile Explanation

### `cas_workflow_core` / `cas_approval_core`
- مسیر بررسی و تأیید
- بازگشت برای اصلاح
- Delegation و Escalation
- ثبت Decision و Audit

### Providerهای زمینه‌ای
- HR/Employee: هویت و انتساب مؤثر
- Organization: واحد، شغل، رابطه مدیریتی و Delegation
- Shift: شیفت مؤثر
- Attendance: حضور و مغایرت
- Document Core: فایل و شاهد
- Notification: یادآوری، تأخیر، بازگشت و تأیید

## ۳. مدل مفهومی

### `cas.work.report`
```text
employee_id
assignment_id
company_id
report_date
period_start
period_end
shift_id
profile_id
form_definition_id
form_version_id
submission_id
schema_snapshot_hash
renderer_key
state
reviewer_id
approval_instance_id
deadline_at
submitted_at
reviewed_at
locked_at
attendance_status
completeness_status
is_late
```

### `cas.work.report.profile`
```text
name
company_id
department_id
job_id
position_id
assignment_type_id
role_key
shift_type_id
frequency
form_definition_id
renderer_key
approval_flow_id
deadline_policy_id
attendance_policy_id
evidence_policy_id
priority
effective_from
effective_to
active
```

### `cas.work.report.projection`
برای فیلدهای تحلیلی و قابل گزارش‌گیری:
```text
report_id
metric_key
value_number
value_text
value_date
source_field_key
source_form_version_id
```

## ۴. الگوریتم Profile Resolver
1. دریافت Employee و Assignmentهای مؤثر در تاریخ گزارش.
2. محدودسازی براساس Company و Active Date Range.
3. Match روی Job، Position، Department، Assignment Type، Role و Shift Type.
4. محاسبه Specificity Score.
5. اعمال Priority.
6. تشخیص تعارض.
7. انتخاب Profile یا نمایش خطای کنترل‌شده.
8. ثبت دلیل انتخاب برای Audit و UI.

### ترتیب پیشنهادی Specificity
```text
assignment exact > position exact > job exact > department exact > role > company default
```

### تعارض
اگر دو Profile امتیاز و Priority برابر داشته باشند، سیستم نباید تصادفی انتخاب کند. گزارش در وضعیت `configuration_error` قرار می‌گیرد و مدیر سامانه مطلع می‌شود.

## ۵. چندوظیفه‌ای
سه Policy پشتیبانی می‌شود:
- `single_primary_profile`: فقط Profile انتساب اصلی
- `multiple_reports`: یک گزارش برای هر Assignment
- `composite_sections`: یک گزارش با Sectionهای ترکیبی

پیشنهاد پایه CAS: `composite_sections` در صورت یکسان‌بودن Reviewer و محرمانگی؛ در غیر این صورت `multiple_reports`.

## ۶. قرارداد ایجاد گزارش
```text
open_daily_report(employee, date)
  → resolve assignments
  → resolve profile(s)
  → resolve form version
  → create/get report draft
  → create/get submission
  → hydrate context fields
  → return render contract
```

## ۷. Render Contract پیشنهادی
```json
{
  "report": {"id": 501, "state": "draft", "deadline_at": "..."},
  "profile": {"id": 20, "code": "WRP-IT-01", "resolution_reason": "job_exact"},
  "context": {"employee": {}, "assignment": {}, "shift": {}, "attendance": {}},
  "form": {"definition_id": 8, "version_id": 31, "schema": {}},
  "renderer": {"key": "work_report_dynamic", "version": 1},
  "permissions": {"edit": true, "submit": true, "delegate": false},
  "review": {"reviewer": {}, "flow": {}, "status": null}
}
```

## ۸. Snapshot و تاریخچه
- هر گزارش به Form Version مشخص متصل است.
- Schema Snapshot Hash ذخیره می‌شود.
- Label و Optionهای مؤثر در Snapshot نگهداری می‌شوند.
- Renderer Version قابل ردیابی است.
- گزارش تاریخی با نسخه جدید فرم Re-render یا Revalidate نمی‌شود.

## ۹. Validation
دو لایه مستقل:

### Form Validation
Required، Regex، Range، Conditional، Formula و Field Rules.

### Domain Validation
Deadline، Duplicate Report، Assignment Validity، Allowed Reporter، Attendance Policy، Approval Preconditions و Lock State.

## ۱۰. امنیت
- Queryهای User-facing بدون `sudo()`
- ACL و Record Rule روی Report و Submission
- Method Check برای Submit، Return، Approve، Reopen و Lock
- Employee فقط گزارش خود را می‌بیند مگر Capability صریح
- Reviewer فقط Scope مؤثر خود را می‌بیند
- Profile Resolver داده خارج از Company را نشت نمی‌دهد
- Field-level Security فرم در Runtime رعایت می‌شود
- Tampering روی employee_id، assignment_id، profile_id و form_version_id در Backend دوباره Resolve می‌شود

## ۱۱. Navigation
منو براساس Capability و Profile مؤثر ساخته می‌شود:
- `report.daily.create` → گزارش امروز
- `report.self.read` → گزارش‌های من
- `report.team.review` → بررسی گزارش‌های حوزه
- `report.profile.manage` → پروفایل‌های گزارش کار

برای هر Form Definition منوی XML مستقل ساخته نمی‌شود.

## ۱۲. UI
پوسته مشترک شامل:
- عنوان فرم و کد Profile
- توضیح دلیل انتخاب فرم
- Context فقط‌خواندنی
- Form Runtime پویا
- Status و Deadline
- مسیر تأیید
- Snapshot Version
- Evidence Upload

Renderer اختصاصی فقط Presentation را تغییر می‌دهد و نباید مدل داده موازی بسازد.

## ۱۳. Reporting و Analytics
فیلدهای مهم Form به Projectionهای تایپ‌شده نگاشت می‌شوند. گزارش‌گیری مستقیم روی JSON خام یا EAV بدون Index ممنوع است. هر Profile مشخص می‌کند کدام Field Keyها برای KPI و گزارش مدیریتی استخراج شوند.

## ۱۴. Migration
1. شناسایی فرم ثابت فعلی.
2. ساخت Form Definition و Version معادل.
3. ساخت Profile پیش‌فرض عملیات.
4. نگاشت رکوردهای قبلی به Submission و Snapshot.
5. حفظ شناسه و Audit.
6. اجرای Dual Read فقط در دوره انتقال.
7. حذف Renderer ثابت پس از تطبیق کامل.

## ۱۵. Performance
- Cache نتیجه Profile Resolver با Invalidation روی تغییر Assignment/Profile
- Lazy Load بخش‌های سنگین فرم
- Projection برای Analytics
- Batch generation برای Missing Reportها
- عدم بارگذاری Form Definitionهای نامرتبط

## ۱۶. Observability
- profile_resolution_success/conflict/error
- report_created/submitted/returned/approved/locked
- attendance_mismatch
- deadline_missed
- form_runtime_error
- projection_failure
- unauthorized_report_operation

## ۱۷. تست حداقلی
- Unit: Resolver، Specificity، Conflict، Deadline و Snapshot
- Security: ID Tampering، Multi-company، Reviewer Scope
- Integration: Report + Submission + Workflow + Attendance
- Migration: رکوردهای فرم ثابت
- UI: نقش‌ها، چندوظیفه‌ای، فرم تخصصی و Renderer fallback
- Load: تولید و مرور گزارش برای سازمان بزرگ

## ۱۸. موارد خارج از دامنه نسخه اول
- طراحی KPI Engine داخل Work Report
- جایگزینی Audit Log
- ساخت ماژول جدا برای هر فرم
- ویرایش Odoo Core
- اجرای محاسبات دلخواه ناامن در Browser

## ۱۹. معیار پذیرش معماری
- فرم نگهبان، IT و عملیات بدون تغییر کد دامنه قابل تعویض باشند.
- Report Lifecycle مستقل از Schema فرم باقی بماند.
- گزارش تاریخی با تغییر Form Version تغییر نکند.
- Profile اشتباه با تغییر Client Payload قابل تحمیل نباشد.
- مدیر بتواند گزارش‌های چند فرم را در نمای واحد تجمیع کند.
