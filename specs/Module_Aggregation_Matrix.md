# ماتریس تجمیع تغییرات ماژول‌ها

این فایل مرجع مرکزی اثر تصمیمات صفحه‌ای بر ماژول‌های پروژه است. ثبت ردیف در این ماتریس مجوز پیاده‌سازی نیست.

## وضعیت‌ها

- `Collected`: ثبت شده ولی هنوز تجمیع ماژولی نشده است.
- `Needs Review`: نیازمند بررسی مرز مالکیت، امنیت یا صفحات دیگر است.
- `Conflict`: تعارض حل‌نشده دارد.
- `Consolidated`: در Specification ماژول تجمیع شده است.
- `Implementation Ready`: آماده تبدیل به دستور اجرایی است.

## خط نسخه‌بندی فعال

```text
CAS UI Prototype v4 → CAS UI Workspace v7 → CAS UI Workspace v8
```

نسخه‌های ۵ و ۶ Release رسمی مستقل نیستند.

# بخش اول — تصمیمات پایه Workspace v7

## میزکار

| تصمیم | ماژول/دامنه | اثر | وضعیت |
|---|---|---|---|
| `PAGE-EMP-DESK-DEC-001..015` | `cas_workspace`, `cas_work_report`, `cas_action_hub`, Attendance, Activity Catalog | میزکار عملیاتی، ثبت تدریجی فعالیت، شخصی‌سازی | Needs Review |
| `PAGE-EMP-DESK-DEC-016..018` | `cas_workspace`, Search Registry | Hero، کارت‌های وضعیت و Command Launcher | Needs Review |
| `PAGE-EMP-DESK-DEC-019..021` | `cas_action_hub`, Calendar, Mail/Bus | Task شخصی، تقویم و گفتگو | Needs Review |
| `PAGE-EMP-DESK-DEC-022..030` | `cas_workspace`, User Preference, Providerها | Widget Layout، DnD، Theme، Drawer و Route Action | Needs Review |

## کارهای شخصی v7

| تصمیم | ماژول/دامنه | اثر | وضعیت |
|---|---|---|---|
| `PAGE-EMP-TASK-DEC-001` | `cas_workspace`, `cas_action_hub` | جداسازی Task شخصی از Action رسمی | Needs Review |
| `PAGE-EMP-TASK-DEC-002` | Access Resolver | Capability `personal.tasks` | Collected |
| `PAGE-EMP-TASK-DEC-003..007` | Personal Task Store، `cas_workspace`, `cas_work_report` | ثبت، تکمیل، زمان‌بندی، Widget و تبدیل اختیاری | Needs Review |

## تقویم v7

| تصمیم | ماژول/دامنه | اثر | وضعیت |
|---|---|---|---|
| `PAGE-EMP-CAL-DEC-001..003` | `cas_workspace`, Calendar Aggregator | Route و سه نمای تقویم | Needs Review |
| `PAGE-EMP-CAL-DEC-004..005` | Jalali Suite، Odoo ORM | نمایش شمسی و ذخیره استاندارد | Needs Review |
| `PAGE-EMP-CAL-DEC-006..007` | Calendar Integration، Shift، Action، Correspondence، Workflow | CRUD و Feed چندمنبعی | Needs Review |

## گفتگوها v7

| تصمیم | ماژول/دامنه | اثر | وضعیت |
|---|---|---|---|
| `PAGE-EMP-CONV-DEC-001..005` | `cas_workspace` | Route، Topbar، Widget، Drawer و صفحه | Collected |
| `PAGE-EMP-CONV-DEC-006..007` | Odoo Mail/Discuss/Bus | Unread، Realtime و مالکیت Message | Needs Review |
| `PAGE-EMP-CONV-DEC-008` | Search | جداسازی Search پیام از Global Search | Collected |

## سایر صفحات v7

| صفحه | ماژول/دامنه | اثر | وضعیت |
|---|---|---|---|
| Global Search | `cas_workspace`, Provider Registry, Access Resolver, `cas_jalali_search` | Search چندمنبعی و امن | Needs Review |
| Notification Center | Notification Service، `cas_action_hub`, Providerها، Mail/Bus/Cron | اعلان، Read State و Delivery | Needs Review |
| Recent History | `cas_workspace`, History Service, Access Resolver | تاریخچه مرور و Privacy | Needs Review |
| Workspace Shell | `cas_workspace`, User Preference | Navigation، Theme، Widget، Router و Overlay | Needs Review |

