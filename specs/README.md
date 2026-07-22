# CAS Specifications — Mandatory Entry Point

> **Status:** `Canonical / Mandatory`  
> **Scope:** تمام فایل‌ها و تغییرات داخل `specs/`  
> **Audience:** انسان، توسعه‌دهنده، تحلیل‌گر، طراح، بازبین و هر AI Agent  
> **Active UI review baseline:** `CAS UI Review Cycle 10 — Through Iteration 13`

## چرا این پوشه وجود دارد؟

`specs/` حافظه مهندسی CAS است. هدف آن زیادکردن تعداد فایل‌ها نیست؛ هدف آن کاهش زمان فهم، جلوگیری از تکرار تصمیم‌ها، مشخص‌کردن حقیقت جاری و تبدیل بازخورد UI به تغییر قابل‌پیاده‌سازی و قابل‌اعتبارسنجی است.

> **اصل حاکم:** هر تغییر مستندی فقط زمانی ارزشمند است که هزینه فهم پروژه را کاهش دهد. اگر تغییری باعث ابهام، تکرار، شلوغی یا سخت‌ترشدن ناوبری شود، باید بازطراحی یا رد شود؛ حتی اگر محتوای آن به‌تنهایی صحیح باشد.

---

## 1. قبل از هر کار چه بخوانم؟

هر انسان یا AI Agent پیش از ایجاد، ویرایش، حذف، انتقال، Commit، Push یا Merge در `specs/` باید این مسیر را طی کند:

1. همین فایل؛
2. [نقشه مرکزی مستندات](00_Project/Documentation_Map.md)؛
3. Registry مرتبط با موضوع؛
4. Specificationها و Decisionهای Canonical مرتبط؛
5. در صورت تغییر مستندات، [راهنمای مشارکت](00_Project/Documentation_Contribution_Guide.md).

برای کارهای پیچیده یا چندماژولی، این اسناد نیز اجباری‌اند:

- [Documentation Governance](00_Project/Documentation_Governance.md)
- [AI Working Guide](00_Project/AI_Working_Guide.md)
- [Documentation Lifecycle](00_Project/Documentation_Lifecycle.md)
- [Review Process Guide](00_Project/Review_Process_Guide.md)
- [Cycle Closeout Checklist](00_Project/Cycle_Closeout_Checklist.md)
- [Metadata and ID Standard](00_Project/Metadata_And_ID_Standard.md)

**خواندن فقط فایل هدف کافی نیست.** موضوع باید در Registryها، تصمیم‌های فعال، ماژول‌ها، صفحات و Change Setهای مرتبط ردیابی شود.

---

## 2. نقشه حقیقت پروژه

ساختار مرجع CAS چهار لایه دارد:

```text
specs/README.md
    ↓
Documentation Map
    ↓
Central Registries
    ↓
Canonical Decisions, Specifications and Contracts
```

### `README`

فقط نقطه ورود، قواعد طلایی و مسیر مطالعه است.

### `Documentation Map`

GPS مستندات است و می‌گوید پاسخ هر نوع سؤال در کدام مرجع قرار دارد.

### Registryها

برای پیدا کردن وضعیت، مالک، ارتباط و مرجع Canonical استفاده می‌شوند. Registry جای Specification را نمی‌گیرد.

### Canonical Documents

Decision، Module Specification، Page Specification، Architecture/Security Contract و Change Set فعال، مرجع محتوایی حقیقت هستند.

### Historical Evidence

Review Cycleها، Iterationها، Screenshotها، Prototypeها و اسناد Superseded برای حفظ تاریخچه و شواهد نگه‌داری می‌شوند؛ ولی به‌تنهایی مرجع تصمیم جاری نیستند.

---

## 3. از کدام Registry استفاده کنم؟

| نیاز | مرجع |
|---|---|
| تصمیم جاری یا Superseded | [Decision Registry](00_Project/Decision_Registry.md) |
| Capability و مالک آن | [Capability Registry](00_Project/Capability_Registry.md) |
| صفحه، Route و ارتباطات | [Page Registry](00_Project/Page_Registry.md) |
| دسترسی نقش‌ها به صفحات | [Role-to-Page Matrix](00_Project/Role_To_Page_Matrix.md) |
| مالک ماژول و داده | [Module Registry](00_Project/Module_Registry.md) |
| تفاوت مستندات و پیاده‌سازی | [Implementation Gap Registry](00_Project/Implementation_Gap_Registry.md) |
| سؤال، تعارض، ریسک یا مورد Deferred | [Open Item Registry](00_Project/Open_Item_Registry.md) |
| زنجیره Observation تا Revalidation | [Traceability Matrix](00_Project/Traceability_Matrix.md) |
| وضعیت اسناد قدیمی | [Historical Document Register](00_Project/Historical_Document_Register.md) |

