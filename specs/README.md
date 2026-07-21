# CAS Specifications Constitution

> **وضعیت:** `Canonical / Mandatory`
>
> **دامنه:** تمام فایل‌ها، تصمیم‌ها، طراحی‌ها و قراردادهای داخل پوشه `specs`
>
> **Baseline فعال:** `CAS UI Workspace v8 — Through Iteration 12`
>
> **مخاطب:** انسان، توسعه‌دهنده، تحلیل‌گر، طراح، مدیر محصول، معمار، بازبین و هر AI Agent
>
> **قاعده مطلق:** هیچ شخص یا Agent حق ندارد پیش از مطالعه کامل این فایل، سندی در `specs` ایجاد، ویرایش، حذف، انتقال، Supersede، Commit یا Merge کند.

---

# 0. اعلام الزام و اثر حقوقی این سند در پروژه

این فایل README یک معرفی ساده نیست. این سند «قانون اساسی مستندسازی CAS» و نقطه شروع اجباری هر فعالیت مستندی است.

هر عامل انسانی یا ماشینی که روی `specs` کار می‌کند، با انجام نخستین تغییر اعلام می‌کند که:

1. این فایل را کامل خوانده است.
2. Baseline فعال را می‌شناسد.
3. تفاوت Product Decision، Architecture Decision، Module Specification، Page Specification، Change Set و Implementation Gap را می‌داند.
4. مالکیت داده و دامنه‌ها را از روی حدس تعیین نمی‌کند.
5. هیچ تصمیمی را صرفاً به دلیل ناسازگاری با کد فعلی تضعیف نمی‌کند.
6. هر تغییر را در تمام اسناد وابسته ردیابی می‌کند.
7. هیچ تصمیم جدیدی را فقط در متن چت، Commit message یا توضیح PR رها نمی‌کند.
8. از ساخت اسناد موازی و متناقض خودداری می‌کند.
9. وضعیت اسناد را صادقانه اعلام می‌کند.
10. قبل از اعلام `Implementation Ready` تمام شروط این سند را کنترل می‌کند.

عدم مطالعه این فایل، کمبود زمان، محدودیت Context، ناآشنایی Agent یا ناقص‌بودن کد فعلی، هیچ‌کدام مجوز ثبت مستند ناقص یا متناقض نیستند.

---

# 1. مأموریت پوشه `specs`

پوشه `specs` باید هم‌زمان نقش‌های زیر را ایفا کند:

1. **مرجع رسمی محصول:** سامانه دقیقاً چه رفتاری باید داشته باشد.
2. **مرجع رسمی دامنه:** هر مفهوم، داده، Rule، State و Lifecycle متعلق به کدام Domain است.
3. **مرجع رسمی مالکیت:** کدام ماژول مالک Record، API، Operation و Audit است.
4. **مرجع رسمی UI/UX:** هر نقش چه صفحه‌ای، چه Stateهایی و چه Actionهایی می‌بیند.
5. **مرجع رسمی معماری:** مرزها، Providerها، Adapterها، Dependencyها و Integrationها چیست.
6. **مرجع رسمی امنیت:** Capability، ACL، Record Rule، Method Check، Company Scope، Delegation و Audit چگونه‌اند.
7. **مرجع رسمی نسخه‌بندی:** Baseline، Iteration، Historical، Superseded و Change Set چگونه مدیریت می‌شوند.
8. **مرجع رسمی ردیابی:** نیاز تا تصمیم، صفحه، ماژول، معماری، امنیت، Migration و Test قابل دنبال‌کردن باشد.
9. **حافظه سازمانی پروژه:** تصمیم‌ها مستقل از حافظه اشخاص و گفتگوها باقی بمانند.
10. **قرارداد تحویل به اجرا:** تیم توسعه برای فهم رفتار مطلوب مجبور به حدس‌زدن نباشد.
11. **مبنای Gap Analysis:** اختلاف کد با Specification به‌صورت Gap قابل اندازه‌گیری باشد.
12. **مبنای Acceptance:** قابل اثبات باشد که پیاده‌سازی چه زمانی با تصمیم مورد توافق منطبق است.

هر فایل باید حداقل یکی از این مأموریت‌ها را به‌صورت روشن پوشش دهد. فایل بدون هدف، مالک، وضعیت یا ارتباط ردیابی‌شده مجاز نیست.

---

# 2. قواعد غیرقابل‌مذاکره پروژه

## 2.1. نسخه ۸ مرجع فعال است

- Baseline فعال: `CAS UI Workspace v8 — Through Iteration 12`.
- نسخه ۸ نباید برای سازگاری با کد، Prototype یا ماژول قدیمی کاهش یابد.
- نبود قابلیت در کد فعلی به معنی Optional بودن آن قابلیت نیست.
- اختلاف کد با Baseline باید به‌عنوان `Implementation Gap` ثبت شود.
- هیچ Agent حق ندارد تصمیم Product را با مشاهده محدودیت فنی فعلی بازنویسی کند.
- تغییر Baseline فقط با تصمیم صریح مالک محصول و ثبت Decision و Change Set مجاز است.

## 2.2. تغییر مستقیم Odoo Core ممنوع است

- هیچ سندی نباید ویرایش مستقیم Odoo Core را پیشنهاد دهد.
- پیاده‌سازی باید با Custom Addon، Extension، Adapter یا Override کنترل‌شده انجام شود.
- هر Override باید دلیل، محل، Upgrade Risk، Fallback و Test Strategy داشته باشد.
- استفاده از Monkey Patch بدون Decision معماری ممنوع است.

## 2.3. Workspace مالک Business Data نیست

`cas_workspace` فقط می‌تواند مالک این موارد باشد:

- Layout و ترتیب Widgetها؛
- Dashboard Configuration؛
- Theme، Density و UI Preference؛
- State موقت رابط؛
- Registry و Orchestration تجربه؛
- Reference سبک Recent History در محدوده مصوب.

Workspace نباید مالک این Domainها شود:

- Personal Task؛
- Organizational Action؛
- Calendar Event و Invitation؛
- Message و Conversation؛
- Work Report؛
- Document و Attachment Business Lifecycle؛
- Correspondence؛
- Workflow و Approval؛
- Employee، Assignment، Shift و Attendance.

## 2.4. قابلیت استاندارد Odoo دوباره ساخته نمی‌شود

- ابتدا باید Gap Analysis انجام شود.
- قابلیت استاندارد مناسب باید Reuse شود.
- Extension فقط برای Gap اثبات‌شده مجاز است.
- ساخت مدل موازی برای Mail، Discuss، Calendar، Attachment یا Activity بدون Decision ممنوع است.

## 2.5. امنیت فقط UI نیست

- مخفی‌کردن Button یا Route کنترل امنیتی محسوب نمی‌شود.
- Backend باید مجوز را دوباره بررسی کند.
- Search Result، Count، Title، Metadata و Export نیز داده‌اند.
- استفاده از `sudo()` برای دورزدن Permission کاربر ممنوع است.
- هر Operation حساس باید Method Check و Audit داشته باشد.

## 2.6. هر Domain فقط یک مالک اصلی دارد

- یک Record نباید دو Owner داشته باشد.
- Consumer می‌تواند View یا Projection داشته باشد، نه مالکیت Lifecycle.
- Workspace، Reporting و Search مالک داده منبع نیستند.
- مالکیت باید در `V8_Module_Ownership_Map.md` ثبت شود.

## 2.7. هیچ تصمیمی فقط در چت باقی نمی‌ماند

