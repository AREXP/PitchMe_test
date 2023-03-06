import argparse
from datetime import datetime
from typing import List

from pydantic import parse_file_as

from profile_schema import Profile


class ProfileFilter:
    def __init__(self):
        self.arg_parser = argparse.ArgumentParser()
        self.arg_parser.add_argument("-f", "--filter", type=str)
        self.arg_parser.add_argument("-d", "--data", type=str)
        self.arg_parser.add_argument("-i", "--input", type=str)
        self.args_loader = self.arg_parser.parse_args()
        self.input_file = self.args_loader.input
        self.profiles = parse_file_as(path=self.input_file, type_=List[Profile])

    # start-method for filtering profiles
    def start(self) -> None:
        checker = {
            "experience": self.experience_filter,
            "location": self.worked_location_filter,
            "skills": self.skills_filter,
            "current_location": self.current_location_filter
        }
        filter_type = self.args_loader.filter.lower()
        input_value = self.args_loader.data

        # calls specific filter-method by input value and filter type from python command
        checker[filter_type](input_value)

    # filter-method by candidate's years of experience
    def experience_filter(self, input_data: str) -> None:
        input_data = int(input_data)
        for candidate in self.profiles:
            years = []
            # call pydantic-method for summarizing total experience without overlapping
            companies_2 = candidate.summarize_experiences()
            for company in companies_2:
                difference = self.get_datetime_difference(company["starts_at"], company['ends_at'])
                years.append(difference)
            years = sum(years)
            if input_data <= years:
                print(f"{candidate.first_name} – True.")
            else:
                print(f"{candidate.first_name} – False, Not enough experience")

    # divider-method by years
    @staticmethod
    def get_datetime_difference(starts_at: datetime, ends_at: datetime):
        delta = ends_at - starts_at
        return delta.days // 365

    # filter-method by candidate's worked location
    def worked_location_filter(self, input_data: str) -> None:
        for candidate in self.profiles:
            for experience in candidate.experiences:
                if (experience.location.country.lower() == input_data or
                        experience.location.city.lower() == input_data):
                    print(f"{candidate.first_name} – True")
                    break
                elif (experience.location.country.upper() == input_data or
                      experience.location.city.upper() == input_data):
                    print(f"{candidate.first_name} – True")
                    break
                else:
                    print(f"{candidate.first_name} – False, Never worked in {input_data}")
                    break

    # filter-method by candidate's skills
    def skills_filter(self, input_data: str) -> None:
        for candidate in self.profiles:
            for experience in candidate.experiences:
                if input_data in experience.skills:
                    print(f"{candidate.first_name} – True")
                    break
                else:
                    print(f"{candidate.first_name} – False, No experience with {input_data}")
                    break

    # filter-method by candidate's current location
    def current_location_filter(self, input_data: str) -> None:
        for candidate in self.profiles:
            if (input_data == candidate.location.city or
                    input_data == candidate.location.country):
                print(f"{candidate.first_name} – True")
            else:
                print(f"{candidate.first_name} – False, Currently not in {input_data}")


if __name__ == "__main__":
    profile = ProfileFilter()
    profile.start()
