from io import BytesIO
from urllib.parse import urlencode

import xlsxwriter

from odoo import _, fields, models
from odoo.exceptions import AccessError, ValidationError


DETAIL_COLUMNS = [
    ("work_date", "تاریخ", "date"), ("employee", "کارمند", "text"), ("department", "واحد", "text"),
    ("day_kind", "نوع روز", "text"), ("planned_base", "موظفی", "minutes"),
    ("presence", "حضور واقعی", "minutes"), ("break", "استراحت کسرشده", "minutes"),
    ("net", "کار خالص", "minutes"), ("leave", "مرخصی", "minutes"), ("mission", "مأموریت", "minutes"),
    ("credited", "موظفی پوشش‌داده‌شده", "minutes"), ("absence", "کسری / غیبت", "minutes"),
    ("tardy", "تأخیر ورود", "minutes"), ("early", "تعجیل خروج", "minutes"),
    ("mandatory_ot", "اضافه‌کاری اجباری", "minutes"), ("candidate_ot", "اضافه‌کاری نیازمند مجوز", "minutes"),
    ("approved_ot", "اضافه‌کاری نهایی", "minutes"), ("holiday_work", "تعطیل‌کاری", "minutes"),
    ("state", "وضعیت", "text"),
]


class CasKardexReportWizard(models.TransientModel):
    _name = "cas.kardex.report.wizard"
    _description = "CAS Kardex Excel Report Wizard"

    date_from = fields.Date(string="از تاریخ", required=True)
    date_to = fields.Date(string="تا تاریخ", required=True)
    employee_id = fields.Many2one("hr.employee", string="کارمند")
    department_id = fields.Many2one("hr.department", string="واحد سازمانی")
    include_detail = fields.Boolean(string="گزارش تفصیلی", default=True)
    include_summary = fields.Boolean(string="گزارش خلاصه", default=True)
    include_draft = fields.Boolean(string="شامل روزهای نهایی‌نشده", default=False)

    def action_export(self):
        self.ensure_one()
        if self.date_to < self.date_from: raise ValidationError(_("تاریخ پایان نمی‌تواند قبل از شروع باشد."))
        if not self.include_detail and not self.include_summary: raise ValidationError(_("حداقل یکی از گزارش تفصیلی یا خلاصه را انتخاب کنید."))
        if not self.env.user.has_group("cas_kardex_management.group_cas_kardex_supervisor"):
            raise AccessError(_("گزارش مدیریتی کاردکس فقط در اختیار سرپرستان مجاز است."))
        params = {
            "date_from": self.date_from, "date_to": self.date_to,
            "employee_id": self.employee_id.id or "", "department_id": self.department_id.id or "",
            "detail": int(self.include_detail), "summary": int(self.include_summary), "draft": int(self.include_draft),
        }
        return {"type": "ir.actions.act_url", "url": "/cas/kardex/export.xlsx?" + urlencode(params), "target": "self"}