هر تصمیم قطعی باید حداقل در یکی از این سطوح ثبت شود:

- Canonical Baseline؛
- Decision Record؛
- Architecture Contract؛
- Module Specification؛
- Page Specification؛
- Change Set؛
- Traceability Matrix.

---

# 3. ترتیب مطالعه اجباری پیش از هر تغییر

Agent باید پیش از نوشتن حتی یک خط، این اسناد را به‌ترتیب بخواند:

1. `specs/README.md`
2. `00_Project/V8_Canonical_Baseline.md`
3. `00_Project/Documentation_Governance.md`
4. `00_Project/Traceability_Matrix.md`
5. `00_Project/Version_History.md`
6. `00_Project/Historical_Document_Register.md`
7. `01_Product/Terminology.md`
8. `01_Product/UX_Principles.md`
9. `03_Modules/V8_Module_Ownership_Map.md`
10. `03_Modules/V8_Dependency_Map.md`
11. `03_Modules/V8_Provider_Registry.md`
12. `05_Architecture/Module_Boundaries.md`
13. `05_Architecture/Capability_And_Security_Model.md`
14. `05_Architecture/Domain_Model.md`
15. `05_Architecture/Integration_Map.md`
16. `00_Project/Open_Questions.md`
17. تمام Page، Module، Decision، Architecture و Change Setهای مرتبط با موضوع.

خواندن فقط فایل هدف ممنوع است.

## 3.1. جست‌وجوی اجباری قبل از نگارش

در کل `specs` باید برای این موارد جست‌وجو شود:

- نام قابلیت به فارسی و انگلیسی؛
- نام ماژول و Domain؛
- Route و Navigation Key؛
- Capability و Permission؛
- Entity، Model و Record Type؛
- Provider و Adapter؛
- Decision ID؛
- نسخه‌های قبلی قابلیت؛
- اصطلاحات مترادف؛
- `Historical`؛
- `Superseded`؛
- `Needs Review`؛
- `Open Question`؛
- `Implementation Ready`؛
- `Out of Scope`؛
- `Future`؛
- `Migration`؛
- `Security`؛
- `Acceptance Criteria`.

## 3.2. خروجی مرحله مطالعه

Agent باید پیش از تغییر برای خودش مشخص کند:

- Baseline حاکم چیست؟
- مالک Domain کیست؟
- سند اصلی کدام است؟
- اسناد وابسته کدام‌اند؟
- تصمیم موجود است یا جدید؟
- تعارض تاریخی وجود دارد؟
- این تغییر Product است یا Technical Detail؟
- آیا Migration لازم است؟
- آیا Security Scope تغییر می‌کند؟
- آیا UI، API، Provider یا Test نیز متأثر است؟

---

# 4. سلسله‌مراتب اعتبار اسناد

در صورت تعارض، ترتیب اعتبار به شکل زیر است:

1. تصمیم صریح و جدید مالک محصول؛
2. `V8_Canonical_Baseline.md`؛
3. Decision Record فعال؛
4. Architecture Contract فعال؛
5. Module Specification فعال؛
6. Security Specification فعال؛
7. Page Specification فعال؛
8. Change Set فعال؛
9. Traceability و Aggregation Matrix؛
10. Historical Documents؛
11. Prototype، Mock Data و Screenshot؛
12. کد فعلی؛
13. گفتگو، یادداشت و Commit message.

قواعد:

- سند پایین‌تر حق نقض سند بالاتر را ندارد.
- کد فعلی مرجع Product نیست.
- Prototype مدرک تجربه است، نه مالکیت یا امنیت.
- اگر تعارض قابل حل نیست، باید `Conflict Record` یا `Open Question` ایجاد شود.
- Agent حق انتخاب سلیقه‌ای یکی از دو سند متعارض را ندارد.

---

# 5. وضعیت‌های رسمی اسناد

فقط وضعیت‌های زیر مجازند:

## 5.1. `Draft`

- در حال شکل‌گیری؛
- قابل استناد نهایی نیست؛
- Open Question ممکن است داشته باشد.

## 5.2. `Needs Review`

- محتوای اصلی نوشته شده؛
- نیازمند بازبینی محصول، معماری یا امنیت است.

## 5.3. `Agreed`

- تصمیم محصولی پذیرفته شده؛
- الزاماً آماده پیاده‌سازی نیست.

## 5.4. `Consolidated`

- اثر تصمیم در اسناد وابسته تجمیع شده است.

## 5.5. `Implementation Ready`

فقط وقتی مجاز است که:

- Scope نهایی است؛
- Owner مشخص است؛
- Security کامل است؛
- Contractها مشخص‌اند؛
- Migration تعیین شده؛
- Acceptance Criteria قابل آزمون‌اند؛
- Open Question مسدودکننده وجود ندارد؛
- Traceability کامل است؛
- Test Strategy نوشته شده؛
- Performance و Failure Mode بررسی شده‌اند.

## 5.6. `Historical`

- برای تاریخ نگهداری می‌شود؛
- مرجع فعال نیست؛
- باید جانشین خود را معرفی کند.

## 5.7. `Superseded`

- با سند جدید جایگزین شده؛
- نباید به‌عنوان تصمیم جاری استفاده شود.

## 5.8. `Rejected`

- پیشنهاد بررسی و رد شده است؛
- دلیل رد باید ثبت شود.

## 5.9. `Deprecated`

- هنوز ممکن است در اجرا وجود داشته باشد؛
- برای طراحی جدید مجاز نیست؛
- Migration Path باید مشخص باشد.

---

# 6. قواعد واژگان الزام‌آور

## 6.1. کلمات هنجاری

- **MUST / باید:** الزام قطعی؛ عدم رعایت نقض Specification است.
- **MUST NOT / نباید:** ممنوعیت قطعی.
- **SHOULD / بهتر است:** قاعده پیش‌فرض؛ انحراف نیازمند دلیل ثبت‌شده است.
- **SHOULD NOT / بهتر است نشود:** رفتار نامطلوب؛ انحراف باید توجیه شود.
- **MAY / می‌تواند:** اختیاری و مجاز؛ نبود آن نقض نیست.

## 6.2. عبارت‌های مبهم ممنوع

این عبارت‌ها بدون تعریف شرط دقیق ممنوع‌اند:

- در صورت نیاز؛
- معمولاً؛
- شاید؛
- احتمالاً؛
- مناسب؛
- سریع؛
- امن؛
- تا حد ممکن؛
- کاربرپسند؛
- استاندارد؛
- بهینه؛
- در آینده؛
- و غیره؛
- مشابه؛
- برحسب شرایط.

هر عبارت باید به شرط، مسئول، معیار یا Scope تبدیل شود.

### نادرست

> نتایج باید سریع نمایش داده شوند.

### درست

> Query اولیه Search باید در صدک ۹۵ برای ۲۰ نتیجه و داده مرجع تعیین‌شده کمتر از ۸۰۰ میلی‌ثانیه پاسخ دهد؛ Timeout Provider پس از ۳ ثانیه به حالت `unavailable` تبدیل می‌شود.

---

# 7. قواعد نام‌گذاری

## 7.1. فایل‌ها

- Markdown با پسوند `.md`؛
- نام انگلیسی خوانا؛
- `Pascal_Case` یا الگوی فعلی پوشه؛
- بدون فاصله؛
- بدون نام‌های مبهم مانند `new.md`، `final.md`، `latest.md`؛
- نسخه در Metadata، نه نام فایل، مگر سند تاریخی خاص.

