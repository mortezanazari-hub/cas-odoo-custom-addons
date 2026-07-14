# CAS Jalali - Employees Bridge

This small bridge converts dates rendered by the Employees module's custom
Versions Timeline component. Those labels are not standard Date fields and
therefore do not pass through the global `date` field registry.

Covered in release 19.0.1.0.0:

- Employee version labels in the top timeline.
- Contract start/end dates in version tooltips.
- RTL-safe numeric label direction.
- The plus button requests a typed Jalali date instead of opening Odoo's Gregorian picker.

Database values remain standard Odoo Gregorian dates.
