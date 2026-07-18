# معماری و راهنمای استفاده از CAS Jalali - QWeb & Reports Bridge

## هدف و مرز

نمایش جلالی t-fieldهای Date/Datetime در QWeb، PDF، portal و ایمیل با امکان خروجی صریح میلادی.

## وابستگی‌ها

- cas_jalali
- base

## اجزای تشکیل‌دهنده

- افزونه ir.qweb
- renderer تاریخ
- renderer تاریخ‌وزمان
- گزینه cas_gregorian برای خروجی ماشین

## نقش و امنیت

نقش مستقل ندارد؛ auto-install با Jalali.

مجوز سمت سرور معیار نهایی است و patch رابط کاربری جای کنترل دسترسی را نمی‌گیرد.

## تجربه کاربری

در render قالب QWeb اثر می‌گذارد و منوی مستقل ندارد.

## سناریوی استفاده

1. در قالب از t-field استاندارد استفاده کنید.
2. renderer خروجی انسانی را جلالی می‌کند.
3. برای payload الزاماً میلادی cas_gregorian را فعال کنید.
4. PDF/ایمیل را با timezone کاربر کنترل کنید.

## قواعد و محدودیت

- فقط خروجی renderer تبدیل می‌شود.
- خروجی ماشین‌خوان باید صریحاً میلادی باشد.
- رشته دستی از این پل عبور نمی‌کند.

## نصب، ارتقا و تست

```bash
./odoo-bin -d <database> -i cas_jalali_qweb --stop-after-init
./odoo-bin -d <database> -u cas_jalali_qweb --stop-after-init
./odoo-bin -d <database> --test-enable --test-tags /cas_jalali_qweb -u cas_jalali_qweb --stop-after-init
```

test_qweb_jalali.py.

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
