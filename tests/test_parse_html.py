from typing import List

import httpx
import pytest
from bs4 import BeautifulSoup

from src.parse_html import (DetailedJobContainerParser, JobContainerParser,
                            RawJobInformation, RawJobInformationFactory,
                            ResponseToContainers)
from src.scraper import ReedJobPageScraper, ReedSearchPageScraper


@pytest.fixture(scope="module")
def get_page_html() -> List[httpx.Response]:
    return ReedSearchPageScraper.get_job_postings(job_title="software-engineer", location="leeds", search_radius=25, max_pages=1)[0]

@pytest.fixture(scope="module")
def get_soupified_page(get_page_html) -> BeautifulSoup:
    return ResponseToContainers.soupify_page(get_page_html)

@pytest.fixture(scope="module")
def get_job_containers(get_soupified_page) -> List[BeautifulSoup]:
    return ResponseToContainers.get_job_summary_containers(get_soupified_page)

@pytest.fixture
def get_job(get_job_containers):
    return get_job_containers[0]

@pytest.fixture
def get_raw_job_information(get_job) -> RawJobInformation:
    return RawJobInformationFactory.populate_raw_job_information_from_job_container(RawJobInformationFactory._get_empty_raw_job_info(), get_job)




@pytest.fixture
def job_page_detailed_html() -> BeautifulSoup:
    detailed_job_description_mock = """
<div class="description-container row ">
<div class="col-xs-12 col-sm-8 col-md-9">

    <div data-qa="recruiterLogoLnk" class="logo-profile-mobile visible-xs-block">
        <a class="logo-wrap--border-bottom" data-gtm-value="recruiter_logo_click" href="/jobs/anson-mccade-ltd-it-and-finance-recruitment/p24742">
            <img src="https://resources.reed.co.uk/profileimages/logos/thumbs/Logo_24742.png?v=20230125133604" alt="Posted by Anson McCade Ltd - IT and Finance Recruitment" class=" b-loaded" style="display: block;">
        </a>

    </div>

<div class="hidden-xs">

    <meta itemprop="industry" content="Information Technology">
    <meta itemprop="url" content="https://www.reed.co.uk/jobs/software-engineer/49341027">
    <div class="metadata container container-max-width-modifier">
        <div class="salary col-xs-12 col-sm-6 col-md-6 col-lg-6">
            <i class="icon icon-pound"></i>
                <span itemprop="baseSalary" itemscope="" itemtype="http://schema.org/MonetaryAmount">
                    <meta itemprop="currency" content="GBP">
                    <span data-qa="salaryLbl">£40,000 - £85,000 per annum</span>
                        <span itemprop="value" itemscope="" itemtype="http://schema.org/QuantitativeValue">

                                <meta itemprop="minValue" content="40000.00">
                                <meta itemprop="maxValue" content="85000.00">

                                    <meta itemprop="unitText" content="YEAR">

                        </span>
                </span>

        </div>
        <div class="location col-xs-12 col-sm-6 col-md-6 col-lg-6">
                    <i class="icon icon-location-new"></i>
                    <span id="jobCountry" value="England"></span>
                        <span>
                            <a href="/jobs/jobs-in-leeds" itemprop="jobLocation" itemscope="" itemtype="http://schema.org/Place">
                                <span itemprop="address" itemscope="" itemtype="http://schema.org/PostalAddress">
                                    <meta itemprop="addressRegion" content="West Yorkshire">
                                    <span itemprop="addressLocality" data-qa="regionLbl">Leeds</span>
                                    <meta itemprop="addressCountry" content="GB">
                                </span>
                            </a>, <span data-qa="localityLbl">West Yorkshire</span>
                        </span>

        </div>

        <div class="time col-xs-12 col-sm-6 col-md-6 col-lg-6">
            <i class="icon icon-clock"></i>
                <span itemprop="employmentType" data-qa="jobTypeLbl" content="FULL_TIME">
                    <a href="/jobs/permanent">Permanent</a>,
                        <a href="/jobs/full-time">
                            full-time
                        </a>
                                                        </span>

        </div>



            <div class="applications col-xs-12 col-sm-6 col-md-6 col-lg-6">
                <i class="icon icon-applicants"></i>
                Be one of the first ten applicants
            </div>

    </div>
</div>
<div class="description">

    <div class="hidden-xs">
            <div class="apply-options text-center top visible-xs-block ">

                    <button class="btn btn-primary apply-btn gtmJobDetailsApplyTop gtmJobseekerRegistrationFunnelClick" id="applyButtonDescriptionTop" data-qa="applyBtn" data-bind="text: draft.applyButtonText(), click: jobApplication.applyForJob, clickBubble: false" data-vpv="/vpv/first_app/on_site/responsive">Apply now</button>
            </div>
    </div>

        <span itemprop="description"> <p><strong>Software Engineer</strong></p> <p><strong>*Positions available from junior level up to principal/tech lead level*</strong></p> <p><strong>Location: London- hybrid working <br><strong>Salary: </strong><strong>£40.000 - £85.000 plus package </strong></strong></p> <p><strong>Overview</strong></p> <p>This cutting-edge cyber security firm is one of the top technology organisations when it comes to national defence. They operate in four key domains of expertise: Cyber Security, Financial Crime, Communications Intelligence and Digital Transformation.<br>Working on large central government projects, this Software Engineer role will provide you with diverse experience across the public sector and provides great opportunities for progression and to develop your career.</p> <p>As a software engineer you would work independently in designing, coding, testing and correcting software from given specifications while also assisting in the implementation of software which forms part of a properly engineered information or communication  system. You will logically analyse code defects and produce timely code fixes.</p> <p><strong>Desired experience:</strong><strong><br><br></strong></p> <ul> <li>A good understanding of any of the following programming languages: Java, JavaScript, React</li><li>The desire to solve complex technical problems, helping our customers achieve their goals</li><li>Knowledge of some cloud engineering such as AWS, Docker, Microservices ect is desirable but not essential</li><li>The ability to work as part of a team, knowledge share and be involved with our Agile ways of working</li></ul> <p><strong>Benefits:</strong></p> <ul> <li>Base salary between £40.000 - £85.000 , based on experience </li><li>Car allowance of up to £6.500</li><li>Bonus up to 13% based on performance</li><li>Private medical &amp; Dental </li><li>9% Pension (6% company contribution)</li><li>Flexible hybrid working</li><li>Long term career plan / fantastic progression</li><li>Plus additional benefits</li></ul> <p><strong>* Only those with the permanent and unrestricted right to live and work in the UK will be considered for this role and must have or undergo Government SC clearance prior to starting *</strong></p> <p><strong>Software Engineer</strong></p> <p><strong>Location:</strong><strong>London</strong><br><strong>Salary: </strong><strong>£40.000 - £85.000 plus package </strong></p> <p><br><strong>Reference: </strong>AMC/SDA/SWEL</p> </span>
</div>

    <div class="application-box">
<form action="/jobs/software-engineer/49341027#apply-form" data-bind="submit: jobApplication.sendApplication" id="apply-form" method="post" novalidate="novalidate">            <input type="hidden" name="InternalApplicationSource" value="searchResults">
<input name="__RequestVerificationToken" type="hidden" value="fo4kxuePArLXTqkeHnlRqwkOtVEIf0yAymNNuaCdsc3UNO0Z4TlwhImWlcDmYQpLiQSUeCUYaO3YfYiP08sijz2EDTQ1">


<section class="cv-coverletter-externalapplication" data-bind="visible: jobApplication.showApplyBox()" style="display:none;">

<input data-val="true" data-val-number="The field JobId must be a number." data-val-required="The JobId field is required." id="JobId" name="JobId" type="hidden" value="49341027">
<input id="Source" name="Source" type="hidden" value="searchResults">
<input data-val="true" data-val-required="The UserHasRegisteredThroughJob field is required." id="UserHasRegisteredThroughJob" name="UserHasRegisteredThroughJob" type="hidden" value="False">
</section>




            <div class="apply-options text-center " data-bind="visible: !jobApplication.showApplyBox()">

                    <button type="button" class="btn btn-primary apply-button gtmJobDetailsApplyBottom gtmJobseekerRegistrationFunnelClick" id="applyButtonDescriptionBottom" data-qa="applyBtn" data-bind="text: draft.applyButtonText(), click: jobApplication.applyForJob, clickBubble: false, visible: !jobApplication.showApplyBox()" data-vpv="/vpv/first_app/on_site/responsive">Apply now</button>


                <div class="secondary-btns visible-xs-block">
                            <button data-qa="shortListMobileBtn" class="btn btn-secondary saved-jobs-button gtmShortlistSignInRegisterModal gtmJobDetailsSaveJob" data-bind="click: modifyShortlistStatus, css: { 'gtmJobDetailsSaveJob': !savedJob.isSavedJob(), 'has-saved-job': savedJob.isSavedJob() }">
            <i class="icon"></i>
            <span style="display:none" data-bind="visible: savedJob.isSavedJob()">Saved</span>
            <span style="" data-bind="visible: !savedJob.isSavedJob()">Save</span>
        </button>


                    
                    <button type="button" class="btn btn-secondary email-job-button gtmJobDetailsEmail" data-bind="click: showEmailJob">
                        <i class="icon icon-share"></i>
                        Share job
                    </button>
                </div>
            </div>
</form></div>


<div class="warning-and-report">
    <p class="reference ">Reference: 49341027</p>

    <p class="warning">To stay safe in your job search and flexible work, we recommend that you visit <a href="http://www.jobsaware.co.uk/" rel="nofollow" target="_blank">JobsAware</a>, a non-profit, joint industry and law enforcement organisation working to combat labour market abuse. Visit the JobsAware website for information and to get free, expert advice for safer work.</p>

    <a class="report-job-link" href="#" title="Report this job" data-bind="click: reportJob">Report this job</a>
</div>

<div class="job-alert-container">
        <div class="job-alert-button-container">
            <button class="btn btn-secondary" data-bind="click: t1RegisterJobAlert">
                <i class="icon icon-bell-new-piccadilly-blue"></i> Get Job Alerts
            </button>
        </div>
</div>

<div class="job-details-footer visible-xs">
</div>
</div>

<aside class="logo-and-options hidden-xs col-sm-4 col-md-3">

        <div class="apply-options text-center " data-bind="visible: !jobApplication.showApplyBox()">
                <button class="btn btn-primary easy-apply-button side gtmJobDetailsApplySide gtmJobseekerRegistrationFunnelClick" id="applyButtonSide" data-qa="applyBtn" data-bind="click: jobApplication.sendApplication, clickBubble: false, visible: !jobApplication.showApplyBox()" data-vpv="/vpv/first_app/on_site/responsive">
                    Apply now
                </button>
                <div class="easy-apply-caption">
                    <p class="easy-apply-caption__cv"><a href="#" title="Register" data-bind="click: jobApplication.sendApplication, clickBubble: false">Register</a> and upload your CV to apply with just one click</p>
                </div>

                    <button data-qa="shortListBtn" class="btn btn-secondary saved-jobs-button gtmShortlistSignInRegisterModal gtmJobDetailsSaveJob" data-bind="click: modifyShortlistStatus, css: { 'gtmJobDetailsSaveJob': !savedJob.isSavedJob(), 'has-saved-job': savedJob.isSavedJob() }">
            <i class="icon"></i>
            <span style="display:none" data-bind="visible: savedJob.isSavedJob()">Saved</span>
            <span style="" data-bind="visible: !savedJob.isSavedJob()">Save</span>
        </button>


            
            <button class="btn btn-secondary email-job-button gtmJobDetailsEmail" data-qa="shareJobBtn" data-bind="click: showEmailJob">
                <i class="icon icon-share"></i>
                Share job
            </button>
        </div>

    <div class="logo-profile hidden-xs text-center">
        <a class="logo-wrap logo-wrap--border-bottom" data-qa="recruiterLogoLnk" data-gtm-value="recruiter_logo_click" href="/jobs/anson-mccade-ltd-it-and-finance-recruitment/p24742">
                <meta itemprop="image" content="https://resources.reed.co.uk/profileimages/logos/thumbs/Logo_24742.png?v=20230125133604">
                <img src="https://resources.reed.co.uk/profileimages/logos/thumbs/Logo_24742.png?v=20230125133604" alt="Posted by Anson McCade Ltd - IT and Finance Recruitment" width="120" height="50" class=" b-loaded" style="display: inline;">
        </a>

        <a class="find-out-more-link" data-qa="viewAllJobsLnk" data-gtm-value="recuiter_find_out_more_click" href="/jobs/anson-mccade-ltd-it-and-finance-recruitment/p24742">View all jobs <i class="icon icon-arrow-thin-blue-right"></i></a>

    </div>

    <div class="similar-jobs hidden-xs hidden-md hidden-lg">
        

    <section class="list-group-container list-group-jobseeker similar-jobs-container" data-qa="similarJobsSec">
            <header class="list-group-header">
                <h4 class="list-group-title">Similar jobs</h4>
            </header>
            <div class="list-group">
                        <script type="text/javascript">
                                        
                                            dataLayer.push({ allpagesPromotedJobID1: 49627154 });
                                        

                        </script>
                        <a href="/jobs/software-engineer/49627154?source=details.similarjobs" title="Software Engineer" class="list-group-item gtmSimilarJob promoted_similar_job">
                            <span class="list-group-item-heading">Software Engineer</span>
                                <span class="list-group-item-text extra-field-1">Competitive salary</span>
                                                            <span class="list-group-item-text extra-field-2">Leeds, West Yorkshire</span>
                        </a>
                        <script type="text/javascript">

                        </script>
                        <a href="/jobs/web-developer/48202858?source=details.similarjobs" title="Web Developer" class="list-group-item gtmSimilarJob standard_similar_job">
                            <span class="list-group-item-heading">Web Developer</span>
                                <span class="list-group-item-text extra-field-1">£25,000 - £35,000 per annum</span>
                                                            <span class="list-group-item-text extra-field-2">Halifax, West Yorkshire</span>
                        </a>
                        <script type="text/javascript">

                        </script>
                        <a href="/jobs/software-engineer/49563423?source=details.similarjobs" title="Software Engineer" class="list-group-item gtmSimilarJob standard_similar_job">
                            <span class="list-group-item-heading">Software Engineer</span>
                                <span class="list-group-item-text extra-field-1">£40,000 - £60,000 per annum</span>
                                                            <span class="list-group-item-text extra-field-2">Leeds, West Yorkshire</span>
                        </a>
                        <script type="text/javascript">

                        </script>
                        <a href="/jobs/software-engineer/49563393?source=details.similarjobs" title="SOFTWARE ENGINEER" class="list-group-item gtmSimilarJob standard_similar_job">
                            <span class="list-group-item-heading">SOFTWARE ENGINEER</span>
                                <span class="list-group-item-text extra-field-1">£38,000 - £55,000 per annum</span>
                                                            <span class="list-group-item-text extra-field-2">Leeds, West Yorkshire</span>
                        </a>
                        <script type="text/javascript">

                        </script>
                        <a href="/jobs/software-engineer/49563423?source=details.similarjobs" title="Software Engineer" class="list-group-item gtmSimilarJob standard_similar_job">
                            <span class="list-group-item-heading">Software Engineer</span>
                                <span class="list-group-item-text extra-field-1">£40,000 - £60,000 per annum</span>
                                                            <span class="list-group-item-text extra-field-2">Leeds, West Yorkshire</span>
                        </a>
                        <script type="text/javascript">

                        </script>
                        <a href="/jobs/software-engineer/49563391?source=details.similarjobs" title="SOFTWARE ENGINEER" class="list-group-item gtmSimilarJob standard_similar_job">
                            <span class="list-group-item-heading">SOFTWARE ENGINEER</span>
                                <span class="list-group-item-text extra-field-1">£40,000 - £60,000 per annum</span>
                                                            <span class="list-group-item-text extra-field-2">Leeds, West Yorkshire</span>
                        </a>
                        <script type="text/javascript">

                        </script>
                        <a href="/jobs/c-software-engineer/49402047?source=details.similarjobs" title="C++ Software Engineer" class="list-group-item gtmSimilarJob standard_similar_job">
                            <span class="list-group-item-heading">C++ Software Engineer</span>
                                <span class="list-group-item-text extra-field-1">£40,000 - £60,000 per annum</span>
                                                            <span class="list-group-item-text extra-field-2">Leeds, West Yorkshire</span>
                        </a>
                    <script type="text/javascript">
                        localStorage.setItem('jobIdsSavedSimilar', [49627154]);
                    </script>

            </div>
    </section>


    </div>
    <div class="courses hidden-xs hidden-md hidden-lg">
        <div class="recommended-courses-panel">



    <section class="list-group-container recommended-courses-container">
        <header class="list-group-header">
            <h4 class="list-group-title">Recommended courses</h4>
        </header>
        <div class="list-group">
                    <a href="/courses/case--certified-application-security-engineer-official-ec-council-training/229783?itm_source=js_job_details&amp;itm_medium=jobseeker&amp;itm_campaign=recommended_courses_panel&amp;itm_content=it security_courses_229783" title="CASE | Certified Application Security Engineer  - Official EC-Council Training" class="list-group-item gtmJobDetailsCourseLink">
                        <span class="list-group-item-heading">CASE | Certified Application Security Engineer  - Official EC-Council Training</span>
                            <span class="list-group-item-text extra-field-1">Online, Self-paced</span>
                                                    <span class="list-group-item-text extra-field-2">Enquire to get more info on pricing</span>
                    </a>
                    <a href="/courses/certified-secure-web-application-engineer-cswae/219786?itm_source=js_job_details&amp;itm_medium=jobseeker&amp;itm_campaign=recommended_courses_panel&amp;itm_content=it security_courses_219786" title="Certified Secure Web Application Engineer (CSWAE)" class="list-group-item gtmJobDetailsCourseLink">
                        <span class="list-group-item-heading">Certified Secure Web Application Engineer (CSWAE)</span>
                            <span class="list-group-item-text extra-field-1">Online, Self-paced</span>
                                                    <span class="list-group-item-text extra-field-2">£149</span>
                    </a>
                    <a href="/courses/certified-incident-handling-engineer-cihe/222056?itm_source=js_job_details&amp;itm_medium=jobseeker&amp;itm_campaign=recommended_courses_panel&amp;itm_content=it security_courses_222056" title="Certified Incident Handling Engineer (CIHE)" class="list-group-item gtmJobDetailsCourseLink">
                        <span class="list-group-item-heading">Certified Incident Handling Engineer (CIHE)</span>
                            <span class="list-group-item-text extra-field-1">Online, Self-paced</span>
                                                    <span class="list-group-item-text extra-field-2">£149</span>
                    </a>

                <a class="list-group-item course-search-link" href="https://www.reed.co.uk/courses/it-security?itm_source=js_job_details&amp;itm_medium=jobseeker&amp;itm_campaign=recommended_courses_panel&amp;itm_content=view_it security_courses" title="View IT security courses" data-gtm="all_subject_courses_link" data-gtm-value="jobseeker_responsive">
                    View IT security courses
                    <span class="icon icon-arrow-blue-right"></span>
                </a>
        </div>
    </section>
</div>


    </div>
</aside>
</div>
"""
    return ResponseToContainers.soupify_page_html(detailed_job_description_mock)

