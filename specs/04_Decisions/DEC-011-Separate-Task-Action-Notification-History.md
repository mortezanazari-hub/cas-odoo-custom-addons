# DEC-011 — تفکیک Task، Action، Notification و History

| مشخصه | مقدار |
|---|---|
| وضعیت | `Agreed` |
| خط مبنا | نسخه ۴ |
| نسخه هدف | نسخه ۷ |

## زمینه

در نسخه ۴ برخی مفاهیم در سطح رابط به‌صورت نزدیک یا مشترک دیده می‌شدند. نسخه ۷ آن‌ها را به Routeها و تجربه‌های مستقل تبدیل می‌کند.

## تصمیم

چهار مفهوم زیر از یکدیگر جدا هستند:

- **Personal Task:** کار شخصی کاربر؛ الزاماً ناشی از فرایند رسمی نیست.
- **Action Item:** اقدام سازمانی که از رکورد، Workflow، Approval یا Deadline منبع تولید می‌شود.
- **Notification:** اطلاع‌رسانی درباره رخداد؛ انجام آن به معنی انجام Action نیست.
- **Recent History:** سابقه مرور و بازگشت سریع؛ Audit رسمی نیست.

## پیامدها

- Route `personal-tasks` از `my-actions` جداست.
- عنوان `my-actions` در UI به «نیازمند اقدام» تغییر می‌کند.
- Read کردن Notification، Action را Complete نمی‌کند.
- پاک‌کردن History، رکورد منبع را حذف نمی‌کند.
- Audit Log مستقل و غیرقابل جایگزینی باقی می‌ماند.

## گزینه‌های ردشده

- ذخیره همه موارد در Action Hub
- استفاده از Notification به‌عنوان Task
- استفاده از Recent History به‌عنوان Audit

## اسناد مرتبط

- `../02_UI_UX/Employee/Personal_Tasks.md`
- `../02_UI_UX/Employee/Notifications_Center.md`
- `../02_UI_UX/Employee/Recent_History.md`
