#lang racket
(require 2htdp/batch-io)

;; returns the list of objects of parsed file to be written out to file
(define (parse-args file num)
    (let 
        ([current_line (read-syntax file file)])
        (if (not (eof-object? current_line))
            (let [(datum (syntax->datum current_line))]
                (if (and (list? datum) (eq? 'check-expect (car datum)))
                    (begin 
                        (display "        (test-case ")
                        (display "\"Test ")
                        (display num)
                        (display " line ")
                        (display (syntax-line current_line))
                        (display "\"")
                        (newline)
                        (display "            ")
                        (writeln (list 'check-equal? (second datum) (third datum)))
                        (displayln "        )")
                        (parse-args file (+ 1 num))
                    )

                    (parse-args file num)
                )
            )
            '()
        )
    )
)

(define (main-helper file_name output)
    (let ([file (open-input-file file_name)])
        (begin 
            (port-count-lines! file)
            (newline)

            (displayln "(define test-suite-wrapper" )
            (displayln "    (test-suite \"Test Suite\"" )
            (parse-args file 1) 
            (displayln "    )")
            (displayln ")")
            (newline)
        )
    )
)

;;writes each test to a separate line at given location
(define (test-separator lot output_file)
    (cond
        [(empty? lot) (values)]
        [(cons? lot) (begin
                        (writeln (first lot) output_file)
                        ;;(newline output_file)
                        (test-separator (rest lot) output_file))])
)

(command-line #:program "Racket check-expect extractor" #:args (input_file) 
    (begin
        (read-accept-reader #t)
        (main-helper input_file '())
    )
)
