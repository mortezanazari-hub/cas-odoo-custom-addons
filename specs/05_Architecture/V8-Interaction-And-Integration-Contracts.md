# قراردادهای معماری تعامل و Integration نسخه ۸

| مشخصه | مقدار |
|---|---|
| وضعیت | `Consolidated` |
| نسخه | `CAS UI Workspace v8 — Through Iteration 12` |
| دامنه | Overlay، Directory، Calendar، Task/Action، Discuss، Notification |

## ۱. اصل معماری

Workspace تجربه یکپارچه ارائه می‌کند، اما مالک داده کسب‌وکاری Providerها نیست. هر Operation به Service ماژول مالک واگذار می‌شود و Permission همان Domain را رعایت می‌کند.

## ۲. Overlay و Focus Contract

Primitiveهای Modal، Dialog، Dropdown و Command از Odoo UI Services Reuse می‌شوند. CAS سیستم Overlay مستقل و موازی ایجاد نمی‌کند.

Workspace Shell Policy مشترک را اعمال می‌کند:

- Stack Order
- Parent/Child Overlay
- فقط Top Overlay Interactive
- Escape روی Top Overlay
- Focus Trap
- Focus Restore به Trigger
- Outside Click مطابق Dismiss Policy
- Scroll Lock در Modalهای لازم
- Cleanup Listener هنگام Unmount/Route Change
- عدم دسترسی Tab به محتوای پشت Dialog

Metadata مفهومی:

```text
overlay_id
type
parent_overlay_id
dismiss_policy
focus_return_target
scroll_lock_policy
accessible_label
```

`z-index` موردی و بدون Contract ممنوع است.

## ۳. Directory Search Contract

### ورودی مفهومی

```json
{
  "query": "مر",
  "organization_unit_id": 12,
  "purpose": "calendar_invite",
  "cursor": null,
  "limit": 20,
  "company_context": 1
}
```

### خروجی مفهومی

```json
{
  "items": [
    {
      "person_id": 101,
      "display_name": "مریم فلاحی",
      "job_title": "مسئول دبیرخانه",
      "organization_unit": "مدیریت اداری",
      "avatar_ref": "...",
      "relationship": "direct_subordinate",
      "eligible": true,
      "restriction_reason": null
    }
  ],
  "next_cursor": "..."
}
```

### الزامات

- Server-side و Cursor/Page-based
- Purpose-aware Scope از `cas_organization_core`
- Company و Record Rule
- حداقل Metadata لازم
- Cancel Request قبلی و Debounce
- عدم بارگذاری کل Directory در Browser
- Sort پایدار

## ۴. Organization Scope Contract

Resolver ورودی‌های زیر را می‌پذیرد:

- actor
- effective datetime
- company
- purpose
- optional target/filter

خروجی باید شامل Eligibility، Relationship، Source و Restriction Reason باشد.

Purposeها می‌توانند نتایج متفاوت بدهند:

- calendar invite
- action assign
- work report review
- search/directory
- audit

Frontend از Department Name یا Role Label مجوز حدس نمی‌زند.

## ۵. Calendar Event Command

### تفکیک مفاهیم

- Invitation: حضور در Event
- Self Task: Personal Task برای Actor
- Assigned Action: Action سازمانی برای شخص دیگر

### Payload مفهومی

```json
{
  "command_id": "uuid",
  "event": {
    "title": "جلسه بررسی تأمین قطعات",
    "start": "2026-07-20T15:00:00+03:30",
    "end": "2026-07-20T16:00:00+03:30",
    "description": "..."
  },
  "attendees": [9001, 9002],
  "self_task": {"enabled": true, "title": "پیگیری صورتجلسه"},
  "assigned_actions": [
    {"target_person_id": 101, "title": "ارسال گزارش"}
  ]
}
```

### پردازش

1. Validate Event و Timezone.
2. Resolve Actor و Purpose Scope.
3. Create/Update Event و Attendees در Calendar Domain.
4. Call Personal Task Service برای Self Task.
5. Call Action Hub Service برای Assigned Actions.
6. ثبت Linkهای منبع.
7. درخواست Notification پس از موفقیت داده اصلی.
8. بازگرداندن نتیجه تفصیلی هر Operation.

### Transaction و Idempotency

