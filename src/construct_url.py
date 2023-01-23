class ConstructUrl:
    BASE_URL = "https://www.reed.co.uk/jobs/"

    @classmethod
    def get_url(cls, job_name: str, location: str, search_radius: int, page_number: int) -> str:
        job_name_segment = ConstructUrl.get_job_name_url_segment(job_name=job_name)
        location_segment = ConstructUrl.get_location_url_segment(location=location)
        search_radius_segment = ConstructUrl.get_search_radius_url_segment(
            search_radius=search_radius)
        page_number_segment = ConstructUrl.get_page_number_url_segment(
            page_number=page_number)

        output_url = cls.BASE_URL + job_name_segment + location_segment
        
        if search_radius_segment or page_number_segment: output_url += "?"

        if search_radius_segment and page_number_segment:
            return output_url + page_number_segment + "&" + search_radius_segment
        
        return output_url + page_number_segment + search_radius_segment

    @staticmethod
    def _basic_clean_input(input_value: str) -> str:
        input_being_cleaned = input_value.strip()
        input_being_cleaned = input_being_cleaned.lower()

        output = ""
        for char in input_being_cleaned:
            if (char.isalnum()):
                output += char
            elif char in [" ", "-"]:
                output += "-"

        return output 

    @staticmethod
    def get_job_name_url_segment(job_name: str) -> str:
        job_name = ConstructUrl._basic_clean_input(job_name)
        if job_name == "": return ""
        return job_name + "-jobs"

    @staticmethod
    def get_location_url_segment(location: str) -> str:
        location = ConstructUrl._basic_clean_input(location)
        if location == "": return ""
        return "-in-" + location

    @staticmethod
    def get_page_number_url_segment(page_number: int) -> str:
        if type(page_number) is str:
            page_number = int(ConstructUrl._basic_clean_input(page_number))

        if page_number == 1: return ""

        return f"pageno={int(page_number)}"

    @staticmethod
    def get_search_radius_url_segment(search_radius: int) -> str:
        if type(search_radius) is str:
             search_radius = int(ConstructUrl._basic_clean_input(search_radius))
        if search_radius == 10: return ""

        return f"proximity={int(search_radius)}"


