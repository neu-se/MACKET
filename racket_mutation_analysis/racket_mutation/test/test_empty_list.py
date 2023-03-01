from racket_mutation_analysis.racket_mutation.mutators.empty_list import EmptyListMutator

from . import mutant_base_test


class TestEmptyListMutator(mutant_base_test.MutantBaseTest):
    def test_list_only(self):
        self.mutant_diff_test(
            '(list 1 2)',
            ['\'()'],
            [EmptyListMutator],
        )

    def test_list_only_with_cons(self):
        self.mutant_diff_test(
            '(cons 1 2)',
            ['\'()'],
            [EmptyListMutator],
        )

    def test_already_empty_list(self):
        self.mutant_diff_test(
            '\'()',
            [],
            [EmptyListMutator]
        )

    def test_non_applciable_empty_list(self):
        self.mutant_diff_test(
            '(+ 1 2)',
            [],
            [EmptyListMutator]
        )

    def test_list_only_run(self):
        self.complete_test(
            '(list 1 2)',
            [EmptyListMutator],
            [('\'()', '\'()')]
        )

    def test_list_only_with_cons_run(self):
        self.complete_test(
            '(cons 1 2)',
            [EmptyListMutator],
            [('\'()', '\'()')]
        )
