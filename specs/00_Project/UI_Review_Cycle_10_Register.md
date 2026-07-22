# ثبت رسمی CAS UI Review Cycle 10

| مشخصه | مقدار |
|---|---|
| Document ID | `REG-UIR10` |
| Document Type | UI Review Register |
| Title | CAS UI Review Cycle 10 Register |
| Status | `Active` |
| Document Version | `1.0` |
| Created At | `2026-07-22` |
| Updated At | `2026-07-22` |
| Owner | Product & Architecture Governance |
| Reviewers | Product Owner, UX, Architecture, Security, QA |
| Source UI Review Cycle | `CAS UI Review Cycle 10` |
| Source Iteration | `1–13` |
| Effective From | `2026-07-22` |
| Supersedes | فقط مواردی که در این سند صریحاً ذکر شده‌اند |
| Superseded By | `N/A` |
| Domain Owner | Cross-domain Workspace Governance |
| Affected Modules | `cas_workspace`, correspondence domain, delegation domain, secretariat domain, `cas_attendance_operations`, `cas_attendance_core` |
| Implementation Status | `Gap Identified` |
| UI Validation Status | `Pending Revalidation` |
| Related Decisions | `DEC-016-UIR10-CONSOLIDATED` |
| Related Change Sets | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` |

## 1. هدف

Cycle 10 برای رفع ابهام‌های منطقی Prototype، جداسازی نقش و Capability، حذف قابلیت‌های خارج از محدوده آلفا و اتصال طراحی UI به مالکیت واقعی ماژول‌های Odoo انجام شد. Prototype فقط شاهد تعامل است و منبع حقیقت Backend نیست.

## 2. وضعیت چرخه

- Prototype review baseline: `Iteration 12`؛
- مستندسازی تجمیعی: `Iteration 13`؛
- وضعیت محصولی تصمیم‌های این سند: `Agreed`؛
- وضعیت Backend: `Gap Identified`؛
- وضعیت Production UI: `Pending Revalidation`؛
- تغییر Odoo Core: ممنوع؛
- مسیر پیاده‌سازی: فقط `custom-addons`.

## 3. Observations

| Observation ID | Iteration | صفحه/نقش/سناریو | مشاهده و تصمیم حاصل | شدت | وضعیت |
|---|---:|---|---|---|---|
| `OBS-UIR10-CORR-001` | 1–2 | مکاتبات / همه نقش‌های مجاز | عملیات نامه، هویت فرستنده رسمی و عامل واقعی، درخواست اقدام بدون Task خودکار و تصمیم گیرنده برای Task باید تفکیک شوند. | High | Converted to Gap |
| `OBS-UIR10-DELEG-001` | 3–8 | تفویض / کاربر عمومی و مدیر تفویض | فرم عمومی و مدیریتی مخلوط بود؛ حوزه، عملیات، اعتبار، حکم و Scope باید صریح باشند. | Critical | Converted to Gap |
| `OBS-UIR10-PEOPLE-001` | 4,12 | انتخاب شخص / چند صفحه | انتخاب شخص باید کامپوننت مشترک، امن، single/multiple و دارای حذف Chip هماهنگ باشد. | High | Converted to Gap |
| `OBS-UIR10-ADMIN-001` | 9 | مرکز مدیریت CAS | «مدیر سامانه» نباید عنوان شغلی یا گروه مطلق باشد؛ گروه‌های مدیریتی باید تفکیک شوند. | Critical | Converted to Gap |
| `OBS-UIR10-SEC-001` | 10 | دبیرخانه / کارشناس اداری | دبیرخانه حوزه دسترسی است؛ وارده و صادره، شماره خودکار، فرستنده/گیرنده و گزارش دفتر باید روشن شوند. | High | Converted to Gap |
| `OBS-UIR10-GUARD-001` | 11–12 | نگهبانی / نگهبان ثبت‌کننده | ثبت سریع و گروهی باید روی مدل‌های واقعی Attendance، با ساعت زنده، اصلاح ممیزی‌پذیر و انتخاب چندگانه عملیاتی باشد. | Critical | Converted to Gap |
| `OBS-UIR10-SCOPE-001` | 10–13 | کل آلفا | OCR و DMS داخلی قبل از معماری Nextcloud خارج از محدوده آلفا هستند. | High | Accepted |

## 4. خلاصه Iterationها

1. **I1:** کاهش وزن Dashboard، تکمیل عملیات مکاتبات، گیرنده/رونوشت، چاپ و PDF.
2. **I2:** فرستنده رسمی و نماینده، درخواست اقدام، پیشنهاد مهلت و تصمیم گیرنده برای ساخت Task.
3. **I3:** تفکیک `تفویض‌های من` از `مدیریت تفویض‌ها`.
4. **I4:** Shared People Picker با single/multiple، جست‌وجو، واحد و Chip.
5. **I5:** بازطراحی رابطه صاحب اختیار، نماینده، نوع و حوزه تفویض.
6. **I6:** صاحب اختیار در فرم عمومی برابر کاربر جاری؛ انتخاب صاحب اختیار فقط برای مدیر مجاز.
7. **I7:** نمایش شرطی عملیات هر حوزه و فعال‌شدن تفویض گزارش کار.
8. **I8:** اعتبار موقت، تا اطلاع ثانوی و بر اساس حکم.
9. **I9:** تفکیک گروه‌های مدیریت سامانه و نقش تجمیعی مدیر ارشد.
10. **I10:** حذف OCR، تعریف دبیرخانه به‌عنوان Access Domain، ثبت وارده/صادره و گزارش دفتر.
11. **I11:** ایستگاه سریع تردد نگهبانی بر پایه `cas.guard.batch` و `cas.attendance.event`.
12. **I12:** اصلاح انتخاب چندگانه و حذف Chip.
13. **I13:** ثبت زنجیره Observation → Decision → Module Impact → Acceptance → Revalidation.

## 5. تصمیم‌های صریح

- تفویض Capability مشخص است، نه انتقال Role، ACL، حساب یا رمز.
- در فرم عمومی صاحب اختیار قابل انتخاب نیست و همان کاربر جاری است.
- حوزه‌های آلفا برای تفویض: مکاتبات، Task/Action، Approval/Request و گزارش کار.
- تفویض می‌تواند موقت، تا اطلاع ثانوی یا بر اساس حکم باشد.
- عنوان شغلی هیچ دسترسی مدیریتی خودکار ایجاد نمی‌کند.
- دبیرخانه عنوان شغلی نیست؛ کارشناس اداری می‌تواند با Capability مناسب به آن دسترسی بگیرد.
- شماره وارده و صادره در Backend و به‌صورت خودکار تخصیص می‌یابد.
- OCR و مدیریت اسناد/DMS داخلی در آلفا حذف می‌شوند؛ Attachment باقی می‌ماند.
- رابط نگهبانی MUST روی مدل‌های موجود Attendance ساخته شود و مدل موازی نسازد.
- رخداد رسمی Attendance append-only است؛ اصلاح از مسیر void/replacement/reopen انجام می‌شود.

## 6. Revalidation Plan

پس از پیاده‌سازی، سناریوها باید با کاربران واقعی یا Test Userهای دارای Capability متناظر روی Desktop و Tablet بازآزمایی شوند. Evidence لازم: Commit/PR، Unit/Integration/Security tests، role-based screenshots، Audit records و نتیجه Pass/Fail معیارهای پذیرش.
