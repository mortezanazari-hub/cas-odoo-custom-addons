# ثبت رسمی CAS UI Review Cycle 9

| مشخصه | مقدار |
|---|---|
| Document ID | `REG-UIR09` |
| Document Type | UI Review Register |
| Title | CAS UI Review Cycle 9 — Through Iteration 13 |
| Status | `Active` |
| Document Version | `1.0` |
| Created At | `2026-07-21` |
| Updated At | `2026-07-21` |
| Owner | Product & Architecture Governance |
| Reviewers | Product Owner, UI/UX, Backend Architecture, Security |
| Source UI Review Cycle | `CAS UI Review Cycle 9` |
| Source Iteration | `Through Iteration 13` |
| Effective From | `2026-07-21` |
| Supersedes | فقط موارد صریح فهرست‌شده در این سند |
| Superseded By | `N/A` |
| Domain Owner | Multiple; see Module Impact |
| Affected Modules | `cas_workspace`, `cas_work_report`, `cas_activity_catalog`, `cas_attendance`, `cas_shift`, `cas_dynamic_form`, `cas_form_builder`, `cas_approval_core` |
| Implementation Status | `Gap Identified` |
| UI Validation Status | `Accepted as Review Baseline; Pending Implementation Revalidation` |
| Related Decisions | `DEC-010-UIR09-CONSOLIDATED` |
| Related Change Sets | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` |

## 1. ماهیت Cycle

Cycle 9 شماره نسخه نرم‌افزار نیست. این سند آخرین چرخه فعال بازنگری UI را تا Iteration 13 ثبت می‌کند. Cycle 8 حذف نمی‌شود و تصمیم‌های Active آن فقط در موارد صریح این سند Supersede می‌شوند.

## 2. منبع طراحی

- Prototype source: `CAS_UI_Review_Cycle_9_Iteration_13.zip`
- آخرین Iteration ثبت‌شده: `13`
- وضعیت Prototype: منبع بازنگری و تصمیم‌سازی؛ نه شواهد پیاده‌سازی Production

## 3. Observation Register

| Observation ID | Iteration | Page/Role | Observation | Severity | Status |
|---|---:|---|---|---|---|
| `OBS-UIR09-NAV-001` | 1–3 | Workspace / all roles | Navigation تخت، نبود مسیر بازگشت و نبود Submenu | High | Accepted |
| `OBS-UIR09-ATT-001` | 4 | Attendance Hub / employee | کارت مغایرت برای کاربر عادی بیش از دامنه ثبت ناقص ورود/خروج بود | High | Accepted |
| `OBS-UIR09-ATT-002` | 4 | Attendance correction | اصلاح ورود/خروج نیازمند تأیید سرپرست، رکورد اصلاحی مستقل و Audit است | Critical | Accepted |
| `OBS-UIR09-ATT-003` | 4 | Delegated audit | کنترل تصادفی اصلاحات باید توسط Capability تفویضی و ارجاع مغایرت به مدیرعامل انجام شود | Critical | Accepted |
| `OBS-UIR09-OT-001` | 4 | Overtime / employee | مشاهده و هر فعالیت اضافه‌کاری باید Capability و اجازه سرپرست داشته باشد | Critical | Accepted |
| `OBS-UIR09-WR-001` | 5–6 | Dashboard work report | فعالیت خارج از فهرست باید بدون توقف گزارش ثبت و برای استانداردسازی پیشنهاد شود | High | Accepted |
| `OBS-UIR09-WR-002` | 7,12,13 | Quick work report | زمان دلخواه، Dropdown جست‌وجوشونده و Layout غیرمتداخل لازم است | Medium | Accepted |
| `OBS-UIR09-FORM-001` | 7,9 | Visual form builder | Form Builder باید Field Providerهای Activity Category/Recurring Activity و Matrix Field داشته باشد | High | Accepted |
| `OBS-UIR09-DASH-001` | 7–11 | Dashboard | مخفی‌سازی ویجت نباید روی خود کارت یا با اعلان «مخفی شده» باشد | Medium | Accepted |
| `OBS-UIR09-DASH-002` | 8–11 | Dashboard header | تنظیمات میزکار فقط از آیکون هدر میزکار باز شود | Medium | Accepted |
| `OBS-UIR09-DASH-003` | 8–11 | Shortcuts | میانبرها باید قابل افزودن، حذف، ترتیب‌دهی و فیلتر Capability باشند | Medium | Accepted |
| `OBS-UIR09-DASH-004` | 10–11 | Workspace brand/header | کلیک لوگو/نام Workspace باید به Home برگرداند؛ Command Center نیز قابل مخفی‌کردن باشد | Medium | Accepted |
| `OBS-UIR09-LAYOUT-001` | 13 | Dashboard | Work Progress widget حذف و Quick Work Report تمام‌عرض و کم‌تراکم‌تر شود | Low | Accepted |

## 4. تصمیم‌های Accepted

1. Navigation درختی و Capability-aware با والد قابل کلیک، Submenu قابل Collapse/Expand و Breadcrumb قابل کلیک.
2. کلیک منوی والد، اولین Child مجاز را باز می‌کند.
3. Notification Center زیر گروه میزکار و Communications بلافاصله پس از میزکار قرار می‌گیرد.
4. Attendance Hub کاربر عادی فقط ثبت ناقص ورود/خروج را در کارت مغایرت نشان می‌دهد.
5. درخواست اصلاح ورود/خروج: Employee Request → Direct Supervisor Approval → Correction Ledger Entry → Audit Pool.
6. داده خام دستگاه یا لاگ نگهبانی بازنویسی نمی‌شود؛ اصلاح در رکورد مستقل ثبت می‌شود.
7. بازبین دارای Capability می‌تواند رکوردهای تأییدشده را تصادفی بررسی کند؛ مغایرت کشف‌شده مستقیم به مدیرعامل ارجاع می‌شود.
8. تأخیر مسیر جدا دارد و می‌تواند به Leave/Mission/Explanation منتهی شود؛ کاردکس فقط پس از تأیید بازمحاسبه می‌شود.
9. تمام قابلیت‌های Overtime با Capabilityهای مجزا و اجازه سرپرست کنترل می‌شوند؛ مخفی‌کردن UI جایگزین کنترل Backend نیست.
10. Activity خارج از Catalog قابل ثبت فوری است؛ گزارش منتظر استانداردسازی نمی‌ماند و عنوان اولیه در Audit حفظ می‌شود.
11. Form Builder باید Field Providerهای Activity Category، Recurring Activity و Dynamic Matrix را ارائه کند.
12. Workspace فقط UI Preference و Widget Settings را مالک است؛ Business Data در Domain Owner باقی می‌ماند.
13. Widget visibility و shortcut customization از آیکون تنظیمات هدر میزکار مدیریت می‌شود؛ روی Widget دکمه Hide وجود ندارد.
14. تنظیمات اختصاصی پیشرفته Widgetها به Cycle بعد Deferred است؛ Cycle 9 فقط Visibility، Shortcut customization و تنظیمات محدود پذیرفته‌شده را تثبیت می‌کند.
15. Work Progress widget از Baseline Cycle 9 حذف و Quick Work Report تمام‌عرض می‌شود.

## 5. موارد Superseded صریح

- Dashboard v8 rule «کاربر عادی فقط Reorder مجاز دارد» در محدوده Cycle 9 با Visibility و Shortcut customization گسترش می‌یابد.
- Navigation تخت Cycle 8 برای Workspace با Navigation درختی Cycle 9 جایگزین می‌شود.
- دکمه مستقل «فعالیت در فهرست نیست» جای خود را به گزینه داخل Dropdown جست‌وجوشونده می‌دهد.
- Work Progress widget در Dashboard baseline Cycle 9 حذف می‌شود.

سایر تصمیم‌های Active Cycle 8 بدون تغییر معتبر می‌مانند.

## 6. وضعیت اجرا و اعتبارسنجی

- UI Prototype review: `Accepted` تا Iteration 13.
- Backend implementation: `Gap Identified`.
- Production validation: `Pending Revalidation`.
- هیچ Requirement این سند بدون Commit/PR، Test Evidence و UI Revalidation نباید `Implemented` یا `Accepted in Production` اعلام شود.

## 7. Open Items برای Cycle بعد

- تنظیمات پیشرفته اختصاصی هر Widget و Schema کامل تنظیمات.
- اصلاحات CSS و Responsive polish باقی‌مانده.
- بازبینی نهایی تراکم، ارتفاع و Breakpointها پس از پیاده‌سازی واقعی Odoo.

## 8. Revalidation Scenarios

1. نقش‌های مختلف فقط Navigation و Childهای مجاز را می‌بینند؛ Count/Title غیرمجاز نشت نمی‌کند.
2. Direct URL برای Capability غیرمجاز `Forbidden` می‌دهد.
3. درخواست اصلاح حضور بدون تغییر لاگ خام، رکورد اصلاحی مستقل می‌سازد.
4. لغو یا انقضای Delegation دسترسی Audit را فوراً قطع می‌کند.
5. Overtime بدون Capability در Menu، Search، Count و Direct Route افشا نمی‌شود.
6. Activity پیشنهادی گزارش را قابل ارسال نگه می‌دارد و Original Label در Audit باقی می‌ماند.
7. Matrix field در Dataset بزرگ Server-side pagination و Field/Row permission را رعایت می‌کند.
8. Widget visibility و Shortcut preferences در Scope صحیح User/Company ذخیره و بازیابی می‌شوند.
9. RTL، Jalali، Mobile، Tablet، Keyboard و Accessibility آزمون می‌شوند.
