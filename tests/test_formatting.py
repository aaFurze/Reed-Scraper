import datetime

import pytest

import src.formatting as formatting


@pytest.fixture
def dirty_string():
    return " dirt@y String!#  "

@pytest.fixture
def dirty_date_and_employer():
    return " 5 October by Some Employer  "

@pytest.fixture
def dirty_days_ago_and_employer():
    return " 4 days ago by Some Employer  "

def test_format_job_title(dirty_string: str):
    assert formatting.format_job_title(dirty_string) == "Dirty string"

def test_format_job_posted_date_actual_date_input(dirty_date_and_employer: str):
    assert formatting.format_job_posted_date(dirty_date_and_employer) == datetime.datetime(year=datetime.datetime.now().year, month=10, day=5).date()

def test_format_job_posted_date_days_ago_input(dirty_days_ago_and_employer: str):
    assert formatting.format_job_posted_date(dirty_days_ago_and_employer) == (datetime.datetime.now() - datetime.timedelta(days=4)).date()

def test_get_year_value_earlier_month():
    assert formatting._get_year_value(current_date=datetime.datetime(month=1, day=1, year=2022).date(),
     other_date=datetime.datetime(month=10, day=5, year=1900).date()) == 2021

def test_get_year_value_same_month_day():
    assert formatting._get_year_value(current_date=datetime.datetime(month=11, day=16, year=2022).date(),
     other_date=datetime.datetime(month=11, day=16, year=1900).date()) == 2022

def test_get_year_value_later_month():
    assert formatting._get_year_value(current_date=datetime.datetime(month=11, day=16, year=2022).date(),
     other_date=datetime.datetime(month=10, day=5, year=1900).date()) == 2022