# بخش دوم — تغییرات Workspace v8

## کارهای من: دسته‌ها

| تصمیم | ماژول/دامنه | نوع اثر | خلاصه | وضعیت |
|---|---|---|---|---|
| `PAGE-EMP-TASK-DEC-008` / `DEC-012` | `cas_personal_task` پیشنهادی، `cas_workspace` | Domain/Data/UI | تفکیک دسته سیستمی و شخصی | Needs Review |
| `PAGE-EMP-TASK-DEC-009` | Personal Task Store | Transaction/Data | حذف دسته و انتقال Taskها به دسته پیش‌فرض | Needs Review |
| `PAGE-EMP-TASK-DEC-010` | Security | ACL/Method Rule | ممنوعیت حذف دسته سیستمی و کنترل مالکیت | Needs Review |

### اثر ماژولی

- `cas_workspace`: UI مدیریت Category و Sync فیلترها
- `cas_personal_task` پیشنهادی: مالک Category، Task و Reminder
- `cas_action_hub`: بدون مالکیت Category؛ فقط حفظ مرزبندی
- `cas_work_report`: Adapter تبدیل Task به Activity

## تقویم: Selector شرکت‌کنندگان

| تصمیم | ماژول/دامنه | نوع اثر | خلاصه | وضعیت |
|---|---|---|---|---|
| `PAGE-EMP-CAL-DEC-008` / `DEC-013` | HR Directory، `cas_workspace` | Search/Performance | جست‌وجوی Server-side و بدون بارگذاری کل کارکنان | Needs Review |
| `PAGE-EMP-CAL-DEC-009` | Calendar/Event، `cas_action_hub` | Domain Boundary | دعوت و Task دو Operation مستقل | Needs Review |
| `PAGE-EMP-CAL-DEC-010` | Organization Scope Resolver | Security | Task فقط برای زیرمجموعه مجاز | Needs Review |
| `PAGE-EMP-CAL-DEC-011` | Calendar Selector | UI/Data | روش ارسال مستقل برای هر فرد | Collected |
| `PAGE-EMP-CAL-DEC-012` / `DEC-015` | `cas_workspace` | Overlay/Accessibility | Selector روی Modal، Focus Restore و Scroll Lock | Needs Review |

### اثر ماژولی

- `cas_workspace`: Modal، Selector، Chip، State و Overlay Manager
- HR/Employee Directory: Search Server-side، Pagination و Scope اطلاعات
- Organization Hierarchy Resolver: رابطه مدیریتی، Delegation و Company Scope
- Odoo Calendar/Event: Event، Attendee، Invitation و RSVP
- `cas_action_hub`: Task/Action برای زیرمجموعه مجاز
- Mail/Notification: Delivery و Failure Feedback
- Jalali Suite: ورودی و نمایش تاریخ

## گفتگوها: تجربه پیام‌رسانی

| تصمیم | ماژول/دامنه | نوع اثر | خلاصه | وضعیت |
|---|---|---|---|---|
| `PAGE-EMP-CONV-DEC-009` / `DEC-014` | Odoo Mail/Discuss/Bus | Integration | استفاده از قابلیت استاندارد و عدم ساخت Message موازی | Needs Review |
| `PAGE-EMP-CONV-DEC-010` | `cas_workspace` | Layout | Composer ثابت و حذف Scroll صفحه | Collected |
| `PAGE-EMP-CONV-DEC-011` | `cas_workspace` | Interaction | Context Menu اختصاصی پیام و گفتگو | Collected |
| `PAGE-EMP-CONV-DEC-012` | Mail/Discuss Adapter | Feature/API | Reply، Forward، Pin و Reaction | Needs Review |
| `PAGE-EMP-CONV-DEC-013` / `DEC-015` | Overlay Manager | UX/Accessibility | Outside Click، Escape، Focus و Viewport Position | Needs Review |

### اثر ماژولی

- `cas_workspace`: Layout، Floating Action، Context Menu، Picker و Adapter
- Odoo Mail/Discuss/Bus: Conversation، Message، Member، Unread، Reaction و Realtime
- `cas_document_core`: Permission فایل در صورت Link به Document
- `cas_correspondence`: مرزبندی با نامه رسمی
- Notification Core: پیام جدید، Mute و Deep Link

