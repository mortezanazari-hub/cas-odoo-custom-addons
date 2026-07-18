# CAS Jalali - Mail & Chatter Bridge

> نسخه: 19.0.2.1.0 · Odoo 19 Community

نمایش جلالی تاریخ پیام، tooltip و مقادیر رهگیری Date/Datetime در Chatter.

## اجزا

- افزونه mail.tracking.value
- patch مدل پیام در مرورگر
- CSS Mail/RTL
- آزمون tracking value

## نقش‌ها

نقش مستقل ندارد؛ auto-install با Mail.

## روش کار

1. پیام یا تغییر فیلد تاریخ‌دار ایجاد کنید.
2. زمان پیام در نمایش جلالی می‌شود.
3. قدیم/جدید tracking جلالی نمایش داده می‌شوند.
4. tooltip زمان دقیق timezone کاربر را حفظ می‌کند.

## نقطه ورود

در chatter و تاریخچه تغییرات ظاهر می‌شود.

## نصب و ارتقا

وابستگی‌ها: cas_jalali، mail.

```bash
./odoo-bin -d <database> -i cas_jalali_mail --stop-after-init
./odoo-bin -d <database> -u cas_jalali_mail --stop-after-init
```

## قواعد و محدودیت‌ها

- مقدار tracking و message date بازنویسی نمی‌شود.
- رشته غیرتاریخی تبدیل نمی‌شود.
- نمایش دقیق با timezone سازگار است.

## آزمون‌ها

test_tracking_value.py و بررسی chatter.

[راهنمای معماری و استفاده](docs/ARCHITECTURE_AND_USAGE.md)

## مستندات

- [معماری و راهنمای استفاده](docs/ARCHITECTURE_AND_USAGE.md)
- [مرجع فنی استخراج‌شده از کد](docs/TECHNICAL_REFERENCE.md)
