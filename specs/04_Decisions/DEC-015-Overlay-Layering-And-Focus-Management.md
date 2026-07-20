# DEC-015 — قرارداد لایه‌بندی Overlay و مدیریت Focus

| مشخصه | مقدار |
|---|---|
| وضعیت | `Agreed` |
| نسخه | `CAS UI Workspace v8` |
| دامنه | Modal / Drawer / Popover / Context Menu / Accessibility |
| صفحات مرتبط | Calendar، Conversations و تمام صفحات Workspace |

## مسئله

در Prototype نسخه ۸، Selector شرکت‌کنندگان از طریق Drawer باز می‌شد، اما به‌دلیل `z-index` برابر و ترتیب DOM پشت Modal اصلی قرار گرفت. این خطا نشان داد لایه‌بندی Overlay نباید موردی و صفحه‌محور باشد.

## تصمیم

`cas_workspace` باید یک Overlay Manager مشترک داشته باشد و Modal، Drawer، Popover، Context Menu، Tooltip و Toast را با Stack صریح مدیریت کند.

## ترتیب پیشنهادی لایه‌ها

اعداد دقیق جزو API عمومی نیستند، اما ترتیب نسبی باید ثابت باشد:

1. محتوای صفحه
2. Sticky Header/Footer
3. Dropdown و Popover عادی
4. Modal و Backdrop
5. Drawer فرزند Modal یا Overlay فعال ثانویه
6. Context Menu و Emoji Picker مرتبط با Overlay فعال
7. Tooltip
8. Toast و پیام بحرانی

هر Overlay جدید باید نسبت به Parent خود Layer بالاتری بگیرد، نه اینکه صرفاً یک مقدار ثابت جهانی داشته باشد.

## قواعد تعامل

- فقط بالاترین Overlay قابل تعامل است.
- Background و Overlayهای زیرین باید Inert یا معادل آن باشند.
- Escape فقط بالاترین Overlay قابل‌بستن را می‌بندد.
- کلیک Backdrop فقط طبق سیاست همان Overlay عمل می‌کند.
- بستن Overlay فرزند نباید Parent را ببندد مگر اینکه Flow صریح چنین بخواهد.
- State فرم Parent هنگام بازشدن Child حفظ می‌شود.

## مدیریت Focus

- هنگام بازشدن، Focus به اولین کنترل معنادار یا عنوان قابل Focus منتقل می‌شود.
- Focus داخل Overlay فعال Trap می‌شود.
- پس از بسته‌شدن، Focus به Trigger قبلی بازمی‌گردد.
- اگر Trigger دیگر وجود نداشت، Focus به نزدیک‌ترین Container معنادار منتقل می‌شود.
- ترتیب Tab در RTL همچنان منطقی و مطابق ساختار DOM است.

## Scroll Lock

- هنگام بازشدن Modal، Scroll بدنه صفحه قفل می‌شود.
- ناحیه محتوای Modal می‌تواند Scroll کنترل‌شده داشته باشد؛ Header و Footer ثابت می‌مانند.
- Overlay فرزند نباید Scroll Parent را ناخواسته فعال کند.
- Scroll تودرتوی غیرضروری ممنوع است.

## کاربرد در تقویم

Selector شرکت‌کنندگان Child Overlay از Modal رویداد است. باید روی Modal نمایش داده شود، Modal زیرین Inert بماند، و پس از تأیید یا انصراف، Modal اصلی با State قبلی فعال شود.

## کاربرد در گفتگو

Context Menu و Emoji Picker باید روی صفحه گفتگو و داخل Viewport نمایش داده شوند، با کلیک بیرون یا Escape بسته شوند و Composer یا انتخاب پیام را تخریب نکنند.

## تست‌های الزامی

- Modal روی صفحه
- Drawer روی Modal
- Emoji Picker روی Composer داخل صفحه ثابت
- Context Menu نزدیک لبه‌های Viewport
- Escape در Stack چندلایه
- بازگشت Focus
- Screen Reader و `aria-modal`
- Scroll Lock در Desktop و Mobile
- RTL و Zoom مرورگر

## پیامد معماری

زیرساخت Overlay باید در `cas_workspace` یا Design System مشترک قرار گیرد. هر صفحه نباید `z-index` مستقل و ناسازگار تعریف کند.
