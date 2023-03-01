"""
Use this for testing our parser. Parses a Racket program and writes
it back out to standard out. Whitespace is somewhat preserved (line break
placement is preserved, but not the specific line ending characters;
tabs are replaced with a single space).
Comments are removed and whitespace is left in their place.

Note that to generate mutants, we don't actually need to modify the AST.
We only need to identify the node to mutate and record its location and the
text to substitute.
"""

import argparse
import sys

from racket_mutation_analysis.racket_ast.scheme_reader import SchemeReader
from racket_mutation_analysis.racket_ast.string_visitor import ToStrVisitor


def main():
    """Run a read-print loop for Scheme expressions."""
    args = parse_args()
    with sys.stdin if args.input_file == '-' else open(args.input_file) as f:
        ast = SchemeReader().read_file(f)

    visitor = ToStrVisitor()
    visitor.visit(ast)
    print(visitor.result)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', default='-')

    return parser.parse_args()


if __name__ == '__main__':
    main()
