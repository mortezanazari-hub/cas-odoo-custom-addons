# تفویض اختیار

| مشخصه | مقدار |
|---|---|
| Document ID | `PAGE-EMP-DELEGATION` |
| Document Type | Page Specification |
| Status | `Active` |
| Document Version | `1.0` |
| Created At | `2026-07-22` |
| Updated At | `2026-07-22` |
| Owner | Delegation Domain |
| Source UI Review Cycle | `CAS UI Review Cycle 10` |
| Source Iteration | `3–8` |
| Domain Owner | Delegation and Authorization |
| Affected Modules | delegation engine, correspondence, tasks, approvals, work reports, workspace |
| Implementation Status | `Gap Identified` |
| UI Validation Status | `Pending Revalidation` |
| Related Decisions | `DEC-016-UIR10-CONSOLIDATED` |
| Related Observations | `OBS-UIR10-DELEG-001` |
| Related Change Sets | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` |

## 1. Page IDs and Routes

- `PAGE-EMP-DELEGATION-MY` — `/workspace/delegations`؛
- `PAGE-ADMIN-DELEGATION-MANAGEMENT` — `/workspace/admin/delegations`.

## 2. Roles and Capabilities

کاربر عمومی، سرپرست و مدیر واحد فقط برای خودشان تفویض می‌سازند. انتخاب صاحب اختیار فقط برای کاربر دارای Capability مدیریت تفویض مجاز است. عنوان شغلی به‌تنهایی Capability ایجاد نمی‌کند.

## 3. General Form

- صاحب اختیار: کاربر جاری، readonly؛
- نماینده: Shared People Picker، single؛
- حوزه: مکاتبات، Task/Action، Approval/Request، گزارش کار؛
- عملیات: فقط عملیات Provider حوزه انتخاب‌شده؛
- اعتبار: موقت، تا اطلاع ثانوی، بر اساس حکم؛
- دلیل و توضیحات؛
- خلاصه قبل از ثبت.

## 4. Administrative Form

- صاحب اختیار و نماینده هر دو با People Picker و Scope مجاز؛
- نوع ثبت: عادی، سازمانی، اضطراری؛
- دلیل و مرجع اجباری؛
- سند/حکم در صورت وجود؛
- ثبت‌کننده، زمان، old/new state و اعلان به طرفین در Audit.

## 5. Domain Operations

### Correspondence
مشاهده صندوق، ایجاد پیش‌نویس، ارسال نهایی، پاسخ، ارجاع و امضای نهایی. عملیات حساس مستقل‌اند و Provider می‌تواند بعضی عملیات را غیرقابل تفویض اعلام کند.

### Task/Action
مشاهده، ایجاد، ارجاع، تغییر مسئول، تغییر مهلت، ثبت پیشرفت، تأیید تکمیل و بستن؛ فقط در محدوده اختیار صاحب اختیار.

### Approval/Request
مشاهده، بررسی، درخواست اصلاح، ارجاع، تأیید و رد. تأیید/رد نهایی عملیات حساس است.

### Work Report
مشاهده گزارش‌های مجاز، ثبت از طرف، ویرایش پیش‌نویس، ارسال، بازگرداندن، تأیید، رد و بازگشایی؛ عملیات حساس باید server-side validate و audit شوند.

## 6. Validity

- Temporary: start و end اجباری؛
- Until revoked: start اجباری، review cadence اجباری؛
- By decree: effective date، decree number/date/issuer/status و attachment؛ end اختیاری.

Expired، revoked، suspended یا replaced قابل استفاده نیستند. تغییر Capability یا Scope صاحب اختیار باید تفویض را دوباره ارزیابی کند.

## 7. Security

تفویض هرگز Role، ACL، Record Rule، حساب، رمز یا Login شخص را منتقل نمی‌کند. هر اقدام نمایندگی باید principal، actor، delegation_id، capability، target، timestamp و result را ثبت کند.

## 8. States

Draft، Active، Scheduled، Suspended، Expired، Revoked و Replaced. انتقال وضعیت باید Method Check و Audit داشته باشد.

## 9. Acceptance Criteria

- صاحب اختیار در فرم عمومی قابل تغییر نباشد؛
- فقط عملیات حوزه انتخاب‌شده دیده شوند؛
- کاربر نتواند بیش از اختیار خودش تفویض کند؛
- گزارش کار قابل تفویض باشد؛
- اعتبار بدون تاریخ پایان با بازبینی دوره‌ای پشتیبانی شود؛
- ابطال فوری در همه Providerها اثر کند؛
- اقدام نمایندگی هویت رسمی و عامل واقعی را حفظ کند.
