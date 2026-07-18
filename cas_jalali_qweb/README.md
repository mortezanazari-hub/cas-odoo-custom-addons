# CAS Jalali - QWeb & Reports Bridge

> نسخه: 19.0.2.1.0 · Odoo 19 Community

نمایش جلالی t-fieldهای Date/Datetime در QWeb، PDF، portal و ایمیل با امکان خروجی صریح میلادی.

## اجزا

- افزونه ir.qweb
- renderer تاریخ
- renderer تاریخ‌وزمان
- گزینه cas_gregorian برای خروجی ماشین

## نقش‌ها

نقش مستقل ندارد؛ auto-install با Jalali.

## روش کار

1. در قالب از t-field استاندارد استفاده کنید.
2. renderer خروجی انسانی را جلالی می‌کند.
3. برای payload الزاماً میلادی cas_gregorian را فعال کنید.
4. PDF/ایمیل را با timezone کاربر کنترل کنید.

## نقطه ورود

در render قالب QWeb اثر می‌گذارد و منوی مستقل ندارد.

## نصب و ارتقا

وابستگی‌ها: cas_jalali، base.

```bash
./odoo-bin -d <database> -i cas_jalali_qweb --stop-after-init
./odoo-bin -d <database> -u cas_jalali_qweb --stop-after-init
```

## قواعد و محدودیت‌ها

- فقط خروجی renderer تبدیل می‌شود.
- خروجی ماشین‌خوان باید صریحاً میلادی باشد.
- رشته دستی از این پل عبور نمی‌کند.

## آزمون‌ها

test_qweb_jalali.py.

[راهنمای معماری و استفاده](docs/ARCHITECTURE_AND_USAGE.md)
