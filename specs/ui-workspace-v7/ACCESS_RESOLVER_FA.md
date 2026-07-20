# قرارداد Access Resolver در Workspace

## اصل

منو و Routeها از ترکیب نقش‌های امنیتی، Scope سازمانی و Capabilityهای مؤثر کاربر ساخته می‌شوند.

## قواعد Production

1. کاربر از Session واقعی Odoo دریافت شود.
2. نقش‌ها و گروه‌ها از Backend و بدون `sudo` خوانده شوند.
3. Scope شرکت، سایت، واحد، سمت، جانشینی و دسترسی موقت در پاسخ Resolver قرار گیرد.
4. Frontend فقط Routeها و عملیات مجاز را نمایش دهد.
5. ACL، Record Rule و کنترل متد مستقل از UI اجرا شوند.
6. Role Switch آزمایشی در Build تولیدی حذف شود.

## پاسخ پیشنهادی

```json
{
  "user_id": 42,
  "workspaces": ["personal", "production_supervision"],
  "routes": ["home", "my-actions", "team-work-reports"],
  "capabilities": ["work_report.read_team", "approval.decide"],
  "scopes": {
    "company_ids": [1],
    "department_ids": [8, 9],
    "employee_ids": [42, 43, 44]
  }
}
```

## اصل امنیتی

عدم نمایش Route یا دکمه صرفاً یک بهبود UX است و نباید جایگزین کنترل سمت سرور شود.