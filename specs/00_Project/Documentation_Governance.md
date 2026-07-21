# حاکمیت و مرجعیت مستندات CAS

| مشخصه | مقدار |
|---|---|
| شناسه | `GOV-DOC-001` |
| نسخه محصول | `v8` |
| وضعیت | `Agreed` |
| سطح مرجعیت | `Canonical` |

## هدف

این سند روش ایجاد، تغییر، جایگزینی و استناد به مستندات پوشه `specs` را مشخص می‌کند تا چند سند متعارض هم‌زمان مرجع اجرا نباشند.

## سلسله‌مراتب مرجعیت

1. `V8_Canonical_Baseline.md`
2. Decision Recordهای `Agreed`
3. Architecture Contractهای v8
4. Module Specificationهای `Implementation Ready`
5. Page Specificationهای v8
6. Change Setهای v8
7. Impact Assessmentها
8. Historical Documents

سند پایین‌تر حق نقض سند بالاتر را ندارد.

## Header استاندارد

هر سند جدید باید حداقل این Metadata را داشته باشد:

```yaml
document_id:
title:
document_type:
product_version: v8
document_version:
status:
authority_level:
owner:
effective_from:
supersedes:
superseded_by:
related_decisions:
related_pages:
affected_modules:
open_questions:
last_reviewed:
```

در Markdown می‌توان همین Metadata را به شکل جدول نمایش داد.

## وضعیت‌های مجاز

| وضعیت | معنا |
|---|---|
| `Draft` | در حال تدوین و غیرمرجع |
| `Needs Decision` | نیازمند تصمیم مالک محصول |
| `Agreed` | تصمیم محصولی تأییدشده |
| `Needs Architecture Review` | محصول تأیید شده ولی قرارداد فنی کامل نیست |
| `Consolidated` | با سایر اسناد هماهنگ شده است |
| `Implementation Ready` | API، Security، Migration و Test Strategy کامل است |
| `Implemented` | پیاده‌سازی انجام شده ولی تطبیق نهایی نشده است |
| `Verified` | با تست و Acceptance Criteria تأیید شده است |
| `Partially Superseded` | بخشی از سند جایگزین شده است |
| `Superseded` | مرجع فعال نیست |
| `Historical` | فقط سابقه تصمیم یا طراحی است |
| `Rejected` | تصمیم رد شده و نباید اجرا شود |

## قاعده Supersession

- نسخه جدیدتر به‌صورت خودکار سند قدیمی را حذف نمی‌کند.
- سند جدید باید صریحاً `supersedes` را ثبت کند.
- سند قدیمی نیز باید در اولین بازنگری `superseded_by` یا `Partially Superseded` دریافت کند.
- اگر اصلاح Header سند بزرگ قدیمی پرریسک باشد، Decision Register و Canonical Index باید آن را Historical اعلام کنند.

## قاعده اسناد نسخه ۷

- اسناد v7 حذف نمی‌شوند.
- انتقال فیزیکی آن‌ها اجباری نیست.
- همه آن‌ها `Historical Reference` محسوب می‌شوند.
- بخش‌های سازگار با v8 فقط به‌عنوان منشأ تصمیم قابل استفاده‌اند.
- هر تعارض با v8 به نفع v8 حل می‌شود.

## انواع اسناد

### Baseline

دامنه و تصمیم‌های غیرقابل‌عقب‌گرد نسخه را تعیین می‌کند.

### Decision Record

یک تصمیم مشترک و دلیل آن را ثبت می‌کند. Decision باید گزینه‌های ردشده و اثر ماژولی را مشخص کند.

### Page Specification

هدف، نقش، Stateها، Flow، Interaction، Security Expectation و Acceptance Criteria صفحه را ثبت می‌کند.

### Architecture Contract

مرزها، مالکیت، قرارداد داده، خطا، Transaction، Security و Integration را مشخص می‌کند.

### Module Specification

مدل‌ها، سرویس‌ها، API، Security، Migration و Test Strategy یک ماژول را تعریف می‌کند.

### Change Set

تفاوت خط مبنا و نسخه مقصد را ثبت می‌کند، ولی به‌تنهایی مجوز پیاده‌سازی نیست.

### Impact Assessment

اثر احتمالی تغییر را تحلیل می‌کند و مرجع نهایی مالکیت یا API نیست.

## ردیابی اجباری

هر Requirement باید مسیر زیر را داشته باشد:

```text
Requirement
→ Decision
→ Page/Flow
→ Architecture Contract
→ Owning Module
→ API/Security
→ Migration/Test
→ Status
```

این مسیر در `Traceability_Matrix.md` ثبت می‌شود.

## Naming

- Decision: `DEC-NNN-Title.md`
- Page: نام نقش و صفحه
- Architecture: نام مفهوم یا Contract
- Change Set: `CS-DOMAIN-VERSION.md`
- Module Specification: `03_Modules/<module>/Specification.md`

## تغییر Baseline

تغییر تصمیم قطعی v8 فقط با این شرایط مجاز است:

1. مسئله و دلیل روشن باشد.
2. اثر روی تمام اسناد و ماژول‌ها مشخص شود.
3. Decision Record ایجاد یا اصلاح شود.
4. مالک محصول تأیید کند.
5. Traceability Matrix به‌روزرسانی شود.

محدودیت کد موجود دلیل کافی برای کاهش Baseline نیست.

## قاعده Agent و توسعه‌دهنده

- پیش از پیشنهاد پیاده‌سازی، Baseline و Decision Register خوانده شود.
- هیچ فرض باز به‌عنوان تصمیم قطعی معرفی نشود.
- هیچ ماژولی صرفاً براساس Page Mockup ساخته نشود.
- تغییر مستقیم `main` بدون بازبینی مجاز نیست.
- هر PR مستندی باید فهرست اسناد ایجادشده، جایگزین‌شده و سؤال‌های باز را اعلام کند.