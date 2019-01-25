"""Convert a Jupyter notebook to OK format for release."""

import argparse
import pathlib

from .to_ok import gen_views

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("master", help="Notebook with solutions and tests.")
    parser.add_argument("result", help="Directory containing the result.")
    parser.add_argument("endpoint", help="OK endpoint; e.g., cal/data8/sp19")
    return parser.parse_args()


def main():
    args = parse_args()
    gen_views(pathlib.Path(args.master), pathlib.Path(args.result),
              args.endpoint)

if __name__ == "__main__":
    main()
