import pytest

from src.job_page import ConstructJobPageUrl


class TestConstructJobPageUrl:
    @pytest.mark.parametrize("job_id", [423423, 324234, 32423, 909432901778])
    def test_get_url_contains_job_id(self, job_id):
        assert ConstructJobPageUrl.get_url(job_id=job_id).find(str(job_id)) != -1

    def test_get_url_contains_base_url(self):
        assert ConstructJobPageUrl.get_url(43234).find(ConstructJobPageUrl.BASE_URL) != -1

