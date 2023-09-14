import argparse
from datetime import datetime, date, timedelta
import json

from profile_schema import Profile, Location, Experience
from profile_models import *


def get_dates(experience: Experience):
    start_date_str = experience.starts_at.strftime("%Y-%m-%d")
    end_date_str = (
        experience.ends_at.strftime("%Y-%m-%d") if experience.ends_at else date.today().strftime("%Y-%m-%d")
    )

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    return start_date, end_date

def calculate_experience(profile: Profile):
    unique_experience_days = set()

    for experience in profile.experiences:
        start_date, end_date = get_dates(experience)

        unique_experience_days.add(start_date)

        current_date = start_date
        while current_date < end_date:
            current_date += timedelta(days=1)
            unique_experience_days.add(current_date)

    total_experience_days = len(unique_experience_days)

    return total_experience_days


def calculate_single_experience(experience: Experience):
    start_date, end_date = get_dates(experience)

    # calculations for one position
    experience_days = (end_date - start_date).days
    return experience_days


def years_to_days(years: int):
    days = years * 365
    leap_years = years // 4
    days += leap_years
    days -= (years // 100) - (years // 400)

    return days


class Filter:
    def __init__(self, profiles: List[Profile]):
        self.profiles = profiles

    def is_experienced_python_dev(self, profile: Profile):
        backend_experience = 0
        faang_experience, last_position_python_cplusplus = None, None
        london_location = Location(city="London", country="UK")

        python_dev_schema = PythonDeveloperCriteriaModel()

        for index, experience in enumerate(profile.experiences):

            if experience.job_title in python_dev_schema.POSITIONS_REQUIRED:
                backend_experience += 1

            if index >= len(profile.experiences) - 2 and experience.company_name.startswith(
                    python_dev_schema.FAANG_COMPANY):
                faang_experience = True

            if index == len(profile.experiences) - 1 and (
                    python_dev_schema.SKILLS_REQUIRED[0] in experience.skills
                    and python_dev_schema.SKILLS_REQUIRED[1] in experience.skills):
                last_position_python_cplusplus = True

        total_experience = calculate_experience(profile)

        error_messages = []

        # Final checks
        if total_experience < years_to_days(python_dev_schema.MIN_TOTAL_EXPERIENCE):
            error_messages.append("Insufficient total experience.")

        if not faang_experience:
            error_messages.append("Lack of experience in FAANG companies in one of the last two positions.")

        if backend_experience < python_dev_schema.BACKEND_TITLES_REQUIRED:
            error_messages.append("Insufficient experience in Backend Developer or Software Engineer positions.")

        if not last_position_python_cplusplus:
            error_messages.append("The last position does not match Python and C++ skills.")

        if profile.location != london_location:
            error_messages.append("The profile does not indicate living in London.")

        if error_messages:
            return False, " ".join(error_messages)
        else:
            return True, ""

    def is_middle_ux_designer(self, profile: Profile):
        design_experience = 0
        last_position_two_years_experience = None

        middle_ux_designer_schema = MiddleUXDesignerCriteria()
        last_position_experience_time = calculate_single_experience(profile.experiences[-1])

        for index, experience in enumerate(profile.experiences):
            if index >= len(profile.experiences) - 2 and (
                    experience.job_title in middle_ux_designer_schema.POSITIONS_REQUIRED or
                    middle_ux_designer_schema.JOB_PATTERN in experience.job_title.lower()):
                design_experience += 1

            if index == len(profile.experiences) - 1 and \
                    last_position_experience_time >= years_to_days(middle_ux_designer_schema.MIN_LAST_JOB_EXPERIENCE):
                last_position_two_years_experience = True

        total_experience = calculate_experience(profile)

        error_messages = []

        skills_count = 0
        for skill in profile.skills:
            if skill in middle_ux_designer_schema.DESIGN_TOOLS_REQUIRED:
                skills_count += 1

            if skills_count == 2:
                break

        if not ((len(profile.experiences) == 1 and design_experience == 1) or design_experience >= 2):
            error_messages.append("Lacks proficiency in design.")

        if skills_count < middle_ux_designer_schema.DESIGN_TOOLS_COUNT_REQUIRED:
            error_messages.append("Lacks proficiency in at least two required tools: Figma, Sketch, UX-research, Miro.")

        if not last_position_two_years_experience:
            error_messages.append("Less than 2 years of experience in the last position.")

        if total_experience > years_to_days(middle_ux_designer_schema.MAX_TOTAL_EXPERIENCE):
            error_messages.append("Total experience exceeds 5 years.")

        if profile.location.country not in middle_ux_designer_schema.EU_COUNTRIES:
            error_messages.append("Not a resident of European Union.")

        if error_messages:
            return False, " ".join(error_messages)
        else:
            return True, ""

    def apply_filter(self, chosen_filter: str):
        results = []
        for profile in self.profiles:
            if chosen_filter == "python_dev":
                result = self.is_experienced_python_dev(profile)
            elif chosen_filter == "ux_designer":
                result = self.is_middle_ux_designer(profile)
            else:
                result = None, "Unknown filter"
            results.append(result)
        return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", type=str, required=True)
    parser.add_argument("--input", type=str, required=True)

    args = parser.parse_args()

    if not args.filter or not args.input:
        print("Missing --filter and --input parameters.")
        return

    try:
        with open(args.input, "r") as file:
            profiles_data = json.load(file)

        profiles = []
        for data in profiles_data:
            profile = Profile(**data)
            profiles.append(profile)

        filter_app = Filter(profiles)
        results = filter_app.apply_filter(args.filter)

        for i, result in enumerate(results):
            if result[0]:
                print(f"{profiles[i].first_name} {profiles[i].last_name} – True")
            elif result[0] is None:
                print(f"{result[1]}")
            else:
                print(f"{profiles[i].first_name} {profiles[i].last_name} – False, {result[1]}")

    except Exception as error:
        print(f"An error occurred: {str(error)}")


if __name__ == "__main__":
    main()
