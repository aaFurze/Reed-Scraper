# Reed-Scraper

A program that scrapes job postings from reed.co.uk, aggregates them, and outputs them to a spreadsheet (.csv)
Program tests run using pytest.

# Contents

###  * What this WebScraper does
###  * Pre-requisites/Requirements to use the WebScraper
###  * Using the Scraper

  
  
   
<br/><br/><br/>

# What This WebScraper Does
This webscraper scrapes Reed Job posting data of the following types: 
- job_id -                ID assigned to the job by Reed.co.uk
- job_title -            Listed roles name
- date -                 Date the job was posted to Reed.co.uk 
- employer -             Name of the employer or recruitment agency that posted the job      
- salary_lower -          Minimum pay for the role
- salary_upper -         Maximum pay for the role
- salary_type -           Type of salary (e.g. competitive, annual, daily)
- location -              Location of the job 
- tenure_type -           Tenure type (e.g. Permanent, Contract)
- remote_status -         Is the job listed as Work from Home?
- description_start -     First 250 letters of the job's description
- full_page_link -        Link to the job postings page 

Additionally, up to 50* job postings can have the following data retrieved:
- number_of_applicants -  Number of applicants that have applied to the job (either <10 or 10+)
- description -           Full description of the job

This data is saved in a .csv format. This format should easily viewed in common spreadsheet programs such as Microsoft Excel and Google Sheets.
<br/><br/>

*Actual number of postings may be slightly lower. This limit is in place to prevent the program triggering CloudFlare anti-DDOS systems.
<br/><br/>

# Pre-requisites/Requirements to use the WebScraper

- Python version 3.7+ (Program originally written using Python 3.9.0 interpreter)
- A standard Command line/prompt or Console (for setting up and running the program)

### Setting up the Virtual Environment
It is good practice to create a virtual environment for this project (and for any other project with non-standard-library dependencies).
See this guide for how to setup and activate a virtual environment: [Python docs](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment "Python docs")

NOTE: Ensure that you activate the environment once you have created it (See Python docs)

To install the relevant packages, select the directory that requirements.txt is in and run the following command:
```
pip install -r requirements.txt
```

To check that all the packages have been installed, run the following command:
```
pip list
```
This should produce an output that looks contains these items
```
Package           Version
----------------- -----------
anyio             3.6.2      
attrs             22.2.0     
beautifulsoup4    4.11.1     
black             22.12.0    
bs4               0.0.1      
certifi           2022.12.7  
click             8.1.3      
colorama          0.4.6      
coverage          7.0.1      
exceptiongroup    1.1.0      
h11               0.14.0
httpcore          0.16.3
httpx             0.23.1
idna              3.4
iniconfig         1.1.1
lxml              4.9.2
mypy-extensions   0.4.3
numpy             1.24.1
packaging         22.0
pandas            1.5.2
pathspec          0.10.3
pip               22.3.1
platformdirs      2.6.0
pluggy            1.0.0
pytest            7.2.0
python-dateutil   2.8.2
pytz              2022.7
rfc3986           1.5.0
setuptools        49.2.1
six               1.16.0
sniffio           1.3.0
soupsieve         2.3.2.post1
tomli             2.0.1
typing_extensions 4.4.0
```

If all of these commands were executed successfully, you can now use the Scraper.

<br/>
<br/>

# Using the Scraper

To use the Scraper:

- Open a Command prompt
- Navigate to the folder that contains the program (Should contain the following files):
```
README.md  data/  main.py  requirements.txt  src/  tests/
```
- Make sure you have activated the virtual environment created in the previous section. [See Python Docs](https://docs.python.org/3/tutorial/venv.html "Python docs")
- Run main.py and follow the prompts raised by the program.
- A csv file will be created in the /data folder in the project.

NOTE: Sometimes, an empty csv file will be created. This signals that no job postings were found that matched your criteria. Consider re-running the program and relaxing the criteria you use to filter job applications.

Thank you for using my Scraper!

END
