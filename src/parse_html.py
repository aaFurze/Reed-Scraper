import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://reed.co.uk"


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


def _get_job_data(metadata_panel: BeautifulSoup, container_type: str, class_name: str) -> str:
    if class_name != "":
        container = metadata_panel.find(container_type, class_=class_name)
    else:
        # returns first item by default.
        container = metadata_panel.find(container_type)

    if container:
        return container.text.strip()
    return ""


def get_job_salary_info_raw(metadata_panel: BeautifulSoup) -> str:
    return _get_job_data(metadata_panel, "li", "job-metadata__item--salary")


def get_job_location_raw(metadata_panel: BeautifulSoup) -> str:
    return _get_job_data(metadata_panel, "li", "job-metadata__item--location")


def get_job_tenure_type_raw(metadata_panel: BeautifulSoup) -> str:
    return _get_job_data(metadata_panel, "li", "job-metadata__item--type")


def get_job_remote_status_raw(metadata_panel: BeautifulSoup) -> str:
    remote_status = _get_job_data(metadata_panel, "li", "job-metadata__item--remote")
    if remote_status == "": return "No"
    return remote_status


def get_job_description_start_raw(container: BeautifulSoup) -> str:
    return _get_job_data(container, "p", "job-result-description__details")


def get_job_full_page_link_raw(container: BeautifulSoup):
    return BASE_URL + container.find("a", class_="job-result-card__block-link")["href"]
