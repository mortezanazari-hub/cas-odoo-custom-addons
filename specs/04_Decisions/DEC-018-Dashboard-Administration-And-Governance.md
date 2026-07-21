# DEC-018 — حاکمیت و مدیریت داشبورد

| مشخصه | مقدار |
|---|---|
| وضعیت | `Agreed` |
| نسخه | `v8` |
| تاریخ تثبیت | `2026-07-21` |

## زمینه

Reorder کاربر به‌تنهایی برای مدیریت Workspace سازمانی کافی نیست. ادمین باید تعیین کند کدام Widgetها، با چه ترتیب و Scope، برای شرکت‌ها و نقش‌ها فعال باشند.

## تصمیم

Dashboard Management Center در v8 ایجاد می‌شود و مالک آن `cas_workspace` است، زیرا Configuration آن UI-specific است.

ادمین می‌تواند:

- Widgetها را فعال یا غیرفعال کند.
- ترتیب و Layout پیش‌فرض تعیین کند.
- Scope شرکت و Role/Profile تعیین کند.
- Widget را Required، Optional، Draggable یا Locked کند.
- Preview، Publish، Version و Rollback انجام دهد.
- Preference کاربران را Reset کند.
- Provider Health و Audit را ببیند.

کاربر عادی در v8 فقط Widgetهای مجاز و Unlocked را Reorder می‌کند. Hide/Show و Resize آزاد در Scope فعلی نیستند.

## Preference Resolution

```text
System Default
→ Company Policy
→ Role/Profile Default
→ User Preference
```

Company Policy می‌تواند تنظیم را Lock کند.

## پیامدها

- Dashboard Configuration داده کسب‌وکاری Widget را ذخیره نمی‌کند.
- Provider باید Metadata و Configuration Schema عرضه کند.
- Publish و Rollback باید Audit شوند.
- Layout نسخه‌بندی‌شده است.

## گزینه ردشده

تنظیم صرفاً Client-side یا Hard-coded برای همه کاربران رد شد.