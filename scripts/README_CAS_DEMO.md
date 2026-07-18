# مولد دموی کامل CAS

اجرا:

```bash
cd /opt/odoo/custom-addons
CAS_DEMO_PASSWORD='رمز-موقت-قوی' ./scripts/run_cas_full_demo.sh cas_odoo_dev
```

اسکریپت idempotent است، رکوردهای رسمی را حذف نمی‌کند و داده‌هایش با `[DEMO]` یا `demo_` مشخص‌اند. حساب‌ها از `demo.ceo@cas.local` تا `demo.employee2@cas.local` ساخته می‌شوند. خروجی موفق باید برای سازمان، فرم، workflow/approval، سند/OCR، مکاتبات، شیفت/حضور/کاردکس، گزارش کار/Excel، Action Hub/SLA و bridgeهای جلالی همگی PASS و مقدار failures برابر صفر نشان دهد.

برای پاک‌سازی کامل از دیتابیس دموی جدا استفاده کنید؛ سوابق append-only عمداً حذف نمی‌شوند.