@pytest.fixture
def job_page_detailed_html_promotional() -> BeautifulSoup:
    detailed_job_description_promotion_mock = """

    <div class="branded-job-details--container">
        <div class="row">
            <div class="branded-job--labels col-md-6 col-sm-6 col-xs-12">


<span class="label label-new">New</span>

<span class="label label-featured">Featured</span>
            </div>
            <div class="branded-job--labels col-md-6 col-sm-6 hidden-xs">

            </div>
        </div>
        <div class="job-header row">
            <div class="col-md-12">
                <div class="job-info--container">
                    <h1>Software Engineer</h1>
                    <meta itemprop="title" content="Software Engineer">
                    <div class="posted">
                        <meta itemprop="datePosted" content="2023-01-25">
                        <meta itemprop="validThrough" content="2023-03-08T23:55:00.0000000">
                            <span itemprop="hiringOrganization" itemscope="" itemtype="http://schema.org/Organization">
                                Posted Today by <a href="/company-profile/BJSS-58381?jobId=49627154" title="View more jobs from BJSS" data-gtm-value="recruiter_name_click">
                                    <span itemprop="name">BJSS</span><meta itemprop="url" content="https://www.reed.co.uk/company-profile/BJSS-58381?jobId=49627154">
                                        <meta itemprop="logo" content="https://resources.reed.co.uk/profileimages/logos/Banner_49807.png?v=20230125131257">
                                </a>
                            </span>

                    </div>
                        <div class="job-info--optional-icons">
                                                            <div>
                                    <i class="icon icon-applicants"></i>
                                    <span>Be one of the first ten applicants</span>
                                </div>
                        </div>
                    <div class="job-info--permament-icons">
                        <div>
                                <img src="/resources/images/controllers/jobs/salaryIcon.svg">
                                <span itemprop="baseSalary" itemscope="" itemtype="http://schema.org/MonetaryAmount">
                                    <meta itemprop="currency" content="GBP">
                                    <span>Competitive salary</span>
                                </span>

                        </div>
                        <div>
                                <img src="/resources/images/controllers/jobs/locationIcon.svg">
                                <span id="jobCountry" value="England"></span>
                                    <span>
                                        <a href="/jobs/jobs-in-leeds" itemprop="jobLocation" itemscope="" itemtype="http://schema.org/Place">
                                            <span itemprop="address" itemscope="" itemtype="http://schema.org/PostalAddress">
                                                <meta itemprop="addressRegion" content="West Yorkshire">
                                                <span itemprop="addressLocality" data-qa="regionLbl">Leeds</span>
                                                <meta itemprop="addressCountry" content="GB">
                                            </span>
                                        </a>, <span data-qa="localityLbl">West Yorkshire</span>
                                    </span>

                        </div>
                        <div>
                            <img src="/resources/images/controllers/jobs/timeIcon.svg">
                                <span itemprop="employmentType" data-qa="jobTypeLbl" content="FULL_TIME">
                                    <a href="/jobs/permanent">Permanent</a>,
                                        <a href="/jobs/full-time">
                                            full-time
                                        </a>
                                                                                                        </span>

                            <meta itemprop="workHours" content="full-time">
                        </div>
                    </div>
                </div>
            </div>
        </div>
            <div class="apply-options apply-options-top text-center " data-bind="visible: !jobApplication.showApplyBox()">
                        <button class="btn btn-primary external-apply-button side gtmExternalAppLinkSide gtmJobseekerRegistrationFunnelClick gtmApplyNowTop" id="applyButtonSide" data-qa="applyBtn" data-bind="click: jobApplication.applyForJob, clickBubble: false, visible: !jobApplication.showApplyBox()" data-vpv="/vpv/apply_now/signed_out/off_site_app/responsive">
                            Apply now
                        </button>
                        <div class="external-app-caption">Apply on employer's website</div>

                

                <div class="visible-xs-block">
                    <a class="find-out-more-link" data-gtm-value="recuiter_find_out_more_click" href="/company-profile/BJSS-58381?jobId=49627154">About this company</a>
                </div>
            </div>
        <div class="branded-job--mobile-devider">
            <hr>
        </div>
        <div class="branded-job--description-container">


            <div>
                <span itemprop="description"> <p><strong><strong>About Us</strong></strong></p> <p>We’re an award-winning innovative tech consultancy - a team of creative problem solvers. Since 1993 we’ve been finding better, more sustainable ways to solve complex technology problems for some of the world’s leading organisations and delivered solutions  that millions of people use every day.</p> <p>In the last 30 years we won several awards, including a prestigious Queen’s Award for Enterprise in the Innovation category for our Enterprise Agile delivery approach.</p> <p>Operating from 26 locations across the world, we bring together teams of creative experts with diverse backgrounds and experiences, who enjoy working and learning in our collaborative and open culture and are committed to world-class delivery.</p> <p>We want to continue to grow our team with people just like you!</p> <p><strong><strong>About the Role</strong></strong></p> <p>We love to experiment with the latest tools, technologies and techniques to improve how we deliver our solutions and as a software engineer you can expect to be involved in:</p> <ul> <li>Engineering software solutions - working with prototypes and proof of concepts and developing fully functioning applications based on frameworks such as .Net and Spring/Spring Boot, and using languages including Java, Scala, JavaScript, Python, C# and Go<em>.</em></li><li>Producing rich front-end UI and efficient services with technologies like React, Angular and Vue.</li><li>The automation of environmental and application deployment, scaling, and management using Kubernetes, Terraform, both in the cloud (AWS, Azure or GCP) or on-premise.</li></ul> <p><strong><strong>About You</strong></strong></p> <ul> <li>You're an engineer at heart and enjoy the challenge of building complex software solutions</li><li>You want to work across a range of tech environments. Your priorities will be building new systems and improving stability, security and efficiency</li><li>You're keen to learn new technologies and languages</li><li>You're comfortable operating in an Agile environment with a good working knowledge in areas such as CI/CD, build pipelines, testing and architecture</li><li>You have a good understanding of computing fundamentals (e.g. logic, data structures, algorithms, low-level architecture, networks stack) along with strong software design skills, including OO, and knowledge of version control systems such as Git</li><li>You love nothing more than grabbing a pen and whiteboarding the next challenge</li></ul> <p><strong><strong>Some of the Perks</strong></strong></p> <ul> <li>Flexible benefits allowance - you choose how to spend your allowance (additional pension contributions, healthcare, dental and more)</li><li>Industry leading health and wellbeing plan - we partner with several wellbeing support functions to cater to each individual's need, including 24/7 GP services, mental health support, and other</li><li>Life Assurance (4 x annual salary)</li><li>25 days annual leave plus bank holidays</li><li>Hybrid working - Our roles are not fully remote as we take pride in the tight knit communities we have created at our local offices. But we offer plenty of flexibility and you can split your time between the office, client site and WFH</li><li>Discounts - we have preferred rates from dozens of retail, lifestyle, and utility brands</li><li>An industry-leading referral scheme with no limits on the number of referrals</li><li>Flexible holiday buy/sell option</li><li>Electric vehicle scheme</li><li>Training opportunities and incentives - we support professional certifications across engineering and non-engineering roles, including unlimited access to O’Reilly</li><li>Giving back - the ability to get involved nationally and regionally with partnerships to get people from diverse backgrounds into tech</li><li>You will become part of a squad with people from different areas within the business who will help you grow at BJSS</li><li>We have a busy social calendar that you can chose to join- quarterly town halls/squad nights out/weekends away with families included/office get togethers</li><li>GymFlex gym membership programme</li></ul> </span>
            </div>

        </div>

        <div class="branded-job--media-skills">

            <div react="" id="brandedJob"><div class="styles__brandedJobCarouselContainer___swC8a" data-qe="ctn-carousel-content"><div class="styles__brandedJobCarouselContent___18Pvc"><div class="styles__brandedJobSlideLeft___2Ejs0" style="display: none;"><a href="#" class="styles__brandedJobSlideLeftBtn___1PGb4" data-qe="lnk-prev-slide"></a><div class="styles__brandedJobLeftGlyph___th9_x"><img class="styles__chevron___1o8Nj" src="/resources/images/controllers/jobs/leftChevron.svg"></div></div><div class="styles__brandedJobMainSlideStyle___3ImAW" data-qe="ctn-slide-container" style="transform: translateX(0px);"><div class="slide" data-displayorder="0" style="float: left; margin-right: 20px; position: relative;"><img data-src="https://img.youtube.com/vi/7N_I6nvWwIg/0.jpg" class="styles__brandedJobSlideImg___3V6NC" style="cursor: pointer;"><img src="/resources/images/controllers/jobs/playButton.svg" class="styles__brandedJobPlayButton___3yO4-" alt=""></div><div class="slide" data-displayorder="1" style="float: left; margin-right: 20px; position: relative;"><img data-src="https://img.youtube.com/vi/V3NGHYaPZTo/0.jpg" class="styles__brandedJobSlideImg___3V6NC" style="cursor: pointer;"><img src="/resources/images/controllers/jobs/playButton.svg" class="styles__brandedJobPlayButton___3yO4-" alt=""></div><div class="slide" data-displayorder="2" style="float: left; margin-right: 20px; position: relative;"><img data-src="https://img.youtube.com/vi/xVJEWHodpYM/0.jpg" class="styles__brandedJobSlideImg___3V6NC" style="cursor: pointer;"><img src="/resources/images/controllers/jobs/playButton.svg" class="styles__brandedJobPlayButton___3yO4-" alt=""></div><div class="slide" data-displayorder="3" style="float: left; margin-right: 20px; position: relative;"><img data-src="https://img.youtube.com/vi/lJZiSUohaSU/0.jpg" class="styles__brandedJobSlideImg___3V6NC" style="cursor: pointer;"><img src="/resources/images/controllers/jobs/playButton.svg" class="styles__brandedJobPlayButton___3yO4-" alt=""></div></div><div class="styles__brandedJobSlideRight___ZLPt5" style="display: block;"><a href="#" class="styles__brandedJobSlideRightBtn___30XWu" data-qe="lnk-next-slide"></a><div class="styles__brandedJobRightGlyph___38-nI"><img class="styles__chevron___1o8Nj" src="/resources/images/controllers/jobs/rightChevron.svg"></div></div></div><div class="styles__brandedJobDotContainer___2oG3y"><div class="styles__brandedJobDotHolder___1V4Ry" data-index="0" data-qe="btn-dot-0" style="background-color: rgb(0, 121, 209);"></div><div class="styles__brandedJobDotHolder___1V4Ry" data-index="1" data-qe="btn-dot-1" style="background-color: rgb(216, 216, 216);"></div><div class="styles__brandedJobDotHolder___1V4Ry" data-index="2" data-qe="btn-dot-2" style="background-color: rgb(216, 216, 216);"></div><div class="styles__brandedJobDotHolder___1V4Ry" data-index="3" data-qe="btn-dot-3" style="background-color: rgb(216, 216, 216);"></div></div></div></div>

        </div>

        
        <div class="application-box">

<form action="/jobs/software-engineer/49627154#apply-form" data-bind="submit: jobApplication.sendApplication" id="apply-form" method="post" novalidate="novalidate">                    <input type="hidden" name="InternalApplicationSource" value="details">
<input name="__RequestVerificationToken" type="hidden" value="jJXSA1-9HP4uguPw0_gEaH4aXmhQMGRGLQ5K5XztqNYZl1gAEp6c3y-n5rzmdQ14TvrAI3VbqaHBZCf09kg1tShQRb81">


<section class="cv-coverletter-externalapplication" data-bind="visible: jobApplication.showApplyBox()" style="display:none;">

<input data-val="true" data-val-number="The field JobId must be a number." data-val-required="The JobId field is required." id="JobId" name="JobId" type="hidden" value="49627154">
<input id="Source" name="Source" type="hidden" value="">
<input data-val="true" data-val-required="The UserHasRegisteredThroughJob field is required." id="UserHasRegisteredThroughJob" name="UserHasRegisteredThroughJob" type="hidden" value="False">
</section>




                    <div class="apply-options apply-options-branded text-center " data-bind="visible: !jobApplication.showApplyBox()">

                            <button class="btn btn-primary external-apply-button side gtmExternalAppLinkSide gtmJobseekerRegistrationFunnelClick" id="applyExternalButtonSide" data-qa="applyBtn" data-bind="click: jobApplication.applyForJob, clickBubble: false, visible: !jobApplication.showApplyBox()" data-vpv="/vpv/apply_now/signed_out/off_site_app/responsive">
                                Apply now
                            </button>
                            <div class="external-app-caption">Apply on employer's website</div>

                    </div>
</form>            <div class="hidden-xs">
                <div class="apply-options ">
                    <div class="secondary-btns ">
                                <button data-qa="shortListMobileBtn" class="btn btn-secondary saved-jobs-button gtmJobDetailsSaveJob" data-bind="click: modifyShortlistStatus, css: { 'gtmJobDetailsSaveJob': !savedJob.isSavedJob(), 'has-saved-job': savedJob.isSavedJob() }">
            <i class="icon"></i>
            <span style="display:none" data-bind="visible: savedJob.isSavedJob()">Saved</span>
            <span style="" data-bind="visible: !savedJob.isSavedJob()">Save</span>
        </button>


                        
                        <button type="button" class="btn btn-secondary email-job-button gtmJobDetailsEmail" data-bind="click: showEmailJob">
                            <i class="icon icon-share"></i>
                            Share job
                        </button>
                    </div>
                </div>
            </div>
            <div class="warning-and-report--container">
                <div class="warning-and-report">
                    <p class="reference ">Reference: 49627154</p>

                    <p class="warning">To stay safe in your job search and flexible work, we recommend that you visit <a href="http://www.jobsaware.co.uk/" rel="nofollow" target="_blank">JobsAware</a>, a non-profit, joint industry and law enforcement organisation working to combat labour market abuse. Visit the JobsAware website for information and to get free, expert advice for safer work.</p>

                    <a class="report-job-link" href="#" title="Report this job" data-bind="click: reportJob">Report this job</a>
                </div>
            </div>
        </div>
    </div>
    """
    return ResponseToContainers.soupify_page_html(detailed_job_description_promotion_mock)