## 7.2. Decisionها

```text
DEC-NNN-Descriptive-Title.md
```

- شماره یکتا؛
- شماره قبلی بازاستفاده نمی‌شود؛
- عنوان باید تصمیم را توصیف کند؛
- Decision حذف نمی‌شود؛ Status آن تغییر می‌کند.

## 7.3. Capabilityها

```text
domain.operation
```

نمونه:

- `search.use`
- `report.self.read`
- `report.scope.review`
- `dashboard.configuration.manage`

قواعد:

- lowercase؛
- پایدار؛
- مستقل از Label نمایشی؛
- Capability با ACL یکی نیست؛
- Capability مبهم مانند `admin` ممنوع است.

## 7.4. Routeها

- فنی و پایدار؛
- Label نمایشی از Route جدا؛
- Route منسوخ باید Redirect یا Controlled Not Found داشته باشد؛
- تغییر Route باید Migration و Deep Link Impact داشته باشد.

## 7.5. Providerها

```text
<domain>.<capability>.provider
```

هر Provider باید Owner، Contract، Permission و Failure Mode داشته باشد.

## 7.6. Entityها و Modelها

- نام مفهومی در Product Docs؛
- نام فنی در Module/Architecture Docs؛
- Mapping میان آن‌ها باید واضح باشد؛
- یک مفهوم با چند نام بدون ثبت در Terminology ممنوع است.

---

# 8. Metadata اجباری هر سند

هر سند فعال باید در ابتدای خود جدول Metadata داشته باشد:

```markdown
| مشخصه | مقدار |
|---|---|
| شناسه | `...` |
| عنوان | ... |
| نوع سند | Product / Page / Module / Architecture / Security / Decision / ChangeSet |
| وضعیت | `Draft / Needs Review / Agreed / Consolidated / Implementation Ready` |
| Baseline | `CAS UI Workspace v8 — Through Iteration 12` |
| مالک محصول | ... |
| مالک دامنه | `cas_...` |
| ماژول‌های متأثر | ... |
| تصمیم‌های مرجع | `DEC-...` |
| نسخه سند | `x.y` |
| آخرین بازبینی | `YYYY-MM-DD` |
| جایگزین سند | در صورت Superseded |
```

## 8.1. قواعد نسخه سند

- تغییر نگارشی بدون تغییر معنا: Patch؛
- افزودن جزئیات سازگار: Minor؛
- تغییر Contract یا رفتار: Major؛
- تغییر Major باید Change Set داشته باشد.

---

# 9. تشخیص نوع تغییر

پیش از ایجاد فایل، تغییر باید طبقه‌بندی شود.

## 9.1. Product Decision

وقتی پاسخ می‌دهد:

- کاربر چه چیزی می‌خواهد؟
- رفتار مورد انتظار چیست؟
- چه Scopeای وجود دارد؟
- چه چیزی Out of Scope است؟

## 9.2. Architecture Decision

وقتی پاسخ می‌دهد:

- مسئولیت کجا قرار می‌گیرد؟
- چه Contract یا Boundaryای انتخاب می‌شود؟
- چه Trade-offی پذیرفته شده است؟

## 9.3. Module Specification

وقتی یک ماژول را از نظر Owner، Model، Lifecycle، API، Security، Migration و Test تعریف می‌کند.

## 9.4. Page Specification

وقتی رفتار یک Route، Screen، Role View یا Interaction Flow را تعریف می‌کند.

## 9.5. Change Set

وقتی اثر یک مجموعه تصمیم را میان چند سند و ماژول ثبت می‌کند.

## 9.6. Impact Assessment

وقتی اثر را تحلیل می‌کند اما هنوز Contract نهایی نیست.

## 9.7. Gap Analysis

وقتی تفاوت Specification فعال با وضعیت اجرا را ثبت می‌کند.

## 9.8. Open Question

وقتی تصمیم برای ادامه لازم است و پاسخ هنوز قطعی نیست.

---

# 10. قالب اجباری Decision Record

هر Decision باید این بخش‌ها را داشته باشد:

1. Metadata؛
2. Context؛
3. Problem Statement؛
4. Decision؛
5. Rationale؛
6. Alternatives Considered؛
7. Reasons for Rejection؛
8. Consequences؛
9. Security Impact؛
10. Data Ownership Impact؛
11. Migration Impact؛
12. UI/UX Impact؛
13. Performance Impact؛
14. Testing Impact؛
15. Observability Impact؛
16. Out of Scope؛
17. Superseded Documents؛
18. Related Documents؛
19. Acceptance Conditions؛
20. Open Questions غیرمسدودکننده.

### Decision ناقص ممنوع

Decision صرفاً شامل یک جمله «تصمیم گرفته شد X» قابل قبول نیست.

---

# 11. قالب اجباری Module Specification

هر ماژول باید حداقل شامل این بخش‌ها باشد:

1. Purpose؛
2. Domain Definition؛
3. Ownership؛
4. Responsibilities؛
5. Non-Responsibilities؛
6. Dependencies؛
7. Optional Integrations؛
8. Conceptual Model؛
9. Technical Models؛
10. Field Semantics؛
11. State Machine؛
12. Lifecycle؛
13. Commands؛
14. Queries؛
15. Events؛
16. Provider Contract؛
17. Adapter Contract؛
18. Access Capabilities؛
19. ACL؛
20. Record Rules؛
21. Method Checks؛
22. Company Scope؛
23. Delegation؛
24. Audit؛
25. Data Retention؛
26. Privacy؛
27. Attachments؛
28. Search؛
29. Reporting؛
30. Projection؛
31. Migration؛
32. Upgrade Strategy؛
33. Failure Modes؛
34. Partial Failure Policy؛
35. Idempotency؛
36. Concurrency؛
37. Performance؛
38. Caching؛
39. Observability؛
40. Unit Tests؛
41. Integration Tests؛
42. Security Tests؛
43. Load Tests؛
44. Acceptance Criteria؛
45. Out of Scope؛
46. Open Questions؛
47. Traceability.

## 11.1. Non-Responsibilities الزامی است

هر Module Spec باید روشن کند چه چیزی متعلق به آن نیست. این بخش از گسترش بی‌قاعده ماژول جلوگیری می‌کند.

---

# 12. قالب اجباری Page Specification

هر Page Spec باید شامل این موارد باشد:

1. Page ID؛
2. Route؛
3. Display Name؛
4. Purpose؛
5. Supported Roles؛
6. Required Capabilities؛
7. Source Providers؛
8. Data Owner؛
9. Entry Points؛
10. Exit Points؛
11. Layout Regions؛
12. Responsive Behavior؛
13. RTL Behavior؛
14. Keyboard Navigation؛
15. Screen Reader Semantics؛
16. Loading State؛
17. Empty State؛
18. Ready State؛
19. Forbidden State؛
20. Unavailable State؛
21. Error State؛
22. Partial Data State؛
23. Offline/Disconnected State در صورت کاربرد؛
24. Actions؛
25. Validation؛
26. Confirmation؛
27. Undo/Recovery؛
28. Deep Links؛
29. Filters؛
30. Sorting؛
31. Pagination/Virtualization؛
32. Permissions؛
33. Sensitive Data Masking؛
34. Audit-relevant Operations؛
35. Performance Budget؛
36. Analytics/Telemetry؛
37. Acceptance Criteria؛
38. Regression Scenarios؛
39. Mobile Constraints؛
40. Historical/Superseded Notes.

