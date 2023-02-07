import asyncio
from typing import List

import httpx

from src.construct_url import UrlConstructor
from src.job_page.construct_url import ConstructJobPageUrl


class ReedJobPageScraper:

    URL_CONSTRUCTOR: UrlConstructor = ConstructJobPageUrl
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
                if cloudflare_limit_counter == 51: print("Page Limit reached. Cannot retrieve any more detailed job description and applicants information. Other job information will still be collected.")
                if cloudflare_limit_counter > 50: 
                    output.append("")
                    continue

                print(f"Retrieving job (id={job_id}).")
                response = await client.get(cls.URL_CONSTRUCTOR.get_url(job_id),
                 timeout=cls.DEFAULT_TIMEOUT_OBJ)
                output.append(response)
        return output
