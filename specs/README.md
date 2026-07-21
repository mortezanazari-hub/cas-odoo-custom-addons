# CAS Design & Product Specifications

این پوشه مرجع رسمی تصمیمات محصول، طراحی رابط کاربری، معماری، مالکیت دامنه‌ها، امنیت، قراردادهای بین‌ماژولی و مسیر آماده‌سازی اجرای پروژه **CAS Organizational Workspace** است.

> **مرجع فعال و نهایی محصول:** `CAS UI Workspace v8 — Through Iteration 12`
>
> نسخه ۸ مورد تأیید است و نباید برای سازگارشدن با کد، Prototype یا ماژول‌های قدیمی تضعیف، ساده‌سازی یا عقب‌گرد داده شود. کد و ماژول‌ها باید در مراحل بعد با این Specificationها منطبق شوند.

---

# دستورالعمل اجباری برای انسان و Agent هوش مصنوعی

## اعلام الزام

هر انسان، توسعه‌دهنده، تحلیل‌گر، طراح، Agent هوش مصنوعی یا ابزار خودکار که قصد دارد یکی از کارهای زیر را انجام دهد، **باید پیش از هر تحلیل، پیشنهاد، ایجاد فایل، ویرایش فایل، Commit یا Pull Request این README را کامل بخواند و از تمام قواعد آن تبعیت کند**:

- ایجاد مستند جدید؛
- ویرایش مستند موجود؛
- ثبت تصمیم محصولی؛
- ثبت تصمیم معماری؛
- طراحی یا اصلاح یک صفحه؛
- افزودن یا اصلاح ماژول؛
- تغییر مالکیت داده یا دامنه؛
- تعریف API، Provider، Capability یا Integration؛
- تغییر نسخه، Iteration یا Baseline؛
- تغییر امنیت، دسترسی، Scope، ACL یا Record Rule؛
- اصلاح Traceability، Change Set یا Impact Assessment؛
- آماده‌کردن مستندات برای پیاده‌سازی؛
- مقایسه مستندات با کد؛
- اعلام اینکه یک ماژول یا قابلیت `Implementation Ready` است.

عدم مطالعه این فایل، دلیل قابل‌قبولی برای ثبت مستند ناقص، ایجاد تعارض، حذف تصمیم، شکستن ردیابی یا کاهش دامنه نسخه ۸ نیست.

## خروجی اجباری Agent پیش از شروع ویرایش

Agent باید پیش از نخستین تغییر، در تحلیل داخلی خود این موارد را تعیین کند و در صورت طولانی‌بودن کار، خلاصه آن را به کاربر اعلام کند:

1. Baseline فعال چیست؟
2. درخواست کاربر Product Decision، Documentation Correction، Architecture Change، Module Specification یا Implementation Gap است؟
3. Source of Truth کدام اسناد هستند؟
4. چه فایل‌هایی احتمالاً متأثر می‌شوند؟
5. چه مواردی قطعی و چه مواردی مبهم‌اند؟
6. آیا تغییر فقط مستندی است یا کد نیز صریحاً درخواست شده است؟
7. آیا Branch جدا لازم است؟ برای تغییرات گسترده پاسخ پیش‌فرض «بله» است.

---

# بخش ۱ — مأموریت پوشه `specs`

پوشه `specs` فقط محل نگهداری توضیحات پراکنده یا یادداشت‌های طراحی نیست. این پوشه باید هم‌زمان نقش‌های زیر را ایفا کند:

1. **مرجع رسمی محصول** برای مشخص‌کردن اینکه سامانه چه رفتاری باید داشته باشد.
2. **مرجع رسمی مالکیت** برای تعیین اینکه هر داده، Rule، Lifecycle و Operation متعلق به کدام Domain یا ماژول است.
3. **مرجع رسمی معماری** برای تعیین مرز ماژول‌ها، قراردادها، Providerها، Integrationها و وابستگی‌ها.
4. **مرجع رسمی امنیت** برای Capability، ACL، Record Rule، Method Check، Company Scope، Delegation و Audit.
5. **مرجع رسمی UI/UX** برای صفحه، Route، State، نقش، تعامل، Accessibility و Responsive behavior.
6. **مرجع رسمی نسخه‌بندی** برای Baseline، Iteration، Supersede، Historical Status و Change Set.
7. **مرجع رسمی ردیابی** از نیاز و تصمیم تا صفحه، ماژول، معماری، امنیت، Migration و Test.
8. **قرارداد تحویل به تیم پیاده‌سازی**؛ به‌گونه‌ای که تیم اجرا برای فهم رفتار مطلوب مجبور به حدس‌زدن یا بازسازی تصمیم‌ها از روی گفتگوها نباشد.
9. **حافظه سازمانی پروژه**؛ تصمیم‌ها باید مستقل از حافظه افراد و چت‌ها قابل بازیابی باشند.
10. **مبنای کنترل تغییرات**؛ هر تغییر آینده باید اثر خود را بر تصمیم‌ها و اسناد مرتبط روشن کند.

هر سندی که یکی از این اهداف را برآورده نمی‌کند، جای درست، Status درست یا ساختار درست ندارد و باید اصلاح شود.

---

# بخش ۲ — قواعد غیرقابل‌مذاکره

## ۲.۱. نسخه ۸ مرجع است

- Baseline فعال پروژه `CAS UI Workspace v8 — Through Iteration 12` است.
- هیچ Agent حق ندارد برای هماهنگ‌شدن با کد فعلی، نسخه ۸ را کاهش دهد.
- هیچ Agent حق ندارد قابلیت تأییدشده نسخه ۸ را صرفاً به‌دلیل نبودن آن در پیاده‌سازی فعلی حذف یا Optional اعلام کند.
- وضعیت فعلی کد، محدودیت طراحی محصول نیست؛ فقط ورودی مرحله Gap Analysis و برنامه پیاده‌سازی است.
- هر تعارض میان کد فعلی و Specification فعال، به‌عنوان **Implementation Gap** ثبت می‌شود، نه دلیل تغییر Specification.

## ۲.۲. تغییر Odoo Core ممنوع است

- هیچ سندی نباید تغییر مستقیم Odoo Core را پیشنهاد، تجویز یا پیش‌فرض بگیرد.
- تمام قابلیت‌های CAS باید از طریق Custom Addon، Extension، Adapter، Override کنترل‌شده یا Integration رسمی پیاده‌سازی شوند.
- هر Override باید محل، دلیل، Upgrade Risk، Fallback و Test Strategy داشته باشد.

## ۲.۳. Workspace مالک داده کسب‌وکاری نیست

`cas_workspace` فقط می‌تواند مالک موارد زیر باشد:

- تنظیمات ظاهری Workspace؛
- Layout و ترتیب Widgetها؛
- Theme، Density و Preferenceهای UI؛
- Configuration مرکز مدیریت داشبورد؛
- State موقت رابط کاربری؛
- Registry و Orchestration تجربه کاربری؛
- Reference سبک Recent History در محدوده تعریف‌شده.

Workspace نباید مالک داده‌های Personal Task، Action، Calendar Event، Invitation، Message، Work Report، Document، Correspondence، Workflow، Approval، Employee، Shift یا سایر Domainها شود.

## ۲.۴. امنیت فقط در UI تعریف نمی‌شود

- مخفی‌کردن دکمه یا Route، کنترل امنیتی کافی نیست.
- هر Operation حساس باید کنترل Backend داشته باشد.
- هر Specification امنیتی باید ACL، Record Rule، Method Check، Company Scope، ID Tampering، Delegation و Audit را بررسی کند.
- استفاده از `sudo()` برای عبور از Permission کاربر در Search، Provider، Workspace یا Report ممنوع است.
- شمارنده، عنوان، Metadata، Search Result و Export نیز داده محسوب می‌شوند و نباید اطلاعات غیرمجاز نشت دهند.

