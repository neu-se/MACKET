from racket_mutation_analysis.racket_mutation.mutators.bool_params_to_bool import BoolParamsToBool

from . import mutant_base_test


class TestBoolParamsToBool(mutant_base_test.MutantBaseTest):
    def test_and_bool_param(self):
        self.mutant_diff_test(
            '(and a b)',
            ['(and #t b)',
             '(and #f b)',
             '(and a #t)',
             '(and a #f)'],
            [BoolParamsToBool])

    def test_or_mutator_param(self):
        self.mutant_diff_test(
            '(or a b)',
            ['(or #t b)',
             '(or #f b)',
             '(or a #t)',
             '(or a #f)'],
            [BoolParamsToBool])

    def test_complete_bool_param(self):
        self.mutant_diff_test(
            '(define (logical a b c) (or (and a b) c))',
            ['(define (logical a b c) (or #t c))',
             '(define (logical a b c) (or #f c))',
             '(define (logical a b c) (or (and a b) #t))',
             '(define (logical a b c) (or (and a b) #f))',
             '(define (logical a b c) (or (and #t b) c))',
             '(define (logical a b c) (or (and #f b) c))',
             '(define (logical a b c) (or (and a #t) c))',
             '(define (logical a b c) (or (and a #f) c))'],
            [BoolParamsToBool])

    def test_non_applicable_mutator_bool_param(self):
        self.mutant_diff_test(
            '(+ 1 2)',
            [],
            [BoolParamsToBool])

    def test_complete_bool_param_run1(self):
        self.complete_test(
            '(define (logical a b c) (or (and a b) c))',
            [BoolParamsToBool],
            [('(define (logical a b c) (or #t c))', '#t'),
             ('(define (logical a b c) (or #f c))', '#t'),
             ('(define (logical a b c) (or (and a b) #t))', '#t'),
             ('(define (logical a b c) (or (and a b) #f))', '#t'),
             ('(define (logical a b c) (or (and #t b) c))', '#t'),
             ('(define (logical a b c) (or (and #f b) c))', '#t'),
             ('(define (logical a b c) (or (and a #t) c))', '#t'),
             ('(define (logical a b c) (or (and a #f) c))', '#t')],
            '(logical #t #t #t)')

    def test_complete_bool_param_run2(self):
        self.complete_test(
            '(define (logical a b c) (or (and a b) c))',
            [BoolParamsToBool],
            [('(define (logical a b c) (or #t c))', '#t'),
             ('(define (logical a b c) (or #f c))', '#t'),
             ('(define (logical a b c) (or (and a b) #t))', '#t'),
             ('(define (logical a b c) (or (and a b) #f))', '#f'),
             ('(define (logical a b c) (or (and #t b) c))', '#t'),
             ('(define (logical a b c) (or (and #f b) c))', '#t'),
             ('(define (logical a b c) (or (and a #t) c))', '#t'),
             ('(define (logical a b c) (or (and a #f) c))', '#t')],
            '(logical #t #f #t)')

    def test_complete_bool_param_run3(self):
        self.complete_test(
            '(define (logical a b c) (or (and a b) c))',
            [BoolParamsToBool],
            [('(define (logical a b c) (or #t c))', '#t'),
             ('(define (logical a b c) (or #f c))', '#f'),
             ('(define (logical a b c) (or (and a b) #t))', '#t'),
             ('(define (logical a b c) (or (and a b) #f))', '#t'),
             ('(define (logical a b c) (or (and #t b) c))', '#t'),
             ('(define (logical a b c) (or (and #f b) c))', '#f'),
             ('(define (logical a b c) (or (and a #t) c))', '#t'),
             ('(define (logical a b c) (or (and a #f) c))', '#f')],
            '(logical #t #t #f)')
