# CAS Specifications Constitution

> **وضعیت:** `Canonical / Mandatory`
>
> **دامنه:** تمام فایل‌ها، تصمیم‌ها، طراحی‌ها، قراردادها، Change Setها و سوابق داخل پوشه `specs`
>
> **آخرین چرخه فعال بازنگری UI:** `CAS UI Review Cycle 10 — Through Iteration 13`
>
> **نسخه نرم‌افزار:** مستقل از شماره چرخه‌های بازنگری UI و فقط در اسناد Release نرم‌افزار تعیین می‌شود.
>
> **مخاطب:** انسان، توسعه‌دهنده، تحلیل‌گر، طراح، مدیر محصول، معمار، بازبین و هر AI Agent
>
> **قاعده مطلق:** هیچ شخص یا Agent حق ندارد پیش از مطالعه کامل این فایل، سندی در `specs` ایجاد، ویرایش، حذف، انتقال، Supersede، Commit، Push یا Merge کند.

---

# 0. ماهیت این سند

این README یک معرفی ساده نیست؛ «قانون اساسی مستندسازی CAS» و نقطه شروع اجباری هر فعالیت مستندی است.

هر عامل انسانی یا ماشینی که روی `specs` کار می‌کند، با انجام نخستین تغییر اعلام می‌کند که:

1. این فایل را کامل خوانده است.
2. هدف واقعی پوشه `specs` را می‌داند.
3. تفاوت UI Review Cycle، Iteration، Document Version و Software Release را می‌داند.
4. زنجیره رفت‌وبرگشتی UI ↔ تحلیل محصول ↔ Backend ↔ اعتبارسنجی مجدد را رعایت می‌کند.
5. هیچ تصمیمی را فقط در چت، Commit message یا توضیح PR رها نمی‌کند.
6. مالکیت داده و دامنه را از روی حدس تعیین نمی‌کند.
7. هیچ تصمیم Active را صرفاً برای هماهنگی با کد فعلی تضعیف نمی‌کند.
8. هیچ چرخه UI را به‌اشتباه نسخه نرم‌افزار یا نسخه نهایی محصول معرفی نمی‌کند.
9. هر تغییر را در تمام اسناد وابسته ردیابی می‌کند.
10. وضعیت اسناد را صادقانه اعلام می‌کند.

---

# 1. هدف واقعی پوشه `specs`

پوشه `specs` حافظه مهندسی چرخه تضمین کیفیت محصول است.

این پوشه برای آن ساخته شده که:

1. ماژول‌های موجود مبنای طراحی اولیه UI قرار گیرند.
2. UI به‌صورت صفحه‌به‌صفحه، نقش‌به‌نقش و سناریوبه‌سناریو بررسی شود.
3. مشکلات، کمبودها، اضافات، ابهام‌ها و نیازهای جدید در UI کشف شوند.
4. هر مشاهده UI به تصمیم محصولی یا معماری قابل‌اجرا تبدیل شود.
5. مشخص شود کدام ماژول موجود باید تغییر کند.
6. مشخص شود کدام ماژول جدید باید ایجاد شود.
7. مشخص شود کدام قابلیت باید حذف، جابه‌جا یا بازطراحی شود.
8. تیم Backend بعداً دقیقاً بداند چه چیزی باید پیاده‌سازی کند.
9. پس از پیاده‌سازی، همان موضوع دوباره در UI اعتبارسنجی شود.
10. نتیجه اعتبارسنجی به `Accepted` یا `Reopened` تبدیل شود.
11. حافظه محدود انسان یا AI باعث تکرار بحث یا ازبین‌رفتن تصمیم نشود.
12. کیفیت نهایی محصول از طریق رفت‌وبرگشت کنترل‌شده افزایش یابد.

چرخه مرجع:

```text
Existing Modules / Current Backend
        ↓
UI Design or UI Review Build
        ↓
Page-by-Page and Role-by-Role Evaluation
        ↓
UI Observation / Problem / Opportunity
        ↓
Product Decision and Architecture Decision
        ↓
Module Impact and Backend Change Specification
        ↓
Implementation / Migration / Tests
        ↓
UI Revalidation
        ↓
Accepted or Reopened
        ↺
Next UI Review Cycle
```

`specs` فقط «توضیح ظاهر UI» نیست و فقط «مستند معماری Backend» هم نیست؛ این پوشه حلقه اتصال این دو و حافظه کامل چرخه QA است.

