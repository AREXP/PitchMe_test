from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class Location(BaseModel):
    city: str
    country: str


class Experience(BaseModel):
    company_name: str
    job_title: str
    description: str
    skills: List[str]
    starts_at: date
    ends_at: Optional[date] = date.today()
    location: Location


class Profile(BaseModel):
    first_name: str
    last_name: str
    skills: List[str]
    description: str
    location: Location
    experiences: List[Experience]

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
