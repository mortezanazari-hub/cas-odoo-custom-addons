# چرخه بازنگری UI و حلقه تضمین کیفیت CAS

| مشخصه | مقدار |
|---|---|
| شناسه | `PROC-UI-REVIEW-LIFECYCLE` |
| وضعیت | `Active` |
| نوع سند | Process / Governance |
| مالک | Product & Architecture Governance |
| آخرین چرخه فعال | `CAS UI Review Cycle 9 — Through Iteration 13` |

## 1. هدف

این سند مشخص می‌کند نسخه‌های UI در پروژه CAS چه معنایی دارند و چگونه خروجی بازنگری UI به تغییرات Backend، ماژول‌ها و اعتبارسنجی نهایی تبدیل می‌شود.

## 2. تعریف UI Review Cycle

`UI Review Cycle` یک بازنگری کلی رابط کاربری است که برای مشاهده، نقد و کشف نیازهای محصول انجام می‌شود.

شماره Cycle:

- شماره نسخه نرم‌افزار نیست؛
- شماره Release محصول نیست؛
- قرارداد سازگاری API نیست؛
- نشان‌دهنده بلوغ یا نهایی‌بودن کل سامانه نیست؛
- فقط ترتیب چرخه‌های بازنگری UI را نشان می‌دهد.

## 3. تعریف Iteration

Iteration اصلاح داخلی درون یک Cycle است. مثال:

```text
Cycle 9 / Iteration 13
```

یعنی سیزدهمین اصلاح داخلی در نهمین چرخه بازنگری UI.

## 4. چرخه QA

```text
Backend Existing State
→ UI Build
→ UI Review
→ Observation
→ Decision
→ Module Impact
→ Backend Specification
→ Implementation
→ Tests
→ UI Revalidation
→ Accepted / Reopened
```

## 5. وضعیت Cycle 9

1. Cycle 9 آخرین چرخه فعال بازنگری UI است.
2. Cycle 8 به‌عنوان منبع تاریخی بازنگری باقی می‌ماند.
3. تصمیم‌های Active کشف‌شده در Cycle 8 خودکار باطل نشده‌اند.
4. فقط موارد صریح ثبت‌شده در `UI_Review_Cycle_9_Register.md` Supersede شده‌اند.
5. Change Set مرجع Cycle 9 برابر `../06_ChangeSets/CS-UIR09-WORKSPACE-UX-CONSOLIDATION.md` است.
6. تصمیم تجمیعی Cycle 9 برابر `../04_Decisions/DEC-010-UIR09-Consolidated-Workspace-And-Operational-UX.md` است.
7. وضعیت UI Prototype تا Iteration 13 به‌عنوان Review Baseline پذیرفته شده است.
8. وضعیت Backend همچنان `Gap Identified` و اعتبارسنجی Production برابر `Pending Revalidation` است.

## 6. مرجع مؤثر

مرجع Backend مجموعه اسناد Active است، نه آخرین Cycle به‌تنهایی:

```text
Active Decisions
+ Active Module Specs
+ Active Architecture and Security Contracts
+ Approved Changes from Latest UI Review
- Superseded Requirements
```

## 7. وضعیت‌های Observation

- `Open`
- `Triaged`
- `Decision Required`
- `Accepted`
- `Rejected`
- `Converted to Gap`
- `Implemented`
- `Pending Revalidation`
- `Validated`
- `Reopened`

## 8. الزامات هر Observation

هر Observation باید دارای این فیلدها باشد:

- ID
- UI Review Cycle
- Iteration
- Page
- Role
- Scenario
- Current Behavior
- Problem or Opportunity
- Evidence
- Severity
- Related Module
- Related Decision
- Status
- Owner

## 9. ورود Cycle بعدی

هنگام ورود Cycle 10:

1. Cycle 10 آخرین چرخه فعال می‌شود.
2. Cycle 9 حذف نمی‌شود و Historical Review Source خواهد شد.
3. تصمیم‌های Active Cycle 9 فقط با Supersede صریح تغییر می‌کنند.
4. تغییرات CSS و تنظیمات پیشرفته Widget که در Cycle 9 Deferred شده‌اند باید Observation و Decision مستقل بگیرند.
5. Traceability، Version History، Change Set و Revalidation Plan باید هم‌زمان اصلاح شوند.

## 10. نتیجه نهایی

هدف Cycle تولید «نسخه نهایی نرم‌افزار» نیست؛ هدف کشف و ثبت دقیق تغییرات لازم برای نزدیک‌ترشدن UI و Backend به محصول باکیفیت نهایی است.
