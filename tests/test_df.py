import datetime

import pandas as pd
import pytest

from src.df import COLUMNS, CreateJobDataFrame, FormatFileName, save_df_to_csv
from src.search_page import FormattedJobInformation


@pytest.fixture
def blank_df_normal() -> pd.DataFrame:
    return CreateJobDataFrame.create_blank_df()

@pytest.fixture
def job_information():
    return FormattedJobInformation(12345, "Software Guy", datetime.datetime.date(
        datetime.datetime(year=2022, month=11, day=24)), employer="Big Tech", salary_lower=123.32,
        salary_upper=146.42, salary_type="daily", location="Telford",
        remote_status="remote", description_start="This is a good job...",
        full_page_link="this_doesnt_go_anywhere.com", tenure_type="Full-time",
        number_of_applicants="<10", full_description="This is a good job for humans.")

@pytest.fixture
def job_information_2():
    return FormattedJobInformation(987654, "Data Bro", datetime.datetime.date(
        datetime.datetime(year=2021, month=5, day=4)), employer="Big Data", salary_lower=125.52,
        salary_upper=186.11, salary_type="daily", location="Bradford",
        remote_status="remote", description_start="This is an exciting job...",
        full_page_link="this_doesnt_go_anywhere_either.com", tenure_type="Full-time",
        number_of_applicants="10+", full_description="This is an exciting job for all people.")

@pytest.fixture
def populated_df(blank_df_normal, job_information, job_information_2) -> pd.DataFrame:
    return CreateJobDataFrame.insert_mutliple_job_information_objects_into_df(blank_df_normal,
    [job_information, job_information_2])


@pytest.fixture
def file_name_no_csv() -> str:
    return "test_name    "

@pytest.fixture
def file_name_with_csv() -> str:
    return "test_name2.csv"

@pytest.fixture
def test_date() -> datetime.datetime:
    return datetime.datetime(year=2021, month=5, day=6, hour=23, minute=43, second=1)



class TestCreateJobDataFrame():
    def test_create_blank_df_column_count(self, blank_df_normal: pd.DataFrame):
        assert len(blank_df_normal.columns) == 14
    
    def test_create_blank_df_column_names(self, blank_df_normal: pd.DataFrame):
        assert list(blank_df_normal.columns) == COLUMNS 

    def test_insert_job_information_object_into_df_length(self, blank_df_normal: pd.DataFrame,
     job_information):
        assert len(CreateJobDataFrame.insert_job_information_object_into_df(blank_df_normal,
            job_information).index) == 1

    def test_insert_job_information_object_into_df_row_one_contents(self, 
    blank_df_normal: pd.DataFrame, job_information):
     assert CreateJobDataFrame.insert_job_information_object_into_df(blank_df_normal,
      job_information).iloc[0][1] == "Software Guy"

    def test_insert_mutliple_job_information_objects_into_df(self, blank_df_normal: pd.DataFrame, 
    job_information, job_information_2):
        assert len(CreateJobDataFrame.insert_mutliple_job_information_objects_into_df(
            blank_df_normal, [job_information, job_information_2]).index) == 2
    
    def test_save_df_to_csv_returns_true(self, populated_df: pd.DataFrame):
        assert save_df_to_csv(populated_df,
        file_name="C:\\Alex\\Data Analysis Projects\\Reed-Word-Search\\data\\test_file",
        prepend_data_folder_to_file_name=False) == True
    
    def test_insert_job_information_object_into_df_no_duplicate_ids(self, blank_df_normal: pd.DataFrame,
    job_information):
        CreateJobDataFrame.insert_job_information_object_into_df(blank_df_normal, job_information)
        CreateJobDataFrame.insert_job_information_object_into_df(blank_df_normal, job_information)
        assert len(blank_df_normal.index) == 1


    def test_insert_job_information_object_into_df_length(self,
     blank_df_normal: pd.DataFrame, job_information_2):
        assert len(CreateJobDataFrame.insert_job_information_object_into_df(blank_df_normal,
            job_information_2).index) == 1
    
    def test_insert_detailed_job_information_object_into_df_second_last_row_contents(self, 
     blank_df_normal: pd.DataFrame, job_information):
     assert CreateJobDataFrame.insert_job_information_object_into_df(blank_df_normal,
      job_information).iloc[0][-2] == "<10"

    def test_insert_mutliple_detailed_job_information_objects_into_df(self, blank_df_normal: pd.DataFrame, 
     job_information, job_information_2):
        assert len(CreateJobDataFrame.insert_mutliple_job_information_objects_into_df(
            blank_df_normal, [job_information, job_information_2]).index) == 2


class TestFormatFileName:
    def test_format_name_correct_end(self, file_name_with_csv: str):
        formatted_name = FormatFileName.format_name(file_name_with_csv) 
        assert formatted_name.find(".csv") == len(formatted_name) - 4

    def test_format_name_raw_name_stripped(self, file_name_no_csv: str):
        formatted_name = FormatFileName.format_name(file_name_no_csv)
        assert formatted_name.find("test_name") == 0
        assert formatted_name.find("  ") == -1

    def test_ensure_ends_csv_adds_csv(self, file_name_no_csv: str):
        assert FormatFileName._ensure_ends_csv(file_name_no_csv).find(".csv") != -1
    
    @pytest.mark.parametrize("file_name, target_length", [("testy", 9),
     ("test.csv", 8)])
    def test_ensure_ends_csv_strip(self, file_name: str, target_length: int):
        assert len(FormatFileName._ensure_ends_csv(file_name)) == target_length
        
    def test_ensure_ends_csv_not_add_csv(self, file_name_with_csv: str):
        formatted_file_name = FormatFileName._ensure_ends_csv(file_name_with_csv)
        assert formatted_file_name.find(".csv") == len(formatted_file_name) - 4
    
    def test_get_timestamp_year(self, test_date: datetime.datetime):
        assert FormatFileName._get_timestamp(test_date).find("21") == 1