class TestResponseToContainers:
    def test_soupify_page(self, get_soupified_page: BeautifulSoup):
        assert isinstance(get_soupified_page, BeautifulSoup)


    def test_get_job_posting_containers_exist(self, get_job_containers: List[BeautifulSoup]):
            assert len(get_job_containers) > 0
    
    def test_response_to_job_posting_containers_returns_multiple_objects(self, get_page_html: httpx.Response):
        assert len(ResponseToContainers.response_to_job_summary_containers(get_page_html)) > 0
    
    def test_responses_to_job_posting_containers_returns_multiple_objects(self, get_page_html: httpx.Response, get_job_containers: List[BeautifulSoup]):
        assert len(ResponseToContainers.responses_to_job_posting_containers([get_page_html, get_page_html])) == len(get_job_containers) * 2

    def test_get_detailed_job_posting_container_length_vs_mock(self, job_page_detailed_html: str):
        details = ResponseToContainers.get_detailed_job_posting_container(job_page_detailed_html)
        assert len(details.text) >= len(job_page_detailed_html)

    def test_get_detailed_job_posting_container_length_vs_mock_promotion(self,
     job_page_detailed_html_promotional: str):
        details = ResponseToContainers.get_detailed_job_posting_container(job_page_detailed_html_promotional)
        assert len(details.text) >= len(job_page_detailed_html_promotional)


