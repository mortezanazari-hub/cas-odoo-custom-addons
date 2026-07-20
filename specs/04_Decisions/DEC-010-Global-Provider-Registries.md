# DEC-010 — Registry مشترک برای Search، Calendar، Notification و History

| مشخصه | مقدار |
|---|---|
| وضعیت | `Needs Review` |
| خط مبنا | نسخه ۴ |
| نسخه هدف | نسخه ۷ |

## زمینه

نسخه ۷ چهار تجربه بین‌ماژولی جدید یا توسعه‌یافته دارد: جست‌وجوی سراسری، تقویم تجمیعی، مرکز اعلان‌ها و تاریخچه اخیر. پیاده‌سازی مستقیم Query هر ماژول در `cas_workspace` باعث وابستگی شدید و تکرار منطق امنیتی می‌شود.

## تصمیم پیشنهادی

`cas_workspace` فقط Registry و قرارداد Provider را نگه می‌دارد. هر ماژول منبع Provider خود را برای قابلیت‌های موردنیاز ثبت می‌کند.

## قرارداد عمومی Provider

هر Provider باید:

- بدون `sudo` اجرا شود.
- Scope و Record Rule منبع را حفظ کند.
- فیلدهای Search و Serialization را Whitelist کند.
- Resource Reference و Route رسمی برگرداند.
- نبود ماژول را با `unavailable` کنترل کند.
- مالکیت داده را به Workspace منتقل نکند.

## Providerهای قابل ثبت

- Search Provider
- Calendar Feed Provider
- Notification Provider
- Recent History Resource Adapter

## گزینه‌های ردشده

1. Query مستقیم تمام مدل‌ها از `cas_workspace`
2. کپی رکوردهای منبع در مدل‌های Workspace
3. استفاده گسترده از `sudo` برای ساده‌سازی تجمیع

## پیامدها

- API و تست هر Provider باید جداگانه تعریف شود.
- Provider Registry باید قابلیت کشف ماژول نصب‌شده و نسخه قرارداد را داشته باشد.
- Error یک Provider نباید کل صفحه یا Shell را متوقف کند.

## اسناد مرتبط

- `../02_UI_UX/Employee/Global_Search.md`
- `../02_UI_UX/Employee/Calendar.md`
- `../02_UI_UX/Employee/Notifications_Center.md`
- `../02_UI_UX/Employee/Recent_History.md`
