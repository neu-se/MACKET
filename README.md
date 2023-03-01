# Racket Mutation Testing
[![DOI](https://zenodo.org/badge/607357150.svg)](https://zenodo.org/badge/latestdoi/607357150)

## Installing the Package
Download the latest version from the release page and install it with pip (requires Python >= 3.10):
```
python3 -m pip install {version}.whl
```

## Basic Usage
First, create an empty phase command script by running:
```
generate-mutants --init
```
Replace {instructor-solution} and {hw-name} to specify the file to seed mutants in
and the file to record the generated mutants in.

Then, edit the generated script "mutation_commands.sh" to include the commands
needed for each phase. The `assignment_template` directory an example
of what this could look like for a racket assignment.

Next, generate the mutants with:
```
generate-mutants {instructor-solution}.rkt {hw-name}-mutants.yml
```

And finally run the mutants with:
```
run-mutants --run_tests_in_one_batch {hw-name}-mutants.yml
```

## Dev Setup
Requires python3.10 (with virtual environments) and [editorconfig](https://editorconfig.org/).

After installing python3.10, create a virtual environment and install dependencies:
```
python3.10 -m venv venv
source venv/bin/activate

python -m pip install --upgrade pip
python -m pip install pip-tools

pip-sync requirements-dev.txt
```

## Linters
To run pycodestyle, isort, and pyright:
```
./lint.sh
```

## Racket AST and Visitor
AST node classes can be found at the beginning of racket_ast/scheme_reader.py, and visitor classes
are in racket_ast/visitor.py. An example use of the visitor class can be found in read_write_test.py.
The `main` function file reads a file from stdin or the command line, parses the AST (by calling
`racket_ast.scheme_reader.read_file`), and invokes a `ToStrVisitor` on the AST, which prints
the AST back out to stdout (discarding comments and replacing tabs with a single space, but
otherwise preserving the source code structure).
