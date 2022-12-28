from bs4 import BeautifulSoup
import httpx


def soupify_page(response: httpx.Response) -> BeautifulSoup:
    return BeautifulSoup(response.text, "lxml")


def get_job_posting_containers(html: BeautifulSoup):
    return html.find_all("article", class_="job-result-card")


def get_job_title(container: BeautifulSoup):
    title_h2 = container.find("h2", class_="job-result-heading__title")
    return title_h2.find("a").text.strip()

def get_job_posted_date_and_employer_info_raw(container: BeautifulSoup):
    date_div = container.find("div", class_="job-result-heading__posted-by")
    return date_div.text.strip()

def get_job_metadata_panel_raw(container: BeautifulSoup) -> BeautifulSoup:
    return container.find("ul", class_="job-metadata")


def _get_job_metadata(metadata_panel: BeautifulSoup, container_type: str, class_name: str):
    if class_name != "": container = metadata_panel.find(container_type, class_=class_name)
    else: container = metadata_panel.find(container_type)  # returns first item by default.

    if container: return container.text.strip()
    return ""

def get_job_salary_info_raw(metadata_panel: BeautifulSoup):
    return _get_job_metadata(metadata_panel, "li", "job-metadata__item--salary")

def get_job_location_raw(metadata_panel: BeautifulSoup):
    return _get_job_metadata(metadata_panel, "li", "job-metadata__item--location")

def get_job_tenure_type_raw(metadata_panel: BeautifulSoup):
    return _get_job_metadata(metadata_panel, "li", "job-metadata__item--type")

def get_job_remote_status_raw(metadata_panel: BeautifulSoup):
    return _get_job_metadata(metadata_panel, "li", "job-metadata__item--remote")

