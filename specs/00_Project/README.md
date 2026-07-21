# 00 — Project

این بخش مرجع سطح پروژه برای حاکمیت مستندات، تاریخچه چرخه‌های بازنگری UI، ردیابی تصمیم‌ها، وضعیت اجرا و اعتبارسنجی مجدد UI است.

## اسناد مرجع

- [چرخه بازنگری UI و حلقه تضمین کیفیت](UI_Review_Lifecycle.md)
- [رکورد چرخه بازنگری UI شماره 8](V8_Canonical_Baseline.md)
- [حاکمیت مستندات](Documentation_Governance.md)
- [تاریخچه چرخه‌های بازنگری رابط](Version_History.md)
- [ماتریس ردیابی UI تا پیاده‌سازی](Traceability_Matrix.md)
- [فهرست اسناد Historical و Superseded](Historical_Document_Register.md)
- [سؤالات باز و موضوعات آینده](Open_Questions.md)

## قاعده استفاده

هر سند جدید باید:

1. نوع نسخه خود را مشخص کند: UI Review Cycle، Iteration، Document Version یا Software Release.
2. Source UI Observation و Cycle منبع را ثبت کند.
3. به Decisionها، صفحه‌ها، ماژول‌ها و Architecture Contractهای مرتبط لینک دهد.
4. در صورت جایگزینی تصمیم قبلی، رابطه `Supersedes` را صریح ثبت کند.
5. Backend Impact، Security، Migration، Test و UI Revalidation را قابل‌ردیابی کند.
6. وضعیت سند، اجرا و اعتبارسنجی UI را جداگانه ثبت کند.

## وضعیت فعلی

`CAS UI Review Cycle 8 — Through Iteration 12` آخرین چرخه فعال بازنگری UI است؛ این عبارت نسخه نرم‌افزار یا Baseline نهایی محصول نیست. با ورود Cycle بعدی، آخرین Cycle فعال تغییر می‌کند، اما تصمیم‌های `Active` فقط با Supersede صریح تغییر می‌کنند.