---

# 2. تفکیک قطعی انواع نسخه

## 2.1. UI Review Cycle

نمونه:

```text
CAS UI Review Cycle 7
CAS UI Review Cycle 8
CAS UI Review Cycle 9
```

این اعداد فقط شماره چرخه‌های بازنگری کلی رابط کاربری هستند.

- Cycle 8 نسخه هشتم نرم‌افزار نیست.
- Cycle 8 نسخه نهایی محصول نیست.
- Cycle 8 مانع ورود Cycle 9 نیست.
- با ورود Cycle 9، Cycle 9 آخرین چرخه فعال بازنگری UI می‌شود.
- Cycle 8 به سابقه بازنگری تبدیل می‌شود.
- تصمیم‌های کشف‌شده در Cycle 8 فقط در صورتی منقضی می‌شوند که سند جدید صریحاً آن‌ها را Supersede کند.

## 2.2. Iteration

Iteration اصلاح داخلی درون یک UI Review Cycle است.

نمونه:

```text
UI Review Cycle 8
├── Iteration 1
├── Iteration 2
└── Iteration 12
```

Iteration 12 دوازدهمین اصلاح داخلی Cycle 8 است، نه نسخه 12 نرم‌افزار.

## 2.3. Document Version

هر سند می‌تواند نسخه خودش را داشته باشد، مانند:

```text
Document Version: 1.0
Document Version: 1.1
Document Version: 2.0
```

این شماره فقط تاریخچه همان سند است و با UI Review Cycle یا Software Release یکی نیست.

## 2.4. Software Release

نسخه نرم‌افزار مستقل است و فقط در اسناد Release تعیین می‌شود، مانند:

```text
CAS Software 1.0
CAS Software 1.1
CAS Software 2.0
```

تا زمانی که Release Strategy رسمی تعیین نشده، هیچ UI Review Cycle نباید Software Version نامیده شود.

---

# 3. مرجع مؤثر برای Backend

مرجع پیاده‌سازی Backend «آخرین UI ZIP» یا «شماره یک Cycle» نیست.

مرجع مؤثر برابر است با:

```text
All Active and Agreed Decisions
+ Active Module Specifications
+ Active Architecture Contracts
+ Active Security Contracts
+ Approved Changes from the Latest UI Review
- Superseded Requirements
- Historical-only Statements
```

بنابراین:

- Cycle جدید همه تصمیم‌های Cycle قبلی را خودکار باطل نمی‌کند.
- فقط تصمیم‌هایی که صریحاً تغییر کرده‌اند Supersede می‌شوند.
- تصمیم Active می‌تواند در Cycle 8 کشف شده باشد و در Cycle 9 همچنان معتبر بماند.
- کد باید با مجموعه Specificationهای مؤثر و Active منطبق شود، نه با یک شماره UI.
- اختلاف کد با اسناد Active یک `Implementation Gap` است.
- اختلاف UI جدید با تصمیم Active یک `Review Conflict` است و باید تحلیل شود.

---

# 4. وضعیت‌های رسمی

## 4.1. وضعیت سند

- `Draft`
- `Under Review`
- `Agreed`
- `Active`
- `Superseded`
- `Historical`
- `Rejected`
- `Archived`

## 4.2. وضعیت اجرا

- `Not Assessed`
- `Gap Identified`
- `Planned`
- `In Development`
- `Implemented`
- `Partially Implemented`
- `Blocked`
- `Deprecated`

## 4.3. وضعیت اعتبارسنجی UI

- `Not Validated`
- `Pending Revalidation`
- `Validated`
- `Accepted`
- `Reopened`
- `Failed Validation`

این سه محور مستقل‌اند. سندی می‌تواند `Active`، از نظر اجرا `Implemented` و از نظر UI `Pending Revalidation` باشد.

---

# 5. سلسله‌مراتب مرجعیت

در تعارض میان اسناد، ترتیب زیر اعمال می‌شود:

1. تصمیم صریح و جدید مالک محصول
2. این Constitution
3. فهرست تصمیم‌های Active و Supersede Records
4. Architecture Decisions و Security Decisions
5. Module Specifications فعال
6. Page Specifications فعال
7. Change Sets
8. Traceability و Impact Matrices
9. UI Review Observations
10. Prototype، Screenshot و Mock Data
11. کد فعلی
12. گفتگو، Commit Message یا حافظه اشخاص

