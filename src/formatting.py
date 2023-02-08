from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import List, Union

from typing_extensions import Protocol

BASE_URL = "https://reed.co.uk"


def multiple_raw_to_formatted_job_information(raw_data : List[RawJobInformation],
 raw_description_data: List[RawJobDescriptionInformation]) -> List[FormattedJobInformation]:

    output = []

    for i in range(len(raw_data)):
        if raw_description_data is not None:
            output.append(raw_to_formatted_job_information(raw_data=raw_data[i],
             raw_description_data=raw_description_data[i]))
        else:
            output.append(raw_to_formatted_job_information(raw_data=raw_data[i],
            raw_description_data=None))
    
    return output


def raw_to_formatted_job_information(raw_data: RawJobInformation,
 raw_description_data: RawJobDescriptionInformation = None) -> FormattedJobInformation:
    """
    Formats any data collected for a Reed job advertisement and cleans it into a presentable format.
    """
    job_id = format_job_id(raw_data.job_id)
    title = format_job_title(raw_data.title)
    date = FormatJobDatePosted.format_job_posted_date(raw_data.date_and_employer)
    employer = format_job_employer(raw_data.date_and_employer)

    salary_lower, salary_upper = FormatJobPay.format_job_salary_range(raw_data.salary)
    salary_type = FormatJobPay.format_job_salary_type(raw_data.salary)
    location = FormatJobWorkConditions.format_job_location(raw_data.location)

    tenure_type = FormatJobWorkConditions.format_job_tenure_type(raw_data.tenure_type)
    remote_status = FormatJobWorkConditions.format_job_remote_status(raw_data.remote_status)
    description_start = format_job_description_start(raw_data.description_start)

    full_page_link = format_job_url(raw_data.full_page_link)

    number_of_applicants = ""
    full_description = ""

    if raw_description_data:
        number_of_applicants = FormatDescriptionJobData.format_job_number_of_applicants(
            raw_description_data.number_of_applicants)
        full_description = FormatDescriptionJobData.format_job_description_full(
            raw_description_data.full_description)
        if full_description == "": full_description = "N/A"


    return FormattedJobInformation(job_id=job_id, title=title, date=date, employer=employer,
    salary_lower=salary_lower, salary_upper=salary_upper, salary_type=salary_type,
    location=location, tenure_type=tenure_type, remote_status=remote_status,
    description_start=description_start, full_page_link=full_page_link,
    number_of_applicants=number_of_applicants, full_description=full_description)


class RawJobInformation(Protocol):
    job_id: str
    title: str
    date_and_employer: str
    salary: str
    location: str
    tenure_type: str
    remote_status: str
    description_start: str
    full_page_link: str


class RawJobDescriptionInformation(Protocol):
    job_id: str
    number_of_applicants: str
    full_description: str


@dataclass
class FormattedJobInformation:
    job_id: int
    title: str
    date: datetime.datetime.date
    employer: str
    salary_lower: Union[float, None]
    salary_upper: Union[float, None]
    salary_type: str
    location: str
    tenure_type: str
    remote_status: str
    description_start: str
    full_page_link: str
    number_of_applicants: str
    full_description: str

    def to_list(self) -> List[str]:
        return list(self.__dict__.values())



def format_job_title(title: str) -> str:
    alnum_title = ""
    for char in title:
        if (char).isalnum() or char in [" ", ",", "'"]: alnum_title += char
    return alnum_title.strip().lower().capitalize()


def format_job_employer(date_employer: str):
    return date_employer[date_employer.find(" by") + 3:].strip()


class FormatJobDatePosted:
    @staticmethod
    def format_job_posted_date(date_employer: str) -> datetime.datetime.date:
        date_value = date_employer[: date_employer.find(" by")].strip()

        temp_date = None
        if date_value.find("days ago") != -1:
            days_ago = int(date_value[:date_value.find(" days")])
            temp_date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).date()
        elif date_value.find("hrs ago") != -1:
            hours_ago = int(date_value[:date_value.find(" hrs")])
            temp_date = (datetime.datetime.now() - datetime.timedelta(hours=hours_ago)).date()
        elif date_value.find("week ago") != -1:
            temp_date = (datetime.datetime.now() - datetime.timedelta(days=7)).date()
        elif date_value.find("Yesterday") != -1:
            temp_date = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
        else:
            if date_value.find(str(datetime.datetime.now().year - 1)) != -1:
                temp_date = datetime.datetime.strptime(date_value, "%d %B %Y").date()
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
    def format_job_salary_type(salary_raw: str) -> str:
        parsing_mode = FormatJobPay._get_salary_parsing_mode(salary_raw)

        if parsing_mode > 3: return salary_raw.strip()

        salary_types = {0: "annual", 1: "daily", 2: "competitive", 3: "negotiable"}

        return salary_types[parsing_mode]
    
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
        output_location = " "
        for char in location_raw:
            if char.isalnum() or char in [",", "-"]:
                output_location += char
            if char == " " and output_location[-1] != " ":
                output_location += char
        return output_location.strip()
    
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


def format_job_description_start(raw_description: str) -> str:
    return raw_description.strip()

def format_job_url(raw_url: str) -> str:
    return BASE_URL + raw_url[:raw_url.find("?")].strip()   

def format_job_id(raw_id: str) -> int:
    output = ""
    for char in raw_id:
        if char.isnumeric():
            output += char
    return int(output)


class FormatDescriptionJobData:

    VALID_SYMBOLS = [".", "-", ",", ":", ";", "£", "$", "€", "&", "%", "(", ")", "/"]

    @staticmethod
    def format_job_number_of_applicants(applicants_raw: str) -> str:
        if applicants_raw == "Be one of the first ten applicants": return "<10"
        if applicants_raw == "": return "10+"
        return applicants_raw

    @classmethod
    def format_job_description_full(cls, description_raw: str):
        output = ""
        for char in description_raw:
            if not cls._is_valid_char(char): continue
            if char == " " and output[-1] == " ": continue
            output += char
            if char == ":": output += " "

        return output
    
    @classmethod
    def _is_valid_char(cls, char: str):
        if char.isalnum(): return True
        if char in cls.VALID_SYMBOLS: return True
        if char == " ": return True
        return False

