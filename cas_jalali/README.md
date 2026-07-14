# CAS Jalali Calendar

Organization-wide Jalali presentation layer for Odoo 19 Community.

## Release 19.0.1.3.0

Implemented:

- Standard `Date` fields in form and list views display Jalali dates.
- Standard `Datetime` fields display Jalali dates after Odoo applies the user timezone.
- Persian, Arabic-Indic, and Latin digits are accepted for input.
- Accepted date examples:
  - `1405/04/23`
  - `۱۴۰۵/۰۴/۲۳`
  - `١٤٠٥/٠٤/٢٣`
- Accepted datetime examples:
  - `1405/04/23 09:30`
  - `۱۴۰۵/۰۴/۲۳، ۰۹:۳۰`
- Shared frontend formatter/parser registry entries are replaced safely.
- Standard date/datetime field definitions are replaced through Odoo registries.
- The Gregorian popup icon is hidden in this release to prevent mixed-calendar input.
- Python conversion and formatting helpers are included for future reports and APIs.
- PostgreSQL and Odoo still store standard Gregorian/UTC values.

Not implemented in this release:

- Jalali graphical date picker.
- Jalali Calendar View.
- Jalali month/year grouping and search-period boundaries.
- Automatic conversion of every QWeb/PDF/email date expression.
- Jalali export conversion for every import/export path.

These items require dedicated integration with their respective Odoo views and
will be implemented after the standard field layer is validated.

## Important architecture rule

Never convert Odoo `fields.Date` or `fields.Datetime` columns into text fields.
The Jalali calendar is a presentation/input layer only.

## Manual verification

After installation:

1. Open Employees.
2. Edit a Date field such as Birthday using `۱۴۰۰/۰۱/۰۱`.
3. Save and reopen the record.
4. Confirm that the field remains Jalali.
5. Confirm the database still stores an ISO date.

## Source policy

Do not modify `/opt/odoo/odoo`. All changes belong in this addon repository.

## Release 1.1 changes

- Removed fixed minimum widths from Date/Datetime inputs.
- Added responsive flex sizing compatible with compact Odoo form rows.
- Added explicit bidi isolation so Persian labels and numeric dates do not mix.
- Added support for separate module-specific bridge addons such as
  `cas_jalali_hr`.

## Release 1.2 changes

- Native graphical Jalali picker for standard Date, Datetime and Date Range fields.
- Saturday-first weekly grid.
- Persian month names and Persian digits.
- Day, month and year navigation.
- Today, clear and close controls.
- Time selection for Datetime fields using Odoo field rounding.
- Min/max date enforcement where the field declares limits.
- Keyboard shortcut: Alt+ArrowDown opens the picker; Escape closes it.
- Direct typed Jalali input remains available.


## Release 1.3 changes

- Replaced SCSS with plain CSS to eliminate Sass compilation failures.
- Fixed graphical picker width, seven-column grid and RTL positioning.
- Added shared long Jalali date and time formatters.
- Added optional `cas_jalali_mail` bridge for Chatter and Mail dates.
- Existing database values and old chatter tracking records are not migrated;
  they are formatted dynamically when displayed.
