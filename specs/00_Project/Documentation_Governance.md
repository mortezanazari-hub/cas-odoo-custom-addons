# حاکمیت مستندات CAS

| مشخصه | مقدار |
|---|---|
| وضعیت | `Active` |
| مرجع بالادستی | `../README.md` |
| مرجع فرایند UI | `UI_Review_Lifecycle.md` |

## 1. هدف

این سند قواعد وضعیت، مالکیت، بازبینی، Supersede و ردیابی اسناد را تعریف می‌کند.

## 2. اصل اصلی

`specs` حافظه چرخه QA میان UI و Backend است. هیچ UI Review Cycle به‌تنهایی نسخه نرم‌افزار یا مرجع کامل Backend نیست.

## 3. انواع سند

- UI Observation
- Product Decision
- Architecture Decision
- Security Decision
- Page Specification
- Module Specification
- Architecture Contract
- Change Set
- Implementation Gap
- Revalidation Record
- Historical Register

## 4. وضعیت‌ها

### اعتبار سند

`Draft`, `Under Review`, `Agreed`, `Active`, `Superseded`, `Historical`, `Rejected`, `Archived`

### اجرا

`Not Assessed`, `Gap Identified`, `Planned`, `In Development`, `Implemented`, `Partially Implemented`, `Blocked`

### اعتبارسنجی UI

`Not Validated`, `Pending Revalidation`, `Validated`, `Accepted`, `Reopened`, `Failed Validation`

## 5. Supersede

- Cycle جدید باعث Supersede خودکار نمی‌شود.
- Supersede باید صریح، دوطرفه و دارای Decision باشد.
- بخش‌های معتبر سند قدیمی می‌توانند Active باقی بمانند.
- فایل تاریخی حذف نمی‌شود.

## 6. مالکیت

هر سند باید Owner داشته باشد. مالک سند با مالک Domain الزاماً یکی نیست، اما Domain Owner باید مشخص باشد.

## 7. تغییرات الزامی همراه

هر تغییر تصمیمی باید حسب اثر، این موارد را هماهنگ کند:

- Decision Register
- Page Spec
- Module Spec
- Architecture
- Security
- Change Set
- Traceability
- Open Questions
- UI Revalidation Plan

## 8. اعلام Implementation Ready

فقط زمانی مجاز است که:

- Requirement Active باشد.
- Ownership مشخص باشد.
- API و Data Model مشخص باشند.
- Security کامل باشد.
- Migration تعریف شده باشد.
- Tests تعریف شده باشند.
- Open Question مسدودکننده وجود نداشته باشد.
- Revalidation Plan وجود داشته باشد.

## 9. ثبت Cycle جدید

Cycle جدید در `Version_History.md` و `UI_Review_Lifecycle.md` ثبت می‌شود. عبارت «نسخه محصول» برای Cycle ممنوع است.
