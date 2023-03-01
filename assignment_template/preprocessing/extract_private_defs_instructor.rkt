#lang racket

;; To be used in local project setup context (i.e., with preprocessing scripts in a subdirectory).
;; Extracts non-public defs (constants, helper methods, structs) that must accompany
;; the instructor check-expects when extracted from the instructor solution.

(require "./extract_private_defs.rkt")
(require "../public-symbols.rkt")

(command-line #:program "Racket instructor private defs extractor" #:args (input_file)
    (begin
        (read-accept-reader #t)
        (extract-private-defs input_file public-def-symbols public-struct-symbols)
    )
)
