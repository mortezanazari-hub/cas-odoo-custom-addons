# Security Specification — `cas_work_report`

| مشخصه | مقدار |
|---|---|
| وضعیت | `Consolidated` |
| نسخه | `v8 through iteration 12` |
| Decision | `DEC-020` |

## اصل امنیت

دسترسی گزارش کار از ترکیب ACL، Record Rule، Domain Method Check، Organization Scope و Work Report Access Grant حاصل می‌شود. هیچ‌کدام به‌تنهایی کافی نیستند.

## مسیرهای دسترسی معتبر

1. مالک گزارش
2. رابطه سازمانی مجاز
3. Reviewer یا Approver
4. Access Grant تفویض‌شده
5. نقش کنترل عملکرد یا ممیزی با Scope صریح
6. Administrator محدود و Audit‌شونده

## Capabilityهای مفهومی

- `work_report.use`
- `work_report.view_own`
- `work_report.edit_own_draft`
- `work_report.submit_own`
- `work_report.view_scope`
- `work_report.comment`
- `work_report.review`
- `work_report.request_correction`
- `work_report.return`
- `work_report.approve`
- `work_report.export`
- `work_report.audit`
- `work_report.manage_profiles`
- `work_report.manage_access_grants`

نام فنی نهایی در Security Implementation تثبیت می‌شود.

## سطح رکورد

Record Rule باید حداقل این متغیرها را لحاظ کند:

- company
- owner
- shift period
- organization scope
- reviewer assignment
- access grant validity
- report/profile/assignment filters
- active state

## سطح Section

دسترسی Report Header الزاماً دسترسی تمام Sectionها نیست.

برای هر Section باید بررسی شود:

- Assignment Scope
- Confidentiality Level
- Reviewer Scope
- Access Grant Section Filter
- Operation Requested

Backend باید Section غیرمجاز را از Read، Search، Export و Aggregate حذف کند.

## Access Grant

### Scope Type

- all company reports
- organization units
- jobs/roles
- persons
- report profiles
- assignment types
- explicit assignments
- explicit reports
- sections
- date/shift range

### Operation Set

- view
- comment
- review
- request correction
- return
- approve
- export
- audit

### Lifecycle

- draft، در صورت نیاز Approval
- active
- expired
- revoked
- rejected

### الزامات

- start/end زمان‌دار
- grantor و reason اجباری
- امکان revoke فوری
- عدم تمدید ضمنی
- Audit کامل
- جلوگیری از self-escalation
- Approval جدا برای Scopeهای حساس، در صورت Policy

## Organization Scope

`cas_organization_core` فقط Scope پایه را Resolve می‌کند. `cas_work_report` تصمیم نهایی دسترسی Report و Operation را می‌گیرد.

مثال:

- Manager ممکن است Report را ببیند ولی Approve نکند.
- Performance Controller ممکن است همه KPIها را ببیند ولی متن محرمانه Section را نبیند.
- Auditor ممکن است Read-only و Export محدود داشته باشد.

## Form Submission و Answer

Reviewer مجاز Report باید دسترسی لازم به Form Submission و Answerهای همان Section را از طریق Rule/Service امن دریافت کند. Rule مالک/Creator ساده برای این نیاز کافی نیست.

Access به Form داده باید از رابطه معتبر Report Section حاصل شود و به سایر Submissionها گسترش پیدا نکند.

## Evidence

- دسترسی Attachment از مجوز Report/Section مشتق می‌شود.
- URL یا Attachment ID به‌تنهایی مجوز ایجاد نمی‌کند.
- Preview، Download و Export می‌توانند Permission جدا داشته باشند.
- Evidence حساس باید Classification داشته باشد.

## Export

Export باید:

- فقط Fieldها و Sectionهای مجاز را شامل شود.
- Scope و زمان Access Grant را دوباره بررسی کند.
- تعداد و معیار Export را Audit کند.
- از Background Job امن استفاده کند، در صورت حجم بالا.
- لینک خروجی منقضی و User-bound باشد، در صورت ذخیره فایل خروجی.

## Search و Aggregate

- Count نباید وجود Report غیرمجاز را افشا کند.
- Search Result Label نباید اطلاعات Section ممنوع را نشان دهد.
- Dashboard KPI فقط از Projection مجاز استفاده کند.
- `sudo` عمومی برای Aggregate ممنوع است.

## Multi-company

- Company Context باید در Backend Validate شود.
- Access Grant میان شرکت‌ها فقط با Scope صریح و گروه سطح بالا ممکن است.
- Switching Company نباید دسترسی Grant خارج از Context را خودکار فعال کند.

## Method Checkهای حساس

Method Check صریح برای:

- submit
- return
- approve
- lock/unlock
- export
- create/revoke grant
- profile change
- migration/rebuild projection

## Audit Eventها

- Report Viewed در Scopeهای حساس، در صورت Policy
- Report Submitted
- Section Returned
- Approval Decision
- Export Requested/Completed
- Access Grant Created/Activated/Expired/Revoked
- Unauthorized Attempt
- Profile یا Reviewer Resolution Change

## تست‌های امنیتی

- Direct RPC با ID حدس‌زده
- Access به Section ممنوع
- Expired Grant
- Revoked Grant در Session فعال
- Cross-company
- Export leakage
- Search count leakage
- Attachment URL leakage
- Reviewer به Submission مرتبط و نامرتبط
- Self-grant یا privilege escalation
- تغییر Clock/Timezone در Grant Boundary

## رفتار Fail-closed

در نبود Resolver، Provider، Rule یا Configuration معتبر:

- دسترسی اعطا نمی‌شود.
- UI Unavailable/Forbidden مناسب نشان می‌دهد.
- خطا Audit و قابل تشخیص است.
- سیستم با Scope گسترده Fallback نمی‌کند.