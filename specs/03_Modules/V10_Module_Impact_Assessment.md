# ارزیابی اثر ماژولی Cycle 10

| مشخصه | مقدار |
|---|---|
| Document ID | `IMPACT-UIR10-MODULES` |
| Document Type | Module Impact Assessment |
| Status | `Active` |
| Document Version | `1.0` |
| Created At | `2026-07-22` |
| Updated At | `2026-07-22` |
| Owner | Architecture Governance |
| Source UI Review Cycle | `CAS UI Review Cycle 10` |
| Source Iteration | `1–13` |
| Domain Owner | Cross-module Architecture |
| Implementation Status | `Gap Identified` |
| UI Validation Status | `Pending Revalidation` |
| Related Decisions | `DEC-016-UIR10-CONSOLIDATED` |
| Related Observations | `OBS-UIR10-*` |
| Related Change Sets | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` |

## 1. `cas_workspace`

مالک Shell، Route، Client Action/OWL، shared component و presentation است. مالک Business Data، Attendance calculations، delegation validity، secretariat sequence یا permission logic نیست.

نیازها: Routeهای تفویض، دبیرخانه و نگهبانی؛ Shared People Picker؛ capability-aware navigation؛ empty/error/forbidden states؛ RTL و responsive.

## 2. Shared People Picker

پیاده‌سازی می‌تواند در `cas_workspace` یا ماژول فنی مستقل قرار گیرد، اما MUST یک Contract مشترک داشته باشد. HR/organization data از مالک موجود مصرف می‌شود. Search endpoint، provider scope، single/multiple، Chip state، keyboard و security tests لازم‌اند.

## 3. Delegation Domain

نیازمند entityهای delegation، delegated capability، domain/provider، validity، decree metadata، review cadence، state و audit است.

Providerهای آلفا:

- correspondence؛
- tasks/actions؛
- approvals/requests؛
- work reports.

هر Provider MUST عملیات قابل تفویض، dependency، scope resolver، method validation و revocation behavior را اعلام کند.

## 4. Correspondence

نیازها:

- official sender و actual actor؛
- delegation check هنگام send/reply/refer/sign؛
- action request بدون auto-create Task؛
- receiver decision برای Task؛
- print/PDF با access check؛
- People Picker برای recipient/CC.

## 5. System Administration and Security Groups

گروه‌های مستقل لازم‌اند:

- user/access manager؛
- organization manager؛
- delegation manager؛
- settings manager؛
- audit viewer؛
- composite super administrator.

عنوان شغلی مثل مسئول IT هیچ group membership خودکار ایجاد نمی‌کند.

## 6. Secretariat Registry

در صورت نبود مالک موجود، ماژول اختصاصی جدید لازم است. مسئولیت‌ها:

- incoming/outgoing registry؛
- backend sequence؛
- routing؛
- send/delivery status؛
- register reports؛
- audit و correction ledger.

این ماژول نباید DMS داخلی بسازد و فقط Attachment مجاز را مصرف می‌کند.

## 7. `cas_attendance_operations`

Reuse مستقیم:

- `cas.guard.batch`؛
- `cas.guard.batch.line`؛
- `site_id`؛
- `default_occurred_at`؛
- `line_ids`؛
- `action_confirm`.

Gapهای محتمل: fields یا audit metadata برای recorded_at، manual time reason، conflict acknowledgement و batch-level UX support. تغییر دقیق باید بعد از Gap Analysis کد تثبیت شود.

## 8. `cas_attendance_core`

مالک `cas.attendance.event`، attribution، reconciliation، conflict، void/replacement و append-only history باقی می‌ماند. UI نگهبانی نباید این منطق را کپی کند.

## 9. Attachments and Nextcloud Boundary

Attachment استاندارد Odoo برای رکوردهای مجاز باقی می‌ماند. OCR و DMS داخلی حذف می‌شوند. Integration با Nextcloud نیازمند Decision و Contract مستقل در Cycle بعد است.

## 10. Migration

- حذف menu/route/referenceهای OCR و DMS آلفا؛
- migration تفویض‌های قدیمی به principal/agent/domain/capability/validity؛
- mapping گروه‌های مدیریت سامانه؛
- تعریف sequence و unique constraints دبیرخانه؛
- حفظ رخدادها و history بدون حذف؛
- preference migration برای routeهای جدید.

## 11. Test Strategy

برای هر ماژول: Unit، Integration، Security، Multi-company، Migration، Audit، Regression و UI Revalidation. Attendance باید تست نیمه‌شب، شیفت، duplicate، conflict و batch confirmation داشته باشد.

## 12. Risks

- privilege escalation از طریق delegation؛
- metadata leakage در People Picker؛
- sequence race condition؛
- duplicate attendance event؛
- stale cache پس از revocation؛
- ساخت DMS موازی؛
- overuse of `sudo()`؛
- مخلوط‌شدن title شغلی با permission.