## ۲.۵. اسناد باید قابل ردیابی باشند

هیچ تصمیمی نباید فقط در متن یک Page Spec یا گفت‌وگو باقی بماند. هر تصمیم باید:

- شناسه داشته باشد؛
- Status داشته باشد؛
- مالک دامنه داشته باشد؛
- مرجع بالادستی داشته باشد؛
- اثر ماژولی داشته باشد؛
- در Traceability ثبت شود؛
- در Change Set مرتبط درج شود؛
- اگر مشترک یا معماری است، Decision Record یا Architecture Contract داشته باشد.

## ۲.۶. هیچ ادعایی بدون وضعیت ثبت نمی‌شود

هر گزاره باید یکی از این ماهیت‌ها را داشته باشد:

- تصمیم قطعی؛
- Requirement قطعی؛
- پیشنهاد؛
- فرض موقت؛
- نمونه؛
- سؤال باز؛
- وضعیت فعلی پیاده‌سازی؛
- هدف آینده.

مخلوط‌کردن این ماهیت‌ها در یک متن، بدون برچسب، ممنوع است.

---

# بخش ۳ — ترتیب مطالعه اجباری قبل از هر تغییر

Agent باید قبل از تغییر هر فایل، اسناد زیر را دقیقاً به همین ترتیب مطالعه کند:

1. این فایل: `specs/README.md`
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
17. تمام اسناد صفحه، ماژول، Decision، Architecture و Change Set مرتبط با موضوع تغییر.

Agent حق ندارد فقط فایل هدف را باز کند و بدون مطالعه زنجیره وابسته آن را ویرایش کند.

## حداقل جست‌وجوی اجباری

پیش از نوشتن، Agent باید در کل `specs` برای موارد زیر جست‌وجو کند:

- نام قابلیت؛
- نام ماژول؛
- نام Domain؛
- Route؛
- Capability؛
- Model یا Entity؛
- شناسه Decision؛
- اصطلاحات هم‌معنی فارسی و انگلیسی؛
- نسخه‌های قبلی همان صفحه یا قابلیت؛
- عبارت‌های `Historical`، `Superseded`، `Needs Review`، `Open Question` و `Implementation Ready` مرتبط.

هدف از جست‌وجو جلوگیری از ساخت سند موازی، Decision تکراری، نام‌گذاری متعارض یا مالکیت دوگانه است.

## مطالعه محتوای کامل، نه فقط Snippet

- برای تصمیم‌گیری درباره یک سند، خواندن عنوان یا چند خط اول کافی نیست.
- اگر سند طولانی است، Agent باید بخش‌های مرتبط و Metadata آن را کامل بخواند.
- برای PDF یا اسناد تصویری باید محتوای بصری مرتبط نیز بررسی شود.
- نتیجه Search فقط ابزار کشف فایل است و جایگزین خواندن سند مرجع نیست.

---

# بخش ۴ — سلسله‌مراتب مرجعیت

در صورت تعارض، ترتیب اعتبار اسناد چنین است:

```text
V8 Canonical Baseline
→ Decision Recordهای Agreed نسخه ۸
→ Architecture Contractهای نسخه ۸
→ Module Specificationهای Implementation Ready
→ Page Specificationهای نسخه ۸
→ Change Setهای نسخه ۸
→ Impact Assessmentها
→ اسناد Historical نسخه ۷ و نسخه ۴
```

## روش برخورد با تعارض

Agent در صورت مشاهده تعارض باید:

1. تعارض را صریحاً شناسایی کند.
2. دو یا چند سند متعارض را نام ببرد.
3. طبق سلسله‌مراتب بالا سند مرجع را تعیین کند.
4. سند پایین‌دستی را اصلاح کند.
5. در صورت نیاز Status آن را `Partially Superseded` یا `Superseded` کند.
6. `superseded_by` و `supersedes` را ثبت کند.
7. Traceability و Historical Register را به‌روزرسانی کند.
8. هیچ متن متعارضی را بدون علامت باقی نگذارد.

حذف بی‌سروصدای تصمیم تاریخی ممنوع است. تصمیم قبلی باید قابل بازیابی بماند.

## تعارض میان دو سند هم‌سطح

اگر دو سند هم‌سطح متعارض باشند:

1. Status و تاریخ اثر بررسی شود.
2. Decision یا Change Set مرجع بررسی شود.
3. اگر مرجع روشن نیست، موضوع Open Question یا Decision جدید شود.
4. Agent حق ندارد بر اساس سلیقه یکی را انتخاب و دیگری را حذف کند.

---

# بخش ۵ — انتخاب محل درست برای سند

## `00_Project`

برای اسناد بالادستی پروژه:

- Baseline؛
- نسخه‌بندی؛
- حاکمیت مستندات؛
- Traceability؛
- Historical Register؛
- Open Questions؛
- قواعد همکاری انسان و Agent؛
- وضعیت کلی پروژه.

## `01_Product`

برای اسناد محصولی غیرصفحه‌ای:

- Vision؛
- اهداف کسب‌وکار؛
- نقش‌ها و Personaها؛
- اصول UX؛
- Terminology و Glossary؛
- قواعد مشترک تجربه محصول.

## `02_UI_UX`

برای Specification تجربه کاربری:

- Page Specification؛
- Role-specific View؛
- Workspace Shell؛
- Admin Center؛
- Route و Navigation؛
- Widget؛
- Modal، Drawer و Overlay behavior؛
- Responsive و Accessibility؛
- Stateهای UI.

## `03_Modules`

برای مرجع ماژولی:

- مالکیت Domain؛
- Dependency Map؛
- Provider Registry؛
- Module Specification؛
- Security ماژول؛
- API Contract ماژول؛
- Migration؛
- Test Strategy؛
- Impact Assessment.

هر ماژول مستقل باید پوشه مستقل داشته باشد.

## `04_Decisions`

برای تصمیم‌هایی که:

- چند صفحه را تحت‌تأثیر قرار می‌دهند؛
- چند ماژول را درگیر می‌کنند؛
- مالکیت داده را تعیین می‌کنند؛
- انتخاب معماری مهم هستند؛
- تغییرشان هزینه یا Migration دارد؛
- باید برای آینده قابل استناد باشند.

Decision نباید به‌جای Specification کامل استفاده شود؛ Decision فقط «چه تصمیمی و چرا» را ثبت می‌کند.

## `05_Architecture`

برای:

- System Context؛
- Domain Model؛
- Data Flow؛
- Integration Map؛
- Module Boundaries؛
- Provider Architecture؛
- Security Model؛
- Assignment Model؛
- Notification Gap Analysis؛
- معماری تخصصی Domainها.

## `06_ChangeSets`

برای بسته تغییر از یک Baseline به Baseline یا Iteration جدید:

- دامنه تغییر؛
- تصمیم‌های اضافه‌شده؛
- اسناد متأثر؛
- Migration مفهومی؛
- Regression Risk؛
- شرط تکمیل.

Change Set جایگزین Specification نیست.

---

# بخش ۶ — نام‌گذاری فایل‌ها و شناسه‌ها

## ۶.۱. قواعد نام فایل

- نام فایل انگلیسی و پایدار باشد.
- از فاصله استفاده نشود؛ از `_` یا `-` مطابق الگوی همان پوشه استفاده شود.
- نام فایل مبهم مانند `New_Doc.md`، `Final.md`، `Latest.md`، `Notes.md` یا `Temp.md` ممنوع است.
- شماره نسخه داخل نام فایل فقط در اسناد واقعاً نسخه‌دار و در صورت نیاز استفاده شود.
- برای سند فعال، واژه‌هایی مانند `final-final` یا `new` ممنوع است.
- نام ماژول باید دقیقاً با Technical Name مورد توافق یکسان باشد.
- Capitalization باید با فایل‌های هم‌نوع همان پوشه سازگار باشد.
- تغییر نام فایل باید دلیل، Migration لینک و بررسی ارجاعات داشته باشد.

