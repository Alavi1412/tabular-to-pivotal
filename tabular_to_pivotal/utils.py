from datetime import datetime


def sort_shorthands(values):
    cal_values = [v for v in values if v.startswith("Cal")]
    date_values = [v for v in values if not v.startswith("Cal")]

    date_values_sorted = sorted(date_values, key=lambda x: datetime.strptime(x, "%b-%y"))

    sorted_values = date_values_sorted + sorted(cal_values)

    return sorted_values
