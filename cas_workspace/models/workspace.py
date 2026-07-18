from datetime import timedelta

from odoo import api, fields, models


FINAL_STATES = ("completed", "cancelled")


class CasWorkspaceDashboard(models.AbstractModel):
    _name = "cas.workspace.dashboard"
    _description = "CAS Organizational Workspace Data Service"

    @api.model
    def get_workspace_data(self):
        user = self.env.user
        now = fields.Datetime.now()
        today = fields.Date.context_today(self)
        start = fields.Datetime.to_datetime(today)
        end = start + timedelta(days=1)

        action_model = self.env["cas.action.item"]
        base = [
            ("visibility_user_ids", "in", user.id),
            ("company_id", "in", self.env.companies.ids),
        ]
        my_open = base + [
            ("assignee_user_id", "=", user.id),
            ("status", "not in", FINAL_STATES),
        ]
        actions = action_model.search(my_open, order=action_model._order, limit=12)

        completed_today = action_model.search_count(
            base
            + [
                ("assignee_user_id", "=", user.id),
                ("status", "=", "completed"),
                ("completed_at", ">=", start),
                ("completed_at", "<", end),
            ]
        )
        waiting = action_model.search_count(my_open + [("status", "=", "waiting")])
        overdue = action_model.search_count(my_open + [("deadline", "<", now)])
        urgent = action_model.search_count(my_open + [("priority", "in", ("urgent", "immediate"))])
        open_count = action_model.search_count(my_open)
        total = completed_today + open_count
        progress = round((completed_today / total) * 100) if total else 0

        action_rows = []
        for item in actions:
            action_rows.append(
                {
                    "id": item.id,
                    "title": item.title,
                    "source": self._source_label(item),
                    "source_icon": self._source_icon(item),
                    "owner": item.assignee_user_id.name,
                    "deadline": fields.Datetime.to_string(item.deadline) if item.deadline else False,
                    "priority": item.priority,
                    "priority_label": dict(item._fields["priority"].selection).get(item.priority, item.priority),
                    "is_overdue": bool(item.deadline and item.deadline < now),
                    "action_type": item.action_type,
                }
            )

        letter_model = self.env["cas.correspondence.letter"]
        letters = letter_model.search([], order="write_date desc, id desc", limit=4)
        letter_rows = [
            {
                "id": letter.id,
                "subject": letter.subject,
                "number": letter.number or "بدون شماره",
                "sender": letter.sender_user_id.name,
                "state": letter.state,
                "date": fields.Datetime.to_string(letter.write_date or letter.create_date),
            }
            for letter in letters
        ]

        return {
            "user": {
                "id": user.id,
                "name": user.name,
                "initials": self._initials(user.name),
                "company": user.company_id.name,
            },
            "actions": action_rows,
            "letters": letter_rows,
            "stats": {
                "total": total,
                "completed": completed_today,
                "open": open_count,
                "waiting": waiting,
                "overdue": overdue,
                "urgent": urgent,
                "progress": progress,
            },
            "today": fields.Date.to_string(today),
        }

    @api.model
    def open_action_item(self, item_id):
        item = self.env["cas.action.item"].browse(int(item_id)).exists()
        if not item:
            return False
        return item.action_open_source()

    @api.model
    def open_letter(self, letter_id):
        letter = self.env["cas.correspondence.letter"].browse(int(letter_id)).exists()
        if not letter:
            return False
        letter.check_access("read")
        return {
            "type": "ir.actions.act_window",
            "res_model": "cas.correspondence.letter",
            "res_id": letter.id,
            "views": [[False, "form"]],
            "target": "current",
        }

    @api.model
    def _source_label(self, item):
        value = (item.source_adapter or item.source_model or "").lower()
        labels = {
            "correspondence": "مکاتبات",
            "attendance": "حضور و کارکرد",
            "workflow": "گردش‌کار",
            "approval": "درخواست‌ها",
            "purchase": "خریدها",
            "contract": "قراردادها",
            "account": "مالی",
        }
        return next((label for key, label in labels.items() if key in value), "سایر امور")

    @api.model
    def _source_icon(self, item):
        value = (item.source_adapter or item.source_model or "").lower()
        icons = {
            "correspondence": "fa-envelope-o",
            "attendance": "fa-clock-o",
            "workflow": "fa-sitemap",
            "purchase": "fa-shopping-cart",
            "contract": "fa-file-text-o",
            "account": "fa-credit-card",
            "approval": "fa-check-square-o",
        }
        return next((icon for key, icon in icons.items() if key in value), "fa-file-o")

    @api.model
    def _initials(self, name):
        parts = [part for part in (name or "").split() if part]
        return "".join(part[0] for part in parts[:2]) or "ک"
