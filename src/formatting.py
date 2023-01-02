import datetime
from typing import List, Union

BASE_URL = "https://reed.co.uk"


def format_job_title(title: str) -> str:
    alnum_title = ""
    for char in title:
        if (char).isalnum() or char in [" ", ",", "'"]: alnum_title += char
    return alnum_title.strip().lower().capitalize()


class FormatJobDatePosted:

    @staticmethod
    def format_job_posted_date(date_employer: str) -> datetime.datetime.date:
        date_value = date_employer[: date_employer.find(" by")].strip()

        temp_date = None
        if date_value.find("days ago") != -1:
            days_ago = int(date_value[:date_value.find(" days")])
            temp_date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).date()
        else:
            temp_date = datetime.datetime.strptime(date_value, "%d %B").date()

        output_date = datetime.datetime(year=FormatJobDatePosted._get_year_value(datetime.datetime.now().date(), temp_date),
        month=temp_date.month, day=temp_date.day).date()

        return output_date

    @staticmethod
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



class FormatJobWorkConditions:

    TENURE_TYPES = ["Permanent", "Contract", "Temporary"]
    WORK_HOUR_TYPES = ["Full or Part-time", "Full-time", "Part-time"]
    REMOTE_STATUS = ["Work From Home", "Unspecified"]

    @staticmethod
    def format_job_location(location_raw: str) -> str:
        return location_raw.strip().capitalize()
    
    @classmethod
    def format_job_tenure_type(cls, tenure_type_raw: str) -> str:
        if tenure_type_raw.find("Permanent") != -1: return FormatJobWorkConditions.TENURE_TYPES[0]
        if tenure_type_raw.find("Contract") != -1: return FormatJobWorkConditions.TENURE_TYPES[1]
        if tenure_type_raw.find("Temporary") != -1: return FormatJobWorkConditions.TENURE_TYPES[2]
        return tenure_type_raw.strip().capitalize()
    
    @classmethod
    def format_job_is_full_time(cls, tenure_type_raw: str) -> str:
        if tenure_type_raw.find("full") and tenure_type_raw.find("part") != -1: return FormatJobWorkConditions.WORK_HOUR_TYPES[0]
        if tenure_type_raw.find("full") != -1: return FormatJobWorkConditions.WORK_HOUR_TYPES[1]
        if tenure_type_raw.find("part") != -1: return FormatJobWorkConditions.WORK_HOUR_TYPES[2]
        return tenure_type_raw.strip().capitalize()
    
    @classmethod
    def format_job_remote_status(cls, remote_status_raw: str) -> str:
        if remote_status_raw.find("from home") != -1: return FormatJobWorkConditions.REMOTE_STATUS[0]
        return FormatJobWorkConditions.REMOTE_STATUS[1]


def format_job_url(raw_url: str) -> str:
    return BASE_URL + raw_url.strip()

