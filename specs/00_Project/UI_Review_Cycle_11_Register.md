# ثبت رسمی CAS UI Review Cycle 11

| مشخصه | مقدار |
|---|---|
| Document ID | `REG-UIR11` |
| Document Type | UI Review Register |
| Status | `Active` |
| Document Version | `1.0` |
| Created At | `2026-07-24` |
| Updated At | `2026-07-24` |
| Owner | Product & Architecture Governance |
| Source UI Review Cycle | `CAS UI Review Cycle 11` |
| Source Iteration | `1–7` |
| Domain Owner | Attendance Operations |
| Affected Modules | `cas_attendance_operations`, `cas_attendance_core`, `cas_workspace`, task/action/approval providers |
| Implementation Status | `Gap Identified` |
| UI Validation Status | `Design Approved` |
| Related Decision | `DEC-UIR11-GUARD-ATTENDANCE-001` |
| Related Page | `PAGE-GUARD-ATTENDANCE-STATION` |

## 1. Scope

Cycle 11 تا Iteration 7 روی نهایی‌سازی طراحی صفحه نگهبانی متمرکز شد. مدیریت سیستم عمداً خارج از Scope این چرخه باقی مانده است.

## 2. نتیجه بازبینی

صفحه نگهبانی از نظر طراحی محصولی و تجربه کاربری `Design Approved` است. این وضعیت به معنی پیاده‌سازی یا پذیرش Production نیست و پس از توسعه باید Revalidation مبتنی بر Evidence انجام شود.

## 3. تصمیم‌های تثبیت‌شده

### 3.1 ثبت عادی ورود و خروج

- جست‌وجو با نام، کد پرسنلی و عنوان شغلی؛
- فیلتر واحد و وضعیت؛
- انتخاب تکی و چندگانه؛
- نمایش کاملاً واضح کارت انتخاب‌شده با پس‌زمینه متمایز، Border ضخیم و نشان «انتخاب شد»؛
- ممنوعیت انتخاب هم‌زمان افراد دارای وضعیت «داخل» و «خارج» در یک Batch؛
- جلوگیری از ورود مجدد فرد داخل و خروج مجدد فرد خارج، در UI و Backend؛
- زمان جاری به‌عنوان پیش‌فرض؛
- امکان تغییر زمان با دلیل اجباری و Audit کامل؛
- ثبت سریع و نمایش آخرین رکوردها.

### 3.2 اصلاح رکورد قبلی

رکورد رسمی مستقیماً بازنویسی نمی‌شود. اصلاح فقط از مسیر ممیزی‌پذیر با نگهداری مقدار قبلی، مقدار جدید، دلیل، اصلاح‌کننده و زمان اصلاح انجام می‌شود.

### 3.3 تردد اعلام‌نشده

نگهبان در حالت «تردد اعلام‌نشده» فقط موارد زیر را مشخص می‌کند:

- فرد یا افراد؛
- نوع مشترک رکورد گمشده: «ورود ثبت نشده» یا «خروج ثبت نشده»؛
- تاریخ مشترک مربوط به مغایرت.

نوع و تاریخ برای همه افراد انتخاب‌شده مشترک است. نگهبان ساعت، توضیح، دلیل یا منبع تشخیص وارد نمی‌کند.

فیلد تاریخ دارای Modal تقویم جلالی است و انتخاب متنی صرف، طراحی نهایی محسوب نمی‌شود.

### 3.4 جریان پیگیری

1. نگهبان مغایرت را ثبت می‌کند؛
2. برای هر فرد یک Task/Action شخصی ایجاد می‌شود؛
3. فرد ساعت پیشنهادی و توضیح را ثبت می‌کند؛
4. سرپرست درخواست را تأیید یا رد می‌کند؛
5. فقط پس از تأیید سرپرست رکورد رسمی Attendance ایجاد می‌شود.

ثبت مغایرت توسط نگهبان نباید مستقیماً رخداد رسمی Attendance بسازد.

## 4. قیود امنیتی و یکپارچگی

- هر فرد Line مستقل و Batch مشترک دارد؛
- Cross-company و ID tampering باید در Backend رد شوند؛
- UI hiding جای ACL، Record Rule و Method Check را نمی‌گیرد؛
- رکورد تأییدشده append-only است؛
- تمام تغییرات و تأییدها باید actor، principal، target، timestamps و outcome را Audit کنند.

## 5. موارد خارج از Scope

- طراحی و تکمیل مرکز مدیریت سیستم؛
- پیاده‌سازی واقعی Backend؛
- تست Production؛
- گزارش‌های مدیریتی کامل Attendance.

## 6. Revalidation لازم پس از پیاده‌سازی

- Desktop و Tablet؛
- مانیتور کم‌کیفیت/کنتراست پایین؛
- انتخاب تکی و گروهی؛
- جلوگیری از Batch ترکیبی داخل/خارج؛
- جلوگیری از ورود/خروج تکراری؛
- تقویم جلالی؛
- Task فرد و Approval سرپرست؛
- ACL، Record Rule، direct RPC و ID tampering؛
- Audit Trail و نمونه رکورد اصلاحی.
