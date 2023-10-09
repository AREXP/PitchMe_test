import argparse
import json
from pydantic import ValidationError

from filters import PyDevProfile, UXProfile
from profile_schema import Profile

FILTERS = {
        "python_dev": PyDevProfile,
        "ux_designer": UXProfile
    }

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--filter', choices=FILTERS.keys(), required=True, help="filter by profile")
    parser.add_argument('--input', required=True, help="path to json file")
    args = parser.parse_args()

    filter_by = args.filter
    profiles_path = args.input

    with open(profiles_path, "r") as file:
        data = json.load(file)

    profiles = []

    for pr in data:
        try:
            profiles.append(Profile(**pr))
        except ValidationError:
            print(f"profile # {data.index(pr)} has incorrect format")

    for profile in profiles:
        person = FILTERS.get(filter_by)(profile)
        person.make_filter()
        print(f"{person.profile.first_name} {person.profile.last_name} – {person.print_result()}")


