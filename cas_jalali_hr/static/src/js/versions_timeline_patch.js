/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { VersionsTimeline } from "@hr/components/versions_timeline/versions_timeline";

import {
    formatJalaliDate,
    parseJalaliDate,
} from "@cas_jalali/core/jalali";

const { DateTime } = luxon;

function parseISODate(value) {
    if (!value) {
        return false;
    }
    const result = DateTime.fromISO(value);
    return result.isValid ? result : false;
}

function formatTimelineDate(value) {
    const date = parseISODate(value);
    return date ? formatJalaliDate(date) : "";
}

patch(VersionsTimeline.prototype, {
    setup() {
        super.setup(...arguments);
        this.casJalaliNotification = useService("notification");
    },

    async onClickDateTimePickerBtn() {
        const defaultValue = formatJalaliDate(DateTime.local());
        const value = window.prompt(
            "تاریخ شروع نسخه جدید را به شمسی وارد کنید؛ نمونه: ۱۴۰۵/۰۴/۲۳",
            defaultValue
        );
        if (value === null) {
            return;
        }

        try {
            const date = parseJalaliDate(value);
            await this.createVersion(date);
        } catch (error) {
            this.casJalaliNotification.add(
                error?.message || "تاریخ شمسی واردشده معتبر نیست.",
                {
                    title: "خطا در تاریخ شمسی",
                    type: "danger",
                }
            );
        }
    },

    getFieldNames(props) {
        const fieldNames = super.getFieldNames(...arguments);
        if (!fieldNames.includes("date_version")) {
            fieldNames.push("date_version");
        }
        return fieldNames;
    },

    getAllItems() {
        const items = super.getAllItems(...arguments);
        const data = this.specialData?.data || [];
        const dataById = new Map(data.map((record) => [record.id, record]));

        return items.map((item) => {
            const version = dataById.get(item.value) || {};
            const label = version.date_version
                ? formatTimelineDate(version.date_version)
                : item.label;

            let toolTip = item.toolTip;
            if (version.contract_date_start) {
                const contractType =
                    version.contract_type_id?.[1] || _t("Contract");
                const contractEnd = version.contract_date_end
                    ? formatTimelineDate(version.contract_date_end)
                    : _t("Indefinite");
                toolTip =
                    `${contractType}: ` +
                    `${formatTimelineDate(version.contract_date_start)} - ${contractEnd}`;
            }

            return {
                ...item,
                label,
                toolTip,
            };
        });
    },
});
