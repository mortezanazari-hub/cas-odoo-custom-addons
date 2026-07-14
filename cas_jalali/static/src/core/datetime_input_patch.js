/** @odoo-module **/

import { useState } from "@odoo/owl";
import { DateTimeInput } from "@web/core/datetime/datetime_input";
import { _t } from "@web/core/l10n/translation";
import { usePopover } from "@web/core/popover/popover_hook";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

import {
    formatJalaliDate,
    formatJalaliDateTime,
    parseJalaliDate,
    parseJalaliDateTime,
} from "@cas_jalali/core/jalali";
import { JalaliPicker } from "@cas_jalali/picker/jalali_picker";

function getSingleValue(value) {
    if (Array.isArray(value)) {
        return value[0] || false;
    }
    return value || false;
}

patch(DateTimeInput.prototype, {
    setup() {
        this.casNotification = useService("notification");
        this.casState = useState({ pickerOpen: false });

        this.casPickerPopover = usePopover(JalaliPicker, {
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
    },

    get casJalaliType() {
        return this.props.type === "date" ? "date" : "datetime";
    },

    get casShowSeconds() {
        // Core technical editors may contain exact day boundaries such as
        // 00:00:00 and 23:59:59. Always preserve them visibly.
        return this.casJalaliType === "datetime";
    },

    get casJalaliDisplayValue() {
        const value = getSingleValue(this.props.value);
        if (!value) {
            return "";
        }
        if (this.casJalaliType === "date") {
            return formatJalaliDate(value);
        }
        return formatJalaliDateTime(value, {
            showDate: true,
            showTime: true,
            showSeconds: this.casShowSeconds,
        });
    },

    casParseValue(value) {
        if (!String(value ?? "").trim()) {
            return false;
        }
        return this.casJalaliType === "date"
            ? parseJalaliDate(value)
            : parseJalaliDateTime(value);
    },

    casPickerProps() {
        return {
            value: getSingleValue(this.props.value),
            type: this.casJalaliType,
            minDate: this.props.minDate || false,
            maxDate: this.props.maxDate || false,
            rounding: this.props.rounding ?? 1,
            showSeconds: this.casShowSeconds,
            showTime: this.casJalaliType === "datetime",
            onApply: (value) => this.casApplyValue(value),
            onClear: () => this.casApplyValue(false),
            onClose: () => this.casClosePicker(),
        };
    },

    onCasJalaliOpen(event) {
        if (this.props.disabled) {
            return;
        }
        event.stopPropagation();
        this.casState.pickerOpen = true;
        this.casPickerPopover.open(
            event.currentTarget,
            this.casPickerProps()
        );
    },

    casClosePicker() {
        this.casState.pickerOpen = false;
        this.casPickerPopover.close();
    },

    async casApplyValue(value) {
        await this.props.onChange?.(value);
        await this.props.onApply?.(value);
        this.casClosePicker();
    },

    async onCasJalaliChange(event) {
        const input = event.currentTarget;
        const previousValue = this.casJalaliDisplayValue;

        try {
            const value = this.casParseValue(input.value);
            await this.props.onChange?.(value);
            await this.props.onApply?.(value);

            input.value = value
                ? (
                    this.casJalaliType === "date"
                        ? formatJalaliDate(value)
                        : formatJalaliDateTime(value, {
                            showDate: true,
                            showTime: true,
                            showSeconds: this.casShowSeconds,
                        })
                )
                : "";
            input.classList.remove("is-invalid");
        } catch (error) {
            input.value = previousValue;
            input.classList.add("is-invalid");
            this.casNotification.add(
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
    },

    onCasJalaliKeydown(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            event.currentTarget.blur();
        } else if (
            event.key === "ArrowDown" &&
            event.altKey
        ) {
            this.onCasJalaliOpen(event);
        } else if (event.key === "Escape") {
            this.casClosePicker();
        }
    },
});
