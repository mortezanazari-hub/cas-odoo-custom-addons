# قراردادهای معماری تعامل و Integration نسخه ۸

| مشخصه | مقدار |
|---|---|
| وضعیت | `Needs Review` |
| نسخه | `CAS UI Workspace v8` |
| دامنه | Overlay، Directory Search، Calendar، Task Assignment، Discuss |

## ۱. اصل معماری

Workspace تجربه یکپارچه ارائه می‌کند، اما مالک داده کسب‌وکاری Providerها نیست. هر Operation باید به ماژول مالک داده واگذار شود و مجوزهای همان ماژول را رعایت کند.

## ۲. Overlay Manager

### هدف

جلوگیری از `z-index`های موردی، Drawer پشت Modal، Focus گم‌شده و Scroll تودرتو.

### قرارداد

هر Overlay باید دارای این Metadata باشد:

- `overlay_id`
- `type`: modal, drawer, popover, context_menu, picker, tooltip, toast
- `parent_overlay_id`
- `dismiss_policy`
- `focus_return_target`
- `scroll_lock_policy`
- `aria_labelledby`

### رفتار

- Stack ترتیب لایه را تعیین می‌کند.
- فقط Overlay بالایی Interactive است.
- Child نسبت به Parent Layer بالاتری دارد.
- Escape به Top Layer ارسال می‌شود.
- Focus هنگام Close به Trigger برمی‌گردد.
- Body Scroll هنگام Modal قفل است.

## ۳. Directory Search Contract

### ورودی پیشنهادی

```json
{
  "query": "مر",
  "department_id": 12,
  "scope": "my_subordinates",
  "cursor": null,
  "limit": 20,
  "company_id": 1
}
```

### خروجی پیشنهادی

```json
{
  "items": [
    {
      "employee_id": 101,
      "partner_id": 9001,
      "display_name": "مریم فلاحی",
      "job_title": "مسئول دبیرخانه",
      "department_name": "مدیریت اداری",
      "avatar_url": "/web/image/...",
      "relationship": "direct_subordinate",
      "can_invite": true,
      "can_assign_task": true,
      "restriction_reason": null
    }
  ],
  "next_cursor": "...",
  "has_more": true
}
```

### الزامات

- Query حداقل دو نویسه، مگر Scope محدود مانند recent/direct reports.
- اجرای Server-side و بدون بارگذاری کامل Directory.
- Company و Record Rule در Query اعمال می‌شوند.
- نتیجه فاقد فیلدهای غیرضروری یا محرمانه است.
- Sort پایدار و Cursor-based ترجیح دارد.

## ۴. Organization Scope Contract

Resolver باید برای هر Target این خروجی را بدهد:

- رابطه مؤثر
- تاریخ اعتبار رابطه
- مجوز دعوت
- مجوز تخصیص Task
- دلیل محدودیت
- منبع مجوز: hierarchy, delegation, explicit capability

Frontend حق ندارد از روی Department Name مجوز Task را حدس بزند.

## ۵. Calendar Event Command

### Payload مفهومی

```json
{
  "title": "جلسه بررسی تأمین قطعات",
  "start": "2026-07-20T15:00:00+03:30",
  "end": "2026-07-20T16:00:00+03:30",
  "event_type": "meeting",
  "description": "...",
  "recipients": [
    {"partner_id": 9001, "mode": "invite_and_task"},
    {"partner_id": 9002, "mode": "invite"}
  ]
}
```

### پردازش Backend

1. Validation تاریخ و زمان
2. Resolve Target و Scope
3. ایجاد Event
4. ایجاد Attendee/Invitation
5. ایجاد Taskهای مجاز
6. ثبت Link میان Event و Task
7. ارسال Notification
8. بازگرداندن نتیجه تفصیلی

### نتیجه تفصیلی

Backend باید Partial Failure را شفاف گزارش کند؛ مثال: Event ایجاد شد، دعوت ارسال شد، اما Task یک نفر به‌دلیل تغییر ساختار سازمانی رد شد.

سیاست Atomic یا Partial Success باید در Specification نهایی تعیین شود.

## ۶. Personal Category Contract

مدل پیشنهادی:

- `name`
- `owner_user_id`
- `system_key`
- `is_system`
- `sequence`
- `active`
- `company_id` در صورت نیاز

### Delete Command

- Category سیستمی: Reject
- Category شخصی غیرمالک: Reject
- Category شخصی مالک: انتقال Taskها به Default + Archive/Delete Category در یک Transaction

## ۷. Discuss Adapter Contract

### خواندن

- فهرست Conversationهای مجاز
- Message Pagination
- Unread State
- Pinned Messages
- Members و Files

### عملیات

- Send Message
- Reply
- Forward
- React/Unreact
- Pin/Unpin Message
- Pin/Unpin Conversation Preference
- Mute/Unmute
- Archive/Unarchive
- Mark Read/Unread
- Delete Own Message در صورت مجازبودن

### قواعد

- Adapter باید از APIهای واقعی Odoo 19 استفاده کند.
- قابلیت استاندارد موجود دوباره مدل‌سازی نمی‌شود.
- Extension فقط جایی مجاز است که قابلیت موردنیاز در Community موجود نباشد.
- هر Extension باید Upgrade Risk و Test داشته باشد.

## ۸. Layout Contract صفحه گفتگو

- Shell ارتفاع Viewport را به Workspace می‌دهد.
- Conversation Page از CSS Grid/Flex با `min-height:0` استفاده می‌کند.
- Sidebar List: `overflow:auto`
- Message Body: `overflow:auto`
- Composer: خارج از ناحیه Scroll و Sticky/Fixed در Container
- Body/Page: بدون Scroll اضافی

## ۹. Outside Click Contract

Context Menu و Picker باید:

- Pointer Event بیرون را تشخیص دهند.
- Event داخلی را به‌اشتباه Outside تلقی نکنند.
- با Escape بسته شوند.
- با Route Change و Conversation Change بسته شوند.
- Listenerها هنگام Unmount پاک شوند.

## ۱۰. Accessibility

- Focus Trap برای Modal/Drawer
- Focus Restore
- `role=dialog` و `aria-modal`
- نام قابل دسترس Icon Buttonها
- Keyboard Navigation برای Menu و Emoji Grid
- Contrast و Focus Ring
- عدم اتکا صرف به رنگ برای Badge مجوز

## ۱۱. Performance

- Debounce جست‌وجوی Directory
- Cancel Request قبلی
- Cursor Pagination
- Message Virtualization در کانال‌های بزرگ
- Lazy Load فایل‌ها و اطلاعات Drawer
- عدم Render همه Emojiها تا زمان بازشدن Picker

## ۱۲. Observability

رویدادهای قابل ثبت:

- Directory Search latency/error
- Event command partial failure
- Unauthorized task assignment attempt
- Discuss adapter error
- Bus disconnect/reconnect
- Overlay focus failure در تست خودکار

## ۱۳. ممنوعیت‌ها

- Odoo Core Edit
- `sudo()` برای دورزدن Permission
- بارگذاری تمام کارکنان در Browser
- مدل Message موازی در Workspace
- `z-index` موردی بدون Overlay Manager
- امنیت مبتنی فقط بر Hidden/Disabled UI
