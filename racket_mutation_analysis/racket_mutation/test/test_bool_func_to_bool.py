from racket_mutation_analysis.racket_mutation.mutators.bool_func_to_bool import (
    BoolFuncToBoolMutator
)

from . import mutant_base_test


class TestBoolFuncToBool(mutant_base_test.MutantBaseTest):
    def test_one_bool_func(self):
        self.mutant_diff_test(
            '(and a b)',
            ['#t', '#f'],
            [BoolFuncToBoolMutator],
        )

    def test_many_bool_func(self):
        self.mutant_diff_test(
            '(and (not #t) (or #f #t))',
            ['#t', '#f',
             '(and #t (or #f #t))',
             '(and #f (or #f #t))',
             '(and (not #t) #t)',
             '(and (not #t) #f)'],
            [BoolFuncToBoolMutator]
        )

    def test_defined_predicate(self):
        self.mutant_diff_test(
            '(string=? hi bye)',
            ['#t', '#f'],
            [BoolFuncToBoolMutator]
        )

    def test_defined_predicate_in_func(self):
        self.mutant_diff_test(
            '(define (foo a b) (if (string=? a b) a b))',
            ['(define (foo a b) (if #t a b))',
             '(define (foo a b) (if #f a b))'],
            [BoolFuncToBoolMutator],
        )

    def test_new_predicate(self):
        self.mutant_diff_test(
            '(if (car? c) 3 4)',
            ['(if #t 3 4)',
             '(if #f 3 4)'],
            [BoolFuncToBoolMutator]
        )

    def test_one_bool_func_run(self):
        self.complete_test(
            '(and #t #f)',
            [BoolFuncToBoolMutator],
            [('#t', '#t'),
             ('#f', '#f')],
        )

    def test_many_bool_func_run(self):
        self.complete_test(
            '(and (not #t) (or #f #t))',
            [BoolFuncToBoolMutator],
            [('#t', '#t'),
             ('#f', '#f'),
             ('(and #t (or #f #t))', '#t'),
             ('(and #f (or #f #t))', '#f'),
             ('(and (not #t) #t)', '#f'),
             ('(and (not #t) #f)', '#f')]
        )

    def test_defined_predicate_run(self):
        self.complete_test(
            '(string=? \"hi\" \"bye\")',
            [BoolFuncToBoolMutator],
            [('#t', '#t'),
             ('#f', '#f')]
        )

    def test_empty_list_handling(self) -> None:
        self.mutant_diff_test(
            "'()",
            [],
            [BoolFuncToBoolMutator]
        )
