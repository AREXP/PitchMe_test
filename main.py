import argparse
import json
from pydantic import ValidationError
from profile_schema import ExperiencedPythonDeveloper, MiddleUxDesigner


def main() -> None:
    """Main function.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", type=str)
    parser.add_argument("--input", type=str)

    args = parser.parse_args()
    
    if args.filter == "experienced-python-dev":
        position_shema = ExperiencedPythonDeveloper
    elif args.filter == "middle-ux-designer":
        position_shema = MiddleUxDesigner


    #Read data from a JSON file
    with open(args.input) as file:
        candidates = json.load(file)
        for candidate in candidates:
            fist_name_val = candidate["first_name"]
            last_name_val = candidate["last_name"]

            try:
                position_shema(**candidate)
                print(f"{fist_name_val} {last_name_val} - {True}")
            except ValidationError as e:
                error_messages = [error["msg"] for error in e.errors()][0]
                print(f"{fist_name_val} {last_name_val} - {False}, {error_messages}")


if __name__ == "__main__":
    print(main())