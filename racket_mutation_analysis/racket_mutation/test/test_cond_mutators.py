from racket_mutation_analysis.racket_mutation.mutators.cond_mut import CondMutator

from . import mutant_base_test


class TestCondMutators(mutant_base_test.MutantBaseTest):
    def test_cond_only_else_mutator(self):
        self.mutant_diff_test(
            '(cond[else 2])',
            [],
            [CondMutator]
        )

    def test_series_cond_expression_mutator(self):
        self.mutant_diff_test(
            '(cond[(< a b) 2][(> a b) 3][(= a b) 4])',
            ['(cond[#t 2][(> a b) 3][(= a b) 4])', '(cond[#f 2][(> a b) 3][(= a b) 4])',
             '(cond[(< a b) 2][#t 3][(= a b) 4])', '(cond[(< a b) 2][#f 3][(= a b) 4])',
             '(cond[(< a b) 2][(> a b) 3][#t 4])', '(cond[(< a b) 2][(> a b) 3][#f 4])'],
            [CondMutator]
        )

    def test_cond_true_mutator(self):
        self.mutant_diff_test(
            '(cond[#t 2][else #f])',
            ['(cond[#t 2][else #f])',
             '(cond[#f 2][else #f])'],
            [CondMutator]
        )

    def test_cond_false_mutator(self):
        self.mutant_diff_test(
            '(cond [#f #t] [else 2])',
            ['(cond [#t #t] [else 2])',
             '(cond [#f #t] [else 2])'],
            [CondMutator]
        )

    def test_cond_expression_mutator(self):
        self.mutant_diff_test(
            '(cond[(= a b) 2][else #t])',
            ['(cond[#t 2][else #t])', '(cond[#f 2][else #t])'],
            [CondMutator]
        )

    def test_complete_cond(self):
        self.mutant_diff_test(
            '(define (foo a b c) (cond [(> a b) a] [(> b a) b] [else c]))',
            ['(define (foo a b c) (cond [#t a] [(> b a) b] [else c]))',
             '(define (foo a b c) (cond [#f a] [(> b a) b] [else c]))',
             '(define (foo a b c) (cond [(> a b) a] [#t b] [else c]))',
             '(define (foo a b c) (cond [(> a b) a] [#f b] [else c]))'],
            [CondMutator]
        )

    def test_complete(self):
        self.mutant_diff_test(
            '(define (foo a b c)\n(cond\n[(> a b) a]\n[(> b a) b]\n[else c]))',
            ['(define (foo a b c)\n(cond\n[#t a]\n[(> b a) b]\n[else c]))',
             '(define (foo a b c)\n(cond\n[#f a]\n[(> b a) b]\n[else c]))',
             '(define (foo a b c)\n(cond\n[(> a b) a]\n[#t b]\n[else c]))',
             '(define (foo a b c)\n(cond\n[(> a b) a]\n[#f b]\n[else c]))'],
            [CondMutator]
        )

    def test_non_applicable_mutator(self):
        self.mutant_diff_test(
            '(if #t 2 3)',
            [],
            [CondMutator]
        )

    def test_empty_list_handling(self) -> None:
        self.mutant_diff_test(
            "'()",
            [],
            [CondMutator]
        )

    def test_cond_true_mutator_run(self):
        self.complete_test(
            '(cond[#t 2][else #f])',
            [CondMutator],
            [('(cond[#t 2][else #f])', '2'),
             ('(cond[#f 2][else #f])', '#f')]
        )

    def test_cond_false_mutator_run(self):
        self.complete_test(
            '(cond [#f #t] [else 2])',
            [CondMutator],
            [('(cond [#t #t] [else 2])', '#t'),
             ('(cond [#f #t] [else 2])', '2')]
        )

    def test_complete_cond_run(self):
        self.complete_test(
            '(define (foo a b c) (cond [(> a b) a] [(> b a) b] [else c]))',
            [CondMutator],
            [('(define (foo a b c) (cond [#t a] [(> b a) b] [else c]))', '1'),
             ('(define (foo a b c) (cond [#f a] [(> b a) b] [else c]))', '2'),
             ('(define (foo a b c) (cond [(> a b) a] [#t b] [else c]))', '2'),
             ('(define (foo a b c) (cond [(> a b) a] [#f b] [else c]))', '3')],
            '(foo 1 2 3)'
        )
