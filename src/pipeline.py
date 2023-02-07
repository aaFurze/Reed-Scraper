from typing import List

import httpx

from src.job_page import *
from src.search_page import *


class JobDataPipeline:
    def __init__(self) -> None:
        self.scraped_responses: List[httpx.Response] = None
        self.raw_results: List[RawJobInformation] = None

        self.description_scraped_responses: List[httpx.Response] = None
        self.description_raw_results: List[RawExtraJobInformation] = None
        
        self.formatted_results: List[FormattedJobInformation] = None

        self.has_run = False


    def run(self, job_title: str, location: str, search_radius: int = 10, max_pages: int = 1,
    get_full_descriptions: bool = False):
        self.scraped_responses = ReedSearchPageScraper.get_job_postings(job_title=job_title,
         location=location, search_radius=search_radius, max_pages=max_pages)
        self.raw_results = RawJobInformationFactory.get_multiple_populated_raw_job_info_objects(
            responses=self.scraped_responses)

        if get_full_descriptions:
            job_ids = self._get_job_ids(self.raw_results)
            self.description_scraped_responses = ReedJobPageScraper.get_job_pages(job_ids=job_ids)
            self.description_raw_results = self._get_raw_results(job_ids=job_ids,
            responses=self.description_scraped_responses)

        self.formatted_results = multiple_raw_to_formatted_job_information(
            self.raw_results, self.description_raw_results
        )    

        self.has_run = True

    
    @staticmethod
    def _get_job_ids(job_info: List[RawJobInformation]) -> List[int]:
        return [int(info.job_id[1:]) for info in job_info]

    @staticmethod
    def _get_raw_results(job_ids: List[int],
     responses: List[httpx.Response]) -> List[RawExtraJobInformation]:
        output = []
        for i in range(min(len(job_ids), len(responses))):
            output.append(DetailedJobContainerParser.get_raw_extra_job_information_object(
                job_id=job_ids[i], response=responses[i]))
        
        return output
