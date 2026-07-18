from __future__ import annotations

import logging
from datetime import datetime, time, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


_logger = logging.getLogger(__name__)


FINAL_STATES = {"completed", "cancelled"}


class CasActionItem(models.Model):
    _name = "cas.action.item"
    _description = "CAS Unified Action Item"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "priority_rank desc, deadline asc, create_date desc, id desc"
    _rec_name = "title"

    source_model = fields.Char(string="مدل منبع", required=True, readonly=True, index=True)
    source_record_id = fields.Integer(string="شناسه منبع", required=True, readonly=True, index=True)
    action_key = fields.Char(string="کلید اقدام", required=True, readonly=True, index=True)
    source_adapter = fields.Char(string="آداپتر منبع", required=True, readonly=True, index=True)
    action_type = fields.Selection(
        [
            ("action", "اقدام"),
            ("decision", "تصمیم"),
            ("reply", "پاسخ"),
            ("information", "اطلاع"),
            ("review", "بازبینی"),
            ("workflow", "گردش‌کار"),
            ("activity", "فعالیت اودوو"),
        ],
        string="نوع اقدام",
        required=True,
        readonly=True,
        index=True,
    )
    title = fields.Char(string="عنوان", required=True, readonly=True)
    summary = fields.Text(string="شرح", readonly=True)
    assignee_user_id = fields.Many2one(
        "res.users", string="مسئول جاری", required=True, readonly=True, ondelete="restrict", index=True
    )
    original_assignee_user_id = fields.Many2one(
        "res.users", string="مسئول اصلی", readonly=True, ondelete="restrict", index=True
    )
    delegate_user_id = fields.Many2one(
        "res.users", string="جانشین", readonly=True, ondelete="restrict", index=True
    )
    actor_user_id = fields.Many2one(
        "res.users", string="اقدام‌کننده واقعی", readonly=True, ondelete="restrict", index=True
    )
    referred_by_user_id = fields.Many2one(
        "res.users", string="ارجاع‌دهنده", readonly=True, ondelete="restrict", index=True
    )
    manager_user_id = fields.Many2one(
        "res.users", string="مدیر مسئول", readonly=True, ondelete="restrict", index=True
    )
    visibility_user_ids = fields.Many2many(
        "res.users",
        "cas_action_item_visible_user_rel",
        "item_id",
        "user_id",
        string="کاربران مجاز",
        readonly=True,
    )
    priority = fields.Selection(
        [("normal", "عادی"), ("urgent", "فوری"), ("immediate", "آنی")],
        string="اولویت",
        required=True,
        default="normal",
        readonly=True,
        index=True,
    )
    priority_rank = fields.Integer(string="رتبه اولویت", required=True, default=0, readonly=True, index=True)
    deadline = fields.Datetime(string="مهلت", readonly=True, index=True)
    company_id = fields.Many2one(
        "res.company", string="شرکت", required=True, readonly=True, ondelete="restrict", index=True
    )
    status = fields.Selection(
        [
            ("pending", "در انتظار اقدام"),
            ("in_progress", "در حال انجام"),
            ("waiting", "منتظر دیگران"),
            ("completed", "تکمیل‌شده"),
            ("cancelled", "لغوشده"),
        ],
        string="وضعیت",
        required=True,
        default="pending",
        readonly=True,
        index=True,
    )
    source_status = fields.Char(string="وضعیت در منبع", readonly=True, index=True)
    destination_model = fields.Char(string="مدل مقصد", readonly=True)
    destination_record_id = fields.Integer(string="شناسه مقصد", readonly=True)
    destination_data = fields.Json(string="اطلاعات مقصد", readonly=True)
    source_created_at = fields.Datetime(string="زمان ایجاد در منبع", readonly=True)
    completed_at = fields.Datetime(string="زمان تکمیل", readonly=True, index=True)
    last_synced_at = fields.Datetime(string="آخرین همگام‌سازی", required=True, readonly=True, index=True)
    last_reminder_at = fields.Datetime(string="آخرین یادآوری", readonly=True, index=True)
    reminder_count = fields.Integer(string="تعداد یادآوری", readonly=True, default=0)
    escalation_level = fields.Integer(string="سطح تصعید", readonly=True, default=0, index=True)
    escalated_to_user_id = fields.Many2one(
        "res.users", string="تصعیدشده به", readonly=True, ondelete="restrict", index=True
    )
    delegation_reference = fields.Char(string="مرجع تفویض", readonly=True)
    delegation_valid_from = fields.Datetime(string="اعتبار تفویض از", readonly=True)
    delegation_valid_to = fields.Datetime(string="اعتبار تفویض تا", readonly=True)
    active = fields.Boolean(string="فعال", default=True, readonly=True, index=True)
    is_delegated = fields.Boolean(string="تفویض‌شده", compute="_compute_flags", store=True, index=True)
    is_overdue = fields.Boolean(string="موعد گذشته", compute="_compute_is_overdue", search="_search_is_overdue")
    event_ids = fields.One2many(
        "cas.action.event", "item_id", string="تاریخچه رسمی", readonly=True
    )

    _source_action_uniq = models.Constraint(
        "UNIQUE(source_model, source_record_id, action_key)",
        "هر اقدام منبع فقط یک‌بار در کارتابل ثبت می‌شود.",
    )
    _source_record_positive = models.Constraint(
        "CHECK(source_record_id > 0)", "شناسه رکورد منبع باید مثبت باشد."
    )

    @api.depends("original_assignee_user_id", "delegate_user_id")
    def _compute_flags(self):
        for item in self:
            item.is_delegated = bool(
                item.delegate_user_id
                and item.original_assignee_user_id
                and item.delegate_user_id != item.original_assignee_user_id
            )

    @api.depends("deadline", "status")
    def _compute_is_overdue(self):
        now = fields.Datetime.now()
        for item in self:
            item.is_overdue = bool(
                item.deadline and item.deadline < now and item.status not in FINAL_STATES
            )

    @api.model
    def _search_is_overdue(self, operator, value):
        positive = (operator in ("=", "==") and bool(value)) or (
            operator == "!=" and not bool(value)
        )
        domain = [
            ("deadline", "!=", False),
            ("deadline", "<", fields.Datetime.now()),
            ("status", "not in", tuple(FINAL_STATES)),
        ]
        if positive:
            return domain
        return [
            "|",
            ("deadline", "=", False),
            "|",
            ("deadline", ">=", fields.Datetime.now()),
            ("status", "in", tuple(FINAL_STATES)),
        ]

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.context.get("cas_action_hub_engine"):
            raise AccessError(_("اقدام‌ها فقط توسط موتور کارتابل ساخته می‌شوند."))
        return super().create(vals_list)

    def write(self, vals):
        if not self.env.context.get("cas_action_hub_engine"):
            raise AccessError(_("اقدام‌ها فقط توسط موتور کارتابل تغییر می‌کنند."))
        return super().write(vals)

    def unlink(self):
        raise ValidationError(_("سابقه اقدام کارتابل قابل حذف نیست."))

    @api.model
    def _model_available(self, model_name):
        return bool(model_name and model_name in self.env)

    @api.model
    def _source_record(self, model_name, record_id):
        if not self._model_available(model_name) or not int(record_id or 0):
            return False
        return self.env[model_name].browse(int(record_id)).exists()

    @api.model
    def _user_can_read(self, record, user):
        if not record or not user or not user.active or user.share:
            return False
        try:
            record.with_user(user).check_access("read")
            return True
        except AccessError:
            return False

    @api.model
    def _manager_for_user(self, user, company=None):
        company = company or user.company_id
        employee = user.sudo().employee_ids.filtered(lambda emp: emp.company_id == company)[:1]
        return employee.parent_id.user_id or employee.department_id.manager_id.user_id

    @api.model
    def _normalize_status(self, value):
        return {
            "delivered": "pending",
            "viewed": "pending",
            "pending": "pending",
            "draft": "pending",
            "in_progress": "in_progress",
            "running": "in_progress",
            "waiting": "waiting",
            "completed": "completed",
            "approved": "completed",
            "replied": "completed",
            "resolved": "completed",
            "applied": "completed",
            "published": "completed",
            "done": "completed",
            "cancelled": "cancelled",
            "rejected": "cancelled",
        }.get(str(value or "pending"), "pending")

    @api.model
    def _normalize_descriptor(self, descriptor):
        descriptor = dict(descriptor or {})
        required = {"source_model", "source_record_id", "action_key", "title", "assignee_user_id"}
        if not required.issubset(descriptor):
            raise ValidationError(_("قرارداد اقدام منبع ناقص است."))
        source = self._source_record(descriptor["source_model"], descriptor["source_record_id"])
        assignee = self.env["res.users"].browse(int(descriptor["assignee_user_id"])).exists()
        if not source or not self._user_can_read(source, assignee):
            return False
        company = self.env["res.company"].browse(
            int(descriptor.get("company_id") or assignee.company_id.id)
        ).exists()
        if not company or company not in assignee.company_ids:
            return False
        priority = descriptor.get("priority")
        if priority not in {"normal", "urgent", "immediate"}:
            priority = "normal"
        raw_status = descriptor.get("status") or "pending"
        status = self._normalize_status(raw_status)
        manager = self.env["res.users"].browse(int(descriptor.get("manager_user_id") or 0)).exists()
        manager = manager or self._manager_for_user(assignee, company)
        user_ids = {
            int(value)
            for value in (
                descriptor.get("assignee_user_id"),
                descriptor.get("original_assignee_user_id"),
                descriptor.get("delegate_user_id"),
                descriptor.get("referred_by_user_id"),
                manager.id,
            )
            if value
        }
        visible_ids = []
        for user in self.env["res.users"].browse(list(user_ids)).exists():
            if company in user.company_ids and self._user_can_read(source, user):
                visible_ids.append(user.id)
        if assignee.id not in visible_ids:
            return False
        destination = descriptor.get("destination") or {}
        destination_model = destination.get("res_model") or descriptor.get("destination_model") or descriptor["source_model"]
        destination_record_id = destination.get("res_id") or descriptor.get("destination_record_id") or descriptor["source_record_id"]
        deadline = descriptor.get("deadline") or False
        if deadline and not isinstance(deadline, datetime):
            deadline = fields.Datetime.to_datetime(deadline)
        values = {
            "source_model": descriptor["source_model"],
            "source_record_id": int(descriptor["source_record_id"]),
            "action_key": str(descriptor["action_key"]),
            "source_adapter": str(descriptor.get("source_adapter") or "generic"),
            "action_type": descriptor.get("action_type") if descriptor.get("action_type") in dict(self._fields["action_type"].selection) else "action",
            "title": str(descriptor["title"])[:512],
            "summary": descriptor.get("summary") or False,
            "assignee_user_id": assignee.id,
            "original_assignee_user_id": descriptor.get("original_assignee_user_id") or assignee.id,
            "delegate_user_id": descriptor.get("delegate_user_id") or False,
            "actor_user_id": descriptor.get("actor_user_id") or False,
            "referred_by_user_id": descriptor.get("referred_by_user_id") or False,
            "manager_user_id": manager.id or False,
            "visibility_user_ids": [(6, 0, visible_ids)],
            "priority": priority,
            "priority_rank": {"normal": 0, "urgent": 10, "immediate": 20}[priority],
            "deadline": deadline,
            "company_id": company.id,
            "status": status,
            "source_status": str(raw_status),
            "destination_model": destination_model,
            "destination_record_id": int(destination_record_id or 0),
            "destination_data": {
                "type": destination.get("type") or "ir.actions.act_window",
                "res_model": destination_model,
                "res_id": int(destination_record_id or 0),
                "views": destination.get("views") or [[False, "form"]],
            },
            "source_created_at": descriptor.get("created_at") or source.create_date,
            "delegation_reference": descriptor.get("delegation_reference") or False,
            "delegation_valid_from": descriptor.get("delegation_valid_from") or False,
            "delegation_valid_to": descriptor.get("delegation_valid_to") or False,
            "completed_at": descriptor.get("completed_at") or (fields.Datetime.now() if status in FINAL_STATES else False),
            "last_synced_at": fields.Datetime.now(),
            "active": True,
        }
        return values

    @api.model
    def _publish(self, descriptor):
        values = self._normalize_descriptor(descriptor)
        if not values:
            return self.browse()
        domain = [
            ("source_model", "=", values["source_model"]),
            ("source_record_id", "=", values["source_record_id"]),
            ("action_key", "=", values["action_key"]),
        ]
        item = self.sudo().search(domain, limit=1)
        engine = self.sudo().with_context(cas_action_hub_engine=True)
        if item:
            ignored = {"last_synced_at", "visibility_user_ids", "destination_data"}
            changed = set()
            for key, value in values.items():
                field = item._fields.get(key)
                if key in ignored or not field:
                    continue
                current = item[key]
                if field.type == "many2one":
                    current = current.id or False
                if current != value:
                    changed.add(key)
            item.with_context(cas_action_hub_engine=True).write(values)
            if changed:
                item._append_event("updated", note=_("به‌روزرسانی: %s", ", ".join(sorted(changed))))
            return item
        item = engine.create(values)
        item._append_event("published")
        return item

    @api.model
    def _update(self, descriptor):
        """Idempotent public contract for source modules; source remains truth."""
        return self._publish(descriptor)

    @api.model
    def _cancel(self, source_model, source_record_id, action_key):
        return self._complete(source_model, source_record_id, action_key, cancelled=True)

    @api.model
    def _check_source_access(self, source_model, source_record_id, user=None, mode="read"):
        source = self._source_record(source_model, source_record_id)
        if not source:
            return False
        user = user or self.env.user
        try:
            source.with_user(user).check_access(mode)
            return True
        except AccessError:
            return False

    def _resolve_destination(self, user=None):
        self.ensure_one()
        user = user or self.env.user
        source = self._source_record(self.source_model, self.source_record_id)
        if not source or not self._check_source_access(self.source_model, self.source_record_id, user):
            raise AccessError(_("دسترسی به منبع این اقدام مجاز نیست."))
        destination = self._source_record(self.destination_model, self.destination_record_id) or source
        destination.with_user(user).check_access("read")
        return destination

    def _event_snapshot(self):
        self.ensure_one()
        return {
            "source_model": self.source_model,
            "source_record_id": self.source_record_id,
            "action_key": self.action_key,
            "assignee_user_id": self.assignee_user_id.id,
            "original_assignee_user_id": self.original_assignee_user_id.id,
            "delegate_user_id": self.delegate_user_id.id,
            "manager_user_id": self.manager_user_id.id,
            "status": self.status,
            "priority": self.priority,
            "deadline": fields.Datetime.to_string(self.deadline) if self.deadline else False,
            "escalation_level": self.escalation_level,
        }

    def _append_event(self, event_type, actor=None, note=False):
        values = []
        actor = actor or self.env.user
        for item in self:
            values.append(
                {
                    "item_id": item.id,
                    "event_type": event_type,
                    "actor_user_id": actor.id,
                    "note": note or False,
                    "snapshot": item._event_snapshot(),
                }
            )
        return self.env["cas.action.event"].sudo().with_context(
            cas_action_hub_engine=True
        ).create(values)

    @api.model
    def _complete(self, source_model, source_record_id, action_key, cancelled=False):
        item = self.sudo().search(
            [
                ("source_model", "=", source_model),
                ("source_record_id", "=", int(source_record_id)),
                ("action_key", "=", action_key),
            ],
            limit=1,
        )
        if item:
            event_type = "cancelled" if cancelled else "completed"
            item.with_context(cas_action_hub_engine=True).write(
                {
                    "status": event_type,
                    "completed_at": fields.Datetime.now(),
                    "last_synced_at": fields.Datetime.now(),
                }
            )
            item._append_event(event_type)
        return item

    def action_open_source(self):
        self.ensure_one()
        self.check_access("read")
        try:
            destination = self._resolve_destination()
        except AccessError:
            self.sudo()._append_event("access_denied", actor=self.env.user)
            raise
        self.sudo()._append_event("opened", actor=self.env.user)
        return {
            "type": "ir.actions.act_window",
            "name": self.title,
            "res_model": destination._name,
            "res_id": destination.id,
            "views": [[False, "form"]],
            "target": "current",
        }

    def action_refresh_item(self):
        self.ensure_one()
        self.env["cas.action.item"].action_sync_all()
        return {"type": "ir.actions.client", "tag": "reload"}

    @api.model
    def get_my_counts(self):
        base = [
            ("visibility_user_ids", "in", self.env.user.id),
            ("company_id", "in", self.env.companies.ids),
        ]
        open_domain = base + [("status", "not in", tuple(FINAL_STATES))]
        return {
            "open": self.search_count(open_domain + [("assignee_user_id", "=", self.env.user.id)]),
            "urgent": self.search_count(open_domain + [("priority", "in", ("urgent", "immediate"))]),
            "overdue": self.search_count(open_domain + [("is_overdue", "=", True)]),
            "waiting": self.search_count(
                open_domain
                + [
                    ("assignee_user_id", "!=", self.env.user.id),
                    "|",
                    ("original_assignee_user_id", "=", self.env.user.id),
                    "|",
                    ("referred_by_user_id", "=", self.env.user.id),
                    ("manager_user_id", "=", self.env.user.id),
                ]
            ),
        }

    @api.model
    def _cron_process_sla(self):
        Rule = self.env["cas.action.sla.rule"].sudo()
        for company in self.env["res.company"].sudo().search([]):
            if not Rule.search_count([("company_id", "=", company.id)]):
                Rule.create(
                    {
                        "name": _("SLA پیش‌فرض کارتابل"),
                        "company_id": company.id,
                        "reminder_interval_hours": 24,
                        "escalation_after_hours": 24,
                        "max_escalation_level": 3,
                    }
                )
        now = fields.Datetime.now()
        items = self.sudo().search(
            [
                ("status", "not in", tuple(FINAL_STATES)),
                ("deadline", "!=", False),
                ("deadline", "<", now),
            ],
            order="deadline, id",
            limit=1000,
        )
        for item in items:
            rule = self.env["cas.action.sla.rule"]._for_item(item)
            interval = rule.reminder_interval_hours if rule else 24.0
            if item.last_reminder_at and item.last_reminder_at + timedelta(hours=interval) > now:
                continue
            overdue_hours = max((now - item.deadline).total_seconds() / 3600.0, 0.0)
            escalation_after = rule.escalation_after_hours if rule else 24.0
            max_level = rule.max_escalation_level if rule else 3
            next_level = item.escalation_level
            target = item.assignee_user_id
            event_type = "reminded"
            if overdue_hours >= escalation_after and item.escalation_level < max_level:
                next_level += 1
                candidate = (rule.escalation_user_id if rule else False) or item.manager_user_id
                source = self._source_record(item.source_model, item.source_record_id)
                if candidate and source and self._user_can_read(source, candidate):
                    target = candidate
                    visible_ids = set(item.visibility_user_ids.ids) | {candidate.id}
                    item.with_context(cas_action_hub_engine=True).write(
                        {"visibility_user_ids": [(6, 0, list(visible_ids))]}
                    )
                event_type = "escalated"
            summary = _("یادآوری کارتابل: %s", item.title)
            duplicate = self.env["mail.activity"].sudo().search_count(
                [
                    ("res_model", "=", self._name),
                    ("res_id", "=", item.id),
                    ("user_id", "=", target.id),
                    ("summary", "=", summary),
                ]
            )
            if not duplicate:
                item.activity_schedule(
                    "mail.mail_activity_data_todo",
                    user_id=target.id,
                    date_deadline=fields.Date.context_today(item),
                    summary=summary,
                    note=_("این اقدام از مهلت تعیین‌شده عبور کرده است."),
                )
            item.with_context(cas_action_hub_engine=True).write(
                {
                    "last_reminder_at": now,
                    "reminder_count": item.reminder_count + 1,
                    "escalation_level": next_level,
                    "escalated_to_user_id": target.id if event_type == "escalated" else item.escalated_to_user_id.id,
                    "priority": "immediate" if event_type == "escalated" else item.priority,
                    "priority_rank": 20 if event_type == "escalated" else item.priority_rank,
                }
            )
            item._append_event(event_type, note=_("%s ساعت از سررسید گذشته است.", round(overdue_hours, 2)))
        return len(items)

    @api.model
    def action_sync_all(self):
        if not (self.env.is_superuser() or self.env.user.has_group("cas_action_hub.group_cas_action_hub_manager")):
            raise AccessError(_("فقط مدیر کارتابل می‌تواند همگام‌سازی کامل را اجرا کند."))
        return self._sync_all()

    @api.model
    def _cron_sync_all(self):
        self._sync_all(full=True)

    @api.model
    def _cron_sync_recent(self):
        parameter = self.env["ir.config_parameter"].sudo()
        raw_since = parameter.get_param("cas_action_hub.last_incremental_sync")
        since = fields.Datetime.to_datetime(raw_since) if raw_since else fields.Datetime.now() - timedelta(minutes=5)
        result = self._sync_all(full=False, since=since - timedelta(minutes=2))
        parameter.set_param("cas_action_hub.last_incremental_sync", fields.Datetime.to_string(fields.Datetime.now()))
        return result

    @api.model
    def _recent_domain(self, domain, since=False):
        return list(domain) + ([('write_date', '>=', since)] if since else [])

    @api.model
    def _sync_all(self, full=True, since=False):
        results = {}
        for adapter, method in self._adapter_methods():
            try:
                descriptors = method(since=since)
                active_keys = set()
                count = 0
                for descriptor in descriptors:
                    item = self._publish(descriptor)
                    if item:
                        active_keys.add(item.action_key)
                        count += 1
                if full:
                    stale = self.sudo().search(
                        [("source_adapter", "=", adapter), ("status", "not in", tuple(FINAL_STATES))]
                    )
                    if active_keys:
                        stale = stale.filtered(lambda item: item.action_key not in active_keys)
                    if stale:
                        stale.with_context(cas_action_hub_engine=True).write(
                            {
                                "status": "completed",
                                "completed_at": fields.Datetime.now(),
                                "last_synced_at": fields.Datetime.now(),
                            }
                        )
                        stale._append_event("completed", note=_("تکمیل در همگام‌سازی کامل"))
                results[adapter] = count
            except Exception:
                _logger.exception("CAS Action Hub adapter failed: %s", adapter)
                results[adapter] = -1
        return results

    @api.model
    def _adapter_methods(self):
        return [
            ("cas_correspondence", self._adapt_correspondence),
            ("cas_approval", self._adapt_approval),
            ("cas_workflow", self._adapt_workflow),
            ("cas_work_report", self._adapt_work_report),
            ("cas_attendance_discrepancy", self._adapt_attendance_discrepancy),
            ("cas_attendance_request", self._adapt_attendance_request),
            ("cas_overtime", self._adapt_overtime),
            ("cas_kardex", self._adapt_kardex),
            ("cas_shift", self._adapt_shift),
            ("odoo_activity", self._adapt_odoo_activity),
        ]

    @api.model
    def _descriptor(self, record, assignee, **values):
        if not assignee:
            return False
        company = values.pop("company", False) or getattr(record, "company_id", False) or assignee.company_id
        return {
            "source_model": record._name,
            "source_record_id": record.id,
            "action_key": values.pop("action_key", f"{record._name}:{record.id}"),
            "title": values.pop("title", record.display_name),
            "assignee_user_id": assignee.id,
            "original_assignee_user_id": values.pop("original_assignee", assignee).id,
            "company_id": company.id,
            "status": values.pop("status", "pending"),
            "destination": values.pop(
                "destination",
                {"res_model": record._name, "res_id": record.id, "views": [[False, "form"]]},
            ),
            **values,
        }

    @api.model
    def _adapt_correspondence(self, since=False):
        descriptors = []
        for model_name in ("cas.correspondence.recipient", "cas.correspondence.referral"):
            if not self._model_available(model_name):
                continue
            records = self.env[model_name].sudo().search(self._recent_domain(
                [("status", "not in", ("completed", "replied", "cancelled")), ("responsible_user_id", "!=", False)], since
            ))
            for record in records:
                descriptor = record._cas_action_descriptor()
                descriptor["assignee_user_id"] = descriptor.pop("responsible_user_id")
                descriptor["original_assignee_user_id"] = descriptor.pop("original_responsible_user_id")
                descriptors.append(descriptor)
        return descriptors

    @api.model
    def _adapt_approval(self, since=False):
        if not self._model_available("cas.approval.line"):
            return []
        result = []
        for line in self.env["cas.approval.line"].sudo().search(self._recent_domain(
            [("status", "=", "pending"), ("request_id.status", "=", "pending")], since
        )):
            assignee = line.delegate_user_id or line.approver_user_id
            result.append(
                self._descriptor(
                    line,
                    assignee,
                    title=_("تصمیم %s - %s", line.request_id.number, line.role_label),
                    action_type="decision",
                    deadline=line.deadline,
                    delegate_user_id=line.delegate_user_id.id,
                    original_assignee=line.approver_user_id,
                    delegation_reference=(f"cas.approval.delegation:{line.delegation_id.id}" if line.delegation_id else False),
                    delegation_valid_from=(line.delegation_id.date_from if line.delegation_id else False),
                    delegation_valid_to=(line.delegation_id.date_to if line.delegation_id else False),
                    source_adapter="cas_approval",
                    destination={"res_model": "cas.approval.request", "res_id": line.request_id.id},
                )
            )
        return result

    @api.model
    def _adapt_workflow(self, since=False):
        if not self._model_available("cas.workflow.instance"):
            return []
        result = []
        for instance in self.env["cas.workflow.instance"].sudo().search(self._recent_domain(
            [("status", "=", "running"), ("responsible_user_id", "!=", False)], since
        )):
            destination = {"res_model": instance._name, "res_id": instance.id}
            if self._source_record(instance.resource_model, instance.resource_id):
                destination = {"res_model": instance.resource_model, "res_id": instance.resource_id}
            result.append(
                self._descriptor(
                    instance,
                    instance.responsible_user_id,
                    title=_("%s - %s", instance.resource_display_name, instance.current_state_id.name),
                    action_type="workflow",
                    status="in_progress",
                    deadline=instance.state_deadline,
                    referred_by_user_id=instance.started_by_id.id,
                    source_adapter="cas_workflow",
                    destination=destination,
                )
            )
        return result

    @api.model
    def _adapt_work_report(self, since=False):
        if not self._model_available("cas.work.report"):
            return []
        return [
            self._descriptor(
                report,
                report.supervisor_user_id,
                title=_("گزارش کار %s - %s", report.number, report.task_title),
                action_type="review",
                deadline=report.submission_deadline,
                referred_by_user_id=report.submitted_by_id.id,
                source_adapter="cas_work_report",
            )
            for report in self.env["cas.work.report"].sudo().search(self._recent_domain(
                [("state", "=", "pending"), ("supervisor_user_id", "!=", False)], since
            ))
        ]

    @api.model
    def _employee_manager_user(self, employee):
        return employee.parent_id.user_id or employee.department_id.manager_id.user_id

    @api.model
    def _adapt_attendance_discrepancy(self, since=False):
        if not self._model_available("cas.attendance.day"):
            return []
        result = []
        for day in self.env["cas.attendance.day"].sudo().search(self._recent_domain(
            [("state", "in", ("conflict", "incomplete"))], since
        )):
            assignee = self._employee_manager_user(day.employee_id)
            descriptor = self._descriptor(
                day,
                assignee,
                title=_("رسیدگی حضور %s - %s", day.employee_id.name, day.work_date),
                action_type="decision" if day.state == "conflict" else "review",
                priority="urgent" if day.state == "conflict" else "normal",
                source_adapter="cas_attendance_discrepancy",
            )
            if descriptor:
                result.append(descriptor)
        return result

    @api.model
    def _adapt_attendance_request(self, since=False):
        if not self._model_available("cas.attendance.request"):
            return []
        return [
            self._descriptor(
                request,
                request.approver_user_id,
                title=_("تصمیم %s %s", dict(request._fields["request_type"].selection).get(request.request_type), request.number),
                action_type="decision",
                referred_by_user_id=request.employee_id.user_id.id,
                source_adapter="cas_attendance_request",
            )
            for request in self.env["cas.attendance.request"].sudo().search(self._recent_domain(
                [("state", "=", "pending"), ("approver_user_id", "!=", False)], since
            ))
        ]

    @api.model
    def _adapt_overtime(self, since=False):
        if not self._model_available("cas.overtime.request"):
            return []
        result = []
        for request in self.env["cas.overtime.request"].sudo().search(self._recent_domain(
            [("state", "in", ("pending_manager", "pending_ceo"))], since
        )):
            assignee = request.manager_user_id if request.state == "pending_manager" else request.company_id.cas_ceo_user_id
            descriptor = self._descriptor(
                request,
                assignee,
                title=_("تصمیم اضافه‌کاری %s", request.number),
                action_type="decision",
                referred_by_user_id=request.employee_id.user_id.id,
                source_adapter="cas_overtime",
            )
            if descriptor:
                result.append(descriptor)
        return result

    @api.model
    def _adapt_kardex(self, since=False):
        result = []
        if self._model_available("cas.kardex.day"):
            for day in self.env["cas.kardex.day"].sudo().search(self._recent_domain(
                [("break_waiver_state", "=", "pending")], since
            )):
                assignee = self._employee_manager_user(day.employee_id)
                descriptor = self._descriptor(
                    day,
                    assignee,
                    title=_("تصمیم استراحت %s - %s", day.employee_id.name, day.work_date),
                    action_type="decision",
                    source_adapter="cas_kardex",
                )
                if descriptor:
                    result.append(descriptor)
        if self._model_available("cas.kardex.reopen"):
            for reopen in self.env["cas.kardex.reopen"].sudo().search(self._recent_domain(
                [("active", "=", True)], since
            )):
                assignee = reopen.opened_by_id or getattr(reopen.company_id, "cas_ceo_user_id", False)
                descriptor = self._descriptor(
                    reopen,
                    assignee,
                    title=_("مجوز بازگشایی کاردکس %s تا %s", reopen.date_from, reopen.date_to),
                    action_type="information",
                    deadline=datetime.combine(reopen.date_to, time.max).replace(microsecond=0) if reopen.date_to else False,
                    source_adapter="cas_kardex",
                )
                if descriptor:
                    result.append(descriptor)
        return result

    @api.model
    def _adapt_shift(self, since=False):
        result = []
        if self._model_available("cas.shift.assignment"):
            for assignment in self.env["cas.shift.assignment"].sudo().search(self._recent_domain(
                [("state", "=", "draft"), ("supervisor_user_id", "!=", False)], since
            )):
                result.append(
                    self._descriptor(
                        assignment,
                        assignment.supervisor_user_id,
                        title=_("انتشار برنامه شیفت %s", assignment.name),
                        action_type="review",
                        deadline=datetime.combine(assignment.date_from, time.min) if assignment.date_from else False,
                        source_adapter="cas_shift",
                    )
                )
        if self._model_available("cas.shift.swap"):
            for swap in self.env["cas.shift.swap"].sudo().search(self._recent_domain(
                [("state", "=", "draft")], since
            )):
                if swap.create_uid and not swap.create_uid.share:
                    result.append(
                        self._descriptor(
                            swap,
                            swap.create_uid,
                            title=_("اعمال جابه‌جایی شیفت %s", swap.name),
                            action_type="action",
                            source_adapter="cas_shift",
                        )
                    )
        return result

    @api.model
    def _adapt_odoo_activity(self, since=False):
        if not self._model_available("mail.activity"):
            return []
        result = []
        activities = self.env["mail.activity"].sudo().search(self._recent_domain(
            [("user_id", "!=", False), ("res_model", "!=", self._name)], since
        ))
        for activity in activities:
            source = self._source_record(activity.res_model, activity.res_id)
            if not source:
                continue
            company = getattr(source, "company_id", False) or activity.user_id.company_id
            deadline = (
                datetime.combine(fields.Date.to_date(activity.date_deadline), time.max).replace(microsecond=0)
                if activity.date_deadline
                else False
            )
            result.append(
                {
                    "source_model": "mail.activity",
                    "source_record_id": activity.id,
                    "action_key": f"activity:{activity.id}",
                    "title": activity.summary or activity.activity_type_id.name,
                    "summary": activity.note,
                    "assignee_user_id": activity.user_id.id,
                    "original_assignee_user_id": activity.user_id.id,
                    "referred_by_user_id": activity.create_uid.id,
                    "company_id": company.id,
                    "status": "pending",
                    "action_type": "activity",
                    "priority": "normal",
                    "deadline": deadline,
                    "source_adapter": "odoo_activity",
                    "destination": {"res_model": activity.res_model, "res_id": activity.res_id},
                }
            )
        return result
