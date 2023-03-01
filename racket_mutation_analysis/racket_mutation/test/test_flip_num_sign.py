from racket_mutation_analysis.racket_mutation.mutators.flip_num_sign import FlipNumSignMutator

from . import mutant_base_test


class TestFlipNumSignMutator(mutant_base_test.MutantBaseTest):
    def test_addition_flip_num(self):
        self.mutant_diff_test(
            '(+ 1 2)',
            ['(+ (- 1) 2)',
             '(+ 1 (- 2))'],
            [FlipNumSignMutator],
        )

    def test_non_literal_flip_sign(self):
        self.mutant_diff_test(
            '(/ a b)',
            [],
            [FlipNumSignMutator]
        )

    def test_run_simple_arithmetic_flip_sign(self):
        self.complete_test(
            '(+ 1 2)',
            [FlipNumSignMutator],
            [('(+ (- 1) 2)', '1'),
             ('(+ 1 (- 2))', '-1')]
        )

    def test_run_simple_floating_point_flip_sign(self):
        self.complete_test(
            '(/ 4.0 2.0)',
            [FlipNumSignMutator],
            [('(/ (- 4.0) 2.0)', '-2.0'),
             ('(/ 4.0 (- 2.0))', '-2.0')]
        )
