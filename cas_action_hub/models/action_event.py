from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CasActionEvent(models.Model):
    _name = "cas.action.event"
    _description = "CAS Action Hub Append-only Event"
    _order = "event_at desc, id desc"

    item_id = fields.Many2one(
        "cas.action.item", string="اقدام", required=True, ondelete="restrict", index=True
    )
    company_id = fields.Many2one(
        related="item_id.company_id", string="شرکت", store=True, index=True
    )
    event_type = fields.Selection(
        [
            ("published", "انتشار"),
            ("updated", "به‌روزرسانی"),
            ("opened", "بازکردن منبع"),
            ("completed", "تکمیل"),
            ("cancelled", "لغو"),
            ("reminded", "یادآوری"),
            ("escalated", "تصعید"),
            ("access_denied", "رد دسترسی"),
        ],
        string="رویداد",
        required=True,
        readonly=True,
        index=True,
    )
    actor_user_id = fields.Many2one(
        "res.users", string="اقدام‌کننده", required=True, readonly=True, ondelete="restrict"
    )
    event_at = fields.Datetime(
        string="زمان رویداد", required=True, default=fields.Datetime.now, readonly=True, index=True
    )
    note = fields.Text(string="توضیح", readonly=True)
    snapshot = fields.Json(string="تصویر متادیتا", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.context.get("cas_action_hub_engine"):
            raise AccessError(_("رویداد کارتابل فقط توسط موتور ثبت می‌شود."))
        return super().create(vals_list)

    def write(self, vals):
        raise ValidationError(_("رویداد رسمی کارتابل قابل تغییر نیست."))

    def unlink(self):
        raise ValidationError(_("رویداد رسمی کارتابل قابل حذف نیست."))
