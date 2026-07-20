# Change Set جامع — CAS UI Workspace v7

| مشخصه | مقدار |
|---|---|
| شناسه | `CS-WORKSPACE-V7` |
| خط مبنا | `CAS_UI_Prototype_V4` |
| نسخه هدف | `CAS UI Workspace v7` |
| وضعیت | `Collected` |
| مجوز پیاده‌سازی | ندارد |
| دامنه | کل Workspace و Adapterهای وابسته |

## مبنای Audit

مقایسه مستقیم فایل‌های Prototype نسخه ۴ و نسخه ۷ نهایی انجام شده است.

### نتیجه کمی

- Routeهای عمومی جدید: ۶ Route مستقل
- Functionهای رابط: از ۹۷ به ۱۲۲
- Actionهای UI: از ۴۴ به ۸۰
- Data Routeهای صریح: از ۳۴ به ۴۰
- تغییر خالص بسته Prototype: بیش از ۱۵۰۰ خط افزوده/اصلاح‌شده
- Capabilityهای عمومی جدید: ۶ Capability برای تمام نقش‌های مرتبط

این اعداد نشان می‌دهند نسخه ۷ صرفاً اصلاح ظاهر میزکار نیست و یک Change Set بین‌ماژولی گسترده است.

## Routeهای جدید

| Route | عنوان | Capability | وضعیت نسبت به v4 |
|---|---|---|---|
| `personal-tasks` | کارهای من | `personal.tasks` | جدید |
| `calendar` | تقویم | `calendar.use` | جدید |
| `messages` | گفت‌وگوها | `discuss.use` | جدید |
| `global-search-page` | جست‌وجوی سازمان | `search.global` | جدید |
| `notifications-center` | مرکز اعلان‌ها | `notification.read` | جدید |
| `recent-history` | تاریخچه اخیر | `history.read` | جدید |

## Routeهای تغییرمعنا یافته

| Route | نسخه ۴ | نسخه ۷ |
|---|---|---|
| `home` | خانه/داشبورد | میزکار و مرکز فرمان شخصی |
| `my-actions` | کارهای من | نیازمند اقدام سازمانی |
| `correspondence` | مکاتبات با آیکن مشابه پیام | مکاتبات رسمی با مرزبندی روشن از گفتگو |

## Capabilityهای افزوده‌شده به نقش‌ها

قابلیت‌های زیر به نقش‌های employee، supervisor، manager، ceo، guard، secretariat، shift planner، form designer، workflow designer، document manager و system admin بر اساس دسترسی مؤثر افزوده شده‌اند:

- `personal.tasks`
- `calendar.use`
- `discuss.use`
- `search.global`
- `notification.read`
- `history.read`

این تغییر باید در Access Resolver، Role Matrix، تست دسترسی و Seed/Test Users منعکس شود.

## تغییر Navigation

گروه «فضای کاری» اکنون شامل میزکار، کارهای من، تقویم، گفت‌وگوها، نیازمند اقدام، جست‌وجوی سازمان، مرکز اعلان‌ها، تاریخچه اخیر، ثبت درخواست، پیگیری درخواست، گزارش روزانه، حضور و شیفت و مکاتبات است.

## تغییرات میزکار

- Hero سه‌ردیفه
- Briefing روزانه
- وضعیت فشرده حضور
- چهار Status Card هم‌اندازه
- Command Launcher تمام‌عرض
- نوار عملیات یکپارچه
- Widget کارهای شخصی
- Widget تقویم سه‌نما
- Widget گفتگوهای اخیر
- Widget ترکیبی ثبت و مرور فعالیت
- Widget پیشرفت روز
- Widget اطلاعیه‌ها
- Drag & Drop Widgetها
- ذخیره ترتیب
- ارتفاع ثابت و Scroll داخلی Body
- Placeholder غیرفعال برای ظرفیت بصری

## تغییرات Shell

- Sidebar Collapse/Expand پایدار
- حفظ Sidebar State
- Theme روشن/تیره
- Accent Color
- Font Scale
- Density
- Drawer تنظیمات ظاهر
- Quick Conversations در Topbar
- Route و Actionهای جدید
- Stateهای مستقل Calendar، Conversation، Task و Widget Order

## Actionهای جدید عمده

### Task
`add-personal-task`, `confirm-personal-task`, `inline-task-add`, `task-quick-capture`, `toggle-personal-task`, `toggle-task-real`, `move-tomorrow`, `schedule-task`, `task-to-report`, `task-view`, `personal-task-menu`, `all-personal-tasks`.

### Calendar
`calendar-view`, `calendar-next`, `calendar-prev`, `calendar-today`, `new-calendar-event`, `calendar-event-detail`, `open-calendar-day`, `home-calendar-view`, `home-calendar-month-next`, `home-calendar-month-prev`.

### Conversation
`quick-conversations`, `open-home-conversation`, `open-drawer-conversation`, `select-conversation`, `send-chat-message`, `new-conversation`, `message-search`, `chat-info`, `chat-files`.

### Appearance/Shell
`toggle-sidebar`, `appearance-settings`, `set-v7-setting`.

## اسناد صفحه‌ای منبع

