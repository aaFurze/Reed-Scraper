
class GetUserInput:

    JOB_TITLE_PROMPT = "\nEnter the Title of the Job you would like to search for: \n"
    LOCATION_PROMPT = "\nEnter the Location which you would like to search for jobs at:\n"
    SEARCH_RADIUS_PROMPT = "\nEnter the radius around the location you would like to search (miles):\n"
    MAX_RESULTS_PROMPT =  "\nEnter the maximum number of results you would like to retrive (rounds down to nearest 25):\n"
    SAVE_NAME_PROMPT = "\nEnter the name of the save file (do not include filetype e.g. .csv)\n"

    def __init__(self) -> None:
        self.job_title = ""
        self.location = ""
        self.search_radius = 0
        self.max_pages = 0
        self.save_name = ""

    @classmethod
    def run_get_input(cls):
        user_input = GetUserInput()
        
        user_input.job_title = cls.clean_input_string(input(cls.JOB_TITLE_PROMPT))
        user_input.location = cls.clean_input_string(input(cls.LOCATION_PROMPT))
        user_input.search_radius = cls.clean_input_int(input(cls.SEARCH_RADIUS_PROMPT))
        user_input.max_pages = cls.clean_input_int(input(cls.MAX_RESULTS_PROMPT))
        user_input.max_pages = int(user_input.max_pages // 25)
        user_input.save_name = cls.clean_input_string(input(cls.SAVE_NAME_PROMPT))

        return user_input


    @staticmethod
    def clean_input_string(dirty: str) -> str:
        output = ""
        for char in dirty.strip():
            if char.isalnum(): output += char
            if char == " " and output[-1] != "-": output += "-"
        return output.strip().lower()
    
    @staticmethod
    def clean_input_int(dirty: str) -> int:
        output_str = ""
        for char in dirty:
            if char.isnumeric(): output_str += char
            if char == ".": break
        return int(output_str)