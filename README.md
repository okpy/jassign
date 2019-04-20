# jassign: Jupyter Notebook Assignments
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
* `some/course` is the endpoint/path of the assignment that's listed on okpy (typically starts with your university abbreviation and has a course name in it, ending with the assignment name).


Before you run the `jassign` command, make sure that you **run the entire notebook** top to bottom (`Cell -> Run All`) to make sure that every cell has the correct output -- the output of the cells will be turned into the appropriate tests stored in the provided output directory (second argument of the `jassign` command). If you change the tests, you need to re-generate the files by re-running the notebook and the `jassign` command. **Note**: `jassign` will issue an error and quit if the output directory already exists.




You can then generate a PDF from the result:

```python
jassign-pdf tests/output/autograder/example.ipynb tests/output/autograder/example.pdf
```