کد فعلی برای تشخیص Gap مهم است، اما نمی‌تواند تصمیم Active را خودکار باطل کند.

---

# 6. ترتیب مطالعه اجباری Agent

پیش از هر تغییر:

1. `specs/README.md`
2. `00_Project/UI_Review_Lifecycle.md`
3. `00_Project/Documentation_Governance.md`
4. `00_Project/Version_History.md`
5. `00_Project/Traceability_Matrix.md`
6. `00_Project/Historical_Document_Register.md`
7. `00_Project/Open_Questions.md`
8. `01_Product/Terminology.md`
9. `01_Product/UX_Principles.md`
10. Module Ownership Map
11. Dependency Map
12. Provider Registry
13. Module Boundaries
14. Capability and Security Model
15. تمام Decisionها، Page Specها، Module Specها و Change Setهای مرتبط

Agent حق ندارد فقط فایل هدف را بخواند.

---

# 7. پروتکل اجباری پیش از نگارش

Agent باید:

1. موضوع تغییر را یک جمله دقیق تعریف کند.
2. چرخه UI منبع را مشخص کند.
3. Observation یا نیاز اولیه را ثبت کند.
4. در کل `specs` برای نام قابلیت، مترادف‌ها، Module، Route، Capability، Entity و Decision جست‌وجو کند.
5. تصمیم‌های Active و Superseded مرتبط را جدا کند.
6. مالک Domain را مشخص کند.
7. مشخص کند تغییر UI-only، Backend-only یا Cross-layer است.
8. اثر امنیت، Migration، Test، Reporting و Audit را بررسی کند.
9. فایل‌های لازم برای تغییر را فهرست کند.
10. از ساخت سند موازی جلوگیری کند.
11. در صورت تعارض، Conflict Record بسازد.
12. فقط بعد از این مراحل نگارش را شروع کند.

---

# 8. واحد پایه ثبت تغییر

هر تغییر ناشی از UI باید حداقل این زنجیره را داشته باشد:

```text
UI Observation
→ Decision
→ Module Impact
→ Backend Requirement
→ Implementation Status
→ UI Revalidation
→ Final Outcome
```

## 8.1. UI Observation

باید شامل:

- شناسه Observation
- UI Review Cycle
- Iteration
- صفحه
- نقش
- سناریو
- رفتار مشاهده‌شده
- مشکل یا فرصت
- شواهد
- شدت
- وضعیت
- اسناد مرتبط

## 8.2. Decision

باید شامل:

- شناسه Decision
- تصمیم دقیق
- دلیل
- گزینه‌های ردشده
- اثر محصولی
- اثر معماری
- مالک Domain
- تصمیم‌های Superseded
- Source Observation
- وضعیت

## 8.3. Module Impact

باید شامل:

- ماژول موجود یا جدید
- نوع تغییر
- Models
- Fields
- Services
- Access
- Migration
- Tests
- Dependencies
- Risks

## 8.4. UI Revalidation

باید شامل:

- Build یا Cycle اعتبارسنجی
- سناریو
- نقش
- نتیجه
- Evidence
- Acceptance Criteria
- Outcome: `Accepted` یا `Reopened`

---

# 9. قواعد ورود UI Review Cycle جدید

هنگام ورود Cycle جدید:

1. Cycle جدید به‌عنوان آخرین چرخه فعال بازنگری UI ثبت می‌شود.
2. Cycle قبلی حذف نمی‌شود.
3. Cycle قبلی فقط Historical Review Source می‌شود.
4. تمام صفحات و سناریوهای Cycle جدید فهرست می‌شوند.
5. تفاوت‌ها با اسناد Active استخراج می‌شوند.
6. هر تفاوت طبقه‌بندی می‌شود:
   - New Requirement
   - Modification
   - Removal
   - UI-only Change
   - Backend Change
   - New Module
   - Security Change
   - Workflow Change
   - Reversal
   - Bug Fix
7. تغییرات صریح Decision Record می‌گیرند.
8. تصمیم قبلی فقط با `Supersedes` صریح باطل می‌شود.
9. Module Impact و Change Set به‌روزرسانی می‌شوند.
10. Traceability Matrix اصلاح می‌شود.
11. هیچ سندی صرفاً به‌دلیل قدیمی‌تر بودن حذف نمی‌شود.
12. وضعیت «آخرین چرخه فعال» در Indexها به‌روزرسانی می‌شود.

