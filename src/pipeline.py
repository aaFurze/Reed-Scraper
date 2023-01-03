from typing import List

import httpx

from src.formatting import (FormattedJobInformation,
                            raw_to_formatted_job_information)
from src.parse_html import RawJobInformation, RawJobInformationFactory
from src.scraper import ReedJobPostingsScraper


class JobDataPipeline:
    def __init__(self) -> None:
        self.scraped_responses: List[httpx.Response] = None
        self.raw_results: List[RawJobInformation] = None
        self.formatted_results: List[FormattedJobInformation]  = None
    
    def run(self, job_title: str, location: str, search_radius: int = 10, max_pages: int = 1):
        self.scraped_responses = ReedJobPostingsScraper.get_job_postings(job_title=job_title, location=location,
         search_radius=search_radius, max_pages=max_pages)
        self.raw_results = RawJobInformationFactory.get_multiple_populated_raw_job_info_objects(responses=self.scraped_responses)
        self.formatted_results = [raw_to_formatted_job_information(raw_data) for raw_data in self.raw_results]