## ۶.۲. شناسه Page

الگوی پیشنهادی:

```text
PAGE-{ROLE}-{DOMAIN}-{NNN}
```

مثال:

```text
PAGE-EMP-WR-001
PAGE-ADM-DASH-001
```

## ۶.۳. شناسه Decision

```text
DEC-NNN
```

نام فایل:

```text
DEC-NNN-Short-English-Title.md
```

شماره Decision نباید بدون بررسی Index و فایل‌های موجود انتخاب شود.

## ۶.۴. شناسه Change Set

```text
CS-{DOMAIN}-{VERSION-OR-TOPIC}
```

مثال:

```text
CS-WORKSPACE-V8
CS-WORK-REPORT-DYNAMIC-FORM
```

## ۶.۵. شناسه Capability

- به‌صورت `domain.operation` باشد.
- کوتاه، صریح و پایدار باشد.
- Capability با Model ACL یا Group Name یکسان فرض نشود.
- نمونه: `search.use`, `report.self.read`, `report.scope.review`.

## ۶.۶. شناسه Provider

- نام Provider باید Domain را نشان دهد.
- Provider نباید با نام UI Component تعریف شود.
- Provider Key باید در Registry یکتا باشد.

## ۶.۷. شناسه Open Question

```text
OQ-{DOMAIN}-{NNN}
```

شناسه سؤال حل‌شده دوباره استفاده نمی‌شود.

---

# بخش ۷ — Metadata اجباری هر سند

هر سند فعال باید در ابتدای خود یک جدول Metadata داشته باشد. فیلدها با توجه به نوع سند انتخاب می‌شوند، اما حذف فیلدهای بنیادی ممنوع است.

## Metadata عمومی

```markdown
| مشخصه | مقدار |
|---|---|
| شناسه | `...` |
| عنوان رسمی | `...` |
| نوع سند | `Page Specification / Decision / Architecture / Module Specification / Change Set / Impact Assessment` |
| وضعیت | `Draft / Proposed / Needs Review / Agreed / Implementation Ready / Verified / Historical / Partially Superseded / Superseded` |
| نسخه محصول | `CAS UI Workspace v8 — Through Iteration 12` |
| نسخه سند | `1.0` |
| مالک دامنه | `...` |
| ماژول مالک | `...` |
| اسناد بالادستی | `...` |
| اسناد پایین‌دستی | `...` |
| supersedes | `... / ندارد` |
| superseded_by | `... / ندارد` |
| تاریخ اثر | `YYYY-MM-DD / نامشخص` |
| آخرین بازنگری | `YYYY-MM-DD` |
```

## قواعد Metadata

- `Agreed` فقط برای تصمیم یا رفتار تأییدشده استفاده می‌شود.
- `Implementation Ready` فقط با تکمیل تمام شروط بخش مربوط مجاز است.
- `Verified` فقط پس از تطبیق با پیاده‌سازی و تست معتبر مجاز است.
- `Historical` یعنی سند برای تاریخچه نگهداری می‌شود و مرجع فعال نیست.
- `Partially Superseded` باید دقیقاً مشخص کند کدام بخش‌ها منسوخ شده‌اند.
- `Superseded` باید سند جایگزین را معرفی کند.
- Statusهای ساختگی یا مبهم ممنوع‌اند.
- Version سند با Version محصول اشتباه نشود.
- تاریخ باید دقیق و استاندارد باشد؛ عبارت «امروز» یا «اخیراً» در Metadata ممنوع است.
- ماژول مالک نباید صرفاً بر اساس محل نمایش در UI تعیین شود.

---

# بخش ۸ — قالب اجباری Page Specification

هر Page Specification باید حداقل بخش‌های زیر را داشته باشد:

1. Metadata کامل.
2. هدف صفحه.
3. مسئله‌ای که صفحه حل می‌کند.
4. نقش‌ها و Personaهای مجاز.
5. Preconditions.
6. Route و Navigation Entry.
7. Capability لازم برای مشاهده.
8. منابع داده و Providerها.
9. مالک داده هر بخش.
10. ساختار صفحه.
11. Componentها و Widgetها.
12. اطلاعات هر Component.
13. عملیات اصلی و ثانویه.
14. رفتار Desktop.
15. رفتار Tablet.
16. رفتار Mobile.
17. رفتار RTL.
18. Keyboard Navigation.
19. Accessibility.
20. Loading State.
21. Empty State.
22. Error State.
23. Forbidden State.
24. Unavailable Provider State.
25. Partial Failure State.
26. Offline یا Reconnect behavior در صورت ارتباط Realtime.
27. Validationهای UI.
28. Validationهای Backend مرتبط.
29. Permission و Scope.
30. Deep Link و Back behavior.
31. Overlay، Focus و Scroll behavior.
32. Audit موردنیاز.
33. Performance و Pagination.
34. Observability.
35. معیارهای پذیرش قابل تست.
36. اثر ماژولی.
37. تصمیم‌های مرتبط.
38. سؤال‌های باز.
39. موارد خارج از دامنه.
40. اسناد مرتبط.

## معیار کیفیت Acceptance Criteria

هر معیار پذیرش باید:

- یک رفتار مشخص داشته باشد؛
- نقش یا Actor را روشن کند؛
- Precondition را روشن کند؛
- Action را روشن کند؛
- نتیجه قابل مشاهده یا قابل اندازه‌گیری داشته باشد؛
- حالت خطا یا عدم مجوز را در صورت ارتباط پوشش دهد.

عبارت «صفحه درست کار کند» معیار پذیرش نیست.

## ممنوعیت‌های Page Specification

- استفاده از عبارت «واضح است» بدون تعریف رفتار.
- استفاده از عبارت «و غیره» برای Requirementهای اصلی.
- ثبت Permission فقط به‌شکل «دکمه مخفی شود».
- استفاده از داده نمونه به‌عنوان Model Contract.
- تعریف مالکیت داده داخل Workspace به‌دلیل نمایش در Workspace.
- ترکیب Invite و Task Assignment به‌عنوان یک Operation.
- تعریف UI بدون Loading/Empty/Error/Forbidden.
- استفاده از واژه «مدیر» بدون تعیین Scope سازمانی.
- تعریف رفتار فقط برای Happy Path.

---

# بخش ۹ — قالب اجباری Module Specification

هر Module Specification باید حداقل این بخش‌ها را داشته باشد:

1. Metadata.
2. هدف ماژول.
3. مسئولیت‌های داخل دامنه.
4. مسئولیت‌های خارج دامنه.
5. داده‌ها و Entityهای مالکیت‌شده.
6. Modelهای مفهومی.
7. Lifecycle هر Entity.
8. State Machine.
9. Invariantها.
10. Business Ruleها.
11. Validationها.
12. Operationها و Commandها.
13. Queryها.
14. API یا Service Contract.
15. Eventهای منتشرشده.
16. Eventهای مصرف‌شده.
17. Providerهای ارائه‌شده.
18. Providerهای مصرف‌شده.
19. Dependencyهای سخت.
20. Dependencyهای اختیاری.
21. رفتار در نبود Dependency اختیاری.
22. ACL.
23. Record Rule.
24. Method Check.
25. Capability Mapping.
26. Company Scope.
27. Delegation.
28. Field-level Security.
29. Attachment Security.
30. Export Security.
31. Audit Log.
32. جلوگیری از ID Tampering.
33. Multi-company behavior.
34. داده مرجع و Seed.
35. Migration Strategy.
36. Rollback Strategy.
37. Backward Compatibility.
38. Performance.
39. Index و Query Strategy.
40. Cache و Invalidation.
41. Observability.
42. Error Taxonomy.
43. Test Strategy.
44. Acceptance Criteria.
45. Upgrade Risk.
46. Out of Scope.
47. Open Questions.
48. اسناد مرتبط.

