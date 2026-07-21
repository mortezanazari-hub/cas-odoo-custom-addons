# قرارداد معماری CSS و Design System فضای کار CAS

| مشخصه | مقدار |
|---|---|
| Document ID | `ARCH-CSS-DS-001` |
| Document Type | Architecture Contract |
| Title | Workspace CSS and Design System Contract |
| Status | `Active` |
| Document Version | `1.0` |
| Created At | `2026-07-21` |
| Updated At | `2026-07-21` |
| Owner | Architecture Governance |
| Reviewers | Product Design, Frontend, Odoo Module Owners |
| Source UI Review Cycle | `CAS UI Review Cycle 9` |
| Source Iteration | `Through Iteration 13` |
| Effective From | `2026-07-21` |
| Supersedes | هر الگوی پراکنده یا ضمنی که با این قرارداد تعارض دارد |
| Superseded By | `N/A` |
| Domain Owner | `cas_workspace` for shared UI system; each business module for scoped component styles |
| Affected Modules | تمام Custom Addonهایی که UI، Widget، Form، Dialog، Table، Dashboard یا Workspace surface تولید می‌کنند |
| Implementation Status | `Gap Identified` |
| UI Validation Status | `Pending Revalidation` |
| Related Decisions | `DEC-010-UIR09-CONSOLIDATED` |
| Related Observations | `OBS-UIR09-LAYOUT-001` و Observationهای مرتبط با UI maintainability |
| Related Change Sets | `CS-UIR09-WORKSPACE-UX-CONSOLIDATION` |

## 1. هدف

این قرارداد تضمین می‌کند اصلاحات ظاهری پس از راه‌اندازی، بدون تغییر غیرضروری در Template، JavaScript، Backend یا مدل داده انجام شوند و Styleهای ماژول‌ها با Odoo Core یا یکدیگر تداخل نکنند.

این سند برای تمام UIهای CAS الزام‌آور است و توصیه اختیاری محسوب نمی‌شود.

## 2. اصول قطعی

1. Odoo Core و Assetهای Core مستقیماً ویرایش نمی‌شوند.
2. Workspace مالک Design Tokenها، Primitiveهای مشترک، Layout Shell و Theme contract است.
3. هر Business Module فقط Styleهای Componentها و Stateهای متعلق به Domain خود را نگهداری می‌کند.
4. تغییر رنگ، فاصله، اندازه، Radius، Shadow، Typography و تراکم عادی MUST بدون تغییر Python Model یا Business Workflow قابل انجام باشد.
5. DOM structure فقط زمانی تغییر می‌کند که نیاز محصولی یا Accessibility واقعی وجود داشته باشد؛ CSS polish به‌تنهایی مجوز بازنویسی DOM نیست.

## 3. لایه‌بندی اجباری Styleها

Assetها MUST به این لایه‌ها تفکیک شوند:

```text
01_tokens      Design tokens and semantic variables
02_foundation  reset, typography, direction, focus, accessibility
03_layout      shell, grid, sidebar, topbar, page containers
04_components  shared buttons, fields, cards, tables, dialogs, badges
05_patterns    dashboard, form layouts, matrix, action lists, calendars
06_modules     domain-specific scoped styles
07_utilities   minimal approved utility classes
08_overrides   documented and narrowly scoped Odoo overrides
```

یک فایل واحد و نامحدود برای تمام Styleهای Workspace مجاز نیست.

## 4. Design Tokenها

مقادیر زیر MUST از CSS Custom Property یا SCSS token مرکزی خوانده شوند:

- رنگ‌های پایه و Semantic: background، surface، text، muted، border، primary، success، warning، danger، info؛
- فاصله‌ها و Gapها؛
- Border radius؛
- Shadow/Elevation؛
- Typography scale، line-height و font weight؛
- ارتفاع input/button؛
- Sidebar width، topbar height و page max-width؛
- Z-index layers؛
- Motion duration و easing؛
- Breakpointها.

نام‌گذاری استاندارد:

```css
--cas-color-surface-1
--cas-color-text-primary
--cas-space-1
--cas-radius-md
--cas-shadow-2
--cas-control-height-md
--cas-z-dialog
```

Business Module نباید مقدارهای تکراری معادل Tokenها را Hardcode کند.

## 5. Namespace و Naming Convention

تمام Selectorهای اختصاصی CAS MUST با Namespace مشخص آغاز شوند:

```text
.cas-workspace-*
.cas-widget-*
.cas-form-*
.cas-attendance-*
.cas-work-report-*
```

برای Component State از الگوی زیر استفاده می‌شود:

```text
.is-active
.is-loading
.is-disabled
.has-error
[data-state="open"]
```

Selector عمومی مانند `button`, `table`, `.card`, `.row`, `.active` بدون Scope اختصاصی در Assetهای CAS ممنوع است.

## 6. ممنوعیت Inline Style و Style Mutation