---

# 10. Metadata اجباری هر سند

هر سند باید متناسب با نوع خود این Metadata را داشته باشد:

```text
Document ID
Document Type
Title
Status
Document Version
Created At
Updated At
Owner
Reviewers
Source UI Review Cycle
Source Iteration
Effective From
Supersedes
Superseded By
Domain Owner
Affected Modules
Implementation Status
UI Validation Status
Related Decisions
Related Observations
Related Change Sets
```

فیلد نامرتبط می‌تواند `N/A` باشد، اما حذف بدون دلیل ممنوع است.

---

# 11. نام‌گذاری فایل‌ها و شناسه‌ها

## 11.1. Observation

```text
OBS-UIR08-EMP-GUARD-001
```

## 11.2. Decision

```text
DEC-021-Guard-Attendance-Interaction
```

## 11.3. Change Set

```text
CS-UIR09-GUARD-REDESIGN
```

## 11.4. Module Specification

```text
specs/03_Modules/cas_guard/Specification.md
```

## 11.5. Page Specification

```text
specs/02_UI_UX/Guard/Attendance_Registration.md
```

شناسه‌ها هرگز Reuse نمی‌شوند.

---

# 12. قواعد زبان و نگارش

- زبان اصلی توضیحات فارسی است.
- نام فنی Model، Field، Route، API و Capability انگلیسی و داخل Backtick است.
- جمله باید قطعی، آزمون‌پذیر و بدون ابهام باشد.
- «در صورت نیاز»، «احتمالاً»، «شاید» و «بهتر است» بدون تعیین تصمیم یا شرط ممنوع‌اند.
- هر الزام باید Subject، Action و Condition روشن داشته باشد.
- واژه‌های `MUST`، `SHOULD` و `MAY` فقط با معنی دقیق استفاده شوند.
- اصطلاح جدید باید در Terminology ثبت شود.
- یک مفهوم نباید چند نام متناقض داشته باشد.
- مثال‌ها نباید جای Rule را بگیرند.
- متن باید تفاوت Observation، Decision و Implementation Proposal را روشن نگه دارد.

---

# 13. قواعد Decision Record

Decision جدید زمانی لازم است که:

- رفتار محصول تغییر کند.
- مالک Domain تغییر کند.
- ماژول جدید لازم شود.
- Route یا Capability اضافه/حذف شود.
- امنیت یا Scope تغییر کند.
- Lifecycle یا State Machine تغییر کند.
- تصمیم قبلی برگشت داده شود.
- قرارداد Integration تغییر کند.
- یک UI Observation اثر چندماژولی داشته باشد.

هر Decision باید:

1. Context
2. Problem
3. Decision
4. Rationale
5. Consequences
6. Alternatives
7. Domain Owner
8. Module Impact
9. Security Impact
10. Migration Impact
11. Test Impact
12. Source Observation
13. Supersedes
14. Acceptance Criteria

داشته باشد.

---

# 14. قواعد Module Specification

هر Module Specification باید شامل:

1. Purpose
2. In Scope
3. Out of Scope
4. Domain Ownership
5. Dependencies
6. Entities and Models
7. State Machines
8. Services and Commands
9. Queries
10. Events
11. Provider Interfaces
12. ACL
13. Record Rules
14. Method Checks
15. Field/Section Security
16. Multi-company
17. Audit
18. Migration
19. Performance
20. Observability
21. Failure Modes
22. Test Strategy
23. Acceptance Criteria
24. UI Review Sources
25. Revalidation Plan

باشد.

---

# 15. قواعد Page Specification

هر Page Specification باید شامل:

1. Page ID
2. Route
3. Roles
4. Capabilities
5. Source UI Review Cycle
6. Goal
7. Entry Conditions
8. Layout
9. Components
10. Data Sources
11. Actions
12. States
13. Loading
14. Empty
15. Error
16. Forbidden
17. Unavailable
18. Responsive
19. RTL
20. Accessibility
21. Keyboard
22. Security
23. Performance
24. Analytics
25. Module Impacts
26. Acceptance Criteria
27. Revalidation Scenarios

باشد.

---

# 16. قواعد امنیت

هر تغییر باید بررسی کند:

- ACL
- Record Rule
- Company Scope
- Organization Scope
- Delegation
- Method Permission
- Field Security
- Section Security
- Export Security
- Search Leakage
- Count Leakage
- Metadata Leakage
- ID Tampering
- Attachment Permission
- Audit
- Retention
- Impersonation Risk
- `sudo()` misuse
- Cross-company access
- Revocation behavior

