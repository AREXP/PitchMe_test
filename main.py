import argparse
import json

from filters import PyDevProfile, UXProfile
from profile_schema import Profile

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filter', choices=["senior python dev", "ux"], required=True)
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    filter_by = args.filter
    data = args.input
    d = []
    positions = {
        "senior python dev": PyDevProfile,
        "ux": UXProfile
    }
    with open("profiles.json", "r") as file:
        d = json.load(file)
    profiles = [Profile(**profile) for profile in d]

    for profile in profiles:
        person = positions.get(filter_by)(profile)
        person.make_filter()
        print(f"{person.profile.first_name} {person.profile.last_name} – {person.match}, {person.reason}")


