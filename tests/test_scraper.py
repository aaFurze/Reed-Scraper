import time
from typing import List

import httpx
import pytest

import src.scraper as scraper


@pytest.fixture(scope="module")
def get_reed_webpages() -> httpx.Response:
    return scraper.ReedJobPostingsScraper.get_job_postings("software-engineer", "leeds", 11, 10)

@pytest.fixture
def get_non_existant_webpages():
    return scraper.ReedJobPostingsScraper.get_job_postings("archaeology", "highlands", 0, 1)

@pytest.fixture
def get_zero_input_webpages():
    return scraper.ReedJobPostingsScraper.get_job_postings("teacher", "highlands", 11, 0)



def test_get_reed_webpage_status_code(get_reed_webpages: List[httpx.Response]):
    assert get_reed_webpages[0].status_code == 200

def test_get_reed_webpage_has_html(get_reed_webpages: List[httpx.Response]):
    print(get_reed_webpages[0].url)
    assert get_reed_webpages[0].text.find("job-result-heading__title") != -1

def test_get_job_pages_count(get_reed_webpages: List[httpx.Response]):
    assert len(get_reed_webpages) == 10


def test_get_job_pages_out_of_pages(get_non_existant_webpages: List[httpx.Response]):
    assert len(get_non_existant_webpages) == 1


def test_get_job_pages_zero_pages_input(get_zero_input_webpages: List[httpx.Response]):
    assert len(get_zero_input_webpages) == 1


def test_get_number_of_job_postings_exists(get_non_existant_webpages: List[httpx.Response]):
    assert scraper.ReedJobPostingsScraper._get_number_of_job_postings(get_non_existant_webpages[0]) == 0


def test_get_number_of_pages_to_return():
    assert scraper.ReedJobPostingsScraper._get_number_of_pages_to_return(number_of_jobs=120, max_pages=20) == 6
    assert scraper.ReedJobPostingsScraper._get_number_of_pages_to_return(number_of_jobs=11, max_pages=20) == 1
    assert scraper.ReedJobPostingsScraper._get_number_of_pages_to_return(number_of_jobs=111, max_pages=1) == 1
