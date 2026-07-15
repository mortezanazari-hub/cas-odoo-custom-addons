{
    "name": "CAS Dynamic Form Runtime",
    "summary": "Persian and RTL runtime for secure CAS dynamic forms",
    "description": """
End-user runtime for CAS organizational forms on Odoo 19 Community.

It presents published forms through an OWL client action, supports typed input,
Jalali Date/Datetime values, draft save/resume and final submission while all
definitive validation and persistence remain in cas_form_core.
""",
    "version": "19.0.1.0.6",
    "category": "Productivity",
    "author": "Chodan Ara Shomal",
    "website": "https://erp.chodanara.com",
    "license": "LGPL-3",
    "depends": ["cas_form_core", "cas_jalali", "web"],
    "data": [
        "views/cas_dynamic_form_actions.xml",
        "views/cas_dynamic_form_views.xml",
        "views/cas_dynamic_form_menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "cas_dynamic_form/static/src/js/dynamic_reference_field.js",
            "cas_dynamic_form/static/src/js/dynamic_form_app.js",
            "cas_dynamic_form/static/src/xml/dynamic_reference_field.xml",
            "cas_dynamic_form/static/src/xml/dynamic_form_app.xml",
            "cas_dynamic_form/static/src/scss/dynamic_form.scss",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
