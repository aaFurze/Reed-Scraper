from __future__ import annotations

from dataclasses import dataclass
from typing import List

from typing_extensions import Protocol


class RawExtraJobInformation(Protocol):
    job_id: str
    description: str
    number_of_applicants: str


@dataclass
class FormattedExtraJobInformation:
    job_id: str
    number_of_applicants: str
    description: str

    def to_list(self) -> List[str]:
        return [self.job_id, self.number_of_applicants, self.description]



class FormatExtraJobData:

    VALID_SYMBOLS = [".", "-", ",", ":", ";", "£", "$", "€", "&", "%", "(", ")", "/"]

    @classmethod
    def raw_to_formatted_extra_job_information(cls, raw: RawExtraJobInformation):
        number_of_applicants = FormatExtraJobData._format_job_number_of_applicants(
            raw.number_of_applicants)
        description = FormatExtraJobData._format_job_description_full(raw.description)

        return FormattedExtraJobInformation(job_id=raw.job_id,
        description=description, number_of_applicants=number_of_applicants)

    @staticmethod
    def _format_job_number_of_applicants(applicants_raw: str) -> str:
        if applicants_raw == "Be one of the first ten applicants": return "<10"
        if applicants_raw == "": return "10+"
        return applicants_raw

    @classmethod
    def _format_job_description_full(cls, description_raw: str):
        output = ""
        for char in description_raw:
            if not cls._is_valid_char(char): continue
            if char == " " and output[-1] == " ": continue
            output += char
            if char == ":": output += " "

        return output
    
    @classmethod
    def _is_valid_char(cls, char: str):
        if char.isalnum(): return True
        if char in cls.VALID_SYMBOLS: return True
        if char == " ": return True
        return False
