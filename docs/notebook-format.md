# Notebook Assignments with Embedded Solutions and Tests

The following specification for embedding tests into a Jupyter notebook has the
following characteristics:

1. Each test is a cell with the expressions or statements to be evaluated. The
   expected output of the test is the output of the cell.
2. Tests are grouped into questions, and each question has associated metadata
   such as the question name and number of points.
3. Metadata are expressed within notebook cells in YAML.

This format is designed for easy assignment authoring. A notebook in this format
can be converted automatically to the [OK
format](https://github.com/data-8/Gofer-Grader/blob/master/docs/ok-test-format.md)
before it is distributed to students.

## Questions

An example question within a notebook:

<img src="example-question.png" />

Also see this [longer example
notebook](https://github.com/okpy/jupyter-assignment/blob/master/tests/example.ipynb).

A question is a description *Markdown* cell, followed by a response cell,
followed by zero or more test *code* cells. The description cell must contain a
code block (enclosed in triple backticks) that begins with `BEGIN QUESTION` on
its own line, followed by YAML that defines metadata associated with the
question.

The rest of the code block within the description cell must be YAML-formatted
with the following fields (in any order):

* name (required) - a string identifier that is a legal file name.
* manual (optional) - a boolean (default False); whether to include the response
  cell in a PDF for manual grading.
* points (optional) - a number (default 1); how many points the question is
  worth.

The response cell must always appear directly below the description cell (where
the question metadata is defined) and contain a correct response, along with
annotations describing how the cell should be presented to students. See
*Solution Removal* below.

The test cells are any code cells following the response cell that begin with a
comment containing either the capitalized word `TEST` or `HIDDEN TEST`. A `TEST`
is distributed to students so that they can validate their work. A `HIDDEN TEST`
is not distributed to students, but is used for scoring their work.

**Note:** Currently, the conversion to ok format does not handle multi-line
tests if any line but the last one generates output. So, if you want to print
twice, make two separate test cells instead of:

```python
print(1)
print(2)
```

## Solution Removal

Solutions are removed from all cells if formatted as follows.

* A line ending in `# SOLUTION` will be replaced by `...`, properly indented. If
  that line is an assignment statement, then only the expression(s) after the
  `=` symbol will be replaced.
* A line ending in `# SOLUTION NO PROMPT` will be removed.

```python
def square(x):
    y = x * x # SOLUTION NO PROMPT
    return y # SOLUTION

nine = square(3) # SOLUTION
```

would be presented to students as

```python
def square(x):
    ...

nine = ...
```

* A line `# BEGIN SOLUTION` or `# BEGIN SOLUTION NO PROMPT` must be paired with
  a later line `# END SOLUTION`. All lines in between are replaced with `...` or
  removed completely in the case of `NO PROMPT`.
* A line `""" # BEGIN PROMPT` must be paired with a later line `""" # END
  PROMPT`. The contents of this multiline string (excluding the `# BEGIN
  PROMPT`) appears in the student cell. Single or double quotes are allowed.
  Optionally, a semicolon can be used to suppress output: `"""; # END PROMPT`

```python
pi = 3.14
if True:
    # BEGIN SOLUTION
    radius = 3
    area = radius * pi * pi
    # END SOLUTION
    print('A circle with radius', radius, 'has area', area)
def circumference(r):
    # BEGIN SOLUTION NO PROMPT
    return 2 * pi * r
    # END SOLUTION
    """ # BEGIN PROMPT
    # Next, define a circumference function.
    pass
    """; # END PROMPT
```

would be presented to students as

```python
pi = 3.14
if True:
    ...
    print('A circle with radius', radius, 'has area', area)
def circumference(r):
    # Next, define a circumference function.
    pass
```

* A line starting with `**SOLUTION**` or `**SOLUTION:**` is replaced with
  `*Write your answer here, replacing this text.*`, which will be rendered as
  italics within a Markdown cell.

## More info

**TODO pointers to docs on how to distribute assignments to students, configure autograders, etc.**