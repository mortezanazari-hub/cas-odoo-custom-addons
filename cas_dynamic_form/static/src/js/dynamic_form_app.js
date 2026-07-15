/** @odoo-module **/

import { Component, onError, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";

import { DynamicReferenceField } from "./dynamic_reference_field";
import { JalaliPicker } from "@cas_jalali/picker/jalali_picker";
import {
    formatJalaliDate,
    formatJalaliDateTime,
    parseJalaliDate,
    parseJalaliDateTime,
} from "@cas_jalali/core/jalali";

const { DateTime } = luxon;

const REFERENCE_TYPES = new Set([
    "user",
    "employee",
    "department",
    "company",
    "record_reference",
]);
const SUPPORTED_INPUT_TYPES = new Set([
    "short_text",
    "long_text",
    "rich_text",
    "integer",
    "decimal",
    "percentage",
    "monetary",
    "boolean",
    "single_select",
    "multi_select",
    "radio",
    "dropdown",
    "tag",
    "date",
    "datetime",
    "time",
    ...REFERENCE_TYPES,
]);

export class DynamicFormApp extends Component {
    static template = "cas_dynamic_form.DynamicFormApp";
    static components = { DynamicReferenceField, JalaliPicker };

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.state = useState({
            loading: true,
            busy: false,
            mode: "catalog",
            catalog: { forms: [], drafts: [], recent: [] },
            runtime: null,
            values: {},
            errors: {},
            dirty: false,
            datePickerFieldKey: false,
        });
        onError((error) => {
            // Keep the complete OWL error visible during browser validation;
            // an RPC can succeed while the following template render fails.
            console.error("CAS Dynamic Form OWL render error", error, error?.cause);
            this.state.busy = false;
            this.notification.add(
                error?.cause?.message || error?.message || _t("نمایش فرم کامل نشد."),
                { type: "danger", title: _t("خطای رابط فرم") }
            );
        });
        onWillStart(() => this.loadInitial());
    }

    async loadInitial() {
        const params = this.props.action?.params || {};
        if (params.submission_id) {
            await this.openSubmission(params.submission_id);
        } else if (params.definition_id) {
            await this.startForm(params.definition_id);
        } else {
            await this.loadCatalog();
        }
        this.state.loading = false;
    }

    async loadCatalog() {
        this.state.loading = true;
        this.state.catalog = await this.orm.call(
            "cas.form.definition",
            "runtime_catalog",
            []
        );
        this.state.mode = "catalog";
        this.state.runtime = null;
        this.state.loading = false;
    }

    async startForm(definitionId) {
        this.state.busy = true;
        try {
            const payload = await this.orm.call(
                "cas.form.definition",
                "runtime_start_submission",
                [[definitionId]]
            );
            this.applyRuntime(payload);
        } catch (error) {
            this.showRpcError(error);
        } finally {
            this.state.busy = false;
        }
    }

    async openSubmission(submissionId) {
        this.state.busy = true;
        try {
            const payload = await this.orm.call(
                "cas.form.submission",
                "runtime_load",
                [[submissionId]]
            );
            this.applyRuntime(payload);
        } catch (error) {
            this.showRpcError(error);
        } finally {
            this.state.busy = false;
        }
    }

    applyRuntime(payload) {
        this.state.runtime = payload;
        const values = {};
        for (const field of payload.schema.fields) {
            if (Object.hasOwn(payload.answers, field.key)) {
                values[field.key] = payload.answers[field.key];
            } else if (field.default !== null && field.default !== undefined) {
                values[field.key] = field.default;
            } else if (field.type === "boolean") {
                values[field.key] = false;
            } else if (field.type === "multi_select") {
                values[field.key] = [];
            } else {
                values[field.key] = null;
            }
        }
        this.state.values = values;
        this.state.errors = {};
        this.state.dirty = false;
        this.state.mode = "form";
    }

    get submission() {
        return this.state.runtime?.submission || {};
    }

    get schema() {
        return this.state.runtime?.schema || { fields: [], layout: [] };
    }

    get fieldByUuid() {
        return Object.fromEntries(this.schema.fields.map((field) => [field.uuid, field]));
    }

    get isReadonly() {
        return this.submission.state !== "draft";
    }

    isSupported(field) {
        return SUPPORTED_INPUT_TYPES.has(field.type);
    }

    isReference(field) {
        return REFERENCE_TYPES.has(field.type);
    }

    fieldReadonly(field) {
        return this.isReadonly || field.readonly || !this.isSupported(field);
    }

    fieldValue(field) {
        return this.state.values[field.key];
    }

    scalarValue(field) {
        const value = this.fieldValue(field);
        if (field.type === "monetary" && value && typeof value === "object") {
            return value.amount ?? "";
        }
        return value ?? "";
    }

    setValue(field, value) {
        if (this.fieldReadonly(field)) {
            return;
        }
        this.state.values[field.key] = value;
        delete this.state.errors[field.key];
        this.state.dirty = true;
    }

    onTextInput(field, event) {
        this.setValue(field, event.target.value);
    }

    onNumberInput(field, event) {
        const raw = event.target.value;
        if (raw === "") {
            this.setValue(field, null);
            return;
        }
        const value = field.type === "integer" ? Number.parseInt(raw, 10) : Number(raw);
        if (field.type === "monetary") {
            const previous = this.fieldValue(field);
            this.setValue(field, {
                amount: value,
                currency_id:
                    previous && typeof previous === "object"
                        ? previous.currency_id
                        : false,
            });
        } else {
            this.setValue(field, value);
        }
    }

    onBooleanToggle(field) {
        this.setValue(field, !Boolean(this.fieldValue(field)));
    }

    onSelectInput(field, event) {
        this.setValue(field, event.target.value || null);
    }

    onMultiToggle(field, optionKey, event) {
        const current = new Set(this.fieldValue(field) || []);
        if (event.target.checked) {
            current.add(optionKey);
        } else {
            current.delete(optionKey);
        }
        this.setValue(field, [...current]);
    }

    dateTimeValue(field) {
        const raw = this.fieldValue(field);
        if (!raw) {
            return false;
        }
        if (field.type === "date") {
            const value = DateTime.fromISO(String(raw), { zone: "local" });
            return value.isValid ? value : false;
        }
        const value = DateTime.fromSQL(String(raw), { zone: "utc" }).toLocal();
        return value.isValid ? value : false;
    }

    dateDisplayValue(field) {
        const value = this.dateTimeValue(field);
        if (!value) {
            return "";
        }
        return field.type === "date"
            ? formatJalaliDate(value)
            : formatJalaliDateTime(value, {
                  showDate: true,
                  showTime: true,
                  showSeconds: false,
              });
    }

    datePlaceholder(field) {
        return field.type === "date" ? "۱۴۰۵/۰۴/۲۴" : "۱۴۰۵/۰۴/۲۴ ۰۹:۳۰";
    }

    onDateBlur(field, event) {
        const raw = String(event.target.value || "").trim();
        if (!raw) {
            this.setValue(field, null);
            event.target.classList.remove("is-invalid");
            return;
        }
        try {
            const value = field.type === "date"
                ? parseJalaliDate(raw)
                : parseJalaliDateTime(raw);
            const serverValue = field.type === "date"
                ? value.toISODate()
                : value.toUTC().toFormat("yyyy-MM-dd HH:mm:ss");
            this.setValue(field, serverValue);
            event.target.value = this.dateDisplayValue(field);
            event.target.classList.remove("is-invalid");
        } catch (error) {
            event.target.value = this.dateDisplayValue(field);
            event.target.classList.add("is-invalid");
            this.notification.add(
                error?.message || _t("تاریخ شمسی واردشده معتبر نیست."),
                { type: "danger", title: _t("تاریخ نامعتبر") }
            );
        }
    }

    get activeDatePickerField() {
        if (!this.state.datePickerFieldKey) {
            return false;
        }
        return this.schema.fields.find(
            (field) => field.key === this.state.datePickerFieldKey
        ) || false;
    }

    get activeDatePickerValue() {
        return this.activeDatePickerField
            ? this.dateTimeValue(this.activeDatePickerField)
            : false;
    }

    get activeDatePickerType() {
        return this.activeDatePickerField?.type || "date";
    }

    openDatePicker(field, event) {
        if (this.fieldReadonly(field)) {
            return;
        }
        event.preventDefault();
        this.state.datePickerFieldKey = field.key;
    }

    closeDatePicker() {
        this.state.datePickerFieldKey = false;
    }

    applyDatePicker(value) {
        const field = this.activeDatePickerField;
        if (!field) {
            return;
        }
        const serverValue = field.type === "date"
            ? value.toISODate()
            : value.toUTC().toFormat("yyyy-MM-dd HH:mm:ss");
        this.setValue(field, serverValue);
        this.closeDatePicker();
    }

    clearDatePicker() {
        const field = this.activeDatePickerField;
        if (field) {
            this.setValue(field, null);
        }
        this.closeDatePicker();
    }

    isOptionSelected(field, optionKey) {
        return (this.fieldValue(field) || []).includes(optionKey);
    }

    isEmpty(field, value) {
        if (field.type === "boolean") {
            return false;
        }
        if (Array.isArray(value)) {
            return value.length === 0;
        }
        if (REFERENCE_TYPES.has(field.type) && value && typeof value === "object") {
            return !value.id;
        }
        return value === null || value === undefined || String(value).trim() === "";
    }

    validate() {
        const errors = {};
        for (const field of this.schema.fields) {
            if (!this.isSupported(field) || field.readonly) {
                continue;
            }
            const value = this.fieldValue(field);
            if (field.required && this.isEmpty(field, value)) {
                errors[field.key] = _t("تکمیل این فیلد الزامی است.");
                continue;
            }
            if (this.isEmpty(field, value)) {
                continue;
            }
            const config = field.validation || {};
            if (["short_text", "long_text", "rich_text"].includes(field.type)) {
                const text = String(value);
                if (config.min_length !== undefined && text.length < Number(config.min_length)) {
                    errors[field.key] = _t("مقدار واردشده کوتاه‌تر از حد مجاز است.");
                } else if (config.max_length !== undefined && text.length > Number(config.max_length)) {
                    errors[field.key] = _t("مقدار واردشده بلندتر از حد مجاز است.");
                } else if (config.regex) {
                    try {
                        if (!new RegExp(`^(?:${config.regex})$`).test(text)) {
                            errors[field.key] = config.error_message || _t("فرمت مقدار معتبر نیست.");
                        }
                    } catch {
                        errors[field.key] = _t("قانون اعتبارسنجی این فیلد معتبر نیست.");
                    }
                }
            }
            if (["integer", "decimal", "percentage", "monetary"].includes(field.type)) {
                const numeric = Number(
                    field.type === "monetary" && typeof value === "object"
                        ? value.amount
                        : value
                );
                if (!Number.isFinite(numeric)) {
                    errors[field.key] = _t("یک عدد معتبر وارد کنید.");
                } else if (config.min !== undefined && numeric < Number(config.min)) {
                    errors[field.key] = _t("مقدار کمتر از حداقل مجاز است.");
                } else if (config.max !== undefined && numeric > Number(config.max)) {
                    errors[field.key] = _t("مقدار بیشتر از حداکثر مجاز است.");
                }
            }
        }
        this.state.errors = errors;
        return Object.keys(errors).length === 0;
    }

    get savePayload() {
        return Object.fromEntries(
            this.schema.fields
                .filter((field) => this.isSupported(field) && !field.readonly)
                .map((field) => {
                    let value = this.fieldValue(field);
                    if (REFERENCE_TYPES.has(field.type) && value && typeof value === "object") {
                        value = value.id;
                    }
                    return [field.key, value];
                })
        );
    }

    get completionPercent() {
        const required = this.schema.fields.filter(
            (field) => field.required && this.isSupported(field) && !field.readonly
        );
        if (!required.length) {
            return 100;
        }
        const completed = required.filter(
            (field) => !this.isEmpty(field, this.fieldValue(field))
        ).length;
        return Math.round((completed / required.length) * 100);
    }

    async saveDraft() {
        if (this.isReadonly) {
            return;
        }
        this.state.busy = true;
        try {
            const payload = await this.orm.call(
                "cas.form.submission",
                "runtime_save",
                [[this.submission.id], this.savePayload]
            );
            this.applyRuntime(payload);
            this.notification.add(_t("پیش‌نویس فرم ذخیره شد."), { type: "success" });
        } catch (error) {
            this.showRpcError(error);
        } finally {
            this.state.busy = false;
        }
    }

    async submitForm() {
        if (!this.validate()) {
            this.notification.add(_t("فیلدهای مشخص‌شده را اصلاح کنید."), {
                type: "warning",
                title: _t("فرم کامل نیست"),
            });
            return;
        }
        this.state.busy = true;
        try {
            const payload = await this.orm.call(
                "cas.form.submission",
                "runtime_submit",
                [[this.submission.id], this.savePayload]
            );
            this.applyRuntime(payload);
            this.notification.add(
                _t("فرم با شماره رهگیری %s ارسال شد.", this.submission.number),
                { type: "success", title: _t("ارسال موفق") }
            );
        } catch (error) {
            this.showRpcError(error);
        } finally {
            this.state.busy = false;
        }
    }

    showRpcError(error) {
        this.notification.add(
            error?.data?.message || error?.message || _t("انجام عملیات با خطا مواجه شد."),
            { type: "danger", title: _t("خطا") }
        );
    }

    openHistory() {
        return this.action.doAction("cas_form_core.action_cas_form_submission");
    }

    nodeGridStyle(node) {
        const columns = Math.min(Math.max(Number(node.columns || 1), 1), 4);
        return `--cas-grid-columns:${columns}`;
    }

    fieldSpanStyle(node) {
        const span = Math.min(Math.max(Number(node.span || 1), 1), 4);
        return `--cas-field-span:${span}`;
    }
}

registry.category("actions").add("cas_dynamic_form.Runtime", DynamicFormApp);
