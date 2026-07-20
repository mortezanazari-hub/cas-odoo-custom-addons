# قرارداد اتصال Workspace به Odoo 19 Community

## معماری

رابط به‌صورت OWL Client Action در ماژول `cas_workspace` پیاده‌سازی می‌شود. Shell فقط State رابط و Route داخلی را مدیریت می‌کند و داده را از مدل‌های منبع می‌خواند.

مدل سرویس پیشنهادی:

```python
class CasWorkspaceDashboard(models.AbstractModel):
    _name = "cas.workspace.dashboard"
```

متدهای پیشنهادی:

```python
get_navigation(role_context=None)
get_workspace_data(route=None)
get_page_data(route, query=None, offset=0, limit=25, filters=None, order=None)
get_record_detail(route, record_id)
execute_route_action(route, record_id, action_code, payload=None)
```

## امنیت

1. Query عادی بدون `sudo` اجرا شود.
2. `get_record_detail` دسترسی `read` رکورد منبع را بررسی کند.
3. Search، Order و Filter فقط از Whitelist همان Route پذیرفته شوند.
4. فیلدهای HTML خام، Binary و Relationهای حجیم در صفحه عمومی Serialize نشوند.
5. تصمیم، ثبت، تأیید، رد، ابطال و بازگشایی متد دامنه ماژول منبع را فراخوانی کنند.
6. Download و Export هم مجوز سند و هم مجوز رکورد منبع را کنترل کنند.
7. منو و صفحه فقط UX هستند؛ ACL، Record Rule و Method Check مرجع نهایی‌اند.

## Action Hub

Workspace نباید منطق تخصصی منبع را بازسازی کند. Action Item فقط شناسه منبع، مسئول، اولویت، Deadline، SLA و Route بازکردن رکورد را نگه می‌دارد.

## فرم و گردش‌کار

- Runtime فقط نسخه منتشرشده فرم را اجرا کند.
- Submission به نسخه فرم Pin شود.
- Workflow Instance به نسخه Workflow Pin شود.
- Designer فقط Draft را ویرایش کند.
- انتشار، ساختار، مسیر، Binding و مجوز را اعتبارسنجی کند.
- Approval نتیجه تصمیم را ثبت و Transition تعریف‌شده Workflow را فراخوانی کند.

## Jalali

- Date در ORM/PostgreSQL استاندارد بماند.
- Datetime در UTC ذخیره شود.
- تبدیل جلالی فقط در ورودی، نمایش، فیلتر و QWeb انجام شود.
- بازه Datetime در Timezone کاربر محاسبه شود.

## حالت‌های اجباری هر Route

- `loading`
- `empty`
- `forbidden`
- `unavailable`
- `error`
- `ready`

ماژول اختیاری نصب‌نشده باید `unavailable` کنترل‌شده برگرداند و Shell را Crash نکند.