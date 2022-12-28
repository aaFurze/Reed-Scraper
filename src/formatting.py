import datetime


def format_job_title(title: str) -> str:
    alnum_title = ""
    for char in title:
        if (char).isalnum() or char in [" ", ",", "'"]: alnum_title += char
    return alnum_title.strip().lower().capitalize()

def format_job_posted_date(date_employer: str):
    date_value = date_employer[: date_employer.find(" by")].strip()

    temp_date = None
    if date_value.find("days ago") != -1:
        days_ago = int(date_value[:date_value.find(" days")])
        temp_date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).date()
    else:
        temp_date = datetime.datetime.strptime(date_value, "%d %B").date()

    output_date = datetime.datetime(year=_get_year_value(datetime.datetime.now().date(), temp_date),
    month=temp_date.month, day=temp_date.day).date()

    return output_date


def _get_year_value(current_date: datetime.datetime.date, other_date: datetime.datetime.date) -> int:
    comparison_date = datetime.datetime(year=current_date.year, month=other_date.month, day=other_date.day).date()
    if comparison_date > current_date:
        return comparison_date.year - 1
    return comparison_date.year