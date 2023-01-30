import datetime

import pytest

import src.formatting as formatting
import src.parse_html as parse_html


@pytest.fixture
def dirty_string():
    return " dirt@y String!#  "

@pytest.fixture
def dirty_date_and_employer():
    return " 5 October by Big Pharma  "

@pytest.fixture
def dirty_days_ago_and_employer():
    return " 4 days ago by Industrial Agriculture  "


@pytest.fixture
def salary_range_yearly():
    return "    £30,000 - £40,000 per annum "

@pytest.fixture
def salary_range_daily():
    return "£120.00 - £130.00 per day  "

@pytest.fixture
def salary_competitive():
    return "  Competitive salary"

@pytest.fixture
def location():
    return " Leeds, \n\r   West Yorkshire     "

@pytest.fixture
def tenure_permanent_full_time():
    return "Permanent, full-time "

@pytest.fixture
def tenure_contract_optional_time():
    return "Contract, full-time or part-time "

@pytest.fixture
def remote_status():
    return "   Work from home  "

@pytest.fixture
def remote_status_empty():
    return "   "

@pytest.fixture
def partial_url():
    return "  /jobs/software-engineer/48648894?source=searchResults&filter=%2fjobs%2fsoftware-engineer-jobs-in-leeds    "

@pytest.fixture
def unclean_job_id():
    return "/5435345  "


def test_format_job_title(dirty_string: str):
    assert formatting.format_job_title(dirty_string) == "Dirty string"


def test_format_job_employer_dirty_date_and_employer(dirty_date_and_employer):
    assert formatting.format_job_employer(dirty_date_and_employer) == "Big Pharma"

def body_of_test_format_job_employer_dirty_days_ago_and_employer(dirty_days_ago_and_employer: str):
    assert formatting.format_job_employer(dirty_days_ago_and_employer) == "Industrial Agriculture"



