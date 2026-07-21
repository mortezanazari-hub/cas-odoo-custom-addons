# System Context — CAS Workspace v8

| مشخصه | مقدار |
|---|---|
| وضعیت | `Consolidated` |
| نسخه | `v8 through iteration 12` |

## سیستم

CAS یک Workspace سازمانی اختصاصی روی Odoo 19 Community است. هیچ تغییری در Odoo Core انجام نمی‌شود و تمام قابلیت‌ها از Custom Addons، Serviceها، Registryها و Extensionهای استاندارد پیاده می‌شوند.

## بازیگران

- کاربر عادی
- سرپرست
- مدیر
- مدیرعامل
- نگهبان و نقش‌های عملیاتی
- مسئول کنترل عملکرد
- Reviewer و Approver
- ممیز
- Workspace Administrator
- System Administrator

## سیستم‌های داخلی

```text
Users
  ↓
CAS Workspace Experience
  ↓ Provider Contracts / Domain Services
CAS Domain Modules
  ↓
Odoo Standard Platform
  ├── Web Client
  ├── ORM / Security
  ├── Mail / Discuss / Bus
  ├── HR / Employee
  ├── Calendar
  ├── Attachment
  └── PostgreSQL
```

## سیستم‌های بیرونی فعلی و آینده

- Reverse Proxy و SSO، در صورت فعال‌سازی
- Email Server
- Nextcloud، در نسخه آینده Document Integration
- سرویس‌های HR یا Attendance خارجی، در صورت اتصال
- ابزارهای Reporting یا BI، فقط از API/Projection امن

## مرز Workspace

Workspace شامل UI Shell، Navigation، Command Palette، Dashboard Configuration و Provider Orchestration است. Business Data و Lifecycleها خارج از این مرز و نزد Domain Owner قرار دارند.

## جریان‌های کلیدی

### ورود روزانه

1. کاربر وارد Workspace می‌شود.
2. Shell Capability و Navigation را Resolve می‌کند.
3. Dashboard Policy و Preference Resolve می‌شوند.
4. Widget Providers داده مجاز را مستقل عرضه می‌کنند.

### Search

1. کاربر Command Palette را باز می‌کند.
2. `search.use` و Context بررسی می‌شود.
3. Query به Providerهای فعال ارسال می‌شود.
4. هر Provider Permission منبع را enforce می‌کند.
5. نتایج مجاز Group و Rank می‌شوند.

### گزارش کار

1. Shift Occurrence و Applicability Resolve می‌شوند.
2. Assignmentهای مؤثر Resolve می‌شوند.
3. Report و Sectionها Idempotent ایجاد می‌شوند.
4. Form Version هر Section Pin می‌شود.
5. Submit، Review و Approval از Workflow/Approval استفاده می‌کنند.

### دسترسی کنترل عملکرد

1. Organization Scope پایه Resolve می‌شود.
2. Work Report Access Grant بررسی می‌شود.
3. Section و Operation مجاز تعیین می‌شوند.
4. View یا Export فقط روی Projection مجاز اجرا می‌شود.

## Trust Boundaries

- Browser غیرقابل اعتماد است.
- Company و Scope ارسالی Client باید Validate شوند.
- Deep Link Permission را دوباره بررسی می‌کند.
- Provider و Domain Service مرز اعمال Security هستند.
- فایل و Export باید Access Token و Retention امن داشته باشند.

## الزامات سراسری

- RTL و Jalali UI
- Multi-company
- Auditability
- Accessibility
- Performance در Directory و Search بزرگ
- Partial Failure Handling
- Idempotency در Flowهای Cross-domain
- Observability بدون افشای داده حساس