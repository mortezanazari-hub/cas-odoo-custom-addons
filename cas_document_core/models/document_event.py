from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CasDocumentEvent(models.Model):
    _name = "cas.document.event"
    _description = "CAS Document Append-only Event"
    _order = "event_at desc, id desc"

    document_id = fields.Many2one("cas.document", string="سند", required=True, ondelete="restrict", index=True)
    company_id = fields.Many2one(related="document_id.company_id", store=True, index=True)
    version_id = fields.Many2one("cas.document.version", string="نسخه", ondelete="restrict")
    event_type = fields.Selection(
        [
            ("created", "ایجاد"),
            ("metadata_updated", "تغییر متادیتا"),
            ("version_added", "نسخه جدید"),
            ("activated", "فعال‌سازی"),
            ("archived", "بایگانی"),
            ("destroyed", "ثبت امحا"),
            ("ocr_completed", "تکمیل OCR"),
            ("linked", "اتصال به رکورد"),
        ],
        string="رویداد",
        required=True,
        readonly=True,
        index=True,
    )
    actor_user_id = fields.Many2one("res.users", string="اقدام‌کننده", required=True, readonly=True, ondelete="restrict")
    event_at = fields.Datetime(string="زمان", required=True, default=fields.Datetime.now, readonly=True, index=True)
    note = fields.Text(string="توضیح", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.context.get("cas_document_engine"):
            raise AccessError(_("رویداد سند فقط توسط موتور ثبت می‌شود."))
        return super().create(vals_list)

    def write(self, vals):
        raise ValidationError(_("تاریخچه رسمی سند قابل تغییر نیست."))

    def unlink(self):
        raise ValidationError(_("تاریخچه رسمی سند قابل حذف نیست."))
