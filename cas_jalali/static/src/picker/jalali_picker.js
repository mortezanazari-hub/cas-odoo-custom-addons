/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";

import {
    JALALI_MONTH_NAMES,
    JALALI_WEEKDAY_NAMES,
    formatJalaliDate,
    jalaliMonthLength,
    jalaliToDateTime,
    toJalali,
    toPersianDigits,
} from "@cas_jalali/core/jalali";

const { DateTime } = luxon;

function clampNumber(value, min, max) {
    return Math.min(max, Math.max(min, Number(value)));
}

function getInitialTime(value) {
    const current = value || DateTime.local();
    return {
        hour: current.hour,
        minute: current.minute,
        second: current.second,
    };
}

function saturdayFirstIndex(dateTime) {
    // Luxon: Monday=1 ... Saturday=6, Sunday=7
    return (dateTime.weekday + 1) % 7;
}

export class JalaliPicker extends Component {
    static template = "cas_jalali.JalaliPicker";
    static props = {
        value: { type: [DateTime, { value: false }, { value: null }], optional: true },
        type: { type: [{ value: "date" }, { value: "datetime" }] },
        minDate: { type: [String, { value: false }, { value: null }], optional: true },
        maxDate: { type: [String, { value: false }, { value: null }], optional: true },
        rounding: { type: Number, optional: true },
        showSeconds: { type: Boolean, optional: true },
        showTime: { type: Boolean, optional: true },
        onApply: Function,
        onClear: Function,
        onClose: Function,
    };
    static defaultProps = {
        rounding: 5,
        showSeconds: false,
        showTime: true,
        value: false,
        minDate: false,
        maxDate: false,
    };

    setup() {
        const base = this.props.value || DateTime.local();
        const jalali = toJalali(base.year, base.month, base.day);
        const time = getInitialTime(this.props.value);

        this.state = useState({
            viewMode: "days",
            viewYear: jalali.jy,
            viewMonth: jalali.jm,
            selectedYear: jalali.jy,
            selectedMonth: jalali.jm,
            selectedDay: jalali.jd,
            hour: time.hour,
            minute: time.minute,
            second: time.second,
            yearPageStart: Math.floor(jalali.jy / 12) * 12,
        });
    }

    get monthNames() {
        return JALALI_MONTH_NAMES;
    }

    get weekdays() {
        return JALALI_WEEKDAY_NAMES;
    }

    get title() {
        if (this.state.viewMode === "days") {
            return `${this.monthNames[this.state.viewMonth - 1]} ${toPersianDigits(
                this.state.viewYear
            )}`;
        }
        if (this.state.viewMode === "months") {
            return toPersianDigits(this.state.viewYear);
        }
        return `${toPersianDigits(this.state.yearPageStart)} تا ${toPersianDigits(
            this.state.yearPageStart + 11
        )}`;
    }

    get minuteStep() {
        const rounding = Number(this.props.rounding);
        return rounding > 0 && rounding <= 60 ? rounding : 1;
    }

    get hourOptions() {
        return Array.from({ length: 24 }, (_, value) => ({
            value,
            label: toPersianDigits(String(value).padStart(2, "0")),
        }));
    }

    get minuteOptions() {
        const values = [];
        for (let value = 0; value < 60; value += this.minuteStep) {
            values.push({
                value,
                label: toPersianDigits(String(value).padStart(2, "0")),
            });
        }
        if (!values.some((item) => item.value === this.state.minute)) {
            values.push({
                value: this.state.minute,
                label: toPersianDigits(String(this.state.minute).padStart(2, "0")),
            });
            values.sort((a, b) => a.value - b.value);
        }
        return values;
    }

    get secondOptions() {
        return Array.from({ length: 60 }, (_, value) => ({
            value,
            label: toPersianDigits(String(value).padStart(2, "0")),
        }));
    }

    get years() {
        return Array.from({ length: 12 }, (_, index) => {
            const year = this.state.yearPageStart + index;
            return {
                year,
                label: toPersianDigits(year),
                selected: year === this.state.viewYear,
            };
        });
    }

    get months() {
        return this.monthNames.map((name, index) => ({
            month: index + 1,
            name,
            selected: index + 1 === this.state.viewMonth,
        }));
    }