## تعریف Invariant

Invariant قاعده‌ای است که در تمام مسیرهای UI، RPC، Import، Cron، Server Action و Integration باید برقرار بماند. هر Rule حیاتی باید مشخص کند آیا Invariant است یا فقط UI behavior.

## شروط `Implementation Ready`

یک Module Specification فقط زمانی می‌تواند `Implementation Ready` شود که همه موارد زیر وجود داشته باشند:

- مالکیت Domain قطعی؛
- Model و Lifecycle مشخص؛
- API و Provider Contract مشخص؛
- Security کامل؛
- Multi-company مشخص؛
- Migration مشخص؛
- Test Strategy مشخص؛
- خطاها و Failure Modeها مشخص؛
- Performance و Indexing بررسی‌شده؛
- Dependencyها و Optional behavior مشخص؛
- تصمیم باز بحرانی باقی نمانده؛
- Traceability کامل؛
- معیار پذیرش قابل تست؛
- تعارض با Baseline یا Decision Agreed وجود نداشته باشد.

اگر یکی از این شروط ناقص باشد، Status باید `Needs Review` بماند.

---

# بخش ۱۰ — قالب اجباری Decision Record

هر Decision باید شامل این بخش‌ها باشد:

1. شناسه و عنوان.
2. Status.
3. تاریخ تصمیم.
4. Context.
5. Problem Statement.
6. Constraints.
7. گزینه‌های بررسی‌شده.
8. مزایا و معایب هر گزینه.
9. تصمیم نهایی.
10. دلیل تصمیم.
11. Consequenceهای مثبت.
12. Consequenceهای منفی.
13. ریسک‌ها.
14. اثر بر UI.
15. اثر بر Domain.
16. اثر بر Moduleها.
17. اثر بر Security.
18. اثر بر Migration.
19. اثر بر Test.
20. تصمیم‌های Superseded.
21. Decisionهای وابسته.
22. شرط بازنگری آینده.
23. اسناد مرتبط.

Decision نباید فقط یک جمله اعلام نتیجه باشد.

## چه زمانی Decision جدید لازم است؟

- تغییر مالک داده؛
- تغییر مرز Domain؛
- افزودن ماژول بنیادی؛
- تغییر مدل امنیت یا Scope؛
- تغییر Route یا Interaction مشترک؛
- تغییر سیاست Migration؛
- انتخاب بین ساخت قابلیت جدید و Reuse زیرساخت Odoo؛
- Supersede یک تصمیم Agreed؛
- انتخابی که چند ماژول یا چند صفحه را متأثر می‌کند.

---

# بخش ۱۱ — قالب اجباری Architecture Contract

هر سند معماری باید موارد زیر را پوشش دهد:

- مسئله معماری؛
- Scope؛
- Context Diagram یا توضیح Context؛
- Componentها؛
- مالکیت داده؛
- مرز Transaction؛
- Data Flow؛
- Command Flow؛
- Query Flow؛
- Event Flow؛
- قرارداد ورودی؛
- قرارداد خروجی؛
- Error Contract؛
- Partial Failure؛
- Retry و Idempotency؛
- Permission Boundary؛
- Multi-company؛
- Cache؛
- Invalidation؛
- Performance؛
- Observability؛
- Security؛
- Upgrade Risk؛
- Alternatives؛
- Test Contract؛
- Open Questions.

مثال JSON فقط نمونه است و نباید بدون مشخص‌کردن اینکه Conceptual است، به‌عنوان API نهایی تلقی شود.

## مرز Transaction

هر Flow چندمرحله‌ای باید مشخص کند:

- کدام عملیات Atomic هستند؛
- کدام عملیات Partial Success دارند؛
- در شکست مرحله میانی چه چیزی Rollback می‌شود؛
- چه نتیجه‌ای به کاربر نمایش داده می‌شود؛
- Retry چگونه از Duplicate جلوگیری می‌کند؛
- Audit چه چیزی را ثبت می‌کند.

---

# بخش ۱۲ — قواعد مالکیت دامنه

پیش از افزودن هر Entity یا Field، Agent باید پاسخ دهد:

1. این داده متعلق به کدام Domain است؟
2. مالک Lifecycle آن کدام ماژول است؟
3. چه ماژول‌هایی فقط Consumer هستند؟
4. آیا داده در چند ماژول کپی می‌شود؟ اگر بله، چرا؟
5. Source of Truth چیست؟
6. آیا Projection یا Snapshot لازم است؟
7. چه کسی مجاز به ایجاد، ویرایش، حذف و مشاهده است؟
8. Retention و Archive چیست؟
9. Audit چه چیزی را ثبت می‌کند؟
10. حذف مالک چه اثری بر Referenceها دارد؟

## قواعد قطعی مالکیت فعلی

- `cas_personal_task`: مالک Personal Task و Personal Category.
- `cas_action_hub`: مالک Action یا Task رسمی سازمانی.
- Calendar/Event Domain: مالک Event، Attendee، Invitation و RSVP.
- Odoo Mail/Discuss/Bus: مالک Conversation، Message، Member و Realtime Delivery.
- `cas_work_report`: مالک هویت، دوره، Lifecycle، Review و دسترسی گزارش کار.
- Form Engine: مالک Definition، Version، Field، Rule، Submission Structure و Answer Runtime.
- `cas_activity_catalog`: مالک فعالیت استاندارد سازمانی.
- `cas_organization_core`: مالک Resolution ساختار، Assignment، Hierarchy، Delegation و Scope.
- `cas_workspace`: مالک تجربه و تنظیمات UI خود؛ نه داده Domainها.

هر تغییر این مالکیت‌ها نیازمند Decision Record جدید یا اصلاح Decision موجود است.

## کپی داده

کپی داده فقط در یکی از حالت‌های زیر مجاز است:

- Snapshot تاریخی؛
- Projection تحلیلی؛
- Cache کنترل‌شده؛
- Denormalization با Invalidation مشخص؛
- Audit Evidence.

هر کپی باید Source، دلیل، زمان به‌روزرسانی و سیاست ناسازگاری داشته باشد.

---

# بخش ۱۳ — قواعد Provider و Integration

هر Provider باید مشخص کند:

- Provider Key؛
- ماژول مالک؛
- Resource Typeها؛
- Operationهای ارائه‌شده؛
- Query Contract؛
- Result Contract؛
- Safe Serializer؛
- Permission Revalidation؛
- Pagination؛
- Sort Stability؛
- Timeout behavior؛
- Unavailable behavior؛
- Error behavior؛
- Deep Link Contract؛
- Observability؛
- Versioning.

## ممنوعیت‌ها

- Provider نباید Permission را به Workspace واگذار کند.
- Workspace نباید Model داخلی Provider را حدس بزند.
- Provider نباید با `sudo()` نتیجه غیرمجاز تولید کند.
- Provider نباید Count یا عنوان رکورد غیرمجاز را افشا کند.
- نبود Provider اختیاری نباید باعث Crash Workspace شود.
- Dependency سخت به تمام Providerها ممنوع است مگر در Specification توجیه شود.

## قرارداد Error مشترک

هر Provider باید خطاهای حداقلی زیر را تفکیک کند:

- `forbidden`؛
- `not_found`؛
- `unavailable`؛
- `timeout`؛
- `invalid_request`؛
- `configuration_error`؛
- `partial_failure` در صورت کاربرد.

UI نباید همه خطاها را به یک پیام عمومی غیرقابل اقدام تبدیل کند.

---

# بخش ۱۴ — قواعد Security Documentation

هر تغییر باید حداقل این ابعاد امنیتی را بررسی کند:

