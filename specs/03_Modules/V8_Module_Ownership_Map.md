# نقشه مالکیت ماژول‌ها و دامنه‌ها — v8

| مشخصه | مقدار |
|---|---|
| شناسه | `MODULE-OWNERSHIP-V8` |
| وضعیت | `Agreed` |
| نسخه | `v8 through iteration 12` |

## اصل مالکیت

هر داده کسب‌وکاری باید دقیقاً یک مالک داشته باشد. Workspace و Search مالکیت را تغییر نمی‌دهند.

| مفهوم / داده | مالک | مصرف‌کنندگان اصلی | مواردی که مالک نیست |
|---|---|---|---|
| Workspace Layout | `cas_workspace` | همه نقش‌ها | داده Widgetها |
| User UI Preference | `cas_workspace` | Shell, Dashboard | Preference کسب‌وکاری Domainها |
| Dashboard Configuration | `cas_workspace` | Workspace Shell | داده Provider |
| Provider Protocol | `cas_workspace_contract` | Workspace و Providerها | داده کسب‌وکاری |
| Personal Task | `cas_personal_task` | Workspace, Calendar Self Task | Action سازمانی |
| Personal Task Category | `cas_personal_task` | Personal Tasks UI | دسته Action Hub |
| Organizational Action | `cas_action_hub` | Workspace, Calendar Assignment | Personal Task |
| Employee / HR Identity | Odoo HR / Employee | Organization Core, Directory | Access Grant گزارش |
| Organization Scope | `cas_organization_core` | Calendar, Actions, Reports, Search | Permission اختصاصی Domain |
| Effective Assignment | `cas_organization_core` | Work Report, Calendar | Form Answer |
| Calendar Event | Calendar Domain | Workspace, Notifications | Assigned Action |
| Conversation / Message | Odoo Mail/Discuss | Workspace | Correspondence رسمی |
| Notification Delivery | Odoo Mail/Discuss/Bus | Notification Center | CAS Aggregation Policy |
| Notification Gap Extension | CAS Extension بعد از Gap Analysis | Notification Center | بازسازی Mail/Bus |
| Correspondence | Correspondence Domain | Workspace | Conversation |
| Work Report | `cas_work_report` | Workspace, Reviewer, Reporting | Form Definition |
| Work Report Section | `cas_work_report` | Reviewer, Reporting | Assignment Master |
| Work Report Access Grant | `cas_work_report` | Security Resolver | Organization Hierarchy |
| Report Profile | `cas_work_report` | Profile Resolver | Form Schema |
| Form Definition/Version | Form Engine | Work Report و فرم‌های دیگر | Report Lifecycle |
| Form Submission/Answer | Form Engine | Work Report | Workflow State |
| Workflow State | `cas_workflow_core` | Work Report و Domainها | Approval Decision |
| Approval Decision | `cas_approval_core` | Domainها | Workflow Definition |
| Activity Catalog | `cas_activity_catalog` | Work Report, Quick Activity | Activity Snapshot گزارش |
| Attachment Binary | Odoo Attachment / Document | Work Report, Form Engine | Evidence Semantics |
| Evidence Relation | `cas_work_report` | Reviewer, Audit | فایل Binary |
| Jalali Display/Input | Jalali Suite | همه UIها | تاریخ ذخیره‌شده اصلی |

## مالکیت Workspace

مجاز:

- Layout
- Widget Order
- Theme
- Density
- Sidebar State
- Command Palette UI
- Recent Resource Reference
- Dashboard Admin Configuration

ممنوع:

- ذخیره کپی Personal Task، Action، Report، Event، Message یا Document
- اعمال Business Rule ماژول Provider
- ایجاد رکورد Domain با دورزدن Service رسمی آن
- استفاده از `sudo` برای تجمیع داده غیرمجاز

## مالکیت دسترسی

- `cas_organization_core`: واقعیت سازمانی و Scope پایه
- Domain Owner: Permission خاص همان Domain
- `cas_work_report`: Access Grant و Section-level Report Access
- `cas_workspace`: فقط Capability و Navigation Presentation

## مالکیت State

- Form Submission State: Form Engine
- Process State: Workflow
- Approval Decision: Approval Core
- Report User-facing Projection: Work Report

Stateهای موازی نباید مستقل و متناقض تغییر کنند.

## قاعده توسعه

قبل از ایجاد مدل جدید باید مشخص شود:

1. آیا Odoo استاندارد مالک این مفهوم است؟
2. آیا یکی از ماژول‌های CAS مالک آن است؟
3. آیا مدل جدید فقط Projection یا Reference است؟
4. آیا ایجاد آن داده را کپی می‌کند؟
5. آیا Lifecycle و Security مستقل واقعی دارد؟

در صورت نبود پاسخ روشن، مدل جدید نباید ایجاد شود.