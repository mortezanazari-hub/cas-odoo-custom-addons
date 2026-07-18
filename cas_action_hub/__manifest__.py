{
    "name": "CAS Action Hub",
    "summary": "Secure unified action inbox for CAS and Odoo work items",
    "version": "19.0.1.1.0",
    "category": "Productivity",
    "author": "Chodan Ara Shomal",
    "website": "https://erp.chodanara.com",
    "license": "LGPL-3",
    "depends": ["mail"],
    "data": [
        "security/cas_action_hub_security.xml",
        "security/ir.model.access.csv",
        "data/cas_action_hub_cron.xml",
        "views/cas_action_item_views.xml",
        "views/cas_action_sla_views.xml",
        "views/cas_action_hub_menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "cas_action_hub/static/src/js/action_hub_systray.js",
            "cas_action_hub/static/src/xml/action_hub_systray.xml",
        ],
    },
    "post_init_hook": "post_init_hook",
    "application": True,
    "installable": True,
    "auto_install": False,
}
