from racket_mutation_analysis.racket_mutation.mutators.flip_bools import FlipBooleansMutator

from . import mutant_base_test


class TestFlipNumSignMutator(mutant_base_test.MutantBaseTest):
    def test_true_flip(self):
        self.mutant_diff_test(
            '#t',
            ['#f'],
            [FlipBooleansMutator],
        )

    def test_false_flip(self):
        self.mutant_diff_test(
            '#f',
            ['#t'],
            [FlipBooleansMutator]
        )

    def test_run_unapplicable_boolean_flip(self):
        self.mutant_diff_test(
            '(/ 4.0 2.0)',
            [],
            [FlipBooleansMutator]
        )

    def test_run_simple_expression_flip_booleans(self):
        self.complete_test(
            '(if #t #f #t)',
            [FlipBooleansMutator],
            [('(if #f #f #t)', '#t'),
             ('(if #t #t #t)', '#t'),
             ('(if #t #f #f)', '#f')]
        )