1. چه کسی می‌تواند Route را ببیند؟
2. چه کسی می‌تواند رکورد را Query کند؟
3. چه کسی می‌تواند Operation را اجرا کند؟
4. Scope شخصی، تیمی، واحدی، شرکتی یا تفویض‌شده چیست؟
5. آیا ID در Request قابل دستکاری است؟
6. آیا Backend مجدداً Context را Resolve می‌کند؟
7. آیا Multi-company نشت دارد؟
8. آیا Field-level Security لازم است؟
9. آیا Attachment یا Evidence Permission جدا دارد؟
10. آیا Export دسترسی گسترده‌تری ایجاد می‌کند؟
11. آیا Search Result اطلاعات غیرمجاز را نشت می‌دهد؟
12. آیا Count، Badge یا Notification Metadata حساس است؟
13. آیا Audit لازم است؟
14. آیا Delegation تاریخ شروع و پایان دارد؟
15. آیا Capability به‌تنهایی کافی است یا Record Rule هم لازم است؟
16. آیا Reviewer فقط Sectionهای مجاز را می‌بیند؟
17. آیا Admin Configuration با Business Data اشتباه شده است؟

## دسترسی تفویض‌شده

هر Access Grant باید حداقل این مشخصات را داشته باشد:

- دریافت‌کننده؛
- Scope افراد؛
- Scope سازمانی؛
- Scope گزارش یا Resource؛
- Sectionهای مجاز؛
- Operationهای مجاز؛
- تاریخ شروع؛
- تاریخ پایان؛
- تفویض‌کننده؛
- دلیل؛
- قابلیت لغو؛
- Audit.

`View`، `Comment`، `Review`، `Request Correction`، `Approve`، `Export` و `Audit` Operationهای مستقل‌اند و نباید خودکار از یکدیگر نتیجه گرفته شوند.

## تست امنیت اجباری

هر Module Specification باید Test Caseهای حداقلی زیر را تعریف کند:

- دسترسی مجاز؛
- دسترسی غیرمجاز؛
- تغییر ID؛
- تغییر Company؛
- دسترسی منقضی‌شده؛
- Delegation لغوشده؛
- Export غیرمجاز؛
- Attachment غیرمجاز؛
- Search leakage؛
- Count leakage؛
- RPC مستقیم برخلاف UI؛
- Import یا Server Action برخلاف Rule.

---

# بخش ۱۵ — قواعد UI/UX Documentation

هر صفحه و Component باید:

- فارسی و RTL واقعی باشد؛
- معادل انگلیسی اصطلاحات فنی را فقط در صورت نیاز ثبت کند؛
- متن کاربردی کمتر از ۱۲ پیکسل نداشته باشد؛
- Stateهای Loading، Empty، Error، Forbidden، Unavailable و Ready داشته باشد؛
- Keyboard و Screen Reader را در نظر بگیرد؛
- Focus behavior مشخص داشته باشد؛
- Scroll Contract مشخص داشته باشد؛
- Mobile behavior مشخص داشته باشد؛
- اطلاعات محرمانه را در Empty/Error State نشت ندهد؛
- Action اصلی و ثانویه واضح داشته باشد؛
- از Placeholder به‌عنوان Label اصلی استفاده نکند؛
- خطا را نزدیک فیلد یا Operation نمایش دهد؛
- رفتار Back، Refresh و Deep Link را تعریف کند.

## Overlay

برای Modal، Drawer، Picker، Context Menu و Popover باید تعیین شود:

- Parent Overlay؛
- Layering؛
- Focus Trap؛
- Focus Restore؛
- Escape behavior؛
- Outside Click؛
- Scroll Lock؛
- Route Change behavior؛
- Viewport positioning؛
- Mobile adaptation.

## Scroll

- Routeهای عادی Scroll بومی مرورگر دارند.
- `overflow:hidden` سراسری ممنوع است.
- صفحات خاص مانند Conversation می‌توانند Scroll داخلی تعریف کنند.
- Header/Footer ثابت نباید محتوای قابل دسترسی را بپوشاند.
- `min-height:0` در Flex/Grid chainهای Scroll داخلی باید در قرارداد ذکر شود.

## داده نمونه

- داده نمونه فقط برای توضیح UI است.
- داده نمونه نباید Requirement یا Permission جدید ایجاد کند.
- نام، مقدار و تعداد نمونه نباید به‌عنوان محدودیت واقعی سامانه ثبت شود.
- Mock behavior باید از Production contract تفکیک شود.

---

# بخش ۱۶ — قواعد گزارش کار

هر مستند مرتبط با Work Report باید تصمیم‌های قطعی زیر را حفظ کند:

- مبنای گزارش `Shift Occurrence` واقعی است.
- شیفت عبوری از نیمه‌شب یک گزارش واحد دارد.
- هر شخص در هر Shift Occurrence حداکثر یک گزارش دارد.
- چند Assignment در همان شیفت، Sectionهای یک گزارش ترکیبی هستند.
- Applicability می‌تواند `Required`، `Optional` یا `Disabled` باشد.
- `Disabled` یعنی Form، Draft و Reminder شخصی ایجاد نمی‌شود.
- مدیر بدون گزارش شخصی می‌تواند در صورت Scope، فقط فهرست گزارش دیگران را ببیند.
- دسترسی به گزارش فقط بر پایه زیردستی نیست.
- مسئول کنترل عملکرد یا ممیز می‌تواند Access Grant مستقل داشته باشد.
- Section-level Security باید قابل تعریف باشد.
- Reviewer و Confidentiality هر Section باید بررسی شود.
- فایل و Evidence در v8 از زیرساخت فعلی استفاده می‌کنند؛ بازطراحی Document Infrastructure خارج از Scope v8 است.

هیچ سندی نباید گزارش را دوباره بر پایه روز تقویمی تعریف کند مگر برای Display Label و با حفظ Shift Occurrence به‌عنوان واحد یکتا.

---

# بخش ۱۷ — قواعد Notification و Conversation

- Odoo Mail/Discuss/Bus زیرساخت پایه است.
- CAS نباید سیستم اعلان یا Message موازی از صفر بسازد مگر Gap Analysis ضرورت را اثبات کند.
- Notification Center می‌تواند UI مستقل داشته باشد، اما مالک رکوردهای کسب‌وکاری منبع نیست.
- Notification با Action یکسان نیست.
- Read/Unread اعلان با انجام Action یکسان نیست.
- Conversation و Message متعلق به Odoo Mail/Discuss هستند.
- هر Extension باید با Odoo 19 Community تطبیق داده شود.
- نبود Bus باید Fallback کنترل‌شده داشته باشد.

## Gap Analysis پیش از Extension

پیش از پیشنهاد هر Extension باید ثبت شود:

1. قابلیت استاندارد Odoo چیست؟
2. چه Gap واقعی وجود دارد؟
3. آیا Configuration یا Adapter Gap را حل می‌کند؟
4. آیا Extension کم‌خطرتر ممکن است؟
5. Upgrade Risk چیست؟
6. Fallback چیست؟
7. تست سازگاری نسخه بعد چیست؟

---

# بخش ۱۸ — قواعد نسخه‌بندی و Iteration

خط رسمی نسخه‌بندی:

```text
CAS UI Prototype v4 → CAS UI Workspace v7 → CAS UI Workspace v8
```

- نسخه‌های ۵ و ۶ Release رسمی نیستند.
- نسخه ۷ Historical Baseline است.
- نسخه ۸ شامل تصمیم‌های تأییدشده تا Iteration 12 است.
- Iteration به‌تنهایی Release مستقل نیست مگر در Version History ثبت شود.
- افزودن Iteration جدید باید در Baseline، Version History، Change Set، READMEهای Index و Traceability ثبت شود.
- Agent حق ندارد فقط عدد Iteration را در یک فایل تغییر دهد.

## Supersede

هنگام جایگزینی تصمیم یا سند:

