{
    "name": "CAS Attendance Core",
    "summary": "Auditable guard and device attendance reconciliation",
    "version": "19.0.1.0.2",
    "category": "Human Resources",
    "author": "Chodan Ara Shomal",
    "license": "LGPL-3",
    "depends": ["cas_shift_management", "mail"],
    "data": [
        "security/cas_attendance_security.xml",
        "security/ir.model.access.csv",
        "views/attendance_site_views.xml",
        "views/attendance_event_views.xml",
        "views/attendance_day_views.xml",
        "views/attendance_menus.xml",
    ],
    "application": True,
    "installable": True,
}
