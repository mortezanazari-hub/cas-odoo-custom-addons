# CAS Jalali Calendar

> نسخه: 19.0.2.1.0 · Odoo 19 Community

لایه ورودی و نمایش جلالی فیلدهای Date/Datetime و DateTimeInput؛ ذخیره استاندارد Odoo را تغییر نمی‌دهد.

## اجزا

- helperهای Python برای parse/format
- هسته تبدیل JavaScript
- picker گرافیکی
- field/formatter/parser registry
- patch مؤلفه DateTimeInput
- CSS سازگار با RTL

## نقش‌ها

نقش مستقل ندارد؛ برای کاربران backend فعال است.

## روش کار

1. ماژول را نصب و assetها را بازسازی کنید.
2. کاربر با رقم فارسی، عربی یا لاتین یا picker تاریخ را وارد می‌کند.
3. مقدار به تاریخ استاندارد Odoo تبدیل می‌شود.
4. Datetime با timezone کاربر نمایش و UTC ذخیره می‌شود.
5. در کد Python از helperهای tools استفاده کنید.

## نقطه ورود

منوی مستقل ندارد و داخل فیلدهای تاریخ ظاهر می‌شود.

## نصب و ارتقا

وابستگی‌ها: web، cas_core.

```bash
./odoo-bin -d <database> -i cas_jalali --stop-after-init
./odoo-bin -d <database> -u cas_jalali --stop-after-init
```

## قواعد و محدودیت‌ها

- PostgreSQL میلادی و Datetime به UTC می‌ماند.
- تبدیل فقط لایه انسانی است.
- group_by جلالی و import/export شفاف در این نسخه نیست.

## آزمون‌ها

test_jalali.py و آزمون asset.

[راهنمای معماری و استفاده](docs/ARCHITECTURE_AND_USAGE.md)

## مستندات

- [معماری و راهنمای استفاده](docs/ARCHITECTURE_AND_USAGE.md)
- [مرجع فنی استخراج‌شده از کد](docs/TECHNICAL_REFERENCE.md)