- `02_UI_UX/Employee/Workspace.md`
- `02_UI_UX/Employee/Personal_Tasks.md`
- `02_UI_UX/Employee/Calendar.md`
- `02_UI_UX/Employee/Conversations.md`
- `02_UI_UX/Employee/Global_Search.md`
- `02_UI_UX/Employee/Notifications_Center.md`
- `02_UI_UX/Employee/Recent_History.md`
- `02_UI_UX/Shared/Workspace_Shell.md`

## ماژول‌های متأثر

| ماژول/دامنه | نوع اثر | شدت |
|---|---|---:|
| `cas_workspace` | Shell، Router، Navigation، Widget Registry، Preference، Drawer، Theme، Provider Registry | بسیار زیاد |
| `cas_action_hub` | تفکیک Action از Task، Deadline Provider، نیازمند اقدام، Notification | زیاد |
| `cas_work_report` | ثبت سریع، تبدیل Task به Activity، Widget فعالیت، مجموع زمان | زیاد |
| `cas_attendance_core` | خلاصه حضور، مغایرت، Hero Provider، Notification | متوسط |
| `cas_attendance_operations` | Deep Link ثبت نگهبانی و رخدادها؛ تغییر مستقیم محدود | کم/متوسط |
| `cas_shift_management` | شیفت امروز، Calendar Provider، Notification | متوسط |
| `cas_correspondence` | Search، Notification، Calendar Provider و مرزبندی با Conversation | متوسط |
| `cas_correspondence_advanced` | Search و Notification دفتر/امضا | کم/متوسط |
| `cas_document_core` | Search Provider، Recent History، فایل‌های گفتگو و مجوز Download | متوسط |
| `cas_form_core` | Search Provider و Recent History | کم/متوسط |
| `cas_dynamic_form` | Recent History و Deep Link Runtime | کم |
| `cas_workflow_core` | Action، Calendar Deadline، Search، Notification و History | متوسط |
| `cas_workflow_designer` | History و Search مدیریتی | کم |
| `cas_approval_core` | نیازمند اقدام، Notification و Deep Link تصمیم | متوسط |
| `cas_kardex_management` | Search، Notification، Calendar Deadline و History | متوسط |
| `cas_kardex_report` | Search و Recent History خروجی‌ها | کم |
| Jalali Suite | تاریخ شمسی Calendar/Search/History | متوسط |
| Odoo Mail/Discuss/Bus | Conversation و Realtime | زیاد |
| Employee/Organization | Search Provider و نمایش شخص | متوسط |

## دامنه‌های جدید یا نیازمند تصمیم مالکیت

- Personal Task Store
- Notification Service
- Recent History Service
- Calendar Aggregation Service
- Global Search Provider Registry
- Workspace Preference Store
- Conversation Adapter

ایجاد ماژول مستقل برای این دامنه‌ها هنوز تصویب نشده است. پیش‌فرض معماری این است که Shell و Registry در `cas_workspace` باشند و داده کسب‌وکاری در Provider یا ماژول منبع باقی بماند.

## وابستگی‌های امنیتی

- تمام Routeهای جدید باید در Access Resolver ثبت شوند.
- تمام Providerها Query بدون `sudo` اجرا کنند.
- Search و History نباید عنوان رکورد غیرمجاز را افشا کنند.
- Conversation تابع عضویت و Record Rule است.
- Notification تابع مجوز رکورد منبع است.
- Calendar Event تجمیعی باید Scope ماژول منبع را رعایت کند.
- مخفی‌کردن Route یا Widget جایگزین ACL و Method Check نیست.

## وابستگی‌های فنی

- OWL Client Action برای Shell
- Router داخلی با Deep Link و Browser History
- Widget Registry
- Provider Registry برای Search، Calendar، Notification و History
- Preference Service سمت سرور
- Mail/Bus Adapter
- Jalali Formatter/Parser
- Error Boundary در سطح Widget

## مواردی که در نسخه ۷ حفظ شده‌اند

صفحات و قابلیت‌های تخصصی نسخه ۴ حذف نشده‌اند: فرم، Form Builder، Submission، Workflow، Approval، Action Hub، Document، Correspondence، Secretariat، Shift، Attendance، Guard، Kardex، Work Report، Supervisor/Manager/CEO Dashboard و Admin Center. نسخه ۷ پوسته و دسترسی عمومی به آن‌ها را توسعه می‌دهد.

## موارد خارج از دامنه این Change Set

- کدنویسی
- Migration
- انتخاب قطعی Schema سرویس‌های جدید
- تعیین نهایی Module Boundary
- پیاده‌سازی Backend Realtime
- بازطراحی تخصصی تمام صفحات مدیر و سرپرست

## شرط تبدیل به Implementation Ready

1. تکمیل اسناد تمام صفحات جدید
2. بررسی اثر Shell بر نقش‌های سرپرست، مدیر، مدیرعامل، نگهبان و دبیرخانه
3. تصویب مالکیت Personal Task، Notification، History و Calendar Aggregation
4. تجمیع آثار در Specification هر ماژول
5. تعیین API، Security، Migration و Test Strategy
6. تأیید نهایی ماژول‌به‌ماژول
