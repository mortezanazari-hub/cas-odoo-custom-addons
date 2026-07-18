# CAS Jalali - Search Bridge

> نسخه: 19.0.2.1.0 · Odoo 19 Community

فیلتر تاریخ شمسی در منوی جستجوی Odoo با دوره سریع و بازه سفارشی.

## اجزا

- dialog انتخاب فیلد و بازه
- patch منوی Filters
- CSS RTL
- تبدیل بازه به domain استاندارد

## نقش‌ها

نقش مستقل ندارد؛ روی search view دارای تاریخ فعال است.

## روش کار

1. فیلتر تاریخ شمسی را باز کنید.
2. فیلد Date/Datetime را انتخاب کنید.
3. دوره سریع یا بازه سفارشی را برگزینید.
4. برای Datetime کران بالا ابتدای روز بعد است.
5. Odoo domain میلادی/UTC را اجرا می‌کند.

## نقطه ورود

در منوی Filters نمای جستجو ظاهر می‌شود.

## نصب و ارتقا

وابستگی‌ها: cas_jalali، web.

```bash
./odoo-bin -d <database> -i cas_jalali_search --stop-after-init
./odoo-bin -d <database> -u cas_jalali_search --stop-after-init
```

## قواعد و محدودیت‌ها

- timezone در Datetime لحاظ می‌شود.
- مرز ماه/فصل جلالی درست تبدیل می‌شود.
- semantics group_by ORM تغییر نمی‌کند.

## آزمون‌ها

آزمون دوره، timezone و domain.

[راهنمای معماری و استفاده](docs/ARCHITECTURE_AND_USAGE.md)

## مستندات

- [معماری و راهنمای استفاده](docs/ARCHITECTURE_AND_USAGE.md)
- [مرجع فنی استخراج‌شده از کد](docs/TECHNICAL_REFERENCE.md)
