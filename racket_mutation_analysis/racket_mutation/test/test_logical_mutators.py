from racket_mutation_analysis.racket_mutation.mutators.logical_mut import LogicalMutator

from . import mutant_base_test


class TestLogicalOperators(mutant_base_test.MutantBaseTest):
    def test_and_mutator(self):
        self.mutant_diff_test(
            '(and #t #f)',
            ['(or #t #f)'],
            [LogicalMutator])

    def test_or_mutator(self):
        self.mutant_diff_test(
            '(or a b)',
            ['(and a b)'],
            [LogicalMutator])

    def test_and_or_mutators(self):
        self.mutant_diff_test(
            '(and (or (and (or #t #f) #t) #f) #t)',
            ['(or (or (and (or #t #f) #t) #f) #t)',
             '(and (and (and (or #t #f) #t) #f) #t)',
             '(and (or (or (or #t #f) #t) #f) #t)',
             '(and (or (and (and #t #f) #t) #f) #t)'],
            [LogicalMutator])

    def test_and_or_mutators_multi_line(self):
        self.mutant_diff_test(
            '(and (or \n(and (or \n#t #f) #t) #f) #t)',
            ['(or (or \n(and (or \n#t #f) #t) #f) #t)',
             '(and (and \n(and (or \n#t #f) #t) #f) #t)',
             '(and (or \n(or (or \n#t #f) #t) #f) #t)',
             '(and (or \n(and (and \n#t #f) #t) #f) #t)'],
            [LogicalMutator])

    def test_complete(self):
        self.mutant_diff_test(
            '(define (logical a b c) (or (and a b) c))',
            ['(define (logical a b c) (and (and a b) c))',
             '(define (logical a b c) (or (or a b) c))'],
            [LogicalMutator])

    def test_non_applicable_mutator(self):
        self.mutant_diff_test(
            '(+ 1 2)',
            [],
            [LogicalMutator])

    def test_and_mutator_run(self):
        self.complete_test(
            '(and #t #f)',
            [LogicalMutator],
            [('(or #t #f)', '#t')])

    def test_and_or_mutators_run(self):
        self.complete_test(
            '(and (or (and (or #t #f) #t) #f) #t)',
            [LogicalMutator],
            [('(or (or (and (or #t #f) #t) #f) #t)', '#t'),
             ('(and (and (and (or #t #f) #t) #f) #t)', '#f'),
             ('(and (or (or (or #t #f) #t) #f) #t)', '#t'),
             ('(and (or (and (and #t #f) #t) #f) #t)', '#f')])

    def test_complete_logical_run(self):
        self.complete_test(
            '(define (logical a b c) (or (and a b) c))',
            [LogicalMutator],
            [('(define (logical a b c) (and (and a b) c))', '#f'),
             ('(define (logical a b c) (or (or a b) c))', '#t')],
            '(logical #t #f #t)'
        )

    def test_empty_list_handling(self) -> None:
        self.mutant_diff_test(
            "'()",
            [],
            [LogicalMutator]
        )
