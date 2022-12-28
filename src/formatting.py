import datetime
from typing import List, Union


def format_job_title(title: str) -> str:
    alnum_title = ""
    for char in title:
        if (char).isalnum() or char in [" ", ",", "'"]: alnum_title += char
    return alnum_title.strip().lower().capitalize()

def format_job_posted_date(date_employer: str) -> datetime.datetime.date:
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



class FormatJobPay:
    @staticmethod
    def format_job_salary_range(salary_raw: str) -> Union[List[float], List[None]]:
        parsing_mode = FormatJobPay._get_salary_parsing_mode(salary_raw)

        output = [None, None]  # Default return type if no salary figures provided.

        if parsing_mode <= 1:
            output = FormatJobPay._get_salary_figures(salary_raw)

        return output

    @staticmethod
    def _get_salary_figures(salary_raw: str):
        money_values = salary_raw.strip()[1 : salary_raw.find(" per")]
        if salary_raw.find("-") != -1:
            output = FormatJobPay._get_salary_range_of_values(money_values)
        else:
            output = FormatJobPay._get_salary_one_value(money_values)

        return output

    @staticmethod
    def _get_salary_range_of_values(money_values: str) -> List[float]:
            cleaned_range = ""
            for char in money_values:
                if char.isnumeric() or char in ["-", "."]: cleaned_range += char
            
            return [float(cleaned_range[0 : cleaned_range.find("-")]),
             float(cleaned_range[cleaned_range.find("-") + 1:])]
    
    @staticmethod
    def _get_salary_one_value(money_values: str) -> List[float]:
        cleaned_value = ""
        for char in money_values:
            if char.isnumeric(): cleaned_value += char
        return [cleaned_value, cleaned_value]

    @staticmethod
    def format_job_salary_type(salary_raw: str) -> str:
        parsing_mode = FormatJobPay._get_salary_parsing_mode(salary_raw)

        if parsing_mode == 0: output = "annual"
        elif parsing_mode == 1: output = "daily"
        elif parsing_mode == 2: output = "competitive"
        elif parsing_mode == 3: output = "negotiable"
        else: output = salary_raw.strip()

        return output
    
    @staticmethod
    def _get_salary_parsing_mode(salary_raw: str):
        if salary_raw.find("annum") != -1: return 0
        if salary_raw.find("day") != -1: return 1
        if salary_raw.find("Competitive") != -1: return 2
        if salary_raw.find("negotiable") != -1: return 3
        return 4

