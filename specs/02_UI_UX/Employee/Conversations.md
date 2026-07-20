# سند تصمیم صفحه گفت‌وگوها

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-EMP-CONV-001` |
| خط مبنا | نسخه ۴ |
| نسخه هدف | نسخه ۷ |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Needs Review` |
| نقش‌ها | همه کاربران دارای `discuss.use` |

## تغییر نسبت به نسخه ۴

نسخه ۴ قابلیت عمومی و Route سطح اول برای گفت‌وگو نداشت. نسخه ۷ Route مستقل `messages`، Capability مستقل `discuss.use`، Widget گفت‌وگوهای اخیر، دسترسی سریع Topbar، Drawer جزئیات و Composer پیام را اضافه کرده است. عنوان نمایشی «گفت‌وگوها» است و Route فنی `messages` برای سازگاری حفظ می‌شود.

## تصمیمات

- `PAGE-EMP-CONV-DEC-001`: گفت‌وگو یک قابلیت سطح اول Workspace است و در گروه «فضای کاری» قرار می‌گیرد.
- `PAGE-EMP-CONV-DEC-002`: گفت‌وگو از مکاتبات رسمی جداست؛ `cas_correspondence` مالک نامه رسمی و ارجاع است و گفت‌وگو ارتباط سریع سازمانی را پوشش می‌دهد.
- `PAGE-EMP-CONV-DEC-003`: دسترسی از Sidebar، Topbar و Widget میزکار فراهم است.
- `PAGE-EMP-CONV-DEC-004`: فهرست گفت‌وگو، پنل پیام و Composer ساختار اصلی صفحه‌اند.
- `PAGE-EMP-CONV-DEC-005`: اعضا، فایل‌ها و اطلاعات جانبی فقط هنگام درخواست در Drawer باز می‌شوند.
- `PAGE-EMP-CONV-DEC-006`: وضعیت خوانده‌نشده باید در Navigation، Topbar و فهرست همگام باشد.
- `PAGE-EMP-CONV-DEC-007`: اتصال Production باید از Mail/Discuss/Bus یا Adapter رسمی استفاده کند و Workspace مالک Message Record نشود.
- `PAGE-EMP-CONV-DEC-008`: جست‌وجوی داخل پیام‌ها از جست‌وجوی سراسری سازمان جداست.

## Actionهای نسخه ۷

`quick-conversations`، `open-home-conversation`، `open-drawer-conversation`، `select-conversation`، `send-chat-message`، `new-conversation`، `message-search`، `chat-info` و `chat-files`.

## اثر ماژولی

| ماژول/دامنه | اثر |
|---|---|
| `cas_workspace` | Route، Widget، Drawer، Topbar و State انتخاب گفتگو |
| Odoo Mail/Discuss/Bus | منبع واقعی Conversation، Message، Member و Unread |
| `cas_document_core` | فایل‌های پیوست و کنترل مجوز Download |
| `cas_correspondence` | مرزبندی روشن با مکاتبه رسمی |
| Notification Service | اعلان پیام جدید |

## قواعد امنیتی

- مشاهده گفتگو تابع عضویت و Record Rule است.
- فایل پیوست علاوه بر مجوز پیام، مجوز سند/Attachment را بررسی می‌کند.
- Frontend نباید با مخفی‌کردن گفتگو جایگزین کنترل سمت سرور شود.
- ارسال پیام باید Author واقعی Session را استفاده کند.

## معیارهای پذیرش

- گفت‌وگو در سه نقطه Sidebar، Topbar و میزکار در دسترس باشد.
- انتخاب گفتگو بدون Reload کامل انجام شود.
- Drawer جزئیات مزاحم فضای اصلی نباشد.
- شمارنده خوانده‌نشده میان نقاط مختلف همگام باشد.
- نبود Bus یا Mail Adapter به حالت `unavailable` کنترل‌شده منجر شود.
