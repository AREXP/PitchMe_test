import argparse
from enum import Enum
from pathlib import Path
from typing import List

import pydantic

from profile_schema import Profile
from profile_filter import CheckException, ExperiencedPythonDeveloperFilter


class Filters(Enum):
    EXPERIENCED_PYTHON = "EXPERIENCED_PYTHON"

    def __str__(self) -> str:
        return self.value


def main(profiles_path: Path, profile_filter: Filters):
    profiles: List[Profile] = pydantic.parse_file_as(List[Profile], profiles_path)

    if profile_filter is Filters.EXPERIENCED_PYTHON:
        filter = ExperiencedPythonDeveloperFilter()
    
    for profile in profiles:
        try:
            filter.check(profile)
            print(f"{profile.first_name} {profile.last_name} - True")
        except CheckException as e:
            print(f"{profile.first_name} {profile.last_name} - False, {e.fail_reason}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Filter profiles based on their contents")
    parser.add_argument("--profiles_path", type=Path, required=True, help="path to json-file with profiles")
    parser.add_argument("--filter", type=Filters, choices=list(Filters), required=True, help="filter to use for profiles")
    args = parser.parse_args()

    main(args.profiles_path, args.filter)
