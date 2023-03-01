from racket_mutation_analysis.racket_mutation.mutators.empty_string import EmptyStringMutator

from . import mutant_base_test


class TestEmptyStringMutator(mutant_base_test.MutantBaseTest):
    def test_hello_empty_string(self):
        self.mutant_diff_test(
            '\"hello\"',
            ['\"\"'],
            [EmptyStringMutator],
        )

    def test_already_empty_string(self):
        self.mutant_diff_test(
            '\"\"',
            ['\"\"'],
            [EmptyStringMutator]
        )

    def test_run_simple_arithmetic_flip_sign(self):
        self.complete_test(
            '\"hello\"',
            [EmptyStringMutator],
            [('\"\"', '\"\"')]
        )
