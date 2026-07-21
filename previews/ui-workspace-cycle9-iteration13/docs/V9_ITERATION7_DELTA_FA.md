# UI Review Cycle 9 — Iteration 7

## تصمیم‌های پذیرفته‌شده

1. زمان فعالیت در گزارش کار محدود به گزینه‌های از پیش تعریف‌شده نیست؛ مقدار دلخواه دقیقه‌ای پذیرفته می‌شود.
2. فرم‌ساز به Providerهای دامنه گزارش کار دسترسی کنترل‌شده دارد:
   - دسته‌بندی‌های گزارش کار
   - عناوین فعالیت‌های تکرارشونده
3. فیلد ماتریسی پویا اضافه می‌شود؛ ردیف‌ها می‌توانند از منبع پرسنل/زیرمجموعه/واحد و ستون‌ها از فیلدهای تعریف‌شده ساخته شوند.
4. هر کاربر می‌تواند ویجت‌های میزکار خود را مخفی و دوباره بازیابی کند.

## مالکیت داده

- Taxonomy و Recurring Activity Catalog متعلق به ماژول گزارش کار است.
- Form Builder فقط Provider آن‌ها را مصرف می‌کند و کپی Business Data در Workspace یا Form Builder ایجاد نمی‌کند.
- تنظیم مخفی‌بودن ویجت، UI Preference متعلق به Workspace است.
- ماتریس فقط Schema و Binding را در Form Engine ذخیره می‌کند؛ داده پرسنلی از مدل مالک و با ACL/Record Rule خوانده می‌شود.

## اثر Backend

- نیازمند Provider Contract برای taxonomy و recurring activity catalog.
- نیازمند Field Type جدید برای source-backed selection و Matrix.
- نیازمند pagination/virtualization و server-side domain برای ماتریس‌های بزرگ.
- مخفی‌کردن ویجت بدون تغییر Business Model و در تنظیمات شخصی Workspace ذخیره می‌شود.
