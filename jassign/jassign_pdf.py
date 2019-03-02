"""Convert a Jupyter notebook to a PDF."""

import argparse

try:
    from .to_pdf import generate_pdf_cmdline
except ImportError:
    from to_pdf import generate_pdf_cmdline


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook", help="Notebook with export annotations.")
    parser.add_argument("pdf", help="PDF containing the result.")
    return parser.parse_args()


def main():
    args = parse_args()
    generate_pdf_cmdline(args.notebook, args.pdf)

if __name__ == "__main__":
    main()
