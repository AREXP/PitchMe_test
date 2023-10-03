import argparse
import json

from pydantic import ValidationError

from applicants import ExperiencePythonDeveloper, MiddleUXDesigner
from profile_schema import Profile

FILTERS = {
    'experience_python_developer': ExperiencePythonDeveloper,
    'middle_ux_designer': MiddleUXDesigner,
}


def main():
    parser = argparse.ArgumentParser(description='Check profiles')
    parser.add_argument(
        '--filter',
        type=str,
        choices=['experience_python_developer', 'middle_ux_designer'],
        help='choose role',
        required=True
    )
    parser.add_argument(
        '--input',
        type=str,
        default='data/profiles.json',
        help='profile files (json)',
    )
    args = parser.parse_args()
    filter = args.filter
    data = args.input

    applicant = FILTERS.get(filter)

    with open(data, 'r', encoding='utf-8') as file:
        data = json.load(file)
        profiles = []
        for item in data:
            try:
                profiles.append(Profile(**item))
            except ValidationError:
                continue

        for profile in profiles:
            filter_profile = applicant(profile)
            filter_profile.check_role()


if __name__ == '__main__':
    main()
