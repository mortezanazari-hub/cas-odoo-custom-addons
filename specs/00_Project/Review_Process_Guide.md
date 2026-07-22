---
document_id: GOV-REV-001
title: CAS Review Process Guide
document_type: Governance Guide
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
owner: Documentation Governance
domain_owner: Project Governance
created_at: 2026-07-22
updated_at: 2026-07-22
canonical: true
related_documents:
  - Documentation_Contribution_Guide.md
  - Cycle_Closeout_Checklist.md
---

# راهنمای اجرای Review Cycle و Iteration

## ۱. شروع Cycle

در ابتدای هر Cycle باید این موارد ثبت شوند:

- هدف و Scope؛
- صفحات، ماژول‌ها یا جریان‌های تحت بررسی؛
- نقش‌های درگیر؛
- Baseline ورودی؛
- موارد خارج از Scope؛
- Owner و Reviewerها.

## ۲. ساختار هر Iteration

هر Iteration باید بخش‌های زیر را داشته باشد:

1. ورودی‌ها و منابع بررسی‌شده؛
2. مشاهدات و مشکلات؛
3. تغییرات پیشنهادی؛
4. تصمیم‌های Accepted؛
5. موارد Rejected و دلیل؛
6. موارد Deferred؛
7. Gapهای فنی یا امنیتی؛
8. فایل‌ها و Registryهای تحت تأثیر؛
9. معیار پذیرش Iteration بعدی.

## ۳. طبقه‌بندی خروجی

هر یافته باید دقیقاً یکی از این خروجی‌ها را داشته باشد:

- Accepted Decision
- Rejected Proposal
- Deferred Open Item
- Implementation Gap
- Documentation Correction
- No Change Required

عبارت‌هایی مانند «بعداً بررسی شود» بدون Open Item ID قابل قبول نیستند.

## ۴. پایان Iteration

در پایان هر Iteration:

- Decision IDهای جدید استخراج شوند؛
- Page و Capabilityهای درگیر مشخص شوند؛
- Open Item و Gap ثبت شوند؛
- فایل‌های نیازمند Update فهرست شوند؛
- وضعیت Iteration روشن شود.

## ۵. پایان Cycle

Cycle فقط با تکمیل `Cycle_Closeout_Checklist.md` بسته می‌شود. آخرین Iteration نباید به‌تنهایی جایگزین Registryها یا Specificationهای فعال شود.

## ۶. قواعد Review رابط کاربری

- Prototype فقط Evidence طراحی است، نه Evidence پیاده‌سازی.
- Acceptance UI از Implementation Backend مستقل است.
- هر صفحه باید Page ID، Role، Route یا Entry Point، Data Owner و Capability داشته باشد.
- تغییر UI که رفتار کسب‌وکار یا امنیت را عوض می‌کند، نیازمند Decision و احتمالاً Architecture Review است.

## ۷. جلوگیری از انباشت Cycleها

در پایان هر Cycle باید یک خلاصه Current State تولید یا به‌روزرسانی شود. هدف این است که Cycle 50 بتواند مستقیماً از Baseline جاری شروع کند، نه اینکه برای فهم وضعیت، Cycleهای 1 تا 49 را دوباره بخواند.