## زیرساخت Overlay مشترک v8

| حوزه | ماژول/دامنه | اثر | وضعیت |
|---|---|---|---|
| Overlay Stack | `cas_workspace` | Parent/Child Layer و حذف z-index موردی | Needs Review |
| Focus | `cas_workspace` | Trap، Restore و Keyboard | Needs Review |
| Scroll | `cas_workspace` | Body Lock و جلوگیری از Scroll تودرتو | Collected |
| Context Menu/Picker | `cas_workspace` | Outside Click، Escape و Viewport Boundary | Collected |
| Accessibility | Design System / Workspace | `aria-modal`، Label و Focus Ring | Needs Review |

# بخش سوم — نمای ماژول‌محور جامع پس از v8

## `cas_workspace` — اثر بسیار زیاد

- Shell، Router و Navigation
- Widget Registry و Preference
- صفحات Personal Tasks، Calendar و Conversations
- Overlay Manager
- Directory Search Adapter
- Organization Scope Adapter
- Calendar Attendee Selector
- Discuss Adapter
- Context Menu و Emoji Picker
- Layout ثابت گفتگو و Composer

وضعیت: `Needs Review`.

## `cas_personal_task` پیشنهادی — اثر ساختاری

- Personal Task
- Personal Category
- System Category Seed
- Reminder و Ownership
- Archive/Retention

وضعیت: `Needs Review`؛ ایجاد ماژول هنوز قطعی نشده است.

## `cas_action_hub` — اثر زیاد

- حفظ جداسازی Action رسمی از Task شخصی
- ایجاد Task از Event برای Target مجاز
- Deadline، Notification و Deep Link

وضعیت: `Needs Review`.

## HR/Employee Directory — اثر زیاد

- Search Server-side
- Cursor/Pagination
- Company Scope
- حداقل Metadata مجاز

وضعیت: `Needs Review`.

## Organization Hierarchy Resolver — اثر زیاد

- رابطه مستقیم/غیرمستقیم
- تاریخ مؤثر Assignment
- Delegation
- Multi-company
- Task Assignment Scope

وضعیت: `Needs Review`؛ محل نهایی Service مشخص نشده است.

## Odoo Calendar/Event — اثر زیاد

- Event و Attendee
- Invitation و RSVP
- Timezone و Jalali Adapter
- Event-to-Task Link

وضعیت: `Needs Review`.

## Odoo Mail/Discuss/Bus — اثر زیاد

- Conversation Source
- Reply/Forward/Reaction/Pin
- Unread و Realtime
- Member/File Permission
- Mute/Archive Preference

وضعیت: `Needs Review`؛ تطبیق دقیق با Odoo 19 لازم است.

## سایر ماژول‌ها

- `cas_document_core`: فایل و Permission
- Notification Core: دعوت، پیام و Failure Feedback
- Jalali Suite: تاریخ تقویم
- `cas_work_report`: تبدیل اختیاری Task
- `cas_correspondence`: مرزبندی با Conversation

وضعیت: `Needs Review`.

# بخش چهارم — اسناد مرجع

- `02_UI_UX/Employee/Personal_Tasks.md`
- `02_UI_UX/Employee/Calendar.md`
- `02_UI_UX/Employee/Conversations.md`
- `04_Decisions/DEC-012-Personal-Task-Category-Governance.md`
- `04_Decisions/DEC-013-Calendar-Attendee-Selection-And-Assignment-Authorization.md`
- `04_Decisions/DEC-014-Discuss-Reuse-And-Message-Interaction.md`
- `04_Decisions/DEC-015-Overlay-Layering-And-Focus-Management.md`
- `03_Modules/V8_Impact_Assessment.md`
- `05_Architecture/V8-Interaction-And-Integration-Contracts.md`
- `06_ChangeSets/CS-WORKSPACE-V8.md`

## قواعد به‌روزرسانی

1. هر صفحه جدید سند مستقل دارد.
2. هر تصمیم با شناسه در این ماتریس ثبت می‌شود.
3. Decisionهای بین‌صفحه‌ای در `04_Decisions` ثبت می‌شوند.
4. Change Set جامع هر نسخه مرجع Audit همان نسخه است.
5. آثار در `03_Modules` Consolidate می‌شوند.
6. فقط Specification ماژولی با وضعیت `Implementation Ready` مجوز اجرا دارد.
