/** @odoo-module **/

/**
 * Dependency-free Jalali conversion and formatting helpers.
 *
 * Odoo/Luxon DateTime objects remain Gregorian internally. Only presentation
 * and typed input are converted.
 */

import { ConversionError } from "@web/core/l10n/dates";
import { _t } from "@web/core/l10n/translation";

const { DateTime } = luxon;

const BREAKS = [
    -61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181,
    1210, 1635, 2060, 2097, 2192, 2262, 2324, 2394,
    2456, 3178,
];

const PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹";
const ARABIC_INDIC_DIGITS = "٠١٢٣٤٥٦٧٨٩";

export const JALALI_MONTH_NAMES = [
    "فروردین",
    "اردیبهشت",
    "خرداد",
    "تیر",
    "مرداد",
    "شهریور",
    "مهر",
    "آبان",
    "آذر",
    "دی",
    "بهمن",
    "اسفند",
];

export const JALALI_WEEKDAY_NAMES = [
    { short: "ش", long: "شنبه" },
    { short: "ی", long: "یکشنبه" },
    { short: "د", long: "دوشنبه" },
    { short: "س", long: "سه‌شنبه" },
    { short: "چ", long: "چهارشنبه" },
    { short: "پ", long: "پنجشنبه" },
    { short: "ج", long: "جمعه" },
];

function div(a, b) {
    return Math.trunc(a / b);
}

function mod(a, b) {
    return a - Math.trunc(a / b) * b;
}

function jalCal(jy) {
    const bl = BREAKS.length;
    const gy = jy + 621;
    let leapJ = -14;
    let jp = BREAKS[0];

    if (jy < jp || jy >= BREAKS[bl - 1]) {
        throw new RangeError(`Jalali year out of supported range: ${jy}`);
    }

    let jump = 0;
    for (let i = 1; i < bl; i++) {
        const jm = BREAKS[i];
        jump = jm - jp;
        if (jy < jm) {
            break;
        }
        leapJ += div(jump, 33) * 8 + div(mod(jump, 33), 4);
        jp = jm;
    }

    let n = jy - jp;
    leapJ += div(n, 33) * 8 + div(mod(n, 33) + 3, 4);
    if (mod(jump, 33) === 4 && jump - n === 4) {
        leapJ += 1;
    }

    const leapG = div(gy, 4) - div((div(gy, 100) + 1) * 3, 4) - 150;
    const march = 20 + leapJ - leapG;

    if (jump - n < 6) {
        n = n - jump + div(jump + 4, 33) * 33;
    }

    let leap = mod(mod(n + 1, 33) - 1, 4);
    if (leap === -1) {
        leap = 4;
    }

    return { leap, gy, march };
}

function g2d(gy, gm, gd) {
    let result =
        div((gy + div(gm - 8, 6) + 100100) * 1461, 4) +
        div(153 * mod(gm + 9, 12) + 2, 5) +
        gd -
        34840408;
    result =
        result -
        div(div(gy + 100100 + div(gm - 8, 6), 100) * 3, 4) +
        752;
    return result;
}

function d2g(jdn) {
    let j = 4 * jdn + 139361631;
    j = j + div(div(4 * jdn + 183187720, 146097) * 3, 4) * 4 - 3908;
    const i = div(mod(j, 1461), 4) * 5 + 308;
    const gd = div(mod(i, 153), 5) + 1;
    const gm = mod(div(i, 153), 12) + 1;
    const gy = div(j, 1461) - 100100 + div(8 - gm, 6);
    return { gy, gm, gd };
}

function j2d(jy, jm, jd) {
    const calibration = jalCal(jy);
    return (
        g2d(calibration.gy, 3, calibration.march) +
        (jm - 1) * 31 -
        div(jm, 7) * (jm - 7) +
        jd -
        1
    );
}

