import pytest
import httpx
from src.scraper import get_job_postings
import src.parse_html as parse_html
from typing import List
from bs4 import BeautifulSoup


@pytest.fixture(scope="module")
def get_page_html() -> List[httpx.Response]:
    return get_job_postings(job_title="software-engineer", location="leeds", search_radius=25, max_pages=1)[0]

@pytest.fixture(scope="module")
def get_soupified_page(get_page_html) -> BeautifulSoup:
    return parse_html.soupify_page(get_page_html)

@pytest.fixture(scope="module")
def get_job_containers(get_soupified_page):
    return parse_html.get_job_posting_containers(get_soupified_page)


def test_soupify_page(get_soupified_page: BeautifulSoup):
    assert isinstance(get_soupified_page, BeautifulSoup)


def test_get_job_posting_containers_exist(get_job_containers: BeautifulSoup):
    assert len(get_job_containers) > 0

def test_get_job_title_raw(get_job_containers: BeautifulSoup):
    assert parse_html.get_job_title_raw(get_job_containers[0]) is not None

