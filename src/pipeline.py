from src.parse_html import RawJobInformationFactory
from src.scraper import ReedJobPostingsScraper


class JobDataPipeline:
    def __init__(self) -> None:
        self.scraped_results = None
        self.parsed_results = None
        self.formatted_results = None
    
    def run(self, job_title: str, location: str, search_radius: int = 10, max_pages: int = 1):
        self.scraped_results = ReedJobPostingsScraper.get_job_postings(job_title=job_title, location=location,
         search_radius=search_radius, max_pages=max_pages)
        self.parsed_results = RawJobInformationFactory.get_multiple_populated_raw_job_info_objects(responses=self.scraped_results)
        # self.formatted_results = 
