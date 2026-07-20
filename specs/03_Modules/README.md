# 03 — Modules

پس از بررسی صفحات، تصمیم‌ها در این بخش بر اساس ماژول تجمیع می‌شوند. تا پیش از وضعیت `Implementation Ready`، اسناد این بخش مجوز پیاده‌سازی نیستند.

## مرجع مرکزی نسخه ۷

- [فهرست جامع ماژول‌های متأثر، ماژول‌های جدید پیشنهادی، سرویس‌های داخلی و Adapterها](V7_Module_Impact_And_New_Modules.md)

## ارزیابی‌های اثر نسخه ۷

- [`cas_workspace`](cas_workspace/V7_Impact_Assessment.md)
- [`cas_action_hub`](cas_action_hub/V7_Impact_Assessment.md)
- [`cas_work_report`](cas_work_report/V7_Impact_Assessment.md)
- [ارزیابی بین‌ماژولی سایر ماژول‌ها](Cross_Module_V7_Impact_Assessment.md)

## ارزیابی اثر نسخه ۸

- [ارزیابی جامع اثر ماژولی Workspace v8](V8_Impact_Assessment.md)

این سند اثر نسخه ۸ را بر موارد زیر ثبت می‌کند:

- `cas_workspace`
- `cas_personal_task` پیشنهادی
- `cas_action_hub`
- HR/Employee Directory
- Organization Hierarchy Resolver
- Calendar/Event Integration
- Odoo Mail/Discuss/Bus
- `cas_document_core`
- Notification Core
- Jalali Suite

همچنین APIهای پیشنهادی، امنیت، Migration، Dependency و Test Strategy حداقلی را مشخص می‌کند.

## وضعیت

این فایل‌ها Impact Assessment هستند، نه Specification نهایی. برای هر ماژول باید Specification، Architecture، API، Security، Migration و Test Strategy مستقل تولید و تصویب شود.
