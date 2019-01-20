# jassign: Jupyter Notebook Assignments
Format and tools for authoring and distributing Jupyter notebook assignments

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

This command will create `tests/output` with a student version and an autograder
version as subdirectories.

For options, run: `jassign -h`