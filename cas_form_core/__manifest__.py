{
    "name": "CAS Form Core",
    "summary": "Versioned and secure form-definition foundation",
    "description": """
Technical foundation for CAS organizational forms.

It provides stable form identities, immutable published revisions, typed field
metadata, layout nodes and controlled publication. Runtime submissions,
workflow and business-specific forms live in separate modules.
""",
    "version": "19.0.1.0.3",
    "category": "Technical",
    "author": "Chodan Ara Shomal",
    "website": "https://erp.chodanara.com",
    "license": "LGPL-3",
    "depends": ["cas_core", "mail", "web"],
    "data": [
        "security/cas_form_security.xml",
        "security/ir.model.access.csv",
        "views/cas_form_definition_views.xml",
        "views/cas_form_version_views.xml",
        "views/cas_form_menus.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
