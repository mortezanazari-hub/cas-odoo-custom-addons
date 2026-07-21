# Assignment Model — CAS Workspace v8

| مشخصه | مقدار |
|---|---|
| وضعیت | `Consolidated` |
| مالک معماری | `cas_organization_core` |

## هدف

Assignment Model واقعیت نقش و مسئولیت مؤثر فرد را در زمان مشخص تعریف می‌کند. این مدل مبنای Calendar Scope، Action Assignment و Work Report Sectionهاست.

## Assignment

Assignment حداقل شامل:

- Person/Employee/User
- Company
- Organization Unit
- Job/Role
- Responsibility Type
- Reporting Line
- Start/End Datetime
- Primary/Secondary Flag
- Active State
- Optional Shift/Profile References

## Effective Dating

تمام Resolutionها باید `effective_datetime` یا بازه معتبر داشته باشند. وضعیت فعلی به‌تنهایی برای گزارش تاریخی کافی نیست.

## چند Assignment

یک فرد می‌تواند هم‌زمان چند Assignment داشته باشد. سیستم نباید یکی را به‌صورت ضمنی حذف یا جایگزین کند.

برای Work Report:

- Assignmentهای مؤثر در Shift Context Resolve می‌شوند.
- هر Assignment یک Section می‌سازد.
- یک Report ترکیبی حفظ می‌شود.

## Shift Occurrence

Shift Occurrence دارای:

- stable identifier
- person/employee
- planned start/end
- actual context، در صورت Policy
- timezone
- source schedule/attendance
- status

شیفت عبوری از نیمه‌شب یک Occurrence است.

## Reporting Relationship

رابطه Manager/Subordinate باید:

- Effective-dated باشد.
- Direct و Recursive را تفکیک کند.
- Company و Unit را رعایت کند.
- Source و Reason قابل توضیح داشته باشد.

## Delegation

Delegation سازمانی با Work Report Access Grant متفاوت است.

- Organization Delegation: جانشینی یا تفویض مسئولیت سازمانی
- Report Access Grant: دسترسی محدود به گزارش‌ها و عملیات مشخص

Delegation ممکن است یکی از ورودی‌های Reviewer Resolution باشد، اما خودکار تمام Permissionهای Report را ایجاد نمی‌کند.

## Purpose-aware Scope

Resolver باید Purpose را بداند:

- `directory_view`
- `calendar_invite`
- `action_assign`
- `work_report_review`
- `search`
- `audit`

یک شخص ممکن است برای دعوت تقویمی مجاز باشد ولی برای تخصیص Action مجاز نباشد.

## Work Report Profile Resolution

ورودی‌ها:

- company
- employee
- shift occurrence
- effective assignments
- user override

خروجی:

- applicability
- section profiles
- form versions
- reviewer policies
- evidence defaults
- resolution explanation

## Conflict Resolution

اگر چند Policy هم‌زمان اعمال شوند:

1. User Override مجاز
2. Assignment-specific Policy
3. Job/Profile Policy
4. Company Default

مقدار `Disabled` شخصی فقط با مجوز مدیر تنظیمات گزارش قابل اعمال است.

## Snapshot

Report باید Snapshot موارد زیر را ذخیره کند:

- Assignment Key و عنوان
- Unit و Job
- Reporting Line Source
- Shift start/end/timezone
- Profile Resolution Source

Snapshot تاریخچه است و Master Data را جایگزین نمی‌کند.

## معیار پذیرش

- Multi-assignment صحیح Resolve شود.
- Shift عبوری از نیمه‌شب یک Occurrence باشد.
- Purposeهای مختلف Scope متفاوت داشته باشند.
- نتیجه Resolver Explainable باشد.
- تغییر ساختار امروز گزارش تاریخی را تغییر ندهد.
- Delegation منقضی اثر نداشته باشد.