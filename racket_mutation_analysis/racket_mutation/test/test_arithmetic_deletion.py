from racket_mutation_analysis.racket_mutation.mutators.arithmetic_deletion import (
    ArithmeticDeletionMutator
)

from . import mutant_base_test


class TestArithmeticDeletionMutator(mutant_base_test.MutantBaseTest):
    def test_addition_deletion(self):
        self.mutant_diff_test(
            '(+ 1 2)',
            ['1',
             '2'],
            [ArithmeticDeletionMutator],
        )

    def test_many_addition_deletion(self):
        self.mutant_diff_test(
            '(+ f (+ (+ (+ a b) c) d e))',
            ['f',
             '(+ (+ (+ a b) c) d e)',
             '(+ f (+ (+ a b) c))',
             '(+ f d)',
             '(+ f e)',
             '(+ f (+ (+ a b) d e))',
             '(+ f (+ c d e))',
             '(+ f (+ (+ a c) d e))',
             '(+ f (+ (+ b c) d e))'],
            [ArithmeticDeletionMutator]
        )

    def test_mult_and_div_deletion(self):
        self.mutant_diff_test(
            '(/ (* 5 b) 1)',
            ['(* 5 b)', '1', '(/ 5 1)', '(/ b 1)'],
            [ArithmeticDeletionMutator]
        )

    def test_all_arithmetic_deletion(self):
        self.mutant_diff_test(
            '(define (math a b c d)\n  (* (/ c (+ a b)) d))',
            ['(define (math a b c d)\n  (/ c (+ a b)))',
             '(define (math a b c d)\n  d)',
             '(define (math a b c d)\n  (* c d))',
             '(define (math a b c d)\n  (* (+ a b) d))',
             '(define (math a b c d)\n  (* (/ c a) d))',
             '(define (math a b c d)\n  (* (/ c b) d))'],
            [ArithmeticDeletionMutator]
        )

    def test_all_arithmetic_2_deletion(self):
        self.mutant_diff_test(
            '(define (foo a b c) (- 6 (/ (+ 1 2 (* 3 4)) 5)))',
            ['(define (foo a b c) 6)',
             '(define (foo a b c) (/ (+ 1 2 (* 3 4)) 5))',
             '(define (foo a b c) (- 6 (+ 1 2 (* 3 4))))',
             '(define (foo a b c) (- 6 5))',
             '(define (foo a b c) (- 6 (/ 1 5)))',
             '(define (foo a b c) (- 6 (/ 2 5)))',
             '(define (foo a b c) (- 6 (/ (* 3 4) 5)))',
             '(define (foo a b c) (- 6 (/ (+ 1 2 3) 5)))',
             '(define (foo a b c) (- 6 (/ (+ 1 2 4) 5)))'],
            [ArithmeticDeletionMutator]
        )

    def test_empty_list_handling(self) -> None:
        self.mutant_diff_test(
            "'()",
            [],
            [ArithmeticDeletionMutator]
        )
