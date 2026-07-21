# واژگان رسمی CAS Workspace v8

| اصطلاح | تعریف رسمی | مالک مفهوم |
|---|---|---|
| Workspace | پوسته و محیط عملیاتی مشترک نقش‌ها؛ مالک داده کسب‌وکاری نیست | `cas_workspace` |
| Widget | واحد نمایش قابل ثبت در Dashboard؛ داده را از Provider می‌گیرد | Workspace / Provider |
| Provider | پیاده‌سازی قراردادی که داده یا اقدام یک Domain را بدون انتقال مالکیت به Workspace عرضه می‌کند | ماژول منبع |
| Personal Task | کار شخصی که کاربر برای خودش مدیریت می‌کند | `cas_personal_task` |
| Organizational Action | کار یا اقدام سازمانی که برای دیگری تخصیص داده می‌شود یا در فرایند رسمی قرار دارد | `cas_action_hub` |
| Calendar Invitation | دعوت به Event؛ به‌خودی‌خود Task نیست | Calendar Domain |
| Assignment | انتساب مؤثر فرد به نقش، مسئولیت یا وظیفه سازمانی در بازه زمانی | `cas_organization_core` |
| Shift Occurrence | رخداد واقعی یک شیفت با شروع و پایان مشخص، حتی اگر از نیمه‌شب عبور کند | Shift/Attendance Integration |
| Work Report | رکورد دامنه‌ای گزارش عملکرد یک شخص در یک Shift Occurrence | `cas_work_report` |
| Report Section | بخش یک Work Report که به یک Assignment مؤثر متصل است | `cas_work_report` |
| Report Profile | تنظیمات Applicability، Form Version، Section Policy و Reviewer برای گزارش | `cas_work_report` |
| Applicability | وضعیت نیاز به گزارش: `Required`، `Optional` یا `Disabled` | Work Report Profile/User Override |
| Activity Catalog | فرهنگ فعالیت‌های استاندارد و قابل استفاده سازمان | `cas_activity_catalog` |
| Evidence | فایل، تصویر، Reference یا داده‌ای که انجام فعالیت یا صحت گزارش را پشتیبانی می‌کند | Work Report + Attachment/Document |
| Reviewer | شخص یا نقش مجاز به بررسی گزارش؛ الزاماً مدیر مستقیم نیست | Work Report Security |
| Approver | شخص یا نقش دارای اختیار تصمیم رسمی Approval | `cas_approval_core` |
| Access Grant | دسترسی تفویض‌شده و محدود به گزارش‌ها، مستقل از رابطه زیردستی | `cas_work_report` |
| Organization Scope | مجموعه افراد، واحدها، شرکت‌ها و Assignmentهایی که کاربر در Context مشخص مجاز به مشاهده یا انتخاب آن‌هاست | `cas_organization_core` |
| Capability | مجوز سطح قابلیت برای Navigation و UX؛ جایگزین ACL یا Record Rule نیست | Security Model |
| Command Palette | ابزار مشترک Search، Quick Navigation و Recent Items | `cas_workspace` |
| Recent Resource Reference | اشاره فنی به رکورد اخیراً بازشده، بدون کپی داده رکورد | `cas_workspace` |
| Notification Center | نمای مستقل تجمیع اعلان‌ها؛ Delivery پایه از Odoo استفاده می‌کند | Workspace View + Odoo Mail/Discuss |
| Overlay | لایه شناور مانند Modal، Dropdown، Selector یا Command Palette | Odoo UI Services / Workspace Shell |
| Company Policy | تنظیم سازمانی که می‌تواند Default یا Lock ایجاد کند | Admin Configuration |
| User Preference | انتخاب ظاهری کاربر در محدوده Policy سازمان | `cas_workspace` |
| Correspondence | مکاتبه رسمی سازمانی؛ با Conversation روزمره یکسان نیست | Correspondence Domain |
| Conversation | رشته پیام مبتنی بر Odoo Mail/Discuss | Odoo Mail/Discuss |
| Historical Document | سندی که فقط منشأ تصمیم یا طراحی گذشته را نگه می‌دارد | Documentation Governance |
| Canonical Baseline | بالاترین مرجع نسخه فعال محصول | Project Governance |

## تفکیک‌های اجباری

### Personal Task در برابر Organizational Action

- Self-managed و شخصی: Personal Task
- Assigned to another person یا رسمی: Organizational Action

### Invitation در برابر Assignment

- دعوت به حضور در رویداد: Invitation
- الزام به انجام کار: Assignment/Action

### Notification در برابر Action

- Notification اطلاع‌رسانی است.
- Action نیازمند انجام یا تصمیم است.

### History در برابر Audit

- Recent History برای راحتی Navigation کاربر است.
- Audit برای ردیابی رسمی تغییرات و امنیت است.

### Conversation در برابر Correspondence

- Conversation تعاملی و مبتنی بر Discuss است.
- Correspondence سند رسمی با Lifecycle و شماره‌گذاری مستقل است.

### Reviewer در برابر Manager

Reviewer می‌تواند مدیر، سرپرست، مسئول کنترل عملکرد، ممیز یا شخص دارای Access Grant باشد. رابطه زیردستی تنها یکی از مسیرهای دسترسی است.