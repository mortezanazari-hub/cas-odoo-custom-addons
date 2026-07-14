/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { usePopover } from "@web/core/popover/popover_hook";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import {
    DateTimeField,
    dateField,
    dateRangeField,
    dateTimeField,
} from "@web/views/fields/datetime/datetime_field";
import {
    listDateField,
    listDateRangeField,
    listDateTimeField,
} from "@web/views/fields/datetime/list_datetime_field";

import {
    formatJalaliDate,
    formatJalaliDateTime,
    parseJalaliDate,
    parseJalaliDateTime,
} from "@cas_jalali/core/jalali";
import { JalaliPicker } from "@cas_jalali/picker/jalali_picker";

export class JalaliDateTimeField extends Component {
    static template = "cas_jalali.JalaliDateTimeField";
    static props = DateTimeField.props;
    static defaultProps = DateTimeField.defaultProps;

    setup() {
        this.notification = useService("notification");
        this.state = useState({
            activeIndex: 0,
        });

        this.pickerPopover = usePopover(JalaliPicker, {
            animation: false,
            arrow: false,
            closeOnClickAway: true,
            closeOnEscape: true,
            extendedFlipping: true,
            fixedPosition: false,
            popoverClass: "cas_jalali_picker_popover",
            position: "bottom-middle",
            setActiveElement: false,
        });
    }

    get field() {
        return this.props.record.fields[this.props.name];
    }

    get isRange() {
        return Boolean(this.props.startDateField || this.props.endDateField);
    }

    get startFieldName() {
        return this.props.startDateField || this.props.name;
    }

    get endFieldName() {
        return this.props.endDateField || this.props.name;
    }

    get startValue() {
        return this.props.record.data[this.startFieldName];
    }

    get endValue() {
        return this.isRange ? this.props.record.data[this.endFieldName] : false;
    }

    get activeFieldName() {
        return this.isRange && this.state.activeIndex === 1
            ? this.endFieldName
            : this.startFieldName;
    }

    get activeValue() {
        return this.props.record.data[this.activeFieldName];
    }

    get placeholder() {
        return this.field.type === "date"
            ? "۱۴۰۵/۰۴/۲۳"
            : "۱۴۰۵/۰۴/۲۳ ۰۹:۳۰";
    }

    get formattedStart() {
        return this.formatValue(this.startValue);
    }

    get formattedEnd() {
        return this.formatValue(this.endValue);
    }

    formatValue(value) {
        if (!value) {
            return "";
        }
        if (this.field.type === "date") {
            return formatJalaliDate(value);
        }
        return formatJalaliDateTime(value, {
            showDate: true,
            showTime: this.props.showTime !== false,
            showSeconds: this.props.showSeconds === true,
        });
    }

    parseValue(value) {
        if (!String(value).trim()) {
            return false;
        }
        if (this.field.type === "date") {
            return parseJalaliDate(value);
        }
        return parseJalaliDateTime(value);
    }

    getPickerProps() {
        return {
            value: this.activeValue || false,
            type: this.field.type,
            minDate: this.props.minDate || false,
            maxDate: this.props.maxDate || false,
            rounding: this.props.rounding || 5,
            showSeconds: this.props.showSeconds === true,
            showTime: this.props.showTime !== false,
            onApply: (value) => this.applyPickerValue(value),
            onClear: () => this.clearPickerValue(),
            onClose: () => this.closePicker(),
        };
    }

    openPicker(event, valueIndex = 0) {
        event.preventDefault();
        event.stopPropagation();

        this.state.activeIndex = valueIndex;

        const target =
            event.currentTarget.closest(".cas_jalali_input_group") ||
            event.currentTarget;

        this.pickerPopover.open(target, this.getPickerProps());
    }

    closePicker() {
        this.pickerPopover.close();
    }

    async applyPickerValue(value) {
        await this.props.record.update({
            [this.activeFieldName]: value,
        });
        this.closePicker();
    }

    async clearPickerValue() {
        await this.props.record.update({
            [this.activeFieldName]: false,
        });
        this.closePicker();
    }

    async onInputChange(event, valueIndex = 0) {
        const input = event.currentTarget;
        const fieldName =
            this.isRange && valueIndex === 1
                ? this.endFieldName
                : this.startFieldName;
        const previousValue = this.props.record.data[fieldName];

        try {
            const parsedValue = this.parseValue(input.value);
            await this.props.record.update({
                [fieldName]: parsedValue,
            });
            input.value = this.formatValue(parsedValue);
            input.classList.remove("is-invalid");
        } catch (error) {
            input.value = this.formatValue(previousValue);
            input.classList.add("is-invalid");
            this.notification.add(
                error?.message ||
                    _t(
                        "The Jalali date is invalid. Use a value such as 1405/04/23."
                    ),
                {
                    title: _t("Invalid Jalali date"),
                    type: "danger",
                }
            );
        }
    }

    onKeydown(event, valueIndex = 0) {
        if (event.key === "Enter") {
            event.currentTarget.blur();
        } else if (
            event.key === "ArrowDown" &&
            event.altKey
        ) {
            this.openPicker(event, valueIndex);
        } else if (event.key === "Escape") {
            this.closePicker();
        }
    }
}

const fieldRegistry = registry.category("fields");
const formatterRegistry = registry.category("formatters");
const parserRegistry = registry.category("parsers");

const originalDateFormatter = formatterRegistry.get("date");
const originalDateTimeFormatter = formatterRegistry.get("datetime");

function jalaliDateFormatter(value, options = {}) {
    return formatJalaliDate(value, options);
}
jalaliDateFormatter.extractOptions =
    originalDateFormatter.extractOptions;

function jalaliDateTimeFormatter(value, options = {}) {
    return formatJalaliDateTime(value, options);
}
jalaliDateTimeFormatter.extractOptions =
    originalDateTimeFormatter.extractOptions;

formatterRegistry
    .add("date", jalaliDateFormatter, { force: true })
    .add("datetime", jalaliDateTimeFormatter, { force: true });

parserRegistry
    .add("date", parseJalaliDate, { force: true })
    .add("datetime", parseJalaliDateTime, { force: true });

fieldRegistry
    .add(
        "date",
        { ...dateField, component: JalaliDateTimeField },
        { force: true }
    )
    .add(
        "datetime",
        { ...dateTimeField, component: JalaliDateTimeField },
        { force: true }
    )
    .add(
        "daterange",
        { ...dateRangeField, component: JalaliDateTimeField },
        { force: true }
    )
    .add(
        "list.date",
        { ...listDateField, component: JalaliDateTimeField },
        { force: true }
    )
    .add(
        "list.datetime",
        { ...listDateTimeField, component: JalaliDateTimeField },
        { force: true }
    )
    .add(
        "list.daterange",
        { ...listDateRangeField, component: JalaliDateTimeField },
        { force: true }
    );
