---
document_id: GOV-DOC-003
title: CAS Documentation Lifecycle
document_type: Governance Policy
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
owner: Documentation Governance
domain_owner: Project Governance
created_at: 2026-07-22
updated_at: 2026-07-22
canonical: true
related_documents:
  - Documentation_Contribution_Guide.md
  - Metadata_And_ID_Standard.md
---

# چرخه عمر مستندات CAS

## ۱. وضعیت‌های مجاز

```text
Draft → Under Review → Agreed/Active → Superseded/Historical → Archived
                         ↘ Rejected
```

| وضعیت | معنی | استفاده مجاز |
|---|---|---|
| Draft | پیش‌نویس ناقص یا در حال تدوین | مرجع اجرا نیست |
| Under Review | آماده بررسی رسمی | هنوز Baseline نیست |
| Agreed | محتوای مورد توافق، اما ممکن است هنوز مرجع عملیاتی فعال نباشد | تصمیم یا Spec مصوب |
| Active | مرجع جاری و Canonical | مبنای خواندن و اجرا |
| Superseded | با سند یا تصمیم دیگری جایگزین شده | فقط تاریخچه و Traceability |
| Historical | سابقه معتبر که دیگر Baseline نیست | مطالعه تاریخچه |
| Rejected | بررسی شده و پذیرفته نشده | نباید اجرا شود |
| Archived | خارج از جریان روزمره و نگهداری‌شده برای سابقه | فقط با نیاز خاص |

## ۲. انتقال وضعیت

- انتقال `Draft` به `Under Review` نیازمند Metadata کامل و Owner است.
- انتقال به `Agreed` یا `Active` نیازمند مرجع Review یا تأیید مالک دامنه است.
- انتقال به `Superseded` نیازمند `superseded_by` است.
- انتقال به `Historical` نباید مفهوم ردشدن را القا کند.
- انتقال به `Rejected` باید دلیل و Source Review داشته باشد.
- حذف فایل جایگزین Lifecycle نیست.

## ۳. وضعیت سند و وضعیت پیاده‌سازی مستقل‌اند

نمونه معتبر:

```yaml
document_status: Active
implementation_status: Gap Identified
ui_validation_status: Accepted
```

این یعنی Specification فعال و UI پذیرفته شده، ولی Backend هنوز پیاده‌سازی نشده است.

## ۴. آخرین فایل الزاماً مرجع نهایی نیست

تاریخ جدیدتر یا Cycle بالاتر به‌تنهایی سند را Canonical نمی‌کند. مرجع جاری از طریق Metadata، Registry و Documentation Map تعیین می‌شود.

## ۵. بازگشت از Superseded

فعال‌سازی دوباره سند Superseded فقط با Decision جدید، ثبت دلیل و اصلاح Registryها مجاز است. تغییر ساده Status بدون سابقه ممنوع است.
