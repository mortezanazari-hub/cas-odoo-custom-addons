# اصول UX محصول CAS Workspace

| مشخصه | مقدار |
|---|---|
| وضعیت | `Agreed` |
| خط مبنا تاریخی | `CAS_UI_Prototype_V4`, `Workspace v7` |
| نسخه فعال | `CAS UI Workspace v8 — Through Iteration 12` |
| مرجع | `../00_Project/V8_Canonical_Baseline.md` |

## اصول

### ۱. Action-First

میزکار ابتدا کارها، تصمیم‌ها، رویدادها و موارد قابل اقدام را نشان می‌دهد؛ KPI و نمودار در اولویت بعدی‌اند.

### ۲. خوانایی مقدم بر تراکم

هیچ متن کاربردی کمتر از ۱۲ پیکسل نیست. Compact Mode فقط فاصله‌ها و تراکم را کاهش می‌دهد.

### ۳. فارسی و RTL واقعی

Navigation، Form، Table، Calendar، Drawer، Pagination و Direction Control از ابتدا RTL طراحی می‌شوند.

### ۴. یکپارچگی نقش‌ها

همه نقش‌ها از Shell، Design Token، Navigation و Interaction Pattern مشترک استفاده می‌کنند. تفاوت در محتوا و Permission است.

### ۵. Progressive Disclosure

جزئیات ثانویه در Drawer، Modal یا Detail View نمایش داده می‌شوند و فضای اصلی را اشغال نمی‌کنند.

### ۶. Scroll متناسب با Context

- Routeهای عادی از Scroll بومی صفحه استفاده می‌کنند.
- Conversation Route Scroll کلی ندارد.
- Conversation List و Message Body Scroll مستقل دارند.
- Widget فقط در صورت محدودیت ارتفاع واقعی Scroll داخلی دارد.

### ۷. شخصی‌سازی کنترل‌شده

ترتیب حل تنظیمات:

```text
System Default
→ Company Policy
→ Role/Profile Default
→ User Preference
```

Company Policy می‌تواند تنظیم را Lock کند.

در v8 کاربر عادی Widgetهای مجاز را جابه‌جا می‌کند. Hide/Show و Resize آزاد در Scope فعلی نیستند.

### ۸. حاکمیت داشبورد

ادمین باید از Dashboard Management Center بتواند Widgetها، Layout، Scope، Lock، Preview، Publish، Version و Rollback را مدیریت کند.

### ۹. ارتباط سطح اول

گفتگو قابلیت اصلی است و از Sidebar، Topbar و Workspace قابل دسترسی است. زیرساخت Odoo Mail/Discuss/Bus Reuse می‌شود.

### ۱۰. تقویم در متن کار

مرور روز، هفته و ماه بدون خروج از محیط کاری ممکن است. Invitation، Self Task و Assigned Action مفاهیم جدا هستند.

### ۱۱. Command Palette ابزار است، نه Destination

Search و Recent History صفحه مستقل ندارند. Command Palette از Topbar، Hero و میانبر صفحه‌کلید باز می‌شود.

### ۱۲. Search مجوز ایجاد نمی‌کند

Search فقط نتایجی را نشان می‌دهد که Provider و Backend برای کاربر مجاز کرده‌اند.

### ۱۳. Workspace مالک داده نیست

Workspace فقط نمایش، Orchestration و تنظیمات ظاهری را مدیریت می‌کند. داده کسب‌وکاری نزد Domain Owner باقی می‌ماند.

### ۱۴. Profile-driven Experience

Form، Work Report Applicability، Sectionها، Reviewerها و Context باید از Profile و Assignment مؤثر Resolve شوند و دلیل Resolution قابل توضیح باشد.

### ۱۵. Shift-aware Work Report

گزارش کار براساس Shift Occurrence ایجاد می‌شود. عبور شیفت از نیمه‌شب نباید گزارش را به دو بخش تقویمی تقسیم کند.

### ۱۶. Multi-assignment بدون تکثیر بی‌دلیل

چند Assignment در یک شیفت یک گزارش ترکیبی با Sectionهای مستقل می‌سازند.

### ۱۷. Reuse before Rebuild

قابلیت استاندارد Odoo، به‌ویژه Mail، Discuss، Bus، Attachment، Dialog و Services، ابتدا Reuse می‌شود. CAS فقط Gap واقعی را Extend می‌کند.

### ۱۸. Overlay و Focus قابل پیش‌بینی

Modal، Dropdown، Selector و Command Palette از Stack، Escape، Focus Trap، Focus Restore و Outside Click مشترک پیروی می‌کنند.

### ۱۹. حالت‌های کامل صفحه

هر صفحه باید این Stateها را پوشش دهد:

- Loading
- Empty
- Forbidden
- Unavailable
- Error
- Ready
- Partial Failure، در Flowهای چند Provider

### ۲۰. UI مرجع امنیت نیست

ACL، Record Rule، Capability، Method Check و Scope Resolver مرجع امنیت‌اند. مخفی‌شدن کنترل فقط UX است.

## واژگان ترجیحی

- «میزکار» برای صفحه روزانه کاربر
- «گفت‌وگوها» برای Conversation
- «نیازمند اقدام» برای موارد منتظر اقدام
- «فوری»، «نزدیک موعد» و «عقب‌افتاده» به‌جای نمایش SLA فنی
- «گزارش شیفت» یا «گزارش کار» براساس Context
- «تفویض دسترسی» برای Access Grant مستقل از زیردستی

## موارد ممنوع

- فونت کاربردی زیر ۱۲ پیکسل
- Theme ناسازگار میان صفحات
- آیکن نامه برای گفتگو
- Scroll کلی در Conversation Route
- Route مستقل Search یا Recent History
- ذخیره تاریخ شمسی به‌عنوان تاریخ اصلی
- `sudo` برای دورزدن دسترسی
- کپی داده Domainها در Workspace
- Message Model موازی Odoo
- Notification System موازی بدون Gap Analysis
- تغییر مستقیم Odoo Core
- تقسیم شیفت عبوری از نیمه‌شب به دو گزارش صرفاً براساس تاریخ تقویمی