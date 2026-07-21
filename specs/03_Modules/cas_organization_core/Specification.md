# Module Specification — `cas_organization_core`

| مشخصه | مقدار |
|---|---|
| وضعیت محصول | `Agreed` |
| وضعیت اجرا | `Needs Detailed Domain/API/Security Design` |
| مالک دامنه | Organization Scope و Effective Assignment |

## هدف

این ماژول مرجع مشترک رابطه سازمانی، Assignment مؤثر، Scope، جانشینی و Delegation سازمانی است. Calendar، Action Hub، Work Report و Search نباید منطق زیردستی را جداگانه پیاده‌سازی کنند.

## دامنه

- واحد و ساختار سازمانی
- رابطه Manager/Supervisor
- Assignment فرد به شغل یا مسئولیت
- Assignment چندگانه
- Effective Dating
- جانشینی موقت
- Delegation سازمانی
- Scope Resolver
- Reviewer Candidate Resolution

## خارج از دامنه

- Permission اختصاصی Work Report
- Personal Task Ownership
- Workflow و Approval
- HR Payroll یا Contract Lifecycle

## مدل‌های مفهومی

### Organization Unit

- company
- parent unit
- name/code
- manager assignment
- validity period
- active

### Assignment

- employee/user
- company
- organization unit
- job/role
- responsibility type
- start/end datetime
- primary flag
- reporting line
- shift/profile references اختیاری
- active

### Delegation

- delegator
- delegate
- scope type
- valid from/to
- reason
- status
- audit metadata

## Effective Resolution

Resolver باید Contextهای زیر را بپذیرد:

- user/employee
- company
- effective datetime
- purpose: view, assign, review, attendee selection
- optional domain filter

و خروجی Explainable ارائه دهد:

- Assignmentهای مؤثر
- واحدها
- managers/subordinates
- delegation path
- reason/source هر نتیجه

## Scopeهای اصلی

- self
- direct reports
- recursive reports، در صورت Policy
- organization unit
- company
- delegated scope
- explicit assignment set

## Calendar

Attendee Directory و Task Assignment از Resolver استفاده می‌کنند. دعوت به Event می‌تواند Scope گسترده‌تری از تخصیص Action داشته باشد و Purpose باید در Resolve مشخص شود.

## Work Report

- Assignmentهای مؤثر Shift را Resolve می‌کند.
- Reviewer Candidate پایه را پیشنهاد می‌دهد.
- Access Grant اختصاصی گزارش همچنان در `cas_work_report` است.

## امنیت

- Resolver نباید صرفاً فهرست کل سازمان را بازگرداند و Filtering را به Client بسپارد.
- Purpose و Caller Capability باید بررسی شود.
- Multi-company isolation اجباری است.
- Delegation زمان‌دار و قابل لغو است.
- تغییر ساختار و Assignment Audit می‌شود.

## Performance

- جست‌وجوی Directory باید Server-side و صفحه‌بندی‌شده باشد.
- Effective Date Queryها Index مناسب دارند.
- Recursive hierarchy باید از N+1 جلوگیری کند.
- Cache فقط با Invalidation معتبر استفاده می‌شود.

## API مفهومی

- resolve effective assignments
- resolve reporting scope
- search directory within purpose scope
- resolve assignable users
- resolve reviewer candidates
- create/revoke delegation
- explain resolution

## Test Strategy

- Effective dating
- Multiple assignments
- Shift crossing midnight
- Temporary delegation
- Recursive hierarchy
- Cross-company leakage
- Purpose-specific scope
- Revoked delegation
- Performance on large directory

## معیار پذیرش

- یک فرد چند Assignment مؤثر داشته باشد.
- Resolver نتیجه را با Source توضیح دهد.
- Calendar، Action Hub و Work Report از یک منطق مشترک استفاده کنند.
- Permission خاص Domainها به این ماژول منتقل نشود.
- Delegation منقضی یا لغوشده اثر نداشته باشد.