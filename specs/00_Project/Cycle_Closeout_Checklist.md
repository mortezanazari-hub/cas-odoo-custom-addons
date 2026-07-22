---
document_id: GOV-DOC-002
title: CAS Cycle Closeout Checklist
document_type: Governance Checklist
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
  - Documentation_Map.md
---

# چک‌لیست اجباری پایان Cycle

این چک‌لیست باید در پایان هر Cycle یا Review عمده تکمیل شود. وجود فایل‌های Review بدون انتقال نتیجه به مراجع Canonical به معنی بسته‌شدن Cycle نیست.

## A. مشخصات Cycle

- [ ] Cycle ID و شماره Iterationها یکتا و ثبت شده‌اند.
- [ ] Scope بررسی روشن است.
- [ ] آخرین Iteration معتبر مشخص شده است.
- [ ] وضعیت Cycle شامل Draft، Under Review یا Closed مشخص است.
- [ ] مالک Review و تاریخ بسته‌شدن ثبت شده‌اند.

## B. خروجی Review

- [ ] موارد Accepted ثبت شده‌اند.
- [ ] موارد Rejected با دلیل ثبت شده‌اند.
- [ ] موارد Deferred در Open Item Registry ثبت شده‌اند.
- [ ] موارد نیازمند پیاده‌سازی در Implementation Gap Registry ثبت شده‌اند.
- [ ] هیچ تصمیمی فقط در متن گفتگو یا فایل Iteration باقی نمانده است.

## C. Decision Governance

- [ ] همه تصمیم‌های جدید ID یکتا دارند.
- [ ] `Decision_Registry.md` به‌روزرسانی شده است.
- [ ] تصمیم‌های جایگزین‌شده `Superseded` شده‌اند.
- [ ] روابط `supersedes` و `superseded_by` دوطرفه هستند.
- [ ] تصمیم‌های قدیمی بدون دلیل باطل نشده‌اند.
- [ ] تصمیم‌های باز به‌اشتباه Agreed یا Active اعلام نشده‌اند.

## D. Page و UI Governance

- [ ] همه صفحات جدید در `Page_Registry.md` ثبت شده‌اند.
- [ ] Page ID، Route، Owner و Roleها مشخص‌اند.
- [ ] وضعیت Backend و UI جدا ثبت شده‌اند.
- [ ] Page Specificationهای تحت تأثیر به‌روزرسانی شده‌اند.
- [ ] صفحات حذف‌شده یا جایگزین‌شده Historical/Superseded شده‌اند.
- [ ] `Role_To_Page_Matrix.md` بررسی و در صورت نیاز اصلاح شده است.

## E. Capability و Security

- [ ] Capabilityهای جدید در `Capability_Registry.md` ثبت شده‌اند.
- [ ] Capability Owner و Consumer مشخص است.
- [ ] هیچ Capability جای ACL، Record Rule یا Method Check معرفی نشده است.
- [ ] تغییر نقش یا Scope در ماتریس دسترسی منعکس شده است.
- [ ] موارد امنیتی حل‌نشده در Open Item Registry ثبت شده‌اند.

## F. Module و Architecture

- [ ] `Module_Registry.md` برای مالک فنی و وضعیت وجود ماژول بررسی شده است.
- [ ] بین ماژول موجود و ماژول صرفاً پیشنهادی تفکیک وجود دارد.
- [ ] Specification ماژول‌های تحت تأثیر اصلاح شده است.
- [ ] قراردادهای معماری تحت تأثیر به‌روزرسانی شده‌اند.
- [ ] هیچ تغییر معماری بدون Decision یا Change Set رها نشده است.

## G. Open Items و Gaps

- [ ] Open Itemهای جدید ثبت شده‌اند.
- [ ] Open Itemهای حل‌شده با Resolution و مرجع بسته شده‌اند.
- [ ] Gapهای جدید ثبت شده‌اند.
- [ ] Gapهای پیاده‌سازی‌شده با Evidence به `Implemented` یا `Verified` منتقل شده‌اند.
- [ ] Prototype به‌عنوان Implementation Evidence قطعی معرفی نشده است.

## H. Traceability و History

- [ ] `Traceability_Matrix.md` اصلاح شده است.
- [ ] `Historical_Document_Register.md` بررسی شده است.
- [ ] هر سند Superseded به سند جایگزین لینک دارد.
- [ ] هر سند Canonical به Source Review یا Decision مربوط وصل است.
- [ ] لینک‌های متقابل اصلی سالم هستند.

## I. Documentation Map و Indexها

- [ ] `Documentation_Map.md` آخرین Baseline را نشان می‌دهد.
- [ ] README پوشه‌های تحت تأثیر به‌روزرسانی شده‌اند.
- [ ] نقطه شروع برای خواننده جدید همچنان روشن است.
- [ ] هیچ فایل اصلی بدون Index یا Registry باقی نمانده است.

## J. کیفیت و اعتبارسنجی

- [ ] Metadata اسناد جدید کامل است.
- [ ] ID تکراری ایجاد نشده است.
- [ ] Statusها از واژگان مجاز استفاده می‌کنند.
- [ ] لینک شکسته شناخته‌شده باقی نمانده است.
- [ ] فایل خارج از Scope به‌اشتباه تغییر نکرده است.
- [ ] گزارش Validation یا Change Summary ثبت شده است.

## K. آمادگی Merge

- [ ] Diff نهایی بررسی شده است.
- [ ] تغییرات کد و مستندات در صورت لزوم تفکیک شده‌اند.
- [ ] Change Set مربوط موجود است.
- [ ] Rollback یا مسیر بازگشت مشخص است.
- [ ] موارد باقی‌مانده صریحاً ثبت شده‌اند.
- [ ] مالک مسئول، Cycle را برای Merge تأیید کرده است.

## معیار بسته‌شدن

Cycle زمانی Closed محسوب می‌شود که:

1. خروجی آن در Registryها و Specificationهای فعال منعکس شده باشد؛
2. موارد حل‌نشده گم نشده باشند؛
3. وضعیت جاری بدون خواندن همه Iterationها قابل فهم باشد؛
4. این چک‌لیست بدون مورد بحرانی باز تکمیل شده باشد.
