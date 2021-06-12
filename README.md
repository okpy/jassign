# jassign: Jupyter Notebook Assignments

**This project is DEPRECATED because its functionality now exists in [otter grader](https://github.com/ucbds-infra/otter-grader). Use that instead!**

Format and tools for authoring and distributing Jupyter notebook assignments

Requires: **Python 3** (even if it's installed, check that it's your working version `python --version`)


## Getting started
Course instructors author assignments as Jupyter notebooks by creating a
notebook that contains setup code, questions, solutions, and tests to validate
those solutions. This project prepares an assignment to be distributed to
students and later scored automatically.

The [notebook format](docs/notebook-format.md) is not specific to a programming
language or autograding framework, but was designed to be used with
[okpy](https://github.com/okpy/ok), which is Python based. Contributions to
support other testing frameworks, such as [nbgrader[](), and other programming
languages are welcome.

An example notebook appears in `tests/example.ipynb`, which uses the [notebook
format](docs/notebook-format.md). To convert it, run:

```python
jassign tests/example.ipynb tests/output some/course
```


* `tests/example.ipynb`: an example notebook path that you'll need to replace with the _path to the master solution notebook_, which was augmented with the metadata and commands from the [notebook format](docs/notebook-format.md).
* `tests/output`: _the path to where the output will be stored_ 
  * the output contains two directories `autograder` and `student`
  * the `autograder` directory contains the full set of tests and a solution notebook (a solution notebook is different from the master notebook, because it is not formatted accordidng to the [notebook format](docs/notebook-format.md) but instead looks like the student notebook with solutions)
  * the `student` directory contains an automatically created redacted version. 
  * **Note**: currently, the output directories will **not** contain the data files, e.g., csv or json files, that you used when creating the master notebook: make sure you add them to the `student` directory before releasing it to students
* `some/course` is the endpoint/path of the assignment that's listed on okpy.org when you create the new assignment (typically starts with your university abbreviation and has a course name in it, ending with the assignment name).


Before you run the `jassign` command, **run the entire notebook** top to bottom (`Cell -> Run All`) to make sure that every cell has the correct output -- the output of the cells will be turned into the appropriate tests stored in the provided output directory (second argument of the `jassign` command). If you change the tests, you need to re-generate the files by re-running the notebook and the `jassign` command. **Note**: `jassign` will issue an error and quit if the output directory already exists, so you need to remove the output directory first (taking care to keep the master solution notebook safe).


You can then generate a PDF from the result:

```python
jassign-pdf tests/output/autograder/example.ipynb tests/output/autograder/example.pdf
```


# Caution / Troubleshooting

### PROBLEM: "Test outside of a question"

```
File "/opt/conda/lib/python3.6/site-packages/jassign/to_ok.py", line 141, in gen_ok_cells
    assert not is_test_cell(cell), 'Test outside of a question: ' + str(cell)
AssertionError: Test outside of a question:
```

If you get this error, this means that you have _more than one cell_ between the markdown cell that declared the question (i.e., the one that contains `#BEGIN QUESTION`) and the cell that contains the `# TEST`. 

**SOLUTION**: remove the extra code/markdown cell(s) either between the solution cell and the markdown cell with the `#BEGIN QUESTION` or between the solution cell and the `# TEST` cell.


### PROBLEM: Test cell with a blank on the last line

If your test contains a blank/newline after the test, jassign seems to automatically add a semicolon at the end of the test, thus, supressing the output of the command.

Example:
```
# TEST
movies.head(1)['plots'][0]=='Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.'

```

The above statement turns into the following failed test in the students' notebook:
```
>>> movies.head(1)['plots'][0]=='Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.';
>>> 

# Error: expected
#     True
# but got

```
**SOLUTION**: remove the blank line at the end of the `# TEST` cell.


### PROBLEM: `# SOLUTION` shows up in the student notebook 

If your test has no space between the `#` and a command before it, then that line will show up in the student notebook, even though it is marked as `# SOLUTION`. 

**SOLUTION**: add a space before the test command and `# SOLUTION` and re-run the jassign command to update the tests.
