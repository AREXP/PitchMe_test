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

    @validator("experiences", pre=False)
    def sorted_experiences(cls, experiences):
        if not isinstance(experiences, list):
            raise TypeError(f"Value `{experiences}` is not a list!")
        for e in experiences:
            if not isinstance(e, Experience):
                raise TypeError(f"Value `{e}` is not of type 'Experience'!")
        
        # sort not ended experiences from the most recently start to the oldest start
        not_ended_experiences = sorted(
            [e for e in experiences if e.ends_at is None],
            key=lambda e: e.starts_at,
            reverse=True
        )
        # sort ended experiences firstly from the most recently ended,
        # and secondly from the most recently started 
        ended_experiences = sorted(
            [e for e in experiences if e.ends_at is not None],
            key=lambda e: (e.ends_at, e.starts_at),
            reverse=True
        )
        return not_ended_experiences + ended_experiences
