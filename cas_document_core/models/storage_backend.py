from __future__ import annotations

import posixpath
from urllib.parse import quote

import requests

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError


class CasDocumentStorageBackend(models.Model):
    _name = "cas.document.storage.backend"
    _description = "CAS Document Storage Backend"
    _inherit = ["mail.thread"]
    _order = "company_id, sequence, name"

    sequence = fields.Integer(default=10)
    name = fields.Char(string="عنوان", required=True, tracking=True)
    active = fields.Boolean(default=True, tracking=True)
    company_id = fields.Many2one(
        "res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True
    )
    backend_type = fields.Selection(
        [("database", "پایگاه داده Odoo"), ("nextcloud", "Nextcloud WebDAV")],
        string="نوع ذخیره‌سازی",
        required=True,
        default="database",
        tracking=True,
    )
    base_url = fields.Char(string="نشانی Nextcloud")
    root_path = fields.Char(string="مسیر ریشه", default="CAS")
    username = fields.Char(string="نام کاربری")
    secret_parameter_key = fields.Char(
        string="کلید رمز در تنظیمات سیستم",
        help="رمز در این رکورد ذخیره نمی‌شود؛ مقدار آن باید در ir.config_parameter ثبت شود.",
    )
    timeout_seconds = fields.Integer(string="مهلت اتصال (ثانیه)", default=30)
    verify_ssl = fields.Boolean(string="اعتبارسنجی SSL", default=True)
    is_default = fields.Boolean(string="پیش‌فرض شرکت", default=False, tracking=True)
    document_ids = fields.One2many("cas.document", "storage_backend_id", string="اسناد", readonly=True)

    @api.constrains(
        "backend_type", "base_url", "root_path", "username", "secret_parameter_key", "timeout_seconds", "is_default", "company_id"
    )
    def _check_contract(self):
        for backend in self:
            if backend.timeout_seconds <= 0:
                raise ValidationError(_("مهلت اتصال باید مثبت باشد."))
            if backend.backend_type == "nextcloud":
                if not all((backend.base_url, backend.root_path, backend.username, backend.secret_parameter_key)):
                    raise ValidationError(_("برای Nextcloud نشانی، مسیر، نام کاربری و کلید رمز الزامی است."))
                if not backend.base_url.startswith(("https://", "http://")):
                    raise ValidationError(_("نشانی Nextcloud باید با http یا https شروع شود."))
            if backend.is_default:
                duplicate = self.search_count(
                    [("id", "!=", backend.id), ("company_id", "=", backend.company_id.id), ("is_default", "=", True)]
                )
                if duplicate:
                    raise ValidationError(_("برای هر شرکت فقط یک ذخیره‌ساز پیش‌فرض مجاز است."))

    def _credential(self):
        self.ensure_one()
        if self.backend_type != "nextcloud":
            return False
        secret = self.env["ir.config_parameter"].sudo().get_param(self.secret_parameter_key)
        if not secret:
            raise UserError(_("رمز Nextcloud در تنظیمات سیستم ثبت نشده است."))
        return secret

    def _remote_url(self, relative_path):
        self.ensure_one()
        clean = posixpath.normpath(str(relative_path or "").replace("\\", "/")).lstrip("/")
        if clean.startswith("../") or clean == "..":
            raise ValidationError(_("مسیر سند نامعتبر است."))
        base = self.base_url.rstrip("/")
        segments = ["remote.php", "dav", "files", self.username, self.root_path.strip("/"), clean]
        return base + "/" + "/".join(quote(part, safe="") for part in segments if part)

    def _request(self, method, relative_path="", data=None, headers=None, expected=(200, 201, 204, 207)):
        self.ensure_one()
        if self.backend_type != "nextcloud":
            raise ValidationError(_("این عملیات فقط برای Nextcloud معتبر است."))
        try:
            response = requests.request(
                method,
                self._remote_url(relative_path),
                data=data,
                headers=headers or {},
                auth=(self.username, self._credential()),
                timeout=self.timeout_seconds,
                verify=self.verify_ssl,
            )
        except requests.RequestException as error:
            raise UserError(_("ارتباط با Nextcloud ناموفق بود: %s", error)) from error
        if response.status_code not in expected:
            raise UserError(_("Nextcloud پاسخ نامعتبر %s برگرداند.", response.status_code))
        return response

    def _ensure_remote_folder(self, relative_folder):
        self.ensure_one()
        current = ""
        for segment in str(relative_folder or "").replace("\\", "/").split("/"):
            if not segment:
                continue
            current = posixpath.join(current, segment)
            self._request("MKCOL", current, expected=(201, 405))

    def upload(self, relative_path, content, mimetype="application/octet-stream"):
        self.ensure_one()
        if self.backend_type == "database":
            raise ValidationError(_("ذخیره پایگاه داده از طریق Attachment انجام می‌شود."))
        folder = posixpath.dirname(relative_path)
        self._ensure_remote_folder(folder)
        self._request("PUT", relative_path, data=content, headers={"Content-Type": mimetype}, expected=(200, 201, 204))
        return relative_path

    def download(self, relative_path):
        self.ensure_one()
        if not self.env.user.has_group("cas_document_core.group_cas_document_user"):
            raise AccessError(_("مجوز دریافت سند را ندارید."))
        return self._request("GET", relative_path, expected=(200,)).content

    def action_test_connection(self):
        for backend in self:
            if backend.backend_type == "database":
                continue
            backend._request("PROPFIND", "", headers={"Depth": "0"}, expected=(207,))
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {"title": _("ذخیره‌سازی"), "message": _("اتصال با موفقیت بررسی شد."), "type": "success"},
        }

    @api.model
    def default_for_company(self, company):
        backend = self.search([("company_id", "=", company.id), ("is_default", "=", True), ("active", "=", True)], limit=1)
        if backend:
            return backend
        return self.search([("company_id", "=", company.id), ("backend_type", "=", "database"), ("active", "=", True)], limit=1)
