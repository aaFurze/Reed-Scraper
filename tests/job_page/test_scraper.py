import time
from typing import List

import httpx
import pytest

import src.job_page.scraper as scraper


class TestReedJobPageScraper:
    def test_get_job_pages_returns_list(self):
        assert type(scraper.ReedJobPageScraper.get_job_pages([543543, 554334])) is list
    
    def test_get_job_pages_returns_httpx_responses(self):
        result = scraper.ReedJobPageScraper.get_job_pages([123, 321])
        for value in result:
            assert type(value) is httpx.Response
