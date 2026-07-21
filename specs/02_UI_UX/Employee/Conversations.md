# Page Specification — گفت‌وگوها

| مشخصه | مقدار |
|---|---|
| شناسه | `PAGE-EMP-CONV-001` |
| نسخه هدف | `CAS UI Workspace v8 — Through Iteration 12` |
| وضعیت محصول | `Agreed` |
| وضعیت معماری | `Consolidated / Needs Odoo 19 Verification` |
| وضعیت Prototype | Iteration 11 تأییدشده |
| Capability | `conversation.use` |
| مالک داده | Odoo Mail/Discuss/Bus |
| مالک تجربه Workspace | `cas_workspace` و Discuss Adapter |

## هدف

ارائه ارتباط سازمانی سریع در Workspace با Reuse زیرساخت Odoo Mail/Discuss/Bus و بدون ساخت مدل موازی Conversation، Message، Thread یا Realtime Bus.

## مرزبندی

- Conversation برای هماهنگی روزمره، پیام، Channel، Reaction و Attachment است.
- Correspondence رسمی، شماره‌گذاری، ثبت و ارجاع متعلق به Domain مکاتبات است.
- Search داخل Conversation با Search سراسری Workspace متفاوت است.
- Notification پیام جدید از زیرساخت Odoo استفاده می‌کند؛ CAS فقط View و Metadata لازم را Extend می‌کند.

## ساختار صفحه

1. فهرست فشرده Conversationها
2. Search و Filter همان فهرست
3. Floating Action برای Conversation جدید
4. Header Conversation فعال
5. Message Body
6. Composer پایدار
7. Drawer اعضا، اطلاعات و فایل‌ها
8. Context Menu و Emoji Picker

## فهرست Conversationها

هر ردیف شامل:

- Avatar
- عنوان
- Preview یک‌خطی
- زمان
- Unread
- Pin/Mute/Archive State، در صورت پشتیبانی

قواعد:

- ردیف‌ها فشرده و با ارتفاع پایدارند.
- متن بلند Ellipsis می‌شود.
- فقط List Scroll مستقل دارد.
- Conversation فعال واضح است.
- List براساس Membership و Permission ساخته می‌شود.

## Scroll Contract

- Route گفتگو Scroll کلی ندارد.
- Conversation List و Message Body دو Scroll Container مستقل‌اند.
- Headerها و Composer خارج از Message Scroll باقی می‌مانند.
- Wheel، Scrollbar، Keyboard، Touch و Auto-scroll در Containerها کار می‌کنند.
- Flex/Grid Chain از `min-height: 0` استفاده می‌کند.
- Scroll Lock Route گفتگو نباید Scroll سایر Routeهای Workspace را غیرفعال کند.

## موقعیت اولیه و انتهای Chat

- ورود و تغییر Conversation از آخرین پیام آغاز می‌شود.
- پس از Send، اگر کاربر Near-bottom است انتها حفظ می‌شود.
- اگر کاربر برای مطالعه تاریخچه بالا رفته باشد، پیام جدید او را اجباری پایین نمی‌برد.
- New Message Indicator در حالت دور از انتها نمایش داده می‌شود.
- Load Older Messages باید Anchor بصری را حفظ کند.

## Composer

- همیشه در پایین پنل قابل دسترسی است.
- Reply Preview، Attachment و Emoji Picker آن را از Viewport خارج نمی‌کنند.
- در Mobile با Visual Viewport و Keyboard هماهنگ است.
- ارسال تکراری ناشی از Retry کنترل می‌شود.

## عملیات Message

قابلیت‌های استاندارد Odoo ابتدا Reuse می‌شوند:

- Send
- Reply
- Copy
- Reaction
- Mark Read/Unread
- Edit/Delete Own Message، مطابق Permission

قابلیت‌های زیر فقط پس از Verification Odoo 19 Community و Gap Analysis فعال یا Extend می‌شوند:

- Forward
- Pin/Unpin Message
- Message Info توسعه‌یافته
- Attachment Forward Policy

## عملیات Conversation

- Pin/Unpin Preference
- Mute/Unmute
- Archive/Unarchive
- Mark Read/Unread
- Members/Info
- Leave Channel، در صورت Permission

هر Operation باید از API واقعی Odoo یا Extension مستند و آزمون‌شده استفاده کند.

## Overlay و Focus

Context Menu، Emoji Picker و Drawer از Odoo UI Services و Workspace Overlay Policy استفاده می‌کنند:

- Outside Click
- Escape
- Focus Restore
- Route/Conversation Change Cleanup
- Position داخل Viewport
- Keyboard Navigation

## Attachment و Document

- Attachment ساده Mail لزوماً Document Core نیست.
- فایل تابع Permission Message/Thread و Attachment است.
- Document-linked Attachment باید Permission Document را نیز رعایت کند.
- Metadata فایل غیرمجاز نباید افشا شود.
- بازطراحی بنیادی Document Infrastructure خارج از v8 است.

## Notification و Realtime

- Bus استاندارد Odoo برای Realtime Reuse می‌شود.
- نبود Bus صفحه را از کار نمی‌اندازد؛ Fetch/Polling کنترل‌شده ممکن است.
- Notification Delivery موازی ساخته نمی‌شود.
- Badge و Unread باید Permission-aware و همگام باشند.

## امنیت

- Read تابع Membership، ACL و Record Rule است.
- Author از Session معتبر گرفته می‌شود.
- Client نمی‌تواند Author یا Membership را تحمیل کند.
- Delete/Edit تابع Ownership و Policy است.
- Forward مقصد، متن و Attachment را دوباره بررسی می‌کند.
- Search داخل Conversation داده Channel غیرمجاز را افشا نمی‌کند.
- broad `sudo` ممنوع است.

## Odoo Verification لازم

قبل از Implementation Ready شدن باید روی Odoo 19 Community بررسی شود:

- API و UI Message Pagination
- Reaction
- Reply Reference
- Pin
- Forward
- Archive/Mute Preference
- Edit/Delete Policy
- Read/Unread Sync
- Bus Reconnect
- Attachment Permission

قابلیت استاندارد موجود دوباره مدل‌سازی نمی‌شود.

## Stateها

- Loading
- Empty Conversation List
- No Active Conversation
- Ready
- Bus/Reatime Unavailable
- Attachment Forbidden
- Partial Feature Unavailable
- Error

## معیار پذیرش

1. هیچ مدل موازی Conversation/Message/Bus ساخته نشود.
2. Route Scroll کلی نداشته باشد.
3. List و Message Body Scroll مستقل داشته باشند.
4. Initial Bottom، Send Anchoring و Load Older Anchor صحیح باشند.
5. نبود Bus صفحه را غیرقابل استفاده نکند.
6. عملیات فاقد پشتیبانی Odoo بدون Gap Extension فعال نشوند.
7. Attachment و Membership Permission در Backend اعمال شوند.
8. Context Menu، Focus، Keyboard، RTL و Mobile صحیح باشند.

## اسناد مرتبط

- `../../04_Decisions/DEC-014-Discuss-Reuse-And-Message-Interaction.md`
- `../../05_Architecture/V8-Interaction-And-Integration-Contracts.md`
- `../../05_Architecture/Odoo_Notification_Gap_Analysis.md`
- `../../00_Project/V8_Canonical_Baseline.md`