# چرخه بازنگری UI و حلقه تضمین کیفیت CAS

| مشخصه | مقدار |
|---|---|
| شناسه | `PROC-UI-REVIEW-LIFECYCLE` |
| وضعیت | `Active` |
| نوع سند | Process / Governance |
| مالک | Product & Architecture Governance |
| آخرین چرخه فعال | `CAS UI Review Cycle 8 — Through Iteration 12` |

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
Cycle 8 / Iteration 12
```

یعنی دوازدهمین اصلاح داخلی در هشتمین چرخه بازنگری UI.

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

## 5. ورود Cycle جدید

هنگام ورود Cycle 9:

1. Cycle 9 آخرین چرخه فعال بازنگری UI می‌شود.
2. Cycle 8 به‌عنوان منبع تاریخی بازنگری باقی می‌ماند.
3. تصمیم‌های Active کشف‌شده در Cycle 8 خودکار باطل نمی‌شوند.
4. تفاوت‌های Cycle 9 با اسناد Active استخراج می‌شوند.
5. فقط تصمیم‌های صریحاً تغییرکرده Supersede می‌شوند.
6. Change Set جدید ساخته می‌شود.
7. Traceability به‌روزرسانی می‌شود.
8. Backend Impact برای تغییرات جدید ثبت می‌شود.
9. سناریوهای Revalidation تعریف می‌شوند.

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

## 9. نتیجه نهایی

هدف Cycle تولید «نسخه نهایی نرم‌افزار» نیست؛ هدف کشف و ثبت دقیق تغییرات لازم برای نزدیک‌ترشدن UI و Backend به محصول باکیفیت نهایی است.
