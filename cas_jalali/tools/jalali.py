"""Jalali/Gregorian conversion helpers.

The implementation uses the well-known break-year method used by common
Jalali conversion implementations. It is kept dependency-free so the addon
does not alter the server Python environment.

Odoo Date/Datetime storage is never changed by this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
import math
import re
from typing import Union


_BREAKS = (
    -61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181,
    1210, 1635, 2060, 2097, 2192, 2262, 2324, 2394,
    2456, 3178,
)

_PERSIAN_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

_JALALI_MONTH_NAMES = (
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند",
)

_WEEKDAY_NAMES = (
    "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه",
    "جمعه", "شنبه", "یکشنبه",
)

_INPUT_DIGITS = str.maketrans(
    "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
    "01234567890123456789",
)


@dataclass(frozen=True, slots=True)
class JalaliDate:
    year: int
    month: int
    day: int


def _div(a: int, b: int) -> int:
    return math.trunc(a / b)


def _mod(a: int, b: int) -> int:
    return a - math.trunc(a / b) * b


def _jal_cal(jy: int) -> dict[str, int]:
    bl = len(_BREAKS)
    gy = jy + 621
    leap_j = -14
    jp = _BREAKS[0]

    if jy < jp or jy >= _BREAKS[-1]:
        raise ValueError(f"Jalali year out of supported range: {jy}")

    jump = 0
    for index in range(1, bl):
        jm = _BREAKS[index]
        jump = jm - jp
        if jy < jm:
            break
        leap_j += _div(jump, 33) * 8 + _div(_mod(jump, 33), 4)
        jp = jm

    n = jy - jp
    leap_j += _div(n, 33) * 8 + _div(_mod(n, 33) + 3, 4)
    if _mod(jump, 33) == 4 and jump - n == 4:
        leap_j += 1

    leap_g = _div(gy, 4) - _div((_div(gy, 100) + 1) * 3, 4) - 150
    march = 20 + leap_j - leap_g

    if jump - n < 6:
        n = n - jump + _div(jump + 4, 33) * 33

    leap = _mod(_mod(n + 1, 33) - 1, 4)
    if leap == -1:
        leap = 4

    return {"leap": leap, "gy": gy, "march": march}


def _g2d(gy: int, gm: int, gd: int) -> int:
    result = (
        _div((gy + _div(gm - 8, 6) + 100100) * 1461, 4)
        + _div(153 * _mod(gm + 9, 12) + 2, 5)
        + gd
        - 34840408
    )
    result = result - _div(_div(gy + 100100 + _div(gm - 8, 6), 100) * 3, 4) + 752
    return result


def _d2g(jdn: int) -> tuple[int, int, int]:
    j = 4 * jdn + 139361631
    j = j + _div(_div(4 * jdn + 183187720, 146097) * 3, 4) * 4 - 3908
    i = _div(_mod(j, 1461), 4) * 5 + 308
    gd = _div(_mod(i, 153), 5) + 1
    gm = _mod(_div(i, 153), 12) + 1
    gy = _div(j, 1461) - 100100 + _div(8 - gm, 6)
    return gy, gm, gd


def _j2d(jy: int, jm: int, jd: int) -> int:
    calibration = _jal_cal(jy)
    return (
        _g2d(calibration["gy"], 3, calibration["march"])
        + (jm - 1) * 31
        - _div(jm, 7) * (jm - 7)
        + jd
        - 1
    )


def _d2j(jdn: int) -> JalaliDate:
    gy, _, _ = _d2g(jdn)
    jy = gy - 621
    calibration = _jal_cal(jy)
    jdn_first_farvardin = _g2d(gy, 3, calibration["march"])
    k = jdn - jdn_first_farvardin

    if k >= 0:
        if k <= 185:
            return JalaliDate(jy, 1 + _div(k, 31), _mod(k, 31) + 1)
        k -= 186
    else:
        jy -= 1
        k += 179
        if calibration["leap"] == 1:
            k += 1

    return JalaliDate(jy, 7 + _div(k, 30), _mod(k, 30) + 1)


def is_jalali_leap(year: int) -> bool:
    return _jal_cal(year)["leap"] == 0


def jalali_month_length(year: int, month: int) -> int:
    if not 1 <= month <= 12:
        raise ValueError("Jalali month must be between 1 and 12")
    if month <= 6:
        return 31
    if month <= 11:
        return 30
    return 30 if is_jalali_leap(year) else 29


def validate_jalali_date(year: int, month: int, day: int) -> None:
    max_day = jalali_month_length(year, month)
    if not 1 <= day <= max_day:
        raise ValueError(
            f"Invalid Jalali day {day} for {year:04d}/{month:02d}; "
            f"maximum is {max_day}"
        )


DateLike = Union[date, datetime]


def to_jalali(value: DateLike) -> JalaliDate:
    if not isinstance(value, (date, datetime)):
        raise TypeError("value must be datetime.date or datetime.datetime")
    return _d2j(_g2d(value.year, value.month, value.day))


def from_jalali(year: int, month: int, day: int) -> date:
    validate_jalali_date(year, month, day)
    gy, gm, gd = _d2g(_j2d(year, month, day))
    return date(gy, gm, gd)


def normalize_digits(value: str) -> str:
    return value.translate(_INPUT_DIGITS).replace("\u200e", "").replace("\u200f", "")


def to_persian_digits(value: str) -> str:
    return value.translate(_PERSIAN_DIGITS)


_DATE_PATTERN = re.compile(
    r"^\s*(?P<year>\d{3,4})\s*[/\-.]\s*"
    r"(?P<month>\d{1,2})\s*[/\-.]\s*"
    r"(?P<day>\d{1,2})\s*$"
)


def parse_jalali_date(value: str) -> date:
    normalized = normalize_digits(value)
    match = _DATE_PATTERN.match(normalized)
    if not match:
        raise ValueError("Expected a Jalali date such as 1405/04/23")
    return from_jalali(
        int(match.group("year")),
        int(match.group("month")),
        int(match.group("day")),
    )


def format_jalali_date(
    value: DateLike | None,
    *,
    persian_digits: bool = True,
) -> str:
    if not value:
        return ""
    jalali = to_jalali(value)
    result = f"{jalali.year:04d}/{jalali.month:02d}/{jalali.day:02d}"
    return to_persian_digits(result) if persian_digits else result


def format_jalali_datetime(
    value: datetime | None,
    *,
    persian_digits: bool = True,
    show_seconds: bool = False,
) -> str:
    if not value:
        return ""
    date_part = format_jalali_date(value, persian_digits=False)
    time_format = "%H:%M:%S" if show_seconds else "%H:%M"
    result = f"{date_part} {value.strftime(time_format)}"
    return to_persian_digits(result) if persian_digits else result


def format_jalali_time(
    value: datetime | None,
    *,
    persian_digits: bool = True,
    show_seconds: bool = False,
) -> str:
    if not value:
        return ""
    time_format = "%H:%M:%S" if show_seconds else "%H:%M"
    result = value.strftime(time_format)
    return to_persian_digits(result) if persian_digits else result


def format_jalali_date_long(
    value: DateLike | None,
    *,
    persian_digits: bool = True,
    include_weekday: bool = False,
) -> str:
    if not value:
        return ""
    jalali = to_jalali(value)
    day = str(jalali.day)
    year = str(jalali.year)
    if persian_digits:
        day = to_persian_digits(day)
        year = to_persian_digits(year)
    result = f"{day} {_JALALI_MONTH_NAMES[jalali.month - 1]} {year}"
    if include_weekday:
        result = f"{_WEEKDAY_NAMES[value.weekday()]} {result}"
    return result


def format_jalali_datetime_long(
    value: datetime | None,
    *,
    persian_digits: bool = True,
    include_weekday: bool = False,
    show_seconds: bool = False,
) -> str:
    if not value:
        return ""
    return (
        f"{format_jalali_date_long(value, persian_digits=persian_digits, include_weekday=include_weekday)}، "
        f"{format_jalali_time(value, persian_digits=persian_digits, show_seconds=show_seconds)}"
    )
