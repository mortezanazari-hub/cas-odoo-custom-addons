# معیارهای پذیرش آلفا — Cycle 10

| مشخصه | مقدار |
|---|---|
| Document ID | `ACC-UIR10-ALPHA` |
| Document Type | Acceptance Specification |
| Status | `Active` |
| Document Version | `1.0` |
| Created At | `2026-07-22` |
| Updated At | `2026-07-22` |
| Owner | Product QA |
| Source UI Review Cycle | `CAS UI Review Cycle 10` |
| Source Iteration | `1–13` |
| Domain Owner | Cross-domain QA |
| Implementation Status | `Gap Identified` |
| UI Validation Status | `Pending Revalidation` |
| Related Decisions | `DEC-016-UIR10-CONSOLIDATED` |
| Related Observations | `OBS-UIR10-*` |
| Related Change Sets | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` |

## Shared People Picker

- [ ] single و multiple عملیاتی‌اند.
- [ ] multiple انتخاب‌های قبلی را حفظ می‌کند.
- [ ] حذف Chip، list state، checkbox، count و CTA را هم‌زمان اصلاح می‌کند.
- [ ] Search و unit filter کار می‌کنند.
- [ ] Select all فقط نتایج فیلترشده و مجاز را انتخاب می‌کند.
- [ ] API هیچ شخص، count یا metadata غیرمجاز را بازنمی‌گرداند.
- [ ] Backend انتخاب نهایی و ID tampering را اعتبارسنجی می‌کند.

## Delegation

- [ ] در فرم عمومی صاحب اختیار readonly و برابر کاربر جاری است.
- [ ] فقط مدیر دارای Capability می‌تواند برای دیگران تفویض ثبت کند.
- [ ] کاربر نمی‌تواند بیش از Capability و Scope خودش تفویض کند.
- [ ] فقط عملیات Provider حوزه انتخاب‌شده نمایش داده می‌شوند.
- [ ] حوزه گزارش کار عملیاتی است.
- [ ] عملیات حساس مستقل، هشداردهنده و server-side validated هستند.
- [ ] Temporary، Until Revoked و By Decree پشتیبانی می‌شوند.
- [ ] تفویض بدون پایان review cadence دارد.
- [ ] Expired/Revoked/Suspended/Replaced قابل استفاده نیست.
- [ ] هر اقدام principal، actor، delegation و target را Audit می‌کند.

## System Administration

- [ ] گروه‌های user/access، organization، delegation، settings و audit تفکیک شده‌اند.
- [ ] عنوان شغلی دسترسی خودکار ایجاد نمی‌کند.
- [ ] مدیر ارشد فقط نقش تجمیعی گروه‌های مصوب است.
- [ ] audit viewer امکان تغییر Audit ندارد.
- [ ] تفکیک وظایف و حداقل دسترسی رعایت می‌شود.

## Secretariat

- [ ] دبیرخانه Access Domain است، نه title شغلی.
- [ ] کارشناس اداری فقط با Capability مجاز وارد می‌شود.
- [ ] وارده، فرستنده خارجی و گیرنده داخلی مستقل دارد.
- [ ] شماره وارده خودکار و backend-controlled است.
- [ ] صادره قبل از Approved/Signed/Ready state شماره نمی‌گیرد.
- [ ] تهیه‌کننده، فرستنده رسمی، امضاکننده، ثبت‌کننده و گیرنده مستقل‌اند.
- [ ] گزارش دفتر صفحه واقعی و فیلترهای عملیاتی دارد.
- [ ] Print/PDF/Excel Access و Export Security را رعایت می‌کنند.
- [ ] اصلاح رکورد رسمی بدون حذف تاریخچه انجام می‌شود.

## Guard Attendance

- [ ] صفحه روی `cas.guard.batch` و مدل‌های موجود کار می‌کند.
- [ ] انتخاب تکی، چندگانه و حذف Chip عملیاتی است.
- [ ] ثبت بدون فرد غیرفعال است.
- [ ] زمان زنده پیش‌فرض است.
- [ ] تغییر ساعت/دقیقه فقط با دلیل و نگهداری recorded_at ممکن است.
- [ ] هر فرد Line مستقل و همه Lineها Batch مشترک دارند.
- [ ] وضعیت داخل/خارج و آخرین رخداد نمایش داده می‌شود.
- [ ] ورود/خروج متعارض هشدار، reason و audit دارد.
- [ ] `action_confirm` رخدادهای رسمی را ایجاد می‌کند.
- [ ] رخداد رسمی قابل ویرایش/حذف عادی نیست.
- [ ] آخرین ثبت‌ها زمان رخداد، زمان ثبت، محل، actor و source را نشان می‌دهند.

## Alpha Scope

- [ ] هیچ Menu، Route، Queue، Setting یا وابستگی محصولی OCR فعال نیست.
- [ ] مدیریت اسناد/DMS داخلی در Navigation آلفا وجود ندارد.
- [ ] Attachment مجاز برای رکورد کسب‌وکار باقی مانده است.
- [ ] هیچ مدل DMS موازی پیش از Decision یکپارچه‌سازی Nextcloud ایجاد نشده است.

## Non-functional

- [ ] RTL، Keyboard، Focus، Zoom 200% و متن فارسی طولانی بررسی شده‌اند.
- [ ] Desktop و Tablet سناریوهای عملیاتی را Pass می‌کنند.
- [ ] Cross-company، revoked access، direct RPC و ID tampering تست شده‌اند.
- [ ] Evidence شامل Commit/PR، test report، screenshot و audit sample است.
- [ ] بدون Evidence هیچ موردی `Implemented` یا `Accepted` اعلام نمی‌شود.
