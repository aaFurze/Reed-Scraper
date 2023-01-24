import datetime
from typing import List, Union

import pandas as pd
from typing_extensions import Protocol


class FormattedJobInformation(Protocol):
    job_id: str
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

    def to_list(self) -> List[str]:
        ...

COLUMNS = [
    "job_id",
    "job_title",
    "date",
    "employer",
    "salary_lower",
    "salary_upper",
    "salary_type",
    "location",
    "tenure_type",
    "remote_status",
    "description_start",
    "full_page_link"
]

class CreateJobDataFrame:

    @staticmethod
    def create_blank_df():
        return pd.DataFrame(columns=COLUMNS)
    
    @staticmethod
    def insert_job_information_object_into_df(df: pd.DataFrame, job_info: FormattedJobInformation):
        if job_info.job_id in df["job_id"].values: return df
        df.loc[len(df)] = job_info.to_list()
        return df  

    @staticmethod
    def insert_mutliple_job_information_objects_into_df(df: pd.DataFrame,
        job_infos: List[FormattedJobInformation]) -> pd.DataFrame:
        for info in job_infos:
            df = CreateJobDataFrame.insert_job_information_object_into_df(df, info)
        return df
    


class FormatFileName:
    @staticmethod
    def format_name(raw_name: str) -> str:
        name = raw_name.strip() + FormatFileName._get_timestamp(datetime.datetime.now())
        return FormatFileName._ensure_ends_csv(raw_file_name=name)

    @staticmethod
    def _ensure_ends_csv(raw_file_name: str) -> str:
        if raw_file_name.find(".csv") == -1:
                return raw_file_name.strip() + ".csv"
        return raw_file_name.replace(".csv", "") + ".csv"
    @staticmethod
    def _get_timestamp(date: datetime.datetime) -> str:
        return date.strftime("-%y%m%d-%H%M%S")


def save_df_to_csv(df: pd.DataFrame, file_name: str,
 prepend_data_folder_to_file_name: bool = True) -> bool:
    file_name = FormatFileName.format_name(file_name)
    try:
        if prepend_data_folder_to_file_name: file_name = "data//" + file_name
        df.to_csv(file_name, sep=",", index=False)
        return True
    except OSError:
        print(f"Could not save file. Does a \"data\" folder exist in the project root?")
        return False
