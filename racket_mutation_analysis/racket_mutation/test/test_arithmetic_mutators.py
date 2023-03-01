from racket_mutation_analysis.racket_mutation.mutators.arithmetic_mut import ArithmeticMutator

from . import mutant_base_test


class TestArithmeticOpMutators(mutant_base_test.MutantBaseTest):
    def test_addition(self):
        self.mutant_diff_test(
            '(+ 1 2)',
            ['(- 1 2)'],
            [ArithmeticMutator],
        )

    def test_many_addition(self):
        self.mutant_diff_test(
            '(+ f (+ (+ (a b) c) d e))',
            ['(- f (+ (+ (a b) c) d e))',
             '(+ f (- (+ (a b) c) d e))',
             '(+ f (+ (- (a b) c) d e))'],
            [ArithmeticMutator]
        )

    def test_subtraction(self):
        self.mutant_diff_test(
            '(- a b)',
            ['(+ a b)'],
            [ArithmeticMutator],
        )

    def test_many_subtraction(self):
        self.mutant_diff_test(
            '(- f (- (- (a b) c) d e))',
            ['(+ f (- (- (a b) c) d e))',
             '(- f (+ (- (a b) c) d e))',
             '(- f (- (+ (a b) c) d e))'],
            [ArithmeticMutator]
        )

    def test_multiplication(self):
        self.mutant_diff_test(
            '(* a b)',
            ['(/ a b)'],
            [ArithmeticMutator],
        )

    def test_many_multiplication(self):
        self.mutant_diff_test(
            '(* f (* (* (a b) c) d e))',
            ['(/ f (* (* (a b) c) d e))',
             '(* f (/ (* (a b) c) d e))',
             '(* f (* (/ (a b) c) d e))', ],
            [ArithmeticMutator]
        )

    def test_division(self):
        self.mutant_diff_test(
            '(/ 1 2)',
            ['(* 1 2)'],
            [ArithmeticMutator],
        )

    def test_many_division(self):
        self.mutant_diff_test(
            '(/ f (/ (/ (a b) c) d e))',
            ['(* f (/ (/ (a b) c) d e))',
             '(/ f (* (/ (a b) c) d e))',
             '(/ f (/ (* (a b) c) d e))', ],
            [ArithmeticMutator]
        )

    def test_add_and_sub(self):
        self.mutant_diff_test(
            '(+ (- 5 b))',
            ['(- (- 5 b))', '(+ (+ 5 b))'],
            [ArithmeticMutator]
        )

    def test_mult_and_div(self):
        self.mutant_diff_test(
            '(/ (* 5 b))',
            ['(* (* 5 b))', '(/ (/ 5 b))'],
            [ArithmeticMutator]
        )

    def test_all_arithmetic(self):
        self.mutant_diff_test(
            '(define (math a b c d)\n  (* (/ c (+ a b)) d))',
            ['(define (math a b c d)\n  (/ (/ c (+ a b)) d))',
             '(define (math a b c d)\n  (* (* c (+ a b)) d))',
             '(define (math a b c d)\n  (* (/ c (- a b)) d))'],
            [ArithmeticMutator]
        )

    # mutators are applied outside in
    def test_all_arithmetic_2(self):
        self.mutant_diff_test(
            '(define (foo a b c) (- 6 (/ (+ 1 2 (* 3 4)) 5)))',
            ['(define (foo a b c) (+ 6 (/ (+ 1 2 (* 3 4)) 5)))',
             '(define (foo a b c) (- 6 (* (+ 1 2 (* 3 4)) 5)))',
             '(define (foo a b c) (- 6 (/ (- 1 2 (* 3 4)) 5)))',
             '(define (foo a b c) (- 6 (/ (+ 1 2 (/ 3 4)) 5)))'],
            [ArithmeticMutator]
        )

    def test_run_simple_arithmetic(self):
        self.complete_test(
            '(+ 1 2)',
            [ArithmeticMutator],
            [('(- 1 2)', '-1')]
        )

    def test_run_simple_arithmetic_method(self):
        self.complete_test(
            '(define (foo a b) \n (+ a b))',
            [ArithmeticMutator],
            [('(define (foo a b) \n (- a b))', '-1')],
            '(foo 1 2)'
        )

    def test_all_run_arithmetic(self):
        self.complete_test(
            '(define (math a b c d)\n  (* (/ c (+ a b)) d))',
            [ArithmeticMutator],
            [('(define (math a b c d)\n  (/ (/ c (+ a b)) d))', '1/4'),
             ('(define (math a b c d)\n  (* (* c (+ a b)) d))', '36'),
             ('(define (math a b c d)\n  (* (/ c (- a b)) d))', '-12')],
            '(math 1 2 3 4)'
        )

    def test_all_2_run_arithmetic(self):
        self.complete_test(
            '(define (foo a b c) (- 6 (/ (+ 1 2 (* 3 4)) 5)))',
            [ArithmeticMutator],
            [('(define (foo a b c) (+ 6 (/ (+ 1 2 (* 3 4)) 5)))', '9'),
             ('(define (foo a b c) (- 6 (* (+ 1 2 (* 3 4)) 5)))', '-69'),
             ('(define (foo a b c) (- 6 (/ (- 1 2 (* 3 4)) 5)))', '43/5'),
             ('(define (foo a b c) (- 6 (/ (+ 1 2 (/ 3 4)) 5)))', '21/4')],
            '(foo 1 2 3)'
        )

    def test_empty_list_handling(self) -> None:
        self.mutant_diff_test(
            "'()",
            [],
            [ArithmeticMutator]
        )
