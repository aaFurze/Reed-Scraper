from typing import List

import httpx
import pytest
from bs4 import BeautifulSoup

from src.parse_html import JobContainerParser, ResponseToContainers
from src.scraper import ReedJobPostingsScraper


@pytest.fixture(scope="module")
def get_page_html() -> List[httpx.Response]:
    return ReedJobPostingsScraper.get_job_postings(job_title="software-engineer", location="leeds", search_radius=25, max_pages=1)[0]

@pytest.fixture(scope="module")
def get_soupified_page(get_page_html) -> BeautifulSoup:
    return ResponseToContainers.soupify_page(get_page_html)

@pytest.fixture(scope="module")
def get_job_containers(get_soupified_page):
    return ResponseToContainers.get_job_posting_containers(get_soupified_page)

@pytest.fixture
def get_job(get_job_containers):
    return get_job_containers[0]


class TestResponseToContainers:
    def test_soupify_page(self, get_soupified_page: BeautifulSoup):
        assert isinstance(get_soupified_page, BeautifulSoup)


    def test_get_job_posting_containers_exist(self, get_job_containers: List[BeautifulSoup]):
        assert len(get_job_containers) > 0


class TestJobContainerParser:
    def test_get_job_title_exists(self, get_job: BeautifulSoup):
        assert type(JobContainerParser.get_job_title(get_job)) is str


    def test_get_posted_date_info_and_employer_raw_exists(self, get_job: BeautifulSoup):
        assert type(JobContainerParser.get_job_posted_date_and_employer_info_raw(get_job)) is str

    def test_get_posted_date_info_and_employer_raw_gets_employer(self, get_job: BeautifulSoup):
        assert JobContainerParser.get_job_posted_date_and_employer_info_raw(get_job).find("by") != -1


    def test_get_job_metadata_panel_raw_exists(self, get_job: BeautifulSoup):
        assert type(JobContainerParser._get_job_metadata_panel_raw(get_job)) is not None

    def test_get_job_metadata_no_class_returns_first_item(self, get_job: BeautifulSoup):
        assert len(JobContainerParser._get_job_metadata(get_job, "li", "")) > 0

    def test_get_job_metadata_when_invalid_tag_class(self, get_job: BeautifulSoup):
        assert type(JobContainerParser._get_job_metadata(get_job, "dsfadf", "dsfadsf")) is str

    def test_get_job_salary_info_raw(self, get_job: BeautifulSoup) -> str:
        assert len(JobContainerParser.get_job_salary_info_raw(get_job)) > 0


    def test_get_job_location_raw(self, get_job: BeautifulSoup) -> str:
        assert len(JobContainerParser.get_job_location_raw(get_job)) > 0


    def test_get_job_tenure_type_raw(self, get_job: BeautifulSoup) -> str:
        assert len(JobContainerParser.get_job_tenure_type_raw(get_job)) > 0


    def test_get_job_remote_status_raw(self, get_job: BeautifulSoup) -> str:
        assert len(JobContainerParser.get_job_remote_status_raw(get_job)) > 0


    def get_job_description_start_raw(self, container: BeautifulSoup) -> str:
        return JobContainerParser._get_job_metadata(container, "p", "job-result-description__details")

    def test_get_job_description_start_raw_exists(self, get_job: BeautifulSoup):
        assert type(JobContainerParser.get_job_description_start_raw(get_job)) is str

    def test_get_job_full_page_link_raw_exists(self, get_job: BeautifulSoup):
        print(JobContainerParser.get_job_full_page_link_raw(get_job))
        assert type(JobContainerParser.get_job_full_page_link_raw(get_job)) is str