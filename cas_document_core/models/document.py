from __future__ import annotations

import base64
import hashlib
import mimetypes
import re

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError

from .document_folder import CONFIDENTIALITY


def _safe_filename(value):
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", str(value or "document"))
    return value.strip("._") or "document"


class CasDocumentTag(models.Model):
    _name = "cas.document.tag"
    _description = "CAS Document Tag"
    _order = "name"

    name = fields.Char(string="عنوان", required=True, translate=True)
    color = fields.Integer()

    _name_uniq = models.Constraint("UNIQUE(name)", "عنوان برچسب باید یکتا باشد.")


class CasDocument(models.Model):
    _name = "cas.document"
    _description = "CAS Versioned Document"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc, id desc"
    _rec_name = "number"

    number = fields.Char(string="شماره سند", default="New", readonly=True, copy=False, index=True)
    name = fields.Char(string="عنوان", required=True, tracking=True)
    description = fields.Text(string="شرح")
    company_id = fields.Many2one(
        "res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True
    )
    folder_id = fields.Many2one("cas.document.folder", string="پوشه", required=True, ondelete="restrict", index=True)
    owner_user_id = fields.Many2one(
        "res.users", string="مالک", required=True, default=lambda self: self.env.user, ondelete="restrict", index=True
    )
    authorized_user_ids = fields.Many2many(
        "res.users", "cas_document_authorized_user_rel", "document_id", "user_id", string="کاربران مجاز"
    )
    confidentiality = fields.Selection(
        CONFIDENTIALITY, string="محرمانگی", required=True, default="normal", tracking=True, index=True
    )
    tag_ids = fields.Many2many("cas.document.tag", string="برچسب‌ها")
    storage_backend_id = fields.Many2one(
        "cas.document.storage.backend", string="ذخیره‌ساز", required=True, ondelete="restrict"
    )
    state = fields.Selection(
        [("draft", "پیش‌نویس"), ("active", "فعال"), ("archived", "بایگانی"), ("destroyed", "امحاشده")],
        string="وضعیت",
        required=True,
        default="draft",
        readonly=True,
        tracking=True,
        index=True,
    )
    retention_until = fields.Date(string="نگهداری تا")
    legal_hold = fields.Boolean(string="توقف حقوقی امحا", tracking=True)
    current_version_id = fields.Many2one(
        "cas.document.version", string="نسخه جاری", readonly=True, copy=False, ondelete="restrict"
    )
    version_ids = fields.One2many("cas.document.version", "document_id", string="نسخه‌ها", copy=False)
    version_count = fields.Integer(string="تعداد نسخه", compute="_compute_version_count")
    current_sha256 = fields.Char(related="current_version_id.sha256", string="SHA-256 نسخه جاری", readonly=True)
    link_ids = fields.One2many("cas.document.link", "document_id", string="پیوندهای کسب‌وکار", copy=False)
    event_ids = fields.One2many("cas.document.event", "document_id", string="تاریخچه رسمی", copy=False)

    _number_company_uniq = models.Constraint(
        "UNIQUE(number, company_id)", "شماره سند باید در هر شرکت یکتا باشد."
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = self.browse()
        for vals in vals_list:
            values = dict(vals)
            company = self.env["res.company"].browse(values.get("company_id")) or self.env.company
            if values.get("number", "New") == "New":
                values["number"] = self.env["ir.sequence"].with_company(company).next_by_code("cas.document") or "New"
            if not values.get("storage_backend_id"):
                backend = self.env["cas.document.storage.backend"].default_for_company(company)
                if not backend:
                    backend = self.env["cas.document.storage.backend"].sudo().create(
                        {"name": _("پایگاه داده Odoo"), "company_id": company.id, "backend_type": "database", "is_default": True}
                    )
                values["storage_backend_id"] = backend.id
            record = super(CasDocument, self).create(values)
            record._append_event("created")
            records |= record
        return records

    def write(self, vals):
        protected = {"number", "company_id", "storage_backend_id", "current_version_id", "state"}
        if protected.intersection(vals) and not self.env.context.get("cas_document_engine"):
            raise ValidationError(_("فیلدهای رسمی سند فقط از عملیات کنترل‌شده تغییر می‌کنند."))
        if any(document.state == "destroyed" for document in self) and not self.env.context.get("cas_document_engine"):
            raise ValidationError(_("سند امحاشده قابل تغییر نیست."))
        result = super().write(vals)
        if not self.env.context.get("cas_document_engine"):
            self._append_event("metadata_updated", note=", ".join(sorted(vals)))
        return result

    def unlink(self):
        raise ValidationError(_("سند و تاریخچه رسمی آن قابل حذف نیست."))

    @api.depends("version_ids")
    def _compute_version_count(self):
        for document in self:
            document.version_count = len(document.version_ids)

    @api.constrains("company_id", "folder_id", "owner_user_id", "authorized_user_ids", "storage_backend_id")
    def _check_company_contract(self):
        for document in self:
            if document.folder_id.company_id != document.company_id:
                raise ValidationError(_("پوشه و سند باید متعلق به یک شرکت باشند."))
            if document.storage_backend_id.company_id != document.company_id:
                raise ValidationError(_("ذخیره‌ساز و سند باید متعلق به یک شرکت باشند."))
            users = document.owner_user_id | document.authorized_user_ids
            if any(document.company_id not in user.company_ids for user in users):
                raise ValidationError(_("همه کاربران سند باید عضو همان شرکت باشند."))

    def _require_editor(self):
        for document in self:
            allowed = bool(
                self.env.is_superuser()
                or document.owner_user_id == self.env.user
                or self.env.user in document.authorized_user_ids
                or document.folder_id.manager_user_id == self.env.user
                or self.env.user.has_group("cas_document_core.group_cas_document_manager")
            )
            if not allowed:
                raise AccessError(_("مجوز ویرایش این سند را ندارید."))

    def _append_event(self, event_type, note=False, version=False):
        values = []
        for document in self:
            values.append(
                {
                    "document_id": document.id,
                    "version_id": version.id if version else False,
                    "event_type": event_type,
                    "actor_user_id": self.env.user.id,
                    "note": note or False,
                }
            )
        return self.env["cas.document.event"].sudo().with_context(cas_document_engine=True).create(values)

    def action_activate(self):
        self._require_editor()
        for document in self:
            if document.state != "draft" or not document.current_version_id:
                raise ValidationError(_("فقط پیش‌نویس دارای نسخه قابل فعال‌سازی است."))
            document.with_context(cas_document_engine=True).write({"state": "active"})
            document._append_event("activated")
        return True

    def action_archive(self):
        self._require_editor()
        for document in self:
            if document.state not in ("draft", "active"):
                raise ValidationError(_("این سند قابل بایگانی نیست."))
            document.with_context(cas_document_engine=True).write({"state": "archived"})
            document._append_event("archived")
        return True

    def action_destroy(self):
        if not self.env.user.has_group("cas_document_core.group_cas_document_manager"):
            raise AccessError(_("فقط مدیر اسناد می‌تواند امحا را ثبت کند."))
        today = fields.Date.context_today(self)
        for document in self:
            if document.legal_hold:
                raise ValidationError(_("این سند توقف حقوقی دارد و قابل امحا نیست."))
            if not document.retention_until or document.retention_until > today:
                raise ValidationError(_("دوره نگهداری سند هنوز پایان نیافته است."))
            document.with_context(cas_document_engine=True).write({"state": "destroyed"})
            document._append_event("destroyed")
        return True

    def action_open_upload_version(self):
        self.ensure_one()
        self._require_editor()
        return {
            "type": "ir.actions.act_window",
            "name": _("افزودن نسخه سند"),
            "res_model": "cas.document.upload.version.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_document_id": self.id},
        }

    def add_version(self, filename, content, mimetype=False, note=False):
        self.ensure_one()
        self._require_editor()
        if self.state == "destroyed":
            raise ValidationError(_("سند امحاشده نسخه جدید نمی‌پذیرد."))
        if isinstance(content, str):
            content = base64.b64decode(content)
        if not isinstance(content, (bytes, bytearray)) or not content:
            raise ValidationError(_("محتوای نسخه الزامی است."))
        content = bytes(content)
        filename = _safe_filename(filename)
        mimetype = mimetype or mimetypes.guess_type(filename)[0] or "application/octet-stream"
        number = (max(self.version_ids.mapped("version_number")) if self.version_ids else 0) + 1
        digest = hashlib.sha256(content).hexdigest()
        duplicate = self.version_ids.filtered(lambda version: version.sha256 == digest)
        if duplicate:
            raise ValidationError(_("این محتوا قبلاً به‌عنوان نسخه %s ثبت شده است.", duplicate[0].version_number))
        attachment = False
        external_path = False
        backend = self.storage_backend_id
        if backend.backend_type == "database":
            attachment = self.env["ir.attachment"].sudo().create(
                {
                    "name": filename,
                    "datas": base64.b64encode(content),
                    "mimetype": mimetype,
                    "res_model": self._name,
                    "res_id": self.id,
                    "company_id": self.company_id.id,
                }
            )
        else:
            external_path = "/".join(
                (_safe_filename(self.company_id.name), _safe_filename(self.number), f"v{number:04d}-{filename}")
            )
            backend.upload(external_path, content, mimetype)
        version = self.env["cas.document.version"].sudo().with_context(cas_document_engine=True).create(
            {
                "document_id": self.id,
                "version_number": number,
                "filename": filename,
                "mimetype": mimetype,
                "size_bytes": len(content),
                "sha256": digest,
                "attachment_id": attachment.id if attachment else False,
                "external_path": external_path,
                "created_by_user_id": self.env.user.id,
                "note": note or False,
            }
        )
        self.with_context(cas_document_engine=True).write({"current_version_id": version.id})
        self._append_event("version_added", version=version, note=note)
        return version


