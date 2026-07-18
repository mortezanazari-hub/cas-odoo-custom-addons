{
    "name": "CAS Visual Workflow Designer",
    "summary": "Node-based visual designer and form binding for CAS workflows",
    "version": "19.0.1.0.0",
    "category": "Productivity",
    "author": "Chodan Ara Shomal",
    "website": "https://erp.chodanara.com",
    "license": "LGPL-3",
    "depends": ["cas_workflow_core", "cas_form_core", "web"],
    "data": ["views/cas_workflow_designer_views.xml"],
    "assets": {
        "web.assets_backend": [
            "cas_workflow_designer/static/src/workflow_designer.js",
            "cas_workflow_designer/static/src/workflow_designer.xml",
            "cas_workflow_designer/static/src/workflow_designer.scss",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
