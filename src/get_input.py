
class GetUserInput:

    JOB_TITLE_PROMPT = "\nEnter the Title of the Job you would like to search for:\n"
    LOCATION_PROMPT = "\nEnter the Location which you would like to search for jobs at:\n"
    SEARCH_RADIUS_PROMPT = "\nEnter the radius around the location you would like to search (miles):\n"
    MAX_RESULTS_PROMPT =  "\nEnter the maximum number of results you would like to retrive (rounds down to nearest 25):\n"
    GET_DESCRIPTION_PROMPT = "\nWould you like to get more detailed description and applicant data? (maximum of first 50 results):\n[Y/y]    [N/n]\n"
    SAVE_NAME_PROMPT = "\nEnter the name of the save file (do not include filetype e.g. .csv):\n"

    def __init__(self) -> None:
        self.job_title = ""
        self.location = ""
        self.search_radius = 0
        self.max_pages = 0
        self.get_description = False
        self.save_name = ""

    @classmethod
    def run_get_input(cls):
        user_input = GetUserInput()
        
        user_input.job_title = cls._clean_input_string(input(cls.JOB_TITLE_PROMPT))
        user_input.location = cls._clean_input_string(input(cls.LOCATION_PROMPT))
        user_input.search_radius = cls._clean_input_int(input(cls.SEARCH_RADIUS_PROMPT))
        user_input.max_pages = cls._clean_input_int(input(cls.MAX_RESULTS_PROMPT))
        user_input.max_pages = int(user_input.max_pages // 25)

        user_input.get_description = input(cls.GET_DESCRIPTION_PROMPT)
        user_input.get_description = True if (user_input.get_description.find("Y") != -1 or 
         user_input.get_description.find("y") != -1) else False

        user_input.save_name = cls._clean_input_string(input(cls.SAVE_NAME_PROMPT))

        return user_input


    @staticmethod
    def _clean_input_string(dirty: str) -> str:
        output = ""
        for char in dirty.strip():
            if char.isalnum(): output += char
            if char == " " and output[-1] != "-": output += "-"
        return output.strip().lower()
    
    @staticmethod
    def _clean_input_int(dirty: str) -> int:
        output_str = ""
        for char in dirty:
            if char.isnumeric(): output_str += char
            if char == ".": break
        return int(output_str)