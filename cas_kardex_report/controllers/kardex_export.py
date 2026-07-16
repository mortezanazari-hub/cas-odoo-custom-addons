from odoo import fields, http
from odoo.http import request
from werkzeug.exceptions import Forbidden


class CasKardexExportController(http.Controller):
    @http.route("/cas/kardex/export.xlsx", type="http", auth="user", methods=["GET"], csrf=False)
    def export_xlsx(self, date_from, date_to, employee_id=None, department_id=None, detail="1", summary="1", draft="0", **_kwargs):
        if not request.env.user.has_group("cas_kardex_management.group_cas_kardex_supervisor"):
            raise Forbidden()
        start = fields.Date.to_date(date_from); end = fields.Date.to_date(date_to)
        content, _count = request.env["cas.kardex.report.service"].build_xlsx(
            start, end, employee_id=employee_id or False, department_id=department_id or False,
            include_detail=detail == "1", include_summary=summary == "1", include_draft=draft == "1",
        )
        filename = f"kardex_{start}_{end}.xlsx"
        return request.make_response(content, headers=[
            ("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            ("Content-Disposition", f'attachment; filename="{filename}"'),
        ])