## 12.1. نقش‌ها باید جدا نوشته شوند

عبارت «برای همه کاربران» بدون تعیین تفاوت نقش‌ها مجاز نیست. حداقل باید رفتار این گروه‌ها بررسی شود:

- کاربر عادی؛
- سرپرست؛
- مدیر؛
- مدیرعامل؛
- مدیر سامانه؛
- ناظر یا ممیز؛
- کاربر دارای دسترسی تفویض‌شده؛
- کاربر بدون Scope؛
- کاربر Multi-company.

---

# 13. قالب اجباری Architecture Contract

هر Contract باید این موارد را تعریف کند:

1. Context؛
2. Owner؛
3. Consumer؛
4. Preconditions؛
5. Input Schema؛
6. Output Schema؛
7. Field Semantics؛
8. Validation؛
9. Authorization؛
10. Company Scope؛
11. Error Codes؛
12. Failure Modes؛
13. Timeout؛
14. Retry Policy؛
15. Idempotency؛
16. Concurrency؛
17. Transaction Boundary؛
18. Partial Success؛
19. Pagination؛
20. Sorting؛
21. Caching؛
22. Invalidation؛
23. Versioning؛
24. Backward Compatibility؛
25. Observability؛
26. Audit؛
27. Performance Budget؛
28. Security Tests؛
29. Contract Tests؛
30. Example Request؛
31. Example Response؛
32. Negative Examples.

---

# 14. قواعد مالکیت داده

برای هر Entity باید مشخص شود:

- System of Record؛
- Module Owner؛
- Creator؛
- Updater؛
- Reader Scope؛
- Lifecycle Owner؛
- Audit Owner؛
- Retention Owner؛
- Search Provider؛
- Reporting Projection؛
- Attachment Relation؛
- Deletion Policy.

## 14.1. Projection مالکیت نیست

وجود داده در Dashboard، Search Index، Report Projection یا Cache به معنی مالکیت Consumer نیست.

## 14.2. Snapshot مالکیت نیست

Snapshot برای تاریخچه و Audit نگهداری می‌شود، اما Record منبع همچنان Owner اصلی خود را دارد.

## 14.3. Reference باید حداقلی باشد

Consumer فقط شناسه و Metadata لازم را نگه می‌دارد. کپی بی‌دلیل داده منبع ممنوع است.

---

# 15. قواعد Security Specification

هر قابلیت باید حداقل این ماتریس را پوشش دهد:

- چه کسی Record را می‌بیند؟
- چه کسی ایجاد می‌کند؟
- چه کسی ویرایش می‌کند؟
- چه کسی حذف یا Archive می‌کند؟
- چه کسی Submit می‌کند؟
- چه کسی Review می‌کند؟
- چه کسی Approve می‌کند؟
- چه کسی Export می‌کند؟
- چه کسی Attachment را می‌بیند؟
- چه کسی Delegation می‌دهد؟
- چه کسی Audit را می‌بیند؟

## 15.1. کنترل‌های اجباری

- Capability؛
- ACL؛
- Record Rule؛
- Method Check؛
- Field-level Rule در صورت نیاز؛
- Section-level Rule در صورت نیاز؛
- Company Scope؛
- Organization Scope؛
- Delegation Scope؛
- Effective Date؛
- ID Tampering Protection؛
- Export Authorization؛
- Attachment Authorization؛
- Audit Logging؛
- Revocation Behavior.

## 15.2. Delegation

هر Delegation باید داشته باشد:

- Grantor؛
- Grantee؛
- Domain؛
- Operation؛
- Scope؛
- Effective From؛
- Effective To؛
- Reason؛
- Revocation؛
- Audit؛
- عدم گسترش خودکار به Domainهای دیگر.

## 15.3. تست‌های امنیتی اجباری

- RPC مستقیم؛
- تغییر ID؛
- تغییر Company؛
- تغییر Assignment؛
- تغییر Profile؛
- دسترسی پس از Revocation؛
- Export غیرمجاز؛
- Attachment غیرمجاز؛
- Count Leakage؛
- Search Leakage؛
- Cache Leakage؛
- Multi-company Crossing؛
- Delegation Expiry؛
- Race Condition در Approval.

---

# 16. قواعد Provider و Adapter

هر Provider باید مشخص کند:

- Provider Key؛
- Module Owner؛
- Capability ارائه‌شده؛
- Input؛
- Output؛
- Safe Serializer؛
- Permission Check؛
- Company Scope؛
- Pagination؛
- Sort؛
- Timeout؛
- Unavailable State؛
- Version؛
- Observability؛
- Contract Tests.

قواعد:

- Provider اختیاری نباید Workspace را Crash کند.
- Workspace نباید dependency سخت به همه Providerها داشته باشد.
- Provider نباید داده غیرمجاز را حتی در Count افشا کند.
- نام Provider باید پایدار باشد.
- حذف Provider باید Migration و Fallback داشته باشد.

---

# 17. قواعد Workflow و Approval

هر Workflow Spec باید شامل این موارد باشد:

- Trigger؛
- Instance Owner؛
- States؛
- Transitions؛
- Actor؛
- Preconditions؛
- Guards؛
- Sequential/Parallel Policy؛
- Delegation؛
- Escalation؛
- Deadline؛
- Return for Correction؛
- Cancellation؛
- Reopen؛
- Finalization؛
- Locking؛
- Audit؛
- Notification؛
- Idempotency؛
- Concurrent Decision Policy؛
- Failure Recovery.

هیچ State Machine نباید فقط به‌صورت فهرست Stateها نوشته شود؛ Transitionها و Actorها الزامی‌اند.

---

# 18. قواعد Form Engine و Dynamic Forms

هر فرم پویا باید مشخص کند:

- Definition؛
- Version؛
- Publication State؛
- Effective Date؛
- Section؛
- Field Key پایدار؛
- Field Type؛
- Required Rule؛
- Readonly Rule؛
- Visibility Rule؛
- Domain Rule؛
- Validation؛
- Regex؛
- Range؛
- Conditional Logic؛
- Formula؛
- Option Source؛
- Security؛
- Snapshot؛
- Submission؛
- Answer Storage؛
- Projection؛
- Migration؛
- Historical Rendering.

قواعد:

- گزارش تاریخی با Form Version جدید Revalidate نمی‌شود.
- Field Key پس از انتشار بدون Migration تغییر نمی‌کند.
- Label قابل تغییر است، اما Snapshot تاریخی حفظ می‌شود.
- Formula دلخواه ناامن در Browser ممنوع است.
- داده پویا برای Analytics باید Projection تایپ‌شده داشته باشد.

---

# 19. قواعد Work Report

تصمیم‌های قطعی:

- واحد گزارش `Shift Occurrence` است.
- شیفت عبوری از نیمه‌شب یک گزارش دارد.
- یک شخص در یک شیفت حداکثر یک گزارش دارد.
- چند Assignment در یک شیفت در یک گزارش ترکیبی با Sectionهای جدا ثبت می‌شوند.
- Applicability می‌تواند `Required`، `Optional` یا `Disabled` باشد.
- در حالت `Disabled` فرم، Draft و Reminder شخصی وجود ندارد.
- دسترسی به گزارش دیگران فقط تابع رابطه زیردستی نیست.
- Access Grant می‌تواند Scope و Operation مستقل بدهد.
- Reviewer فقط بخش‌های مجاز را می‌بیند.
- Export باید همان Scope نمایش را رعایت کند.
- فایل و Evidence فعلاً از زیرساخت موجود استفاده می‌کنند.
- بازطراحی بنیادی Document Infrastructure خارج از Scope نسخه ۸ و موضوع آینده است.

