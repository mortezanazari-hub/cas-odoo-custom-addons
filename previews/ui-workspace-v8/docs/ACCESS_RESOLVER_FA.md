# قرارداد Access Resolver در نمونه رابط CAS

این نمونه منو را از ترکیب نقش‌های امنیتی هر کاربر آزمایشی و متادیتای Route می‌سازد.

در نسخه Production:

1. کاربر از Session واقعی Odoo دریافت شود.
2. نقش‌ها و گروه‌ها از Backend و بدون `sudo` خوانده شوند.
3. حوزه شرکت، سایت، واحد، سمت، جانشینی و دسترسی موقت در پاسخ Resolver قرار گیرد.
4. Frontend فقط Routeها و عملیات مجاز را نمایش دهد.
5. ACL، Record Rule و کنترل متد سمت سرور مستقل از UI اجرا شوند.
6. انتخاب‌گر «کاربر آزمایشی» در Build تولیدی حذف شود.

پاسخ پیشنهادی Resolver:

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
