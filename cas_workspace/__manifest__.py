{
    "name": "CAS Organizational Workspace",
    "summary": "A fully custom RTL operational workspace for CAS on Odoo",
    "version": "19.0.2.0.0",
    "category": "Productivity",
    "author": "Chodan Ara Shomal",
    "website": "https://erp.chodanara.com",
    "license": "LGPL-3",
    "depends": ["web", "cas_action_hub", "cas_correspondence", "cas_attendance_core", "cas_workflow_core", "cas_form_core"],
    "data": [
        "views/cas_workspace_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "cas_workspace/static/src/workspace.js",
            "cas_workspace/static/src/workspace.xml",
            "cas_workspace/static/src/workspace.scss",
        ],
        "web.assets_frontend": [
            "cas_workspace/static/src/login_theme.scss",
        ],
    },
    "application": True,
    "installable": True,
    "auto_install": False,
}
