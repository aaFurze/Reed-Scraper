from __future__ import annotations

from dataclasses import dataclass
from typing import List

import httpx
from bs4 import BeautifulSoup

from src.parse_html import ResponseToContainers


class DetailedJobContainerParser:

    @classmethod
    def get_raw_extra_job_information_object(cls, job_id: int, response: httpx.Response):
        # Attribute occasionally comes up due to page_html not being found.
        # Happens when try to retrieve > 75 pages, causing Cloudflare to activate.
        try:
            page_html = ResponseToContainers.response_to_detailed_job_posting_container(response)
            applicants_raw = cls.get_number_of_applicants_raw(page_html)
            description_raw = cls.get_job_full_description_raw(page_html)

            return RawExtraJobInformation(job_id=job_id,
            number_of_applicants=applicants_raw, description=description_raw)
            
        except AttributeError:
            return RawExtraJobInformation(job_id=job_id,
             number_of_applicants="N/A", description="N/A")



    @staticmethod
    def get_number_of_applicants_raw(details_container: BeautifulSoup) -> str:
        if details_container is None: return ""
        
        applicants_container = details_container.find("div", class_="applications")
        if not applicants_container: 
            applicants_container = details_container.find_all("div", class_="job-info--optional-icons")
            if not applicants_container: return ""
            applicants_container = applicants_container[-1].find("span")
        
        return applicants_container.text.strip()

    @classmethod
    def get_job_full_description_raw(cls, details_container: BeautifulSoup) -> str:
        description_container = details_container.find("span", itemprop="description")
        output_text = ""
        for child in description_container.findChildren():
            output_text = cls._add_text_or_space_depending_on_duplicate(output_text, child.text)
        return output_text.strip()

    @staticmethod
    def _add_text_or_space_depending_on_duplicate(original: str, to_add: str):
        match_value = original.find(to_add)
        if (match_value) == -1:
            original += f"{to_add} "
        else:
            original = original[: match_value] + " " + original[match_value: ]
        
        return original



@dataclass
class RawExtraJobInformation:
    job_id: str
    description: str
    number_of_applicants: str
