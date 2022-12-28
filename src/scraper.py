from typing import List
import httpx
from bs4 import BeautifulSoup
import asyncio

PAGE_SIZE = 20  # Max number of job posting per page.


# Todo: Currently breaks if search_radius == 10 (default value). Have hack to fix it, but not good.
# Todo: Use a construct url function instead of constructing them in this function. 
def get_job_postings(job_title: str, location: str, search_radius: int = 10, max_pages: int = 1) -> httpx.Response:

    if search_radius == 10: search_radius == 11
    if max_pages <= 0: max_pages = 1

    first_response = _get_first_page(job_title, location, search_radius)

    number_of_job_postings = _get_number_of_job_postings(first_response)
    number_of_pages_to_get = _get_number_of_pages_to_return(number_of_job_postings, max_pages)

    if (number_of_pages_to_get <= 1): return [first_response]

    return [first_response] + asyncio.run(_get_more_pages(job_title, location, search_radius, number_of_pages_to_get, start_page=2))


def _get_first_page(job_title: str, location: str, search_radius: int) -> httpx.Response:
    return httpx.get(f"https://www.reed.co.uk/jobs/{job_title}-jobs-in-{location}?proximity={search_radius}&pageno=1")


async def _get_more_pages(job_title: str, location: str, search_radius: int, no_pages: int, start_page: int = 2) -> List[httpx.Response]:
    output = []
    async with httpx.AsyncClient() as client:
        for i in range(start_page, no_pages + 1):
            response = await client.get(f"https://www.reed.co.uk/jobs/{job_title}-jobs-in-{location}?proximity={search_radius}&pageno={i}")
            output.append(response)
    return output


def _get_number_of_job_postings(response: httpx.Response) -> int:
    soup = BeautifulSoup(response.text, "lxml")
    count_tag_contents: str = soup.find("span", class_="count").text

    number = "".join([char for char in count_tag_contents if char.isnumeric()])
    return int(number.strip())


def _get_number_of_pages_to_return(number_of_jobs: int, max_pages: int) -> int:
    num_pages = (number_of_jobs // PAGE_SIZE)
    if number_of_jobs % PAGE_SIZE != 0: num_pages += 1
    if num_pages > max_pages: return max_pages
    return int(num_pages)