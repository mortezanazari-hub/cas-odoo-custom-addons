from datetime import date, datetime, timedelta

from odoo import api, fields, models


FINAL_STATES = ("completed", "cancelled")


PAGE_CONFIGS = {
    "actions": {
        "title": "همه اقدام‌ها", "subtitle": "کارتابل یکپارچه کارهای قابل اقدام", "icon": "fa-tasks",
        "model": "cas.action.item", "order": "deadline asc, id desc",
        "fields": ["title", "action_type", "assignee_user_id", "deadline", "priority", "status"],
    },
    "urgent": {
        "title": "اقدام‌های فوری", "subtitle": "کارهای با اولویت بالا و خیلی بالا", "icon": "fa-bell-o",
        "model": "cas.action.item", "order": "deadline asc, id desc",
        "domain": [("priority", "in", ("urgent", "immediate"))],
        "fields": ["title", "action_type", "assignee_user_id", "deadline", "priority", "status"],
    },
    "forms": {
        "title": "فرم‌ها و پاسخ‌ها", "subtitle": "پیگیری فرم‌های سازمانی و پاسخ‌های ثبت‌شده", "icon": "fa-file-text-o",
        "model": "cas.form.submission", "fields": ["form_definition_id", "form_version_id", "state", "create_uid", "create_date"],
    },
    "form_builder": {
        "title": "فرمساز دیداری", "subtitle": "تعریف و مدیریت فرم‌های قابل طراحی", "icon": "fa-object-group",
        "model": "cas.form.definition", "fields": ["name", "code", "state", "active", "write_date"],
    },
    "workflows": {
        "title": "گردش‌کارها", "subtitle": "نمونه‌های در حال اجرا و سابقه گردش", "icon": "fa-random",
        "model": "cas.workflow.instance", "fields": ["number", "resource_display_name", "definition_id", "current_state_id", "status", "started_at"],
    },
    "workflow_builder": {
        "title": "ورک‌فلو ساز نودی", "subtitle": "تعریف نسخه‌ها، گره‌ها و مسیرهای گردش‌کار", "icon": "fa-sitemap",
        "model": "cas.workflow.definition", "fields": ["name", "code", "target_model_id", "active_version_id", "active", "write_date"],
    },
    "letters": {
        "title": "مکاتبات", "subtitle": "نامه‌های داخلی، ارجاعات و دبیرخانه", "icon": "fa-envelope-o",
        "model": "cas.correspondence.letter", "fields": ["subject", "number", "sender_user_id", "state", "write_date"],
    },
    "documents": {
        "title": "اسناد", "subtitle": "مخزن اسناد، نسخه‌ها و پوشه‌های سازمانی", "icon": "fa-folder-open-o",
        "model": "cas.document", "fields": ["number", "name", "title", "folder_id", "state", "owner_user_id", "write_date"],
    },
    "approvals": {
        "title": "تأییدها", "subtitle": "درخواست‌ها و تصمیم‌های در انتظار", "icon": "fa-check-square-o",
        "model": "cas.approval.request", "fields": ["number", "policy_id", "status", "requested_at", "completed_at"],
    },
    "attendance": {
        "title": "حضور و کارکرد", "subtitle": "روزهای حضور، مغایرت‌ها و کارکرد محاسبه‌شده", "icon": "fa-clock-o",
        "model": "cas.attendance.day", "fields": ["employee_id", "work_date", "state", "effective_entry", "effective_exit", "total_work_minutes"],
    },
    "attendance_ops": {
        "title": "عملیات تردد", "subtitle": "ورود فایل، ثبت نگهبانی و بازبینی داده‌ها", "icon": "fa-exchange",
        "model": "cas.attendance.import", "fields": ["name", "import_type", "site_id", "filename", "state", "parsed_at"],
    },
    "shifts": {
        "title": "شیفت‌ها", "subtitle": "برنامه‌ریزی شیفت و انتساب‌های مؤثر", "icon": "fa-calendar",
        "model": "cas.shift.assignment", "fields": ["number", "name", "department_id", "date_from", "date_to", "state"],
    },
    "kardex": {
        "title": "کاردکس", "subtitle": "دوره‌های کارکرد، کنترل و نهایی‌سازی", "icon": "fa-table",
        "model": "cas.kardex.period", "fields": ["name", "date_from", "date_to", "state", "company_id", "write_date"],
    },
    "work_reports": {
        "title": "گزارش کار", "subtitle": "گزارش‌های روزانه و زمان ثبت‌شده", "icon": "fa-line-chart",
        "model": "cas.work.report", "fields": ["number", "employee_id", "work_date", "state", "total_minutes", "write_date"],
    },
    "settings": {
        "title": "تنظیمات سامانه", "subtitle": "کاربران، دسترسی‌ها و وضعیت ماژول‌های CAS", "icon": "fa-cog",
        "model": "res.users", "domain": [("share", "=", False)], "fields": ["name", "login", "active", "company_id", "write_date"],
    },
}


