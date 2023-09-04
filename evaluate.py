import json
import os
import logging
from collections.abc import Iterable
from datetime import date, timedelta, datetime
from typing import List, Optional, Union, Tuple
from profile_schema import Experience, Profile
from pydantic import validate_arguments
from dataclasses import dataclass
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


@dataclass
class EvaluatorResult:
    profile: Profile
    status: bool
    reason: Optional[str]


@dataclass
class ExperiencePeriod:
    starts_at: date
    ends_at: date


class Evaluator(ABC):
    # filled in __init__
    FAANG = []
    COUNTRY = {}

    def __init__(self, config_file="./static_data.json"):
        with open(config_file, "r") as config:
            data = json.load(config)

        self.FAANG = data["FAANG"]
        self.COUNTRY = data["COUNTRY"]

    @abstractmethod
    def custom_check(self, profile: Profile) -> Tuple[bool, str]:
        return (True, "")

    def sort_jobs_oldest_first(self, experiences: List[Experience]) -> List[Experience]:
        today = datetime.today()
        return sorted(experiences, key=lambda e: e.ends_at if e.ends_at else today)

    def fixup_exp_end_dates(self, experiences: List[Experience]):
        # fixup experience end date
        for exp in experiences:
            if not exp.ends_at:
                exp.ends_at = datetime.today()

    def calculate_exp_days(self, experiences: List[Experience]) -> timedelta:
        sorted_exp = sorted(experiences, key=lambda e: e.starts_at)
        current_exp = ExperiencePeriod(sorted_exp[0].starts_at, sorted_exp[0].ends_at)
        total_days = timedelta(days=0)

        for i in range(1, len(sorted_exp)):
            if sorted_exp[i].starts_at <= current_exp.ends_at:
                # if there is overlap with current range
                current_exp = ExperiencePeriod(
                    current_exp.starts_at,
                    max(current_exp.ends_at, sorted_exp[i].ends_at),
                )
            else:
                # if there is no overlap with current range
                total_days += current_exp.ends_at - current_exp.starts_at
                current_exp = ExperiencePeriod(
                    sorted_exp[i].starts_at, sorted_exp[i].ends_at
                )

        total_days += current_exp.ends_at - current_exp.starts_at

        return total_days

    @validate_arguments
    def evaluate(self, profiles: List[Profile]) -> Iterable[EvaluatorResult]:
        for profile in profiles:
            is_success, rejection_reason = self.custom_check(profile)
            yield EvaluatorResult(profile, is_success, rejection_reason)


class Designer(Evaluator):
    def __init__(self):
        super().__init__()

    def custom_check(self, profile):
        return (True, "")


class Developer(Evaluator):
    def __init__(
        self,
        city="london",
        country_code_iso3166="gb",
        experience_years=8,
        skills=("python", "c++"),
        last_three_job_titles=("software engineer", "backend developer"),
    ):
        super().__init__()
        self.city = city
        self.country_code = country_code_iso3166
        self.experience_years = experience_years
        self.skills = set(skills)
        self.last_three_job_titles = set(last_three_job_titles)

    def custom_check(self, profile):
        if profile.location.country.lower() not in self.COUNTRY[self.country_code]:
            return (
                False,
                f"Unsuitable country: {profile.location.country} instead of {self.country_code}",
            )

        if profile.location.city.lower() != self.city:
            return (
                False,
                f"Unsuitable city: {profile.location.city} instead of {self.city}",
            )

        # fixup end dates once, so they are never None
        self.fixup_exp_end_dates(profile.experiences)

        sorted_exp = self.sort_jobs_oldest_first(profile.experiences)

        if len(sorted_exp) < 3:
            return (False, "Does not have at least 3 last positions")

        last_exp = sorted_exp[-1]
        if self.skills.issubset(last_exp.skills):
            return (False, "Did not work with {self.skills} in the last position")

        for i in range(-1, -3, -1):
            company_name = sorted_exp[i].company_name.lower().strip()
            if company_name not in self.FAANG:
                return (False, "Did not work in FAANG for the last 2 positions")

        for i in range(-1, -4, -1):
            title = sorted_exp[i].job_title.lower()
            if title not in self.last_three_job_titles:
                return (
                    False,
                    "Does not have 'Software Engineer' or 'Backend Developer' exact title for the last 3 positions",
                )

        # calculate all experiences not just relevant
        days_of_experience = self.calculate_exp_days(profile.experiences)
        if days_of_experience.days < self.experience_years * 365:
            # TODO: not every year is 365 days
            return (
                False,
                f"Not enough experience, {days_of_experience.days} instead of {self.experience_years} years",
            )

        return (True, "")
