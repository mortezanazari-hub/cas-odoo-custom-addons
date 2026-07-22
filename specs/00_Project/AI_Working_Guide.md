---
document_id: GOV-AI-001
title: CAS AI Working Guide
document_type: AI Governance Guide
document_status: Active
implementation_status: N/A
ui_validation_status: N/A
owner: Documentation Governance
domain_owner: Project Governance
created_at: 2026-07-22
updated_at: 2026-07-22
canonical: true
related_documents:
  - Documentation_Map.md
  - Documentation_Contribution_Guide.md
  - Cycle_Closeout_Checklist.md
---

# راهنمای کار هوش مصنوعی با مستندات CAS

این سند برای ChatGPT، Codex، Agentها و هر ابزار هوش مصنوعی دیگری است که روی CAS کار می‌کند.

## ۱. ترتیب اجباری مطالعه

عامل هوش مصنوعی باید قبل از نتیجه‌گیری یا تغییر مستندات، به‌ترتیب این منابع را بخواند:

1. `Documentation_Map.md`
2. `Documentation_Contribution_Guide.md`
3. Registry مرتبط با موضوع
4. Specification فعال صفحه، ماژول یا معماری
5. Decisionهای مرتبط
6. آخرین Review Cycle مرتبط
7. اسناد Historical فقط در صورت نیاز به سابقه

## ۲. منابع با اولویت بالاتر

در تعارض میان منابع، این ترتیب رعایت شود:

```text
قانون و Constitution پروژه
→ Registry و Specification Canonical فعال
→ Decision فعال
→ Change Set مصوب
→ آخرین Review معتبر
→ اسناد Historical و گفتگوها
```

عامل هوش مصنوعی نباید صرفاً از روی آخرین فایل یا آخرین Cycle نتیجه بگیرد.

## ۳. ممنوعیت‌ها

AI نباید:

- تصمیم باز را قطعی اعلام کند؛
- Prototype را پیاده‌سازی‌شده فرض کند؛
- عنوان شغلی را معادل دسترسی امنیتی بداند؛
- فایل Historical را مرجع جاری معرفی کند؛
- ID جدید را بدون بررسی Registry بسازد؛
- سند قبلی را بدون رابطه Supersede حذف یا بی‌اعتبار کند؛
- برای پرکردن خلأ، نام ماژول، Capability، Route یا Owner ساختگی تعیین کند؛
- تغییر کد یا Core Odoo را از تغییر مستندات استنباط کند.

## ۴. قبل از ایجاد سند

AI باید بررسی کند:

- آیا سند مشابهی وجود دارد؟
- آیا موضوع باید در Registry موجود ثبت شود؟
- آیا Update سند فعال کافی است؟
- آیا Metadata و ID جدید یکتا هستند؟
- آیا این تغییر به Decision یا Change Set نیاز دارد؟

## ۵. بعد از هر تغییر

AI باید اثر تغییر را روی این موارد ارزیابی کند:

- Documentation Map
- Decision Registry
- Capability Registry
- Page Registry
- Role-to-Page Matrix
- Module Registry
- Open Item Registry
- Implementation Gap Registry
- Traceability Matrix
- Historical Document Register

## ۶. گزارش خروجی AI

در پایان کار باید روشن اعلام شود:

- چه فایل‌هایی ایجاد یا اصلاح شدند؛
- چه تصمیمی تغییر نکرد؛
- چه مواردی همچنان باز است؛
- آیا کد تغییر کرده است یا فقط مستندات؛
- تغییر روی کدام Branch یا PR قرار دارد؛
- چه اعتبارسنجی انجام شده است.

## ۷. Context Recovery در Cycleهای آینده

برای بازیابی سریع Context در Cycle 50 یا بالاتر، AI نباید همه Cycleها را از ابتدا بخواند. ابتدا Registryها و Baseline را استخراج کند و فقط Cycleهایی را بخواند که به شناسه‌های مرتبط لینک شده‌اند.

## ۸. اصل عدم جعل قطعیت

وقتی دو سند معتبر تعارض دارند یا مالک نهایی مشخص نیست، AI باید تعارض را در Open Item Registry ثبت یا گزارش کند؛ نه اینکه یکی را بدون شواهد انتخاب کند.
