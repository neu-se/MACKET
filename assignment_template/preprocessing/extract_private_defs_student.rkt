#lang racket

;; To be used only in autograding context (i.e., all files in one flat directory)
;; Extracts non-public defs (constants, helper methods, structs) needed to run
;; student test cases during mutation testing.

(require "./extract_private_defs.rkt")
(require "./public-symbols.rkt")

(command-line #:program "Racket student private defs extractor" #:args (input_file)
    (begin
        (read-accept-reader #t)
        (extract-private-defs input_file public-def-symbols public-struct-symbols)
    )
)
