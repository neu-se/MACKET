#lang racket
(require "./hw-instructor-solution.rkt")
(require rackunit al2-test-runner)


(define test-suite-wrapper
    (test-suite "Test Suite"
        (test-case "Regular test"
            (check-equal? (add 1 2) 3)
        )

        (test-case "Regular test 2"
            (check-equal? (add 0 2) 2)
        )

        (test-case "Regular test 3"
            (check-equal? (add 2 0) 2)
        )

        (test-case "False positive test"
            (check-equal? (add 1 2) 5)
        )

        (test-case "Timeout test"
            (infloop1)
        )
    )
)

(define (infloop1) (infloop2))
(define (infloop2) (infloop1))

(command-line #:program "Test Runner" #:args (test_name)
    (run-tests
        #:only `(("Test Suite" ,test_name))
        test-suite-wrapper
    )
)
