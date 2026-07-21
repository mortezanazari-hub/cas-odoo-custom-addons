# قرارداد پیشنهادی اتصال رابط به Odoo 19 Community

## معماری پیشنهادی

رابط به‌عنوان OWL Client Action در `cas_workspace` پیاده‌سازی شود. پوسته فقط state رابط و route داخلی را مدیریت کند و داده را از مدل‌های منبع بخواند.

### سرویس Backend

مدل پیشنهادی:

```python
class CasWorkspaceDashboard(models.AbstractModel):
    _name = "cas.workspace.dashboard"
```

متدهای اصلی:

```python
@api.model
get_navigation(role_context=None)

@api.model
get_workspace_data(route=None)

@api.model
get_page_data(route, query=None, offset=0, limit=25, filters=None, order=None)

@api.model
get_record_detail(route, record_id)

@api.model
execute_route_action(route, record_id, action_code, payload=None)
```

## قرارداد امنیت

1. Query عادی بدون `sudo` اجرا شود.
2. هر `get_record_detail` قبل از serialization، دسترسی `read` رکورد منبع را بررسی کند.
3. `search`, `order` و `filters` فقط از whitelist همان route پذیرفته شوند.
4. فیلدهای HTML خام، Binary و رابطه‌های حجیم در صفحه عمومی serialize نشوند.
5. عملیات تصمیم، ثبت، تأیید، رد، ابطال و بازگشایی مستقیماً متد دامنه ماژول منبع را فراخوانی کند.
6. Export و Download هم مجوز سند و هم مجوز رکورد منبع را کنترل کنند.
7. صفحه و منو فقط UX هستند؛ ACL، Record Rule و کنترل متد مرجع نهایی‌اند.

## PAGE_CONFIG نمونه

```python
PAGE_CONFIGS = {
    "my-actions": {
        "model": "cas.action.item",
        "domain": lambda env: [("responsible_user_id", "=", env.user.id)],
        "fields": ["name", "source_label", "deadline", "priority", "status"],
        "search_fields": ["name", "resource_display_name"],
        "order_fields": ["deadline", "priority", "create_date"],
    },
    "correspondence": {
        "model": "cas.correspondence.letter",
        "fields": ["number", "subject", "sender_id", "state", "confidentiality"],
        "search_fields": ["number", "subject"],
    },
    "documents": {
        "model": "cas.document",
        "fields": ["name", "folder_id", "current_version_id", "state", "tag_ids"],
        "search_fields": ["name", "tag_ids.name"],
    },
}
```

## قرارداد Action Hub

Workspace یا Action Hub نباید منطق تخصصی منبع را بازسازی کند. آیتم اقدام فقط شامل شناسه منبع، مسئول، اولویت، deadline، SLA و route بازکردن رکورد باشد. پس از اجرای متد رکورد منبع، Adapter وضعیت آیتم را همگام کند.

## قرارداد فرم و گردش‌کار

- Runtime فقط نسخه منتشرشده فرم را اجرا کند.
- Submission به نسخه فرم pin شود.
- Workflow Instance به نسخه گردش‌کار pin شود.
- Designer فقط نسخه Draft را ویرایش کند.
- انتشار باید اعتبارسنجی ساختار، مسیر، binding و مجوز را اجرا کند.
- Approval نتیجه تصمیم را ثبت کند و transition تعریف‌شده Workflow را فراخوانی کند.

## قرارداد تاریخ جلالی

- Date در ORM/PostgreSQL استاندارد باقی بماند.
- Datetime در UTC ذخیره شود.
- تبدیل جلالی فقط در مرز ورودی، نمایش، فیلتر و QWeb انجام شود.
- فیلتر Datetime، کران بالای بازه را ابتدای روز بعد در timezone کاربر محاسبه کند.

## حالت‌های اجباری صفحه

هر route باید حالت‌های زیر را مستقل نمایش دهد:

- `loading`
- `empty`
- `forbidden`
- `unavailable`
- `error`
- `ready`

مدل اختیاری نصب‌نشده باید `unavailable` کنترل‌شده برگرداند و باعث crash پوسته نشود.

## پیشنهاد تفکیک Asset

```text
cas_workspace/static/src/
├── app/
│   ├── workspace_app.js
│   ├── workspace_app.xml
│   └── workspace_app.scss
├── core/
│   ├── router.js
│   ├── rpc_service.js
│   ├── permission_service.js
│   └── formatters.js
├── pages/
│   ├── dashboard/
│   ├── action_hub/
│   ├── forms/
│   ├── workflow/
│   ├── correspondence/
│   ├── documents/
│   ├── attendance/
│   ├── kardex/
│   └── work_report/
└── components/
    ├── sidebar/
    ├── data_table/
    ├── detail_drawer/
    ├── jalali_filter/
    └── state_panel/
```
