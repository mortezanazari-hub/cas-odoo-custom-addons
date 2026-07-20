# سند تصمیم صفحه جست‌وجوی سراسری سازمان

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-EMP-SEARCH-001` |
| خط مبنا | نسخه ۴ |
| نسخه هدف | نسخه ۷ |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Needs Review` |
| نقش‌ها | کاربران دارای `search.global` |

## تغییر نسبت به نسخه ۴

در نسخه ۴ فقط Action یا Modal جست‌وجوی عمومی وجود داشت و Route مستقل در Navigation تعریف نشده بود. نسخه ۷ Route مستقل `global-search-page`، Capability مستقل `search.global`، Command Launcher تمام‌عرض در Hero و دسترسی صفحه‌ای برای نتایج سازمانی اضافه کرده است.

## تصمیمات

- `PAGE-EMP-SEARCH-DEC-001`: جست‌وجوی سراسری یک قابلیت سطح اول Workspace است.
- `PAGE-EMP-SEARCH-DEC-002`: Command Launcher میزکار ورودی سریع همان سرویس Search است و صفحه کامل برای نتایج، فیلتر و مرور استفاده می‌شود.
- `PAGE-EMP-SEARCH-DEC-003`: جست‌وجو باید Route، فرم، اقدام، شخص، سند، مکاتبه، فرایند و رکوردهای مجاز را پوشش دهد.
- `PAGE-EMP-SEARCH-DEC-004`: هر Provider فقط فیلدهای Whitelist‌شده را جست‌وجو و Serialize می‌کند.
- `PAGE-EMP-SEARCH-DEC-005`: نتیجه‌ای که کاربر مجوز خواندن آن را ندارد نباید حتی به‌صورت عنوان یا شمارش افشا شود.
- `PAGE-EMP-SEARCH-DEC-006`: جست‌وجوی Navigation/Command با جست‌وجوی داده کسب‌وکاری تفکیک می‌شود ولی در UI یک تجربه واحد دارد.
- `PAGE-EMP-SEARCH-DEC-007`: تاریخ‌های شمسی در Query به بازه استاندارد Date/Datetime تبدیل می‌شوند.

## Providerهای موردنیاز

- Route و قابلیت‌های Workspace
- کارتابل و Action Hub
- Form Definition و Submission
- Workflow Definition و Instance
- Correspondence
- Document Core
- Employee/Organization Directory
- Attendance/Shift در محدوده مجاز
- Work Report در محدوده مجاز

## اثر ماژولی

| ماژول | اثر |
|---|---|
| `cas_workspace` | Route، Command UI، Provider Registry و Result Navigation |
| تمام ماژول‌های منبع | Search Adapter و Whitelist فیلدها |
| `cas_jalali_search` | Parse و تبدیل Queryهای تاریخ شمسی |
| Access Resolver | حذف Provider و نتیجه غیرمجاز |

## معیارهای پذیرش

- میانبر `Ctrl+K` و نوار Hero به یک سرویس متصل باشند.
- نتایج بر اساس نوع منبع گروه‌بندی شوند.
- نتیجه بدون مجوز نشت نکند.
- ماژول نصب‌نشده باعث Crash نشود.
- انتخاب نتیجه کاربر را به Route و رکورد صحیح ببرد.
