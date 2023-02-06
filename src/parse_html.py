from __future__ import annotations

from typing import List

import httpx
from bs4 import BeautifulSoup


class ResponseToContainers:
    @staticmethod    
    def soupify_page(response: httpx.Response) -> BeautifulSoup:
        return BeautifulSoup(response.text, "lxml")
    
    @staticmethod
    def soupify_page_html(text: str) -> BeautifulSoup:
        return BeautifulSoup(text, "lxml")

    @staticmethod
    def get_job_summary_containers(html: BeautifulSoup) -> List[BeautifulSoup]:
        return html.find_all("article", class_="job-result-card")
    
    @staticmethod
    def response_to_job_summary_containers(response: httpx.Response) -> List[BeautifulSoup]:
        page = ResponseToContainers.soupify_page(response)
        return ResponseToContainers.get_job_summary_containers(page)

    @staticmethod
    def responses_to_job_posting_containers(responses: List[httpx.Response]) -> List[BeautifulSoup]:
        output = []

        for response in responses:
            page = ResponseToContainers.soupify_page(response)
            output += ResponseToContainers.get_job_summary_containers(page)
        
        return output
    
    @classmethod
    def response_to_detailed_job_posting_container(cls,
     response: httpx.Response) -> BeautifulSoup:
        page = cls.soupify_page(response)
        return cls.get_detailed_job_posting_container(page)


    @staticmethod
    def get_detailed_job_posting_container(html: BeautifulSoup) -> BeautifulSoup:
        standard_container = html.find("div", class_="description-container")
        if not standard_container: 
            return html.find("div", class_="branded-job-details--container")
        return standard_container

