# سند تصمیم صفحه گفت‌وگوها

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-EMP-CONV-001` |
| خط مبنا | نسخه ۴ |
| نسخه قبلی | نسخه ۷ |
| نسخه هدف | نسخه ۸ |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Needs Review` |
| وضعیت پیاده‌سازی | Prototype تأییدشده؛ اتصال Production به Mail/Discuss الزامی است |
| نقش‌ها | همه کاربران دارای `discuss.use` |

## هدف

ارائه پیام‌رسانی سازمانی سریع و یکپارچه در Workspace، با استفاده از قابلیت‌های واقعی Odoo Mail/Discuss/Bus و بدون ساخت مدل موازی پیام در `cas_workspace`.

## مرزبندی با مکاتبات

- گفت‌وگو برای ارتباط سریع، کانال، پیام، واکنش و فایل در متن گفتگو است.
- `cas_correspondence` مالک نامه رسمی، شماره، ثبت، ارجاع و سوابق مکاتبات است.
- آیکن و زبان بصری این دو حوزه نباید مشابه باشد.

## تغییرات نسخه ۸ نسبت به نسخه ۷

- جایگزینی آیکن نامه با نماد حباب گفت‌وگو
- اصلاح شکل و اندازه آواتارها
- حذف Header معرفی و توضیح بدیهی صفحه
- حذف جست‌وجوی تکراری کنار دکمه گفت‌وگوی جدید
- انتقال دکمه گفت‌وگوی جدید به Floating Action روی فهرست
- فشرده‌سازی ردیف‌های فهرست گفتگو
- محدودکردن Preview به یک خط
- حذف Scroll کل صفحه و ثابت‌ماندن Composer
- اضافه‌شدن Context Menu اختصاصی پیام و گفتگو
- Reply، Forward، Delete مجاز، Pin پیام و Pin گفتگو
- Mute و Archive گفتگو
- Emoji Reaction و Emoji Picker در Composer
- بسته‌شدن Menu/Picker با کلیک بیرون و Escape

## ساختار صفحه

1. فهرست گفتگوها
2. Search و فیلترهای همان فهرست
3. Floating Action «گفت‌وگوی جدید»
4. Header فشرده گفتگوی فعال
5. بدنه پیام‌ها
6. Composer ثابت
7. Drawer اطلاعات، اعضا و فایل‌ها
8. Context Menu و Emoji Picker

## فهرست گفتگوها

هر ردیف شامل:

- آواتار یا نشان کانال
- عنوان گفتگو
- Preview یک‌خطی آخرین پیام
- زمان آخرین فعالیت
- شمارنده خوانده‌نشده
- وضعیت Pin/Mute در صورت نیاز

قواعد:

- ارتفاع ردیف‌ها فشرده و ثابت باشد.
- متن بلند Ellipsis شود.
- فقط فهرست گفتگو Scroll بخورد.
- گفتگوی فعال به‌وضوح مشخص باشد.
- راست‌کلیک/منوی بیشتر عملیات مجاز همان گفتگو را نشان دهد.

## Header گفتگوی فعال

فقط اطلاعات عملیاتی نگه داشته می‌شود:

- نام گفتگو یا کانال
- وضعیت یا تعداد اعضا در صورت مفیدبودن
- دسترسی به Search داخل پیام‌ها
- فایل‌ها و اطلاعات گفتگو
- عملیات بیشتر

اطلاعات جانبی سنگین در Drawer قرار می‌گیرد. Breadcrumbها یا برچسب رکورد مرتبط فقط زمانی نمایش داده می‌شوند که برای Context عملیاتی لازم باشند.

## Scroll و Composer

- Body صفحه گفتگو نباید Scroll مستقل مرورگر ایجاد کند.
- فهرست گفتگو و بدنه پیام‌ها ناحیه Scroll کنترل‌شده دارند.
- Composer همیشه در پایین View گفتگو قابل مشاهده است.
- بازشدن Reply Preview یا Attachment نباید Composer را از Viewport خارج کند.
- در موبایل، ارتفاع صفحه با Visual Viewport و Keyboard هماهنگ می‌شود.

## Context Menu پیام

حداقل عملیات:

- پاسخ
- فوروارد
- کپی متن
- واکنش Emoji
- پین/برداشتن پین
- مشاهده اطلاعات پیام
- حذف، فقط برای پیام خود کاربر و در محدوده سیاست

قواعد:

- منوی مرورگر در محدوده پیام با منوی اختصاصی جایگزین می‌شود.
- کلیک بیرون، Escape، تغییر گفتگو یا بازشدن Menu دیگر آن را می‌بندد.
- Menu داخل Viewport Position می‌شود.
- عملیات غیرمجاز نمایش داده نمی‌شود.

## Context Menu گفتگو

حداقل عملیات:

- پین/برداشتن پین
- بی‌صدا/فعال‌کردن اعلان
- آرشیو
- علامت‌گذاری خوانده/خوانده‌نشده
- مشاهده اعضا و اطلاعات
- ترک کانال در صورت مجازبودن

حذف Conversation عملیات عمومی نیست و فقط مطابق سیاست واقعی Discuss مجاز است.

## Reply

