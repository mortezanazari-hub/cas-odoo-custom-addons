# ماتریس ردیابی چرخه UI تا پیاده‌سازی

| مشخصه | مقدار |
|---|---|
| وضعیت | `Active` |
| هدف | ردیابی کامل Observation تا UI Revalidation |
| مرجع | `UI_Review_Lifecycle.md` |

## مسیر اجباری

```text
UI Observation
→ Decision
→ Page Specification
→ Module Impact
→ Backend Requirement
→ Architecture/Security
→ Implementation
→ Test Evidence
→ UI Revalidation
→ Accepted / Reopened
```

## ستون‌های اجباری

| ستون | توضیح |
|---|---|
| Observation ID | مشاهده منبع |
| UI Review Cycle | Cycle و Iteration |
| Page / Role / Scenario | محل کشف |
| Decision ID | تصمیم حاصل |
| Page Spec | سند UI |
| Module Owner | مالک Domain |
| Affected Modules | ماژول‌های متأثر |
| Backend Requirement | تغییر دقیق |
| Security Reference | امنیت |
| Change Set | بسته تغییر |
| Implementation Status | وضعیت اجرا |
| Implementation Evidence | PR/Commit/Ticket |
| Test Evidence | شواهد آزمون |
| Revalidation Cycle | Cycle بازآزمایی |
| Revalidation Result | نتیجه |
| Final Status | Accepted/Reopened |
| Supersedes | تصمیم قبلی |

## قواعد

1. ردیف بدون Observation برای تغییر UI ناقص است.
2. ردیف بدون Module Owner برای Backend ناقص است.
3. `Implemented` بدون Evidence مجاز نیست.
4. `Accepted` بدون UI Revalidation مجاز نیست.
5. Cycle جدید ردیف‌های قبلی را حذف نمی‌کند.
6. تصمیم تغییرکرده باید Supersede صریح داشته باشد.
7. یک Requirement می‌تواند در چند Cycle اعتبارسنجی شود.
8. Version نرم‌افزار فقط در صورت Release واقعی ثبت می‌شود.

## وضعیت فعلی

Cycle 8 آخرین Cycle فعال بازنگری UI است. این وضعیت با ورود Cycle 9 تغییر می‌کند، اما تصمیم‌های Active تنها با Supersede صریح تغییر می‌کنند.
