# سند تصمیم جست‌وجوی سراسری سازمان

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-EMP-SEARCH-001` |
| نسخه هدف | `CAS UI Workspace v8` |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Needs Review` |
| نوع تجربه | Modal / Command Palette؛ بدون صفحه مستقل |

## تصمیم نهایی نسخه ۸

صفحه و Route مستقل `global-search-page` حذف می‌شود. جست‌وجوی سازمانی یک ابزار عبور سریع است و از Topbar، Launcher میزکار، آیکن موبایل و میانبر `Ctrl+K` در یک Modal مشترک باز می‌شود.

## ساختار Modal

1. Header فشرده با عنوان، راهنمای میانبر و Close
2. ورودی Autofocus با Debounce و امکان لغو Request قبلی
3. چیپ‌های تک‌انتخابی نوع نتیجه
4. بدنه نتایج گروه‌بندی‌شده
5. Recent Items در حالت Query خالی
6. Loading، Empty، Error و Unavailable State

## حالت خالی جست‌وجو

تا پیش از تایپ کاربر، Modal می‌تواند این موارد را نمایش دهد:

- اخیراً مشاهده‌شده‌ها
- جست‌وجوهای اخیر
- موارد سنجاق‌شده
- عملیات پرتکرار مجاز

با شروع تایپ، این محتوا با نتایج جست‌وجو جایگزین می‌شود.

## دامنه نتایج

- اشخاص و ساختار سازمانی
- اقدام‌های نیازمند انجام
- فرم و Submission
- Workflow و Approval
- مکاتبات
- اسناد
- Routeها و عملیات مجاز Workspace
- رکوردهای سایر Providerهای نصب‌شده

## رفتار تعامل

- `Ctrl+K` Modal را باز می‌کند.
- Escape، Close و Outside Click آن را می‌بندند.
- Focus پس از Close به Trigger برمی‌گردد.
- انتخاب نتیجه Modal را می‌بندد و Deep Link صحیح را باز می‌کند.
- فیلتر نوع نتیجه تک‌انتخابی است.
- در موبایل Modal به Sheet تمام‌عرض کنترل‌شده تبدیل می‌شود.

## قرارداد داده و Performance

- Search به‌صورت Server-side انجام می‌شود.
- هر Provider حداقل سه نویسه یا سیاست مخصوص خود را اعمال می‌کند.
- Queryها Debounce و Request قبلی Cancel می‌شوند.
- نتایج Limit و Pagination/Cursor دارند.
- Providerهای اختیاری در نبود ماژول، `unavailable` کنترل‌شده برمی‌گردانند.

## امنیت

- هر Provider فقط فیلدهای Whitelist‌شده را جست‌وجو و Serialize می‌کند.
- ACL، Record Rule، Company Scope و Method Permission در Backend اعمال می‌شوند.
- عنوان، Count یا Metadata رکورد غیرمجاز نباید افشا شود.
- UI جایگزین Permission Check نیست.

## اثر ماژولی

| ماژول/دامنه | اثر |
|---|---|
| `cas_workspace` | Command Palette، Overlay، Provider Registry، State و Result Navigation |
| ماژول‌های منبع | Search Adapter و Safe Serializer |
| `cas_jalali_search` | Parse تاریخ شمسی و تبدیل به Date/Datetime استاندارد |
| Access Resolver | کنترل Provider و نتیجه مجاز |

## تصمیمات

- `PAGE-EMP-SEARCH-DEC-001`: Search قابلیت مشترک Workspace است، نه Route سطح اول.
- `PAGE-EMP-SEARCH-DEC-002`: صفحه مستقل و Navigation Item حذف می‌شوند.
- `PAGE-EMP-SEARCH-DEC-003`: همه Triggerها یک Modal و یک Service را استفاده می‌کنند.
- `PAGE-EMP-SEARCH-DEC-004`: Query خالی Recent Items را نشان می‌دهد.
- `PAGE-EMP-SEARCH-DEC-005`: Provider Whitelist و عدم نشت نتیجه الزامی است.
- `PAGE-EMP-SEARCH-DEC-006`: Search داده و Command Navigation در UI یک تجربه دارند ولی قرارداد Backend جدا دارند.
- `PAGE-EMP-SEARCH-DEC-007`: ورودی تاریخ شمسی بدون تغییر ذخیره استاندارد Parse می‌شود.

## معیارهای پذیرش

- `global-search-page` در Router و Navigation وجود نداشته باشد.
- `Ctrl+K` و Triggerهای UI یک Modal مشترک را باز کنند.
- Recent Items فقط در Query خالی دیده شوند.
- نتایج گروه‌بندی و فیلترپذیر باشند.
- هیچ داده غیرمجاز نشت نکند.
- Focus و Keyboard Navigation کامل باشند.
