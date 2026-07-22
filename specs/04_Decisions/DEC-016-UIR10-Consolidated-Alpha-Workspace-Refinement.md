# DEC-016 — تصمیم تجمیعی Cycle 10 برای اصلاح Workspace آلفا

| مشخصه | مقدار |
|---|---|
| Document ID | `DEC-016-UIR10-CONSOLIDATED` |
| Document Type | Architecture/Product Decision |
| Status | `Agreed` |
| Document Version | `1.0` |
| Created At | `2026-07-22` |
| Updated At | `2026-07-22` |
| Owner | Product & Architecture Governance |
| Reviewers | Product Owner, UX, Architecture, Security, QA |
| Source UI Review Cycle | `CAS UI Review Cycle 10` |
| Source Iteration | `1–13` |
| Effective From | `2026-07-22` |
| Supersedes | فقط baselineهای متعارض UI درباره تفویض عمومی، OCR، DMS داخلی، دبیرخانه به‌عنوان نقش، مدیر سامانه مطلق و فرم لیستی نگهبانی |
| Superseded By | `N/A` |
| Domain Owner | Cross-domain Governance |
| Affected Modules | Workspace, delegation, correspondence, secretariat, attendance, security groups |
| Implementation Status | `Gap Identified` |
| UI Validation Status | `Pending Revalidation` |
| Related Observations | `OBS-UIR10-*` |
| Related Change Sets | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` |

## Context

بازنگری Cycle 10 نشان داد چند صفحه Prototype ظاهر قابل قبول ولی منطق نقش، مالکیت و Domain مبهم داشتند. برخی قابلیت‌ها نیز قبل از تعیین معماری نهایی وارد آلفا شده بودند.

## Problem

- فرم عمومی تفویض امکان انتخاب صاحب اختیار دیگران را القا می‌کرد؛
- عملیات حوزه‌های مختلف هم‌زمان نمایش داده می‌شدند؛
- انتخاب شخص در صفحات مختلف ناسازگار بود؛
- عنوان شغلی با گروه دسترسی مخلوط شده بود؛
- دبیرخانه، وارده/صادره و شماره‌گذاری مرز روشن نداشتند؛
- OCR و DMS داخلی بدون نیاز آلفا و پیش از معماری Nextcloud وجود داشتند؛
- UI نگهبانی از مدل‌های واقعی ثبت گروهی استفاده مؤثر نمی‌کرد.

## Decision

1. تفویض فقط Capability مشخص را منتقل می‌کند، نه Role، ACL، حساب یا رمز.
2. صاحب اختیار در فرم عمومی همیشه کاربر جاری و readonly است؛ انتخاب صاحب اختیار فقط برای مدیر مجاز تفویض است.
3. تفویض حوزه‌محور است و عملیات فقط پس از انتخاب Provider همان حوزه نمایش داده می‌شوند.
4. حوزه‌های آلفا شامل مکاتبات، Task/Action، Approval/Request و گزارش کار هستند.
5. اعتبار تفویض موقت، تا اطلاع ثانوی یا بر اساس حکم است؛ تفویض بدون پایان review cadence دارد.
6. Shared People Picker تنها الگوی انتخاب شخص است و امنیت نتایج و انتخاب نهایی server-side enforce می‌شود.
7. مدیر سامانه عنوان شغلی نیست؛ گروه‌های user/access، organization، delegation، settings و audit تفکیک و مدیر ارشد تجمیعی است.
8. دبیرخانه حوزه دسترسی است، نه عنوان شغلی. وارده خارجی و ثبت نهایی صادره جریان مستقل دارند.
9. شماره وارده/صادره فقط در Backend و به‌صورت اتمیک تخصیص می‌یابد.
10. OCR و DMS داخلی در آلفا حذف می‌شوند؛ Attachment باقی می‌ماند؛ معماری DMS بعداً با Nextcloud تعیین می‌شود.
11. ایستگاه نگهبانی روی `cas.guard.batch`, `cas.guard.batch.line`, `cas.attendance.event` و `action_confirm` ساخته می‌شود.
12. زمان دستی فقط با دلیل و ثبت هم‌زمان occurred_at و recorded_at مجاز است.
13. رخداد رسمی Attendance append-only است.
14. هر صفحه قبل از طراحی باید ownership، role/capability، scope، state، security، audit، failure mode و acceptance را مشخص کند.

## Rationale

این تصمیم حداقل دسترسی، تفکیک وظایف، قابلیت ردیابی و reuse ماژول‌های موجود را حفظ می‌کند و از ایجاد مدل‌ها و UIهای موازی جلوگیری می‌کند.

## Alternatives Rejected

- یک فرم تفویض واحد برای همه نقش‌ها؛
- گروه مطلق «مدیر سامانه»؛
- نقش شغلی «دبیرخانه»؛
- DMS داخلی مستقل از Nextcloud؛
- مدل جدید برای ثبت تردد نگهبانی؛
- ویرایش مستقیم رخداد رسمی.

## Consequences

Backend providerها، Capabilityها، Audit و تست‌های امنیتی جدید یا تکمیلی لازم‌اند. Prototype به‌تنهایی Implementation Evidence نیست.

## Security Impact

ACL، Record Rule، Method Check، Company/Organization Scope، revocation، search/count/metadata leakage، ID tampering، attachment security و impersonation audit الزامی‌اند.

## Migration Impact

Navigationهای OCR/DMS حذف، تفویض‌های موجود به domain/capability/validity نگاشت، گروه‌های مدیریتی تفکیک و sequenceهای دبیرخانه تعریف می‌شوند. Migration نباید تاریخچه را حذف کند.

## Test Impact

Unit، Integration، Security، Multi-company، Migration، Regression، UI، RTL، Accessibility و Audit لازم‌اند.

## Acceptance Criteria

معیارهای `specs/05_Acceptance/V10_Alpha_Acceptance_Criteria.md` باید Pass شوند و سپس UI Production به `Accepted` تغییر کند.
