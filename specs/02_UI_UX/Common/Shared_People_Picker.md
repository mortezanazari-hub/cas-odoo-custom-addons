# Shared People Picker

| مشخصه | مقدار |
|---|---|
| Document ID | `PAGE-COMMON-PEOPLE-PICKER` |
| Document Type | Shared UI Component Specification |
| Status | `Active` |
| Document Version | `1.0` |
| Created At | `2026-07-22` |
| Updated At | `2026-07-22` |
| Owner | Workspace Experience |
| Source UI Review Cycle | `CAS UI Review Cycle 10` |
| Source Iteration | `4, 12` |
| Domain Owner | Shared Workspace Components |
| Affected Modules | `cas_workspace`, HR/organization providers, all consumers |
| Implementation Status | `Gap Identified` |
| UI Validation Status | `Pending Revalidation` |
| Related Decisions | `DEC-016-UIR10-CONSOLIDATED` |
| Related Observations | `OBS-UIR10-PEOPLE-001` |
| Related Change Sets | `CS-UIR10-ALPHA-WORKSPACE-REFINEMENT` |

## 1. Goal

یک کامپوننت واحد برای انتخاب اشخاص سازمانی فراهم شود تا مکاتبات، تفویض، Task، Workflow، Approval، گزارش‌ها و فرم‌ها منطق و ظاهر ناسازگار نسازند.

## 2. Modes

- `single`: انتخاب دقیقاً یک شخص؛
- `multiple`: انتخاب تجمعی چند شخص؛
- `max_selection`: سقف اختیاری؛
- `allow_units`: امکان انتخاب واحد فقط در مصرف‌کننده‌ای که قرارداد آن را پشتیبانی می‌کند؛
- `exclude_current_user`؛
- `preselected_ids`؛
- `required_capability` و `scope_provider`.

## 3. Layout and Components

- عنوان و توضیح Context-aware؛
- جست‌وجوی نام، نام خانوادگی، کد پرسنلی، سمت؛
- فیلتر واحد، وضعیت فعال و فیلترهای Provider؛
- فهرست شامل Avatar، نام، سمت، واحد و وضعیت؛
- Checkbox در multiple و Radio/row selection در single؛
- ناحیه انتخاب‌شده‌ها به‌صورت Chip؛
- شمارنده انتخاب؛
- پاک‌کردن انتخاب، انصراف و تأیید.

## 4. Required Interaction Rules

1. انتخاب جدید در حالت multiple انتخاب‌های قبلی را حفظ می‌کند.
2. کلیک روی Chip remove همان شخص را حذف و List state، count و CTA را هم‌زمان به‌روزرسانی می‌کند.
3. `Select all results` فقط نتایج فیلترشده و قابل انتخاب صفحه/Query جاری را انتخاب می‌کند.
4. تغییر Query انتخاب‌های قبلی را حذف نمی‌کند، مگر Provider صریحاً invalidation اعلام کند.
5. شناسه‌ها در Client باید normalized شوند و مقایسه عدد/رشته باعث از دست رفتن state نشود.
6. CTA در حالت required و انتخاب خالی غیرفعال است.

## 5. Data Contract

Provider فقط اشخاص مجاز را بازمی‌گرداند و هر نتیجه حداقل شامل `person_id`, `display_name`, `employee_code`, `job_title`, `unit_name`, `active`, `selectable`, `disabled_reason` است. انتخاب نهایی MUST در Backend دوباره اعتبارسنجی شود.

## 6. Security

- Search leakage، count leakage و metadata leakage ممنوع است.
- دست‌کاری ID در RPC باید رد شود.
- UI filtering جای ACL، record rule و method check را نمی‌گیرد.
- Cache باید user/company/capability scoped و revocation-aware باشد.

## 7. States

Loading، Empty، No Results، Error، Forbidden، Partially Unavailable و Disabled Person باید حالت مستقل و قابل فهم داشته باشند.

## 8. Accessibility and RTL

Keyboard navigation، focus trap، Escape، Enter/Space، labelهای قابل خواندن، contrast، RTL و متن فارسی طولانی الزامی است.

## 9. Acceptance Criteria

- single و multiple بدون از دست رفتن state کار کنند؛
- remove Chip تمام stateها را هم‌زمان اصلاح کند؛
- جست‌وجو و واحد عملیاتی باشند؛
- شخص غیرمجاز در response، count یا metadata دیده نشود؛
- مصرف‌کننده بتواند Provider و محدودیت انتخاب را بدون Fork کردن کامپوننت تعیین کند.
