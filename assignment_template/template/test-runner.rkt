#lang racket

(require rackunit)
(require al2-test-runner)

(define tests-to-run (make-hash))

(define (test-runner-cmd-line test-suite-wrapper)
    (command-line #:program "Test Runner"
        #:multi
        [
            ("-t" "--include-test") suite_name test_name "Name of test suite and test case to run"
            (hash-set! tests-to-run suite_name
                (append (hash-ref tests-to-run suite_name (list)) (list test_name))
            )
        ]
        #:args ()
        (let ((requested_tests (hash-map tests-to-run (lambda (key value) (cons key value)))))
            (if (empty? requested_tests)
                (run-tests test-suite-wrapper)
                (run-tests #:only requested_tests test-suite-wrapper)
            )
        )
    )
)

(provide test-runner-cmd-line)
