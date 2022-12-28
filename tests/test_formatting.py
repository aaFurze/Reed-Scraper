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


@pytest.fixture
def salary_range_yearly():
    return "    £30,000 - £40,000 per annum "

@pytest.fixture
def salary_range_daily():
    return "£120.00 - £130.00 per day  "

@pytest.fixture
def salary_competitive():
    return "  Competitive salary"


def test_format_job_title(dirty_string: str):
    assert formatting.format_job_title(dirty_string) == "Dirty string"


class TestFormattingDates:
    def test_format_job_posted_date_actual_date_input(self, dirty_date_and_employer: str):
        assert formatting.format_job_posted_date(dirty_date_and_employer) == datetime.datetime(year=datetime.datetime.now().year, month=10, day=5).date()

    def test_format_job_posted_date_days_ago_input(self, dirty_days_ago_and_employer: str):
        assert formatting.format_job_posted_date(dirty_days_ago_and_employer) == (datetime.datetime.now() - datetime.timedelta(days=4)).date()

    def test_get_year_value_earlier_month(self):
        assert formatting._get_year_value(current_date=datetime.datetime(month=1, day=1, year=2022).date(),
        other_date=datetime.datetime(month=10, day=5, year=1900).date()) == 2021

    def test_get_year_value_same_month_day(self):
        assert formatting._get_year_value(current_date=datetime.datetime(month=11, day=16, year=2022).date(),
        other_date=datetime.datetime(month=11, day=16, year=1900).date()) == 2022

    def test_get_year_value_later_month(self):
        assert formatting._get_year_value(current_date=datetime.datetime(month=11, day=16, year=2022).date(),
        other_date=datetime.datetime(month=10, day=5, year=1900).date()) == 2022


class TestFormatJobPay:
    def test_format_job_salary_range_yearly(self, salary_range_yearly):
        assert formatting.FormatJobPay.format_job_salary_range(salary_range_yearly) == [30000, 40000]
    
    def test_format_job_salary_range_daily(self, salary_range_daily):
        assert formatting.FormatJobPay.format_job_salary_range(salary_range_daily) == [120.00, 130.00]
    
    def test_format_job_salary_range_competitive(self, salary_competitive):
        assert formatting.FormatJobPay.format_job_salary_range(salary_competitive) == [None, None]
    
    def test_format_job_salary_type_yearly(self, salary_range_yearly):
        assert formatting.FormatJobPay.format_job_salary_type(salary_range_yearly) == "annual"
    
    def test_format_job_salary_type_daily(self, salary_range_daily):
        assert formatting.FormatJobPay.format_job_salary_type(salary_range_daily) == "daily"
    
    def test_format_job_salary_type_competitive(self, salary_competitive):
        assert formatting.FormatJobPay.format_job_salary_type(salary_competitive) == "competitive"
    
