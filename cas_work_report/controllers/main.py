from odoo import fields, http
from odoo.http import content_disposition, request


class CasWorkReportExportController(http.Controller):
    @http.route("/cas/work-report/export.xlsx", type="http", auth="user", methods=["GET"])
    def export_work_reports(self, **params):
        domain = [("company_id", "in", request.env.companies.ids)]
        if params.get("date_from"):
            domain.append(("work_date", ">=", fields.Date.to_date(params["date_from"])))
        if params.get("date_to"):
            domain.append(("work_date", "<=", fields.Date.to_date(params["date_to"])))
        for param, field_name in (
            ("employee_id", "employee_id"),
            ("department_id", "employee_department_id"),
            ("work_station_id", "work_station_id"),
        ):
            if params.get(param):
                domain.append((field_name, "=", int(params[param])))
        if params.get("state_code") in {"draft", "pending", "approved", "rejected"}:
            domain.append(("state_code", "=", params["state_code"]))
        reports = request.env["cas.work.report"].search(domain, order="work_date desc, id desc")
        payload = request.env["cas.work.report"]._xlsx_bytes(reports)
        return request.make_response(
            payload,
            headers=[
                ("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
                ("Content-Disposition", content_disposition("cas_work_reports.xlsx")),
                ("Content-Length", str(len(payload))),
            ],
        )
