/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";

import {
    formatJalaliDate,
    formatJalaliDateTime,
    parseJalaliDate,
    parseJalaliDateTime,
} from "@cas_jalali/core/jalali";
import { JalaliPicker } from "@cas_jalali/picker/jalali_picker";

const { DateTime } = luxon;

export class DynamicDateField extends Component {
    static template = "cas_dynamic_form.DynamicDateField";
    static components = { JalaliPicker };
    static props = {
        field: Object,
        value: { optional: true },
        readonly: { type: Boolean, optional: true },
        onChange: Function,
    };
    static defaultProps = { readonly: false };

    setup() {
        this.notification = useService("notification");
        // The picker must not participate in the client action's first render.
        // It is mounted locally and lazily only after the calendar is clicked.
        this.state = useState({ pickerOpen: false });
    }

    get dateTimeValue() {
        if (!this.props.value) {
            return false;
        }
        if (this.props.field.type === "date") {
            const value = DateTime.fromISO(String(this.props.value), { zone: "local" });
            return value.isValid ? value : false;
        }
        const value = DateTime.fromSQL(String(this.props.value), { zone: "utc" }).toLocal();
        return value.isValid ? value : false;
    }

    get displayValue() {
        if (!this.dateTimeValue) {
            return "";
        }
        if (this.props.field.type === "date") {
            return formatJalaliDate(this.dateTimeValue);
        }
        return formatJalaliDateTime(this.dateTimeValue, {
            showDate: true,
            showTime: true,
            showSeconds: false,
        });
    }

    get placeholder() {
        return this.props.field.type === "date"
            ? "۱۴۰۵/۰۴/۲۴"
            : "۱۴۰۵/۰۴/۲۴ ۰۹:۳۰";
    }

    toServerValue(value) {
        if (!value) {
            return null;
        }
        if (this.props.field.type === "date") {
            return value.toISODate();
        }
        return value.toUTC().toFormat("yyyy-MM-dd HH:mm:ss");
    }

    parseInput(value) {
        if (!String(value || "").trim()) {
            return false;
        }
        return this.props.field.type === "date"
            ? parseJalaliDate(value)
            : parseJalaliDateTime(value);
    }

    onBlur(event) {
        try {
            this.props.onChange(this.toServerValue(this.parseInput(event.target.value)));
            event.target.classList.remove("is-invalid");
        } catch (error) {
            event.target.value = this.displayValue;
            event.target.classList.add("is-invalid");
            this.notification.add(
                error?.message || _t("تاریخ شمسی واردشده معتبر نیست."),
                { type: "danger", title: _t("تاریخ نامعتبر") }
            );
        }
    }

    openPicker(event) {
        if (this.props.readonly) {
            return;
        }
        event.preventDefault();
        this.state.pickerOpen = !this.state.pickerOpen;
    }

    applyPickerValue(value) {
        this.props.onChange(this.toServerValue(value));
        this.state.pickerOpen = false;
    }

    clearPickerValue() {
        this.props.onChange(null);
        this.state.pickerOpen = false;
    }

    closePicker() {
        this.state.pickerOpen = false;
    }
}
