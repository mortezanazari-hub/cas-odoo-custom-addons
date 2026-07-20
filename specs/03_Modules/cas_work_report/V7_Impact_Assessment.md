# ارزیابی اثر نسخه ۷ بر `cas_work_report`

| مشخصه | مقدار |
|---|---|
| وضعیت | `Needs Review` |
| نوع سند | ارزیابی اثر؛ نه Specification اجرایی |

## آثار نسخه ۷

- ثبت سریع فعالیت از میزکار
- ساخت تدریجی گزارش روزانه
- Widget واحد برای ثبت و مرور فعالیت‌های امروز
- نمایش مجموع زمان
- تبدیل اختیاری Personal Task به ردیف Activity
- حفظ Snapshot عنوان و توضیح اولیه
- ثبت فعالیت ناموجود بدون توقف گزارش
- هشدار غیرمسدودکننده اختلاف حضور و زمان ثبت‌شده
- Search Provider و Recent History Provider
- Notification برای گزارش ناقص یا نیازمند اصلاح

## مرزبندی

`cas_workspace` فقط UI و Orchestration را ارائه می‌کند. Header/Line گزارش، وضعیت، Validation، Snapshot و عملیات نهایی‌سازی متعلق به `cas_work_report` باقی می‌مانند.

## نیازهای احتمالی داده

- Daily Report Header
- Activity Line
- Standard Activity Reference
- Original Title/Description Snapshot
- Duration و Result
- Draft/Final/Reopened State
- Standardization Request Reference

## وابستگی‌ها

- Activity Catalog
- Attendance Summary
- Personal Task Adapter
- Approval/Workflow برای بررسی در صورت تصویب

## سؤال‌های باز

- مالک Activity Catalog کدام ماژول است؟
- بازگشایی گزارش نهایی چگونه کنترل می‌شود؟
- تبدیل Task به Activity کپی است یا Reference؟
- حد اختلاف زمان و Policy مسدودکننده کجا تنظیم می‌شود؟
