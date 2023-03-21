from pydantic_factories import ModelFactory, PostGenerated
from random import choice, randint, sample
from datetime import date, timedelta

from profile_schema import Location, Experience, Profile


def add_timedelta(name: str, values: dict, *args, **kwds):
    delta = timedelta(days=randint(10, 3650))
    return values["starts_at"] + delta


def set_country(name: str, values: dict, *args, **kwds):
    if values["city"] == "London":
        return "gb"
    return choice(["uk", "Brazil", "Country1", "Country2"])


def get_date():
    start_date = date(2000, 1, 1)
    end_date = date(2010, 12, 31)
    delta = end_date - start_date
    random_date = start_date + timedelta(days=randint(0, delta.days))
    return random_date


class LocationFactory(ModelFactory):
    __model__ = Location

    city = lambda: choice(["London", "City1", "City2"])
    country = PostGenerated(set_country)


class ExperienceFactory(ModelFactory):
    __model__ = Experience

    company_name = lambda: choice(
        [
            "Facebook",
            "Amazon",
            "Apple",
            "Netflix",
            "Google",
            "Company1",
            "Company2",
            "Company3",
            "Company4",
        ]
    )
    job_title = lambda: choice(
        [
            "Backend developer",
            "Software engineer",
            "Product designer",
            "UX-designer",
            "JobTitle1",
            "JobTitle2",
        ]
    )
    skills = lambda: sample(
        [
            "Python",
            "C++",
            "Figma",
            "Sketch",
            "UX-research",
            "Miro",
            "Skill1",
            "Skill2",
            "Skill3",
        ],
        randint(1, 5),
    )

    starts_at = lambda: get_date()
    ends_at = PostGenerated(add_timedelta)


class ProfileFactory(ModelFactory):
    __model__ = Profile

    location = lambda: LocationFactory.build()
    experiences = lambda: ExperienceFactory.batch(size=randint(0, 3))


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Generate random profiles and save them to a JSON file"
    )
    parser.add_argument(
        "num_profiles", type=int, help="the number of profiles to generate"
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="the name of the output file to save the JSON dataset",
    )

    args = parser.parse_args()

    result = ProfileFactory.batch(size=args.num_profiles)
    with open(args.output_file, "w") as outfile:
        json.dump([x.dict() for x in result], outfile, indent=2, default=str)
