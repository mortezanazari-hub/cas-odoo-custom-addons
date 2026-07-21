# فهرست اسناد Historical و Superseded

| مشخصه | مقدار |
|---|---|
| وضعیت | `Consolidated` |
| نسخه فعال مرجع | `Workspace v8 through iteration 12` |

این فایل اسناد قدیمی را حذف نمی‌کند؛ فقط جایگاه مرجعیت آن‌ها را روشن می‌سازد.

## Historical Baselineهای نسخه ۷

- `02_UI_UX/Employee/Workspace.md`
- `02_UI_UX/Shared/Workspace_Shell.md`
- `03_Modules/V7_Module_Impact_And_New_Modules.md`
- `03_Modules/Cross_Module_V7_Impact_Assessment.md`
- `03_Modules/cas_workspace/V7_Impact_Assessment.md`
- `03_Modules/cas_action_hub/V7_Impact_Assessment.md`
- `03_Modules/cas_work_report/V7_Impact_Assessment.md`
- `05_Architecture/Workspace_UI_Integration_Notes.md`
- `06_ChangeSets/CS-WORKSPACE-V7.md`

مرجع فعال جایگزین:

- `02_UI_UX/Employee/Workspace_V8.md`
- `02_UI_UX/Shared/Workspace_Shell_V8.md`
- `00_Project/V8_Canonical_Baseline.md`
- معماری‌ها و Module Mapهای نسخه ۸

## Partially Superseded

### `DEC-009-Workspace-Route-And-Capability-Expansion.md`

بخش‌های Route مستقل Search و Recent History و Capability مستقل `history.read` توسط `DEC-016` جایگزین شده‌اند.

### اسناد پیشنهاد `cas_recent_history`

در v8 ماژول مستقل ایجاد نمی‌شود. Recent Resource Reference در Workspace UI Preference/History Layer باقی می‌ماند.

### اسناد پیشنهاد Notification Core کامل

ساخت Notification System کامل تصویب نشده است. Odoo Mail/Discuss/Bus Reuse می‌شود و Extension فقط پس از Gap Analysis مجاز است.

## اسناد فعال با منشأ قدیمی

Decisionهای `DEC-004` تا `DEC-011` در بخش‌هایی که با Baseline v8 سازگارند همچنان معتبرند. مرجعیت آن‌ها زیر Baseline و Decisionهای جدیدتر است.

## قاعده استناد

- برای طراحی جدید ابتدا اسناد فعال Indexشده خوانده شوند.
- Historical Document فقط برای فهم منشأ تصمیم یا اختلاف نسخه استفاده شود.
- هیچ Agent یا Developer نباید عبارت v7 را از سند Historical به‌عنوان Target فعلی اجرا کند.
- در تعارض، Canonical Baseline v8 مرجع است.

## انتقال فیزیکی

اسناد Historical فعلاً در مسیر اصلی خود باقی می‌مانند تا لینک‌های قبلی نشکنند. انتقال به پوشه Archive فقط در Change Set جداگانه و همراه Link Migration انجام می‌شود.