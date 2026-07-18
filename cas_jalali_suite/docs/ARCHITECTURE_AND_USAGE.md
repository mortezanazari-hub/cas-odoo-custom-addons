# معماری و راهنمای استفاده از CAS Jalali Suite

## هدف و مرز

متامodule نصب یکپارچه خانواده جلالی؛ مدل، منو یا داده مستقل ندارد.

## وابستگی‌ها

- cas_jalali
- cas_jalali_hr
- cas_jalali_mail
- cas_jalali_search
- cas_jalali_qweb

## اجزای تشکیل‌دهنده

- manifest تجمیعی پنج جزء
- فاقد مدل، view، asset و منوی اختصاصی

## نقش و امنیت

فاقد نقش مستقل.

مجوز سمت سرور معیار نهایی است و patch رابط کاربری جای کنترل دسترسی را نمی‌گیرد.

## تجربه کاربری

از Apps نصب می‌شود و منوی مستقل ندارد.

## سناریوی استفاده

1. Suite را نصب کنید.
2. Odoo همه bridgeها را نصب می‌کند.
3. فیلد، chatter، گزارش و فیلتر را smoke-test کنید.
4. پیش از uninstall اثر وابستگی Suite را بررسی کنید.

## قواعد و محدودیت

- منطق تکراری نباید داشته باشد.
- نسخه اجزا هماهنگ می‌ماند.
- آزمایشگاه QA در بسته production نیست.

## نصب، ارتقا و تست

```bash
./odoo-bin -d <database> -i cas_jalali_suite --stop-after-init
./odoo-bin -d <database> -u cas_jalali_suite --stop-after-init
./odoo-bin -d <database> --test-enable --test-tags /cas_jalali_suite -u cas_jalali_suite --stop-after-init
```

با تست اجزا و نصب تمیز سنجیده می‌شود.

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
