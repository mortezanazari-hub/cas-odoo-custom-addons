# DEC-016 — ادغام جست‌وجوی سازمانی و تاریخچه اخیر در Command Palette

| مشخصه | مقدار |
|---|---|
| وضعیت | `Agreed` |
| نسخه | `CAS UI Workspace v8` |
| دامنه | Search، Recent History، Navigation، Capability، Overlay |

## زمینه

در نسخه ۷ برای «جست‌وجوی سازمانی» و «تاریخچه اخیر» دو Route و صفحه مستقل تعریف شده بود. بررسی تجربه کاربری نسخه ۸ نشان داد هیچ‌کدام مقصد کاری مستقل نیستند؛ جست‌وجو ابزار عبور به رکورد و تاریخچه نیز ابزار بازگشت سریع است.

## تصمیم

1. Routeهای `global-search-page` و `recent-history` از Navigation و Router حذف می‌شوند.
2. جست‌وجوی سازمانی به‌صورت Modal/Command Palette مشترک ارائه می‌شود.
3. وقتی Query خالی است، همان Modal موارد اخیر، جست‌وجوهای اخیر و موارد سنجاق‌شده را نشان می‌دهد.
4. با شروع تایپ، History جای خود را به نتایج گروه‌بندی‌شده Search می‌دهد.
5. `Ctrl+K`، نوار جست‌وجوی Topbar و Launcher میزکار یک Overlay و یک سرویس مشترک را باز می‌کنند.
6. Recent History سرویس سبک داخل Workspace/Preference است و فعلاً ماژول مستقل `cas_recent_history` ایجاد نمی‌شود.
7. قابلیت مستقل `history.read` حذف می‌شود؛ نمایش هر مورد تابع دسترسی همان Resource است.

## قرارداد UX

- Autofocus روی ورودی جست‌وجو
- بستن با Escape، دکمه Close و Outside Click
- فیلتر تک‌انتخابی نوع نتیجه
- گروه‌بندی اشخاص، اقدامات، فرم‌ها، نامه‌ها، اسناد و فرایندها
- نمایش Loading، Empty، Error و Unavailable
- بازگشت Focus به Trigger پس از Close

## امنیت

- Provider فقط فیلدهای Whitelist‌شده را جست‌وجو و Serialize می‌کند.
- عنوان، Count یا Metadata رکورد غیرمجاز نباید افشا شود.
- Permission هنگام تولید نتیجه، نمایش Recent Item و بازکردن مجدد بررسی می‌شود.
- Recent History فقط Resource Reference و Snapshot حداقلی نگه می‌دارد.
- Routeها و رکوردهای حساس می‌توانند از ثبت History مستثنا شوند.

## اثر معماری

- `cas_workspace`: مالک Overlay، Search UI، History UI و Registry است؛ مالک رکورد منبع نیست.
- Providerهای منبع: Search Adapter و Safe Resource Reference ارائه می‌دهند.
- `cas_jalali_search`: Parse تاریخ شمسی را حفظ می‌کند.
- Access Resolver و Record Rule مرجع نهایی مجوز هستند.

## معیار پذیرش

- هیچ لینک یا Route مستقلی برای Search و Recent History وجود نداشته باشد.
- `Ctrl+K` و تمام Triggerها یک Modal واحد را باز کنند.
- Query خالی Recent Items و Query غیرخالی نتایج Search را نشان دهد.
- رکورد غیرمجاز در Search یا History نشت نکند.
- نبود Provider اختیاری باعث Crash Workspace نشود.
