{
    "name": "CAS Kardex Reports",
    "summary": "Detailed and summarized Excel reports for CAS Kardex",
    "version": "19.0.1.0.1",
    "category": "Human Resources",
    "author": "Chodan Ara Shomal",
    "license": "LGPL-3",
    "depends": ["cas_kardex_management"],
    "data": ["security/ir.model.access.csv", "views/kardex_report_views.xml"],
    "installable": True,
    "external_dependencies": {"python": ["xlsxwriter"]},
}
