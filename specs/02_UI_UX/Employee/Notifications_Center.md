# Page Specification — مرکز اعلان‌ها

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-EMP-NOTIF-001` |
| نسخه هدف | `Workspace v8 through iteration 12` |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Consolidated / Needs Odoo Gap Verification` |
| Route | `notifications-center` |
| Capability ابزار | `notifications.use` |
| مالک Delivery | Odoo Mail/Discuss/Bus |
| مالک View | `cas_workspace` |

## هدف

مرکز اعلان‌ها یک Route مستقل برای مشاهده اعلان‌های مجاز و مرتبط با کاربر است. این صفحه Action Hub یا Inbox موازی Odoo نیست و Notification System را از صفر بازسازی نمی‌کند.

## تصمیم پایه

```text
Odoo Mail / Discuss / Activity / Bus
= زیرساخت اصلی Message و Notification Delivery

CAS Notification Center
= نمای تجمیعی، Deep Link و Extension محدود برای Gapهای واقعی
```

قبل از ساخت مدل یا سرویس جدید، `Odoo_Notification_Gap_Analysis.md` باید بررسی و با Odoo 19 Community Verify شود.

## تفاوت Notification و Action

- Notification اطلاع‌رسانی است.
- Action نیازمند انجام یا تصمیم است.
- خواندن Notification به معنی انجام Action نیست.
- Notification می‌تواند به Action یا رکورد منبع Deep Link داشته باشد، ولی آن را کپی نمی‌کند.

## منابع

- Odoo Mail/Discuss
- Workflow و Approval
- Action Hub
- Calendar
- Correspondence
- Documents
- Attendance و Shift
- Work Report
- System Health، فقط در صورت Scope

هر منبع از Provider/Adapter امن استفاده می‌کند.

## ساختار صفحه

### Filterها

- همه
- خوانده‌نشده
- نیازمند توجه
- نوع یا منبع
- بازه زمانی

### Notification Item

- عنوان
- خلاصه حداقلی
- منبع
- زمان
- وضعیت خوانده‌شدن
- Severity، در صورت Extension معتبر
- Primary Deep Link
- Action Button، فقط در صورت Contract و Permission

### Bulk Actions

فقط اگر زیرساخت Odoo و Security اجازه دهد:

- Mark as Read
- Mark as Unread
- Archive/Hide from Center

Bulk Action نباید رکورد منبع را تغییر دهد مگر Action صریح Domain اجرا شود.

## Count

- Sidebar و Topbar از یک Provider/Source of Truth استفاده می‌کنند.
- Count باید Permission-aware باشد.
- رکورد Forbidden در Count افشا نمی‌شود.
- در نبود Realtime، Fetch یا Polling امن قابل استفاده است.

## Deep Link

- Resource Reference استاندارد دارد.
- Permission در مقصد دوباره بررسی می‌شود.
- رکورد حذف‌شده یا از دسترس خارج‌شده Unavailable State نشان می‌دهد.
- Notification نباید Label حساس رکورد Forbidden را افشا کند.

## Stateها

- Loading
- Empty
- Ready
- Provider Partial Failure
- Realtime Unavailable
- Forbidden
- Source Record Unavailable
- Error

## Realtime

Bus استاندارد Odoo در صورت امکان Reuse می‌شود. نبود Realtime نباید صفحه را غیرقابل استفاده کند.

## Extensionهای مجاز فقط پس از Gap Analysis

- CAS Deep Link Metadata
- Severity سازمانی
- Actionable Metadata
- Aggregation Category
- Company Policy
- Retention مکمل

مدل Notification کامل موازی، Bus موازی یا Email Queue موازی ممنوع است.

## امنیت

- Provider Permission منبع را enforce می‌کند.
- `sudo` عمومی برای Count و List ممنوع است.
- Multi-company context کنترل می‌شود.
- Bulk Read/Archive نیازمند Method Check است.
- Action Button از Service رسمی Domain استفاده می‌کند.

## معیار پذیرش

1. Route مستقل `notifications-center` وجود داشته باشد.
2. Odoo زیرساخت Delivery باقی بماند.
3. Notification و Action جدا باشند.
4. Count در Topbar و صفحه همگام و Permission-aware باشد.
5. Deep Link به رکورد صحیح و مجاز برود.
6. Provider Failure به‌صورت Partial نمایش داده شود.
7. نبود Bus صفحه را از کار نیندازد.
8. هیچ مدل موازی بدون Gap اثبات‌شده ایجاد نشود.