مخفی‌شدن دکمه یا Route کنترل امنیتی کافی نیست.

---

# 17. قواعد Backend Impact

برای هر تغییر باید روشن شود:

- ماژول موجود تغییر می‌کند یا ماژول جدید ایجاد می‌شود؟
- مالک داده کیست؟
- Model جدید لازم است؟
- Field جدید لازم است؟
- Constraint چیست؟
- Migration چیست؟
- API یا Service چیست؟
- Provider چیست؟
- Event چیست؟
- Permission چیست؟
- Performance Risk چیست؟
- Test چیست؟
- Rollback چیست؟
- UI چگونه مجدداً اعتبارسنجی می‌شود؟

عبارت «Backend باید اصلاح شود» به‌تنهایی غیرقابل‌قبول است.

---

# 18. قواعد Odoo

- Odoo Core نباید ویرایش شود.
- قابلیت استاندارد ابتدا Gap Analysis می‌شود.
- قابلیت استاندارد مناسب Reuse می‌شود.
- Extension فقط برای Gap اثبات‌شده مجاز است.
- Override باید Upgrade Risk و Test داشته باشد.
- ذخیره تاریخ استاندارد Odoo باقی می‌ماند؛ Jalali لایه UI است.
- `sudo()` برای عبور از Permission کاربر ممنوع است.
- Workspace مالک Business Data نیست.
- هیچ مدل موازی برای Mail، Discuss، Calendar یا Attachment بدون Decision ساخته نمی‌شود.

---

# 19. Traceability اجباری

هر Requirement فعال باید در Traceability قابل دنبال‌کردن باشد:

```text
Observation ID
Decision ID
Page Spec
Module Spec
Architecture Contract
Security Contract
Change Set
Implementation Ticket/Commit
Test Evidence
UI Revalidation Evidence
Final Status
```

ردیف بدون Owner، Status یا Source ناقص است.

---

# 20. Change Set

Change Set باید تفاوت را ثبت کند، نه اینکه جای Decision یا Specification را بگیرد.

هر Change Set باید شامل:

- Source UI Review Cycle
- Scope
- Observations
- Added
- Changed
- Removed
- Superseded
- Module Impacts
- Security Impacts
- Migration
- Tests
- Revalidation Plan
- Open Questions
- Risks
- Rollback

باشد.

---

# 21. Historical و Superseded

- Historical یعنی منبع تاریخی و غیرمرجع برای رفتار جاری.
- Superseded یعنی تصمیم یا بخش مشخص با تصمیم جدید جایگزین شده است.
- Cycle قبلی به‌خودی‌خود تمام تصمیم‌هایش را Supersede نمی‌کند.
- حذف فایل تاریخی ممنوع است مگر دلیل حقوقی یا امنیتی وجود داشته باشد.
- لینک `Superseded By` و `Supersedes` باید دوطرفه باشد.
- بخش‌های هنوز معتبر می‌توانند Active بمانند، حتی اگر منبع کشف آن‌ها Cycle قدیمی باشد.

---

# 22. Implementation Gap

Gap باید شامل:

- Gap ID
- Active Requirement
- Current Behavior
- Expected Behavior
- Affected Module
- Severity
- Security Impact
- Migration Need
- Proposed Work
- Owner
- Status
- Test
- UI Revalidation

باشد.

Gap دلیل تغییر Requirement نیست؛ Gap نشان می‌دهد کد هنوز با Requirement منطبق نیست.

---

# 23. Conflict Record

در تعارض میان UI جدید و اسناد Active:

1. هیچ‌کدام خودکار حذف نمی‌شوند.
2. Conflict ثبت می‌شود.
3. منبع هر دو طرف ذکر می‌شود.
4. اثر محصولی و Backend تحلیل می‌شود.
5. مالک تصمیم مشخص می‌شود.
6. Decision جدید Conflict را حل می‌کند.
7. فقط سپس Supersede انجام می‌شود.

---

# 24. Test و Acceptance

هر قابلیت باید حسب نیاز این آزمون‌ها را پوشش دهد:

- Unit
- Integration
- Security
- Multi-company
- Migration
- Regression
- UI
- Accessibility
- RTL
- Responsive
- Load
- Failure Recovery
- Audit
- Revalidation

