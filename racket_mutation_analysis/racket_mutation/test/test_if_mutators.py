from racket_mutation_analysis.racket_mutation.mutators.if_mut import IfMutator

from . import mutant_base_test


class TestIfMutators(mutant_base_test.MutantBaseTest):
    def test_if_true_mutator(self):
        self.mutant_diff_test(
            '(if #t 2 3)',
            ['(if #t 2 3)',
             '(if #f 2 3)'],
            [IfMutator]
        )

    def test_if_false_mutator(self):
        self.mutant_diff_test(
            '(if #f #t #f)',
            ['(if #t #t #f)',
             '(if #f #t #f)'],
            [IfMutator]
        )

    def test_nested_if_mutator(self):
        self.mutant_diff_test(
            '(if (if (= 1 2) #t #f) #t #f)',
            ['(if #t #t #f)',
             '(if #f #t #f)',
             '(if (if #t #t #f) #t #f)',
             '(if (if #f #t #f) #t #f)'],
            [IfMutator]
        )

    def test_nested_if_mutator2(self):
        self.mutant_diff_test(
            '(if (if (= a b) #t #f) 3 4)',
            ['(if #t 3 4)', '(if #f 3 4)',
             '(if (if #t #t #f) 3 4)', '(if (if #f #t #f) 3 4)'],
            [IfMutator]
        )

    def test_complete_if(self):
        self.mutant_diff_test(
            '(define (foo a b) (if (= a b) #t #f))',
            ['(define (foo a b) (if #t #t #f))',
             '(define (foo a b) (if #f #t #f))'],
            [IfMutator]
        )

    def test_complete_if_2(self):
        self.mutant_diff_test(
            '(define (foo a b c) (if (> a b) (+ a b c) (- a b c)))',
            ['(define (foo a b c) (if #t (+ a b c) (- a b c)))',
             '(define (foo a b c) (if #f (+ a b c) (- a b c)))'],
            [IfMutator]
        )

    def test_already_boolean(self):
        self.mutant_diff_test(
            '(define (foo a b c) (if #t (+ a b c) (- a b c)))',
            ['(define (foo a b c) (if #t (+ a b c) (- a b c)))',
             '(define (foo a b c) (if #f (+ a b c) (- a b c)))'],
            [IfMutator]
        )

    def test_multi_line(self):
        self.mutant_diff_test(
            '(define (foo a b)\n    (if (= a b) a b))',
            ['(define (foo a b)\n    (if #t a b))',
             '(define (foo a b)\n    (if #f a b))'],
            [IfMutator]
        )

    def test_multi_line2(self):
        self.mutant_diff_test(
            '(define (foo a b c d)\n    (if\n(=c d)\na\nb))',
            ['(define (foo a b c d)\n    (if\n#t\na\nb))',
             '(define (foo a b c d)\n    (if\n#f\na\nb))'],
            [IfMutator]
        )

    def test_mutant_across_lines_if(self):
        self.mutant_diff_test(
            '(define (foo a b c) (if (and\na\nb\nc)\na b))',
            ['(define (foo a b c) (if #t\na b))',
             '(define (foo a b c) (if #f\na b))'],
            [IfMutator]
        )

    def test_non_applicable_mutator(self):
        self.mutant_diff_test(
            '(and #t #f)',
            [],
            [IfMutator])

    def test_empty_list_handling(self) -> None:
        self.mutant_diff_test(
            "'()",
            [],
            [IfMutator]
        )

    def test_if_true_mutator_run(self):
        self.complete_test(
            '(if #t 2 3)',
            [IfMutator],
            [('(if #t 2 3)', '2'),
             ('(if #f 2 3)', '3')]
        )

    def test_if_false_mutator_run(self):
        self.complete_test(
            '(if #f #t #f)',
            [IfMutator],
            [('(if #t #t #f)', '#t'),
             ('(if #f #t #f)', '#f')]
        )

    def test_nested_if_mutator_run(self):
        self.complete_test(
            '(if (if (= 1 2) #t #f) #t #f)',
            [IfMutator],
            [('(if #t #t #f)', '#t'),
             ('(if #f #t #f)', '#f'),
             ('(if (if #t #t #f) #t #f)', '#t'),
             ('(if (if #f #t #f) #t #f)', '#f')]
        )

    def test_nested_if_mutator2_run(self):
        self.complete_test(
            '(if (if (= a b) #t #f) 3 4)',
            [IfMutator],
            [('(if #t 3 4)', '3'),
             ('(if #f 3 4)', '4'),
             ('(if (if #t #t #f) 3 4)', '3'),
             ('(if (if #f #t #f) 3 4)', '4')],
        )

    def test_complete_if_run(self):
        self.complete_test(
            '(define (foo a b) (if (= a b) #t #f))',
            [IfMutator],
            [('(define (foo a b) (if #t #t #f))', '#t'),
             ('(define (foo a b) (if #f #t #f))', '#f')],
            '(foo 1 2)'
        )

    def test_complete_if_2_run(self):
        self.complete_test(
            '(define (foo a b c) (if (> a b) (+ a b c) (- a b c)))',
            [IfMutator],
            [('(define (foo a b c) (if #t (+ a b c) (- a b c)))', '6'),
             ('(define (foo a b c) (if #f (+ a b c) (- a b c)))', '-4')],
            '(foo 1 2 3)'
        )

    def test_multi_line2_run(self):
        self.complete_test(
            '(define (foo a b c d)\n    (if\n(=c d)\na\nb))',
            [IfMutator],
            [('(define (foo a b c d)\n    (if\n#t\na\nb))', '1'),
             ('(define (foo a b c d)\n    (if\n#f\na\nb))', '2')],
            '(foo 1 2 3 4)'
        )