- انتخاب Reply، Preview پیام مرجع را بالای Composer نشان می‌دهد.
- کاربر می‌تواند Reply را لغو کند.
- پیام نهایی مرجع Reply را حفظ می‌کند.
- کلیک روی Preview پیام مرجع، در صورت مجازبودن، به پیام اصلی Scroll می‌کند.

## Forward

- مقصد از Conversation/Partnerهای قابل دسترس انتخاب می‌شود.
- Forward نباید مجوز متن، فایل یا رکورد مرتبط را دور بزند.
- منبع پیام در Forward قابل ردیابی است.

## Pin

- Pin پیام باید Scope و Permission روشن داشته باشد.
- Pin گفتگو می‌تواند Preference کاربر یا Channel State باشد؛ تصمیم نهایی در Integration Spec مشخص می‌شود.
- پیام‌های Pinشده از Header/Drawer قابل دسترسی‌اند.

## Emoji Reaction و Picker

- Reaction Picker از Context Menu یا دکمه پیام باز می‌شود.
- Composer Picker Emoji را در محل Cursor درج می‌کند.
- Picker با کلیک بیرون و Escape بسته می‌شود.
- Keyboard Navigation، Focus و `aria-label` الزامی است.
- Reaction به مدل استاندارد Mail/Discuss یا Extension سازگار متصل می‌شود.

## تصمیمات قطعی

- `PAGE-EMP-CONV-DEC-001`: گفت‌وگو قابلیت سطح اول Workspace است.
- `PAGE-EMP-CONV-DEC-002`: گفت‌وگو از مکاتبه رسمی جداست.
- `PAGE-EMP-CONV-DEC-003`: دسترسی از Sidebar، Topbar و Widget فراهم است.
- `PAGE-EMP-CONV-DEC-004`: فهرست، پیام‌ها و Composer ساختار اصلی‌اند.
- `PAGE-EMP-CONV-DEC-005`: اطلاعات جانبی در Drawer است.
- `PAGE-EMP-CONV-DEC-006`: Unread در همه نقاط همگام است.
- `PAGE-EMP-CONV-DEC-007`: Workspace مالک Message نیست.
- `PAGE-EMP-CONV-DEC-008`: Search پیام از Global Search جداست.
- `PAGE-EMP-CONV-DEC-009`: از قابلیت‌های استاندارد Mail/Discuss/Bus استفاده می‌شود.
- `PAGE-EMP-CONV-DEC-010`: Composer همیشه در دسترس باقی می‌ماند.
- `PAGE-EMP-CONV-DEC-011`: Context Menu اختصاصی جایگزین منوی مرورگر می‌شود.
- `PAGE-EMP-CONV-DEC-012`: Reply، Forward، Pin و Reaction جزو رفتار پایه هستند.
- `PAGE-EMP-CONV-DEC-013`: Menu و Picker با Outside Click و Escape بسته می‌شوند.

## امنیت

- مشاهده Conversation تابع Membership و Record Rule است.
- ارسال پیام Author واقعی Session را استفاده می‌کند.
- Delete تابع مالکیت، زمان و سیاست سازمان است.
- Forward دسترسی مقصد و Attachment را دوباره بررسی می‌کند.
- Pin/Mute/Archive Scope روشن کاربر یا کانال دارند.
- Download فایل علاوه بر پیام، مجوز Attachment/Document را بررسی می‌کند.
- Frontend جایگزین ACL و Method Check نیست.

## اثر ماژولی

| ماژول/دامنه | اثر |
|---|---|
| `cas_workspace` | Route، Layout، Floating Action، Context Menu، Overlay و Adapter |
| Odoo Mail/Discuss/Bus | مالک Conversation، Message، Member، Reaction و Realtime |
| `cas_document_core` | Permission فایل‌های مرتبط در صورت استفاده |
| `cas_correspondence` | مرزبندی با نامه رسمی و Context Link |
| Notification Core | اعلان پیام جدید و Mute Policy |

## معیارهای پذیرش

- Composer در تمام زمان‌ها قابل مشاهده باشد.
- کل صفحه Scroll نخورد.
- فهرست گفتگو تراکم مناسب داشته باشد.
- Context Menu با کلیک بیرون و Escape بسته شود.
- Emoji Picker در پیام و Composer کار کند.
- Reply، Forward، Pin و Reaction به رکورد واقعی متصل شوند.
- حذف فقط برای پیام مجاز نمایش داده شود.
- Unread میان Sidebar، Topbar و فهرست همگام بماند.
- نبود Bus به حالت کنترل‌شده منجر شود.

## تست‌های ضروری

- کلیک بیرون Context Menu و Picker
- Escape و Focus Restore
- Composer در ارتفاع‌های مختلف
- Keyboard باز در موبایل
- ردیف‌های طولانی و عنوان‌های طولانی
- گفتگوهای Pin/Mute/Archive
- Attachment غیرمجاز
- Forward به مقصد غیرمجاز
- Realtime قطع و وصل
- RTL، Zoom و Responsive

## اسناد مرتبط

- `04_Decisions/DEC-014-Discuss-Reuse-And-Message-Interaction.md`
- `04_Decisions/DEC-015-Overlay-Layering-And-Focus-Management.md`
- `05_Architecture/V8-Interaction-And-Integration-Contracts.md`
- `03_Modules/V8_Impact_Assessment.md`
- `06_ChangeSets/CS-WORKSPACE-V8.md`
