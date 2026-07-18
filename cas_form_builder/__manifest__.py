{
    "name": "CAS Visual Form Builder",
    "summary": "Drag-and-drop visual designer for versioned CAS forms",
    "version": "19.0.1.0.0",
    "category": "Productivity",
    "author": "Chodan Ara Shomal",
    "website": "https://erp.chodanara.com",
    "license": "LGPL-3",
    "depends": ["cas_form_core", "web"],
    "data": ["views/cas_form_builder_views.xml"],
    "assets": {
        "web.assets_backend": [
            "cas_form_builder/static/src/form_builder.js",
            "cas_form_builder/static/src/form_builder.xml",
            "cas_form_builder/static/src/form_builder.scss",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
