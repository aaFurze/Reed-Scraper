import httpx
import pytest

from src.parse_html import RawJobInformation
from src.pipeline import DetailedJobDataPipeline, JobDataPipeline


@pytest.fixture(scope="module")
def standard_pipeline() -> JobDataPipeline:
    test_pipeline = JobDataPipeline()
    test_pipeline.run(job_title="software engineer", location="london", search_radius=25, max_pages=1)
    return test_pipeline

@pytest.fixture(scope="module")
def detailed_pipeline(standard_pipeline: JobDataPipeline) -> DetailedJobDataPipeline:
    test_pipeline = DetailedJobDataPipeline()
    test_pipeline.run(job_ids=[container.job_id for container in standard_pipeline.formatted_results])
    return test_pipeline


class TestJobDataPipeline:
    def test_scraper_returns_list(self, standard_pipeline: JobDataPipeline):
        assert type(standard_pipeline.scraped_responses) is list

    @pytest.mark.parametrize("index", [0, -1])
    def test_scraper_returns_httpx_responses(self, standard_pipeline: JobDataPipeline, index: int):
        assert type(standard_pipeline.scraped_responses[index]) is httpx.Response
    
    def test_parsed_results_returns_list(self, standard_pipeline: JobDataPipeline):
        assert type(standard_pipeline.raw_results) is list
    
    @pytest.mark.parametrize("index", [0, -1])
    def test_parser_returns_httpx_responses(self, standard_pipeline: JobDataPipeline, index: int):
        assert type(standard_pipeline.raw_results[index]) is RawJobInformation

    

class TestDetailedJobDataPipeline:
    def test_scraper_returns_httpx_responses(self, detailed_pipeline: DetailedJobDataPipeline):
        for response in detailed_pipeline.scraped_responses:
            assert type(response) is httpx.Response
        # assert type(detailed_pipeline.scraped_responses[index]) is httpx.Response
    
    def test_scraper_status_codes_equal_200(self, detailed_pipeline: DetailedJobDataPipeline):
        for response in detailed_pipeline.scraped_responses:
            assert response.status_code == 200
    
    def test_raw_results_job_ids_not_none(self, detailed_pipeline: DetailedJobDataPipeline):
        for raw_info in detailed_pipeline.raw_results:
            assert raw_info.job_id is not None
    
    def test_raw_results_number_of_applicants_not_none(self, detailed_pipeline: DetailedJobDataPipeline):
        for raw_info in detailed_pipeline.raw_results:
            assert raw_info.number_of_applicants is not None
    
    def test_raw_results_descriptions_not_none(self, detailed_pipeline: DetailedJobDataPipeline):
        for raw_info in detailed_pipeline.raw_results:
            assert raw_info.description is not None
    
    def test_formatted_results_job_ids_not_none(self,
     detailed_pipeline: DetailedJobDataPipeline):
        for formatted_info in detailed_pipeline.formatted_results:
            assert formatted_info.job_id is not None

    def test_formatted_results_number_of_applicants_not_none(self,
     detailed_pipeline: DetailedJobDataPipeline):
        for formatted_info in detailed_pipeline.formatted_results:
            assert formatted_info.job_id is not None

    def test_formatted_results_descriptions_not_none(self,
     detailed_pipeline: DetailedJobDataPipeline):
        for formatted_info in detailed_pipeline.formatted_results:
            assert formatted_info.job_id is not None