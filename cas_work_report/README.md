# CAS Daily Work Reports

> نسخه: `19.0.1.0.0` · Odoo 19 Community

گزارش روزانه کار کارکنان با ایستگاه، نمایندگی، مهلت، تأیید رسمی و Excel.

## اجزای ماژول

- `cas.work.station`: ایستگاه کاری مستقل از واحد سازمانی
- `cas.work.report`: گزارش روزانه و ساعات
- `cas.work.report.delegation`: مجوز نمایندگی تاریخ‌دار
- `cas.work.report.export.wizard`: Excel
- افزونه `hr.employee`
- workflow/approval پیش‌فرض در post-init

## نقش‌ها

کاربر، سرپرست و مدیر گزارش کار.

## روش کار

1. کارمند یا نماینده مجاز گزارش روز/شیفت را در ایستگاه ثبت می‌کند.
2. ساعت شروع/پایان، کار عادی، اضافه‌کاری و شرح فعالیت تکمیل می‌شود.
3. گزارش حداکثر تا مهلت ۱۲ ساعته ارسال می‌شود.
4. تأیید رسمی سرپرست از Approval/Workflow انجام می‌شود؛ ثبت توسط مدیر مستقیم می‌تواند خودکار تأیید شود.
5. کاربر مجاز خروجی Excel حوزه قابل مشاهده را می‌گیرد.

## منوها

گزارش‌های من، گزارش‌های حوزه من، خروجی Excel، ایستگاه‌ها و نمایندگی‌ها.

## نصب و ارتقا

وابستگی‌ها: `hr`، `mail`، `cas_workflow_core`، `cas_approval_core`.

```bash
./odoo-bin -d <database> -i cas_work_report --stop-after-init
./odoo-bin -d <database> -u cas_work_report --stop-after-init
```

## قواعد کلیدی

- نمایندگی باید صریح، تاریخ‌دار و متناسب با حوزه باشد.
- دیدن گزارش تابع زنجیره سازمانی و record rule است.
- شماره، chatter و تاریخچه تأیید حفظ می‌شوند.

## آزمون‌ها

آزمون‌های deadline، visibility، delegation، approval و export.

جزئیات معماری و سناریوها: [راهنمای کامل](docs/ARCHITECTURE_AND_USAGE.md).

## مستندات

- [معماری و راهنمای استفاده](docs/ARCHITECTURE_AND_USAGE.md)
- [مرجع فنی استخراج‌شده از کد](docs/TECHNICAL_REFERENCE.md)
