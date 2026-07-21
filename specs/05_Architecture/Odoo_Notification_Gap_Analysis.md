# Odoo Notification Gap Analysis — CAS v8

| مشخصه | مقدار |
|---|---|
| وضعیت | `Needs Implementation Verification` |
| تصمیم محصول | Reuse Odoo; Extend only real gaps |
| نسخه هدف | Odoo 19 Community / CAS v8 |

## اصل

CAS سیستم Notification را از صفر بازسازی نمی‌کند. Odoo Mail/Discuss/Bus زیرساخت پایه Message، Thread، Inbox، Realtime و Delivery را فراهم می‌کند. هر Extension باید Gap مشخص و آزمون‌شده داشته باشد.

## قابلیت‌هایی که باید ابتدا از Odoo Reuse شوند

- Mail Thread و Message
- Discuss Inbox
- Follower و Subscription
- Email/In-app Delivery Preference
- Mention
- Activity
- Bus Realtime Update
- Message Read/Interactionهای استاندارد
- Chatter Link به Record

جزئیات دقیق پشتیبانی Odoo 19 باید در Spike اجرایی Verify شود.

## نیازهای CAS برای ارزیابی Gap

| نیاز | راهبرد اولیه | وضعیت |
|---|---|---|
| Notification Center مستقل Workspace | View/Aggregation روی Odoo و Providerها | نیازمند طراحی Adapter |
| Deep Link یکنواخت به Route CAS | Metadata/Resolver Extension | Gap محتمل |
| Severity سازمانی | Metadata محدود | Gap محتمل |
| Actionable Notification | استفاده از Activity/Action و Extension محدود | نیازمند Verify |
| Read/Unread تجمیعی | Reuse استاندارد؛ مدل مکمل فقط اگر کافی نبود | نیازمند Verify |
| Company Policy | Preference/Policy Adapter | Gap محتمل |
| Snooze | فقط در صورت نیاز تأییدشده | آینده یا Gap |
| Retention/Archive | Reuse استاندارد یا Policy مکمل | نیازمند Verify |
| Multi-provider aggregation | Notification Provider Contract | Gap محتمل |
| Realtime badge | Bus + Permission-aware count | قابل Reuse/Extend |

## مواردی که نباید دوباره ساخته شوند

- Message Model موازی
- Bus موازی
- Email Queue موازی
- Thread/Participant Model موازی
- Chatter کامل موازی
- Preference Delivery موازی، تا زمانی که Odoo کافی است

## معماری پیشنهادی

```text
Domain Event
→ CAS Notification Adapter
→ Odoo Mail/Discuss/Activity/Bus
→ Optional CAS Metadata
→ Notification Provider
→ Workspace Notification Center
```

Notification Center مالک Source Notification نیست و فقط نمای مجاز و تجمیعی ارائه می‌کند.

## Metadata احتمالی CAS

- provider key
- resource reference
- CAS deep link
- severity
- action key
- company context
- expiry
- category

فقط Metadataهای فاقد معادل استاندارد اضافه می‌شوند.

## امنیت

- Notification وجود رکورد Forbidden را افشا نمی‌کند.
- Badge Count Permission-aware است.
- Deep Link Permission را دوباره بررسی می‌کند.
- Notification حذف یا دسترسی‌ازدست‌رفته باید Unavailable شود.
- Cross-company aggregation محدود است.

## Spikeهای لازم

1. بررسی رفتار Inbox و Read/Unread Odoo 19 Community
2. بررسی قابلیت Actionable Notification با Activity/Message
3. بررسی Deep Link به Client Action سفارشی
4. بررسی Bus برای Badge و Center Update
5. بررسی Archive/Retention
6. بررسی Preference Email/In-app
7. بررسی Discuss Integration در Workspace سفارشی

## معیار ایجاد Extension

Extension فقط زمانی ساخته می‌شود که:

- Gap با Spike و Test ثابت شود.
- Odoo Standard با Configuration یا Adapter حل نکند.
- مدل جدید Lifecycle واقعی و Security مستقل لازم داشته باشد.
- داده استاندارد Odoo کپی نشود.

## تصمیم فعلی

- `cas_notification_core` کامل تصویب نشده است.
- Notification Center مستقل تصویب شده است.
- Adapter و Metadata محدود پس از Gap Analysis مجاز است.
- Odoo Mail/Discuss/Bus مرجع Delivery باقی می‌ماند.