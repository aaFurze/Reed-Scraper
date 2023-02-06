import time
from typing import List

import httpx
import pytest

import src.search_page.scraper as scraper


@pytest.fixture(scope="module")
def get_reed_webpages() -> httpx.Response:
    return scraper.ReedSearchPageScraper.get_job_postings("software-engineer", "leeds", 25, 10)

@pytest.fixture
def get_non_existant_webpages():
    return scraper.ReedSearchPageScraper.get_job_postings("zzczcz-czzc", "highlands", 0, 1)

@pytest.fixture
def get_zero_input_webpages():
    return scraper.ReedSearchPageScraper.get_job_postings("teacher", "highlands", 5, 0)



class TestReedSearchPageScraper:
    def test_get_reed_webpage_status_code(self, get_reed_webpages: List[httpx.Response]):
        assert get_reed_webpages[0].status_code == 200

    def test_get_reed_webpage_has_html(self, get_reed_webpages: List[httpx.Response]):
        assert get_reed_webpages[0].text.find("job-result-heading__title") != -1

    def test_get_job_pages_count(self, get_reed_webpages: List[httpx.Response]):
        assert len(get_reed_webpages) == 10


    def test_get_job_pages_out_of_pages(self, get_non_existant_webpages: List[httpx.Response]):
        assert len(get_non_existant_webpages) == 1


    def test_get_job_pages_zero_pages_input(self, get_zero_input_webpages: List[httpx.Response]):
        assert len(get_zero_input_webpages) == 1


    def test_get_number_of_job_postings_exists(self, get_non_existant_webpages: List[httpx.Response]):
        assert scraper.ReedSearchPageScraper._get_number_of_job_postings(get_non_existant_webpages[0]) == 0


    @pytest.mark.parametrize("test_number_of_jobs, test_max_pages, expected_result", [(120, 20, 5), (11, 20, 1), (111, 1, 1)])
    def test_get_number_of_pages_to_return(self, test_number_of_jobs, test_max_pages, expected_result):
        assert scraper.ReedSearchPageScraper._get_number_of_pages_to_return(number_of_jobs=test_number_of_jobs,
            max_pages=test_max_pages) == expected_result
