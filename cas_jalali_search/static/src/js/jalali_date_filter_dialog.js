/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import {
    serializeDate,
    serializeDateTime,
} from "@web/core/l10n/dates";
import { useService } from "@web/core/utils/hooks";

import {
    formatJalaliDate,
    jalaliToDateTime,
    parseJalaliDate,
    toJalali,
} from "@cas_jalali/core/jalali";

const { DateTime } = luxon;

function nextJalaliMonth(year, month) {
    if (month === 12) {
        return { year: year + 1, month: 1 };
    }
    return { year, month: month + 1 };
}

function previousJalaliMonth(year, month) {
    if (month === 1) {
        return { year: year - 1, month: 12 };
    }
    return { year, month: month - 1 };
}

function nextJalaliQuarter(year, startMonth) {
    const nextMonth = startMonth + 3;
    if (nextMonth > 12) {
        return { year: year + 1, month: nextMonth - 12 };
    }
    return { year, month: nextMonth };
}

function previousJalaliQuarter(year, startMonth) {
    const previousMonth = startMonth - 3;
    if (previousMonth < 1) {
        return { year: year - 1, month: previousMonth + 12 };
    }
    return { year, month: previousMonth };
}

function saturdayStart(value) {
    // Luxon weekday: Monday=1 ... Saturday=6, Sunday=7.
    const daysSinceSaturday = (value.weekday + 1) % 7;
    return value.startOf("day").minus({ days: daysSinceSaturday });
}

function jalaliMonthRange(year, month) {
    const start = jalaliToDateTime(year, month, 1).startOf("day");
    const next = nextJalaliMonth(year, month);
    const end = jalaliToDateTime(next.year, next.month, 1)
        .startOf("day")
        .minus({ days: 1 });
    return { start, end };
}

function jalaliQuarterRange(year, startMonth) {
    const start = jalaliToDateTime(year, startMonth, 1).startOf("day");
    const next = nextJalaliQuarter(year, startMonth);
    const end = jalaliToDateTime(next.year, next.month, 1)
        .startOf("day")
        .minus({ days: 1 });
    return { start, end };
}

function jalaliYearRange(year) {
    const start = jalaliToDateTime(year, 1, 1).startOf("day");
    const end = jalaliToDateTime(year + 1, 1, 1)
        .startOf("day")
        .minus({ days: 1 });
    return { start, end };
}

export function getJalaliQuickRange(periodId, reference = DateTime.local()) {
    const today = reference.startOf("day");
    const jalali = toJalali(today.year, today.month, today.day);
    const quarterStartMonth = Math.floor((jalali.jm - 1) / 3) * 3 + 1;

    switch (periodId) {
        case "today":
            return { start: today, end: today };
        case "yesterday": {
            const yesterday = today.minus({ days: 1 });
            return { start: yesterday, end: yesterday };
        }
        case "this_week": {
            const start = saturdayStart(today);
            return { start, end: start.plus({ days: 6 }) };
        }
        case "last_week": {
            const start = saturdayStart(today).minus({ days: 7 });
            return { start, end: start.plus({ days: 6 }) };
        }
        case "this_month":
            return jalaliMonthRange(jalali.jy, jalali.jm);
        case "last_month": {
            const previous = previousJalaliMonth(jalali.jy, jalali.jm);
            return jalaliMonthRange(previous.year, previous.month);
        }
        case "this_quarter":
            return jalaliQuarterRange(jalali.jy, quarterStartMonth);
        case "last_quarter": {
            const previous = previousJalaliQuarter(
                jalali.jy,
                quarterStartMonth
            );
            return jalaliQuarterRange(previous.year, previous.month);
        }
        case "this_year":
            return jalaliYearRange(jalali.jy);
        case "last_year":
            return jalaliYearRange(jalali.jy - 1);
        default:
            return false;
    }
}

export function makeJalaliDomain(field, start, end) {
    const domain = [];

    if (field.type === "date") {
        if (start) {
            domain.push([field.name, ">=", serializeDate(start)]);
        }
        if (end) {
            domain.push([field.name, "<=", serializeDate(end)]);
        }
        return domain;
    }

    if (start) {
        domain.push([
            field.name,
            ">=",
            serializeDateTime(start.startOf("day")),
        ]);
    }
    if (end) {
        domain.push([
            field.name,
            "<",
            serializeDateTime(end.plus({ days: 1 }).startOf("day")),
        ]);
    }
    return domain;
}