- `style="..."` در XML/HTML برای Layout و Theme ثابت ممنوع است.
- تغییر `element.style.*` در JavaScript برای Style ثابت ممنوع است.
- مقدارهای واقعاً پویا مانند درصد پیشرفت، مختصات Drag یا اندازه محاسبه‌شده MAY از CSS variable محلی استفاده کنند.
- JavaScript باید State یا Attribute را تغییر دهد و CSS مسئول Render ظاهری باشد.

نمونه مجاز:

```js
node.style.setProperty("--cas-progress", `${percent}%`);
```

نمونه نامجاز:

```js
node.style.backgroundColor = "#1f6feb";
node.style.padding = "12px";
```

## 7. قانون `!important`

استفاده از `!important` به‌صورت پیش‌فرض ممنوع است.

استثنا فقط زمانی مجاز است که هر سه شرط برقرار باشند:

1. Override محدود یک Style خارجی یا Odoo قابل حل با Specificity منطقی نباشد؛
2. Scope دقیق و کوچک باشد؛
3. Comment شامل دلیل، Source و مسیر حذف آینده ثبت شود.

هر PR شامل `!important` جدید MUST در Review به‌صورت صریح تأیید شود.

## 8. Breakpoint و Responsive Contract

Breakpointها فقط از Registry مرکزی استفاده می‌شوند. ماژول‌ها حق تعریف Breakpoint دلخواه و متناقض ندارند.

Baseline پیشنهادی تا زمان تثبیت در Token implementation:

```text
compact/mobile: < 768px
tablet: 768px–1199px
desktop: >= 1200px
wide: >= 1600px
```

الزام‌ها:

- RTL و LTR structural behavior با Logical Propertyها نوشته شود: `margin-inline`, `padding-inline`, `inset-inline`, `border-inline`؛
- `left/right` فقط برای موارد هندسی اجتناب‌ناپذیر و مستند استفاده شود؛
- Layout باید متن فارسی بلند، Zoom 200% و Font scaling را تحمل کند؛
- Horizontal scroll برای کل صفحه ممنوع است؛ فقط Data Grid/Matrix با Container مشخص MAY scroll افقی داشته باشد؛
- Touch target کمتر از 44×44 CSS pixel برای Action اصلی مجاز نیست.

## 9. Shared Component Contract

Componentهای زیر MUST از Primitive یا کلاس مشترک استفاده کنند و هر ماژول نسخه ظاهری موازی نسازد:

- Button و Icon Button؛
- Input، Select/Searchable Select، Textarea، Checkbox، Radio، Switch؛
- Card/Widget shell؛
- Badge/Status؛
- Table/Data grid؛
- Dialog/Drawer/Popover/Tooltip؛
- Loading، Skeleton، Empty، Error، Forbidden، Unavailable؛
- Breadcrumb، Page header و Toolbar؛
- Form row، Form group و validation message.

Business Module MAY variant تعریف کند، اما MUST بر پایه Primitive مشترک باشد.

## 10. Widget Contract

هر Widget MUST این ساختار را رعایت کند:

```text
widget shell
├── widget header
├── widget actions
├── widget body
└── widget state/feedback
```

- Padding، radius، elevation و header spacing از Token مشترک می‌آید.
- Widget نباید برای جبران Layout parent از margin منفی یا absolute positioning استفاده کند.
- Widget باید در عرض‌های استاندارد `full`, `half`, `third` و حالت stack رفتار تعریف‌شده داشته باشد.
- مخفی‌سازی Widget از Preference و render condition انجام می‌شود؛ `display:none` پراکنده جایگزین Governance نیست.

## 11. Form و Dynamic Form Contract

- Grid فرم MUST responsive و مبتنی بر container باشد.
- Label، Help، Required marker و Error message جایگاه ثابت و قابل پیش‌بینی داشته باشند.
- Field conditional visibility نباید باعث overlap شود؛ عنصر مخفی از flow خارج و layout مجدداً محاسبه می‌شود.
- Searchable Dropdown MUST از Component مشترک استفاده کند و Overlay آن با Layer contract هماهنگ باشد.
- Matrix field MUST container مستقل، sticky header کنترل‌شده و scroll مشخص داشته باشد.

## 12. Odoo Asset Bundle

هر ماژول MUST Style را در Asset bundle استاندارد Odoo ثبت کند و ترتیب dependency را رعایت کند:

```text
cas_workspace tokens/foundation
→ shared components
→ module styles
→ documented Odoo overrides
```

- Import مستقیم فایل ماژول نامرتبط ممنوع است؛ dependency باید در Manifest صریح باشد.
- Assetهای Backend و Public Website مخلوط نمی‌شوند.
- Cache busting و upgrade باید از مکانیزم Asset Odoo استفاده کند.

## 13. Overrideهای Odoo

Override فقط برای Gap مستند مجاز است.

هر Override MUST شامل:

