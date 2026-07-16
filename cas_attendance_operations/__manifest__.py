{
    "name": "CAS Attendance Operations",
    "summary": "Offline Excel imports and rapid guard attendance entry",
    "version": "19.0.1.0.0",
    "category": "Human Resources",
    "author": "Chodan Ara Shomal",
    "license": "LGPL-3",
    "depends": ["cas_kardex_management"],
    "data": [
        "security/cas_attendance_operations_security.xml",
        "security/ir.model.access.csv",
        "views/identity_views.xml",
        "views/import_views.xml",
        "views/guard_batch_views.xml",
        "views/operations_menus.xml",
    ],
    "application": False,
    "installable": True,
    "external_dependencies": {"python": ["openpyxl"]},
}

