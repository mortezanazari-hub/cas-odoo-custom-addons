/** @odoo-module **/

import { Message } from "@mail/core/common/message_model";
import { patch } from "@web/core/utils/patch";

import {
    formatJalaliDateLong,
    formatJalaliDateTimeLong,
    formatJalaliTime,
} from "@cas_jalali/core/jalali";

const { DateTime } = luxon;

patch(Message.prototype, {
    get dateDay() {
        if (this.datetime.hasSame(DateTime.now(), "day")) {
            return "امروز";
        }
        return formatJalaliDateLong(this.datetime);
    },

    get dateSimple() {
        return formatJalaliTime(this.datetime);
    },

    get dateSimpleWithDay() {
        if (this.datetime.hasSame(DateTime.now(), "day")) {
            return formatJalaliTime(this.datetime);
        }

        if (this.datetime.hasSame(DateTime.now().minus({ days: 1 }), "day")) {
            return `دیروز، ${formatJalaliTime(this.datetime)}`;
        }

        return formatJalaliDateTimeLong(this.datetime);
    },

    get datetimeShort() {
        return formatJalaliDateTimeLong(this.datetime, {
            includeWeekday: true,
            showSeconds: true,
        });
    },

    get scheduledDateSimple() {
        if (!this.scheduledDatetime) {
            return "";
        }
        return formatJalaliDateTimeLong(this.scheduledDatetime);
    },
});