هر تغییر Work Report باید حداقل این اسناد را بررسی کند:

- Decision 017؛
- Decision 019؛
- Decision 020؛
- Module Specification؛
- Security Specification؛
- Assignment Model؛
- Form Engine Architecture؛
- Dynamic Work Report Page؛
- Change Set؛
- Aggregation Matrix.

---

# 20. قواعد Dashboard و Workspace Configuration

- Workspace مالک Business Record نیست.
- Admin Dashboard Management Center مالک UI Configuration است.
- Configuration باید Versioned باشد.
- Draft و Published جدا هستند.
- Publish باید Audit شود.
- Rollback باید نسخه جدید ایجاد کند، نه تاریخچه را حذف کند.
- Company Default، Role/Profile و User Preference باید precedence روشن داشته باشند.
- Company می‌تواند مقدار را Lock کند.
- User فعلاً فقط ترتیب Widgetهای مجاز را تغییر می‌دهد.
- Hide/Show کاربر تا تصمیم آینده فعال نیست.
- Mandatory Widget قابل حذف نیست.
- Preview باید بدون اثر بر کاربران Production باشد.

---

# 21. قواعد Notification

- زیرساخت Odoo Mail/Discuss/Inbox/Notification باید اولویت Reuse داشته باشد.
- Notification System موازی بدون Gap Analysis ممنوع است.
- Notification با Action یکی نیست.
- خوانده‌شدن Notification به معنی انجام Action نیست.
- Notification Center Route مستقل باقی می‌ماند.
- Deep Link باید Permission را دوباره بررسی کند.
- Count باید از منبع واحد بیاید.
- نبود Realtime نباید صفحه را غیرقابل استفاده کند.
- Extensionهای آینده باید فقط Gapهای اثبات‌شده مانند Snooze، Aggregation یا Action Button را پوشش دهند.

---

# 22. قواعد Search و Recent History

- Search قابلیت Overlay/Command Palette است.
- Route مستقل Search وجود ندارد.
- Capability `search.use` فقط بازکردن Palette را مجاز می‌کند.
- هر Provider Permission خودش را اعمال می‌کند.
- Recent History ماژول مستقل نیست.
- Recent History فقط Reference سبک نگه می‌دارد.
- Permission هنگام نمایش و Open دوباره بررسی می‌شود.
- حذف History هیچ Business Recordی را حذف نمی‌کند.
- مسیرهای حساس قابل استثنا هستند.
- Search Count و Metadata نباید نشت کنند.

---

# 23. قواعد Calendar

- رویداد شخصی خود کاربر می‌تواند Personal Task مرتبط داشته باشد.
- تخصیص کار به دیگری متعلق به Action Hub است.
- دعوت جلسه متعلق به Calendar/Event است.
- Invitation Permission با Task Assignment Permission یکسان نیست.
- Directory Search باید Server-side و محدود باشد.
- بارگذاری تمام کارکنان در Browser ممنوع است.
- Task Assignment باید Scope سازمانی را در Backend Resolve کند.
- Partial Failure باید تفصیلی گزارش شود.
- تاریخ ذخیره‌شده استاندارد Odoo/UTC باقی می‌ماند.
- ورودی و نمایش جلالی از Adapter استفاده می‌کند.

---

# 24. قواعد Document و Attachment

در نسخه ۸:

- فایل واقعی در زیرساخت Attachment/Document موجود ذخیره می‌شود.
- Form Engine نوع فیلد و Validation را تعریف می‌کند.
- Domain مقصد ارتباط معنایی فایل را نگه می‌دارد.
- Permission فایل باید جداگانه بررسی شود.
- Metadata فایل غیرمجاز نباید نمایش داده شود.

موضوعات آینده که باید Decision مستقل داشته باشند:

- Document Versioning؛
- Retention؛
- Archive؛
- Classification؛
- Digital Signature؛
- Check-in/Check-out؛
- Nextcloud Integration؛
- Legal Hold؛
- Advanced Access Policy.

عبارت «در آینده بازطراحی می‌شود» بدون ثبت در Future Scope یا Open Questions کافی نیست.

---

# 25. قواعد Migration

هر تغییر Schema، Contract، Ownership، Route یا State باید Migration را بررسی کند.

Migration Spec باید شامل این موارد باشد:

1. Source State؛
2. Target State؛
3. Data Mapping؛
4. Default Values؛
5. Invalid Data Policy؛
6. Duplicate Policy؛
7. Historical Preservation؛
8. Audit Preservation؛
9. Attachment Mapping؛
10. Access Mapping؛
11. Dry Run؛
12. Backup؛
13. Rollback؛
14. Idempotency؛
15. Batch Size؛
16. Performance؛
17. Verification Query؛
18. Reconciliation Report؛
19. Cutover؛
20. Dual Read/Write در صورت نیاز؛
21. Removal of Legacy Path؛
22. Post-migration Monitoring.

هیچ Agent حق ندارد بنویسد «Migration لازم نیست» مگر دلیل قابل اثبات ارائه کند.

---

# 26. قواعد Performance

هر Specification باید در صورت مرتبط‌بودن این موارد را تعیین کند:

- Dataset Assumption؛
- Expected Volume؛
- Peak Concurrency؛
- Response Time Budget؛
- Pagination؛
- Batch Size؛
- Cache؛
- Invalidation؛
- Index Strategy؛
- Background Job؛
- Timeout؛
- Retry؛
- Memory Constraint؛
- Browser Rendering Limit؛
- Virtualization؛
- Attachment Size؛
- Export Limit؛
- Load Test Scenario.

عبارت «باید سریع باشد» ممنوع است.

---

# 27. قواعد Observability و Audit

هر عملیات حساس باید مشخص کند:

- چه Eventی ثبت می‌شود؛
- چه Metadataای ثبت می‌شود؛
- چه داده حساسی ثبت نمی‌شود؛
- Correlation ID چگونه است؛
- Actor چگونه مشخص می‌شود؛
- Source و Target چیست؛
- Failure چگونه ثبت می‌شود؛
- Alert Threshold چیست؛
- Retention Log چیست؛
- چه کسی Audit را می‌بیند.

حداقل Eventهای عمومی:

- create؛
- update؛
- submit؛
- approve؛
- return؛
- reject؛
- delete/archive؛
- permission denied؛
- delegation granted/revoked؛
- export؛
- configuration published؛
- migration failure؛
- provider timeout.

---

# 28. قواعد Testing

هر Feature باید با توجه به دامنه این لایه‌ها را پوشش دهد:

## 28.1. Unit Test

- Rule؛
- Resolver؛
- Validation؛
- State Transition؛
- Permission Function؛
- Formula؛
- Mapping.

## 28.2. Integration Test

- Module-to-module؛
- Provider؛
- Workflow؛
- Calendar؛
- Mail؛
- Attachment؛
- Notification؛
- Migration.

## 28.3. Security Test

- Unauthorized Read؛
- Unauthorized Write؛
- ID Tampering؛
- Company Crossing؛
- Delegation Expiry؛
- Export Leakage؛
- Search Leakage؛
- Attachment Leakage.

## 28.4. UI Test

