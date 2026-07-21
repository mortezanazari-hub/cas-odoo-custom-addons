# Page Specification — مرکز مدیریت داشبورد

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-ADMIN-DASHBOARD-MGMT-V8` |
| نسخه | `v8 through iteration 12` |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Consolidated` |
| نقش | Workspace Administrator / System Administrator |
| مالک | `cas_workspace` |
| Decision | `DEC-018` |

## هدف

ادمین باید بتواند Dashboard و Widgetهای Workspace را بدون تغییر کد برای شرکت، نقش یا Profile پیکربندی، Preview، Publish و Rollback کند.

## دامنه

این صفحه فقط تنظیمات ظاهری و حاکمیت Dashboard را مدیریت می‌کند. داده کسب‌وکاری Widgetها نزد Providerها باقی می‌ماند.

## ساختار صفحه

### ۱. فهرست Configurationها

ستون‌ها:

- نام Configuration
- Company
- Role/Profile Scope
- Version
- Status: Draft / Published / Archived
- Effective From
- آخرین ویرایشگر
- Provider Health Summary

### ۲. Configuration Editor

- انتخاب Widgetهای مجاز
- تعیین ترتیب و Grid Position
- تعیین اندازه پیش‌فرض از Supported Sizes Provider
- Required / Optional
- Draggable / Locked
- Default Visibility توسط ادمین
- Provider Availability
- تنظیمات Widget در محدوده Contract
- Preview در Desktop، Tablet و Mobile

### ۳. Policy Resolution Preview

ادمین باید بتواند برای یک کاربر نمونه نتیجه این زنجیره را ببیند:

```text
System Default
→ Company Policy
→ Role/Profile Default
→ User Preference
```

برای هر مقدار باید Source و Lock Status نمایش داده شود.

### ۴. Publish

- Validate Provider Keys
- Validate Capabilityها
- Validate Grid
- نمایش Impact Summary
- ثبت Change Reason
- Publish Version جدید
- حفظ نسخه قبلی برای Rollback

### ۵. Rollback

- انتخاب نسخه قبلی
- Preview تفاوت
- ثبت دلیل
- ایجاد نسخه Published جدید از Snapshot قدیمی
- عدم حذف تاریخچه

### ۶. User Reset

ادمین مجاز می‌تواند:

- Preference یک کاربر را Reset کند.
- Preference یک Scope را Reset کند.
- قبل از Reset تعداد کاربران و اثر را ببیند.
- عملیات در Audit ثبت شود.

## قواعد Widget

هر Widget باید Registry Metadata داشته باشد:

- `provider_key`
- `widget_key`
- عنوان و توضیح
- Capability
- Supported Sizes
- Configuration Schema
- Default Size
- Required Dependencies
- Availability Check
- Data Sensitivity
- Deep Link

Widget ناشناخته یا Provider غیرفعال نباید بدون هشدار Publish شود.

## رفتار کاربر عادی در v8

- فقط Widgetهای مجاز و Unlocked را Reorder می‌کند.
- Hide/Show آزاد ندارد.
- Resize آزاد ندارد.
- نمی‌تواند Widget اجباری را حذف یا جابه‌جایی Lock‌شده را تغییر دهد.

## Stateها

- Loading
- Empty: هنوز Configuration ساخته نشده
- Draft
- Validation Error
- Provider Unavailable
- Publish Conflict
- Forbidden
- Ready

## امنیت

- فقط گروه‌های مدیریتی مجاز به ورود هستند.
- ACL و Method Check برای Create، Edit، Publish، Rollback و Reset جداست.
- تغییر Client-side Scope پذیرفته نمی‌شود.
- Cross-company Edit فقط با مجوز صریح ممکن است.
- تمام Publish، Rollback و Resetها Audit می‌شوند.

## هم‌زمانی

- Optimistic Lock یا Version Check برای جلوگیری از overwrite لازم است.
- دو ادمین نباید یک Version را بدون Conflict Resolution هم‌زمان Publish کنند.

## معیار پذیرش

1. ادمین بدون کدنویسی Layout پیش‌فرض بسازد.
2. Scope شرکت و Role/Profile اعمال شود.
3. Preview نتیجه نهایی یک کاربر ممکن باشد.
4. Configuration نسخه‌بندی و Rollback شود.
5. Widget Provider نامعتبر Publish را متوقف کند.
6. User Preference نتواند Company Lock را Override کند.
7. تمام عملیات حساس Audit شوند.
8. هیچ داده کسب‌وکاری Widget در Workspace کپی نشود.