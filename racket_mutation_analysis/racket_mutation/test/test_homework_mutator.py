from racket_mutation_analysis.racket_mutation.mutators.homework_mutator import Homework4and5Mutator

from . import mutant_base_test


class TestArithmeticDeletionMutator(mutant_base_test.MutantBaseTest):
    def test_mutants_for_take_n(self):
        self.mutant_diff_test(
            '(take-n 5 (list 1 2 3))',
            ["(take-n 5 '())",
             "'()",
             '(drop-n 5 (list 1 2 3))'],
            [Homework4and5Mutator],
        )

    def test_mutants_for_drop_n(self):
        self.mutant_diff_test(
            '(drop-n 5 (list 1 2 3))',
            ["(drop-n 5 '())",
             "'()",
             '(take-n 5 (list 1 2 3))'],
            [Homework4and5Mutator],
        )

    def test_mutants_for_take_while(self):
        self.mutant_diff_test(
            '(take-while even? (list 1 2 3))',
            ["(take-while even? '())",
             "'()",
             '(drop-while even? (list 1 2 3))'],
            [Homework4and5Mutator],
        )

    def test_mutants_for_drop_while(self):
        self.mutant_diff_test(
            '(drop-while even? (list 1 2 3))',
            ["(drop-while even? '())",
             "'()",
             '(take-while even? (list 1 2 3))'],
            [Homework4and5Mutator],
        )

    def test_mutants_for_group_by(self):
        self.mutant_diff_test(
            '(group-by = (list 1 2 3))',
            ["(group-by = '())"],
            [Homework4and5Mutator],
        )

    def test_empty_list_handling(self) -> None:
        self.mutant_diff_test(
            "'()",
            [],
            [Homework4and5Mutator]
        )
