from jassign.to_pdf import is_question_cell, fix_dollar_sign
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


def test_fix_dollar_sign():
    cases = [
        ("Diff $ x^2 $ and $ x^3$ and you'll get $3.",
         "Diff $x^2$ and $x^3$ and you'll get $3."),
        ("$ \exp(3) $ is larger than $20 $.",
         "$\exp(3)$ is larger than $20$.")
    ]
    for input, expected in cases:
        assert fix_dollar_sign(input) == expected





