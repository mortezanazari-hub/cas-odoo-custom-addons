# Change Set — Cycle 10 Alpha Workspace Refinement

| مشخصه | مقدار |
|---|---|
| Document ID | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` |
| Document Type | Change Set |
| Status | `Active` |
| Document Version | `1.0` |
| Created At | `2026-07-22` |
| Updated At | `2026-07-22` |
| Owner | Product & Architecture Governance |
| Source UI Review Cycle | `CAS UI Review Cycle 10` |
| Source Iteration | `1–13` |
| Domain Owner | Cross-domain Workspace Governance |
| Implementation Status | `Gap Identified` |
| UI Validation Status | `Pending Revalidation` |
| Related Decisions | `DEC-016-UIR10-CONSOLIDATED` |
| Related Observations | `OBS-UIR10-*` |

## Scope

اصلاح تجربه و قراردادهای آلفا در مکاتبات، تفویض، انتخاب شخص، مدیریت سامانه، دبیرخانه و ثبت نگهبانی؛ حذف OCR و DMS داخلی از Scope آلفا.

## Observations

- `OBS-UIR10-CORR-001`
- `OBS-UIR10-DELEG-001`
- `OBS-UIR10-PEOPLE-001`
- `OBS-UIR10-ADMIN-001`
- `OBS-UIR10-SEC-001`
- `OBS-UIR10-GUARD-001`
- `OBS-UIR10-SCOPE-001`

## Added

- Shared People Picker contract؛
- `تفویض‌های من` و مدیریت تفویض سازمانی به‌عنوان دو مسیر مستقل؛
- حوزه و Provider عملیات تفویض؛
- اعتبار موقت، تا اطلاع ثانوی و بر اساس حکم؛
- گروه‌های تفکیک‌شده مدیریت سامانه؛
- ثبت وارده خارجی، ثبت نهایی صادره و گزارش دفتر؛
- ایستگاه سریع تردد نگهبانی؛
- ثبت official principal و actual actor؛
- معیارهای پذیرش و Revalidation.

## Changed

- مکاتبات: درخواست اقدام بدون Task خودکار و تصمیم گیرنده؛
- تفویض: صاحب اختیار در فرم عمومی readonly؛
- انتخاب شخص: reuse مشترک و state هماهنگ؛
- دبیرخانه: Access Domain به‌جای title شغلی؛
- نگهبانی: UI عملیاتی روی `cas.guard.batch`؛
- مدیریت سامانه: گروه‌های granular به‌جای گروه مطلق.

## Removed from Alpha

- OCR؛
- مدیریت اسناد/DMS داخلی؛
- Navigation و Routeهای مربوط؛
- انتخاب صاحب اختیار دیگران در فرم عمومی؛
- نمایش عملیات حوزه نامرتبط؛
- ویرایش عادی رخداد رسمی Attendance.

## Superseded

فقط baselineهای UI متعارض با `DEC-016-UIR10-CONSOLIDATED` Supersede می‌شوند. تصمیم‌های Active Cycle 8 و 9 که تعارض صریح ندارند همچنان معتبرند.

## Module Impacts

مرجع: `../03_Modules/V10_Module_Impact_Assessment.md`.

## Security Impacts

- Capability و Scope server-side؛
- delegation revocation؛
- principal/actor audit؛
- search/count/metadata leakage controls؛
- sequence authorization؛
- append-only attendance؛
- attachment permission؛
- multi-company isolation.

## Migration

- حذف referenceهای OCR/DMS بدون حذف Attachment؛
- تبدیل تفویض‌های موجود؛
- mapping گروه‌های مدیریت؛
- sequence و state migration دبیرخانه؛
- حفظ attendance history؛
- route/preference migration.

## Tests

Unit، Integration، Security، Multi-company، Migration، Regression، UI، RTL، Accessibility، Audit و Failure Recovery.

## Revalidation Plan

تمام معیارهای `../05_Acceptance/V10_Alpha_Acceptance_Criteria.md` با کاربران نقش‌دار، داده واقعی/نمونه معتبر و Evidence اجرا شوند.

## Open Questions

- نام و ownership نهایی ماژول دبیرخانه؛
- قرارگیری Shared People Picker در `cas_workspace` یا ماژول فنی مستقل؛
- threshold و approval policy زمان دستی Attendance؛
- Integration Contract آینده Nextcloud.

## Risks

Privilege escalation، stale delegation cache، duplicate sequence/event، metadata leakage، title-permission confusion و DMS duplication.

## Rollback

Rollback UI نباید داده Domain را حذف کند. Feature flag/route rollback مجاز است، اما ثبت‌های رسمی، Audit و Migration history باید حفظ شوند.
