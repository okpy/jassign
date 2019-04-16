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


In your workflow, you would replace the example notebook `tests/example.ipynb` with the master solution notebook, which was augmented with the metadata and commands from the [notebook format](docs/notebook-format.md).
`tests/output` is the path to where the output will be stored (currently, the output contains two directories `autograder` and `student`, which contain the full set of tests and solutions, and the redacted version respectively).
`some/course` is the endpoint of the assignment that's listed on okpy.


Before you run the `jassign` command, make sure that you **run the entire notebook** top to bottom (`Cell -> Run All`) to make sure that every cell has the correct output -- the output of the cells will be turned into the appropriate tests stored in the provided output directory (second argument of the `jassign` command). If you change the tests, you need to re-generate the files by re-running the notebook and the `jassign` command. **Note**: `jassign` will issue an error and quit if the output directory already exists.




You can then generate a PDF from the result:

```python
jassign-pdf tests/output/autograder/example.ipynb tests/output/autograder/example.pdf
```
