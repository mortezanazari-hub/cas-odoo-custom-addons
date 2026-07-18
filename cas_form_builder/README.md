# CAS Form Builder

> نسخه: `19.0.1.0.0` · Odoo 19 Community

طراح دیداری drag-and-drop نسخه فرم؛ ابزار طراح است، نه مقصد روزمره کاربر.

## اجزای ماژول

- افزونه `cas.form.version`
- `action_open_visual_designer`: ورود به طراح
- `form_builder.js/xml/scss`: بوم، پالت، تنظیمات و ظاهر
- patch نمای نسخه فرم

## نقش‌ها

طراح، منتشرکننده و مدیر فرم.

## روش کار

1. نسخه پیش‌نویس را در Form Core بسازید.
2. طراح دیداری را از همان نسخه باز کنید.
3. فیلدها را روی بوم رها و ویژگی‌ها و ترتیب را تنظیم کنید.
4. ذخیره کنید؛ کنترل هم‌زمانی از بازنویسی تغییر جدیدتر جلوگیری می‌کند.
5. پس از بازبینی نسخه را در Form Core منتشر کنید.

## منوها

از نسخه پیش‌نویس فرم باز می‌شود.

## نصب و ارتقا

وابستگی‌ها: `cas_form_core`، `web`.

```bash
./odoo-bin -d <database> -i cas_form_builder --stop-after-init
./odoo-bin -d <database> -u cas_form_builder --stop-after-init
```

## قواعد کلیدی

- نسخه منتشرشده قفل است.
- ساختار نامعتبر یا گره دست‌نیافتنی ذخیره نمی‌شود.
- schema جدا از Form Core ساخته نمی‌شود.

## آزمون‌ها

آزمون‌های concurrency، reachability و published lock.

جزئیات معماری و سناریوها: [راهنمای کامل](docs/ARCHITECTURE_AND_USAGE.md).
