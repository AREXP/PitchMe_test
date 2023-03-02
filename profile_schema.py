from datetime import date
from typing import List, Optional

from pydantic import BaseModel, validator


class Location(BaseModel):
    city: str
    country: str


class Experience(BaseModel):
    company_name: str
    job_title: str
    description: str
    skills: List[str]
    starts_at: date
    ends_at: Optional[date]
    location: Location


class Profile(BaseModel):
    first_name: str
    last_name: str
    skills: List[str]
    description: str
    location: Location
    experiences: List[Experience]
    

class ExperiencedPythonDeveloper(Profile):
    
    @validator("experiences")
    def required_company(cls, v):

        DESIRED_COMPANIES = {"facebook", "amazon", "apple", "netflix", "google", "meta"}
        titles = sorted(v, key=lambda k: k.ends_at, reverse=True)[:2]
        has_experice = False
        for title in titles:
            if title.company_name.strip().lower() in DESIRED_COMPANIES:
                has_experice = True
            if has_experice == False:
                raise ValueError(f"Lack of experience with the following FAANG companies: {DESIRED_COMPANIES}")
        return v

    @validator("experiences")
    def required_titles(cls, v):

        DESIRED_TITLE = {"backend developer", "software engineer"}
        titles = sorted(v, key=lambda k: k.ends_at, reverse=True)[:3]

        for title in titles:
            if title.job_title.strip().lower() not in DESIRED_TITLE:
                raise ValueError(f"Lack of required titles: {DESIRED_TITLE}")
        return v


    @validator("experiences")
    def required_experience(cls, v):
        
        DESIRED_TOTAL_EXPERIENCE_TIME = 8
        experience = sorted(v, key=lambda k: k.ends_at)
        
        experience_total_job_days = 0
        for job in experience:
            days_amount = job.ends_at - job.starts_at
            experience_total_job_days = experience_total_job_days + days_amount.days
        experience_total_job_years = experience_total_job_days//365
        if experience_total_job_years < DESIRED_TOTAL_EXPERIENCE_TIME:
            raise ValueError(f"Not enough experience: total duration {DESIRED_TOTAL_EXPERIENCE_TIME} years")
        return v
    

    @validator("experiences")
    def required_skills(cls, v):

        DESIRED_SKILLS = ["c++", "python"]
        last_postion = sorted(v, key=lambda k: k.ends_at, reverse=True)[0]
        skills = last_postion.skills
        for skill in skills:
            if skill.strip().lower() not in DESIRED_SKILLS:
                raise ValueError("No c++ or python on skill list")
        return v
    

    @validator("location")
    def required_location(cls, v):

        DESIRED_CITY = "london"
        if v.city.strip().lower() != DESIRED_CITY:
            raise ValueError(f"Current location is not {DESIRED_CITY}")
        return v   
    
