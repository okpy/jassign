"""Convert a Jupyter notebook to OK format for release."""

import argparse
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
    parser.add_argument("--no-submit-cell", help="Don't output submit cell at end of notebook",
    	dest="no_submit_cell", const=True, default=False, action="store_const"
    	)
    return parser.parse_args()


def main():
    args = parse_args()
    gen_views(pathlib.Path(args.master), pathlib.Path(args.result),
              args.endpoint, args.no_submit_cell)

if __name__ == "__main__":
    main()
