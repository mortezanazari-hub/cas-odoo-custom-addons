# CAS Jalali Calendar — Odoo 19

Core of the organization-wide Jalali suite.

## Covered by the 2.0 RC suite

- Standard Date, Datetime and Date Range fields.
- Form, list, editable list and standard kanban formatter paths.
- Persian/Arabic-Indic/Latin typed digits.
- Native graphical Jalali picker.
- RTL-safe responsive layout.
- Timezone-aware Datetime display.
- Backend Python helpers for reports and templates.

## Internal rule

Odoo/PostgreSQL values remain standard Gregorian dates and UTC datetimes.
Jalali is the human-facing presentation and input layer.

## Deliberately separate workstreams

- True Jalali Calendar View navigation and month boundaries.
- True Jalali ORM month/quarter/year group aggregation.
- Transparent import/export conversion.


## RC4: Core DateTimeInput bridge

The shared Odoo `DateTimeInput` now uses Jalali formatting, parsing and the
graphical Jalali popover.

Covered technical paths include:

- Custom Filter
- Domain Selector
- Tree Editor date conditions
- Date and Datetime range operands

The patched component still returns Luxon DateTime values. Odoo therefore
continues serializing domains as standard Gregorian/UTC ISO values internally.
