from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError


class CasDocumentOcrProvider(models.Model):
    _name = "cas.document.ocr.provider"
    _description = "CAS OCR Provider"
    _order = "company_id, sequence, name"

    sequence = fields.Integer(default=10)
    name = fields.Char(string="عنوان", required=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one("res.company", string="شرکت", required=True, default=lambda self: self.env.company)
    provider_type = fields.Selection(
        [("manual", "ثبت دستی/بازبینی انسانی"), ("webhook", "سرویس HTTP")],
        string="نوع سرویس",
        required=True,
        default="manual",
    )
    endpoint_url = fields.Char(string="نشانی سرویس")
    secret_parameter_key = fields.Char(string="کلید توکن در تنظیمات سیستم")
    timeout_seconds = fields.Integer(default=60, string="مهلت (ثانیه)")

    @api.constrains("provider_type", "endpoint_url", "timeout_seconds")
    def _check_contract(self):
        for provider in self:
            if provider.timeout_seconds <= 0:
                raise ValidationError(_("مهلت OCR باید مثبت باشد."))
            if provider.provider_type == "webhook" and not provider.endpoint_url:
                raise ValidationError(_("نشانی سرویس OCR الزامی است."))


class CasDocumentOcrJob(models.Model):
    _name = "cas.document.ocr.job"
    _description = "CAS OCR Review Job"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc, id desc"

    version_id = fields.Many2one("cas.document.version", string="نسخه سند", required=True, ondelete="restrict", index=True)
    document_id = fields.Many2one(related="version_id.document_id", store=True, index=True)
    company_id = fields.Many2one(related="version_id.company_id", store=True, index=True)
    provider_id = fields.Many2one("cas.document.ocr.provider", string="سرویس", required=True, ondelete="restrict")
    state = fields.Selection(
        [("queued", "در صف"), ("processing", "در حال پردازش"), ("review", "نیازمند بازبینی"), ("done", "تکمیل"), ("failed", "خطا")],
        string="وضعیت",
        required=True,
        default="queued",
        readonly=True,
        tracking=True,
        index=True,
    )
    extracted_text = fields.Text(string="متن استخراج‌شده")
    reviewer_user_id = fields.Many2one("res.users", string="بازبین", ondelete="restrict")
    attempt_count = fields.Integer(string="تعداد تلاش", readonly=True)
    error_message = fields.Text(string="خطا", readonly=True)
    completed_at = fields.Datetime(string="زمان تکمیل", readonly=True)

    _version_provider_uniq = models.Constraint(
        "UNIQUE(version_id, provider_id)", "برای هر نسخه و سرویس فقط یک کار OCR مجاز است."
    )

    def write(self, vals):
        protected = {"state", "attempt_count", "error_message", "completed_at"}
        if protected.intersection(vals) and not self.env.context.get("cas_document_ocr_engine"):
            raise ValidationError(_("وضعیت OCR فقط از عملیات رسمی تغییر می‌کند."))
        return super().write(vals)

    def action_submit_review(self):
        for job in self:
            if job.provider_id.provider_type != "manual" or job.state not in ("queued", "failed"):
                raise ValidationError(_("این کار OCR قابل ارسال به بازبینی دستی نیست."))
            job.with_context(cas_document_ocr_engine=True).write({"state": "review", "reviewer_user_id": self.env.user.id})
        return True

    def action_confirm_text(self):
        for job in self:
            if job.state != "review" or not str(job.extracted_text or "").strip():
                raise ValidationError(_("متن بازبینی‌شده برای تکمیل OCR الزامی است."))
            if not (
                self.env.is_superuser()
                or job.reviewer_user_id == self.env.user
                or self.env.user.has_group("cas_document_core.group_cas_document_manager")
            ):
                raise AccessError(_("شما بازبین این کار OCR نیستید."))
            # OCR is an internal engine operation. The immutable version model has
            # no public write ACL, so only this narrowly-scoped field update is
            # elevated; the reviewer identity remains the current user in audit.
            job.version_id.sudo().with_context(cas_document_ocr_engine=True).write({"ocr_text": job.extracted_text})
            job.with_context(cas_document_ocr_engine=True).write({"state": "done", "completed_at": fields.Datetime.now()})
            job.document_id._append_event("ocr_completed", version=job.version_id)
        return True

    @api.model
    def _cron_process_webhooks(self):
        jobs = self.sudo().search(
            [("state", "in", ("queued", "failed")), ("provider_id.provider_type", "=", "webhook")],
            limit=20,
        )
        for job in jobs:
            # Provider-specific payload contracts are intentionally explicit extensions.
            # Jobs remain auditable instead of silently guessing an external API schema.
            job.with_context(cas_document_ocr_engine=True).write(
                {
                    "state": "failed",
                    "attempt_count": job.attempt_count + 1,
                    "error_message": _("قرارداد سرویس OCR باید در آداپتر سازمانی پیاده‌سازی شود."),
                }
            )
        return len(jobs)
