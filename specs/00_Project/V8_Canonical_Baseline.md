# خط مبنای رسمی CAS UI Workspace v8

| مشخصه | مقدار |
|---|---|
| شناسه | `BASELINE-CAS-WORKSPACE-V8` |
| نسخه محصول | `CAS UI Workspace v8 — Through Iteration 12` |
| وضعیت | `Agreed` |
| سطح مرجعیت | `Canonical` |
| دامنه | Product, UI/UX, Domain Ownership, Cross-Module Architecture |
| جایگزین | تمام برداشت‌های متعارض نسخه‌های ۴ و ۷ |

## ۱. هدف

این سند مرجع بالادستی و قطعی نسخه ۸ است. تمام Page Specificationها، Decision Recordها، Architecture Contractها و Module Specificationها باید با آن سازگار باشند.

کد یا ماژول‌های موجود معیار کاهش دامنه این سند نیستند. هر اختلاف میان وضع موجود و این Baseline به معنی نیاز به اصلاح ماژول‌ها، Migration یا بازطراحی است.

## ۲. اصول غیرقابل‌نقض

1. هیچ تغییری در Odoo Core مجاز نیست.
2. Odoo Community و سرویس‌های استاندارد آن تا حد امکان Reuse و Extend می‌شوند.
3. Workspace مالک داده کسب‌وکاری نیست.
4. UI مرجع امنیت نیست.
5. داده‌های هر Domain فقط توسط مالک همان Domain ایجاد و تغییر می‌کنند.
6. Search، Dashboard و Workspace فقط Orchestrator یا Consumer هستند.
7. فارسی، RTL، تقویم جلالی و دسترس‌پذیری باید از ابتدا در طراحی لحاظ شوند.
8. تاریخ واقعی در قالب استاندارد Odoo ذخیره می‌شود؛ Jalali لایه نمایش و ورود است.
9. هر قابلیت باید Loading، Empty، Forbidden، Unavailable، Error و Ready را پوشش دهد.
10. هیچ سند Historical نمی‌تواند بدون Decision صریح، تصمیم v8 را تغییر دهد.

## ۳. مالکیت Workspace

`cas_workspace` فقط مالک موارد زیر است:

- چیدمان و Layout رابط کاربری
- Preferenceهای ظاهری کاربر
- تنظیمات Sidebar و Theme
- ترتیب Widgetها
- تنظیمات Dashboard Admin
- وضعیت‌های موقت UI و Navigation
- Command Palette Shell و Orchestration
- Recent Resource Referenceهای فنی، بدون کپی داده کسب‌وکاری

Workspace مالک موارد زیر نیست:

- Personal Task
- Organizational Action
- Calendar Event
- Conversation و Message
- Notification کسب‌وکاری
- Work Report
- Activity Catalog
- Document و Attachment
- Employee، Assignment یا Organization Hierarchy
- Workflow و Approval

## ۴. نقشه مالکیت دامنه‌ها

| دامنه | مالک |
|---|---|
| Personal Task | `cas_personal_task` |
| Action سازمانی | `cas_action_hub` |
| Calendar Event و Invitation | Calendar/Event Integration |
| Organization Scope و Assignment مؤثر | `cas_organization_core` |
| Work Report Lifecycle | `cas_work_report` |
| فرم و پاسخ پویا | `cas_form_core` و ماژول‌های Form Engine |
| Workflow State | `cas_workflow_core` |
| Approval Decision | `cas_approval_core` |
| Activity Catalog | `cas_activity_catalog` |
| Conversation و Message | Odoo Mail/Discuss/Bus با Adapterهای CAS |
| Notification Delivery | Odoo Mail/Discuss/Bus |
| Notification Aggregation Gap | Extension محدود CAS، فقط پس از Gap Analysis |
| File Storage | Odoo Attachment و زیرساخت موجود Document |
| Dashboard Layout و Preferences | `cas_workspace` |

## ۵. Workspace Shell

Workspace Shell مشترک همه نقش‌هاست و شامل این اجزاست:

- Sidebar جمع‌شونده
- Topbar
- Route Outlet
- Command Palette
- Notification Entry
- User Menu
- Theme و Density Resolver
- Overlay Coordination
- Native Scroll Policy
- Provider Availability States

Shell باید از Odoo UI Services استفاده کند و Dialog، Overlay یا Keyboard System موازی و ناسازگار نسازد.

## ۶. Routeها و قابلیت‌های اصلی

### Routeهای فعال

- Workspace Home
- Personal Tasks
- Calendar
- Conversations
- Notifications Center
- Dynamic Work Report، فقط در صورت دسترسی یا Applicability
- صفحات Domainهای Provider براساس Capability
- Dashboard Management Center برای ادمین

