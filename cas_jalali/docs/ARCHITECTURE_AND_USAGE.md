# معماری و راهنمای استفاده از CAS Jalali Calendar

## هدف و مرز

لایه ورودی و نمایش جلالی فیلدهای Date/Datetime و DateTimeInput؛ ذخیره استاندارد Odoo را تغییر نمی‌دهد.

## وابستگی‌ها

- web
- cas_core

## اجزای تشکیل‌دهنده

- helperهای Python برای parse/format
- هسته تبدیل JavaScript
- picker گرافیکی
- field/formatter/parser registry
- patch مؤلفه DateTimeInput
- CSS سازگار با RTL

## نقش و امنیت

نقش مستقل ندارد؛ برای کاربران backend فعال است.

مجوز سمت سرور معیار نهایی است و patch رابط کاربری جای کنترل دسترسی را نمی‌گیرد.

## تجربه کاربری

منوی مستقل ندارد و داخل فیلدهای تاریخ ظاهر می‌شود.

## سناریوی استفاده

1. ماژول را نصب و assetها را بازسازی کنید.
2. کاربر با رقم فارسی، عربی یا لاتین یا picker تاریخ را وارد می‌کند.
3. مقدار به تاریخ استاندارد Odoo تبدیل می‌شود.
4. Datetime با timezone کاربر نمایش و UTC ذخیره می‌شود.
5. در کد Python از helperهای tools استفاده کنید.

## قواعد و محدودیت

- PostgreSQL میلادی و Datetime به UTC می‌ماند.
- تبدیل فقط لایه انسانی است.
- group_by جلالی و import/export شفاف در این نسخه نیست.

## نصب، ارتقا و تست

```bash
./odoo-bin -d <database> -i cas_jalali --stop-after-init
./odoo-bin -d <database> -u cas_jalali --stop-after-init
./odoo-bin -d <database> --test-enable --test-tags /cas_jalali -u cas_jalali --stop-after-init
```

test_jalali.py و آزمون asset.

بعد از ارتقا asset، timezone، RTL، ورودی ارقام مختلف و خروجی PDF را بررسی کنید.

## راهنمای توسعه

- patchهای OWL را کوچک و سازگار با API Odoo 19 نگه دارید.
- تبدیل تاریخ نباید قرارداد ORM/RPC را تغییر دهد.
- API و export باید قرارداد میلادی/UTC روشن داشته باشند.
- پس از تغییر JS/XML/CSS ماژول را ارتقا و asset واقعی Odoo را compile کنید.
- هر تغییر باید مرز سال کبیسه، نیمه‌شب و timezone را تست کند.

## عیب‌یابی

- **تغییر دیده نمی‌شود:** upgrade، rebuild asset و hard refresh.
- **تاریخ جابه‌جا است:** timezone و مرز روز را بررسی کنید.
- **OwlError:** اولین خطای template/event در console را مبنا بگیرید.
- **PDF میلادی/جلالی اشتباه است:** نوع t-field و گزینه cas_gregorian را کنترل کنید.

## مرجع فنی

فهرست دقیق مدل‌ها، فیلدها، متدها، ACL، record rule، منوها، actionها، cronها، assetها و آزمون‌ها در [مرجع فنی استخراج‌شده از کد](TECHNICAL_REFERENCE.md) نگهداری می‌شود.
