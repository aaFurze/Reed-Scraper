import asyncio
from typing import List

import httpx
from bs4 import BeautifulSoup
from typing_extensions import Protocol

from src.construct_url import (ConstructJobPageUrl, ConstructSearchPageUrl,
                               UrlConstructor)

PAGE_SIZE = 25  # Max number of job posting per page.   


class ReedSearchPageScraper:
    URL_CONSTRUCTOR: UrlConstructor = ConstructSearchPageUrl
    DEFAULT_TIMEOUT_OBJ = httpx.Timeout(timeout=15.0)

    @classmethod
    def get_job_postings(cls, job_title: str, location: str, search_radius: int = 10,
     max_pages: int = 1) -> List[httpx.Response]:
        print(f"""base url = {ConstructSearchPageUrl.get_url(job_name=job_title, location=location,
         search_radius=search_radius, page_number=1)}""")
        if max_pages <= 0: max_pages = 1
        first_response = cls._get_first_page(job_title, location, search_radius)

        number_of_job_postings = cls._get_number_of_job_postings(first_response)
        number_of_pages_to_get = cls._get_number_of_pages_to_return(number_of_job_postings, max_pages)

        if (number_of_pages_to_get <= 1): return [first_response]

        return [first_response] + asyncio.run(cls._get_more_pages(job_title, location, search_radius, number_of_pages_to_get, start_page=2))

    @classmethod
    def _get_first_page(cls, job_title: str, location: str, search_radius: int) -> httpx.Response:
        return httpx.get(cls.URL_CONSTRUCTOR.get_url(job_name=job_title,
         location=location, search_radius=search_radius, page_number=1), timeout=cls.DEFAULT_TIMEOUT_OBJ)

    @classmethod
    async def _get_more_pages(cls, job_title: str, location: str, search_radius: int, no_pages: int, start_page: int = 2) -> List[httpx.Response]:
        output = []
        async with httpx.AsyncClient() as client:
            for page_number in range(start_page, no_pages + 1):
                print(f"Retrieving page {page_number}.")
                response = await client.get(cls.URL_CONSTRUCTOR.get_url(
                    job_name=job_title, location=location, search_radius=search_radius,
                     page_number=page_number), timeout=cls.DEFAULT_TIMEOUT_OBJ)
                output.append(response)
        return output

    @staticmethod
    def _get_number_of_job_postings(response: httpx.Response) -> int:
        soup = BeautifulSoup(response.text, "lxml")
        count_tag_contents: str = soup.find("span", class_="count").text

        number = "".join([char for char in count_tag_contents if char.isnumeric()])
        return int(number.strip())

    @staticmethod
    def _get_number_of_pages_to_return(number_of_jobs: int, max_pages: int) -> int:
        num_pages = (number_of_jobs // PAGE_SIZE)
        if number_of_jobs % PAGE_SIZE != 0: num_pages += 1
        if num_pages > max_pages: return max_pages
        return int(num_pages)


"""
TODO: Add limit to number of pages can retrive (~= 50). Retrieving too many does not work
as Reed has Cloudflare for > 75 visits in a short period.
"""
class ReedJobPageScraper:

    URL_CONSTRUCTOR = ConstructJobPageUrl
    DEFAULT_TIMEOUT_OBJ = httpx.Timeout(timeout=15.0)

    @classmethod
    def get_job_pages(cls, job_ids: List[int]) -> List[httpx.Response]:
        return asyncio.run(cls._get_job_pages_responses(job_ids))

    @classmethod
    async def _get_job_pages_responses(cls, job_ids: List[int]) -> List[httpx.Response]:
        output = []
        cloudflare_limit_counter = 0
        
        async with httpx.AsyncClient() as client:
            for job_id in job_ids:

                cloudflare_limit_counter += 1
                if cloudflare_limit_counter == 50: print("Page Limit reached. Cannot retrieve any more detailed job description and applicants information. Normal information will still be collected.")
                if cloudflare_limit_counter > 50: 
                    output.append("")
                    continue

                print(f"Retrieving job (id={job_id}).")
                response = await client.get(cls.URL_CONSTRUCTOR.get_url(job_id),
                 timeout=cls.DEFAULT_TIMEOUT_OBJ)
                output.append(response)
        return output
