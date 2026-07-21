# سؤالات باز و موضوعات آینده

| مشخصه | مقدار |
|---|---|
| شناسه | `OPEN-CAS-V8` |
| وضعیت | `Consolidated` |
| نسخه | `v8 through iteration 12` |

## نتیجه تصمیم‌های محصولی

سؤال‌های محصولی اصلی Consolidation نسخه ۸ پاسخ داده شده‌اند:

- Iteration 12 جزو v8 است.
- v7 Historical است.
- Personal Task مالک مستقل دارد.
- Self Task و Assigned Action تفکیک شده‌اند.
- Odoo Notification Reuse می‌شود.
- Recent History ماژول مستقل ندارد.
- Provider Contract مشترک است.
- Organization Scope مالک مستقل دارد.
- Search Capability از Permission منابع جداست.
- Notification Center Route مستقل دارد.
- Overlay بر پایه Odoo UI Services هماهنگ می‌شود.
- Preference Resolution تعیین شده است.
- Dashboard Management Center لازم است.
- Work Report چند Assignment یک گزارش ترکیبی است.
- واحد گزارش Shift Occurrence است.
- File Infrastructure در v8 بازطراحی نمی‌شود.
- Activity Catalog مستقل است.
- Applicability گزارش در Profile یا شخص قابل Disabled است.
- Access Grant مستقل از زیردستی لازم است.

## سؤالات فنی غیرمسدودکننده Baseline

این موارد تصمیم محصولی v8 را تغییر نمی‌دهند و باید هنگام Module Specification نهایی شوند.

### Q-TECH-001 — نام نهایی ماژول قرارداد Workspace

نام فعلی پیشنهادی: `cas_workspace_contract`.

معیار تصمیم:

- عدم وابستگی به UI Runtime
- جلوگیری از Circular Dependency
- امکان استفاده Providerها بدون وابستگی مستقیم به `cas_workspace`

### Q-TECH-002 — API دقیق Providerها

باید Schema نهایی برای موارد زیر تعیین شود:

- Widget Provider
- Search Provider
- Action Provider
- History Resource Reference
- Dashboard Availability
- Deep Link Resolver

### Q-TECH-003 — ذخیره Recent History

گزینه‌های فنی:

- Preference Model اختصاصی Workspace
- مدل فنی Lightweight با Retention محدود

در هر دو حالت کپی داده کسب‌وکاری ممنوع است.

### Q-TECH-004 — Gap دقیق Notification در Odoo 19 Community

قبل از ایجاد Extension باید بررسی شود:

- Read/Unread موردنیاز CAS
- Aggregation چند منبع
- Severity
- Action Button
- Deep Link
- Snooze
- Company Policy

### Q-TECH-005 — نام و مدل Calendar Integration

باید تعیین شود آیا Extension در ماژول موجود Calendar قرار می‌گیرد یا Bridge مستقل CAS ایجاد می‌شود. مالکیت Event همچنان Calendar است.

### Q-TECH-006 — Policy دقیق Section Reviewer

محصول تعیین کرده گزارش ترکیبی است. Specification باید تعیین کند:

- چند Reviewer برای Section مجاز است؟
- Approval نهایی در سطح Report است یا Section؟
- در صورت Return یک Section، وضعیت سایر Sectionها چیست؟

### Q-TECH-007 — Formula و Projection گزارش

باید Fieldهای Reportable، Index Strategy و Projection Refresh مشخص شود تا گزارش‌گیری روی Answerهای پویا قابل اتکا باشد.

### Q-TECH-008 — Migration از گزارش ثابت به پویا

نیازمند Mapping، Dual Read، Validation و Rollback Plan است.

### Q-TECH-009 — Widget Resize و Hide/Show کاربر

در v8 فعال نیست. برای نسخه آینده باید Interaction و Governance جداگانه تصویب شود.

### Q-TECH-010 — File/Document Infrastructure Redesign

خارج از دامنه v8 و موضوع آینده:

- Versioning
- Retention
- Archive
- Advanced Permissions
- Digital Signature
- Nextcloud Integration
- Storage Policy

### Q-TECH-011 — Delegation Approval Authority

برای هر نوع Access Grant باید مشخص شود چه نقش یا گروهی حق ایجاد، تمدید، لغو و Audit آن را دارد.

### Q-TECH-012 — Data Retention

Retention برای Recent History، Notification Aggregation، Audit و Work Report Evidence باید در Security و Compliance Specification تعیین شود.

## قاعده برخورد با سؤال باز

- سؤال فنی نباید باعث تضعیف Baseline محصولی شود.
- تا زمان پاسخ، امن‌ترین رفتار با حداقل دسترسی انتخاب می‌شود.
- هر پاسخ نهایی باید در Decision یا Architecture Contract ثبت و از این فایل خارج شود.
- موضوع آینده نباید به‌صورت ضمنی وارد Scope نسخه ۸ شود.