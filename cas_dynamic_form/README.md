# CAS Dynamic Form

> نسخه: `19.0.1.0.6` · Odoo 19 Community

اجرای دیداری و RTL فرم‌های منتشرشده با OWL، ذخیره پیش‌نویس و ورودی جلالی.

## اجزای ماژول

- افزونه مدل‌های تعریف، نسخه، فیلد و submission
- `dynamic_form_app.js/xml`: برنامه اجرا
- `dynamic_reference_field.js/xml`: انتخاب رکورد مرجع
- `dynamic_form.scss`: ظاهر واکنش‌گرا
- Client action با تگ `action_cas_dynamic_form_runtime`

## نقش‌ها

کاربر مجاز ثبت فرم؛ انتشار و طراحی تابع Form Core.

## روش کار

1. کاربر یک نسخه منتشرشده را باز می‌کند.
2. Runtime schema را بارگذاری و کنترل مناسب هر نوع فیلد را نمایش می‌دهد.
3. پاسخ‌ها پیش‌نویس ذخیره و بازیابی می‌شوند.
4. ارسال نهایی اعتبارسنجی سمت کاربر و سرور را اجرا می‌کند.
5. تاریخ برای کاربر جلالی و در Odoo به‌صورت استاندارد میلادی/UTC ذخیره می‌شود.

## منوها

از فرم منتشرشده یا Workspace باز می‌شود؛ منوی مدیریتی مستقل لازم ندارد.

## نصب و ارتقا

وابستگی‌ها: `cas_form_core`، `cas_jalali`، `web`.

```bash
./odoo-bin -d <database> -i cas_dynamic_form --stop-after-init
./odoo-bin -d <database> -u cas_dynamic_form --stop-after-init
```

## قواعد کلیدی

- Runtime فقط نسخه منتشرشده و مجاز را اجرا می‌کند.
- اعتبارسنجی سرور مرجع نهایی است.
- نمایش جلالی مقدار ذخیره‌شده را تغییر نمی‌دهد.

## آزمون‌ها

آزمون‌های runtime در `tests/`.

جزئیات معماری و سناریوها: [راهنمای کامل](docs/ARCHITECTURE_AND_USAGE.md).

## مستندات

- [معماری و راهنمای استفاده](docs/ARCHITECTURE_AND_USAGE.md)
- [مرجع فنی استخراج‌شده از کد](docs/TECHNICAL_REFERENCE.md)