class TestFormattingDates:
    def test_format_job_posted_date_actual_date_input(self, dirty_date_and_employer: str):
        assert formatting.FormatJobDatePosted.format_job_posted_date(dirty_date_and_employer) == datetime.datetime(year=2022, month=10, day=5).date()

    def test_format_job_posted_date_days_ago_input(self, dirty_days_ago_and_employer: str):
        assert formatting.FormatJobDatePosted.format_job_posted_date(dirty_days_ago_and_employer) == (datetime.datetime.now() - datetime.timedelta(days=4)).date()

    def test_get_year_value_earlier_month(self):
        assert formatting.FormatJobDatePosted._get_year_value(current_date=datetime.datetime(month=1, day=1, year=2022).date(),
        other_date=datetime.datetime(month=10, day=5, year=1900).date()) == 2021

    def test_get_year_value_same_month_day(self):
        assert formatting.FormatJobDatePosted._get_year_value(current_date=datetime.datetime(month=11, day=16, year=2022).date(),
        other_date=datetime.datetime(month=11, day=16, year=1900).date()) == 2022

    def test_get_year_value_later_month(self):
        assert formatting.FormatJobDatePosted._get_year_value(current_date=datetime.datetime(month=11, day=16, year=2022).date(),
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
    

class TestFormatJobWorkConditions:
    def test_format_job_location(self, location):
        assert formatting.FormatJobWorkConditions.format_job_location(location) == "Leeds, West Yorkshire"
    
    def test_format_job_tenure_type_permanent_full_time_input(self, tenure_permanent_full_time):
        assert formatting.FormatJobWorkConditions.format_job_tenure_type(tenure_permanent_full_time) == "Permanent"
    
    def test_format_job_is_full_time_permanent_full_time_input(self, tenure_permanent_full_time):
        assert formatting.FormatJobWorkConditions.format_job_is_full_time(tenure_permanent_full_time) == "Full-time"
    
    def test_format_job_tenure_type_contract_optional_time_input(self, tenure_contract_optional_time):
        assert formatting.FormatJobWorkConditions.format_job_tenure_type(tenure_contract_optional_time) == "Contract"
    
    def test_format_job_is_full_time_contract_optional_time_input(self, tenure_contract_optional_time):
        assert formatting.FormatJobWorkConditions.format_job_is_full_time(tenure_contract_optional_time) == "Full or Part-time"
    
    def test_format_job_remote_work_status_work_from_home_input(self, remote_status):
        assert formatting.FormatJobWorkConditions.format_job_remote_status(remote_status) == "Work From Home"
    
    def test_format_job_remote_work_status_empty_input(self, remote_status_empty):
        assert formatting.FormatJobWorkConditions.format_job_remote_status(remote_status_empty) == "Unspecified"

    
def test_format_job_url_contains_reed(partial_url):
    assert formatting.format_job_url(partial_url).find("reed.co.uk") != -1

def test_format_job_id_numeric(unclean_job_id: str):
    assert type(formatting.format_job_id(unclean_job_id)) is int

@pytest.fixture
def example_raw_job_information():
    return parse_html.RawJobInformation(job_id="/12456?", title="   Software engineer", date_and_employer="5 days ago by Mega Corp",
     salary="    £30,000 - £40,000 per annum ", location="Leeds", tenure_type="Permanent, full-time ",
      remote_status="   Work from home  ", description_start="This is the best company in the world...",
       full_page_link="  /jobs/software-engineer/48648894?source=searchResults&filter=%2fjobs%2fsoftware-engineer-jobs-in-leeds    ")

@pytest.fixture
def example_formatted_job_information(example_raw_job_information):
    return formatting.raw_to_formatted_job_information(example_raw_job_information)


class TestFormatJobData:
    @pytest.mark.parametrize("attribute", ["job_id", "title", "date", "employer", "salary_lower", "salary_upper", "salary_type", "location", "tenure_type",
     "remote_status", "description_start", "full_page_link"])

    def test_raw_job_info_to_formatted_job_info_fills_attributes(self, example_formatted_job_information, attribute):
        assert getattr(example_formatted_job_information, attribute) != ""


@pytest.fixture
def example_description_raw():
    return """
Software Engineer  *Positions available from junior level up to principal/tech lead level*   
Location:  London- hybrid working   Salary:   £40.000 - £85.000 plus package   
Overview This cutting-edge cyber security firm is one of the top technology organisations when it comes to national defence. 
They operate in four key domains of expertise: Cyber Security, Financial Crime, Communications Intelligence and Digital Transformation.
Working on large central government projects, this Software Engineer role will provide you with diverse experience
 across the public sector and provides great opportunities for progression and
  to develop your career. As a software engineer you would work independently in designing,
   coding, testing and correcting software from given specifications while also
    assisting in the implementation of software which forms part of a properly engineered
     information or communication  system. You will logically analyse code defects and
      produce timely code fixes.  Desired experience:   
      A good understanding of any of the following programming languages: Java, JavaScript,
       React The desire to solve complex technical problems,
        helping our customers achieve their goals Knowledge of some cloud engineering such as
         AWS, Docker, Microservices ect is desirable but not essential
          The ability to work as part of a team, knowledge share and be involved with our
           Agile ways of working  Benefits:   Base salary between £40.000 - £85.000 , 
           based on experience  Car allowance of up to £6.500 Bonus up to 13% based on 
           performance Private medical & Dental  9% Pension (6% company contribution) 
           Flexible hybrid working Long term career plan / fantastic progression 
           Plus additional benefits  * Only those with the permanent and unrestricted right to 
           live and work in the UK will be considered for this role and must have or 
           undergo Government SC clearance prior to starting * 
           Location:LondonSalary: £40.000 - £85.000 plus package   Reference: AMC/SDA/SWEL
    """




class TestFormatDetailedJobData:
    @pytest.mark.parametrize("raw, expected", [("", "10+"),
     ("Be one of the first ten applicants", "<10")])
    def test_format_job_number_of_applicants(self, raw: str, expected: str):
        assert formatting.FormatExtraJobData.format_job_number_of_applicants(raw) == expected

    def test_format_job_description_full_standard(self, example_description_raw: str):
        assert formatting.FormatExtraJobData.format_job_description_full(
            example_description_raw).find("Software Engineer Positions available from junior level up to principal/tech lead level") != -1
