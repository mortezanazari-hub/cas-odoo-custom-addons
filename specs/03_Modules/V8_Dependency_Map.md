# نقشه وابستگی ماژول‌های نسخه ۸

| مشخصه | مقدار |
|---|---|
| شناسه | `MODULE-DEPENDENCY-V8` |
| وضعیت | `Consolidated` |

## هدف

این سند جهت وابستگی‌ها را مشخص می‌کند تا Workspace به هسته مالکیت داده تبدیل نشود و Circular Dependency ایجاد نشود.

## لایه‌ها

```text
Odoo Standard Services
├── base / web / mail / bus / hr / calendar / attachment
│
CAS Foundation
├── cas_core
├── cas_workspace_contract
├── cas_organization_core
├── cas_activity_catalog
├── cas_form_core
├── cas_workflow_core
└── cas_approval_core
│
CAS Domain Modules
├── cas_personal_task
├── cas_action_hub
├── cas_work_report
├── correspondence modules
├── document modules
└── attendance / shift modules
│
CAS Experience Layer
├── cas_workspace
└── bridge / adapter modules
```

## قواعد جهت وابستگی

1. Foundation به Workspace وابسته نمی‌شود.
2. Domain Module برای ثبت Provider به `cas_workspace_contract` وابسته می‌شود، نه `cas_workspace`.
3. Workspace به Protocolها وابسته است و Providerها را در Runtime کشف می‌کند.
4. Bridge Module فقط Integration دو Domain را نگهداری می‌کند.
5. `cas_organization_core` به Work Report، Calendar یا Action Hub وابسته نمی‌شود.
6. `cas_work_report` می‌تواند از Organization، Form، Workflow و Approval استفاده کند.
7. `cas_form_core` به Work Report وابسته نمی‌شود.
8. `cas_activity_catalog` به Work Report وابسته نمی‌شود؛ Work Report مصرف‌کننده آن است.
9. Odoo Mail/Discuss/Bus زیرساخت Conversation و Notification Delivery باقی می‌ماند.

## وابستگی‌های پیشنهادی

| ماژول | وابستگی مستقیم مجاز | وابستگی ممنوع یا نامطلوب |
|---|---|---|
| `cas_workspace_contract` | `base` | Domain Modules, Workspace UI |
| `cas_organization_core` | `base`, `hr` | Work Report, Action Hub, Workspace |
| `cas_activity_catalog` | `base`, در صورت نیاز KPI Contract | Work Report, Workspace |
| `cas_personal_task` | `base`, `mail` اختیاری, Workspace Contract | `cas_workspace` |
| `cas_action_hub` | Foundation و Workflow/Approval در صورت نیاز | `cas_workspace` |
| `cas_work_report` | Organization, Form, Workflow, Approval, Activity Catalog | `cas_workspace` |
| `cas_workspace` | Workspace Contract, Web/UI و Adapterها | مالکیت مستقیم Domain Models |

## Bridgeهای پیشنهادی

در صورت نیاز برای جلوگیری از وابستگی‌های متقاطع:

- `cas_workspace_personal_task_bridge`
- `cas_workspace_action_hub_bridge`
- `cas_workspace_work_report_bridge`
- `cas_workspace_calendar_bridge`
- `cas_workspace_discuss_bridge`
- `cas_workspace_correspondence_bridge`
- `cas_workspace_document_bridge`
- `cas_workspace_attendance_bridge`

نام و تعداد نهایی Bridgeها در Specification اجرایی تعیین می‌شود. اصل مهم جداسازی مالکیت و جهت وابستگی است.

## Calendar

Calendar Event مالک مستقل دارد. ایجاد Self Task یا Assigned Action از Calendar از طریق Service رسمی Domain مقصد انجام می‌شود. Calendar نباید مدل Task موازی بسازد.

## Notifications

Workspace و Domainها نباید Mail/Bus موازی ایجاد کنند. Adapter فقط درخواست اعلان استاندارد، Deep Link و Metadata افزوده را تبدیل می‌کند.

## Work Report

```text
cas_work_report
├── cas_organization_core
├── cas_form_core
├── cas_workflow_core
├── cas_approval_core
├── cas_activity_catalog
├── shift / attendance contract
└── attachment / document contract
```

Dependency به Workspace ممنوع است. Workspace فقط Provider گزارش را مصرف می‌کند.

## معیار پذیرش

- هیچ Domain Module برای کارکرد اصلی به `cas_workspace` وابسته نباشد.
- Provider Contract بدون UI Runtime قابل نصب باشد.
- حذف Workspace داده یا Lifecycle Domainها را از کار نیندازد.
- Organization Scope در یک نقطه مشترک Resolve شود.
- Circular Dependency در Manifestها وجود نداشته باشد.