### Routeهای حذف‌شده

- `global-search-page`
- `recent-history`

Search و Recent History در Command Palette مشترک قرار دارند.

## ۷. Search و Recent History

- بازکردن Palette با Capability سطح ابزار مانند `search.use` کنترل می‌شود.
- هر Provider مجوز رکوردهای خود را مستقل اعمال می‌کند.
- Search هیچ Permission جدیدی ایجاد نمی‌کند.
- Query خالی Recent Items مجاز را نشان می‌دهد.
- Recent History فقط Resource Reference نگه می‌دارد.
- رکورد حذف‌شده، منقضی یا غیرمجاز نمایش داده نمی‌شود.
- ماژول مستقل `cas_recent_history` در v8 ایجاد نمی‌شود.

## ۸. Personal Task و Action

- Personal Task برای کار خود شخص است و در `cas_personal_task` ذخیره می‌شود.
- Assignment یک Task برای شخص دیگر، Action سازمانی است و در `cas_action_hub` ذخیره می‌شود.
- Workspace هیچ مدل موقت یا دائمی برای Personal Task ندارد.
- دسته‌های Personal Task می‌توانند شخصی یا سیستمی باشند.
- دسته سیستمی در Backend محافظت می‌شود.

## ۹. Calendar

- Invitation با Task Assignment یکسان نیست.
- Self Task از Calendar در `cas_personal_task` ایجاد می‌شود.
- Task برای دیگری در `cas_action_hub` ایجاد می‌شود.
- Attendee Selector باید Server-side، صفحه‌بندی‌شده و Scope-aware باشد.
- `cas_organization_core` محدوده افراد قابل انتخاب را تعیین می‌کند.
- ایجاد Event و Action باید Transactional و Idempotent طراحی شود.

## ۱۰. Conversations

- Odoo Mail/Discuss/Bus زیرساخت مرجع است.
- CAS مدل Message موازی ایجاد نمی‌کند.
- قابلیت‌های استاندارد Odoo Reuse می‌شوند.
- فقط شکاف‌های واقعی مانند Policyهای سازمانی یا Interactionهای تأییدشده Extension می‌شوند.
- Conversation با Correspondence رسمی متفاوت است.
- فهرست گفتگو و Message Body Scroll مستقل دارند؛ Route گفتگو Scroll کلی ندارد.

## ۱۱. Notification Center

- Route مستقل Notification Center در v8 حفظ می‌شود.
- Notification Delivery از Odoo Mail/Discuss/Bus استفاده می‌کند.
- CAS سیستم اعلان را از صفر بازسازی نمی‌کند.
- قبل از هر توسعه، `Odoo_Notification_Gap_Analysis.md` مرجع است.
- Extension احتمالی فقط برای Aggregation، Deep Link، Severity، Actionability یا Policyهای فاقد معادل استاندارد ایجاد می‌شود.

## ۱۲. Dashboard Governance

### کاربر عادی

- Widgetهای مجاز را جابه‌جا می‌کند.
- Hide/Show عمومی در دامنه فعلی v8 نیست.
- Resize تا تصمیم بعدی فعال نیست.
- Policy سازمانی بر Preference کاربر مقدم است.

### ادمین

Dashboard Management Center باید امکان این موارد را فراهم کند:

- فعال و غیرفعال‌کردن Widgetها
- تعیین ترتیب و Layout پیش‌فرض
- تعیین Scope شرکت، نقش یا Profile
- اجباری یا اختیاری‌کردن Widget
- Lock جابه‌جایی Widgetهای مشخص
- Preview و Publish
- Versioning و Rollback تنظیمات
- Reset Preferenceهای کاربر
- نمایش Provider و Availability
- Audit تغییرات

ترتیب حل Preference:

```text
System Default
→ Company Policy
→ Role/Profile Default
→ User Preference
```

Company Policy می‌تواند مقدار را Lock کند.

## ۱۳. Organization Scope

`cas_organization_core` مرجع مشترک این مفاهیم است:

- شرکت و واحد
- ساختار سرپرستی و مدیریتی
- Assignment مؤثر در یک بازه زمانی
- چندوظیفه‌ای بودن فرد
- جانشینی و Delegation سازمانی
- Scope قابل مشاهده یا قابل تخصیص
- Reviewer پیش‌فرض براساس ساختار

هیچ ماژولی نباید منطق زیردستی یا Assignment را مستقل و متفاوت بازنویسی کند.

## ۱۴. Work Report

### ۱۴.۱ واحد گزارش

مبنای گزارش `Shift Occurrence` است:

```text
هر شخص + هر Shift Occurrence = حداکثر یک Work Report
```

شیفت عبوری از نیمه‌شب یک گزارش واحد دارد.

