# تاریخچه نسخه‌های رسمی رابط CAS

| مشخصه | مقدار |
|---|---|
| وضعیت | `Agreed` |
| دامنه | Product / UI Versioning |

## خط نسخه‌بندی رسمی

آخرین خط مبنای پیش از بازنگری گسترده Workspace، بسته `CAS_UI_Prototype_V4` است. نسخه‌های ۵ و ۶ Release رسمی مستقل نیستند و Iterationهای داخلی طراحی محسوب می‌شوند.

```text
CAS UI Prototype v4 → CAS UI Workspace v7 → CAS UI Workspace v8
```

## نسخه ۴

- معماری نقش‌محور
- صفحات تخصصی ماژول‌ها
- نگهبانی کارت‌محور
- داشبوردهای سرپرست، مدیر و مدیرعامل
- قراردادهای اولیه Workspace و Odoo

## نسخه ۷

- تبدیل میزکار کاربر عادی به مرکز فرمان شخصی
- Routeهای مستقل کارهای شخصی، تقویم، گفتگو، جست‌وجو، اعلان و تاریخچه
- سیستم Widget قابل جابه‌جایی
- تقویم تعاملی
- گفتگو به‌عنوان قابلیت سطح اول
- Theme و خوانایی سراسری
- Sidebar جمع‌شونده
- ارتفاع ثابت Widgetها و Scroll داخلی
- توسعه اثر ماژولی و Provider Registryها

مرجع: `06_ChangeSets/CS-WORKSPACE-V7.md`

## نسخه ۸

نسخه ۸ تکمیل عملیاتی سه صفحه و یک زیرساخت مشترک است:

### کارهای من

- تفکیک دسته‌های سیستمی و شخصی
- CRUD دسته‌های شخصی
- حذف امن دسته و انتقال Taskها
- کنترل مالکیت و ممنوعیت حذف دسته سیستمی در Backend

### تقویم

- بازطراحی Modal ساخت رویداد
- Selector مستقل شرکت‌کنندگان
- جست‌وجوی Server-side و مقیاس‌پذیر
- فیلتر واحد و محدوده سازمانی
- تفکیک دعوت‌نامه از تخصیص وظیفه
- محدودکردن Task به زیرمجموعه مجاز
- جمع‌بندی انتخاب‌ها با Chip
- Layering و Focus صحیح میان Modal و Selector

### گفت‌وگوها

- استفاده صریح از قابلیت‌های Mail/Discuss/Bus
- آیکن و آواتار استاندارد
- حذف Header و Search تکراری
- Floating Action گفت‌وگوی جدید
- فهرست فشرده گفتگو
- Composer ثابت و حذف Scroll کل صفحه
- Reply، Forward، Pin، Reaction، Delete مجاز، Mute و Archive
- Context Menu اختصاصی و Emoji Picker

### زیرساخت مشترک

- Overlay Manager
- Focus Trap و Focus Restore
- Scroll Lock
- Outside Click Contract
- Child Overlay روی Parent

مرجع: `06_ChangeSets/CS-WORKSPACE-V8.md`

## Iterationهای داخلی نسخه ۸

- `v8 iteration 1`: دسته‌ها، شرکت‌کنندگان اولیه و عملیات پیام
- `v8 iteration 2`: Scroll، Context Menu، Emoji و Rule تخصیص
- `v8 iteration 3`: Selector مقیاس‌پذیر شرکت‌کنندگان
- `v8 iteration 4`: رفع Layering و Focus

این Iterationها Release مستقل نیستند؛ مجموع آن‌ها نسخه رسمی Workspace v8 را تشکیل می‌دهد.

## قاعده نسخه‌بندی آینده

یک نسخه فقط زمانی Release رسمی محسوب می‌شود که:

1. خط مبنا و دامنه در این سند ثبت شود.
2. اسناد صفحه در `02_UI_UX` به‌روزرسانی شوند.
3. تصمیم‌های مشترک در `04_Decisions` ثبت شوند.
4. Change Set و ماتریس تجمیع به‌روزرسانی شوند.
5. اثر ماژولی و قرارداد معماری ثبت شود.
6. در صورت آماده‌بودن اجرا، Specification، Security، Migration و Test Strategy تصویب شوند.