1. سند جدید ایجاد یا اصلاح شود.
2. سند قبلی حذف نشود.
3. Status قبلی تغییر کند.
4. `superseded_by` ثبت شود.
5. سند جدید `supersedes` را ثبت کند.
6. Historical Register اصلاح شود.
7. لینک‌ها و Indexها اصلاح شوند.
8. اثر در Change Set ثبت شود.

## شماره نسخه سند

- اصلاح نگارشی بدون تغییر معنا: Patch.
- افزودن جزئیات سازگار: Minor.
- تغییر رفتار، مالکیت یا Contract: Major.
- افزایش نسخه سند باید در Metadata و Change Set قابل توضیح باشد.

---

# بخش ۱۹ — قواعد Open Questions

یک سؤال فقط زمانی در `Open_Questions.md` ثبت شود که:

- پاسخ آن واقعاً تأیید نشده باشد؛
- روی اجرا یا معماری اثر داشته باشد؛
- پاسخ از اسناد موجود قابل استخراج نباشد.

هر Open Question باید شامل این موارد باشد:

- شناسه؛
- سؤال دقیق؛
- زمینه؛
- اثر تصمیم؛
- گزینه‌های شناخته‌شده؛
- پیشنهاد فعلی؛
- تصمیم‌گیرنده؛
- Deadline یا مرحله نیاز؛
- اسناد متأثر؛
- وضعیت.

عبارت‌های مبهم مانند «بعداً بررسی شود» بدون Context ممنوع است.

وقتی سؤال پاسخ داده شد:

- از فایل حذف نشود؛
- Status آن `Resolved` شود؛
- پاسخ و سند تصمیم مرجع ثبت شود؛
- اسناد متأثر اصلاح شوند.

---

# بخش ۲۰ — قواعد Traceability

هر تغییر معنادار باید زنجیره زیر را کامل کند:

```text
نیاز / مسئله
→ Product Decision
→ Page Specification
→ Decision Record
→ Domain Owner
→ Module Specification
→ Architecture Contract
→ Security Contract
→ Migration
→ Test Strategy
→ Implementation
→ Verification
```

Agent باید بعد از هر تغییر بررسی کند:

- آیا Traceability Matrix نیاز به ردیف جدید دارد؟
- آیا ردیف موجود باید Status جدید بگیرد؟
- آیا Decision به Page و Module لینک دارد؟
- آیا Module به Architecture و Security لینک دارد؟
- آیا Change Set همه اسناد را پوشش می‌دهد؟
- آیا سند Historical به جای سند فعال لینک نشده است؟

هیچ فایل جدیدی بدون ورود مناسب به Index یا Traceability رها نشود.

## حداقل ستون‌های ردیابی

هر ردیف باید در حد موضوع خود این اطلاعات را قابل بازیابی کند:

- Requirement یا موضوع؛
- Decision؛
- Page؛
- Module Owner؛
- Architecture؛
- Security؛
- Change Set؛
- Status؛
- Open Question؛
- Implementation Reference در آینده؛
- Verification Reference در آینده.

---

# بخش ۲۱ — قواعد Change Set

هر تغییر چندفایلی یا تغییر Baseline باید Change Set داشته باشد.

Change Set باید شامل:

- شناسه؛
- Baseline مبدأ؛
- Baseline مقصد؛
- هدف؛
- دامنه؛
- تصمیم‌های جدید؛
- تصمیم‌های حفظ‌شده؛
- تصمیم‌های Superseded؛
- صفحات متأثر؛
- ماژول‌های متأثر؛
- Architectureهای متأثر؛
- Security Impact؛
- Data/Migration Impact؛
- Test/Regression Impact؛
- Out of Scope؛
- شرط Completion؛
- فهرست دقیق فایل‌ها.

---

# بخش ۲۲ — ثبت اطلاعات نامطمئن

Agent نباید حدس را به‌عنوان تصمیم قطعی ثبت کند.

برای هر مورد نامطمئن باید یکی از این رفتارها را انتخاب کند:

1. از اسناد بالادستی استخراج کند.
2. در Open Questions ثبت کند.
3. با برچسب `Proposed` یا `Needs Review` ثبت کند.
4. در صورت نیاز از مالک پروژه سؤال کند.

## تفاوت واژگان

- **Agreed:** تأییدشده.
- **Proposed:** پیشنهاد مشخص اما تأییدنشده.
- **Needs Review:** سند ناقص یا نیازمند بررسی تخصصی.
- **Assumption:** فرض موقت؛ نباید مبنای Implementation Ready باشد.
- **Example:** نمونه توضیحی؛ Contract نیست.
- **Conceptual:** مدل مفهومی؛ نام نهایی API یا Model نیست.

هر مثال JSON، Model یا API باید مشخص کند Conceptual است یا Final Contract.

## اصل عدم اختراع جزئیات

Agent نباید نام Model، Field، Method، API یا Route نهایی را بدون منبع یا تصمیم معتبر قطعی جلوه دهد. نام پیشنهادی باید با `proposed` یا توضیح صریح مشخص شود.

---

# بخش ۲۳ — قواعد زبان و نگارش

- زبان اصلی مستندات فارسی است.
- نام فنی Model، Module، Capability، Route و Field به انگلیسی و داخل Backtick نوشته شود.
- اصطلاحات رسمی باید مطابق `01_Product/Terminology.md` باشند.
- یک مفهوم نباید در اسناد مختلف چند نام فارسی متعارض داشته باشد.
- جملات باید صریح، آزمون‌پذیر و بدون ابهام باشند.
- از «احتمالاً»، «شاید»، «معمولاً» و «بهتر است» در Requirement قطعی استفاده نشود.
- Requirement قطعی با «باید» و ممنوعیت با «نباید» نوشته شود.
- پیشنهاد تأییدنشده صریحاً با «پیشنهاد» مشخص شود.
- از عبارت «و غیره» برای فهرست‌های الزامی استفاده نشود.
- عنوان‌ها سلسله‌مراتب منطقی داشته باشند.
- جدول برای Metadata، Ownership، Matrix و Comparison استفاده شود.
- Code Block فقط برای Schema، Flow، Contract یا نمونه ساختاری استفاده شود.
- لینک‌ها Relative باشند مگر منبع خارجی ضروری باشد.
- هیچ سندی نباید به چت خصوصی به‌عنوان تنها مرجع وابسته باشد؛ تصمیم چت باید به سند منتقل شود.
- تاریخ‌ها باید مطلق باشند، نه «امروز»، «فردا» یا «هفته قبل».
- هر Acronym در نخستین استفاده تعریف شود.

---

# بخش ۲۴ — قواعد لینک و Index

پس از ایجاد یا تغییر سند، Agent باید این موارد را بررسی کند:

- README پوشه مربوط؛
- README اصلی `specs` در صورت تغییر Baseline یا ساختار؛
- Traceability Matrix؛
- Decision Index؛
- Architecture Index؛
- Module Index؛
- UI/UX Index؛
- Change Set Index؛
- Historical Register؛
- لینک رفت و برگشت میان اسناد.

## ممنوعیت‌ها

- فایل یتیم بدون لینک ورودی ممنوع است.
- لینک به مسیر فرضی ممنوع است.
- تغییر نام فایل بدون اصلاح تمام لینک‌ها ممنوع است.
- جابه‌جایی Historical Doc بدون بررسی Broken Link ممنوع است.
- لینک به Branch موقت در متن مرجع دائمی ممنوع است.

---

# بخش ۲۵ — کنترل تکرار و هم‌پوشانی

پیش از ایجاد فایل جدید، Agent باید پاسخ دهد:

1. آیا سند مشابهی وجود دارد؟
2. آیا باید همان سند اصلاح شود؟
3. آیا موضوع Decision است یا Specification؟
4. آیا موضوع معماری مشترک است یا جزئیات ماژول؟
5. آیا فایل جدید باعث دو Source of Truth می‌شود؟
6. آیا محتوای مشترک باید Extract شود؟

