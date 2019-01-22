"""Export a notebook as a PDF for manual grading.

Adapted from https://github.com/dibyaghosh/gsExport
"""

from IPython.core.display import display, HTML
from nbconvert import PDFExporter
from tqdm import tqdm

import glob
import hashlib
import nbconvert
import nbformat
import os
import pkg_resources
import re
import shutil


def generate_pdf(nb_path, pdf_path, **kwargs):
    assert run_from_ipython(), "You must run this from within a notebook"
    print("Generating PDF...")
    filtered = load_and_filter(nb_path)
    if not export_notebook(filtered, pdf_path, **kwargs):
        display(HTML(
            """<h2>Export to PDF failed. Please read the error message above.</h2>
            Try running one of these functions to debug:
            <ul>
            <li> generate_submission({nb}, {pdf}, debug=True) # See full error message
            <li> cell_by_cell({nb}) # See which cell is causing you grief
            </ul>
            """.format(nb=nb_path, pdf=pdf_path)
            ))


def cell_by_cell(nb_path):
    assert run_from_ipython(), "You must run this from within a notebook"
    filtered = load_and_filter(nb_path)
    temp_nb = filtered.copy()

    for cell in tqdm(filtered.cells):
        if cell['cell_type'] == 'code':
            continue
        temp_nb.cells = [cell]
        error = has_error(temp_nb)

        if error is not None:
            print("""

            There is an error with the following cell:
            ==========================================================================

            %s

            ==========================================================================
            Here's the error message we were able to extract

            %s

            ==========================================================================
            """%(cell['source'],str(error)))


QUESTION_TAG = re.compile(r"\s*<!--\s*EXPORT TO PDF\s*-->\s*")
NUM_QUESTIONS_TAG = re.compile(r"\s*<!--\s*EXPECT (\d+) EXPORTED QUESTIONS\s*-->\s*")


def is_question_cell(cell):
    return cell['cell_type'] == 'markdown' and bool(QUESTION_TAG.search(cell['source']))


def load_and_filter(nb_path):
    nb = nbformat.read(nb_path, nbformat.current_nbformat)
    check_num_questions(nb)
    return filter_nb(nb)


def fix_dollar_sign(cell):
    if 'cell_type' in cell and cell['cell_type'] == 'markdown':
        cell['source'] = cell['source'].replace('$ ','$').replace(' $','$')


def paraphrase(text,fromBegin=3,fromEnd=3):
    numLines = text.count('\n')
    if numLines < fromBegin + fromEnd:
        return text
    textSplit = text.split('\n')
    newParts = (textSplit[:fromBegin] +
                ['... Omitting %d lines ... ' % (numLines-fromBegin-fromEnd)] +
                textSplit[-1*fromEnd:])
    return '\n'.join(newParts)


def clean_cells(cells):
    """ Works in place """
    for cell in cells:
        if 'outputs' in cell:
            # Paraphrase output
            for output in cell['outputs']:
                if output.get('output_type', 'NA') == 'stream' and 'text' in output:
                    output['text'] = paraphrase(output['text'])
                if output.get('output_type','NA') == 'execute_result':
                    if 'data' in output and 'text/plain' in output['data']:
                        output['data']['text/plain'] = paraphrase(output['data']['text/plain'])
                if output.get('output_type', 'NA') == 'error' and 'traceback' in output:
                    output['traceback'] = output['traceback'][:1]

        if 'source' in cell and (cell['source'].count('\n') > 30 or len(cell['source']) > 4000):
            print('This cell has a lot of content! Perhaps try to shorten your response. ')
            print("\n\n\n", cell['source'][:200])

        # TODO(denero) Ask Dibya why this was here.
        # fix_dollar_sign(cell)


def check_num_questions(nb):
    """Check that the number of questions that appear is the number expected."""
    num_questions = len([cell for cell in nb['cells'] if is_question_cell(cell)])
    expected_tags = [NUM_QUESTIONS_TAG.search(cell['source']) for cell in nb['cells']]
    num_expecteds = [int(m.group(1)) for m in expected_tags if m]
    if num_expecteds:
        num_expected = num_expecteds[0]
        assert all(n == num_expected for n in num_expecteds[1:]), 'conflicting num expected'
        assert num_expected == num_questions,(
            "The number of questions (%d) is different than the expected number (%d). "
            "Did you accidentally delete a question?") % (num_questions, num_expected)


def filter_nb(nb):
    """Returns the parts of nb tagged for export."""
    new_cells = []
    for i, cell in enumerate(nb['cells']):
        if is_question_cell(cell):
            new_cells.append(cell)
            assert len(nb['cells']) > i + 1, 'A response cell must follow each question cell'
            assert not is_question_cell(nb['cells'][i+1]), 'Two question cells in a row'
            new_cells.append(nb['cells'][i + 1])

    clean_cells(new_cells)
    filtered = nb.copy()
    filtered['cells'] = new_cells
    return filtered


def export_notebook(nb, pdf_path, template="test.tplx", debug=False):
    """Write notebook as PDF to pdf_path. Return True on success or False on error."""
    shutil.copyfile(pkg_resources.resource_filename(__name__, template), "test.tplx")
    pdf_exporter = PDFExporter()
    pdf_exporter.template_file = "test.tplx"
    try:
        pdf_output = pdf_exporter.from_notebook_node(nb)
        with open(pdf_path, "wb") as out:
            out.write(pdf_output[0])
            print("Saved", pdf_path)
        return True
    except nbconvert.pdf.LatexFailed as error:
        print("There was an error generating your LaTeX")
        output = error.output
        if not debug:
            print("To see the full error message, run with debug=True")
            output = "\n".join(error.output.split("\n")[-15:])
        print("=" * 30)
        print(output)
        print("=" * 30)
        return False


def has_error(nb):
    pdf_exporter = PDFExporter()
    try:
        pdf_exporter.from_notebook_node(nb)
        return None
    except nbconvert.pdf.LatexFailed as error:
        return "\n".join(error.output.split("\n")[-15:])


def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False
