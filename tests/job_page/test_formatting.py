import datetime

import pytest

import src.job_page.formatting as formatting


@pytest.fixture
def example_description_raw():
    return """
Software Engineer  *Positions available from junior level up to principal/tech lead level*   
Location:  London- hybrid working   Salary:   £40.000 - £85.000 plus package   
Overview This cutting-edge cyber security firm is one of the top technology organisations when it comes to national defence. 
They operate in four key domains of expertise: Cyber Security, Financial Crime, Communications Intelligence and Digital Transformation.
Working on large central government projects, this Software Engineer role will provide you with diverse experience
 across the public sector and provides great opportunities for progression and
  to develop your career. As a software engineer you would work independently in designing,
   coding, testing and correcting software from given specifications while also
    assisting in the implementation of software which forms part of a properly engineered
     information or communication  system. You will logically analyse code defects and
      produce timely code fixes.  Desired experience:   
      A good understanding of any of the following programming languages: Java, JavaScript,
       React The desire to solve complex technical problems,
        helping our customers achieve their goals Knowledge of some cloud engineering such as
         AWS, Docker, Microservices ect is desirable but not essential
          The ability to work as part of a team, knowledge share and be involved with our
           Agile ways of working  Benefits:   Base salary between £40.000 - £85.000 , 
           based on experience  Car allowance of up to £6.500 Bonus up to 13% based on 
           performance Private medical & Dental  9% Pension (6% company contribution) 
           Flexible hybrid working Long term career plan / fantastic progression 
           Plus additional benefits  * Only those with the permanent and unrestricted right to 
           live and work in the UK will be considered for this role and must have or 
           undergo Government SC clearance prior to starting * 
           Location:LondonSalary: £40.000 - £85.000 plus package   Reference: AMC/SDA/SWEL
    """




class TestFormatDetailedJobData:
    @pytest.mark.parametrize("raw, expected", [("", "10+"),
     ("Be one of the first ten applicants", "<10")])
    def test_format_job_number_of_applicants(self, raw: str, expected: str):
        assert formatting.FormatExtraJobData._format_job_number_of_applicants(raw) == expected

    def test_format_job_description_full_standard(self, example_description_raw: str):
        assert formatting.FormatExtraJobData._format_job_description_full(
            example_description_raw).find("Software Engineer Positions available from junior level up to principal/tech lead level") != -1
