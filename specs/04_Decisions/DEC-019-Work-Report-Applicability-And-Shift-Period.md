# DEC-019 — گزارش کار Shift-based و Applicability

| مشخصه | مقدار |
|---|---|
| وضعیت | `Agreed` |
| نسخه | `v8` |
| تاریخ تثبیت | `2026-07-21` |

## زمینه

روز تقویمی برای کارکنان شیفتی، مخصوصاً شیفت عبوری از نیمه‌شب، واحد مناسبی برای گزارش نیست. همچنین همه افراد الزام یکسان برای ثبت گزارش ندارند و برخی مدیران فقط گزارش دیگران را مشاهده می‌کنند.

## تصمیم

### واحد گزارش

```text
هر شخص + هر Shift Occurrence = حداکثر یک Work Report
```

- شیفت ۱۹:۳۰ تا ۰۷:۳۰ یک گزارش واحد است.
- کارکنان اداری نیز گزارش را برای رخداد شیفت روزانه خود ثبت می‌کنند.
- ایجاد Draft باید Idempotent باشد.

### چند Assignment

اگر فرد در یک Shift چند Assignment مؤثر داشته باشد، یک گزارش ترکیبی با Sectionهای مجزا ایجاد می‌شود.

### Applicability

- `Required`
- `Optional`
- `Disabled`

Applicability از Company Default، Report Profile و User Override Resolve می‌شود.

در `Disabled` هیچ Form، Draft یا Reminder شخصی وجود ندارد. دسترسی مشاهده گزارش دیگران مستقل است.

## پیامدها

- Shift Occurrence باید Reference پایدار داشته باشد.
- Form Version در سطح Section Pin می‌شود.
- Organization Core Assignmentهای مؤثر را Resolve می‌کند.
- UI برای شخص Disabled فقط Monitoring/Review را در صورت دسترسی نشان می‌دهد.

## گزینه‌های ردشده

- یک گزارش ثابت برای هر روز تقویمی
- چند گزارش جدا برای Assignmentهای هم‌زمان یک Shift
- ساخت Form خالی برای فردی که Applicability او Disabled است