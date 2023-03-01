from racket_mutation_analysis.racket_mutation.mutators.num_comparison_mutator import (
    NumberComparisonMutator
)

from . import mutant_base_test


class TestNumberComparisonMutator(mutant_base_test.MutantBaseTest):
    def test_greater_than_replacements(self):
        self.mutant_diff_test(
            '(> 1 2)',
            ['(>= 1 2)',
             '(< 1 2)',
             '(<= 1 2)',
             '(= 1 2)'],
            [NumberComparisonMutator],
        )

    def test_greater_than__or_equal_to_replacements(self):
        self.mutant_diff_test(
            '(>= 1 2)',
            ['(> 1 2)',
             '(< 1 2)',
             '(<= 1 2)',
             '(= 1 2)'],
            [NumberComparisonMutator],
        )

    def test_less_than_replacements(self):
        self.mutant_diff_test(
            '(< 1 2)',
            ['(> 1 2)',
             '(>= 1 2)',
             '(<= 1 2)',
             '(= 1 2)'],
            [NumberComparisonMutator],
        )

    def test_less_than__or_equal_to_replacements(self):
        self.mutant_diff_test(
            '(<= 1 2)',
            ['(> 1 2)',
             '(>= 1 2)',
             '(< 1 2)',
             '(= 1 2)'],
            [NumberComparisonMutator],
        )

    def test_greater_than_replacements_run(self):
        self.complete_test(
            '(> 1 2)',
            [NumberComparisonMutator],
            [('(>= 1 2)', '#f'),
             ('(< 1 2)', '#t'),
             ('(<= 1 2)', '#t'),
             ('(= 1 2)', '#f')]
        )

    def test_greater_than__or_equal_to_replacements_run(self):
        self.complete_test(
            '(>= 1 2)',
            [NumberComparisonMutator],
            [('(> 1 2)', '#f'),
             ('(< 1 2)', '#t'),
             ('(<= 1 2)', '#t'),
             ('(= 1 2)', '#f')]
        )

    def test_less_than_replacements_run(self):
        self.complete_test(
            '(< 1 2)',
            [NumberComparisonMutator],
            [('(> 1 2)', '#f'),
             ('(>= 1 2)', '#f'),
             ('(<= 1 2)', '#t'),
             ('(= 1 2)', '#f')]
        )

    def test_less_than__or_equal_to_replacements_run(self):
        self.complete_test(
            '(<= 1 2)',
            [NumberComparisonMutator],
            [('(> 1 2)', '#f'),
             ('(>= 1 2)', '#f'),
             ('(< 1 2)', '#t'),
             ('(= 1 2)', '#f')]
        )

    def test_empty_list_handling(self) -> None:
        self.mutant_diff_test(
            "'()",
            [],
            [NumberComparisonMutator]
        )
