from bs4 import BeautifulSoup
import httpx


def soupify_page(response: httpx.Response) -> BeautifulSoup:
    return BeautifulSoup(response.text, "lxml")


def get_job_posting_containers(html: BeautifulSoup):
    return html.find_all("article", class_="job-result-card")


def get_job_title_raw(container: BeautifulSoup):
    title_h2 = container.find("h2", class_="job-result-heading__title")
    return title_h2.find("a").text.strip()