    get calendarDays() {
        const firstGregorian = jalaliToDateTime(
            this.state.viewYear,
            this.state.viewMonth,
            1
        );
        const leading = saturdayFirstIndex(firstGregorian);
        const currentLength = jalaliMonthLength(
            this.state.viewYear,
            this.state.viewMonth
        );

        let prevYear = this.state.viewYear;
        let prevMonth = this.state.viewMonth - 1;
        if (prevMonth < 1) {
            prevMonth = 12;
            prevYear -= 1;
        }
        const previousLength = jalaliMonthLength(prevYear, prevMonth);

        const today = DateTime.local();
        const todayJalali = toJalali(today.year, today.month, today.day);
        const days = [];

        for (let cell = 0; cell < 42; cell++) {
            let year = this.state.viewYear;
            let month = this.state.viewMonth;
            let day = cell - leading + 1;
            let inCurrentMonth = true;

            if (day <= 0) {
                year = prevYear;
                month = prevMonth;
                day = previousLength + day;
                inCurrentMonth = false;
            } else if (day > currentLength) {
                day -= currentLength;
                month += 1;
                if (month > 12) {
                    month = 1;
                    year += 1;
                }
                inCurrentMonth = false;
            }

            const dateTime = jalaliToDateTime(year, month, day);
            days.push({
                key: `${year}-${month}-${day}`,
                year,
                month,
                day,
                label: toPersianDigits(day),
                inCurrentMonth,
                isToday:
                    year === todayJalali.jy &&
                    month === todayJalali.jm &&
                    day === todayJalali.jd,
                isSelected:
                    year === this.state.selectedYear &&
                    month === this.state.selectedMonth &&
                    day === this.state.selectedDay,
                disabled: !this.isAllowed(dateTime),
            });
        }
        return days;
    }

    parseLimit(value, endOfDay = false) {
        if (!value) {
            return false;
        }
        const result =
            value === "today"
                ? DateTime.local()
                : DateTime.fromISO(String(value), { zone: "default" });
        if (!result.isValid) {
            return false;
        }
        return endOfDay ? result.endOf("day") : result.startOf("day");
    }

    isAllowed(value) {
        const minDate = this.parseLimit(this.props.minDate);
        const maxDate = this.parseLimit(this.props.maxDate, true);
        return (!minDate || value >= minDate) && (!maxDate || value <= maxDate);
    }

    previous() {
        if (this.state.viewMode === "days") {
            this.changeMonth(-1);
        } else if (this.state.viewMode === "months") {
            this.state.viewYear -= 1;
        } else {
            this.state.yearPageStart -= 12;
        }
    }

    next() {
        if (this.state.viewMode === "days") {
            this.changeMonth(1);
        } else if (this.state.viewMode === "months") {
            this.state.viewYear += 1;
        } else {
            this.state.yearPageStart += 12;
        }
    }

    changeMonth(delta) {
        let month = this.state.viewMonth + delta;
        let year = this.state.viewYear;
        if (month < 1) {
            month = 12;
            year -= 1;
        } else if (month > 12) {
            month = 1;
            year += 1;
        }
        this.state.viewMonth = month;
        this.state.viewYear = year;
    }

    openHigherView() {
        if (this.state.viewMode === "days") {
            this.state.viewMode = "months";
        } else if (this.state.viewMode === "months") {
            this.state.yearPageStart = Math.floor(this.state.viewYear / 12) * 12;
            this.state.viewMode = "years";
        }
    }

    selectYear(year) {
        this.state.viewYear = year;
        this.state.viewMode = "months";
    }

    selectMonth(month) {
        this.state.viewMonth = month;
        this.state.viewMode = "days";
    }

    async selectDay(item) {
        if (item.disabled) {
            return;
        }
        this.state.selectedYear = item.year;
        this.state.selectedMonth = item.month;
        this.state.selectedDay = item.day;
        this.state.viewYear = item.year;
        this.state.viewMonth = item.month;

        if (this.props.type === "date" || this.props.showTime === false) {
            await this.apply();
        }
    }

    setHour(event) {
        this.state.hour = clampNumber(event.currentTarget.value, 0, 23);
    }

    setMinute(event) {
        this.state.minute = clampNumber(event.currentTarget.value, 0, 59);
    }

    setSecond(event) {
        this.state.second = clampNumber(event.currentTarget.value, 0, 59);
    }

    async apply() {
        const value = jalaliToDateTime(
            this.state.selectedYear,
            this.state.selectedMonth,
            this.state.selectedDay,
            {
                hour:
                    this.props.type === "datetime" && this.props.showTime !== false
                        ? this.state.hour
                        : 0,
                minute:
                    this.props.type === "datetime" && this.props.showTime !== false
                        ? this.state.minute
                        : 0,
                second:
                    this.props.type === "datetime" &&
                    this.props.showTime !== false &&
                    this.props.showSeconds
                        ? this.state.second
                        : 0,
            }
        );
        if (!this.isAllowed(value)) {
            return;
        }
        await this.props.onApply(value);
    }

    async today() {
        const now = DateTime.local();
        const jalali = toJalali(now.year, now.month, now.day);
        this.state.viewYear = jalali.jy;
        this.state.viewMonth = jalali.jm;
        this.state.selectedYear = jalali.jy;
        this.state.selectedMonth = jalali.jm;
        this.state.selectedDay = jalali.jd;
        this.state.hour = now.hour;
        this.state.minute = now.minute;
        this.state.second = now.second;
        this.state.viewMode = "days";

        if (this.props.type === "date" || this.props.showTime === false) {
            await this.apply();
        }
    }

    selectedLabel() {
        const selected = jalaliToDateTime(
            this.state.selectedYear,
            this.state.selectedMonth,
            this.state.selectedDay,
            {
                hour: this.state.hour,
                minute: this.state.minute,
                second: this.state.second,
            }
        );
        return formatJalaliDate(selected);
    }
}
