{
    "name": "CAS Workflow Core",
    "summary": "Versioned and auditable workflow foundation for CAS business processes",
    "description": """
Secure workflow foundation for Chodan Ara organizational processes.

It provides immutable published workflow revisions, states, guarded
transitions, version-pinned runtime instances, current responsibility, SLA
deadlines and append-only transition history. Approval policies remain in a
separate extension module.
""",
    "version": "19.0.1.0.2",
    "category": "Productivity",
    "author": "Chodan Ara Shomal",
    "website": "https://erp.chodanara.com",
    "license": "LGPL-3",
    "depends": ["cas_form_core", "mail"],
    "data": [
        "data/cas_workflow_sequence.xml",
        "security/cas_workflow_security.xml",
        "security/ir.model.access.csv",
        "views/cas_workflow_definition_views.xml",
        "views/cas_workflow_runtime_views.xml",
        "views/cas_workflow_menus.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
