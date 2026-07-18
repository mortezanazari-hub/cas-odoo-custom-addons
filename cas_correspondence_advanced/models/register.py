import base64
import hashlib

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CasCorrespondenceRegister(models.Model):
    _name = "cas.correspondence.register"
    _description = "CAS Inbound Outbound Correspondence Register"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "registered_at desc, id desc"
    _rec_name = "number"

    number = fields.Char(string="شماره ثبت", default="New", readonly=True, copy=False, index=True)
    direction = fields.Selection([("inbound", "وارده"), ("outbound", "صادره")], required=True, tracking=True, index=True)
    subject = fields.Char(string="موضوع", required=True, tracking=True, index=True)
    company_id = fields.Many2one("res.company", string="شرکت", required=True, default=lambda self: self.env.company, index=True)
    owner_user_id = fields.Many2one("res.users", string="مسئول", required=True, default=lambda self: self.env.user, ondelete="restrict")
    counterparty = fields.Char(string="فرستنده/گیرنده بیرونی", required=True)
    external_number = fields.Char(string="شماره بیرونی", index=True)
    external_date = fields.Date(string="تاریخ بیرونی")
    channel = fields.Selection(
        [("physical", "فیزیکی"), ("email", "ایمیل"), ("portal", "درگاه"), ("fax", "نمابر"), ("other", "سایر")],
        required=True, default="physical",
    )
    confidentiality = fields.Selection(
        [("normal", "عادی"), ("confidential", "محرمانه"), ("highly_confidential", "خیلی محرمانه")],
        required=True, default="normal", tracking=True,
    )
    note = fields.Html(string="شرح", sanitize=True)
    attachment_id = fields.Many2one("ir.attachment", string="فایل اصلی", ondelete="restrict")
    file_data = fields.Binary(string="بارگذاری فایل", attachment=True)
    file_name = fields.Char(string="نام فایل")
    document_folder_id = fields.Many2one("cas.document.folder", string="پوشه اسناد", ondelete="restrict")
    document_id = fields.Many2one("cas.document", string="سند نسخه‌دار", readonly=True, copy=False, ondelete="restrict")
    current_sha256 = fields.Char(related="document_id.current_sha256", readonly=True)
    state = fields.Selection(
        [("draft", "پیش‌نویس"), ("registered", "ثبت‌شده"), ("closed", "مختومه"), ("cancelled", "باطل‌شده")],
        required=True, default="draft", readonly=True, tracking=True, index=True,
    )
    registered_at = fields.Datetime(readonly=True, index=True)
    closed_at = fields.Datetime(readonly=True)
    signature_ids = fields.One2many("cas.correspondence.signature", "register_id", string="امضاها", copy=False)
    event_ids = fields.One2many("cas.correspondence.register.event", "register_id", string="تاریخچه", copy=False)

    _number_company_uniq = models.Constraint("UNIQUE(number, company_id)", "شماره ثبت در هر شرکت باید یکتا باشد.")

    @api.constrains("company_id", "owner_user_id", "document_folder_id", "attachment_id")
    def _check_contract(self):
        for record in self:
            if record.company_id not in record.owner_user_id.company_ids:
                raise ValidationError("مسئول باید عضو همان شرکت باشد.")
            if record.document_folder_id and record.document_folder_id.company_id != record.company_id:
                raise ValidationError("پوشه و مکاتبه باید متعلق به یک شرکت باشند.")
            if record.attachment_id.company_id and record.attachment_id.company_id != record.company_id:
                raise ValidationError("فایل و مکاتبه باید متعلق به یک شرکت باشند.")

    def write(self, vals):
        protected = {"number", "state", "registered_at", "closed_at", "document_id"}
        if protected.intersection(vals) and not self.env.context.get("cas_correspondence_advanced_engine"):
            raise ValidationError("فیلدهای ثبتی فقط از عملیات رسمی تغییر می‌کنند.")
        return super().write(vals)

    def unlink(self):
        if any(record.state != "draft" for record in self):
            raise ValidationError("مکاتبه ثبت‌شده قابل حذف نیست.")
        return super().unlink()

    def _folder(self):
        self.ensure_one()
        folder = self.document_folder_id
        if not folder:
            folder = self.env["cas.document.folder"].sudo().search(
                [("company_id", "=", self.company_id.id), ("code", "=", "CORRESPONDENCE")], limit=1
            )
        if not folder:
            folder = self.env["cas.document.folder"].sudo().create({
                "name": _("مکاتبات رسمی"), "code": "CORRESPONDENCE", "company_id": self.company_id.id,
                "manager_user_id": self.owner_user_id.id,
            })
        return folder

    def _append_event(self, event_type, note=False, digest=False):
        return self.env["cas.correspondence.register.event"].sudo().with_context(
            cas_correspondence_advanced_engine=True
        ).create({
            "register_id": self.id, "event_type": event_type, "actor_user_id": self.env.user.id,
            "note": note or False, "digest": digest or False,
        })

    def action_register(self):
        for record in self:
            if record.state != "draft" or (not record.attachment_id and not record.file_data):
                raise ValidationError("ثبت رسمی فقط برای پیش‌نویس دارای فایل اصلی ممکن است.")
            if not record.attachment_id:
                attachment = self.env["ir.attachment"].sudo().create({
                    "name": record.file_name or "correspondence.bin", "datas": record.file_data,
                    "res_model": record._name, "res_id": record.id, "company_id": record.company_id.id,
                })
                record.attachment_id = attachment
            number = self.env["ir.sequence"].with_company(record.company_id).next_by_code(
                f"cas.correspondence.{record.direction}"
            ) or "New"
            content = base64.b64decode(record.attachment_id.sudo().datas or b"")
            if not content:
                raise ValidationError("فایل اصلی خالی است.")
            document = self.env["cas.document"].create({
                "name": record.subject, "company_id": record.company_id.id, "folder_id": record._folder().id,
                "owner_user_id": record.owner_user_id.id, "authorized_user_ids": [(6, 0, [record.owner_user_id.id])],
                "confidentiality": record.confidentiality,
            })
            version = document.add_version(record.attachment_id.name, content, record.attachment_id.mimetype, _("ثبت دبیرخانه %s", number))
            self.env["cas.document.link"].create({
                "document_id": document.id, "source_model": record._name, "source_record_id": record.id,
                "source_title": record.subject, "relation_type": "primary",
            })
            record.with_context(cas_correspondence_advanced_engine=True).write({
                "number": number, "state": "registered", "registered_at": fields.Datetime.now(), "document_id": document.id,
            })
            record._append_event("registered", digest=version.sha256)
        return True

    def action_close(self):
        for record in self:
            if record.state != "registered":
                raise ValidationError("فقط مکاتبه ثبت‌شده قابل اختتام است.")
            record.with_context(cas_correspondence_advanced_engine=True).write({"state": "closed", "closed_at": fields.Datetime.now()})
            record._append_event("closed")
        return True


class CasCorrespondenceRegisterEvent(models.Model):
    _name = "cas.correspondence.register.event"
    _description = "CAS Immutable Correspondence Register Event"
    _order = "event_at, id"

    register_id = fields.Many2one("cas.correspondence.register", required=True, ondelete="restrict", index=True)
    company_id = fields.Many2one(related="register_id.company_id", store=True, index=True)
    event_type = fields.Selection([("registered", "ثبت رسمی"), ("closed", "اختتام"), ("signed", "امضا")], required=True)
    actor_user_id = fields.Many2one("res.users", required=True, ondelete="restrict")
    event_at = fields.Datetime(required=True, default=fields.Datetime.now, readonly=True)
    note = fields.Text(readonly=True)
    digest = fields.Char(readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.context.get("cas_correspondence_advanced_engine"):
            raise AccessError("رویداد فقط توسط موتور رسمی ثبت می‌شود.")
        return super().create(vals_list)

    def write(self, vals):
        raise ValidationError("رویداد رسمی تغییرپذیر نیست.")

    def unlink(self):
        raise ValidationError("رویداد رسمی حذف‌پذیر نیست.")
