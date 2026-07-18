# CAS Correspondence Advanced

> نسخه: `19.0.1.0.0` · Odoo 19 Community

لایه پیشرفته دبیرخانه: قالب، دفتر وارده/صادره، PDF رسمی و امضای ممیزی‌پذیر.

## اجزای ماژول

- `cas.correspondence.template`: قالب
- `cas.correspondence.register` و event: دفتر ثبت
- `cas.correspondence.signature`: امضا/ابطال
- افزونه letter و audit
- گزارش QWeb/PDF رسمی

## نقش‌ها

کاربر مکاتبات برای عملیات مجاز و مدیر برای قالب و دفتر.

## روش کار

1. قالب و دفترهای ثبت پیکربندی می‌شوند.
2. قالب روی پیش‌نویس اعمال و محتوا نهایی می‌شود.
3. دبیرخانه نامه را وارده/صادره ثبت می‌کند.
4. PDF رسمی تولید و سند نسخه‌دار می‌شود.
5. امضای مجاز یا ابطال با دلیل ثبت می‌شود.

## منوها

دفتر ثبت، دفتر امضا و قالب‌های مکاتبه.

## نصب و ارتقا

وابستگی‌ها: `cas_correspondence`، `cas_document_core`.

```bash
./odoo-bin -d <database> -i cas_correspondence_advanced --stop-after-init
./odoo-bin -d <database> -u cas_correspondence_advanced --stop-after-init
```

## قواعد کلیدی

- PDF رسمی بازنویسی نمی‌شود.
- شماره و رخداد دفتر ممیزی‌پذیرند.
- ابطال امضا سابقه را حذف نمی‌کند.

## آزمون‌ها

آزمون‌های template، register، PDF و signature.

جزئیات معماری و سناریوها: [راهنمای کامل](docs/ARCHITECTURE_AND_USAGE.md).

## مستندات

- [معماری و راهنمای استفاده](docs/ARCHITECTURE_AND_USAGE.md)
- [مرجع فنی استخراج‌شده از کد](docs/TECHNICAL_REFERENCE.md)