Acceptance Criteria باید قابل مشاهده، قابل اندازه‌گیری و دارای نتیجه Pass/Fail باشد.

---

# 25. پروتکل AI Agent

Agent باید:

1. درخواست کاربر را دقیق بازگو کند.
2. نوع کار را تشخیص دهد.
3. اسناد اجباری را بخواند.
4. جست‌وجوی سراسری انجام دهد.
5. Source UI Review را تعیین کند.
6. Active و Historical را جدا کند.
7. Ownership را بررسی کند.
8. فایل‌های متأثر را مشخص کند.
9. تغییر را ثبت کند.
10. Traceability را اصلاح کند.
11. Indexها را اصلاح کند.
12. Change Set را اصلاح کند.
13. تناقض‌ها را بررسی کند.
14. Diff را بازبینی کند.
15. فقط فایل‌های مرتبط را Commit کند.
16. در گزارش نهایی فایل‌ها، تصمیم‌ها، Gapها و Open Questionها را ذکر کند.

Agent نباید:

- شماره UI را Software Version بنامد.
- Cycle جدید را بدون بررسی جایگزین همه تصمیم‌های قبلی کند.
- سند موازی بسازد.
- تصمیم را از روی کد حدس بزند.
- Scope را برای آسان‌شدن پیاده‌سازی کاهش دهد.
- Historical را حذف کند.
- امنیت را فقط در UI تعریف کند.
- Push یا Merge خارج از درخواست انجام دهد.
- `Implementation Ready` را بدون شواهد اعلام کند.

---

# 26. چک‌لیست قبل از Commit و Push

- [ ] هدف واقعی تغییر ثبت شده است.
- [ ] Source UI Review Cycle مشخص است.
- [ ] Observation ثبت شده است.
- [ ] تصمیم‌های مرتبط بررسی شده‌اند.
- [ ] Supersede صریح است.
- [ ] Module Ownership مشخص است.
- [ ] Backend Impact دقیق است.
- [ ] Security بررسی شده است.
- [ ] Migration بررسی شده است.
- [ ] Tests تعریف شده‌اند.
- [ ] UI Revalidation تعریف شده است.
- [ ] Traceability اصلاح شده است.
- [ ] Change Set اصلاح شده است.
- [ ] Indexها اصلاح شده‌اند.
- [ ] لینک‌ها معتبرند.
- [ ] هیچ UI Cycle به‌عنوان Software Version معرفی نشده است.
- [ ] Diff فقط شامل فایل‌های مرتبط است.
- [ ] وضعیت‌ها صادقانه‌اند.

---

# 27. دستور اجرایی استاندارد برای Agent آینده

هنگامی که کاربر می‌گوید «مستندات را به‌روز کن»، Agent باید این درخواست را چنین تفسیر کند:

> آخرین تغییرات UI، تصمیم‌های محصولی یا نیازهای Backend را در زنجیره کامل Observation → Decision → Module Impact → Implementation Requirement → Revalidation ثبت کن؛ تاریخچه را حفظ کن؛ فقط موارد صریح را Supersede کن؛ شماره چرخه UI را با نسخه نرم‌افزار اشتباه نگیر؛ و تمام Indexها، Traceability و Change Setهای متأثر را هماهنگ کن.

---

# 28. وضعیت فعلی

- آخرین چرخه فعال بازنگری UI: `CAS UI Review Cycle 10 — Through Iteration 13`
- Cycle 10 نسخه نرم‌افزار نیست.
- Cycle 10 نسخه نهایی و غیرقابل‌تغییر محصول نیست.
- Cycle 9 به‌عنوان Historical Review Source حفظ می‌شود.
- تصمیم‌های Active از چرخه‌های قبلی تا زمان Supersede صریح معتبر می‌مانند.
- Backend باید با مجموعه Specificationهای مؤثر و Active منطبق شود.
- ثبت رسمی Cycle 10 در `00_Project/UI_Review_Cycle_10_Register.md` نگهداری می‌شود.
- فایل `00_Project/UI_Review_Lifecycle.md` مرجع تفصیلی مدیریت چرخه‌هاست.

---

# 29. اصل نهایی

```text
UI Review Cycle discovers and validates.
Specifications preserve and translate.
Backend implements.
Tests verify.
UI revalidates.
History remains traceable.
```

هر تغییر مستندی که این چرخه را ناقص کند، تغییر کامل محسوب نمی‌شود.
