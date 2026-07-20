# DEC-009 — توسعه Route و Capabilityهای عمومی Workspace

| مشخصه | مقدار |
|---|---|
| وضعیت | `Agreed` |
| خط مبنا | نسخه ۴ |
| نسخه هدف | نسخه ۷ |

## زمینه

نسخه ۷ شش Route و شش Capability عمومی جدید به تمام نقش‌های مرتبط اضافه می‌کند.

## تصمیم

Routeهای `personal-tasks`, `calendar`, `messages`, `global-search-page`, `notifications-center`, `recent-history` و Capabilityهای `personal.tasks`, `calendar.use`, `discuss.use`, `search.global`, `notification.read`, `history.read` بخشی از Shell رسمی Workspace هستند.

## پیامدها

- Access Resolver و Role Matrix باید توسعه یابند.
- Route Registry و تست Deep Link باید به‌روزرسانی شوند.
- Role Switch آزمایشی فقط در Prototype باقی می‌ماند.
- مخفی‌کردن Route جایگزین ACL یا Record Rule نیست.

## اسناد مرتبط

- `../02_UI_UX/Shared/Workspace_Shell.md`
- `../06_ChangeSets/CS-WORKSPACE-V7.md`
