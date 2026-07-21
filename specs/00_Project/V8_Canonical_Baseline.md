# رکورد چرخه بازنگری UI شماره 8

| مشخصه | مقدار |
|---|---|
| شناسه | `UIR-CAS-WORKSPACE-08` |
| عنوان | `CAS UI Review Cycle 8 — Through Iteration 12` |
| نوع | UI Review Record |
| وضعیت Cycle | `Active Review Source` |
| نسخه نرم‌افزار | `N/A` |
| نسخه محصول | `N/A` |
| جایگزین خودکار تصمیم‌های قبلی | خیر |
| مرجع فرایند | `UI_Review_Lifecycle.md` |

## 1. اصلاح اصطلاح

این فایل قبلاً با عنوان «Canonical Baseline محصول» تفسیر شده بود. تفسیر صحیح این است:

- Cycle 8 هشتمین بازنگری کلی UI است.
- Iteration 12 دوازدهمین اصلاح داخلی آن است.
- این Cycle نسخه نرم‌افزار یا نسخه نهایی محصول نیست.
- با ورود Cycle 9، Cycle 9 آخرین چرخه فعال بازنگری UI می‌شود.
- تصمیم‌های Active کشف‌شده در Cycle 8 تا زمان Supersede صریح معتبر می‌مانند.

## 2. هدف Cycle 8

هدف این Cycle بررسی UI و استخراج موارد زیر بوده است:

- تغییرات لازم در ماژول‌های موجود؛
- ماژول‌های جدید موردنیاز؛
- تغییر مالکیت Domain؛
- حذف یا جابه‌جایی قابلیت‌ها؛
- اصلاح امنیت و Scope؛
- تغییر Workflow و Approval؛
- نیازهای Backend برای پشتیبانی از تجربه مطلوب؛
- سناریوهای لازم برای اعتبارسنجی بعد از پیاده‌سازی.

## 3. تصمیم‌های مهم کشف‌شده

- Workspace مالک Business Data نیست.
- Personal Task مالک مستقل دارد.
- Organization Scope باید Resolver مشترک داشته باشد.
- Activity Catalog دامنه مستقل است.
- Search و Recent History در Command Palette تجمیع می‌شوند.
- Odoo Mail/Discuss/Bus باید Reuse شود.
- Notification System موازی بدون Gap Analysis ایجاد نمی‌شود.
- Dashboard Management Center برای مدیریت تنظیمات Workspace لازم است.
- Work Report بر Shift Occurrence تکیه دارد.
- چند Assignment در یک شیفت یک گزارش ترکیبی دارند.
- دسترسی تفویض‌شده گزارش مستقل از Hierarchy قابل تعریف است.
- زیرساخت File/Document در Cycle جاری بازطراحی نمی‌شود و موضوع آینده است.

## 4. وضعیت اعتبار تصمیم‌ها

این تصمیم‌ها به‌دلیل قرارداشتن در Cycle 8 معتبر نیستند؛ اعتبار آن‌ها از وضعیت `Active` یا `Agreed` در Decision و Specification مربوط ناشی می‌شود.

## 5. مرجع Backend

Backend باید با مجموعه اسناد مؤثر منطبق شود، نه با این فایل به‌تنهایی.

## 6. انتقال به Cycle بعدی

در Cycle بعد:

1. Observationهای جدید ثبت می‌شوند.
2. تغییرات نسبت به اسناد Active تحلیل می‌شوند.
3. Decisionهای جدید ساخته می‌شوند.
4. Decisionهای تغییرکرده Supersede می‌شوند.
5. Module Impact به‌روزرسانی می‌شود.
6. Implementation Gapها اصلاح می‌شوند.
7. UI Revalidation اجرا می‌شود.

## 7. اجزای Cycle 8

### Workspace

- Shell
- Sidebar
- Topbar
- Command Palette
- Notifications Center
- Dashboard Governance
- Provider Availability

### Personal Work

- Personal Tasks
- Calendar
- Conversations
- Action Hub Boundary
- Recent History

### Work Report

- Dynamic Form
- Profile Resolution
- Shift Occurrence
- Composite Sections
- Applicability
- Delegated Access
- Evidence
- Projection

## 8. اصل عدم عقب‌گرد

عدم عقب‌گرد به این معناست که تصمیم Active فقط به‌دلیل محدودیت کد حذف نمی‌شود. این اصل به معنی غیرقابل‌تغییر بودن Cycle 8 نیست. Product Owner می‌تواند در Cycle جدید تصمیم را تغییر دهد؛ تغییر باید صریح، ردیابی‌شده و دارای Supersede Record باشد.
