# سند تصمیم صفحه گفت‌وگوها

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-EMP-CONV-001` |
| نسخه هدف | `CAS UI Workspace v8` |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Needs Review` |
| وضعیت Prototype | Iteration 11 تأییدشده |
| نقش‌ها | کاربران دارای `discuss.use` |

## هدف

ارائه پیام‌رسانی سازمانی سریع در Workspace با استفاده از Odoo Mail/Discuss/Bus و بدون ساخت مدل موازی Conversation یا Message در `cas_workspace`.

## مرزبندی

- گفتگو برای پیام سریع، کانال، واکنش، فایل و هماهنگی روزمره است.
- `cas_correspondence` مالک نامه رسمی، شماره، ثبت، ارجاع و سوابق مکاتبات است.
- Search داخل پیام‌ها مستقل از Search سراسری سازمان است.

## ساختار صفحه

1. فهرست فشرده گفتگوها
2. Search و فیلتر همان فهرست
3. Floating Action گفت‌وگوی جدید
4. Header گفت‌وگوی فعال
5. بدنه پیام‌ها
6. Composer ثابت
7. Drawer اطلاعات، اعضا و فایل‌ها
8. Context Menu و Emoji Picker

## فهرست گفتگوها

هر ردیف شامل آواتار، عنوان، Preview یک‌خطی، زمان، Unread و وضعیت Pin/Mute است.

قواعد:

- ارتفاع ردیف‌ها فشرده و ثابت است.
- ردیف‌ها برای پرکردن ارتفاع پنل کشیده نمی‌شوند.
- متن بلند Ellipsis می‌شود.
- فقط خود فهرست Scroll مستقل دارد.
- گفت‌وگوی فعال واضح است.

## قرارداد Scroll صفحه

- خود Route گفت‌وگو Scroll کلی ندارد.
- Header صفحه، Header گفت‌وگوی فعال و Composer خارج از ناحیه Scroll باقی می‌مانند.
- فقط دو ناحیه Scroll مجازند:
  1. فهرست گفتگوها
  2. بدنه پیام‌های گفت‌وگوی فعال
- هر دو ناحیه باید Wheel، Scrollbar، Keyboard، Touch و Auto-scroll دکمه وسط موس را پشتیبانی کنند.
- برای Flex/Grid Containers استفاده از `min-height:0` الزامی است.
- قفل `overflow:hidden` نباید به `.main-content` یا سایر Routeها به‌صورت سراسری اعمال شود.
- سایر صفحات Workspace باید Scroll بومی مرورگر و Auto-scroll را حفظ کنند.

## موقعیت اولیه و رفتار انتهای چت

- هنگام ورود به صفحه، گفت‌وگوی فعال از آخرین پیام باز می‌شود.
- هنگام تغییر گفت‌وگوی فعال، پس از Render پیام‌ها Scroll به انتهای همان گفتگو منتقل می‌شود.
- پس از ارسال پیام جدید، پنل پیام‌ها در انتهای چت باقی می‌ماند.
- اگر کاربر برای مطالعه تاریخچه به بالا Scroll کرده باشد، دریافت پیام جدید نباید او را بدون قاعده به پایین بپراند؛ در Production باید Near-bottom Threshold و نشان «پیام جدید» تعریف شود.
- بارگذاری پیام‌های قدیمی‌تر باید با حفظ Anchor بصری انجام شود تا موقعیت کاربر نپرد.

## Composer

- Composer همیشه در پایین پنل قابل مشاهده است.
- Reply Preview، Attachment و Emoji Picker نباید آن را از Viewport خارج کنند.
- در موبایل ارتفاع با Visual Viewport و Keyboard هماهنگ می‌شود.

## تعامل پیام

عملیات پایه:

- Reply
- Forward
- Copy
- Reaction
- Pin/Unpin
- Message Info
- Delete Own Message در صورت مجازبودن

Context Menu و Picker با Outside Click، Escape، تغییر Route یا تغییر گفت‌وگو بسته می‌شوند و داخل Viewport Position می‌شوند.

## تعامل گفتگو

- Pin/Unpin
- Mute/Unmute
- Archive/Unarchive
- Mark Read/Unread
- Members/Info
- Leave Channel در صورت مجازبودن

## امنیت

- مشاهده Conversation تابع Membership و Record Rule است.
- ارسال پیام با Author واقعی Session انجام می‌شود.
- Delete تابع مالکیت و سیاست سازمان است.
- Forward مجوز مقصد، متن و Attachment را دوباره بررسی می‌کند.
- فایل‌ها تابع Permission پیام و Attachment/Document هستند.
- Frontend جایگزین ACL و Method Check نیست.

## تصمیمات قطعی

- `PAGE-EMP-CONV-DEC-001..009`: مرزبندی، Route، Discuss Reuse و Unread Sync.
- `PAGE-EMP-CONV-DEC-010`: Composer همیشه در دسترس است.
- `PAGE-EMP-CONV-DEC-011`: Context Menu اختصاصی برای پیام و گفتگو وجود دارد.
- `PAGE-EMP-CONV-DEC-012`: Reply، Forward، Pin و Reaction رفتار پایه‌اند.
- `PAGE-EMP-CONV-DEC-013`: Menu و Picker قرارداد Overlay مشترک را رعایت می‌کنند.
- `PAGE-EMP-CONV-DEC-014`: Route گفت‌وگو Scroll کلی ندارد و فقط List و Message Body اسکرول می‌شوند.
- `PAGE-EMP-CONV-DEC-015`: بازشدن گفتگو و ارسال پیام، موقعیت انتهای چت را مدیریت می‌کند.
- `PAGE-EMP-CONV-DEC-016`: قفل Scroll صفحه گفتگو نباید Scroll بومی سایر Routeها را غیرفعال کند.

## اثر ماژولی

| ماژول/دامنه | اثر |
|---|---|
| `cas_workspace` | Layout، Scroll Contract، Initial Position، Context Menu، Overlay و Adapter |
| Odoo Mail/Discuss/Bus | مالک Conversation، Message، Member، Reaction، Pagination و Realtime |
| `cas_document_core` | Permission فایل‌های مرتبط |
| `cas_correspondence` | مرزبندی با نامه رسمی |
| Notification Core | اعلان پیام جدید و Mute Policy |

## معیارهای پذیرش

- کل Route گفت‌وگو Scroll نخورد.
- فهرست و پیام‌ها Scroll و Auto-scroll مستقل داشته باشند.
- سایر Routeها Auto-scroll بومی مرورگر را حفظ کنند.
- ورود و تغییر گفتگو آخرین پیام را نمایش دهد.
- ارسال پیام جدید انتهای چت را حفظ کند.
- Header و Composer ثابت بمانند.
- Context Menu و Emoji Picker با Keyboard و Outside Click کار کنند.
- نبود Bus به حالت `unavailable` کنترل‌شده منجر شود.
