{
    "name": "CAS Jalali - Mail & Chatter Bridge",
    "summary": "Jalali dates in chatter messages, tracking values and tooltips",
    "description": """
Converts date and datetime values shown in Odoo Mail/Chatter to Jalali while
leaving stored tracking values and message datetimes unchanged.
""",
    "version": "19.0.1.0.0",
    "category": "Technical",
    "author": "Chodan Ara Shomal",
    "website": "https://erp.chodanara.com",
    "license": "LGPL-3",
    "depends": ["cas_jalali", "mail"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "cas_jalali_mail/static/src/js/message_model_patch.js",
            "cas_jalali_mail/static/src/css/mail_jalali.css",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": True,
}
