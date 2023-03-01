from racket_mutation_analysis.racket_mutation.mutators.num_literals_mut import NumLiteralsMutator

from . import mutant_base_test


class TestNumLiteralsMutator(mutant_base_test.MutantBaseTest):
    def test_one_num_literal(self):
        self.mutant_diff_test(
            '2',
            ['0', '-1', '1', '1.0', '3.0'],
            [NumLiteralsMutator],
        )

    def test_non_applicable_num_literal(self):
        self.mutant_diff_test(
            '(/ a b)',
            [],
            [NumLiteralsMutator]
        )

    def test_run_simple_arithmetic_num_literals_run(self):
        self.complete_test(
            '(+ 1 2)',
            [NumLiteralsMutator],
            [('(+ 0 2)', '2'),
             ('(+ -1 2)', '1'),
             ('(+ 1 2)', '3'),
             ('(+ 0.0 2)', '2.0'),
             ('(+ 2.0 2)', '4.0'),
             ('(+ 1 0)', '1'),
             ('(+ 1 -1)', '0'),
             ('(+ 1 1)', '2'),
             ('(+ 1 1.0)', '2.0'),
             ('(+ 1 3.0)', '4.0')]
        )

    def test_run_simple_floating_point_num_literals_run(self):
        self.complete_test(
            '(* 4.0 2.0)',
            [NumLiteralsMutator],
            [('(* 0 2.0)', '0'),
             ('(* -1 2.0)', '-2.0'),
             ('(* 1 2.0)', '2.0'),
             ('(* 3.0 2.0)', '6.0'),
             ('(* 5.0 2.0)', '10.0'),
             ('(* 4.0 0)', '0'),
             ('(* 4.0 -1)', '-4.0'),
             ('(* 4.0 1)', '4.0'),
             ('(* 4.0 1.0)', '4.0'),
             ('(* 4.0 3.0)', '12.0')]
        )