- RTL؛
- Keyboard؛
- Screen Reader؛
- Responsive؛
- Loading؛
- Empty؛
- Error؛
- Forbidden؛
- Unavailable؛
- Focus Restore؛
- Scroll؛
- Deep Link.

## 28.5. Regression Test

- تصمیم‌های نسخه قبل که باید حفظ شوند؛
- Routeهای منسوخ؛
- Stateهای تاریخی؛
- Backward Compatibility؛
- Upgrade Odoo.

## 28.6. Load Test

- داده حجیم؛
- Search؛
- Directory؛
- Report Generation؛
- Message History؛
- Export؛
- Batch Migration.

---

# 29. قواعد Acceptance Criteria

Acceptance Criteria باید:

- قابل مشاهده باشد؛
- قابل آزمون باشد؛
- Actor داشته باشد؛
- Preconditions داشته باشد؛
- Outcome روشن داشته باشد؛
- Failure Behavior داشته باشد؛
- Permission را پوشش دهد؛
- Stateهای غیرعادی را پوشش دهد.

### نادرست

> صفحه باید خوب کار کند.

### درست

> کاربر دارای `report.self.create` و Reporting Applicability برابر `Required` باید برای Shift Occurrence فعال خود دقیقاً یک Draft ببیند؛ تلاش دوم باید همان Draft را بازگرداند و Record جدید نسازد.

---

# 30. قواعد Traceability

هر تغییر باید حداقل این زنجیره را داشته باشد:

```text
Requirement
→ Product Decision
→ Decision Record
→ Page/Module Specification
→ Architecture/Security Contract
→ Change Set
→ Traceability Matrix
→ Acceptance Criteria
→ Test Strategy
```

## 30.1. سند یتیم ممنوع

سندی که هیچ مرجع ورودی یا خروجی ندارد باید اصلاح یا Historical شود.

## 30.2. لینک دوطرفه

در حد امکان:

- Decision به Module و Page لینک دهد؛
- Module و Page به Decision لینک دهند؛
- Change Set تمام اسناد متأثر را فهرست کند؛
- Traceability وضعیت را نشان دهد.

## 30.3. شناسه پایدار

شناسه Requirement، Decision، Page و Change Set نباید پس از انتشار تغییر کند.

---

# 31. قواعد Historical و Supersede

هیچ سند تاریخی صرفاً حذف نمی‌شود، مگر اینکه:

- Duplicate بی‌ارزش باشد؛
- داده حساس اشتباه داشته باشد؛
- مالک محصول حذف را تأیید کند؛
- دلیل در Change Set ثبت شود.

برای Historical کردن:

1. Status را `Historical` یا `Superseded` کن.
2. Baseline قدیمی را ثبت کن.
3. سند جانشین را لینک کن.
4. دلیل را ثبت کن.
5. Historical Register را به‌روزرسانی کن.
6. لینک‌های فعال را به جانشین هدایت کن.
7. از باقی‌ماندن ادعای `Current` جلوگیری کن.

سند Historical نباید بی‌هشدار در فهرست اسناد فعال نمایش داده شود.

---

# 32. قواعد Open Question

Open Question باید شامل این موارد باشد:

- ID؛
- Question؛
- Why It Matters؛
- Blocking/Non-blocking؛
- Affected Documents؛
- Options؛
- Recommended Option در صورت وجود؛
- Decision Owner؛
- Due Condition؛
- Status؛
- Resolution Link.

عبارت مبهم «بعداً تصمیم می‌گیریم» ممنوع است.

وقتی پاسخ داده شد:

- سؤال حذف نمی‌شود؛
- Status به `Resolved` تغییر می‌کند؛
- Decision یا سند نهایی لینک می‌شود؛
- اسناد متأثر به‌روزرسانی می‌شوند.

---

# 33. قواعد Out of Scope و Future Scope

هر Out of Scope باید:

- دقیق باشد؛
- دلیل داشته باشد؛
- نسخه هدف آینده در صورت معلوم‌بودن داشته باشد؛
- مانع نسخه فعلی نبودن را روشن کند؛
- وابستگی آینده را مشخص کند؛
- در Open Questions یا Roadmap قابل ردیابی باشد.

Out of Scope نباید برای فرار از نوشتن Security، Test یا Migration استفاده شود.

---

# 34. قواعد نگارش فارسی و فنی

- متن اصلی فارسی و RTL باشد.
- نام فنی، Model، Capability، Route و Status با Backtick نوشته شود.
- جمله‌ها کامل و غیرمحاوره‌ای باشند.
- هر بند یک مفهوم اصلی داشته باشد.
- عنوان‌ها سلسله‌مراتب منطقی داشته باشند.
- جدول فقط وقتی استفاده شود که مقایسه واقعی وجود دارد.
- فهرست‌ها باید هم‌سطح باشند.
- از نیم‌فاصله صحیح استفاده شود.
- تاریخ‌ها به فرمت `YYYY-MM-DD` ثبت شوند.
- تاریخ ذخیره سیستم استاندارد باشد؛ نمایش شمسی موضوع UI است.
- واژه جدید باید در Terminology ثبت شود.
- ترجمه آزاد نام Entity فنی بدون Mapping ممنوع است.
- از عبارت‌های تبلیغاتی و اغراق‌آمیز خودداری شود.
- مثال باید با Rule نوشته‌شده سازگار باشد.

---

# 35. پروتکل اجباری AI Agent

هر AI Agent باید این Workflow را اجرا کند:

## مرحله A — فهم درخواست

1. درخواست کاربر را به Requirementهای اتمی تقسیم کند.
2. Scope، Role، Module و Version را استخراج کند.
3. تفاوت تصمیم جدید با توضیح قبلی را تشخیص دهد.
4. از پرسیدن سؤال تکراری خودداری کند.
5. اگر اطلاعات کافی است، بدون توقف کار کند.

## مرحله B — بازیابی Context

1. README را بخواند.
2. Baseline را بخواند.
3. Terminology را بخواند.
4. Ownership Map را بخواند.
5. اسناد مستقیم موضوع را بخواند.
6. کل `specs` را جست‌وجو کند.
7. Historical Conflictها را شناسایی کند.

## مرحله C — طبقه‌بندی تغییر

1. Product Decision؟
2. Architecture Decision؟
3. Module Spec؟
4. Page Spec؟
5. Security؟
6. Change Set؟
7. Historical Update؟
8. Open Question؟

## مرحله D — تحلیل اثر

حداقل این اثرها بررسی شوند:

- Product؛
- UI/UX؛
- Domain Ownership؛
- Models؛
- API؛
- Provider؛
- Security؛
- Multi-company؛
- Delegation؛
- Audit؛
- Migration؛
- Performance؛
- Testing؛
- Documentation؛
- Historical Records.

## مرحله E — نگارش

1. سند مناسب را انتخاب کند.
2. Metadata را کامل کند.
3. Ruleهای قطعی را با MUST بنویسد.
4. موارد باز را جدا کند.
5. مثال مثبت و منفی ارائه کند.
6. Acceptance Criteria بنویسد.
7. Cross-reference ایجاد کند.

## مرحله F — تجمیع

Agent نباید فقط فایل هدف را تغییر دهد. باید بررسی کند آیا این موارد هم باید تغییر کنند:

- README پوشه؛
- Canonical Baseline؛
- Terminology؛
- Decision Index؛
- Module Index؛
- Architecture Index؛
- Page Index؛
- Change Set Index؛
- Traceability Matrix؛
- Aggregation Matrix؛
- Historical Register؛
- Open Questions.

## مرحله G — Validation

