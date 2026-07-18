# معماری و راهنمای استفاده از CAS Jalali - Employees Bridge

## هدف و مرز

پل نمایش جلالی timeline نسخه‌های کارمند و قراردادها که خارج از registry استاندارد رندر می‌شوند.

## وابستگی‌ها

- cas_jalali
- hr

## اجزای تشکیل‌دهنده

- patch JavaScript timeline کارکنان
- CSS ویژه HR و RTL

## نقش و امنیت

نقش مستقل ندارد؛ با HR و Jalali خودکار نصب می‌شود.

مجوز سمت سرور معیار نهایی است و patch رابط کاربری جای کنترل دسترسی را نمی‌گیرد.

## تجربه کاربری

در صفحه کارمند/قرارداد دیده می‌شود و منوی مستقل ندارد.

## سناریوی استفاده

1. Jalali و Employees را نصب کنید.
2. timeline کارمند را باز کنید.
3. تاریخ نسخه/قرارداد جلالی نمایش داده می‌شود.
4. ویرایش واقعی از مدل HR انجام می‌شود.

## قواعد و محدودیت

- مدل HR و مقدار ذخیره تغییر نمی‌کند.
- patch باید با Odoo 19 هماهنگ بماند.
- این پل مالک قرارداد نیست.

## نصب، ارتقا و تست

```bash
./odoo-bin -d <database> -i cas_jalali_hr --stop-after-init
./odoo-bin -d <database> -u cas_jalali_hr --stop-after-init
./odoo-bin -d <database> --test-enable --test-tags /cas_jalali_hr -u cas_jalali_hr --stop-after-init
```

کنترل timeline و asset پس از ارتقای Odoo.

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
