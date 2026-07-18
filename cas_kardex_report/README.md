# CAS Kardex Reports

> نسخه: `19.0.1.0.1` · Odoo 19 Community

خروجی Excel جزئی و خلاصه کاردکس با فیلتر تاریخ، کارمند و واحد.

## اجزای ماژول

- `cas.kardex.report.wizard`: فیلتر و دانلود
- `cas.kardex.report.service`: تهیه داده و workbook
- Workbook مبتنی بر `xlsxwriter` با برگه جزئیات/خلاصه

## نقش‌ها

سرپرست کاردکس و نقش‌های بالاتر.

## روش کار

1. بازه تاریخ و در صورت نیاز کارمند/واحد را انتخاب کنید.
2. مشخص کنید جزئیات، خلاصه و رکوردهای پیش‌نویس در خروجی باشند یا نه.
3. دکمه دریافت Excel را بزنید.
4. فایل را از نظر مجموع دقیقه‌ها و فیلترهای انتخابی کنترل کنید.

## منوها

گزارش Excel کاردکس در بخش عملیات کاردکس.

## نصب و ارتقا

وابستگی‌ها: `cas_kardex_management`.

```bash
./odoo-bin -d <database> -i cas_kardex_report --stop-after-init
./odoo-bin -d <database> -u cas_kardex_report --stop-after-init
```

## قواعد کلیدی

- گزارش فقط رکوردهای مجاز طبق record rule را می‌بیند.
- جمع زمان از دقیقه محاسبه و فقط در نمایش قالب‌بندی می‌شود.
- خروجی نباید داده شرکت دیگر را افشا کند.

## آزمون‌ها

آزمون‌های service، filter، totals و workbook.

جزئیات معماری و سناریوها: [راهنمای کامل](docs/ARCHITECTURE_AND_USAGE.md).

## مستندات

- [معماری و راهنمای استفاده](docs/ARCHITECTURE_AND_USAGE.md)
- [مرجع فنی استخراج‌شده از کد](docs/TECHNICAL_REFERENCE.md)