NAVIGATION = [
    ("dashboard", "کارتابل من", "fa-inbox", "main"),
    ("urgent", "اقدام‌های فوری", "fa-bell-o", "main"),
    ("actions", "همه کارها", "fa-tasks", "main"),
    ("forms", "فرم‌ها", "fa-file-text-o", "process"),
    ("form_builder", "فرمساز دیداری", "fa-object-group", "process"),
    ("workflows", "گردش‌کارها", "fa-random", "process"),
    ("workflow_builder", "ورک‌فلو ساز", "fa-sitemap", "process"),
    ("letters", "مکاتبات", "fa-envelope-o", "records"),
    ("documents", "اسناد", "fa-folder-open-o", "records"),
    ("approvals", "تأییدها", "fa-check-square-o", "records"),
    ("attendance", "حضور و کارکرد", "fa-clock-o", "operations"),
    ("attendance_ops", "عملیات تردد", "fa-exchange", "operations"),
    ("shifts", "شیفت‌ها", "fa-calendar", "operations"),
    ("kardex", "کاردکس", "fa-table", "reports"),
    ("work_reports", "گزارش کار", "fa-line-chart", "reports"),
    ("settings", "تنظیمات", "fa-cog", "footer"),
]


class CasWorkspaceDashboard(models.AbstractModel):
    _name = "cas.workspace.dashboard"
    _description = "CAS Organizational Workspace Data Service"

    @api.model
    def get_navigation(self):
        modules = self.env["ir.module.module"].sudo().search_read(
            [("name", "like", "cas_%"), ("state", "=", "installed")], ["name", "shortdesc", "installed_version"]
        )
        installed = {row["name"]: row for row in modules}
        return {
            "items": [
                {"key": key, "label": label, "icon": icon, "group": group}
                for key, label, icon, group in NAVIGATION
            ],
            "installed_modules": sorted(installed.values(), key=lambda row: row["name"]),
        }

    @api.model
    def get_workspace_data(self):
        user = self.env.user
        now = fields.Datetime.now()
        today = fields.Date.context_today(self)
        start = fields.Datetime.to_datetime(today)
        end = start + timedelta(days=1)
        action_model = self.env["cas.action.item"]
        base = [("visibility_user_ids", "in", user.id), ("company_id", "in", self.env.companies.ids)]
        my_open = base + [("assignee_user_id", "=", user.id), ("status", "not in", FINAL_STATES)]
        actions = action_model.search(my_open, order=action_model._order, limit=8)
        completed_today = action_model.search_count(base + [("assignee_user_id", "=", user.id), ("status", "=", "completed"), ("completed_at", ">=", start), ("completed_at", "<", end)])
        waiting = action_model.search_count(my_open + [("status", "=", "waiting")])
        overdue = action_model.search_count(my_open + [("deadline", "<", now)])
        urgent = action_model.search_count(my_open + [("priority", "in", ("urgent", "immediate"))])
        open_count = action_model.search_count(my_open)
        total = completed_today + open_count
        letters = self.env["cas.correspondence.letter"].search([], order="write_date desc, id desc", limit=4)
        return {
            "user": {"id": user.id, "name": user.name, "initials": self._initials(user.name), "company": user.company_id.name},
            "actions": [{
                "id": item.id, "title": item.title, "source": self._source_label(item), "source_icon": self._source_icon(item),
                "owner": item.assignee_user_id.name, "deadline": fields.Datetime.to_string(item.deadline) if item.deadline else False,
                "priority": item.priority, "priority_label": self._selection_label(item, "priority"),
                "status": item.status, "status_label": self._selection_label(item, "status"), "is_overdue": bool(item.deadline and item.deadline < now),
            } for item in actions],
            "letters": [{"id": letter.id, "subject": letter.subject, "number": letter.number or "بدون شماره", "sender": letter.sender_user_id.name, "state": letter.state, "date": fields.Datetime.to_string(letter.write_date or letter.create_date)} for letter in letters],
            "stats": {"total": total, "completed": completed_today, "open": open_count, "waiting": waiting, "overdue": overdue, "urgent": urgent, "progress": round((completed_today / total) * 100) if total else 0},
            "today": fields.Date.to_string(today),
        }

    @api.model
    def get_page_data(self, route, query="", offset=0, limit=25):
        config = PAGE_CONFIGS.get(route)
        if not config:
            return {"available": False, "title": "بخش نامعتبر", "rows": [], "columns": [], "total": 0}
        model_name = config["model"]
        if model_name not in self.env:
            return {"available": False, "title": config["title"], "subtitle": config["subtitle"], "icon": config["icon"], "model": model_name, "rows": [], "columns": [], "total": 0}
        model = self.env[model_name]
        available_fields = model.fields_get()
        field_names = [name for name in config["fields"] if name in available_fields and available_fields[name]["type"] not in ("one2many", "many2many", "binary")]
        domain = list(config.get("domain", []))
        query = (query or "").strip()
        if query:
            searchable = [name for name in field_names if available_fields[name]["type"] in ("char", "text", "html")]
            if searchable:
                query_domain = []
                for index, name in enumerate(searchable):
                    if index:
                        query_domain.insert(0, "|")
                    query_domain.append((name, "ilike", query))
                domain += query_domain
        total = model.search_count(domain)
        order = self._safe_order(model, config.get("order"))
        records = model.search(domain, offset=max(int(offset), 0), limit=min(max(int(limit), 1), 100), order=order)
        columns = [{"key": name, "label": available_fields[name].get("string") or name, "type": available_fields[name]["type"]} for name in field_names]
        rows = []
        for record in records:
            cells = []
            for name in field_names:
                cells.append(self._serialize_value(record, name, available_fields[name]))
            rows.append({"id": record.id, "display_name": record.display_name, "cells": cells})
        return {"available": True, "title": config["title"], "subtitle": config["subtitle"], "icon": config["icon"], "model": model_name, "columns": columns, "rows": rows, "total": total, "offset": max(int(offset), 0), "limit": min(max(int(limit), 1), 100)}

    @api.model
    def get_record_detail(self, route, record_id):
        config = PAGE_CONFIGS.get(route)
        if not config or config["model"] not in self.env:
            return False
        record = self.env[config["model"]].browse(int(record_id)).exists()
        if not record:
            return False
        record.check_access("read")
        meta = record.fields_get()
        preferred = [name for name in config["fields"] if name in meta]
        common = ["create_uid", "create_date", "write_uid", "write_date", "company_id"]
        names = preferred + [name for name in common if name in meta and name not in preferred]
        return {"id": record.id, "title": record.display_name, "fields": [{"label": meta[name].get("string") or name, "value": self._serialize_value(record, name, meta[name])["text"]} for name in names if meta[name]["type"] not in ("one2many", "many2many", "binary", "html")]}

    @api.model
    def _serialize_value(self, record, name, meta):
        value = record[name]
        field_type = meta["type"]
        raw = value
        if field_type == "many2one":
            text = value.display_name if value else "—"
            raw = value.id if value else False
        elif field_type == "selection":
            text = self._selection_label(record, name) if value else "—"
        elif field_type == "boolean":
            text = "فعال" if value else "غیرفعال"
        elif field_type == "date":
            text = fields.Date.to_string(value) if value else "—"
        elif field_type == "datetime":
            text = fields.Datetime.to_string(value) if value else "—"
        elif field_type in ("integer", "float", "monetary"):
            text = f"{value:,}"
        else:
            text = str(value) if value not in (False, None, "") else "—"
        return {"key": name, "text": text, "raw": raw, "type": field_type, "tone": self._value_tone(name, raw)}

    @api.model
    def _selection_label(self, record, field_name):
        field = record._fields[field_name]
        selection = field._description_selection(self.env)
        return dict(selection).get(record[field_name], record[field_name])

    @api.model
    def _value_tone(self, name, value):
        value = str(value or "").lower()
        if name in ("state", "status", "priority"):
            if value in ("completed", "approved", "done", "sent", "published", "imported", "active"):
                return "success"
            if value in ("cancelled", "rejected", "overdue", "immediate", "error"):
                return "danger"
            if value in ("waiting", "pending", "draft", "review", "urgent"):
                return "warning"
        return "default"

    @api.model
    def _safe_order(self, model, requested):
        if requested:
            names = [part.strip().split()[0] for part in requested.split(",")]
            if all(name in model._fields for name in names):
                return requested
        return model._order or "id desc"

    @api.model
    def _source_label(self, item):
        value = (item.source_adapter or item.source_model or "").lower()
        labels = {"correspondence": "مکاتبات", "attendance": "حضور و کارکرد", "workflow": "گردش‌کار", "approval": "تأییدها", "purchase": "خریدها", "contract": "قراردادها", "account": "مالی"}
        return next((label for key, label in labels.items() if key in value), "سایر امور")

    @api.model
    def _source_icon(self, item):
        value = (item.source_adapter or item.source_model or "").lower()
        icons = {"correspondence": "fa-envelope-o", "attendance": "fa-clock-o", "workflow": "fa-sitemap", "purchase": "fa-shopping-cart", "contract": "fa-file-text-o", "account": "fa-credit-card", "approval": "fa-check-square-o"}
        return next((icon for key, icon in icons.items() if key in value), "fa-file-o")

    @api.model
    def _initials(self, name):
        parts = [part for part in (name or "").split() if part]
        return "".join(part[0] for part in parts[:2]) or "ک"