1. لینک‌های نسبی؛
2. شناسه‌های تکراری؛
3. Statusهای متناقض؛
4. نام‌های متناقض؛
5. Versionهای قدیمی؛
6. Ownerهای چندگانه؛
7. Capabilityهای تکراری؛
8. Routeهای منسوخ؛
9. Open Questionهای حل‌شده ولی باز؛
10. ادعای Implementation Ready بدون شروط.

## مرحله H — تحویل

گزارش تحویل باید بگوید:

- چه فایل‌هایی تغییر کردند؛
- چرا تغییر کردند؛
- چه تصمیم‌هایی قطعی شدند؛
- چه چیزهایی باز ماندند؛
- چه Validationی انجام شد؛
- آیا کد تغییر کرد یا نه؛
- Branch و PR چیست؛
- Merge انجام شده یا نه.

---

# 36. ممنوعیت‌های صریح Agent

Agent حق ندارد:

1. فقط بر اساس حافظه پاسخ دهد.
2. فایل هدف را بدون جست‌وجوی کل Specs ویرایش کند.
3. Decision موجود را با Decision تکراری جایگزین کند.
4. فایل Historical را Current اعلام کند.
5. تصمیم محصول را برای کد فعلی ضعیف کند.
6. Workspace را مالک Business Data کند.
7. قابلیت Odoo را بدون Gap Analysis دوباره بسازد.
8. `sudo()` را راه‌حل Permission معرفی کند.
9. UI Hidden را امنیت تلقی کند.
10. Open Question را پنهان کند.
11. بدون Owner مدل جدید پیشنهاد دهد.
12. بدون Migration تغییر Schema پیشنهاد دهد.
13. بدون Failure Mode Contract بنویسد.
14. بدون Acceptance Criteria سند را کامل اعلام کند.
15. بدون Traceability فایل جدید ایجاد کند.
16. Decision را حذف کند تا تناقض ظاهری حل شود.
17. فایل کاربر را بدون اجازه روی `main` Push کند.
18. تغییرات مستندی و کدی را در یک Scope مبهم مخلوط کند.
19. ادعا کند کاری انجام شده که ابزار آن را تأیید نکرده است.
20. از عبارت «همه چیز کامل است» بدون Checklist استفاده کند.

---

# 37. چک‌لیست ایجاد سند جدید

قبل از ایجاد فایل:

- [ ] فایل مشابه وجود ندارد.
- [ ] نوع سند مشخص است.
- [ ] جای پوشه صحیح است.
- [ ] نام فایل مطابق قواعد است.
- [ ] شناسه یکتا است.
- [ ] Owner مشخص است.
- [ ] Baseline مشخص است.
- [ ] Decision مرجع مشخص است.
- [ ] Metadata کامل است.
- [ ] Scope و Non-Scope نوشته شده‌اند.
- [ ] Security بررسی شده است.
- [ ] Migration بررسی شده است.
- [ ] Performance بررسی شده است.
- [ ] Test Strategy نوشته شده است.
- [ ] Acceptance Criteria نوشته شده است.
- [ ] Cross-referenceها اضافه شده‌اند.
- [ ] Index مربوط به‌روزرسانی شده است.
- [ ] Traceability به‌روزرسانی شده است.
- [ ] Change Set به‌روزرسانی شده است.

---

# 38. چک‌لیست ویرایش سند موجود

- [ ] Status فعلی بررسی شد.
- [ ] سند Historical نیست یا تغییر Historical توجیه دارد.
- [ ] نسخه سند افزایش یافت.
- [ ] معنای قبلی ناخواسته حذف نشد.
- [ ] Decisionهای مرتبط بررسی شدند.
- [ ] Owner تغییر نکرده یا Decision دارد.
- [ ] Capabilityها بررسی شدند.
- [ ] Routeها بررسی شدند.
- [ ] Security Scope بررسی شد.
- [ ] Migration Impact بررسی شد.
- [ ] Acceptance Criteria اصلاح شد.
- [ ] Change Set اصلاح شد.
- [ ] Traceability اصلاح شد.
- [ ] لینک‌های ورودی و خروجی بررسی شدند.
- [ ] Historical Register در صورت نیاز اصلاح شد.

---

# 39. چک‌لیست Security Review

- [ ] Actorها مشخص‌اند.
- [ ] Capabilityها مشخص‌اند.
- [ ] ACL مشخص است.
- [ ] Record Rule مشخص است.
- [ ] Method Check مشخص است.
- [ ] Company Scope مشخص است.
- [ ] Organization Scope مشخص است.
- [ ] Delegation مشخص است.
- [ ] Effective Date مشخص است.
- [ ] ID Tampering بررسی شده است.
- [ ] Search Leakage بررسی شده است.
- [ ] Count Leakage بررسی شده است.
- [ ] Export Permission بررسی شده است.
- [ ] Attachment Permission بررسی شده است.
- [ ] Field/Section Security بررسی شده است.
- [ ] Audit مشخص است.
- [ ] Revocation Behavior مشخص است.
- [ ] Multi-company Test تعریف شده است.

---

# 40. چک‌لیست UI/UX Review

- [ ] نقش‌ها جدا شده‌اند.
- [ ] Route مشخص است.
- [ ] Capability مشخص است.
- [ ] Loading وجود دارد.
- [ ] Empty وجود دارد.
- [ ] Ready وجود دارد.
- [ ] Forbidden وجود دارد.
- [ ] Unavailable وجود دارد.
- [ ] Error وجود دارد.
- [ ] Partial Data وجود دارد.
- [ ] RTL واقعی بررسی شده است.
- [ ] Keyboard بررسی شده است.
- [ ] Screen Reader بررسی شده است.
- [ ] Mobile بررسی شده است.
- [ ] Focus Management بررسی شده است.
- [ ] Scroll Contract بررسی شده است.
- [ ] Validation بررسی شده است.
- [ ] Confirmation/Undo بررسی شده است.
- [ ] Deep Link بررسی شده است.
- [ ] Performance Budget مشخص است.
- [ ] Acceptance Criteria قابل تست است.

---

# 41. چک‌لیست Module Review

- [ ] Purpose روشن است.
- [ ] Owner روشن است.
- [ ] Non-responsibilities روشن است.
- [ ] Dependencyها مشخص‌اند.
- [ ] Circular Dependency وجود ندارد.
- [ ] Models مشخص‌اند.
- [ ] State Machine مشخص است.
- [ ] Commands و Queries مشخص‌اند.
- [ ] Events مشخص‌اند.
- [ ] API/Provider Contract مشخص است.
- [ ] Security کامل است.
- [ ] Migration کامل است.
- [ ] Failure Mode کامل است.
- [ ] Idempotency بررسی شده است.
- [ ] Concurrency بررسی شده است.
- [ ] Performance بررسی شده است.
- [ ] Observability بررسی شده است.
- [ ] Test Strategy کامل است.
- [ ] Traceability کامل است.

---

# 42. چک‌لیست قبل از Commit

- [ ] فقط فایل‌های Scope تغییر کرده‌اند.
- [ ] تغییر ناخواسته وجود ندارد.
- [ ] READMEهای پوشه به‌روزند.
- [ ] لینک‌ها معتبرند.
- [ ] شناسه تکراری نیست.
- [ ] Status متناقض نیست.
- [ ] Baseline قدیمی در سند فعال باقی نمانده است.
- [ ] اصطلاح جدید در Terminology ثبت شده است.
- [ ] Owner در Ownership Map ثبت شده است.
- [ ] Decision در Index ثبت شده است.
- [ ] Change Set به‌روز است.
- [ ] Traceability به‌روز است.
- [ ] Open Questionها به‌روزند.
- [ ] هیچ ادعای بدون مدرک وجود ندارد.
- [ ] Commit message دقیق است.

