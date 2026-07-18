# CAS Document Core

> نسخه: `19.0.1.0.0` · Odoo 19 Community

مدیریت سند نسخه‌دار، پوشه/برچسب، پیوند رکورد، backend ذخیره‌سازی، OCR و رخداد.

## اجزای ماژول

- `cas.document` و `cas.document.version`: سند و نسخه
- `cas.document.link`: پیوند کسب‌وکاری
- `cas.document.folder` و tag: طبقه‌بندی
- `cas.document.event`: ممیزی
- `cas.document.storage.backend`: ذخیره
- `cas.document.ocr.provider/job`: OCR
- wizard نسخه جدید

## نقش‌ها

کاربر اسناد و مدیر اسناد.

## روش کار

1. سند را در پوشه با برچسب و دسترسی ایجاد کنید.
2. فایل اولیه یا نسخه جدید را بارگذاری کنید.
3. آن را به نامه/فرم/رکورد منبع پیوند دهید.
4. OCR را ارسال، بازبینی و تأیید کنید.
5. سند را فعال، بایگانی یا با مجوز نابود کنید.

## منوها

اسناد، پوشه‌ها، صف OCR، backendها و ارائه‌دهندگان OCR.

## نصب و ارتقا

وابستگی‌ها: `mail`.

```bash
./odoo-bin -d <database> -i cas_document_core --stop-after-init
./odoo-bin -d <database> -u cas_document_core --stop-after-init
```

## قواعد کلیدی

- نسخه قبلی با بارگذاری جدید حذف نمی‌شود.
- دانلود تابع مجوز سند و منبع است.
- رخدادها و OCR قابل ردیابی می‌مانند.

## آزمون‌ها

آزمون‌های version، storage، link، lifecycle، OCR و security.

جزئیات معماری و سناریوها: [راهنمای کامل](docs/ARCHITECTURE_AND_USAGE.md).

## مستندات

- [معماری و راهنمای استفاده](docs/ARCHITECTURE_AND_USAGE.md)
- [مرجع فنی استخراج‌شده از کد](docs/TECHNICAL_REFERENCE.md)