اگر دو سند محتوای مشابه دارند:

- یکی باید مرجع اصلی باشد؛
- دیگری باید Summary و لینک باشد؛
- Ruleها نباید Copy/Paste مستقل شوند؛
- تغییر آینده نباید نیازمند ویرایش چند نسخه متنی یک Rule باشد.

---

# بخش ۲۶ — مقایسه مستندات با کد

مقایسه با کد فقط زمانی انجام می‌شود که کاربر یا مرحله پروژه صریحاً آن را درخواست کرده باشد.

هنگام مقایسه:

- Specification فعال مرجع رفتار مطلوب است.
- کد مرجع وضعیت موجود است.
- خروجی باید Gap Matrix باشد.
- نبود قابلیت در کد، دلیل حذف آن از Specification نیست.
- رفتار اضافه در کد باید به‌عنوان Undocumented Behavior ثبت شود.
- تغییر کد بدون Specification یا Change Set نباید مستقیم پیشنهاد شود.
- Gapها باید Priority، Risk، Dependency و Migration داشته باشند.

## حداقل ستون‌های Gap Matrix

- Requirement؛
- سند مرجع؛
- وضعیت کد؛
- نوع Gap؛
- ماژول مالک؛
- Severity؛
- Dependency؛
- Migration؛
- Test موردنیاز؛
- پیشنهاد اصلاح.

---

# بخش ۲۷ — فرآیند گام‌به‌گام هر به‌روزرسانی

هر Agent موظف است دقیقاً این فرآیند را اجرا کند:

## مرحله A — فهم درخواست

1. درخواست کاربر را به Requirementهای مشخص تبدیل کن.
2. محدوده داخل و خارج را تعیین کن.
3. مشخص کن آیا تصمیم قطعی است یا پیشنهاد.
4. مشخص کن آیا پاسخ قبلاً در اسناد وجود دارد.
5. از تکرار سؤال پاسخ‌داده‌شده خودداری کن.

## مرحله B — مطالعه

1. اسناد اجباری را بخوان.
2. تمام اسناد مرتبط را پیدا کن.
3. Baseline و Status را تشخیص بده.
4. Historicalها را از Activeها جدا کن.
5. تعارض‌ها را فهرست کن.

## مرحله C — طراحی تغییر مستندی

1. فایل‌های لازم برای ایجاد را تعیین کن.
2. فایل‌های لازم برای اصلاح را تعیین کن.
3. Decision لازم را تعیین کن.
4. Architecture و Security Impact را تعیین کن.
5. Traceability و Change Set را تعیین کن.
6. مشخص کن چه چیزهایی Open Question باقی می‌مانند.

## مرحله D — نوشتن

1. Metadata را کامل کن.
2. واژگان رسمی را رعایت کن.
3. Ruleها را آزمون‌پذیر بنویس.
4. Ownership را صریح بنویس.
5. Failure Stateها را بنویس.
6. Security را بنویس.
7. Acceptance Criteria را بنویس.
8. Out of Scope را بنویس.
9. لینک‌های مرتبط را اضافه کن.

## مرحله E — هماهنگ‌سازی

1. Indexها را اصلاح کن.
2. Traceability را اصلاح کن.
3. Change Set را اصلاح کن.
4. Historical Register را اصلاح کن.
5. Open Questions را اصلاح کن.
6. Module Aggregation Matrix را اصلاح کن.
7. تمام ارجاعات نسخه را یکسان کن.

## مرحله F — اعتبارسنجی

1. لینک‌های Relative را بررسی کن.
2. شناسه‌های تکراری را بررسی کن.
3. Statusها را بررسی کن.
4. فایل‌های یتیم را بررسی کن.
5. اصطلاحات متعارض را بررسی کن.
6. مالکیت دوگانه را بررسی کن.
7. Capabilityهای بدون تعریف را بررسی کن.
8. Routeهای منسوخ را بررسی کن.
9. Decisionهای بدون Index را بررسی کن.
10. `Implementation Ready`های بدون Security/Migration/Test را بررسی کن.
11. تعارض با Baseline را بررسی کن.
12. Diff را بررسی کن تا فقط فایل‌های موردنظر تغییر کرده باشند.
13. متن را برای عبارت‌های مبهم جست‌وجو کن.
14. نمونه‌ها را از Contractهای قطعی تفکیک کن.
15. بررسی کن هیچ Requirement فقط در PR Body باقی نمانده باشد.

## مرحله G — تحویل

گزارش نهایی باید شامل این موارد باشد:

- خلاصه تغییر؛
- Branch؛
- فایل‌های ایجادشده؛
- فایل‌های اصلاح‌شده؛
- Decisionهای ثبت‌شده؛
- Open Questionهای باقی‌مانده؛
- Validation انجام‌شده؛
- موارد خارج از Scope؛
- اینکه آیا `main` تغییر کرده است یا خیر؛
- لینک PR یا Commit؛
- وضعیت Merge.

---

# بخش ۲۸ — Checklist اجباری قبل از Commit

Agent باید قبل از Commit تمام موارد زیر را بررسی کند:

## Baseline

- [ ] نسخه فعال صحیح است.
- [ ] Iteration صحیح است.
- [ ] قابلیت تأییدشده v8 حذف یا تضعیف نشده است.
- [ ] Historical Doc به‌عنوان Active استفاده نشده است.

## ساختار

- [ ] فایل در پوشه درست قرار دارد.
- [ ] نام فایل مطابق Convention است.
- [ ] Metadata کامل است.
- [ ] Status صحیح است.
- [ ] شناسه یکتا است.

## محتوا

- [ ] هدف روشن است.
- [ ] Scope روشن است.
- [ ] Out of Scope روشن است.
- [ ] مالک دامنه روشن است.
- [ ] Source of Truth روشن است.
- [ ] Lifecycle روشن است.
- [ ] Stateها روشن‌اند.
- [ ] Validation روشن است.
- [ ] Failure Modeها روشن‌اند.
- [ ] Acceptance Criteria قابل تست است.

## امنیت

- [ ] Capability مشخص است.
- [ ] ACL مشخص است.
- [ ] Record Rule مشخص است.
- [ ] Method Check مشخص است.
- [ ] Company Scope مشخص است.
- [ ] Delegation مشخص است.
- [ ] ID Tampering بررسی شده است.
- [ ] Export و Attachment بررسی شده‌اند.
- [ ] Audit بررسی شده است.
- [ ] `sudo()` برای عبور از Permission پیشنهاد نشده است.

## Integration

- [ ] Provider Owner مشخص است.
- [ ] Query/Command مرزبندی شده است.
- [ ] Optional Dependency behavior مشخص است.
- [ ] Partial Failure مشخص است.
- [ ] Deep Link مشخص است.
- [ ] Event/Notification behavior مشخص است.

## UI/UX

- [ ] RTL بررسی شده است.
- [ ] Responsive بررسی شده است.
- [ ] Accessibility بررسی شده است.
- [ ] Keyboard بررسی شده است.
- [ ] Loading/Empty/Error/Forbidden/Unavailable ثبت شده‌اند.
- [ ] Focus/Overlay/Scroll ثبت شده‌اند.

## ردیابی

- [ ] README پوشه اصلاح شده است.
- [ ] Traceability Matrix اصلاح شده است.
- [ ] Decision Index اصلاح شده است.
- [ ] Module Matrix اصلاح شده است.
- [ ] Change Set اصلاح شده است.
- [ ] Open Questions اصلاح شده است.
- [ ] Historical Register در صورت نیاز اصلاح شده است.
- [ ] لینک‌های رفت و برگشت وجود دارند.

## آماده‌سازی اجرا

