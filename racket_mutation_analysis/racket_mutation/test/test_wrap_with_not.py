from racket_mutation_analysis.racket_mutation.mutators.wrap_with_not import WrapWithNotMutator

from . import mutant_base_test


class TestWrapWithNotMutator(mutant_base_test.MutantBaseTest):
    def test_wrap_and_with_not(self):
        self.mutant_diff_test(
            '(and #t #f)',
            ['(not (and #t #f))'],
            [WrapWithNotMutator])

    def test_wrap_or_with_not(self):
        self.mutant_diff_test(
            '(or a b)',
            ['(not (or a b))'],
            [WrapWithNotMutator])

    def test_and_or_mutators(self):
        self.mutant_diff_test(
            '(and (or (and (or #t #f) #t) #f) #t)',
            ['(not (and (or (and (or #t #f) #t) #f) #t))',
             '(and (not (or (and (or #t #f) #t) #f)) #t)',
             '(and (or (not (and (or #t #f) #t)) #f) #t)',
             '(and (or (and (not (or #t #f)) #t) #f) #t)'],
            [WrapWithNotMutator])

    def test_complete_wrap_with_not(self):
        self.mutant_diff_test(
            '(define (logical a b c) (or (and a b) c))',
            ['(define (logical a b c) (not (or (and a b) c)))',
             '(define (logical a b c) (or (not (and a b)) c))'],
            [WrapWithNotMutator])

    def test_non_applicable_mutator_wrap_not(self):
        self.mutant_diff_test(
            '(+ 1 2)',
            [],
            [WrapWithNotMutator])

    def test_empty_list_handling(self) -> None:
        self.mutant_diff_test(
            "'()",
            [],
            [WrapWithNotMutator]
        )

    def test_wrap_and_mutator_run(self):
        self.complete_test(
            '(and #t #f)',
            [WrapWithNotMutator],
            [('(not (and #t #f))', '#t')])

    def test_and_or_wrap_mutators_run(self):
        self.complete_test(
            '(and (or (and (or #t #f) #t) #f) #t)',
            [WrapWithNotMutator],
            [('(not (and (or (and (or #t #f) #t) #f) #t))', '#f'),
             ('(and (not (or (and (or #t #f) #t) #f)) #t)', '#f'),
             ('(and (or (not (and (or #t #f) #t)) #f) #t)', '#f'),
             ('(and (or (and (not (or #t #f)) #t) #f) #t)', '#f')])

    def test_complete_wrap_run(self):
        self.complete_test(
            '(define (logical a b c) (or (and a b) c))',
            [WrapWithNotMutator],
            [('(define (logical a b c) (not (or (and a b) c)))', '#f'),
             ('(define (logical a b c) (or (not (and a b)) c))', '#t')],
            '(logical #t #f #t)')
