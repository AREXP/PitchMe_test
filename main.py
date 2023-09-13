import json
import argparse
from validator import Validator
from profile_schema import Profile
from pydantic import ValidationError


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--filter",
                        choices=["experienced-python-developer", "middle-ux-designer"],
                        help="Choose the filter to apply")

    parser.add_argument("--input",
                        help="Input file name")

    args = parser.parse_args()

    if not args.input:
        print("Please provide an input file.")
        return

    if args.filter not in ["experienced-python-developer", "middle-ux-designer"]:
        print("Please choose a valid filter.")
        return

    try:
        with open(args.input) as file:
            profiles = json.load(file)
    except FileNotFoundError:
        print("Input file not found.")
        return
    except json.JSONDecodeError:
        print("Invalid JSON file.")
        return

    try:
        result = None
        for profile_data in profiles:
            profile = Profile(**profile_data)

            if args.filter == "experienced-python-developer":
                result = Validator.is_experienced_python_developer(profile)
            elif args.filter == "middle-ux-designer":
                result = Validator.is_middle_ux_designer(profile)

            print(result)

    except ValidationError as e:
        print(f"Invalid profile data: {e}")


if __name__ == "__main__":
    main()
