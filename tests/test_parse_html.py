from typing import List

import httpx
import pytest
from bs4 import BeautifulSoup

import src.parse_html as parse_html
from src.scraper import get_job_postings


@pytest.fixture(scope="module")
def get_page_html() -> List[httpx.Response]:
    return get_job_postings(job_title="software-engineer", location="leeds", search_radius=25, max_pages=1)[0]

@pytest.fixture(scope="module")
def get_soupified_page(get_page_html) -> BeautifulSoup:
    return parse_html.soupify_page(get_page_html)

@pytest.fixture(scope="module")
def get_job_containers(get_soupified_page):
    return parse_html.get_job_posting_containers(get_soupified_page)

@pytest.fixture
def get_job(get_job_containers):
    return get_job_containers[0]



def test_soupify_page(get_soupified_page: BeautifulSoup):
    assert isinstance(get_soupified_page, BeautifulSoup)


def test_get_job_posting_containers_exist(get_job_containers: List[BeautifulSoup]):
    assert len(get_job_containers) > 0


def test_get_job_title_exists(get_job: BeautifulSoup):
    assert type(parse_html.get_job_title(get_job)) is str


def test_get_posted_date_info_and_employer_raw_exists(get_job: BeautifulSoup):
    assert type(parse_html.get_job_posted_date_and_employer_info_raw(get_job)) is str

def test_get_posted_date_info_and_employer_raw_gets_employer(get_job: BeautifulSoup):
    assert parse_html.get_job_posted_date_and_employer_info_raw(get_job).find("by") != -1


def test_get_job_metadata_panel_raw_exists(get_job: BeautifulSoup):
    assert type(parse_html.get_job_metadata_panel_raw(get_job)) is not None

def test_get_job_metadata_no_class_returns_first_item(get_job: BeautifulSoup):
    assert len(parse_html._get_job_data(get_job, "li", "")) > 0

def test_get_job_metadata_when_invalid_tag_class(get_job: BeautifulSoup):
    assert type(parse_html._get_job_data(get_job, "dsfadf", "dsfadsf")) is str

def test_get_job_salary_info_raw(get_job: BeautifulSoup) -> str:
    assert len(parse_html.get_job_salary_info_raw(get_job)) > 0


def test_get_job_location_raw(get_job: BeautifulSoup) -> str:
    assert len(parse_html.get_job_location_raw(get_job)) > 0


def test_get_job_tenure_type_raw(get_job: BeautifulSoup) -> str:
    assert len(parse_html.get_job_tenure_type_raw(get_job)) > 0


def test_get_job_remote_status_raw(get_job: BeautifulSoup) -> str:
    assert len(parse_html.get_job_remote_status_raw(get_job)) > 0


def get_job_description_start_raw(container: BeautifulSoup) -> str:
    return parse_html._get_job_data(container, "p", "job-result-description__details")

def test_get_job_description_start_raw_exists(get_job: BeautifulSoup):
    assert type(parse_html.get_job_description_start_raw(get_job)) is str

def test_get_job_full_page_link_raw_exists(get_job: BeautifulSoup):
    print(parse_html.get_job_full_page_link_raw(get_job))
    assert type(parse_html.get_job_full_page_link_raw(get_job)) is str