import httpx
import pytest

from src.parse_html import RawJobInformation
from src.pipeline import JobDataPipeline


@pytest.fixture(scope="module")
def job_data_pipeline_standard() -> JobDataPipeline:
    test_pipeline = JobDataPipeline()
    test_pipeline.run(job_title="software engineer", location="london", search_radius=25, max_pages=3)
    return test_pipeline



class TestJobDataPipeline:
    def test_scraper_returns_list(self, job_data_pipeline_standard: JobDataPipeline):
        assert type(job_data_pipeline_standard.scraped_results) is list

    @pytest.mark.parametrize("index", [0, -1])
    def test_scraper_returns_httpx_responses(self, job_data_pipeline_standard: JobDataPipeline, index: int):
        assert type(job_data_pipeline_standard.scraped_results[index]) is httpx.Response
    
    def test_parsed_results_returns_list(self, job_data_pipeline_standard: JobDataPipeline):
        assert type(job_data_pipeline_standard.parsed_results) is list
    
    @pytest.mark.parametrize("index", [0, -1])
    def test_parser_returns_httpx_responses(self, job_data_pipeline_standard: JobDataPipeline, index: int):
        assert type(job_data_pipeline_standard.parsed_results[index]) is RawJobInformation
