import io
import subprocess
import tempfile
import unittest
from typing import List, Sequence, Type

from racket_mutation_analysis.racket_ast.scheme_reader import SchemeReader
from racket_mutation_analysis.racket_mutation.mutant_generator import MutantGenerator
from racket_mutation_analysis.racket_mutation.mutators.mutator import MutatorVisitor


class MutantBaseTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.maxDiff = None

    # compares generated mutants for given input to given expected mutants
    def mutant_diff_test(self,
                         program_src: str, expected: List[str],
                         mutator_classes: Sequence[Type[MutatorVisitor]]):

        actual = self.generate_mutants(program_src, mutator_classes)
        self.assertEqual(expected, actual)

    # generates mutants for the given input with the given mutators
    def generate_mutants(self,
                         program_src: str,
                         mutator_classes: Sequence[Type[MutatorVisitor]]):

        ast = SchemeReader().read_file(io.StringIO(program_src))
        input_array = program_src.splitlines(keepends=True)
        mutant_generator = MutantGenerator(ast, input_array, mutator_classes)
        actual_tuple = mutant_generator.run()
        actual = []

        for mutant, mutated_file in actual_tuple:
            actual.append(mutated_file)

        return actual

    def complete_test(self,
                      program_src: str,
                      mutator_classes: Sequence[Type[MutatorVisitor]],
                      # first list is mutated programs, second is expected outputs
                      expected: List[tuple[str, str]],
                      test_case: str = ''):
        actual = self.generate_mutants(program_src, mutator_classes)
        self.assertEqual([item[0] for item in expected], actual)

        for mutated_program, expected_output in expected:
            with tempfile.NamedTemporaryFile() as temp:
                temp.write(b'#lang racket\n' + mutated_program.encode('utf-8')
                           + b'\n' + test_case.encode('utf-8'))
                temp.seek(0)
                output = subprocess.run(['racket', temp.name], text=True, capture_output=True)
                self.assertEqual(expected_output, output.stdout.strip())
