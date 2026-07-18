# CAS Approval Core

> نسخه: `19.0.1.0.2` · Odoo 19 Community

سیاست تأیید چندمرحله‌ای، تعیین تأییدکننده، نمایندگی، تصمیم و تاریخچه رسمی.

## اجزای ماژول

- `cas.approval.policy` و `cas.approval.step`: سیاست و مرحله
- `cas.approval.request` و `cas.approval.line`: درخواست و تصمیم
- `cas.approval.history`: دفتر ممیزی
- `cas.approval.delegation`: جانشینی تاریخ‌دار
- wizard رد
- افزونه workflow version/instance

## نقش‌ها

کاربر تأیید و مدیر تأیید؛ مدیر سیستم نقش مدیر دارد.

## روش کار

1. مدیر سیاست و مراحل را تعریف می‌کند.
2. درخواست ایجاد و تأییدکننده هر مرحله resolve می‌شود.
3. تأییدکننده یا نماینده معتبر تصمیم می‌گیرد.
4. تأیید مرحله بعد/گذار را فعال می‌کند؛ رد دلیل می‌خواهد.
5. همه تصمیم‌ها در تاریخچه می‌مانند.

## منوها

صندوق تأیید، درخواست‌ها، سیاست‌ها و نمایندگی‌ها.

## نصب و ارتقا

وابستگی‌ها: `cas_workflow_core`، `mail`، `hr`.

```bash
./odoo-bin -d <database> -i cas_approval_core --stop-after-init
./odoo-bin -d <database> -u cas_approval_core --stop-after-init
```

## قواعد کلیدی

- تصمیم فقط توسط مسئول یا نماینده معتبر است.
- رد بدون دلیل ثبت نمی‌شود.
- سوابق رسمی بازنویسی نمی‌شوند.

## آزمون‌ها

آزمون‌های policy، delegation، approve/reject و workflow integration.

جزئیات معماری و سناریوها: [راهنمای کامل](docs/ARCHITECTURE_AND_USAGE.md).