function d2j(jdn) {
    const { gy } = d2g(jdn);
    let jy = gy - 621;
    const calibration = jalCal(jy);
    const firstFarvardin = g2d(gy, 3, calibration.march);
    let k = jdn - firstFarvardin;

    if (k >= 0) {
        if (k <= 185) {
            return {
                jy,
                jm: 1 + div(k, 31),
                jd: mod(k, 31) + 1,
            };
        }
        k -= 186;
    } else {
        jy -= 1;
        k += 179;
        if (calibration.leap === 1) {
            k += 1;
        }
    }

    return {
        jy,
        jm: 7 + div(k, 30),
        jd: mod(k, 30) + 1,
    };
}

export function isJalaliLeapYear(year) {
    return jalCal(year).leap === 0;
}

export function jalaliMonthLength(year, month) {
    if (month < 1 || month > 12) {
        throw new RangeError(_t("Jalali month must be between 1 and 12."));
    }
    if (month <= 6) {
        return 31;
    }
    if (month <= 11) {
        return 30;
    }
    return isJalaliLeapYear(year) ? 30 : 29;
}

export function validateJalaliDate(year, month, day) {
    const maxDay = jalaliMonthLength(year, month);
    if (day < 1 || day > maxDay) {
        throw new RangeError(
            _t("The Jalali date is invalid. This month has at most %s days.", maxDay)
        );
    }
}

export function toJalali(gy, gm, gd) {
    return d2j(g2d(gy, gm, gd));
}

export function toGregorian(jy, jm, jd) {
    validateJalaliDate(jy, jm, jd);
    return d2g(j2d(jy, jm, jd));
}

export function jalaliToDateTime(jy, jm, jd, options = {}) {
    const { gy, gm, gd } = toGregorian(jy, jm, jd);
    const result = DateTime.fromObject(
        {
            year: gy,
            month: gm,
            day: gd,
            hour: Number(options.hour || 0),
            minute: Number(options.minute || 0),
            second: Number(options.second || 0),
            millisecond: 0,
        },
        { zone: options.tz || "default" }
    );
    if (!result.isValid) {
        throw new RangeError(_t("The Jalali date or time is invalid."));
    }
    return result;
}

export function todayJalali(options = {}) {
    const now = DateTime.now().setZone(options.tz || "default");
    return toJalali(now.year, now.month, now.day);
}

export function normalizeDigits(value) {
    return String(value ?? "")
        .replace(/[۰-۹]/g, (digit) => String(PERSIAN_DIGITS.indexOf(digit)))
        .replace(/[٠-٩]/g, (digit) => String(ARABIC_INDIC_DIGITS.indexOf(digit)))
        .replace(/[\u200e\u200f\u202a-\u202e\u2066-\u2069]/g, "")
        .trim();
}

export function toPersianDigits(value) {
    return String(value).replace(/\d/g, (digit) => PERSIAN_DIGITS[Number(digit)]);
}

function pad2(value) {
    return String(value).padStart(2, "0");
}

export function formatJalaliDate(value, options = {}) {
    if (!value) {
        return "";
    }
    const { jy, jm, jd } = toJalali(value.year, value.month, value.day);
    const result = `${String(jy).padStart(4, "0")}/${pad2(jm)}/${pad2(jd)}`;
    return options.persianDigits === false ? result : toPersianDigits(result);
}

export function formatJalaliDateTime(value, options = {}) {
    if (!value) {
        return "";
    }

    const localValue = value.setZone(options.tz || "default");
    const showDate = options.showDate !== false;
    const showTime = options.showTime !== false;
    const showSeconds = options.showSeconds === true;

    const parts = [];
    if (showDate) {
        parts.push(formatJalaliDate(localValue, { persianDigits: false }));
    }
    if (showTime) {
        const seconds = showSeconds ? `:${pad2(localValue.second)}` : "";
        parts.push(`${pad2(localValue.hour)}:${pad2(localValue.minute)}${seconds}`);
    }

    let result = parts.join(" ");
    if (options.persianDigits !== false) {
        result = toPersianDigits(result);
    }

    // Persian digits inside an RTL parent can visually exchange the Date and
    // Time runs. LRI/PDI isolates the complete value as one LTR sequence:
    // YYYY/MM/DD HH:mm[:ss]. Parsers remove these controls on typed input.
    if (options.bidiSafe !== false && showDate && showTime) {
        result = `\u2066${result}\u2069`;
    }
    return result;
}