---

# 43. چک‌لیست قبل از Pull Request

PR مستندی باید شامل این موارد باشد:

- [ ] هدف؛
- [ ] Baseline؛
- [ ] Scope؛
- [ ] فایل‌های اصلی؛
- [ ] تصمیم‌های قطعی؛
- [ ] تصمیم‌های باز؛
- [ ] اثر ماژولی؛
- [ ] اثر امنیتی؛
- [ ] اثر Migration؛
- [ ] Validation انجام‌شده؛
- [ ] خارج از Scope؛
- [ ] اعلام صریح اینکه کد تغییر کرده یا نه؛
- [ ] اعلام اینکه PR Draft است یا Ready؛
- [ ] عدم Merge مستقیم بدون تأیید.

---

# 44. چک‌لیست `Implementation Ready`

هیچ سند یا ماژولی بدون تیک‌خوردن همه موارد زیر `Implementation Ready` نیست:

- [ ] Product Scope نهایی؛
- [ ] Owner نهایی؛
- [ ] Models نهایی؛
- [ ] State Machine نهایی؛
- [ ] API نهایی؛
- [ ] Provider نهایی؛
- [ ] Security نهایی؛
- [ ] Delegation نهایی؛
- [ ] Multi-company نهایی؛
- [ ] Migration نهایی؛
- [ ] Performance Budget نهایی؛
- [ ] Failure Policy نهایی؛
- [ ] Observability نهایی؛
- [ ] Acceptance Criteria نهایی؛
- [ ] Unit Tests مشخص؛
- [ ] Integration Tests مشخص؛
- [ ] Security Tests مشخص؛
- [ ] Regression Tests مشخص؛
- [ ] Load Tests در صورت نیاز؛
- [ ] Open Question مسدودکننده صفر؛
- [ ] Traceability کامل؛
- [ ] Change Set کامل؛
- [ ] Review محصول؛
- [ ] Review معماری؛
- [ ] Review امنیت.

---

# 45. الگوی خلاصه سند جدید

```markdown
# عنوان سند

| مشخصه | مقدار |
|---|---|
| شناسه | `...` |
| نوع | `...` |
| وضعیت | `Draft` |
| Baseline | `CAS UI Workspace v8 — Through Iteration 12` |
| مالک دامنه | `cas_...` |
| تصمیم مرجع | `DEC-...` |
| نسخه سند | `1.0` |

## هدف

## Context

## Scope

## Out of Scope

## مالکیت

## قواعد قطعی

## مدل یا ساختار

## Security

## Failure Modes

## Migration

## Performance

## Observability

## Test Strategy

## Acceptance Criteria

## Open Questions

## اسناد مرتبط
```

این الگو حداقل است؛ قالب تخصصی نوع سند بر آن مقدم است.

---

# 46. الگوی Conflict Record

```markdown
# Conflict — عنوان

| مشخصه | مقدار |
|---|---|
| شناسه | `CONFLICT-NNN` |
| وضعیت | `Open` |
| سند اول | `...` |
| سند دوم | `...` |
| Baseline حاکم | `...` |
| مالک تصمیم | `...` |

## شرح تعارض

## اثر تعارض

## سلسله‌مراتب اعتبار

## گزینه‌ها

## پیشنهاد

## تصمیم نهایی

## اسناد نیازمند اصلاح
```

Agent نباید تعارض را با حذف خاموش یکی از جملات پنهان کند.

---

# 47. الگوی Implementation Gap

```markdown
# GAP — عنوان

| مشخصه | مقدار |
|---|---|
| شناسه | `GAP-NNN` |
| Specification | `...` |
| وضعیت کد | `...` |
| شدت | `Critical / High / Medium / Low` |
| مالک اجرا | `...` |

## رفتار مورد انتظار

## رفتار فعلی

## فاصله

## ریسک

## تغییرات لازم

## Migration

## Tests

## معیار بسته‌شدن Gap
```

Gap نباید Specification را تضعیف کند.

---

# 48. ساختار رسمی پوشه‌ها

```text
specs/
├── README.md
├── 00_Project/
├── 01_Product/
├── 02_UI_UX/
├── 03_Modules/
├── 04_Decisions/
├── 05_Architecture/
├── 06_ChangeSets/
└── Module_Aggregation_Matrix.md
```

## 48.1. `00_Project`

Baseline، Governance، Version History، Traceability، Historical Register و Open Questions.

## 48.2. `01_Product`

Vision، Terminology، UX Principles، Personas و Business Rules مشترک.

## 48.3. `02_UI_UX`

Page، Route، Role View، Interaction، Responsive و Accessibility.

## 48.4. `03_Modules`

مالکیت، Specification، Security، Provider و Module Impact.

## 48.5. `04_Decisions`

Decision Recordهای پایدار و شماره‌دار.

## 48.6. `05_Architecture`

Context، Domain، Boundary، Data Flow، Integration، Security و Contract.

## 48.7. `06_ChangeSets`

تجمیع تغییرات میان چند سند و ماژول.

---

# 49. منابع رسمی فعال

مرجع آغاز:

1. `00_Project/V8_Canonical_Baseline.md`
2. `00_Project/Documentation_Governance.md`
3. `00_Project/Traceability_Matrix.md`
4. `01_Product/Terminology.md`
5. `01_Product/UX_Principles.md`
6. `03_Modules/V8_Module_Ownership_Map.md`
7. `03_Modules/V8_Dependency_Map.md`
8. `03_Modules/V8_Provider_Registry.md`
9. `05_Architecture/Module_Boundaries.md`
10. `05_Architecture/Capability_And_Security_Model.md`
11. `05_Architecture/Domain_Model.md`
12. `05_Architecture/Integration_Map.md`
13. `Module_Aggregation_Matrix.md`

---

# 50. دستور نهایی برای Agent آینده

وقتی کاربر گفت «مستندات را به‌روز کن»، Agent نباید فوراً یک فایل را ویرایش کند. باید:

1. این README را کامل بخواند.
2. Baseline و Governance را بخواند.
3. موضوع را در کل `specs` جست‌وجو کند.
4. مالک Domain را تعیین کند.
5. نوع تغییر را طبقه‌بندی کند.
6. تمام اسناد متأثر را فهرست کند.
7. تغییر را بدون کاهش نسخه ۸ اعمال کند.
8. Decision، Architecture، Module، Page، Security و Change Set را در صورت اثر به‌روزرسانی کند.
9. Traceability و Indexها را اصلاح کند.
10. Historical Conflictها را علامت بزند.
11. Open Questionها را جدا کند.
12. لینک‌ها، Statusها، Ownerها و Versionها را Validation کند.
13. فقط روی Branch مجاز Commit کند.
14. بدون اجازه مستقیم به `main` Push یا Merge نکند.
15. در گزارش نهایی دقیقاً بگوید چه کرده و چه نکرده است.

> **اصل نهایی:** مستند کامل فقط متنی طولانی نیست. مستند کامل سندی است که مالکیت، رفتار، امنیت، شکست، Migration، Performance، Test، Acceptance و Traceability آن هیچ فضای حدس‌زدنی برای تیم بعدی باقی نگذارد.
