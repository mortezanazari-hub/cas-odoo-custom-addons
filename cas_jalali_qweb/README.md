# CAS Jalali — QWeb & Reports Bridge

Covers standard QWeb `t-field` rendering for:

- Date
- Datetime
- `date_only`
- `time_only`
- timezone-aware output
- hidden/visible seconds
- Persian or Latin digits
- short or long Jalali output

Template helpers are also injected:

```xml
<t t-esc="format_jalali_date(record.date_field)"/>
<t t-esc="format_jalali_datetime(record.datetime_field)"/>
```

A machine-facing template can explicitly retain Gregorian output:

```xml
<span t-field="record.date_field"
      t-options="{'cas_gregorian': True}"/>
```
