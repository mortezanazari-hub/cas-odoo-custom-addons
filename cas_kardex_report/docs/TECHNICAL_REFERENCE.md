# مرجع فنی استخراج‌شده از کد: CAS Kardex Reports

> این فایل از ساختار واقعی Python، XML، CSV و manifest همین ماژول تهیه شده است. برای مفهوم و سناریوی کاربری، فایل [معماری و راهنمای استفاده](ARCHITECTURE_AND_USAGE.md) را بخوانید.

## شناسنامه manifest

| مشخصه | مقدار |
|---|---|
| نام فنی | `cas_kardex_report` |
| نسخه | `19.0.1.0.1` |
| عنوان | CAS Kardex Reports |
| خلاصه | Detailed and summarized Excel reports for CAS Kardex |
| دسته | Human Resources |
| نوع برنامه | Technical/Extension |
| نصب خودکار | — |
| post-init hook | — |
| uninstall hook | — |
| وابستگی | `cas_kardex_management` |
| Python خارجی | xlsxwriter |

## ساختار بسته

| مسیر | تعداد فایل | مسئولیت معمول |
|---|---:|---|
| `models/` | 2 | مدل و منطق دامنه |
| `views/` | 1 | نما، action و menu |
| `security/` | 1 | گروه، ACL و record rule |
| `tests/` | 2 | آزمون خودکار |

## مدل‌ها و افزونه‌های ORM

### `cas.kardex.report.wizard` — کلاس `CasKardexReportWizard`

- منبع: `models/kardex_report.py:23`
- inherits: —
- توضیح فنی: CAS Kardex Excel Report Wizard

| فیلد | نوع | عنوان | رابطه | الزامی | فقط‌خواندنی | tracking | default | compute/store |
|---|---|---|---|---:|---:|---:|---|---|
| `date_from` | `Date` | از تاریخ | — | True | — | — | — | — |
| `date_to` | `Date` | تا تاریخ | — | True | — | — | — | — |
| `employee_id` | `Many2one` | کارمند | `hr.employee` | — | — | — | — | — |
| `department_id` | `Many2one` | واحد سازمانی | `hr.department` | — | — | — | — | — |
| `include_detail` | `Boolean` | گزارش تفصیلی | — | — | — | — | `True` | — |
| `include_summary` | `Boolean` | گزارش خلاصه | — | — | — | — | `True` | — |
| `include_draft` | `Boolean` | شامل روزهای نهایی‌نشده | — | — | — | — | — | — |

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `action_export()` | — | 35 |

### `cas.kardex.report.service` — کلاس `CasKardexReportService`

- منبع: `models/kardex_report.py:49`
- inherits: —
- توضیح فنی: CAS Kardex Excel Report Service

**متدها و hookها**

| متد | decorator | خط |
|---|---|---:|
| `_domain()` | — | 53 |
| `_detail_payload()` | — | 60 |
| `build_xlsx()` | — | 74 |

## گروه‌های امنیتی

گروه اختصاصی در XML این ماژول تعریف نشده است.

## ماتریس ACL

| ACL | مدل | گروه | Read | Write | Create | Unlink |
|---|---|---|---:|---:|---:|---:|
| `access_cas_kardex_report_wizard` | `model_cas_kardex_report_wizard` | `cas_kardex_management.group_cas_kardex_supervisor` | 1 | 1 | 1 | 1 |

## Record Ruleها

Record rule اختصاصی در XML این ماژول تعریف نشده است.

## منوها

| XML ID | عنوان | والد | action | گروه |
|---|---|---|---|---|
| `menu_cas_kardex_report` | گزارش Excel کاردکس | `cas_kardex_management.menu_cas_kardex_operations` | `action_cas_kardex_report_wizard` | `cas_kardex_management.group_cas_kardex_supervisor` |

## Actionها

| XML ID | نوع | عنوان | مدل/تگ | view mode | فایل |
|---|---|---|---|---|---|
| `action_cas_kardex_report_wizard` | `ir.actions.act_window` | گزارش Excel کاردکس | `cas.kardex.report.wizard` | `form` | `views/kardex_report_views.xml` |

## Cron و Sequence

Cron یا sequence اختصاصی در XML ندارد.

## Assetهای رابط کاربری

Asset اختصاصی ندارد.

## داده‌های بارگذاری‌شده از manifest

- `security/ir.model.access.csv`
- `views/kardex_report_views.xml`

## آزمون‌های موجود

- `tests/test_kardex_report.py`

## چک‌لیست اثر تغییر

- تغییر فیلد/مدل: migration، ACL، record rule، view، export و integrationها بررسی شوند.
- تغییر action/menu: گروه دسترسی، route Workspace و لینک‌های Action Hub بررسی شوند.
- تغییر state/action method: تاریخچه، idempotency، نقش تصمیم‌گیر و تست مسیر ناموفق بررسی شوند.
- تغییر asset: upgrade ماژول، compile bundle واقعی Odoo، hard refresh و QA موبایل/RTL انجام شود.
- تغییر cron: batch safety، چندشرکتی، retry، logging و اجرای هم‌زمان بررسی شود.