- Selector محدود زیر Root مربوط به CAS؛
- Odoo component/version target؛
- دلیل Override؛
- Screenshot یا regression scenario؛
- Risk در Upgrade؛
- Test حذف یا شکست Override.

Selectorهای بسیار گسترده روی `.o_web_client` یا `body` بدون Sub-scope ممنوع‌اند.

## 14. Specificity و Selector Depth

- حداکثر عمق پیشنهادی Selector سه سطح است.
- استفاده از ID Selector برای Styling ممنوع است.
- Nesting عمیق SCSS ممنوع است.
- Component نباید به ساختار دقیق چند Parent وابسته باشد.
- State با class/data attribute تعریف می‌شود، نه با `:nth-child` شکننده.

## 15. Accessibility و Interaction States

تمام Componentهای تعاملی MUST حالت‌های زیر را داشته باشند:

- default؛
- hover برای pointer؛
- visible focus؛
- active/pressed؛
- disabled؛
- loading؛
- error در صورت کاربرد.

Focus outline بدون جایگزین قابل مشاهده حذف نمی‌شود. Color تنها وسیله انتقال وضعیت نیست.

## 16. Performance و CSS Budget

- CSS تکراری بین ماژول‌ها باید به Shared Primitive منتقل شود.
- Selectorهای costly و universal ruleهای سنگین ممنوع‌اند.
- هر ماژول جدید UI SHOULD بودجه Style خود را در Design Review اعلام کند.
- unused selector و legacy override باید در migration هر Cycle بررسی شود.
- بارگذاری Style نباید layout shift محسوس ایجاد کند.

## 17. Theme و Personalization

- Theme فقط Semantic Tokenها را override می‌کند.
- Business Module نباید برای Theme خاص selector موازی بسازد.
- User preference مربوط به density، widget visibility و layout در `cas_workspace` ذخیره می‌شود؛ Business Data در Workspace ذخیره نمی‌شود.
- تغییر Theme یا density نباید State یا داده Business را تغییر دهد.

## 18. Migration و Backward Compatibility

برای ورود این قرارداد به کد موجود:

1. Inventory از selectorها، inline styleها، `!important`ها و hardcoded values ساخته شود.
2. Tokenها و Primitiveها ابتدا بدون تغییر ظاهری معرفی شوند.
3. ماژول‌ها مرحله‌ای migrate شوند.
4. Visual regression برای صفحات اصلی اجرا شود.
5. Legacy classها تا پایان migration با deprecation marker حفظ و سپس حذف شوند.
6. Rollback فقط Asset layer را برمی‌گرداند و نباید Business migration ایجاد کند.

## 19. Test Strategy

حداقل آزمون‌های لازم:

- Stylelint/SCSS lint برای `!important`, selector depth, forbidden IDs و hardcoded token values؛
- Visual regression برای Desktop، Tablet و Mobile؛
- RTL/LTR structure؛
- Zoom 200% و متن فارسی بلند؛
- Keyboard focus؛
- Dark/Light theme در صورت فعال‌شدن؛
- Odoo asset build و cache invalidation؛
- Upgrade regression برای overrideها؛
- screenshot comparison برای Shared Components و صفحات بحرانی.

## 20. Definition of Done برای UI Module

یک ماژول UI فقط زمانی از نظر CSS conformant است که:

- Tokenهای مشترک را مصرف کند؛
- Namespace اختصاصی داشته باشد؛
- Inline style ثابت نداشته باشد؛
- `!important` بدون Exception Record نداشته باشد؛
- Breakpoint دلخواه نداشته باشد؛
- RTL، Responsive، Focus و Long Text test پاس شده باشد؛
- Odoo overrideهایش مستند باشند؛
- Visual regression evidence داشته باشد.

## 21. Acceptance Criteria

1. تغییر فاصله و تراکم Dashboard با تغییر Token و بدون تغییر Template ممکن باشد.
2. تغییر Radius و Shadow تمام Widgetها از یک محل مرکزی اعمال شود.
3. هیچ Business Module رنگ اصلی یا spacing scale مستقل نسازد.
4. Searchable Select و custom-duration field در RTL و responsive overlap نداشته باشند.
5. هیچ تغییر CSS عادی نیازمند تغییر Model یا Migration Business نباشد.
6. direct inspection نشان دهد selectorهای CAS خارج از Namespace به Odoo leak نمی‌کنند.
7. تمام Exceptionها به `!important` و Odoo override قابل ردیابی باشند.

## 22. Revalidation Plan

این قرارداد پس از پیاده‌سازی باید حداقل روی صفحات Dashboard، Attendance/Shift، Work Report، Form Builder، Dynamic Matrix، Conversations و Calendar در نقش‌های کاربر عادی، سرپرست، مدیر و مدیر سیستم بازآزمایی شود.

نتیجه تا ارائه Commit، lint report، visual regression و UI evidence برابر `Pending Revalidation` باقی می‌ماند.
