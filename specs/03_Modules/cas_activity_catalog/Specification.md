# Module Specification — `cas_activity_catalog`

| مشخصه | مقدار |
|---|---|
| وضعیت محصول | `Agreed` |
| وضعیت اجرا | `Needs Detailed API/Security/Test Design` |
| مالک دامنه | فرهنگ فعالیت‌های استاندارد سازمان |

## هدف

این ماژول فهرست استاندارد فعالیت‌های سازمان را مستقل از Work Report نگهداری می‌کند تا عنوان، تعریف، Evidence و ارتباط KPI در تمام ماژول‌ها یکسان باشد.

## مدل‌های مفهومی

### Activity Definition

- code
- title
- operational description
- category
- company scope
- organization unit scope
- job/role scope
- assignment type scope
- valid from/to
- active
- evidence policy
- estimated/allowed duration policy اختیاری
- KPI references
- tags

### Activity Proposal

- proposer
- original title
- original description
- context
- submitted at
- review status
- mapped activity
- reviewer
- decision reason

## Snapshot Rule

وقتی Activity در Work Report ثبت می‌شود، موارد زیر در Snapshot گزارش حفظ می‌شوند:

- عنوان اولیه کاربر
- توضیح اولیه کاربر
- Activity Definition انتخاب‌شده در زمان ثبت
- Version یا Effective Date تعریف

اصلاح Catalog نباید تاریخچه گزارش قبلی را بازنویسی کند.

## Evidence Policy

Catalog می‌تواند اعلام کند:

- Evidence لازم نیست.
- Evidence اختیاری است.
- Evidence اجباری است.
- نوع Evidence مجاز چیست.

Enforcement نهایی در Context Work Report و Form Engine انجام می‌شود.

## KPI Integration

Activity می‌تواند به یک یا چند KPI Mapping متصل شود، اما KPI Calculation و Performance Evaluation مالکیت جدا دارند.

## پیشنهاد فعالیت جدید

اگر Activity مناسب وجود نداشته باشد:

1. کاربر عنوان و توضیح خود را ثبت می‌کند.
2. گزارش متوقف نمی‌شود.
3. Activity Proposal ساخته می‌شود.
4. Reviewer یا Catalog Manager آن را Mapping، Approve یا Reject می‌کند.
5. Snapshot اولیه گزارش حفظ می‌شود.

## امنیت

- کاربران مجاز Catalog را جست‌وجو می‌کنند.
- فقط Catalog Manager تعریف را ایجاد یا تغییر می‌دهد.
- Scope شرکت و واحد enforce می‌شود.
- Proposal Reviewer با Role/Capability مشخص می‌شود.
- تغییرات تعریف Audit می‌شوند.

## API مفهومی

- search effective activities
- resolve activity by context
- create proposal
- review proposal
- map proposal to activity
- get evidence policy
- get KPI mappings

## Performance

- Search صفحه‌بندی‌شده و Server-side
- Index روی code، title، scope و validity
- عدم بارگذاری کل Catalog در Client

## Test Strategy

- Effective dating
- Scope filtering
- Proposal lifecycle
- Snapshot immutability
- Evidence policy resolution
- KPI mapping visibility
- Cross-company isolation

## معیار پذیرش

- Catalog مستقل از Work Report نصب شود.
- گزارش منتظر تأیید Proposal نماند.
- تغییر Catalog گزارش تاریخی را تغییر ندهد.
- کاربر Activity خارج از Scope را نبیند.
- Evidence Policy قابل Resolve و توضیح باشد.