---
document_id: INDEX-UI-001
title: UI and UX Documentation Index
document_type: Section Index
document_status: Active
implementation_status: N/A
ui_validation_status: Pending Revalidation
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Product UX Governance
domain_owner: Page Governance
created_at: N/A
updated_at: 2026-07-22
canonical: true
supersedes: []
superseded_by: []
related_decisions: [DEC-UIR09-010-CONSOLIDATED, DEC-UIR10-016-CONSOLIDATED]
related_modules: [cas_workspace]
related_pages: []
related_capabilities: []
---

# 02 — UI & UX

این بخش Page Specificationها و Shared UI Component Specificationهای CAS را نگهداری می‌کند.

> آخرین چرخه فعال بازنگری UI: **Cycle 10 — Through Iteration 13**  
> وضعیت Production UI برای تغییرات Cycle 10: `Pending Revalidation`.

## Navigation مرکزی

- [Page Registry](../00_Project/Page_Registry.md)
- [Role-to-Page Matrix](../00_Project/Role_To_Page_Matrix.md)
- [Capability Registry](../00_Project/Capability_Registry.md)
- [Implementation Gap Registry](../00_Project/Implementation_Gap_Registry.md)

## صفحات پایه Workspace

- [میزکار Workspace](Employee/Workspace_V8.md)
- [کارهای شخصی](Employee/Personal_Tasks.md)
- [تقویم](Employee/Calendar.md)
- [گفت‌وگوها](Employee/Conversations.md)
- [Command Palette و Search](Employee/Global_Search.md)
- [مرکز اعلان‌ها](Employee/Notifications_Center.md)
- [Recent History داخل Command Palette](Employee/Recent_History.md)
- [گزارش کار پویا و شیفت‌محور](Employee/Dynamic_Work_Report.md)
- [Workspace Shell](Shared/Workspace_Shell_V8.md)

## صفحات و کامپوننت‌های Cycle 10

- [تفویض‌های من و مدیریت تفویض](Employee/Delegation.md)
- [Shared People Picker](Common/Shared_People_Picker.md)
- [دبیرخانه و دفتر وارده/صادره](Administrative/Secretariat.md)
- [ایستگاه سریع ثبت تردد نگهبانی](Security/Guard_Attendance_Station.md)

## صفحات مدیریتی

- [مرکز مدیریت داشبورد](Admin/Dashboard_Management_Center.md)
- سایر Pageهای تفصیلی Admin Center برای user/access، organization، settings و audit در [Open Item Registry](../00_Project/Open_Item_Registry.md) ثبت شده‌اند.

## Surfaceهای دارای Decision ولی فاقد Page Spec کامل

- Attendance Correction Request/Ledger؛
- Delegated Random Attendance Audit؛
- Overtime صفحات own/request/history/cancel؛
- Form Builder Activity Providers و Dynamic Matrix؛
- جریان‌های جزئی مکاتبات متأثر از Cycle 10.

این موارد در Page Registry و Gap Registry ثبت شده‌اند و نباید از روی Prototype یا کد فعلی حدس زده شوند.

## Historical و Superseded

- `Employee/Workspace.md` و `Shared/Workspace_Shell.md` منابع Historical Cycle 7 هستند؛
- Routeهای مستقل `global-search-page` و `recent-history` Superseded شده‌اند؛
- UI لیستی ثبت نگهبانی با Cycle 10 Superseded شده است؛
- OCR و DMS Navigation در آلفا خارج از Scope هستند.

## الزامات هر Page Specification

Page ID، عنوان، Route/Entry، Roles، Capability، Owner، Source Cycle/Iteration، Goal، States، Actions، Data Sources، Security، RTL، Responsive، Accessibility، Performance، Module Impact، Acceptance و Revalidation Scenario باید مشخص باشند.
