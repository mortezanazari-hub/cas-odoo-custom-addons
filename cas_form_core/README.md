# CAS Form Core

> نسخه: `19.0.1.1.0` · Odoo 19 Community

هسته نسخه‌دار فرم‌ها، ساختار منطقی، پاسخ تایپ‌شده و چرخه پیش‌نویس تا ارسال.

## اجزای ماژول

- `cas.form.definition`: هویت پایدار فرم
- `cas.form.version`: بازبینی قابل انتشار
- `cas.form.field` و `cas.form.field.option`: فیلد و گزینه
- `cas.form.node`: ساختار منطقی
- `cas.form.submission` و `cas.form.answer`: ثبت و پاسخ تایپ‌شده
- `cas.form.versioned.mixin`: قواعد نسخه‌بندی

## نقش‌ها

کاربر فرم، طراح، منتشرکننده و مدیر فرم.

## روش کار

1. طراح تعریف فرم را می‌سازد و نسخه اولیه خودکار ایجاد می‌شود.
2. فیلدها و گره‌ها روی نسخه پیش‌نویس تنظیم می‌شوند.
3. منتشرکننده نسخه را اعتبارسنجی و منتشر می‌کند.
4. کاربر submission می‌سازد، پیش‌نویس ذخیره و نهایی ارسال می‌کند.
5. تغییر ساختار با بازبینی جدید انجام می‌شود و سوابق به نسخه قبلی متصل می‌مانند.

## منوها

ارسال‌ها، تعاریف فرم، نسخه‌ها و پیکربندی.

## نصب و ارتقا

وابستگی‌ها: `cas_core`، `mail`، `web`.

```bash
./odoo-bin -d <database> -i cas_form_core --stop-after-init
./odoo-bin -d <database> -u cas_form_core --stop-after-init
```

## قواعد کلیدی

- نسخه منتشرشده تغییرناپذیر است.
- نوع پاسخ باید با نوع فیلد سازگار باشد.
- هر submission به نسخه مشخص pin می‌شود.

## آزمون‌ها

آزمون‌های versioning و submission در `tests/`.

جزئیات معماری و سناریوها: [راهنمای کامل](docs/ARCHITECTURE_AND_USAGE.md).

## مستندات

- [معماری و راهنمای استفاده](docs/ARCHITECTURE_AND_USAGE.md)
- [مرجع فنی استخراج‌شده از کد](docs/TECHNICAL_REFERENCE.md)
