from src.construct_url import UrlConstructor


class ConstructJobPageUrl(UrlConstructor):
    BASE_URL = "https://www.reed.co.uk/jobs/job/"
    @classmethod
    def get_url(cls, job_id: int) -> str:
        return cls.BASE_URL + str(job_id)