class TestJobContainerParser:
    def test_get_job_title_exists(self, get_job: BeautifulSoup):
        assert type(JobContainerParser.get_job_title(get_job)) is str


    def test_get_posted_date_info_and_employer_raw_exists(self, get_job: BeautifulSoup):
        assert type(JobContainerParser.get_job_posted_date_and_employer_info_raw(get_job)) is str

    def test_get_posted_date_info_and_employer_raw_gets_employer(self, get_job: BeautifulSoup):
        assert JobContainerParser.get_job_posted_date_and_employer_info_raw(get_job).find("by") != -1


    def test_get_job_metadata_panel_raw_exists(self, get_job: BeautifulSoup):
        assert type(JobContainerParser._get_job_metadata_panel_raw(get_job)) is not None

    def test_get_job_metadata_no_class_returns_first_item(self, get_job: BeautifulSoup):
        assert len(JobContainerParser._get_job_metadata(get_job, "li", "")) > 0

    def test_get_job_metadata_when_invalid_tag_class(self, get_job: BeautifulSoup):
        assert type(JobContainerParser._get_job_metadata(get_job, "dsfadf", "dsfadsf")) is str

    def test_get_job_salary_info_raw(self, get_job: BeautifulSoup) -> str:
        assert len(JobContainerParser.get_job_salary_info_raw(get_job)) > 0


    def test_get_job_location_raw(self, get_job: BeautifulSoup) -> str:
        assert len(JobContainerParser.get_job_location_raw(get_job)) > 0


    def test_get_job_tenure_type_raw(self, get_job: BeautifulSoup) -> str:
        assert len(JobContainerParser.get_job_tenure_type_raw(get_job)) > 0


    def test_get_job_remote_status_raw(self, get_job: BeautifulSoup) -> str:
        assert len(JobContainerParser.get_job_remote_status_raw(get_job)) > 0


    def get_job_description_start_raw(self, container: BeautifulSoup) -> str:
        return JobContainerParser._get_job_metadata(container, "p", "job-result-description__details")

    def test_get_job_description_start_raw_exists(self, get_job: BeautifulSoup):
        assert type(JobContainerParser.get_job_description_start_raw(get_job)) is str

    def test_get_job_full_page_link_raw_exists(self, get_job: BeautifulSoup):
        assert type(JobContainerParser.get_job_full_page_link_raw(get_job)) is str

    def test_get_job_id_raw_exists(self, get_job: BeautifulSoup):
        assert type(JobContainerParser.get_job_id_raw(get_job)) is str        


