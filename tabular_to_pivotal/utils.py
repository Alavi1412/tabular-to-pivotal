import calendar
import re
from datetime import datetime


def sort_shorthands(values):
    cal_values = [v for v in values if v.startswith("Cal")]
    date_values = [v for v in values if not v.startswith("Cal")]

    date_values_sorted = sorted(date_values, key=lambda x: datetime.strptime(x, "%b-%y"))

    sorted_values = date_values_sorted + sorted(cal_values)

    return sorted_values


def validate_shorthand(value: str):
    if re.match(r"^Cal-\d{2}$", value):
        return value
    try:
        datetime.strptime(value, "%b-%y")
    except ValueError:
        raise ValueError("Shorthand must be in the format Mon-YY or Cal-YY")
    return value


def generate_start_and_end_from_shorthand(shorthand: str):
    if shorthand.startswith("Cal"):
        year = int(shorthand.split("-")[1]) + 2000
        start = datetime(year, 1, 1)
        end = datetime(year, 12, 31)
    else:
        end = datetime.strptime(shorthand, "%b-%y")
        last_day = calendar.monthrange(end.year, end.month)[1]
        end = end.replace(day=last_day)
        start = datetime(end.year, end.month, 1)
    date_format = "%d-%m-%Y"
    return start.strftime(date_format), end.strftime(date_format)
