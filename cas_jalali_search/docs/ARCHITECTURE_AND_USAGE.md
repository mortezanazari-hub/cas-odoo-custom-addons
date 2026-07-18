# معماری و راهنمای استفاده از CAS Jalali - Search Bridge

## هدف و مرز

فیلتر تاریخ شمسی در منوی جستجوی Odoo با دوره سریع و بازه سفارشی.

## وابستگی‌ها

- cas_jalali
- web

## اجزای تشکیل‌دهنده

- dialog انتخاب فیلد و بازه
- patch منوی Filters
- CSS RTL
- تبدیل بازه به domain استاندارد

## نقش و امنیت

نقش مستقل ندارد؛ روی search view دارای تاریخ فعال است.

مجوز سمت سرور معیار نهایی است و patch رابط کاربری جای کنترل دسترسی را نمی‌گیرد.

## تجربه کاربری

در منوی Filters نمای جستجو ظاهر می‌شود.

## سناریوی استفاده

1. فیلتر تاریخ شمسی را باز کنید.
2. فیلد Date/Datetime را انتخاب کنید.
3. دوره سریع یا بازه سفارشی را برگزینید.
4. برای Datetime کران بالا ابتدای روز بعد است.
5. Odoo domain میلادی/UTC را اجرا می‌کند.

## قواعد و محدودیت

- timezone در Datetime لحاظ می‌شود.
- مرز ماه/فصل جلالی درست تبدیل می‌شود.
- semantics group_by ORM تغییر نمی‌کند.

## نصب، ارتقا و تست

```bash
./odoo-bin -d <database> -i cas_jalali_search --stop-after-init
./odoo-bin -d <database> -u cas_jalali_search --stop-after-init
./odoo-bin -d <database> --test-enable --test-tags /cas_jalali_search -u cas_jalali_search --stop-after-init
```

آزمون دوره، timezone و domain.

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