const DATE_RE =
    /^(\d{3,4})\s*[\/\-.]\s*(\d{1,2})\s*[\/\-.]\s*(\d{1,2})$/;

const DATETIME_RE =
    /^(\d{3,4})\s*[\/\-.]\s*(\d{1,2})\s*[\/\-.]\s*(\d{1,2})(?:\s*(?:T|،|,|\s)\s*(\d{1,2})\s*:\s*(\d{1,2})(?:\s*:\s*(\d{1,2}))?)?$/;

function createDateTimeFromJalali(parts, options = {}) {
    const [year, month, day, hour = 0, minute = 0, second = 0] =
        parts.map((part) => Number(part ?? 0));

    validateJalaliDate(year, month, day);

    if (hour < 0 || hour > 23 || minute < 0 || minute > 59 || second < 0 || second > 59) {
        throw new RangeError(_t("The time is invalid."));
    }

    const { gy, gm, gd } = toGregorian(year, month, day);
    const result = DateTime.fromObject(
        {
            year: gy,
            month: gm,
            day: gd,
            hour,
            minute,
            second,
            millisecond: 0,
        },
        { zone: options.tz || "default" }
    );

    if (!result.isValid) {
        throw new RangeError(_t("The Jalali date or time is invalid."));
    }
    return result;
}


export function formatJalaliTime(value, options = {}) {
    if (!value) {
        return "";
    }
    const localValue = value.setZone(options.tz || "default");
    const showSeconds = options.showSeconds === true;
    const seconds = showSeconds ? `:${pad2(localValue.second)}` : "";
    const result = `${pad2(localValue.hour)}:${pad2(localValue.minute)}${seconds}`;
    return options.persianDigits === false ? result : toPersianDigits(result);
}

export function formatJalaliDateLong(value, options = {}) {
    if (!value) {
        return "";
    }
    const localValue = value.setZone(options.tz || "default");
    const { jy, jm, jd } = toJalali(
        localValue.year,
        localValue.month,
        localValue.day
    );
    const dateText =
        `${toPersianDigits(jd)} ${JALALI_MONTH_NAMES[jm - 1]} ` +
        `${toPersianDigits(jy)}`;

    if (options.includeWeekday !== true) {
        return dateText;
    }

    const weekdayIndex = (localValue.weekday + 1) % 7;
    return `${JALALI_WEEKDAY_NAMES[weekdayIndex].long} ${dateText}`;
}

export function formatJalaliDateTimeLong(value, options = {}) {
    if (!value) {
        return "";
    }
    const dateText = formatJalaliDateLong(value, options);
    const timeText = formatJalaliTime(value, {
        ...options,
        showSeconds: options.showSeconds === true,
    });
    return `${dateText}، ${timeText}`;
}

export function parseJalaliDate(value, options = {}) {
    const normalized = normalizeDigits(value);
    if (!normalized) {
        return false;
    }
    try {
        const match = normalized.match(DATE_RE);
        if (!match) {
            throw new Error(_t("Use a Jalali date such as 1405/04/23."));
        }
        return createDateTimeFromJalali(match.slice(1, 4), options).startOf("day");
    } catch (error) {
        throw new ConversionError(
            error?.message || _t("The Jalali date is invalid.")
        );
    }
}

export function parseJalaliDateTime(value, options = {}) {
    const normalized = normalizeDigits(value);
    if (!normalized) {
        return false;
    }
    try {
        const match = normalized.match(DATETIME_RE);
        if (!match) {
            throw new Error(_t("Use a Jalali datetime such as 1405/04/23 09:30."));
        }
        return createDateTimeFromJalali(match.slice(1, 7), options);
    } catch (error) {
        throw new ConversionError(
            error?.message || _t("The Jalali date or time is invalid.")
        );
    }
}