- [ ] API مشخص است.
- [ ] Security مشخص است.
- [ ] Migration مشخص است.
- [ ] Test Strategy مشخص است.
- [ ] Performance مشخص است.
- [ ] Observability مشخص است.
- [ ] هیچ سؤال بحرانی باز باقی نمانده است.

فقط پس از تکمیل تمام موارد مرتبط، Commit مجاز است.

---

# بخش ۲۹ — Checklist اجباری قبل از اعلام `Implementation Ready`

- [ ] Product behavior `Agreed` است.
- [ ] Decisionهای مشترک `Agreed` هستند.
- [ ] Domain Owner قطعی است.
- [ ] Module Boundary قطعی است.
- [ ] Entity و Lifecycle کامل است.
- [ ] API/Provider Contract کامل است.
- [ ] Error Contract کامل است.
- [ ] Security کامل است.
- [ ] Multi-company کامل است.
- [ ] Migration و Rollback کامل است.
- [ ] Performance و Index Strategy کامل است.
- [ ] Observability کامل است.
- [ ] Unit Test Strategy کامل است.
- [ ] Integration Test Strategy کامل است.
- [ ] Security Test Strategy کامل است.
- [ ] UI Acceptance Criteria کامل است.
- [ ] Regression Scope کامل است.
- [ ] Traceability کامل است.
- [ ] Open Question بحرانی وجود ندارد.
- [ ] هیچ تعارضی با Baseline وجود ندارد.

Agent حق ندارد برای سریع‌ترشدن پروژه، Status را زودتر از تکمیل این شروط ارتقا دهد.

---

# بخش ۳۰ — خطاهای رایج و رفتار ممنوع

موارد زیر ممنوع‌اند:

- ویرایش فقط یک فایل بدون بررسی اثر زنجیره‌ای؛
- ثبت تصمیم فقط در توضیح PR؛
- ساخت فایل موازی برای موضوع موجود؛
- حذف Historical Doc؛
- تغییر شماره Decision بدون بررسی؛
- اعلام `Final` به‌جای Status رسمی؛
- مالک‌کردن Workspace روی داده کسب‌وکاری؛
- تعریف Permission صرفاً در Frontend؛
- استفاده از `sudo()` به‌عنوان راه‌حل عمومی؛
- فرض اینکه Manager همیشه Subordinate دارد؛
- فرض اینکه دسترسی گزارش فقط سلسله‌مراتبی است؛
- تقسیم شیفت شب به دو گزارش روزانه؛
- ساخت چند گزارش برای چند Assignment در یک شیفت برخلاف تصمیم Composite؛
- ساخت Notification یا Message Model موازی بدون Gap Analysis؛
- تغییر زیرساخت فایل در Scope v8؛
- تغییر Odoo Core؛
- ثبت API نمونه به‌عنوان API نهایی بدون Status؛
- ثبت کد یا مدل فرضی بدون علامت Conceptual؛
- استفاده از عبارت‌های مبهم و غیرقابل تست؛
- باقی‌گذاشتن لینک شکسته؛
- ایجاد فایل یتیم؛
- تغییر `main` بدون مجوز صریح؛
- Push مستقیم بدون Branch و Review در کارهای مستندی گسترده؛
- ادعای Validationی که واقعاً انجام نشده است؛
- اعلام «تمام مستندات کامل شد» بدون Diff Review و بررسی Indexها.

---

# بخش ۳۱ — ساختار پوشه

- `00_Project`: Baseline، حاکمیت، نسخه‌ها، Traceability، Historical Register و Open Questions
- `01_Product`: Vision، اصول محصول، UX و واژگان
- `02_UI_UX`: Page Specification، Role View، Shell و Admin Center
- `03_Modules`: Ownership، Dependency، Provider، Specification، Security، Migration و Test Strategy
- `04_Decisions`: Decision Recordهای مشترک
- `05_Architecture`: System Context، Domain، Data Flow، Integration، Security و معماری تخصصی
- `06_ChangeSets`: بسته‌های تغییر و مسیر انتقال نسخه‌ها

---

# بخش ۳۲ — چرخه رسمی تصمیم تا اجرا

```text
نیاز
→ تحلیل محصول
→ Page Specification
→ Decision Record
→ Domain Ownership
→ Architecture Contract
→ Module Specification
→ Security
→ Migration
→ Test Strategy
→ Implementation Ready
→ پیاده‌سازی
→ Verification
→ Verified
```

هیچ مرحله‌ای نباید بدون ثبت مستند مرحله قبل دور زده شود.

---

# بخش ۳۳ — قواعد Branch، Commit و Pull Request

## Branch

- برای تغییر گسترده، Branch جدا الزامی است.
- نام Branch باید دامنه تغییر را نشان دهد.
- `main` بدون مجوز صریح کاربر تغییر نمی‌کند.
- Branch باید از Baseline درست ساخته شود.

## Commit

- Commit باید Scope روشن داشته باشد.
- فایل نامرتبط نباید وارد Commit شود.
- پیام Commit باید نوع و هدف را نشان دهد.
- در ابزارهایی که هر فایل Commit جدا می‌سازند، PR باید برای Squash Merge مناسب باشد.

## Pull Request

PR مستندی باید شامل:

- هدف؛
- Baseline؛
- فایل‌های اصلی؛
- تصمیم‌های ثبت‌شده؛
- اثر محصولی؛
- اثر معماری؛
- اثر امنیتی؛
- Validation؛
- Out of Scope؛
- Open Questions؛
- وضعیت Draft یا Ready.

PR Body جایگزین ثبت تصمیم داخل `specs` نیست.

---

# بخش ۳۴ — وضعیت فعلی و نقطه شروع

Baseline محصولی نسخه ۸ تا Iteration 12 تجمیع شده است.

هر Agent جدید باید کار خود را از این زنجیره آغاز کند:

1. `specs/README.md`
2. `00_Project/V8_Canonical_Baseline.md`
3. `00_Project/Documentation_Governance.md`
4. `00_Project/Traceability_Matrix.md`
5. `01_Product/Terminology.md`
6. `03_Modules/V8_Module_Ownership_Map.md`
7. `05_Architecture/Module_Boundaries.md`
8. `05_Architecture/Capability_And_Security_Model.md`
9. اسناد تخصصی موضوع درخواست

این مجموعه مرجع طراحی ماژول‌های آینده است. هر ماژول فقط پس از تکمیل API، Security، Migration، Performance، Observability و Test Strategy خود می‌تواند به وضعیت `Implementation Ready` برسد.

---

# فرمان عملیاتی نهایی برای Agentها

هنگامی که کاربر می‌گوید «مستندات را به‌روز کن»، این عبارت به‌معنی ویرایش سریع یک فایل نیست. Agent باید:

1. این README را کامل بخواند.
2. Baseline و اسناد بالادستی را بخواند.
3. تمام اسناد مرتبط را پیدا کند.
4. تعارض و تکرار را بررسی کند.
5. اثر محصولی، صفحه‌ای، ماژولی، معماری، امنیتی، Migration و Test را تحلیل کند.
6. تمام فایل‌های لازم را هماهنگ و هم‌زمان اصلاح کند.
7. Traceability، Index، Change Set و Historical Status را به‌روز کند.
8. Checklistهای این فایل را اجرا کند.
9. تغییرات را در Branch جدا و قابل بازبینی ثبت کند، مگر کاربر صریحاً روش دیگری تعیین کند.
10. هیچ تغییر مستقیمی در `main` ایجاد نکند مگر با مجوز صریح.
11. گزارش نهایی دقیق و قابل ممیزی ارائه دهد.
12. هر موردی را که واقعاً بررسی نشده، صادقانه به‌عنوان بررسی‌نشده اعلام کند.

هر خروجی کمتر از این استاندارد، به‌روزرسانی کامل مستندات محسوب نمی‌شود.