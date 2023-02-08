import httpx
import pytest

from src.pipeline import JobDataPipeline
from src.search_page import RawJobInformation


@pytest.fixture(scope="module")
def standard_pipeline() -> JobDataPipeline:
    test_pipeline = JobDataPipeline()
    test_pipeline.run(job_title="software engineer", location="london", search_radius=25,
     max_pages=1, get_full_descriptions=False)
    return test_pipeline

@pytest.fixture(scope="module")
def detailed_pipeline() -> JobDataPipeline:
    test_pipeline = JobDataPipeline()
    test_pipeline.run(job_title="data analyst", location="manchester", search_radius=10,
     max_pages=1, get_full_descriptions=True)

    return test_pipeline


class TestJobDataPipeline:

    def test_run_executed(self, standard_pipeline: JobDataPipeline):
        assert standard_pipeline._run_successful
    
    def test_run_executed_detailed(self, detailed_pipeline: JobDataPipeline):
        assert detailed_pipeline._run_successful

    def test_scraper_returns_list(self, standard_pipeline: JobDataPipeline):
        assert type(standard_pipeline.scraped_responses) is list

    @pytest.mark.parametrize("index", [0, -1])
    def test_scraper_returns_httpx_responses(self, standard_pipeline: JobDataPipeline, index: int):
        assert type(standard_pipeline.scraped_responses[index]) is httpx.Response
    
    def test_parsed_results_returns_list(self, standard_pipeline: JobDataPipeline):
        assert type(standard_pipeline.raw_results) is list
    
    @pytest.mark.parametrize("index", [0, -1])
    def test_parser_returns_raw_job_information(self, standard_pipeline: JobDataPipeline, index: int):
        assert type(standard_pipeline.raw_results[index]) is RawJobInformation

    def test_raw_results_job_ids_not_none(self, standard_pipeline: JobDataPipeline):
        for raw_info in standard_pipeline.raw_results:
            assert raw_info.job_id is not None



    def test_get_job_ids_returns_list(self, detailed_pipeline: JobDataPipeline):
        assert type(detailed_pipeline.description_scraped_responses) is list
    
    def test_get_job_ids_return_length(self, detailed_pipeline: JobDataPipeline):
        assert len(detailed_pipeline.description_scraped_responses) == 25

    def test_scraper_returns_httpx_responses(self, detailed_pipeline: JobDataPipeline):
        for response in detailed_pipeline.description_scraped_responses:
            assert type(response) is httpx.Response
            
    def test_scraper_status_codes_equal_200(self, detailed_pipeline: JobDataPipeline):
        for response in detailed_pipeline.description_scraped_responses:
            assert response.status_code == 200
    
    def test_raw_results_description_job_ids_not_none(self,
     detailed_pipeline: JobDataPipeline):
        for raw_info in detailed_pipeline.description_raw_results:
            assert raw_info.job_id is not None
    
    def test_raw_results_number_of_applicants_not_none(self, detailed_pipeline: JobDataPipeline):
        for raw_info in detailed_pipeline.description_raw_results:
            assert raw_info.number_of_applicants is not None
    
    def test_raw_results_descriptions_not_none(self, detailed_pipeline: JobDataPipeline):
        for raw_info in detailed_pipeline.description_raw_results:
            assert raw_info.full_description is not None
    
    def test_formatted_results_job_ids_not_none(self,
     detailed_pipeline: JobDataPipeline):
        for formatted_info in detailed_pipeline.formatted_results:
            assert formatted_info.job_id is not None

    def test_formatted_results_number_of_applicants_not_none(self,
     detailed_pipeline: JobDataPipeline):
        for formatted_info in detailed_pipeline.formatted_results:
            assert formatted_info.job_id is not None

    def test_formatted_results_descriptions_not_none(self,
     detailed_pipeline: JobDataPipeline):
        counter = 0

        for formatted_info in detailed_pipeline.formatted_results:
            counter += 1
            assert formatted_info.full_description != ""
