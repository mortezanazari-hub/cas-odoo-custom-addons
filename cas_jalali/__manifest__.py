{
    "name": "CAS Jalali Calendar",
    "summary": "Organization-wide Jalali fields with native graphical picker",
    "description": """
CAS Jalali Calendar provides a safe Persian-calendar presentation layer.

Gregorian/UTC values remain unchanged in PostgreSQL and Odoo internals.
Release 1.3 replaces the picker stylesheet with plain CSS so no Sass
compilation is required, and exposes shared long-date/time formatters for
module-specific bridges.
""",
    "version": "19.0.1.3.0",
    "category": "Technical",
    "author": "Chodan Ara Shomal",
    "website": "https://erp.chodanara.com",
    "license": "LGPL-3",
    "depends": ["web", "cas_core"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "cas_jalali/static/src/core/jalali.js",
            "cas_jalali/static/src/picker/jalali_picker.js",
            "cas_jalali/static/src/fields/jalali_datetime_field.js",
            "cas_jalali/static/src/picker/jalali_picker.xml",
            "cas_jalali/static/src/fields/jalali_datetime_field.xml",
            "cas_jalali/static/src/css/jalali.css",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
