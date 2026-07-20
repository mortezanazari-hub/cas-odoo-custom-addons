# DEC-017 — دامنه گزارش کار از هسته فرم‌ساز استفاده می‌کند

| مشخصه | مقدار |
|---|---|
| وضعیت | `Agreed` |
| نسخه | `CAS UI Workspace v8` |
| دامنه | Work Report / Form Engine / Workspace / Workflow |

## مسئله
فرم گزارش روزانه برای همه واحدها و مشاغل یکسان نیست. حذف کامل `cas_work_report` و تبدیل هر فرم به ماژول مستقل، منطق مشترک گزارش، مهلت، تأیید، مغایرت حضور، گزارش‌های ناقص و تجمیع مدیریتی را پراکنده می‌کند. نگه‌داشتن فرم ثابت نیز نیازهای تخصصی نگهبانی، تولید، IT، اداری و مدیریت را پوشش نمی‌دهد.

## تصمیم
`cas_work_report` حذف نمی‌شود. این ماژول مالک مفهوم و چرخه گزارش کار باقی می‌ماند، اما ساختار فیلدها و بخش‌های هر گزارش را از Form Engine دریافت می‌کند.

```text
cas_form_core       → Schema, Version, Validation, Submission
cas_work_report     → Report Lifecycle, Profile Resolution, Deadline, Review
cas_workspace       → Route, Navigation, Dynamic Page Renderer
cas_workflow_core   → Review/Approval Flow
HR/Shift/Attendance → Context Providers
```

## تصمیم‌های قطعی
1. برای هر فرم گزارش کار ماژول Odoo جدا ساخته نمی‌شود.
2. هر نوع گزارش به‌صورت Form Definition نسخه‌دار تعریف می‌شود.
3. `cas_work_report.profile` فرم مناسب را براساس شرکت، انتساب مؤثر، واحد، شغل، شیفت، نقش و تاریخ اعتبار Resolve می‌کند.
4. رکورد گزارش به Form Definition، Form Version، Submission و Snapshot پایدار متصل است.
5. تغییر فرم آینده، نمایش و تفسیر گزارش‌های تاریخی را تغییر نمی‌دهد.
6. اطلاعات هویتی، واحد، شغل، شیفت و حضور تا حد ممکن از Providerها خوانده و فقط‌خواندنی نمایش داده می‌شوند.
7. Workflow/Approval مالک تصمیم تأیید است؛ Form Engine مالک Lifecycle گزارش نیست.
8. `cas_workspace` داده گزارش یا Submission را مالک نمی‌شود.
9. منوی کاربر براساس Capability و Profile مؤثر ساخته می‌شود؛ نه با XML Menu جدا برای هر فرم.
10. Renderer اختصاصی مجاز است، ولی Schema و داده همچنان از Form Engine می‌آیند.

## پیامدهای مثبت
- فرم تخصصی برای هر شغل و واحد
- حفظ گزارش‌گیری و Lifecycle مشترک
- جلوگیری از انفجار تعداد ماژول‌ها
- پشتیبانی از چندوظیفه‌ای و Assignmentهای هم‌زمان
- Versioning و Snapshot تاریخی
- امکان صفحه اختصاصی بدون Core Edit

## ریسک‌ها
- پیچیدگی Profile Resolver
- نیاز به قرارداد روشن میان Report و Submission
- نیاز به Index/Projection برای گزارش‌گیری تحلیلی
- احتمال تعارض چند Profile هم‌زمان
- نیاز به Migration فرم ثابت موجود

## موارد ردشده
### حذف `cas_work_report`
رد شد؛ چون Form Engine نباید مالک Deadline، تأیید، عدم ارسال، مغایرت حضور و تجمیع مدیریتی شود.

### ساخت ماژول مستقل برای هر فرم
رد شد؛ چون منطق مشترک تکرار و نگهداری، Migration و امنیت پراکنده می‌شود.

## شرط Implementation Ready
- مدل نهایی Profile و Resolver
- قرارداد Snapshot و Submission
- Conflict Resolution برای چند Profile
- APIهای Context Provider
- Security، Migration، Reporting Projection و Test Strategy
