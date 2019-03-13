"""Convert a Jupyter notebook to OK format for release."""

import argparse
import json
import pathlib

try:
    from .to_ok import gen_views
except ImportError:
    from to_ok import gen_views

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("master", help="Notebook with solutions and tests.")
    parser.add_argument("result", help="Directory containing the result.")
    parser.add_argument("endpoint", help="OK endpoint; e.g., cal/data8/sp19")
    parser.add_argument("--no-submit-cell", help="Don't inject a submit cell into the notebook",
                        default=False, action="store_true")
    parser.add_argument("--no-run-tests", help="Don't run tests.",
                        default=False, action="store_true")
    parser.add_argument("--instructions", help="Additional submission instructions")
    return parser.parse_args()


def run_tests(nb_path):
    """Run ok tests in the autograder version of the notebook."""
    with open(nb_path) as f:
        nb = json.load(f)
    print('Run the ok tests before you publish to make sure they work!')
    # TODO implement testing once Gofer-Grader and okpy are compatible


def main():
    args = parse_args()
    master, result = pathlib.Path(args.master), pathlib.Path(args.result)
    gen_views(master, result, args)
    if not args.no_run_tests:
        run_tests(result / 'autograder'  / master.name )

if __name__ == "__main__":
    main()
