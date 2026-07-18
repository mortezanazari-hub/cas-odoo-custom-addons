# CAS Jalali Suite

> نسخه: 19.0.2.1.0 · Odoo 19 Community

متامodule نصب یکپارچه خانواده جلالی؛ مدل، منو یا داده مستقل ندارد.

## اجزا

- manifest تجمیعی پنج جزء
- فاقد مدل، view، asset و منوی اختصاصی

## نقش‌ها

فاقد نقش مستقل.

## روش کار

1. Suite را نصب کنید.
2. Odoo همه bridgeها را نصب می‌کند.
3. فیلد، chatter، گزارش و فیلتر را smoke-test کنید.
4. پیش از uninstall اثر وابستگی Suite را بررسی کنید.

## نقطه ورود

از Apps نصب می‌شود و منوی مستقل ندارد.

## نصب و ارتقا

وابستگی‌ها: cas_jalali، cas_jalali_hr، cas_jalali_mail، cas_jalali_search، cas_jalali_qweb.

```bash
./odoo-bin -d <database> -i cas_jalali_suite --stop-after-init
./odoo-bin -d <database> -u cas_jalali_suite --stop-after-init
```

## قواعد و محدودیت‌ها

- منطق تکراری نباید داشته باشد.
- نسخه اجزا هماهنگ می‌ماند.
- آزمایشگاه QA در بسته production نیست.

## آزمون‌ها

با تست اجزا و نصب تمیز سنجیده می‌شود.

[راهنمای معماری و استفاده](docs/ARCHITECTURE_AND_USAGE.md)