class TestRawJobInformationFactory:
    def test_get_empty_raw_job_info_returns_correct_type(self):
        assert type(RawJobInformationFactory._get_empty_raw_job_info()) is RawJobInformation
    
    def test_get_x_empty_raw_job_info_containers_correct_length(self):
        assert len(RawJobInformationFactory._get_x_empty_raw_job_info_objects(12)) == 12
    
    def test_populate_raw_job_information_from_job_container_title(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.title == JobContainerParser.get_job_title(get_job)
    
    def test_populate_raw_job_information_from_job_container_date_and_employer(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.date_and_employer == JobContainerParser.get_job_posted_date_and_employer_info_raw(get_job)

    def test_populate_raw_job_information_from_job_container_location(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.location == JobContainerParser.get_job_location_raw(get_job)
    
    def test_populate_raw_job_information_from_job_container_salary(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.salary == JobContainerParser.get_job_salary_info_raw(get_job)

    def test_populate_raw_job_information_from_job_container_tenure_type(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.tenure_type == JobContainerParser.get_job_tenure_type_raw(get_job)

    def test_populate_raw_job_information_from_job_container_remote_status(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.remote_status == JobContainerParser.get_job_remote_status_raw(get_job)

    def test_populate_raw_job_information_from_job_container_full_page_link(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.full_page_link == JobContainerParser.get_job_full_page_link_raw(get_job)

    def test_populate_raw_job_information_from_container_job_id(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.job_id == JobContainerParser.get_job_id_raw(get_job)

    def test_populate_raw_job_information_from_job_container_description_start(self, get_raw_job_information: RawJobInformation, get_job: BeautifulSoup):
        assert get_raw_job_information.description_start == JobContainerParser.get_job_description_start_raw(get_job)    

    def test_get_multiple_raw_job_info_objects_length(self, get_page_html: httpx.Response):
        assert len(RawJobInformationFactory.get_multiple_populated_raw_job_info_objects([get_page_html])) >= 20
    
    @pytest.mark.parametrize("index", [0, 1, 2, -2, -1, 0])
    def test_get_multiple_raw_job_info_objects_populated(self, get_page_html: httpx.Response, index: int):
        test_information_objects = RawJobInformationFactory.get_multiple_populated_raw_job_info_objects([get_page_html])
        assert len(test_information_objects[index].title) > 0



class TestDetailedJobContainerParser:
    def test_get_number_of_applicants_raw_standard(self, job_page_detailed_html: BeautifulSoup):
        applicant_raw = DetailedJobContainerParser.get_number_of_applicants_raw(job_page_detailed_html)
        assert applicant_raw == "Be one of the first ten applicants"
    
    def test_get_number_of_applicants_raw_promotional(self, job_page_detailed_html_promotional: BeautifulSoup):
        applicant_raw = DetailedJobContainerParser.get_number_of_applicants_raw(job_page_detailed_html_promotional)
        assert applicant_raw == "Be one of the first ten applicants"

    def test_get_number_of_applicants_raw_none_input(self):
        assert DetailedJobContainerParser.get_number_of_applicants_raw(None) == ""

    def test_get_job_full_description_raw(self, job_page_detailed_html: BeautifulSoup):
        description_raw = DetailedJobContainerParser.get_job_full_description_raw(job_page_detailed_html)
        assert description_raw.find("This cutting-edge cyber security firm is") != -1
        assert description_raw.find("you would work independently in designing,") != -1
    
    def test_get_job_full_description_raw_not_duplicating(self,
     job_page_detailed_html: BeautifulSoup):
        description_raw = DetailedJobContainerParser.get_job_full_description_raw(job_page_detailed_html)
        assert description_raw.find("Private medical & Dental") != -1
        assert (description_raw.find("Private medical & Dental") ==
        description_raw.rfind("Private medical & Dental"))