Registryها Index هستند. متن کامل الزام باید در سند Canonical مرتبط قرار گیرد.

---

## 4. قواعد طلایی

1. **هدف مستندسازی، بهبود عملکرد است؛ نه تولید فایل.**
2. **یک مفهوم، یک مرجع Canonical دارد.** از ساخت سند موازی جلوگیری شود.
3. **اطلاعات تفصیلی در README یا Registry کپی نمی‌شود.** فقط خلاصه و لینک ثبت می‌شود.
4. **تصمیم فقط در چت، Commit message، Prototype یا Screenshot باقی نمی‌ماند.**
5. **کد فعلی حقیقت محصول نیست.** اختلاف کد با Specification فعال، `Implementation Gap` است.
6. **Cycle جدید تصمیم‌های گذشته را خودکار باطل نمی‌کند.** فقط `Supersedes` صریح معتبر است.
7. **وضعیت سند، وضعیت اجرا و وضعیت UI Validation مستقل‌اند.**
8. **مالک Domain، داده و Capability از روی حدس تعیین نمی‌شود.**
9. **هر تغییر Cross-layer باید اثر UI، Backend، Security، Migration، Test، Audit و Revalidation را بررسی کند.**
10. **هر فایل جدید باید در همان Change Set به مسیر ناوبری و Registryهای لازم متصل شود.**
11. **اسناد Historical حذف نمی‌شوند؛ به‌درستی طبقه‌بندی می‌شوند.**
12. **اگر سندی پیدا کردن حقیقت را سخت‌تر کند، باید ادغام، کوتاه یا بازطراحی شود.**

---

## 5. مرجع مؤثر برای پیاده‌سازی

Backend یا UI نباید فقط از روی آخرین ZIP، آخرین Cycle یا یک سند منفرد پیاده‌سازی شود.

```text
Effective Specification
=
Active / Agreed Decisions
+ Active Module Specifications
+ Active Page Specifications
+ Active Architecture and Security Contracts
+ Approved Change Sets
- Superseded Requirements
- Historical-only Statements
```

در تعارض، ترتیب مرجعیت چنین است:

1. تصمیم صریح و جدید مالک محصول؛
2. این README و قواعد Governance؛
3. Decisionهای Active و Supersede Records؛
4. Architecture و Security Contracts؛
5. Module Specifications؛
6. Page Specifications؛
7. Change Sets و Acceptance Criteria؛
8. Traceability و Impact Matrices؛
9. UI Observations و Review Evidence؛
10. Prototype، Screenshot و Mock Data؛
11. کد فعلی؛
12. گفتگو و حافظه اشخاص.

---

## 6. تفاوت نسخه‌ها

این چهار مفهوم نباید با هم مخلوط شوند:

- **UI Review Cycle:** یک چرخه بازنگری کلی رابط کاربری؛
- **Iteration:** اصلاح داخلی داخل همان Cycle؛
- **Document Version:** نسخه یک سند مشخص؛
- **Software Release:** نسخه واقعی نرم‌افزار.

برای مثال، `UI Review Cycle 10` به معنی `CAS Software 10` نیست.

جزئیات چرخه‌ها در [UI Review Lifecycle](00_Project/UI_Review_Lifecycle.md) و [Version History](00_Project/Version_History.md) نگه‌داری می‌شود.

---

## 7. وضعیت‌های رسمی

### Document Status

`Draft` · `Under Review` · `Agreed` · `Active` · `Superseded` · `Historical` · `Rejected` · `Archived`

### Implementation Status

`Not Assessed` · `Gap Identified` · `Planned` · `In Development` · `Implemented` · `Partially Implemented` · `Blocked` · `Deprecated`

### UI Validation Status

`Not Validated` · `Pending Revalidation` · `Validated` · `Accepted` · `Reopened` · `Failed Validation`

تعریف و کاربرد دقیق این وضعیت‌ها در [Metadata and ID Standard](00_Project/Metadata_And_ID_Standard.md) قرار دارد.

---

## 8. پروتکل تغییر مستندات

پیش از نگارش:

1. مسئله یا تغییر را در یک جمله دقیق تعریف کن؛
2. در Documentation Map و Registryها جست‌وجو کن؛
3. مرجع Canonical موجود را پیدا کن؛
4. تصمیم‌های Active، Superseded و موارد باز را تفکیک کن؛
5. Domain Owner و اثرهای Cross-layer را مشخص کن؛
6. تصمیم بگیر سند موجود باید اصلاح شود یا سند جدید واقعاً لازم است؛
7. فقط پس از این مراحل نگارش را آغاز کن.

