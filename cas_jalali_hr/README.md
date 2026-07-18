# CAS Jalali - Employees Bridge

> نسخه: 19.0.2.1.0 · Odoo 19 Community

پل نمایش جلالی timeline نسخه‌های کارمند و قراردادها که خارج از registry استاندارد رندر می‌شوند.

## اجزا

- patch JavaScript timeline کارکنان
- CSS ویژه HR و RTL

## نقش‌ها

نقش مستقل ندارد؛ با HR و Jalali خودکار نصب می‌شود.

## روش کار

1. Jalali و Employees را نصب کنید.
2. timeline کارمند را باز کنید.
3. تاریخ نسخه/قرارداد جلالی نمایش داده می‌شود.
4. ویرایش واقعی از مدل HR انجام می‌شود.

## نقطه ورود

در صفحه کارمند/قرارداد دیده می‌شود و منوی مستقل ندارد.

## نصب و ارتقا

وابستگی‌ها: cas_jalali، hr.

```bash
./odoo-bin -d <database> -i cas_jalali_hr --stop-after-init
./odoo-bin -d <database> -u cas_jalali_hr --stop-after-init
```

## قواعد و محدودیت‌ها

- مدل HR و مقدار ذخیره تغییر نمی‌کند.
- patch باید با Odoo 19 هماهنگ بماند.
- این پل مالک قرارداد نیست.

## آزمون‌ها

کنترل timeline و asset پس از ارتقای Odoo.

[راهنمای معماری و استفاده](docs/ARCHITECTURE_AND_USAGE.md)
