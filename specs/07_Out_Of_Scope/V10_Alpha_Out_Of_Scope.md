# خارج از محدوده آلفا — Cycle 10

| مشخصه | مقدار |
|---|---|
| Document ID | `OOS-UIR10-ALPHA` |
| Document Type | Scope Boundary |
| Status | `Active` |
| Document Version | `1.0` |
| Created At | `2026-07-22` |
| Updated At | `2026-07-22` |
| Owner | Product Governance |
| Source UI Review Cycle | `CAS UI Review Cycle 10` |
| Source Iteration | `10–13` |
| Domain Owner | Product Scope |
| Implementation Status | `Planned Removal / Not In Alpha` |
| UI Validation Status | `Pending Revalidation` |
| Related Decisions | `DEC-016-UIR10-CONSOLIDATED` |
| Related Observations | `OBS-UIR10-SCOPE-001` |
| Related Change Sets | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` |

## 1. OCR

موارد زیر MUST در آلفا وجود نداشته باشند:

- استخراج متن از تصویر یا PDF؛
- صف OCR؛
- تنظیم موتور OCR؛
- confidence/review UI؛
- Route، Menu، Dashboard card، Widget، Setting یا Report مرتبط؛
- وابستگی Backend محصولی برای OCR.

حذف OCR به معنی حذف Attachment نیست.

## 2. مدیریت اسناد داخلی / DMS

تا زمان تصویب معماری یکپارچه با Nextcloud، موارد زیر خارج از محدوده‌اند:

- مخزن فایل مستقل CAS؛
- Folder tree سازمانی DMS؛
- Document lifecycle و versioning مخزن؛
- publish/obsolete/archive در DMS داخلی؛
- file sharing داخلی موازی؛
- Sync یا conflict resolution با Nextcloud؛
- Search index اختصاصی DMS.

علت: ساخت DMS موازی قبل از Integration Decision بدهی فنی و تضاد مالکیت ایجاد می‌کند.

## 3. موارد امنیتی غیرقابل تفویض

- ورود به حساب صاحب اختیار؛
- انتقال Role، Group، ACL یا Record Rule؛
- تغییر رمز یا MFA؛
- تغییر Audit؛
- اعطای Capability بیشتر از صاحب اختیار؛
- عبور از Company/Organization Scope.

## 4. Attendance Operations

- ویرایش مستقیم یا حذف عادی رخداد رسمی؛
- ایجاد مدل موازی تردد نگهبانی؛
- ثبت Batch به‌عنوان یک رخداد مبهم برای چند فرد؛
- تغییر زمان بدون دلیل و recorded_at؛
- دورزدن conflict validation.

## 5. Secretariat

- شماره‌گذاری دستی در جریان عادی؛
- نقش یا عنوان شغلی اجباری «مسئول دبیرخانه»؛
- نگارش اجباری همه نامه‌های تخصصی توسط دبیرخانه؛
- حذف فیزیکی رکورد ثبت‌شده؛
- DMS یا OCR توکار.

## 6. Action Request

علامت درخواست اقدام در نامه به‌تنهایی Task ایجاد نمی‌کند. گیرنده مجاز تصمیم می‌گیرد Task بسازد، بدون Task رسیدگی کند یا عدم نیاز را ثبت کند.

## 7. Allowed Attachments

موارد زیر داخل محدوده باقی می‌مانند:

- Attachment روی نامه، وارده، صادره، Task و گزارش کار؛
- metadata لازم فایل روی رکورد کسب‌وکار؛
- Access control استاندارد Attachment؛
- Integration Contract آینده برای Nextcloud، بدون پیاده‌سازی DMS در آلفا.

## 8. Re-entry Rule

هر قابلیت خارج از محدوده فقط با Observation، Decision، Ownership، Security/Migration/Test Impact و Change Set جدید می‌تواند وارد Scope شود.
