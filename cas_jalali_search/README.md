# CAS Jalali - Search Bridge

Adds **فیلتر تاریخ شمسی…** to the standard Odoo Filters menu.

## Release 19.0.1.0.0

Supported periods:

- امروز
- دیروز
- این هفته (شنبه تا جمعه)
- هفته گذشته
- این ماه شمسی
- ماه گذشته
- این فصل شمسی
- فصل گذشته
- امسال
- سال گذشته
- بازه دلخواه شمسی

The dialog automatically lists searchable Date and Datetime fields exposed by
the current Odoo search model.

For Date fields it creates inclusive ISO date bounds. For Datetime fields it
creates a timezone-aware lower bound and an exclusive start-of-next-day upper
bound. PostgreSQL and Odoo still receive standard Gregorian/UTC values.

This release does not change ORM `group_by` semantics. True Jalali month/year
aggregation requires a separate reporting/grouping layer and is planned for a
later release.
