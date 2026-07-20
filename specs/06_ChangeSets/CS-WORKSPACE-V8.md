# Change Set جامع — CAS UI Workspace v8

| مشخصه | مقدار |
|---|---|
| شناسه | `CS-WORKSPACE-V8` |
| خط مبنا | `CAS UI Workspace v7` |
| نسخه هدف | `CAS UI Workspace v8` |
| Prototype نهایی این مرحله | `ui-workspace-v8-iteration11.zip` |
| وضعیت | `Collected` |
| مجوز Production | ندارد تا Specificationها تصویب شوند |

## دامنه نسخه ۸

نسخه ۸ این حوزه‌ها را تکمیل کرده است:

1. حاکمیت دسته‌های کار شخصی
2. Selector مقیاس‌پذیر شرکت‌کنندگان تقویم
3. تفکیک دعوت از تخصیص وظیفه
4. تجربه عملیاتی گفتگو بر پایه Mail/Discuss
5. Overlay Stack و Focus Management
6. حذف صفحات مستقل Search و Recent History
7. Command Palette مشترک Search/History
8. اصلاح تراکم ردیف گفتگو و جهت تقویم RTL
9. چیپ تک‌انتخابی منبع در «نیازمند اقدام»
10. قرارداد Scroll بومی Workspace و Scroll داخلی گفتگو
11. بازشدن گفتگو از آخرین پیام

## تاریخچه Iterationها

- Iteration 1–4: دسته‌ها، شرکت‌کنندگان، Discuss Interaction و اصلاح Layering
- Iteration 5: فشرده‌سازی ردیف گفتگو و اصلاح فلش ماه قبل/بعد در RTL
- Iteration 6: تبدیل فیلتر منبع Action Hub به چیپ تک‌انتخابی
- Iteration 7: حذف صفحات مستقل Search/History و ایجاد Command Palette
- Iteration 8: بازگرداندن Scroll بومی و Auto-scroll دکمه وسط موس در Routeهای عادی
- Iteration 9: محدودکردن Scroll صفحه گفتگو به List و Message Body
- Iteration 10: افزایش داده نمونه برای آزمون Scroll طولانی
- Iteration 11: شروع گفتگو از آخرین پیام و حفظ انتهای چت پس از Send

## کارهای شخصی

- دسته‌های سیستمی قفل هستند.
- دسته‌های شخصی CRUD و ترتیب دارند.
- حذف دسته Taskها را حذف نمی‌کند و انتقال اتمیک انجام می‌شود.
- مالکیت پیشنهادی در `cas_personal_task` هنوز نیازمند Specification است.

## تقویم

- فهرست کامل کارکنان داخل Modal ممنوع است.
- Selector مستقل با Search Server-side، Scope، Department و Pagination استفاده می‌شود.
- دعوت و Task دو Operation مستقل هستند.
- Task فقط برای Target مجاز طبق Hierarchy/Delegation ساخته می‌شود.
- Selector به‌عنوان Child Overlay بالاتر از Modal باز می‌شود.
- جهت کنترل ماه در RTL براساس مفهوم «ماه قبل/بعد» است، نه جهت خام آیکن.

## گفتگوها

- ردیف‌ها فشرده و Preview یک‌خطی هستند.
- Header و Composer ثابت‌اند.
- Route گفت‌وگو Scroll کلی ندارد.
- فقط List و Message Body اسکرول مستقل دارند.
- هر دو ناحیه Wheel، Scrollbar، Keyboard، Touch و Auto-scroll دکمه وسط موس را پشتیبانی می‌کنند.
- ورود و تغییر گفتگو از آخرین پیام آغاز می‌شود.
- ارسال پیام جدید انتهای چت را حفظ می‌کند.
- Reply، Forward، Reaction، Pin، Mute و Archive از Discuss Adapter استفاده می‌کنند.

## Search و Recent History

- Routeهای `global-search-page` و `recent-history` حذف شده‌اند.
- هر دو Navigation Item حذف شده‌اند.
- Search از Topbar، Hero و `Ctrl+K` در Command Palette باز می‌شود.
- Query خالی Recent Items، Searchهای اخیر و Pinها را نشان می‌دهد.
- Query غیرخالی نتایج گروه‌بندی‌شده و فیلتر نوع نتیجه را نشان می‌دهد.
- `history.read` به‌عنوان Capability مستقل حذف می‌شود؛ Resource Permission مرجع است.
- ماژول مستقل `cas_recent_history` فعلاً ساخته نمی‌شود.

## Action Hub

- فیلتر زمانی تک‌انتخابی باقی می‌ماند.
- فیلتر منبع از Dropdown به چیپ تک‌انتخابی تبدیل شده است.
- انتخاب منبع جدید، منبع قبلی را غیرفعال می‌کند.
- Sort همچنان Dropdown مستقل است.

## قرارداد Scroll سراسری

- Routeهای عادی Workspace باید Scroll Container بومی مرورگر داشته باشند.
- اعمال `overflow:hidden` سراسری روی `html`، `body` یا `.main-content` ممنوع است.
- Scroll Lock فقط هنگام Overlay لازم و با Scope روشن مجاز است.
- Routeهای خاص مانند گفتگو می‌توانند Scroll داخلی داشته باشند، اما نباید Scroll سایر صفحات را مختل کنند.

## ماژول‌ها و زیرساخت‌های متأثر

| دامنه | اثر |
|---|---|
| `cas_workspace` | Router، Navigation، Command Palette، History UI، Overlay، Scroll Contract، Conversation Layout |
| `cas_action_hub` | فیلتر منبع تک‌انتخابی و State |
| Mail/Discuss/Bus | Message، Conversation، Pagination، Realtime و تعاملات |
| Search Provider Registry | Query امن چندمنبعی |
| Preference/History Service | Recent Resource Reference و Search History |
| HR Directory/Hierarchy | Attendee Search و Assignment Scope |
| Calendar/Event | Event، Invitation، RSVP و Task Link |
| Jalali Suite | ورودی تاریخ و جهت/معنای ناوبری ماه |

## امنیت

- بدون `sudo()` برای Query کاربرمحور
- ACL، Record Rule، Company Scope و Method Check در Backend
- عدم افشای عنوان و Count در Search/History
- جلوگیری از ID Tampering در Task Assignment
- Permission مستقل Attachment و Forward
- Workspace مالک داده کسب‌وکاری Providerها نیست

## تست‌های Regression

- نبود دو Route حذف‌شده در Router/Sidebar
- بازشدن Command Palette از تمام Triggerها و `Ctrl+K`
- Query خالی و غیرخالی Search
- عدم نشت رکورد غیرمجاز در Search/History
- Auto-scroll دکمه وسط موس در صفحات عادی
- نبود Scroll کلی در گفتگو
- Scroll مستقل List و Message Body
- شروع گفتگو از آخرین پیام
- حفظ انتهای چت پس از Send
- حفظ Anchor هنگام Load پیام قدیمی در Production
- Modal + Child Drawer + Escape + Focus Restore
- RTL ماه قبل/بعد
- چیپ منبع تک‌انتخابی Action Hub

## شرط `Implementation Ready`

1. تصویب مالکیت Personal Task
2. تعیین Search Provider API و Safe Serializer
3. تعیین History Storage و Retention
4. تطبیق Discuss Adapter با Odoo 19 Community
5. تصویب Scroll/Overlay Accessibility Contract
6. تعیین Event/Invitation/Task Transaction Policy
7. تدوین Security، Migration، Performance و Test Strategy هر ماژول
