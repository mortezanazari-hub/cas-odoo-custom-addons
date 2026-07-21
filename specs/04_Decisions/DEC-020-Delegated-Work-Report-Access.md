# DEC-020 — دسترسی تفویض‌شده گزارش کار

| مشخصه | مقدار |
|---|---|
| وضعیت | `Agreed` |
| نسخه | `v8` |
| تاریخ تثبیت | `2026-07-21` |

## زمینه

برخی نقش‌ها مانند مسئول کنترل عملکرد، ممیز یا نماینده تفویض‌شده هیچ زیردستی ندارند، اما باید همه یا بخشی از گزارش‌های سازمان را مشاهده و بررسی کنند. مدل فقط Manager/Subordinate این نیاز را پوشش نمی‌دهد.

## تصمیم

`cas_work_report` مدل Access Grant مستقل از رابطه زیردستی دارد.

Access Grant می‌تواند Scope را بر مبنای این موارد محدود کند:

- Company
- Organization Unit
- Job/Role
- Person
- Report Profile
- Assignment Type یا Assignment مشخص
- Report یا Section مشخص
- Date/Shift Range

عملیات مستقل:

- View
- Comment
- Review
- Request Correction
- Return
- Approve
- Export
- Audit

View هرگز به‌صورت ضمنی Approve ایجاد نمی‌کند.

## رابطه با Organization Core

- `cas_organization_core` واقعیت سازمانی و Scope پایه را Resolve می‌کند.
- `cas_work_report` Permission اختصاصی Report و Access Grant را enforce می‌کند.
- Grant گزارش نباید دسترسی شخص را در سایر Domainها افزایش دهد.

## الزامات امنیتی

- Grant زمان‌دار و قابل لغو است.
- Grantor، Reason و Scope اجباری‌اند.
- ایجاد، تمدید و لغو Audit می‌شود.
- Section-level visibility در Backend enforce می‌شود.
- Export فقط محتوای مجاز را شامل می‌شود.
- Cross-company Grant نیازمند مجوز صریح است.

## نمونه

مسئول کنترل عملکرد می‌تواند Summary، KPI، مغایرت و Evidence واحدهای تفویض‌شده را View، Comment، Audit و Export کند، بدون اینکه Edit یا Approve داشته باشد.

## گزینه ردشده

اعطای گروه عمومی «مشاهده همه گزارش‌ها» بدون Scope، زمان، عملیات و Audit رد شد.