from typing import Dict

import pytest

from src.get_input import GetUserInput


@pytest.fixture
def dirty_strings() -> Dict[str, str]:
    return {
        "dirty_job_title" : " SOFTWARE  engineeR  ",
        "dirty_job_title_2" :  "    @cleaner",
        "dirty_location" : " Bradford",
        "dirty_location_2" :  "  SOUTH YorkShire  ", 
    }

@pytest.fixture
def dirty_ints() -> Dict[str, int]:
        return {
        "dirty_search_radius" : " SO43 ",
        "dirty_search_radius_2" :  "56.4",
        "dirty_max_results" : " 26",
        "dirty_max_results_2" :  " 56.8 ", 
    }


class TestGetUserInput:
    @pytest.mark.parametrize("key, cleaned_string", [
        ("dirty_job_title", "software-engineer"), ("dirty_job_title_2", "cleaner"),
        ("dirty_location", "bradford"), ("dirty_location_2", "south-yorkshire")])
    def test_clean_input_string(self, key: str, cleaned_string: str,
     dirty_strings: Dict[str, str]):
        assert GetUserInput.clean_input_string(dirty_strings[key]) == cleaned_string
    
    @pytest.mark.parametrize("key, cleaned_int", [
        ("dirty_search_radius", 43), ("dirty_search_radius_2", 56),
        ("dirty_max_results", 26), ("dirty_max_results_2", 56)])
    def test_clean_input_int(self, key: str, cleaned_int: str,
     dirty_ints: Dict[str, str]):
        assert GetUserInput.clean_input_int(dirty_ints[key]) == cleaned_int