class CasKardexReportService(models.AbstractModel):
    _name = "cas.kardex.report.service"
    _description = "CAS Kardex Excel Report Service"

    def _domain(self, date_from, date_to, employee_id=False, department_id=False, include_draft=False):
        domain = [("work_date", ">=", date_from), ("work_date", "<=", date_to)]
        if employee_id: domain.append(("employee_id", "=", int(employee_id)))
        if department_id: domain.append(("employee_id.department_id", "=", int(department_id)))
        if not include_draft: domain.append(("state", "in", ["final", "warning"]))
        return domain

    def _detail_payload(self, day):
        day_kind = dict(day.shift_day_id._fields["day_kind"].selection).get(day.day_kind, day.day_kind or "بدون برنامه") if day.shift_day_id else "بدون برنامه"
        state = dict(day._fields["state"].selection).get(day.state, day.state)
        return {
            "work_date": day.work_date, "employee": day.employee_id.name,
            "department": day.employee_id.department_id.name or "", "day_kind": day_kind,
            "planned_base": day.planned_base_minutes, "presence": day.presence_minutes,
            "break": day.deducted_break_minutes, "net": day.net_work_minutes,
            "leave": day.leave_minutes, "mission": day.mission_minutes, "credited": day.credited_base_minutes,
            "absence": day.absence_minutes, "tardy": day.tardy_minutes, "early": day.early_exit_minutes,
            "mandatory_ot": day.mandatory_overtime_minutes, "candidate_ot": day.discretionary_overtime_minutes,
            "approved_ot": day.approved_overtime_minutes, "holiday_work": day.holiday_work_minutes, "state": state,
        }

    def build_xlsx(self, date_from, date_to, employee_id=False, department_id=False, include_detail=True, include_summary=True, include_draft=False):
        days = self.env["cas.kardex.day"].search(
            self._domain(date_from, date_to, employee_id, department_id, include_draft), order="work_date, employee_id"
        )
        stream = BytesIO(); workbook = xlsxwriter.Workbook(stream, {"in_memory": True})
        header = workbook.add_format({"bold": True, "bg_color": "#1F4E78", "font_color": "white", "align": "center", "border": 1})
        text_fmt = workbook.add_format({"align": "right", "border": 1})
        date_fmt = workbook.add_format({"num_format": "yyyy-mm-dd", "align": "center", "border": 1})
        minutes_fmt = workbook.add_format({"num_format": "[h]:mm", "align": "center", "border": 1})
        if include_detail:
            ws = workbook.add_worksheet("تفصیلی"); ws.right_to_left(); ws.freeze_panes(1, 0)
            for col, (_key, label, _kind) in enumerate(DETAIL_COLUMNS): ws.write(0, col, label, header)
            for row, day in enumerate(days, start=1):
                payload = self._detail_payload(day)
                for col, (key, _label, kind) in enumerate(DETAIL_COLUMNS):
                    value = payload[key]
                    if kind == "minutes": ws.write_number(row, col, (value or 0) / 1440.0, minutes_fmt)
                    elif kind == "date": ws.write_datetime(row, col, fields.Date.to_date(value), date_fmt)
                    else: ws.write(row, col, value or "", text_fmt)
            ws.autofilter(0, 0, max(len(days), 1), len(DETAIL_COLUMNS) - 1); ws.set_column(0, len(DETAIL_COLUMNS) - 1, 16)
            ws.set_column(1, 2, 24)
        if include_summary:
            ws = workbook.add_worksheet("خلاصه"); ws.right_to_left(); ws.freeze_panes(1, 0)
            labels = ["کارمند", "واحد", "روزهای کاردکس", "موظفی", "کار خالص", "مرخصی", "مأموریت", "کسری", "تأخیر", "تعجیل", "اضافه‌کاری اجباری", "اضافه‌کاری نهایی", "تعطیل‌کاری"]
            for col, label in enumerate(labels): ws.write(0, col, label, header)
            grouped = {}
            for day in days:
                item = grouped.setdefault(day.employee_id.id, {"employee": day.employee_id.name, "department": day.employee_id.department_id.name or "", "days": 0, "values": [0] * 10})
                item["days"] += 1
                values = [day.planned_base_minutes, day.net_work_minutes, day.leave_minutes, day.mission_minutes, day.absence_minutes, day.tardy_minutes, day.early_exit_minutes, day.mandatory_overtime_minutes, day.approved_overtime_minutes, day.holiday_work_minutes]
                item["values"] = [a + b for a, b in zip(item["values"], values)]
            for row, item in enumerate(grouped.values(), start=1):
                ws.write(row, 0, item["employee"], text_fmt); ws.write(row, 1, item["department"], text_fmt); ws.write_number(row, 2, item["days"], text_fmt)
                for col, value in enumerate(item["values"], start=3): ws.write_number(row, col, value / 1440.0, minutes_fmt)
            ws.set_column(0, 1, 24); ws.set_column(2, len(labels) - 1, 18)
        workbook.close(); return stream.getvalue(), len(days)
