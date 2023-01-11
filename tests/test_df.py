import datetime

import pandas as pd
import pytest

from src.df import COLUMNS, SaveToDataFrame, _format_file_name
from src.formatting import FormattedJobInformation


@pytest.fixture
def blank_df() -> pd.DataFrame:
    return SaveToDataFrame.create_blank_df()

@pytest.fixture
def job_information():
    return FormattedJobInformation("Software Guy", datetime.datetime.date(
        datetime.datetime(year=2022, month=11, day=24)), employer="Big Tech", salary_lower=123.32,
        salary_upper=146.42, salary_type="daily", location="Telford",
        remote_status="remote", description_start="This is a cool job...",
        full_page_link="this_doesnt_go_anywhere.com", tenure_type="Full-time")

@pytest.fixture
def job_information_2():
    return FormattedJobInformation("Data Bro", datetime.datetime.date(
        datetime.datetime(year=2021, month=5, day=4)), employer="Big Data", salary_lower=125.52,
        salary_upper=186.11, salary_type="daily", location="Bradford",
        remote_status="remote", description_start="This is an exciting job...",
        full_page_link="this_doesnt_go_anywhere_either.com", tenure_type="Full-time")

@pytest.fixture
def populated_df(blank_df, job_information, job_information_2) -> pd.DataFrame:
    return SaveToDataFrame.insert_mutliple_job_information_objects_into_df(blank_df,
    [job_information, job_information_2])


@pytest.fixture
def file_name_no_csv():
    return "test_name    "

@pytest.fixture
def file_name_with_csv():
    return "test_name2.csv"



class TestSaveToDataFrame():
    def test_create_blank_df_column_count(self, blank_df: pd.DataFrame):
        assert len(blank_df.columns) == 11
    
    def test_create_blank_df_column_names(self, blank_df: pd.DataFrame):
        assert list(blank_df.columns) == COLUMNS 
    
    def test_insert_job_information_object_into_df_length(self, blank_df: pd.DataFrame,
     job_information):
        assert len(SaveToDataFrame.insert_job_information_object_into_df(blank_df,
            job_information).index) == 1
    
    def test_insert_job_information_object_into_df_row_one_contents(self, 
    blank_df: pd.DataFrame, job_information):
     assert SaveToDataFrame.insert_job_information_object_into_df(blank_df,
      job_information).iloc[0][0] == "Software Guy"

    def test_insert_mutliple_job_information_objects_into_df(self, blank_df: pd.DataFrame, 
    job_information, job_information_2):
        assert len(SaveToDataFrame.insert_mutliple_job_information_objects_into_df(
            blank_df, [job_information, job_information_2]).index) == 2
    
    def test_save_df_to_csv_returns_true(self, populated_df: pd.DataFrame):
        assert SaveToDataFrame.save_df_to_csv(populated_df,
        file_name="C:\\Alex\\Data Analysis Projects\\Reed-Word-Search\\data\\test_file") == True
    

class TestFormatFileName:
    def test_format_file_name_adds_csv(self, file_name_no_csv: str):
        assert _format_file_name(file_name_no_csv).find(".csv") != -1
    
    @pytest.mark.parametrize("file_name, target_length", [("testy", 9),
     ("test.csv", 8)])
    def test_format_file_name_strip(self, file_name: str, target_length: int):
        assert len(_format_file_name(file_name)) == target_length
        
    def test_format_file_name_not_add_csv(self, file_name_with_csv: str):
        formatted_file_name = _format_file_name(file_name_with_csv)
        assert formatted_file_name.find(".csv") == len(formatted_file_name) - 4