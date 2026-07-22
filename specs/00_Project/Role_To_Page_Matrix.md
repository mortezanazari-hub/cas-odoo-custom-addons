---
document_id: REG-ROLE-PAGE-001
title: CAS Role-to-Page Matrix
document_type: Access Navigation Matrix
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
source_ui_review_cycle: CAS UI Review Cycle 10
source_iteration: 13
owner: Product, UX & Security Governance
domain_owner: Access Governance
created_at: 2026-07-22
updated_at: 2026-07-22
canonical: true
supersedes: []
superseded_by: []
related_decisions: [DEC-UIR09-010-CONSOLIDATED, DEC-UIR10-016-CONSOLIDATED]
related_modules: [cas_workspace]
related_pages: []
related_capabilities: []
---

# ماتریس نقش به صفحه CAS

این Matrix انتظار Navigation و عملیات را خلاصه می‌کند. عنوان شغلی به‌تنهایی دسترسی ایجاد نمی‌کند؛ دسترسی واقعی از Group، Capability، ACL، Record Rule، Scope و Method Check به‌دست می‌آید.

## راهنما

- `✓` دسترسی پایه با Capability متناظر؛
- `S` فقط در Scope مجاز؛
- `A` نیازمند Capability مدیریتی/حساس؛
- `—` بدون دسترسی پایه؛
- `P` Page/Route یا Policy هنوز نیازمند Specification تکمیلی است.

## ماتریس اصلی

| صفحه/Surface | کاربر عادی | سرپرست | مدیر واحد | Reviewer/ممیز | مدیرعامل/مدیر ارشد | مدیر سامانه تفکیکی | کارشناس اداری مجاز | نگهبان |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Workspace Home | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Personal Tasks | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Calendar | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | طبق Capability |
| Conversations | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | طبق Capability |
| Command Palette / Search | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Notification Center | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| My Work Report | طبق Applicability | طبق Applicability | طبق Applicability | طبق Applicability | طبق Applicability | طبق Applicability | طبق Applicability | طبق Applicability |
| Team Review | — | S | S | S | S/A | فقط با Scope | S | — |
| Delegated Work Report Monitoring | — | با Grant | با Grant | S | S | با Grant | با Grant | — |
| My Delegations | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Delegation Management | — | — | در صورت Capability | A | A | A | — | — |
| Dashboard Management Center | — | — | — | Audit only در صورت Capability | A | A | — | — |
| Attendance Correction Request | ✓ | ✓ برای خود | ✓ برای خود | — | — | — | ✓ برای خود | ✓ برای خود |
| Attendance Correction Approval | — | S | S | — | A در Escalation | — | — | — |
| Random Attendance Audit | — | با Grant | با Grant | S | مشاهده/تصمیم Escalation | Audit viewer فقط read | — | — |
| Overtime own/request/history/cancel | طبق Capability | طبق Capability | طبق Capability | طبق Capability | طبق Capability | — | طبق Capability | طبق Capability |
| Secretariat Incoming | — | — | — | — | طبق Capability | تنظیم دسترسی، نه عملیات عادی | A | — |
| Secretariat Outgoing Final Registry | — | — | — | — | طبق Capability | تنظیم دسترسی، نه عملیات عادی | A | — |
| Secretariat Register/Reports | — | — | طبق Capability | Audit Scope | طبق Capability | Audit viewer read-only | A | — |
| Guard Attendance Station | — | — | — | گزارش مستقل، نه Station | — | تنظیم دسترسی | — | A |
| System User/Access Management | — | — | — | Audit only | A | گروه `user/access manager` | — | — |
| Organization Management | — | — | — | Audit only | A | گروه `organization manager` | — | — |
| Settings Management | — | — | — | Audit only | A | گروه `settings manager` | — | — |
| Audit Viewer | — | — | در صورت Capability | A/read-only | A | گروه `audit viewer` read-only | — | — |

## قواعد نقش‌ها

### کاربر عادی

- فقط Scope و رکوردهای خودش یا Grant معتبر را می‌بیند.
- در فرم عمومی تفویض، صاحب اختیار همان کاربر جاری و readonly است.
- عنوان شغلی هیچ Capability مدیریتی خودکار ایجاد نمی‌کند.

### سرپرست و مدیر واحد

- رابطه سازمانی فقط Scope پایه می‌دهد؛ عملیات approve/export/audit نیازمند Capability جداست.
- Random audit یا دسترسی گزارش خارج از Hierarchy فقط با Grant زمان‌دار مجاز است.

### Reviewer و ممیز

- Reviewer الزاماً مدیر مستقیم نیست.
- دسترسی Report Header به معنی دسترسی همه Sectionها نیست.
- Export و Aggregate باید همان Field/Section filtering را اعمال کنند.

### مدیرعامل/مدیر ارشد

- نقش تجمیعی از گروه‌های مصوب ساخته می‌شود؛ گروه مطلق و دورزننده امنیت نیست.
- Escalation مدیرعامل مجوز عمومی مشاهده همه داده‌ها ایجاد نمی‌کند.

### مدیر سامانه

مدیریت سامانه به گروه‌های مستقل تقسیم می‌شود:

1. user/access manager؛
2. organization manager؛
3. delegation manager؛
4. settings manager؛
5. audit viewer؛
6. composite super administrator.

`audit viewer` read-only است و عنوان شغلی «مسئول IT» هیچ Group Membership خودکار ایجاد نمی‌کند.

### کارشناس اداری و دبیرخانه

دبیرخانه Access Domain است. کارشناس اداری فقط با Capability مشخص به وارده، صادره، دفتر یا گزارش دسترسی می‌گیرد.

### نگهبان

- ایستگاه نگهبانی صفحه عملیاتی ثبت Batch است، نه گزارش مدیریتی یا ویرایش مستقیم رخداد رسمی.
- Scope شرکت، سایت و کارکنان server-side enforce می‌شود.
- زمان دستی و عبور از Conflict قابلیت‌های حساس مستقل‌اند.

## وضعیت تکمیل

Pageهای Attendance Correction، Random Audit، Overtime و بخش‌های تفصیلی Admin Center هنوز Page Specification مستقل کامل ندارند و در [Page Registry](Page_Registry.md) و [Open Item Registry](Open_Item_Registry.md) با وضعیت باز ثبت شده‌اند.
