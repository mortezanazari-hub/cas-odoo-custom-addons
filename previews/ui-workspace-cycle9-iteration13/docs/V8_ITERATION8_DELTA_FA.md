# نسخه ۸ — Iteration 8: بازگردانی Auto-scroll مرورگر

## مسئله
در Iterationهای قبلی برای ثابت نگه‌داشتن Composer صفحه گفت‌وگو، قانون سراسری زیر اعمال شده بود:

```css
html, body { overflow: hidden; }
.main-content { overflow: hidden !important; }
```

این قانون Scroll Container اصلی تمام Routeها را حذف می‌کرد. در نتیجه Auto-scroll بومی مرورگر با کلیک دکمه وسط موس در صفحات عادی فعال نمی‌شد.

## تصمیم
- `main-content` در تمام Routeهای عادی دوباره Scroll Container اصلی Workspace است.
- صفحه گفت‌وگو به دلیل داشتن Scroll داخلی مستقل برای فهرست مکالمات و بدنه پیام، همچنان viewport قفل‌شده دارد.
- هیچ Handler جاوااسکریپتی برای شبیه‌سازی Auto-scroll ساخته نمی‌شود؛ رفتار استاندارد مرورگر حفظ می‌شود.
- Overlayها، Modalها و Drawerها همچنان Scroll Lock خود را مستقل مدیریت می‌کنند.

## قرارداد CSS

```css
.main-content { overflow: auto !important; }
body:has(.messenger-page) .main-content { overflow: hidden !important; }
```

## معیار پذیرش
- کلیک دکمه وسط موس در داشبورد و صفحات دارای محتوای بلند، نشانگر Auto-scroll مرورگر را فعال کند.
- حرکت موس پس از فعال‌سازی، صفحه را بالا و پایین ببرد.
- Wheel Scroll و Scrollbar همچنان کار کنند.
- صفحه گفت‌وگو Scroll کل صفحه نداشته باشد؛ فقط فهرست گفتگو و بدنه پیام اسکرول شوند.
- Composer گفتگو ثابت باقی بماند.
- Modal و Drawer باز، Scroll پس‌زمینه را طبق قرارداد Overlay قفل کنند.