class CasDocumentVersion(models.Model):
    _name = "cas.document.version"
    _description = "CAS Immutable Document Version"
    _order = "document_id, version_number desc"
    _rec_name = "filename"

    document_id = fields.Many2one("cas.document", string="سند", required=True, ondelete="restrict", index=True)
    company_id = fields.Many2one(related="document_id.company_id", store=True, index=True)
    version_number = fields.Integer(string="نسخه", required=True, readonly=True)
    filename = fields.Char(string="نام فایل", required=True, readonly=True)
    mimetype = fields.Char(string="نوع فایل", required=True, readonly=True)
    size_bytes = fields.Integer(string="حجم (بایت)", required=True, readonly=True)
    sha256 = fields.Char(string="SHA-256", required=True, readonly=True, index=True)
    attachment_id = fields.Many2one("ir.attachment", string="فایل Odoo", readonly=True, ondelete="restrict")
    external_path = fields.Char(string="مسیر خارجی", readonly=True)
    created_by_user_id = fields.Many2one("res.users", string="ثبت‌کننده", required=True, readonly=True, ondelete="restrict")
    created_at = fields.Datetime(string="زمان ثبت", required=True, default=fields.Datetime.now, readonly=True)
    note = fields.Text(string="شرح نسخه", readonly=True)
    ocr_text = fields.Text(string="متن OCR", readonly=True)

    _document_version_uniq = models.Constraint(
        "UNIQUE(document_id, version_number)", "شماره نسخه در هر سند باید یکتا باشد."
    )
    _storage_pointer_check = models.Constraint(
        "CHECK((attachment_id IS NOT NULL) <> (external_path IS NOT NULL))",
        "هر نسخه باید دقیقاً یک محل ذخیره‌سازی داشته باشد.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.context.get("cas_document_engine"):
            raise AccessError(_("نسخه فقط از عملیات رسمی سند ایجاد می‌شود."))
        return super().create(vals_list)

    def write(self, vals):
        allowed = {"ocr_text"} if self.env.context.get("cas_document_ocr_engine") else set()
        if not vals or not set(vals) <= allowed:
            raise ValidationError(_("نسخه ثبت‌شده قابل تغییر نیست."))
        return super().write(vals)

    def unlink(self):
        raise ValidationError(_("نسخه و سابقه سند قابل حذف نیست."))

    def content(self):
        self.ensure_one()
        self.document_id.check_access("read")
        if self.attachment_id:
            return base64.b64decode(self.attachment_id.sudo().datas or b"")
        return self.document_id.storage_backend_id.download(self.external_path)

    def action_download(self):
        self.ensure_one()
        if self.attachment_id:
            return {"type": "ir.actions.act_url", "url": f"/web/content/{self.attachment_id.id}?download=1", "target": "self"}
        attachment = self.env["ir.attachment"].sudo().create(
            {
                "name": self.filename,
                "datas": base64.b64encode(self.content()),
                "mimetype": self.mimetype,
                "res_model": "cas.document.version",
                "res_id": self.id,
                "company_id": self.company_id.id,
            }
        )
        return {"type": "ir.actions.act_url", "url": f"/web/content/{attachment.id}?download=1", "target": "self"}


class CasDocumentLink(models.Model):
    _name = "cas.document.link"
    _description = "CAS Document Business Link"
    _order = "create_date desc, id desc"

    document_id = fields.Many2one("cas.document", string="سند", required=True, ondelete="restrict", index=True)
    company_id = fields.Many2one(related="document_id.company_id", store=True, index=True)
    source_model = fields.Char(string="مدل منبع", required=True, index=True)
    source_record_id = fields.Integer(string="شناسه منبع", required=True, index=True)
    source_title = fields.Char(string="عنوان منبع", required=True)
    relation_type = fields.Selection(
        [("primary", "سند اصلی"), ("attachment", "پیوست"), ("reference", "مرجع")],
        string="نوع ارتباط",
        required=True,
        default="reference",
    )

    _source_link_uniq = models.Constraint(
        "UNIQUE(document_id, source_model, source_record_id, relation_type)",
        "این ارتباط سند قبلاً ثبت شده است.",
    )
    _source_positive = models.Constraint("CHECK(source_record_id > 0)", "شناسه منبع باید مثبت باشد.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            model = vals.get("source_model")
            record_id = int(vals.get("source_record_id") or 0)
            if model not in self.env or not record_id:
                raise ValidationError(_("منبع ارتباط معتبر نیست."))
            self.env[model].browse(record_id).exists().check_access("read")
        return super().create(vals_list)

    def write(self, vals):
        raise ValidationError(_("ارتباط رسمی سند قابل تغییر نیست؛ ارتباط جدید بسازید."))

    def unlink(self):
        if not self.env.user.has_group("cas_document_core.group_cas_document_manager"):
            raise AccessError(_("فقط مدیر اسناد می‌تواند ارتباط اشتباه را حذف کند."))
        return super().unlink()
