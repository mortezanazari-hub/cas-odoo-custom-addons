# CAS Design & Product Specifications

این پوشه مرجع رسمی تصمیمات محصول، طراحی رابط کاربری، معماری، مالکیت دامنه‌ها، امنیت و مسیر آماده‌سازی اجرای پروژه **CAS Organizational Workspace** است.

> **مرجع فعال و نهایی محصول:** `CAS UI Workspace v8 — Through Iteration 12`
>
> نسخه ۸ مورد تأیید است و نباید برای سازگارشدن با کد یا ماژول‌های قدیمی تضعیف شود. کد و ماژول‌ها باید بعداً با این Specificationها منطبق شوند.

## نقطه شروع اجباری

پیش از استناد به هر سند دیگر، این فایل‌ها باید به‌ترتیب خوانده شوند:

1. [خط مبنای رسمی نسخه ۸](00_Project/V8_Canonical_Baseline.md)
2. [حاکمیت و مرجعیت مستندات](00_Project/Documentation_Governance.md)
3. [ماتریس ردیابی تصمیم تا ماژول](00_Project/Traceability_Matrix.md)
4. [واژگان رسمی محصول](01_Product/Terminology.md)
5. [نقشه مالکیت ماژول‌ها](03_Modules/V8_Module_Ownership_Map.md)
6. [مدل مرزبندی و معماری](05_Architecture/Module_Boundaries.md)
7. [مدل Capability و امنیت](05_Architecture/Capability_And_Security_Model.md)
8. [سؤالات باز و موضوعات آینده](00_Project/Open_Questions.md)

## قاعده مرجعیت

در صورت تعارض، ترتیب اعتبار اسناد چنین است:

```text
V8 Canonical Baseline
→ Decision Recordهای Agreed نسخه ۸
→ Architecture Contractهای نسخه ۸
→ Module Specificationهای Implementation Ready
→ Page Specificationهای نسخه ۸
→ Change Setهای نسخه ۸
→ Impact Assessmentها
→ اسناد نسخه ۷ و نسخه ۴
```

اسناد نسخه‌های قبلی برای حفظ تاریخچه نگهداری می‌شوند، اما در تعارض با v8 مرجع پیاده‌سازی نیستند.

## خط نسخه‌بندی

```text
CAS UI Prototype v4 → CAS UI Workspace v7 → CAS UI Workspace v8
```

- نسخه‌های ۵ و ۶ Release رسمی مستقل نیستند.
- نسخه ۷ یک Historical Baseline است.
- نسخه فعال، `Workspace v8` شامل تمام تصمیم‌های تأییدشده تا Iteration 12 است.

## تصمیم‌های غیرقابل‌عقب‌گرد نسخه ۸

- هیچ تغییری در Odoo Core مجاز نیست.
- Workspace مالک هیچ داده کسب‌وکاری نیست و فقط مالک تنظیمات ظاهری، چیدمان، Preferenceها و وضعیت‌های UI خودش است.
- `cas_personal_task` مالک کامل Personal Task است.
- Task شخصی برای خود کاربر در `cas_personal_task` و Task سازمانی برای دیگران در `cas_action_hub` نگهداری می‌شود.
- دعوت تقویمی با تخصیص وظیفه یکسان نیست.
- جست‌وجو و Recent History در Command Palette مشترک ادغام شده‌اند؛ Route مستقل آن‌ها حذف شده است.
- Notification Center فعلاً Route مستقل دارد، اما از زیرساخت Odoo Mail/Discuss/Bus استفاده می‌کند و CAS فقط شکاف‌های واقعی را تکمیل می‌کند.
- Workspace از Provider Contract برای مصرف داده ماژول‌ها استفاده می‌کند و منطق دامنه آن‌ها را کپی نمی‌کند.
- `cas_organization_core` مرجع رابطه سازمانی، Assignment مؤثر، سلسله‌مراتب، جانشینی و Scope است.
- `cas_activity_catalog` مالک فرهنگ فعالیت‌های استاندارد سازمان است.
- گزارش کار براساس رخداد واقعی شیفت ساخته می‌شود، نه مرز روز تقویمی.
- هر شخص در هر Shift Occurrence حداکثر یک گزارش ترکیبی با Sectionهای چند Assignment دارد.
- الزام گزارش می‌تواند در Profile یا برای شخص `Required`، `Optional` یا `Disabled` باشد.
- دسترسی به گزارش فقط تابع زیردستی نیست؛ دسترسی تفویض‌شده، Reviewer، کنترل عملکرد و ممیزی نیز پشتیبانی می‌شود.
- زیرساخت فایل و Document در v8 بازطراحی بنیادی نمی‌شود و به‌عنوان موضوع نسخه آینده ثبت شده است.
- کاربر عادی در v8 فقط Widgetهای مجاز را جابه‌جا می‌کند؛ حاکمیت داشبورد از مرکز مدیریت ادمین انجام می‌شود.

## ساختار پوشه

- `00_Project`: خط مبنا، حاکمیت اسناد، نسخه‌ها، ردیابی و سؤال‌های باز
- `01_Product`: اصول محصول، UX و واژگان
- `02_UI_UX`: Specification صفحه‌ها و نقش‌ها
- `03_Modules`: مالکیت، وابستگی، Providerها و Specification ماژول‌ها
- `04_Decisions`: Decision Recordهای مشترک
- `05_Architecture`: معماری کلان، امنیت، داده و Integration
- `06_ChangeSets`: بسته‌های تغییر و دامنه انتقال از نسخه‌های قبلی

## چرخه تصمیم تا اجرا

1. ثبت یا اصلاح Page Specification
2. ثبت Decision Record مشترک
3. ثبت اثر در Traceability Matrix
4. تعیین مالک دامنه و Providerها
5. تدوین Architecture Contract
6. تدوین Specification، API، Security، Migration و Test Strategy ماژول
7. تغییر وضعیت به `Implementation Ready`
8. پیاده‌سازی ماژول‌ها براساس Specification
9. تطبیق، تست و ثبت وضعیت `Verified`

## قواعد سخت

- UI جایگزین ACL، Record Rule، Capability و Method Check نیست.
- مخفی‌شدن Route یا دکمه هیچ دسترسی جدید یا محدودیت امنیتی واقعی ایجاد نمی‌کند.
- Search و Workspace حق استفاده از `sudo` برای عبور از مجوز Provider را ندارند.
- داده تاریخ در قالب استاندارد Odoo ذخیره می‌شود؛ Jalali لایه نمایش و ورود است.
- هر تصمیم باید شناسه، وضعیت، مالک، سند مرجع و اثر ماژولی قابل‌ردیابی داشته باشد.
- سند Historical نباید بدون تصمیم صریح به مرجع فعال بازگردد.

## وضعیت فعلی

Baseline محصولی نسخه ۸ تا Iteration 12 تجمیع شده است. این مجموعه مرجع طراحی ماژول‌های آینده است؛ با این حال هر ماژول فقط پس از تکمیل API، Security، Migration و Test Strategy خود به وضعیت `Implementation Ready` می‌رسد.