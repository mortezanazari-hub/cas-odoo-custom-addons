# ارزیابی اثر ماژولی نسخه ۸

| مشخصه | مقدار |
|---|---|
| نسخه | `CAS UI Workspace v8` |
| وضعیت | `Needs Review` |
| نوع سند | Impact Assessment؛ نه Specification اجرایی |
| Change Set | `../06_ChangeSets/CS-WORKSPACE-V8.md` |

## خلاصه

نسخه ۸ سه حوزه را تکمیل می‌کند: مدیریت دسته‌های Task شخصی، انتخاب مقیاس‌پذیر شرکت‌کنندگان رویداد، و تجربه کامل‌تر گفت‌وگو بر پایه Odoo Mail/Discuss. اثر اصلی روی `cas_workspace` است، اما چند Provider و ماژول منبع نیز باید قراردادهای جدید ارائه دهند.

## ۱. `cas_workspace` — اثر بسیار زیاد

### مسئولیت‌های افزوده

- Overlay Manager مشترک
- Stack لایه‌ها و Parent/Child Overlay
- Focus Trap و Focus Restore
- Scroll Lock
- Attendee Selector Component
- Directory Search Adapter
- Organization Scope Adapter
- Context Menu و Emoji Picker Infrastructure
- Conversation Layout با Composer ثابت
- Personal Category UI

### مواردی که نباید مالک شود

- Employee و Organization Assignment
- Calendar Event واقعی
- Invitation و Attendee Record
- Task رسمی زیرمجموعه
- Message، Channel و Reaction
- Category/Task شخصی در صورت تصویب ماژول مستقل

### API/Serviceهای موردنیاز

- `search_people(query, department_id, scope, cursor, limit)`
- `get_assignment_capability(target_ids, event_context)`
- `create_calendar_event(payload, recipient_modes)`
- `get_personal_task_categories()`
- `create_personal_task_category(name)`
- `rename_personal_task_category(id, name)`
- `delete_personal_task_category(id)`
- Discuss Adapter برای Reply/Forward/Reaction/Pin/Mute/Archive

نام نهایی APIها هنوز تصویب نشده است.

## ۲. `cas_personal_task` پیشنهادی — اثر ساختاری

### مسئولیت پیشنهادی

- Personal Task
- Personal Category
- System Category Seed
- Reminder
- Ownership Rule
- Archive/Retention

### قواعد کلیدی

- Category سیستمی قفل است.
- Category شخصی User-scoped است.
- حذف Category، Taskها را منتقل می‌کند.
- تبدیل Task به Work Report از طریق Adapter انجام می‌شود.

### سؤال معماری

آیا این دامنه از ابتدا ماژول مستقل باشد یا موقتاً داخل `cas_workspace` بماند؟ پیشنهاد این سند: ماژول مستقل، به‌دلیل مالکیت داده و Lifecycle جدا.

## ۳. `cas_action_hub` — اثر متوسط

- دریافت Task/Action ایجادشده از Event برای زیرمجموعه مجاز
- حفظ مرزبندی با Task شخصی
- Deep Link به Event منبع
- Notification و Deadline
- بررسی Capability و Assignment Scope

Action Hub نباید Permission رابطه مدیریتی را از Frontend بپذیرد؛ باید Backend Resolver را فراخوانی کند.

## ۴. HR/Employee Directory — اثر زیاد

### نیازها

- Search Server-side نام، سمت، واحد و شناسه پرسنلی
- Pagination/Cursor
- Company Scope
- نمایش محدود اطلاعات
- جلوگیری از نشت افراد غیرمجاز

### خروجی حداقلی

- employee/partner identifier
- display name
- avatar reference
- job title
- department
- effective relationship badge
- invitation eligibility
- task assignment eligibility

## ۵. Organization Hierarchy Resolver — اثر زیاد

این Resolver ممکن است داخل ماژول سازمانی موجود یا یک Service مشترک قرار گیرد.

### مسئولیت

- تعیین زیرمجموعه مستقیم/غیرمستقیم
- بررسی تاریخ مؤثر Assignment
- بررسی Delegation
- Multi-company
- محاسبه Scope برای Task Assignment

نتیجه Resolver باید در Backend معتبر باشد و Cache آن با تغییر ساختار سازمانی Invalid شود.

## ۶. Calendar/Event Integration — اثر زیاد

### مسئولیت

- ایجاد/ویرایش Event
- Attendee Management
- Invitation Delivery
- RSVP State
- Timezone
- Jalali Input Adapter
- Event-to-Task linkage

### Transaction Policy

ایجاد Event، ارسال Invitation و ساخت Task می‌توانند Failureهای متفاوت داشته باشند. سیاست Atomic یا Partial Success باید پیش از پیاده‌سازی تصویب شود و نتیجه به کاربر گزارش شود.

## ۷. Odoo Mail/Discuss/Bus — اثر زیاد

### قابلیت‌های مورد استفاده

- Channel/Conversation
- Message
- Member
- Unread
- Reply/Thread reference
- Forward یا Extension سازگار
- Reaction
- Pin یا Extension سازگار
- Mute/Notification preference
- Archive/User preference
- Realtime Bus

### اصل

هیچ مدل موازی Conversation/Message در Workspace ایجاد نمی‌شود.

## ۸. `cas_document_core` — اثر کم تا متوسط

- Permission دانلود فایل گفتگو در صورت Link به Document
- نمایش فایل‌های مرتبط در Drawer
- عدم افشای Metadata فایل غیرمجاز

Attachment ساده Mail لزوماً Document Core نیست؛ Adapter باید نوع منبع را تشخیص دهد.

## ۹. Notification Core — اثر متوسط

- Invitation Sent/Failed
- Task Created/Failed
- Message Notification
- Mute Policy
- Realtime و fallback
- Deep Link

## ۱۰. Jalali Suite — اثر کم

- Date Picker و نمایش Modal
- تبدیل ورودی جلالی به Datetime استاندارد
- عدم تغییر ذخیره UTC

## Dependency پیشنهادی

```text
cas_core
├── cas_personal_task (پیشنهادی)
├── cas_action_hub
├── cas_workspace
│   ├── hr / employee directory
│   ├── mail / discuss / bus
│   ├── calendar/event integration
│   └── jalali adapters
└── notification core (در صورت تصویب)
```

`cas_workspace` نباید dependency سخت به تمام Providerهای عملیاتی داشته باشد؛ Adapterهای اختیاری و حالت `unavailable` لازم‌اند.

## امنیت مشترک

- بدون `sudo()` برای Queryهای کاربرمحور
- Company Scope
- ACL و Record Rule ماژول منبع
- Method-level permission
- Provider Whitelist
- جلوگیری از ID tampering
- Attachment permission
- Audit برای Task Assignment و Delete Message

## Migration

- Seed دسته‌های سیستمی با XML ID پایدار
- Migration دسته‌های Prototype وجود ندارد مگر داده واقعی قبلاً ذخیره شده باشد
- Preferenceهای Pin/Mute/Archive باید Versioned شوند
- Extensionهای Mail باید با Upgrade Odoo 19 سازگار باشند

## Test Strategy حداقلی

- Unit: Category Rules، Scope Resolver، Permission
- Integration: Event + Invitation + Task
- Integration: Discuss actions
- Security: RPC tampering و multi-company
- UI: Overlay، Focus، Scroll، RTL و Mobile
- Load: Directory Search با داده حجیم
- Realtime: Bus reconnect

## وضعیت نهایی

این سند `Implementation Ready` نیست. برای هر ماژول باید Specification، API، Security، Migration و Test Strategy مستقل نوشته و تصویب شود.
