import logging
from pathlib import Path
from datetime import datetime

from profile_schema import Profile
from evaluate import Evaluator, Developer, Designer

logger = logging.getLogger(__name__)


def main():
    import argparse
    import json

    evaluators = {
        Developer.__name__: Developer,
        Designer.__name__: Designer,
    }

    parser = argparse.ArgumentParser(
        description="Evaluates profiles chosen by a filter"
    )
    parser.add_argument(
        "--filter",
        required=True,
        type=str,
        choices=evaluators.keys(),
        help="Choose one of the filter values",
    )
    parser.add_argument(
        "--input", required=True, type=Path, help="Path to JSON profiles"
    )

    args = parser.parse_args()
    if not args.input.exists() or not args.input.is_file():
        logger.error(f"{args.input} is not a valid input file.")
        return

    with open(args.input, "r") as infile:
        try:
            data = json.load(infile)
        except json.decoder.JSONDecodeError as error:
            logger.error("Input file is not valid JSON.")
            logger.error(error)
            return

    cls: Evaluator = evaluators[args.filter]()
    results = cls.evaluate(data)
    for res in results:
        fmt = f"{res.profile.first_name} {res.profile.last_name} - {res.status} {res.reason}"
        print(fmt)


if __name__ == "__main__":
    main()