هنگام ثبت تغییر:

```text
Observation / Need
→ Decision or Clarification
→ Page and Module Impact
→ Backend / Security Requirement
→ Change Set
→ Implementation Status
→ UI Revalidation
→ Accepted or Reopened
```

پس از تغییر:

- Metadata و لینک‌های دوطرفه را اصلاح کن؛
- Registryهای مرتبط را به‌روزرسانی کن؛
- Traceability را حفظ کن؛
- Broken link و تعارض ایجاد نکن؛
- از [Cycle Closeout Checklist](00_Project/Cycle_Closeout_Checklist.md) استفاده کن.

---

## 9. قواعد ویژه AI Agent

هر AI Agent باید:

- قبل از پاسخ یا تغییر، منبع Canonical را پیدا کند؛
- بین «آنچه تصمیم گرفته شده»، «آنچه اجرا شده» و «آنچه فقط در UI دیده شده» تفکیک کند؛
- نبود اطلاعات را با حدس پر نکند؛
- تصمیم جدید را به‌عنوان تصمیم قبلی جا نزند؛
- Prototype را Implementation Evidence معرفی نکند؛
- تغییرات را در تمام مراجع وابسته ردیابی کند؛
- در پایان اعلام کند چه چیزی تغییر کرده، چه چیزی تغییر نکرده و چه Gapهایی باقی مانده است.

راهنمای اجرایی کامل: [AI Working Guide](00_Project/AI_Working_Guide.md)

---

## 10. معیار کیفیت یک سند

هر سند باید حداقل یکی از این خروجی‌ها را بهتر کند:

- یافتن حقیقت؛
- تصمیم‌گیری؛
- پیاده‌سازی؛
- Review؛
- تست و پذیرش؛
- انتقال دانش؛
- جلوگیری از دوباره‌کاری.

یک سند ناموفق است اگر:

- همان محتوا را در چند محل تکرار کند؛
- معلوم نباشد مرجع است یا تاریخچه؛
- Owner، Status یا ارتباطات آن مشخص نباشد؛
- برای فهم آن مجبور باشیم فایل‌های نامرتبط زیادی بخوانیم؛
- پس از خواندن، اقدام بعدی روشن نباشد.

**معیار عملی:** یک فرد یا AI آشنا با Repository باید بتواند در کمتر از ده دقیقه مرجع جاری، موارد باز، Gapهای اجرا و مسیر ادامه یک موضوع را پیدا کند.

---

## 11. ایجاد UI Review Cycle جدید

برای Cycle جدید از قالب رسمی استفاده شود:

[`02_UI_UX/Review_Cycles/_Template/`](02_UI_UX/Review_Cycles/_Template/)

Cycle جدید تا زمانی بسته محسوب نمی‌شود که:

- Observationها تعیین تکلیف شده باشند؛
- Decisionها و Impactها ثبت شده باشند؛
- Registryها و Traceability به‌روز باشند؛
- موارد باز به Open Item Registry منتقل شده باشند؛
- Validation Report و Change Summary تکمیل شده باشند؛
- [Cycle Closeout Checklist](00_Project/Cycle_Closeout_Checklist.md) پاس شده باشد.

---

## 12. نقطه شروع بر اساس نوع کار

### طراحی یا Review یک صفحه

`Page Registry` → Page Specification → Role Matrix → Decisionها → Module Impact

### تغییر Backend یا ماژول

`Module Registry` → Module Specification → Decisions → Architecture/Security Contracts → Gaps

### بررسی دسترسی و امنیت

`Capability Registry` → Role Matrix → Security Contract → Module Security → Acceptance Criteria

### پاسخ به سؤال «قبلاً چه تصمیمی گرفتیم؟»

`Decision Registry` → Decision Canonical → Supersedes/Superseded By → Change Set

### ادامه یک مورد ناقص

`Open Item Registry` یا `Implementation Gap Registry` → Source Document → Owner → Next Action

### شروع Cycle جدید

`Review Cycle Template` → UI Review Lifecycle → Review Process Guide → Closeout Checklist

---

## 13. مسئولیت نگهداری

هر تغییر‌دهنده مسئول است که مستندات را **قابل‌استفاده‌تر از قبل** تحویل دهد.

افزودن سند بدون اتصال به نقشه، Registry، Owner، Status و مرجع Canonical ناقص است. اصلاح یک سند بدون بررسی وابستگی‌های آن نیز ناقص است.

این README باید کوتاه، مسیرمحور و قابل‌خواندن باقی بماند. جزئیات تخصصی در اسناد اختصاصی نگه‌داری می‌شود و فقط از اینجا لینک می‌گیرد.
