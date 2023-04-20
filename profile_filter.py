import datetime
from typing import List, Callable, Tuple, Optional

from profile_schema import Profile


class CheckAttacher:
    def __init__(self) -> None:
        self.checks: List[Callable[[Profile], Tuple[bool, Optional[str]]]] = []
    
    def attach(self, check_function: Callable[[Profile], Tuple[bool, Optional[str]]]):
        self.checks.append(check_function)
        return check_function


class CheckException(Exception):
    def __init__(self, fail_reason: str) -> None:
        super().__init__(f"Has not passed the check: '{fail_reason}'")
        self.fail_reason = fail_reason


class ProfileFilter:
    checker = CheckAttacher()

    def check(self, profile: Profile) -> bool:
        for check_function in self.checker.checks:
            check_passed, fail_reason = check_function(self, profile)
            if not check_passed:
                raise CheckException(fail_reason=fail_reason)
        return True


class ExperiencedPythonDeveloperFilter(ProfileFilter):
    checker = CheckAttacher()

    faang_companies = {"facebook", "amazon", "apple", "netflix", "google"}
    target_job_titles = {"backend developer", "software engineer"}

    @checker.attach
    def check_latest_2_faang(self, profile: Profile) -> Tuple[bool, Optional[str]]:
        latest_companies = [experience.company_name for experience in profile.experiences[:2]]
        if not any(
            map(
                lambda company_name: company_name.strip().lower() in self.faang_companies,
                latest_companies
            )
        ):
            return False, f"{', '.join(latest_companies)} is not FAANG"
        return True, None

    @checker.attach
    def check_latest_3_swe_or_backend(self, profile: Profile) -> Tuple[bool, Optional[str]]:
        latest_job_titles = [experience.job_title for experience in profile.experiences[:3]]
        if not all(
            map(
                lambda job_title: job_title.strip().lower() in self.target_job_titles,
                latest_job_titles
            )
        ):
            return False, f"{', '.join(latest_job_titles)} are not all Backend developer or Software engineer roles"
        return True, None

    @checker.attach
    def check_experience_over_8_years(self, profile: Profile) -> Tuple[bool, Optional[str]]:
        last_end = datetime.datetime.now().date()
        last_begin = datetime.datetime.now().date()

        total_experience = datetime.timedelta(0)
        for experience in profile.experiences:
            if experience.ends_at is None:
                last_begin = experience.starts_at
                continue

            if experience.ends_at < last_begin:
                total_experience += (last_end - last_begin)
                last_begin = experience.starts_at
                last_end = experience.ends_at
            elif experience.starts_at < last_begin:
                last_begin = experience.starts_at
        
        total_experience += (last_end - last_begin)
        full_years = total_experience.days // 365

        if full_years < 8:
            return False, f"Experience ({full_years} years) is less then 8 years"
        
        return True, None

    @checker.attach
    def check_latest_job_python_and_cpp(self, profile: Profile) -> Tuple[bool, Optional[str]]:
        latest_job_skills = list(map(
            lambda skill: skill.strip().lower(),
            profile.experiences[0].skills
        ))
        
        if "c++" not in latest_job_skills or "python" not in latest_job_skills:
            return False, f"Python and C++ are not in the latest company's skills: {latest_job_skills}"

        return True, None

    @checker.attach
    def check_london_location(self, profile: Profile) -> Tuple[bool, Optional[str]]:
        if profile.location.city.strip().lower() != "london":
            return False, "Doesn't live in London"
        return True, None

