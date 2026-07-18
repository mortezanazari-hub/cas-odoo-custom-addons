# CAS Correspondence

> نسخه: `19.0.1.1.0` · Odoo 19 Community

مکاتبات رسمی داخلی، گیرنده، ارجاع، مشاهده، پاسخ/اصلاح، محرمانگی و ممیزی؛ جدا از چت.

## اجزای ماژول

- `cas.correspondence.letter`: نامه
- `cas.correspondence.recipient`: گیرنده
- `cas.correspondence.referral`: ارجاع
- `cas.correspondence.view.receipt`: رسید مشاهده
- `cas.correspondence.relation`: پاسخ/اصلاح
- `cas.correspondence.audit`: ممیزی
- `cas.correspondence.secretariat.delegation`: نمایندگی
- wizardهای ارجاع، تکمیل و لغو

## نقش‌ها

کاربر مکاتبات و مدیر دبیرخانه.

## روش کار

1. نامه با محرمانگی و گیرندگان آماده می‌شود.
2. ارسال، دسترسی گیرندگان و سابقه رسمی را تثبیت می‌کند.
3. گیرنده مشاهده را ثبت یا نامه را ارجاع می‌دهد.
4. مسئول ارجاع کار را شروع و تکمیل می‌کند.
5. پاسخ/اصلاح با رابطه به اصل ساخته و سپس نامه بسته می‌شود.

## منوها

نامه‌ها، پیش‌نویس‌های من، دبیرخانه و نمایندگی‌ها.

## نصب و ارتقا

وابستگی‌ها: `cas_core`، `mail`، `hr`.

```bash
./odoo-bin -d <database> -i cas_correspondence --stop-after-init
./odoo-bin -d <database> -u cas_correspondence --stop-after-init
```

## قواعد کلیدی

- record rule و محرمانگی مرجع دسترسی‌اند.
- ارسال، مشاهده، ارجاع و اصلاح ممیزی می‌شوند.
- چت جای نامه رسمی نیست.

## آزمون‌ها

آزمون‌های security، lifecycle، referral، delegation و audit.

جزئیات معماری و سناریوها: [راهنمای کامل](docs/ARCHITECTURE_AND_USAGE.md).
