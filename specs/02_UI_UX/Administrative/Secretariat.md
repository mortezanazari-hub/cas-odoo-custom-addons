# دبیرخانه و دفتر وارده/صادره

| مشخصه | مقدار |
|---|---|
| Document ID | `PAGE-ADM-SECRETARIAT` |
| Document Type | Page Specification |
| Status | `Active` |
| Document Version | `1.0` |
| Created At | `2026-07-22` |
| Updated At | `2026-07-22` |
| Owner | Administrative Correspondence Domain |
| Source UI Review Cycle | `CAS UI Review Cycle 10` |
| Source Iteration | `10` |
| Domain Owner | Secretariat Registry |
| Affected Modules | correspondence domain, secretariat registry, workspace, attachments |
| Implementation Status | `Gap Identified` |
| UI Validation Status | `Pending Revalidation` |
| Related Decisions | `DEC-016-UIR10-CONSOLIDATED` |
| Related Observations | `OBS-UIR10-SEC-001`, `OBS-UIR10-SCOPE-001` |
| Related Change Sets | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` |

## 1. Role Model

«دبیرخانه» عنوان شغلی یا Role Profile نیست؛ یک حوزه عملیاتی و Capability set است. کارشناس اداری یا هر کاربر مجاز می‌تواند با گروه دسترسی مناسب وارد این بخش شود.

## 2. Routes

- `/workspace/secretariat/incoming` — ثبت وارده خارجی؛
- `/workspace/secretariat/outgoing` — ثبت نهایی صادره؛
- `/workspace/secretariat/register` — دفتر وارده و صادره؛
- `/workspace/secretariat/reports` — گزارش دفتر.

## 3. Incoming External Letter

فیلدهای اجباری:

- فرستنده خارجی؛
- گیرنده داخلی؛
- موضوع؛
- شماره و تاریخ نامه فرستنده در صورت وجود؛
- تاریخ/زمان دریافت؛
- روش دریافت؛
- فایل اصل یا Attachment مجاز؛
- ثبت‌کننده؛
- ارجاع اولیه و رونوشت داخلی در صورت نیاز.

فرستنده خارجی و گیرنده داخلی دو مفهوم مستقل‌اند و MUST هم‌زمان و جداگانه نمایش داده شوند.

شماره ثبت داخلی فقط در Backend و با Sequence اتمیک ایجاد می‌شود. ورود دستی شماره در جریان عادی ممنوع است.

## 4. Outgoing Letter Final Registration

دبیرخانه محل نگارش همه نامه‌های تخصصی نیست. واحد مبدأ پیش‌نویس را تهیه و مسیر تأیید/امضا را طی می‌کند؛ دبیرخانه فقط نامه آماده خروج را ثبت نهایی، شماره‌گذاری و ارسال می‌کند.

هویت‌ها باید مستقل باشند:

- تهیه‌کننده محتوا؛
- فرستنده رسمی؛
- امضاکننده؛
- ثبت‌کننده دبیرخانه؛
- گیرنده خارجی؛
- رونوشت داخلی/خارجی.

شماره صادره فقط پس از احراز آمادگی نهایی تخصیص می‌یابد تا شماره سوخته ایجاد نشود. روش ارسال، زمان ارسال، کد رهگیری و وضعیت تحویل ثبت می‌شوند.

## 5. Register and Reports

گزارش دفتر MUST صفحه واقعی باز کند و شامل دفتر وارده، دفتر صادره، گزارش روزانه، بازه زمانی، فرستنده، گیرنده، واحد داخلی، نامه‌های ارجاع‌نشده، بدون پاسخ، محرمانه و ثبت‌کننده باشد.

Print/PDF/Excel فقط داده مجاز را صادر می‌کنند و Export Security، count leakage و metadata leakage باید کنترل شوند.

## 6. States

Incoming: Draft → Registered → Routed → Closed/Archived.

Outgoing: Draft in source domain → Approved/Signed → Ready for Registry → Registered → Sent → Delivered/Failed/Returned.

ابطال شماره یا اصلاح رکورد رسمی باید با رکورد اصلاحی و Audit انجام شود؛ حذف فیزیکی مجاز نیست.

## 7. OCR and DMS Boundary

OCR در آلفا هیچ Route، UI، Queue، Setting یا Dependency محصولی ندارد. DMS داخلی نیز تا تعیین معماری Nextcloud خارج از محدوده است. Attachment عادی به رکورد کسب‌وکار مجاز می‌ماند.

## 8. Acceptance Criteria

- عنوان کاربر «کارشناس اداری» می‌تواند مستقل از دسترسی دبیرخانه باشد؛
- فرستنده و گیرنده هم‌زمان و جدا ثبت شوند؛
- شماره‌های وارده/صادره خودکار و backend-controlled باشند؛
- صادره قبل از آمادگی نهایی شماره نگیرد؛
- گزارش دفتر Route و صفحه عملیاتی داشته باشد؛
- هیچ OCR یا DMS داخلی در Navigation آلفا دیده نشود.
