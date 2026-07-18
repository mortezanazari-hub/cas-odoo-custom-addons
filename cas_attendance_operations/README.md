# CAS Attendance Operations

> نسخه: `19.0.1.0.0` · Odoo 19 Community

عملیات ورود آفلاین Excel، نگاشت هویت خارجی و ثبت سریع گروهی نگهبانی.

## اجزای ماژول

- `cas.attendance.identity`: نگاشت شناسه خارجی به کارمند
- `cas.attendance.import`: پرونده ورود مرحله‌ای
- `cas.attendance.import.line`: ردیف آماده/نامشخص/تکراری/خطا
- `cas.guard.batch` و line: ثبت گروهی نگهبانی
- پارسر Excel مبتنی بر `openpyxl`

## نقش‌ها

از نقش‌های Attendance Core استفاده می‌کند: نگهبان، سرپرست و مدیر.

## روش کار

1. فایل را با نوع، محل و دستگاه بارگذاری کنید.
2. «خواندن و آماده‌سازی» ردیف‌ها را بدون ثبت نهایی تحلیل می‌کند.
3. هویت‌های ناشناخته را نگاشت و ردیف‌های تکراری/خطا را بازبینی یا رد کنید.
4. فقط ردیف‌های ready را ثبت نهایی کنید.
5. برای ثبت دستی سریع، batch نگهبانی را تکمیل و یکجا تأیید کنید.

## منوها

ثبت گروهی نگهبانی، ورود فایل دستگاه/نگهبانی و نگاشت شناسه‌های خارجی.

## نصب و ارتقا

وابستگی‌ها: `cas_kardex_management`.

```bash
./odoo-bin -d <database> -i cas_attendance_operations --stop-after-init
./odoo-bin -d <database> -u cas_attendance_operations --stop-after-init
```

## قواعد کلیدی

- parse با import نهایی یکی نیست.
- هویت ناشناخته نباید حدسی به کارمند متصل شود.
- تکراری‌ها باید idempotent تشخیص داده شوند.

## آزمون‌ها

آزمون‌های import staging، duplicate، identity و guard batch.

جزئیات معماری و سناریوها: [راهنمای کامل](docs/ARCHITECTURE_AND_USAGE.md).