### ۱۴.۲ چند Assignment

اگر شخص در یک شیفت چند Assignment فعال داشته باشد:

- یک Work Report ایجاد می‌شود.
- هر Assignment یک Section مستقل دارد.
- اطلاعات مشترک در Header گزارش قرار می‌گیرد.
- Validation، Evidence، Reviewer و Form Version می‌توانند در سطح Section متفاوت باشند.

### ۱۴.۳ Applicability

وضعیت گزارش‌دهی در Profile یا Override شخص تعیین می‌شود:

- `Required`
- `Optional`
- `Disabled`

در حالت `Disabled`:

- فرم شخصی وجود ندارد.
- Draft ساخته نمی‌شود.
- Reminder ثبت گزارش ارسال نمی‌شود.
- کاربر فقط در صورت داشتن Scope، گزارش دیگران را می‌بیند.

### ۱۴.۴ دسترسی

دسترسی به گزارش از مسیرهای زیر ایجاد می‌شود:

1. مالک گزارش
2. رابطه سازمانی
3. Reviewer یا Approver
4. Access Grant تفویض‌شده
5. نقش ممیزی یا کنترل عملکرد

Access Grant می‌تواند براساس شرکت، واحد، شغل، شخص، Profile، Assignment یا Section محدود شود و عملیات View، Comment، Review، Request Correction، Return، Approve، Export یا Audit را جداگانه اعطا کند.

### ۱۴.۵ Form Engine

- `cas_work_report` مالک Lifecycle گزارش است.
- Form Engine مالک ساختار فرم، Version، Field و Answer است.
- Workflow مالک مسیر فرایند است.
- Approval مالک تصمیم رسمی است.
- State گزارش باید Projection قابل‌فهم از منابع مرجع باشد و State Machine موازی ناسازگار ایجاد نکند.

## ۱۵. Activity Catalog

`cas_activity_catalog` ماژول مستقل است و مالک این موارد است:

- کد و عنوان فعالیت استاندارد
- توضیح عملیاتی
- Scope واحد، شغل یا Assignment
- تاریخ اعتبار
- نیاز و نوع Evidence
- ارتباط با KPI
- پیشنهاد فعالیت جدید و فرایند استانداردسازی

Snapshot عنوان و توضیح اولیه کاربر باید در گزارش حفظ شود.

## ۱۶. File و Document

در v8:

- Form Engine نوع Field فایل، تصویر یا Evidence را تعریف می‌کند.
- فایل واقعی در Odoo Attachment یا زیرساخت موجود Document ذخیره می‌شود.
- Work Report ارتباط معنایی فایل با Report، Section، Assignment و Activity را نگه می‌دارد.

بازطراحی بنیادی File/Document Infrastructure خارج از دامنه v8 است و نباید اجرای نسخه ۸ را متوقف کند. این موضوع برای نسخه آینده شامل Versioning، Retention، Archive، Advanced Permission، Digital Signature و Nextcloud Integration خواهد بود.

## ۱۷. امنیت

- Capability برای UX و Navigation است، نه جایگزین ACL.
- ACL، Record Rule و Method Check همگی لازم‌اند.
- Provider باید Permission خود را اعمال کند.
- Search و Dashboard نباید با `sudo` داده غیرمجاز را استخراج کنند.
- Section-level access در Work Report باید در Backend enforce شود.
- Access Grant باید زمان‌دار، قابل لغو و Audit‌شونده باشد.
- Cross-company leakage ممنوع است.

## ۱۸. وضعیت آمادگی اجرا

این Baseline محصولی `Agreed` است. هر ماژول زمانی `Implementation Ready` می‌شود که موارد زیر تکمیل شوند:

- Specification
- Domain Model
- API Contract
- Security Model
- Migration Strategy
- Test Strategy
- Acceptance Criteria
- Observability و Audit Requirements

## ۱۹. موضوعات خارج از دامنه نسخه ۸

- بازطراحی کامل File/Document Infrastructure
- Hide/Show آزاد Widget توسط کاربر عادی
- Resize آزاد Widgetها
- جایگزینی کامل Odoo Notification
- تغییر Odoo Core
- ایجاد Message Model موازی
- ذخیره تاریخ شمسی به‌عنوان تاریخ اصلی

## ۲۰. قاعده تغییر Baseline

هر تغییر این سند نیازمند:

1. Decision Record جدید یا اصلاح‌شده
2. ثبت دلیل و اثر
3. به‌روزرسانی Traceability Matrix
4. تعیین اسناد Superseded
5. تأیید مالک محصول

هیچ اصلاح فنی یا محدودیت کد موجود به‌تنهایی مجوز کاهش نسخه ۸ نیست.