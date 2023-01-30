from typing import List

import httpx

from src.formatting import (FormattedExtraJobInformation,
                            FormattedJobInformation,
                            raw_to_formatted_extra_job_information,
                            raw_to_formatted_job_information)
from src.parse_html import (DetailedJobContainerParser, RawExtraJobInformation,
                            RawJobInformation, RawJobInformationFactory)
from src.scraper import ReedJobPageScraper, ReedSearchPageScraper


class JobDataPipeline:
    def __init__(self) -> None:
        self.scraped_responses: List[httpx.Response] = None
        self.raw_results: List[RawJobInformation] = None
        self.formatted_results: List[FormattedJobInformation] = None
    
    def run(self, job_title: str, location: str, search_radius: int = 10, max_pages: int = 1):
        self.scraped_responses = ReedSearchPageScraper.get_job_postings(job_title=job_title, location=location,
         search_radius=search_radius, max_pages=max_pages)
        self.raw_results = RawJobInformationFactory.get_multiple_populated_raw_job_info_objects(responses=self.scraped_responses)
        self.formatted_results = [raw_to_formatted_job_information(raw_data) for raw_data in self.raw_results]


class DetailedJobDataPipeline:
    def __init__(self) -> None:
        self.scraped_responses: List[httpx.Response] = None
        self.raw_results: List[RawExtraJobInformation] = None
        self.formatted_results: List[FormattedExtraJobInformation] = None
    
    def run(self, job_ids: List[int]):
        self.scraped_responses = ReedJobPageScraper.get_job_pages(job_ids=job_ids)
        self.raw_results = self._get_raw_results(job_ids=job_ids,
         responses=self.scraped_responses)
        self.formatted_results = [raw_to_formatted_extra_job_information(raw_data)
         for raw_data in self.raw_results]

    @staticmethod
    def _get_raw_results(job_ids: List[int],
     responses: List[httpx.Response]) -> List[RawExtraJobInformation]:
        output = []
        for i in range(min(len(job_ids), len(responses))):
            output.append(DetailedJobContainerParser.get_raw_extra_job_information_object(
                job_id=job_ids[i], response=responses[i]))
        
        return output

