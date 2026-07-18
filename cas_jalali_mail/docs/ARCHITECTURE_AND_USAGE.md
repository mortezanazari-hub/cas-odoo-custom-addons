# معماری و راهنمای استفاده از CAS Jalali - Mail & Chatter Bridge

## هدف و مرز

نمایش جلالی تاریخ پیام، tooltip و مقادیر رهگیری Date/Datetime در Chatter.

## وابستگی‌ها

- cas_jalali
- mail

## اجزای تشکیل‌دهنده

- افزونه mail.tracking.value
- patch مدل پیام در مرورگر
- CSS Mail/RTL
- آزمون tracking value

## نقش و امنیت

نقش مستقل ندارد؛ auto-install با Mail.

مجوز سمت سرور معیار نهایی است و patch رابط کاربری جای کنترل دسترسی را نمی‌گیرد.

## تجربه کاربری

در chatter و تاریخچه تغییرات ظاهر می‌شود.

## سناریوی استفاده

1. پیام یا تغییر فیلد تاریخ‌دار ایجاد کنید.
2. زمان پیام در نمایش جلالی می‌شود.
3. قدیم/جدید tracking جلالی نمایش داده می‌شوند.
4. tooltip زمان دقیق timezone کاربر را حفظ می‌کند.

## قواعد و محدودیت

- مقدار tracking و message date بازنویسی نمی‌شود.
- رشته غیرتاریخی تبدیل نمی‌شود.
- نمایش دقیق با timezone سازگار است.

## نصب، ارتقا و تست

```bash
./odoo-bin -d <database> -i cas_jalali_mail --stop-after-init
./odoo-bin -d <database> -u cas_jalali_mail --stop-after-init
./odoo-bin -d <database> --test-enable --test-tags /cas_jalali_mail -u cas_jalali_mail --stop-after-init
```

test_tracking_value.py و بررسی chatter.

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
