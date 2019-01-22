from jassign.to_pdf import is_question_cell
import nbformat

def test_is_question_cell():
    yes = nbformat.v4.new_markdown_cell()
    yes['source'] = """Here's a question cell.

    <!-- EXPORT TO PDF -->

    And that's the whole question!
    """
    no = nbformat.v4.new_markdown_cell()
    no['source'] = """This is not a question to EXPORT"""
    assert is_question_cell(yes)
    assert not is_question_cell(no)