- Event data هم‌دامنه Transactional است.
- `command_id` از Duplicate جلوگیری می‌کند.
- Side Effectهای Cross-domain Retry امن دارند.
- Partial Failure صریح است؛ سیستم رکورد تکراری ایجاد نمی‌کند.
- Compensation Policy در API Spec تعیین می‌شود.

## ۶. Personal Category Contract

مدل در `cas_personal_task` است:

- owner
- name
- system key
- system flag
- sequence
- active

Delete:

- System Category: Reject
- Non-owner: Reject
- Owner: انتقال Taskها به Category مقصد و Archive/Delete در یک Transaction

Workspace فقط UI و Provider Result را نمایش می‌دهد.

## ۷. Discuss Adapter Contract

### اصل

Odoo Mail/Discuss/Bus مالک Conversation و Message است. CAS از API واقعی Odoo 19 Community استفاده می‌کند و فقط Gap تأییدشده را Extend می‌کند.

### خواندن

- Conversations مجاز
- Message Pagination
- Unread State
- Members و Attachments مجاز
- Pin/Preferenceهای قابل پشتیبانی

### عملیات

- Send
- Reply
- Reaction
- Mark Read/Unread
- Mute/Archive/Pin، در صورت استاندارد یا Extension تأییدشده
- Edit/Delete Own Message، مطابق Odoo و Policy
- Forward، فقط پس از Verification و Permission

### ممنوع

- Message Model موازی
- Thread Model موازی
- Bus موازی
- Attachment Metadata غیرمجاز

## ۸. Conversation Layout Contract

- Route گفتگو Scroll کلی ندارد.
- Conversation List: Internal Scroll
- Message Body: Internal Scroll
- Composer: خارج از Message Scroll
- شروع از آخرین پیام
- پس از Send، اگر Near-bottom است انتها حفظ می‌شود.
- هنگام Load Older، Anchor حفظ می‌شود.
- پیام جدید در حالت دور از انتها Indicator نشان می‌دهد.
- `min-height: 0` و Layout صحیح Grid/Flex الزامی است.

## ۹. Notification Integration

```text
Domain Event
→ CAS Adapter
→ Odoo Mail/Discuss/Activity/Bus
→ Optional CAS Metadata
→ Notification Center Provider
```

- Delivery System جدید ساخته نمی‌شود.
- Deep Link Permission را دوباره بررسی می‌کند.
- Count و List Permission-aware هستند.
- نبود Bus فقط Realtime را کاهش می‌دهد و Fetch عادی باقی می‌ماند.

## ۱۰. Timezone و Jalali

- Payload DateTime باید Offset یا UTC معتبر داشته باشد.
- افزودن دستی `Z` به Local DateTime ممنوع است.
- Odoo/User Timezone و DateTime Utility مرجع است.
- Jalali فقط Input/Display Adapter است.
- جهت ماه قبل/بعد در RTL معنایی و آزمون‌شده است.

## ۱۱. Accessibility

- Focus Trap/Restore
- `role=dialog` و `aria-modal`
- Accessible Label برای Icon Button
- Keyboard Navigation برای Menu، Picker و Directory
- Focus Ring
- عدم اتکا صرف به رنگ
- Touch Target مناسب

## ۱۲. Performance

- Directory Cursor Pagination
- Message Pagination/Virtualization
- Lazy Load Drawer و Attachment
- Provider Timeout
- Cancel stale requests
- عدم Render داده سنگین پیش از نیاز

## ۱۳. Observability

- directory latency/error
- scope resolution reason
- calendar command result/partial failure
- duplicate command prevented
- unauthorized assignment attempt
- discuss adapter error
- bus reconnect
- overlay focus error
- notification deep-link failure

## ۱۴. ممنوعیت‌ها

- Odoo Core Edit
- broad `sudo`
- Client-side permission inference
- بارگذاری کل Directory
- مدل Message/Notification موازی
- Global `z-index` و Keyboard Listener متعارض
- DateTime conversion دستی و ناامن

## ۱۵. معیار پذیرش

- Self Task و Assigned Action به مالک درست بروند.
- Event Retry رکورد تکراری نسازد.
- Directory Scope Purpose-aware باشد.
- Overlay با Odoo Services سازگار باشد.
- Conversation Scroll و Focus صحیح باشد.
- Notification زیرساخت Odoo را Reuse کند.
- Timezone و RTL در تست پوشش داده شوند.