import pytest
import httpx
import src.scraper as scraper
from typing import List
import asyncio
import time



@pytest.fixture(scope="module")
def get_reed_webpages() -> httpx.Response:
    return asyncio.run(scraper.get_job_postings("software-engineer", "leeds", 11, 10))

@pytest.fixture
def get_non_existant_webpages():
    return asyncio.run(scraper.get_job_postings("archaeology", "highlands", 0, 1))

@pytest.fixture
def get_zero_input_webpages():
    return asyncio.run(scraper.get_job_postings("teacher", "highlands", 11, 0))



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
    assert scraper._get_number_of_job_postings(get_non_existant_webpages[0]) == 0


def test_get_number_of_pages_to_return():
    assert scraper._get_number_of_pages_to_return(120, 20) == 6
    assert scraper._get_number_of_pages_to_return(11, 20) == 1
    assert scraper._get_number_of_pages_to_return(111, 1) == 1
