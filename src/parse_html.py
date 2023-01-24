from __future__ import annotations

from dataclasses import dataclass
from typing import List

import httpx
from bs4 import BeautifulSoup


class ResponseToContainers:
    @staticmethod    
    def soupify_page(response: httpx.Response) -> BeautifulSoup:
        return BeautifulSoup(response.text, "lxml")

    @staticmethod
    def get_job_posting_containers(html: BeautifulSoup) -> List[BeautifulSoup]:
        return html.find_all("article", class_="job-result-card")
    
    @staticmethod
    def response_to_job_posting_containers(response: httpx.Response) -> List[BeautifulSoup]:
        page = ResponseToContainers.soupify_page(response)
        return ResponseToContainers.get_job_posting_containers(page)

    @staticmethod
    def responses_to_job_posting_containers(responses: List[httpx.Response]) -> List[BeautifulSoup]:
        output = []

        for response in responses:
            page = ResponseToContainers.soupify_page(response)
            output += ResponseToContainers.get_job_posting_containers(page)
        
        return output


class JobContainerParser:
    @staticmethod
    def get_job_title(container: BeautifulSoup) -> str:
        title_h2 = container.find("h2", class_="job-result-heading__title")
        return title_h2.find("a").text.strip()

    @staticmethod
    def get_job_posted_date_and_employer_info_raw(container: BeautifulSoup) -> str:
        date_div = container.find("div", class_="job-result-heading__posted-by")
        return date_div.text.strip()

    @staticmethod
    def _get_job_metadata_panel_raw(container: BeautifulSoup) -> BeautifulSoup:
        return container.find("ul", class_="job-metadata")

    @staticmethod
    def _get_job_metadata(metadata_panel: BeautifulSoup, container_type: str, class_name: str) -> str:
        if class_name != "":
            container = metadata_panel.find(container_type, class_=class_name)
        else:
            # returns first item with specified html tag by default.
            container = metadata_panel.find(container_type)

        if container:
            return container.text.strip()
        return ""

    @staticmethod
    def get_job_salary_info_raw(metadata_panel: BeautifulSoup) -> str:
        return JobContainerParser._get_job_metadata(metadata_panel, "li", "job-metadata__item--salary")

    @staticmethod
    def get_job_location_raw(metadata_panel: BeautifulSoup) -> str:
        return JobContainerParser._get_job_metadata(metadata_panel, "li", "job-metadata__item--location")

    @staticmethod
    def get_job_tenure_type_raw(metadata_panel: BeautifulSoup) -> str:
        return JobContainerParser._get_job_metadata(metadata_panel, "li", "job-metadata__item--type")

    @staticmethod
    def get_job_remote_status_raw(metadata_panel: BeautifulSoup) -> str:
        remote_status = JobContainerParser._get_job_metadata(metadata_panel, "li", "job-metadata__item--remote")
        if remote_status == "": return "no"
        return remote_status

    @staticmethod
    def get_job_description_start_raw(container: BeautifulSoup) -> str:
        return JobContainerParser._get_job_metadata(container, "p", "job-result-description__details")

    @staticmethod
    def get_job_full_page_link_raw(container: BeautifulSoup) -> str:
        return container.find("a", class_="job-result-card__block-link")["href"]

    @staticmethod
    def get_job_id_raw(container: BeautifulSoup) -> str:
        url = container.find("a", class_="job-result-card__block-link")["href"]
        url_until_id_end = url[:url.find("?")]
        return url_until_id_end[url_until_id_end.rfind("/"):]


class RawJobInformationFactory:
    @staticmethod
    def get_empty_raw_job_info() -> RawJobInformation:
        return RawJobInformation("", "", "", "", "", "", "", "", "")

    @staticmethod
    def get_x_empty_raw_job_info_objects(x: int) -> List[RawJobInformation]:
        return [RawJobInformationFactory.get_empty_raw_job_info() for _ in range(x)]

    @staticmethod
    def populate_raw_job_information_from_job_container(destination: RawJobInformation, container: BeautifulSoup) -> RawJobInformation:
        destination.title = JobContainerParser.get_job_title(container)
        destination.date_and_employer = JobContainerParser.get_job_posted_date_and_employer_info_raw(container)

        metadata_panel = JobContainerParser._get_job_metadata_panel_raw(container)

        destination.salary = JobContainerParser.get_job_salary_info_raw(metadata_panel=metadata_panel)
        destination.location = JobContainerParser.get_job_location_raw(metadata_panel=metadata_panel)
        destination.tenure_type = JobContainerParser.get_job_tenure_type_raw(metadata_panel=metadata_panel)
        destination.remote_status = JobContainerParser.get_job_remote_status_raw(metadata_panel=metadata_panel)

        destination.full_page_link = JobContainerParser.get_job_full_page_link_raw(container)
        destination.description_start = JobContainerParser.get_job_description_start_raw(container)
        destination.job_id = JobContainerParser.get_job_id_raw(container)

        return destination

    @staticmethod
    def get_multiple_populated_raw_job_info_objects(responses: List[httpx.Response]) -> List[RawJobInformation]:
        containers = ResponseToContainers.responses_to_job_posting_containers(responses)
        raw_job_info_objects = RawJobInformationFactory.get_x_empty_raw_job_info_objects(len(containers))
        for i in range(len(containers)):
            RawJobInformationFactory.populate_raw_job_information_from_job_container(raw_job_info_objects[i], containers[i])

        return raw_job_info_objects




@dataclass
class RawJobInformation:
    job_id: str
    title: str
    date_and_employer: str
    salary: str
    location: str
    tenure_type: str
    remote_status: str
    description_start: str
    full_page_link: str