export class JalaliDateFilterDialog extends Component {
    static template = "cas_jalali_search.JalaliDateFilterDialog";
    static components = { Dialog };
    static props = {
        close: Function,
        fields: Array,
        onApply: Function,
    };

    setup() {
        this.notification = useService("notification");
        const defaultField = this.props.fields[0];
        const defaultRange = getJalaliQuickRange("this_month");

        this.state = useState({
            fieldName: defaultField?.name || "",
            periodId: "this_month",
            startText: defaultRange
                ? formatJalaliDate(defaultRange.start)
                : "",
            endText: defaultRange
                ? formatJalaliDate(defaultRange.end)
                : "",
        });
    }

    get periodOptions() {
        return [
            { id: "today", label: "امروز" },
            { id: "yesterday", label: "دیروز" },
            { id: "this_week", label: "این هفته؛ شنبه تا جمعه" },
            { id: "last_week", label: "هفته گذشته" },
            { id: "this_month", label: "این ماه شمسی" },
            { id: "last_month", label: "ماه گذشته" },
            { id: "this_quarter", label: "این فصل شمسی" },
            { id: "last_quarter", label: "فصل گذشته" },
            { id: "this_year", label: "امسال" },
            { id: "last_year", label: "سال گذشته" },
            { id: "custom", label: "بازه دلخواه" },
        ];
    }

    get selectedField() {
        return this.props.fields.find(
            (field) => field.name === this.state.fieldName
        );
    }

    get isCustom() {
        return this.state.periodId === "custom";
    }

    onFieldChange(event) {
        this.state.fieldName = event.currentTarget.value;
    }

    onPeriodChange(event) {
        this.state.periodId = event.currentTarget.value;
        if (this.state.periodId === "custom") {
            return;
        }
        const range = getJalaliQuickRange(this.state.periodId);
        this.state.startText = formatJalaliDate(range.start);
        this.state.endText = formatJalaliDate(range.end);
    }

    onStartInput(event) {
        this.state.periodId = "custom";
        this.state.startText = event.currentTarget.value;
    }

    onEndInput(event) {
        this.state.periodId = "custom";
        this.state.endText = event.currentTarget.value;
    }

    get previewText() {
        const field = this.selectedField;
        if (!field) {
            return "";
        }
        const start = this.state.startText || "ابتدا";
        const end = this.state.endText || "انتها";
        return `${field.string}: ${start} تا ${end}`;
    }

    async apply() {
        const field = this.selectedField;
        if (!field) {
            this.notification.add("هیچ فیلد تاریخی در این صفحه انتخاب نشده است.", {
                type: "danger",
            });
            return;
        }

        let start = false;
        let end = false;
        try {
            start = this.state.startText.trim()
                ? parseJalaliDate(this.state.startText)
                : false;
            end = this.state.endText.trim()
                ? parseJalaliDate(this.state.endText)
                : false;
        } catch (error) {
            this.notification.add(
                error?.message || "تاریخ شمسی واردشده معتبر نیست.",
                {
                    title: "خطای تاریخ",
                    type: "danger",
                }
            );
            return;
        }

        if (!start && !end) {
            this.notification.add("حداقل یکی از تاریخ‌های ابتدا یا انتها را وارد کنید.", {
                type: "warning",
            });
            return;
        }

        if (start && end && start > end) {
            this.notification.add("تاریخ ابتدا نباید بعد از تاریخ انتها باشد.", {
                type: "danger",
            });
            return;
        }

        const domainList = makeJalaliDomain(field, start, end);
        const startLabel = start ? formatJalaliDate(start) : "ابتدا";
        const endLabel = end ? formatJalaliDate(end) : "انتها";
        const description = `${field.string}: ${startLabel} تا ${endLabel}`;

        this.props.onApply({
            description,
            domain: JSON.stringify(domainList),
        });
        this.props.close();
    }

    discard() {
        this.props.close();
    }
}
