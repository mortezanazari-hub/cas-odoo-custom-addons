from urllib.parse import urlencode

from odoo import fields, models


class CasWorkReportExportWizard(models.TransientModel):
    _name = "cas.work.report.export.wizard"
    _description = "CAS Work Report Excel Export"

    date_from = fields.Date(string="از تاریخ")
    date_to = fields.Date(string="تا تاریخ")
    employee_id = fields.Many2one("hr.employee", string="کارمند")
    department_id = fields.Many2one("hr.department", string="واحد سازمانی")
    work_station_id = fields.Many2one("cas.work.station", string="ایستگاه کاری")
    state_code = fields.Selection(
        [("draft", "پیش‌نویس"), ("pending", "در انتظار تأیید"), ("approved", "تأییدشده"), ("rejected", "ردشده")],
        string="وضعیت",
    )

    def action_export(self):
        self.ensure_one()
        params = {
            key: value
            for key, value in {
                "date_from": self.date_from,
                "date_to": self.date_to,
                "employee_id": self.employee_id.id or None,
                "department_id": self.department_id.id or None,
                "work_station_id": self.work_station_id.id or None,
                "state_code": self.state_code or None,
            }.items()
            if value
        }
        return {
            "type": "ir.actions.act_url",
            "url": "/cas/work-report/export.xlsx?" + urlencode(params),
            "target": "self",
        }
