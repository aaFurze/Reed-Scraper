import pytest

from src.construct_url import ConstructUrl


@pytest.fixture
def target_url_standard():
    return "https://www.reed.co.uk/jobs/software-engineer-jobs-in-london?pageno=5&proximity=15"

@pytest.fixture
def standard_input_dict():
    return {
        "job_name": "   Software Engineer   ",
        "location": "  London  ",
        "search_radius": "15 ",
        "page_number": 5        
    }


@pytest.fixture
def target_url_special_case():
    return "https://www.reed.co.uk/jobs/cleaner-jobs-in-leeds"

@pytest.fixture
def special_case_input_dict():
    return {
        "job_name": "   $cleaner   ",
        "location": "  l?e%eds  ",
        "search_radius": 10,
        "page_number": " 1 "         
    }



class TestConstructUrl:


    @pytest.mark.parametrize("start, target",
     [("THIS IS A STRING  ", "this-is-a-string"), ("    #lIte", "lite"), ("45.24%", "4524"),
      ("      TEST me    ", "test-me")])
    def test_basic_clean_input(self, start: str, target: str):
        assert ConstructUrl._basic_clean_input(start) == target

    def test_get_url_standard(self, target_url_standard: str, standard_input_dict: dict):
        assert ConstructUrl.get_url(**standard_input_dict) == target_url_standard

    def test_get_job_name_url_segment_standard(self, target_url_standard: str, standard_input_dict: dict):
        assert target_url_standard.find(
            ConstructUrl.get_job_name_url_segment(standard_input_dict["job_name"])) != -1
    
    def test_get_search_radius_url_segment_standard(self, target_url_standard: str, standard_input_dict: dict):
       assert target_url_standard.find(
            ConstructUrl.get_search_radius_url_segment(standard_input_dict["search_radius"])) != -1

    def test_get_page_number_url_segment_standard(self, target_url_standard: str, standard_input_dict: dict):
        assert target_url_standard.find(
            ConstructUrl.get_page_number_url_segment(standard_input_dict["page_number"])) != -1

    def test_get_location_url_segment_standard(self, target_url_standard: str, standard_input_dict: dict):
        assert target_url_standard.find(
            ConstructUrl.get_location_url_segment(standard_input_dict["location"])) != -1



    def test_get_url_special(self, target_url_special_case: str, special_case_input_dict: dict):
        assert ConstructUrl.get_url(**special_case_input_dict) == target_url_special_case

    def test_get_job_name_url_segment_special(self, target_url_special_case: str, special_case_input_dict: dict):
        assert target_url_special_case.find(
            ConstructUrl.get_job_name_url_segment(special_case_input_dict["job_name"])) != -1
    
    def test_get_search_radius_url_segment_special(self, special_case_input_dict: dict):
       assert ConstructUrl.get_search_radius_url_segment(
        special_case_input_dict["search_radius"]) == ""

    def test_get_page_number_url_segment_special(self, special_case_input_dict: dict):
        assert ConstructUrl.get_page_number_url_segment(
            special_case_input_dict["page_number"]) == ""

    def test_get_location_url_segment_special(self, target_url_special_case: str, special_case_input_dict: dict):
        assert target_url_special_case.find(
            ConstructUrl.get_location_url_segment(special_case_input_dict["location"])) != -1


