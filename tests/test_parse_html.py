from typing import List

import httpx
import pytest
from bs4 import BeautifulSoup

from src.parse_html import (JobContainerParser, RawJobInformation,
                            RawJobInformationFactory, ResponseToContainers)
from src.scraper import ReedJobPostingsScraper


@pytest.fixture(scope="module")
def get_page_html() -> List[httpx.Response]:
    return ReedJobPostingsScraper.get_job_postings(job_title="software-engineer", location="leeds", search_radius=25, max_pages=1)[0]

@pytest.fixture(scope="module")
def get_soupified_page(get_page_html) -> BeautifulSoup:
    return ResponseToContainers.soupify_page(get_page_html)

@pytest.fixture(scope="module")
def get_job_containers(get_soupified_page) -> List[BeautifulSoup]:
    return ResponseToContainers.get_job_posting_containers(get_soupified_page)

@pytest.fixture
def get_job(get_job_containers):
    return get_job_containers[0]

@pytest.fixture
def get_raw_job_information(get_job) -> RawJobInformation:
    return RawJobInformationFactory.populate_raw_job_information_from_job_container(RawJobInformationFactory.get_empty_raw_job_info(), get_job)


class TestResponseToContainers:
    def test_soupify_page(self, get_soupified_page: BeautifulSoup):
        assert isinstance(get_soupified_page, BeautifulSoup)


    def test_get_job_posting_containers_exist(self, get_job_containers: List[BeautifulSoup]):
            assert len(get_job_containers) > 0
    
    def test_response_to_job_posting_containers_returns_multiple_objects(self, get_page_html: httpx.Response):
        assert len(ResponseToContainers.response_to_job_posting_containers(get_page_html)) > 0
    
    def test_responses_to_job_posting_containers_returns_multiple_objects(self, get_page_html: httpx.Response, get_job_containers: List[BeautifulSoup]):
        assert len(ResponseToContainers.responses_to_job_posting_containers([get_page_html, get_page_html])) == len(get_job_containers) * 2



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
        assert type(JobContainerParser.get_job_full_page_link_raw(get_job)) is str

    def test_get_job_id_raw_exists(self, get_job: BeautifulSoup):
        assert type(JobContainerParser.get_job_id_raw(get_job)) is str        


class TestRawJobInformationFactory:
    def test_get_empty_raw_job_info_returns_correct_type(self):
        assert type(RawJobInformationFactory.get_empty_raw_job_info()) is RawJobInformation
    
    def test_get_x_empty_raw_job_info_containers_correct_length(self):
        assert len(RawJobInformationFactory.get_x_empty_raw_job_info_objects(12)) == 12
    
    def test_populate_raw_job_information_from_job_container_title(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.title == JobContainerParser.get_job_title(get_job)
    
    def test_populate_raw_job_information_from_job_container_date_and_employer(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.date_and_employer == JobContainerParser.get_job_posted_date_and_employer_info_raw(get_job)

    def test_populate_raw_job_information_from_job_container_location(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.location == JobContainerParser.get_job_location_raw(get_job)
    
    def test_populate_raw_job_information_from_job_container_salary(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.salary == JobContainerParser.get_job_salary_info_raw(get_job)

    def test_populate_raw_job_information_from_job_container_tenure_type(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.tenure_type == JobContainerParser.get_job_tenure_type_raw(get_job)

    def test_populate_raw_job_information_from_job_container_remote_status(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.remote_status == JobContainerParser.get_job_remote_status_raw(get_job)

    def test_populate_raw_job_information_from_job_container_full_page_link(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.full_page_link == JobContainerParser.get_job_full_page_link_raw(get_job)

    def test_populate_raw_job_information_from_container_job_id(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.job_id == JobContainerParser.get_job_id_raw(get_job)

    def test_populate_raw_job_information_from_job_container_description_start(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.description_start == JobContainerParser.get_job_description_start_raw(get_job)    

    def test_get_multiple_raw_job_info_objects_length(self, get_page_html: httpx.Response):
        assert len(RawJobInformationFactory.get_multiple_populated_raw_job_info_objects([get_page_html])) >= 20
    
    @pytest.mark.parametrize("index", [0, 1, 2, -2, -1, 0])
    def test_get_multiple_raw_job_info_objects_populated(self, get_page_html: httpx.Response, index: int):
        test_information_objects = RawJobInformationFactory.get_multiple_populated_raw_job_info_objects([get_page_html])
        assert len(test_information_objects[index].title) > 0

