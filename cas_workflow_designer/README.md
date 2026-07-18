# CAS Workflow Designer

> نسخه: `19.0.1.0.0` · Odoo 19 Community

طراح node-based گردش کار و اتصال گره‌های فرایند به فرم‌ها.

## اجزای ماژول

- افزونه definition/version/state
- `action_open_node_designer`: ورود به بوم
- `action_start_submission`: شروع فرم متصل
- بوم OWL در JS/XML/SCSS
- binding وضعیت به نسخه فرم

## نقش‌ها

طراح، منتشرکننده و مدیر گردش کار.

## روش کار

1. نسخه پیش‌نویس را باز کنید.
2. گره‌ها را بسازید و با یال جهت‌دار وصل کنید.
3. برای گره داده‌گیر نسخه فرم را bind کنید.
4. آغاز، پایان، مسئولیت و گذارها را تنظیم و ذخیره کنید.
5. پس از کنترل دسترسی‌پذیری، نسخه را منتشر کنید.

## منوها

از نسخه پیش‌نویس گردش کار باز می‌شود؛ منوی روزمره ندارد.

## نصب و ارتقا

وابستگی‌ها: `cas_workflow_core`، `cas_form_core`، `web`.

```bash
./odoo-bin -d <database> -i cas_workflow_designer --stop-after-init
./odoo-bin -d <database> -u cas_workflow_designer --stop-after-init
```

## قواعد کلیدی

- نسخه منتشرشده قفل است.
- هر مسیر باید از آغاز دست‌پذیر باشد.
- binding باید به نسخه فرم معتبر اشاره کند.

## آزمون‌ها

آزمون‌های concurrency، reachability، published lock و form binding.

جزئیات معماری و سناریوها: [راهنمای کامل](docs/ARCHITECTURE_AND_USAGE.md).
