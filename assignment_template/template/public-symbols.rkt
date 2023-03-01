#lang racket
;; Populate the lists below with top-level symbols that students are required to
;; define in their implementation. This is used to distinguish between required
;; symbols and student defined helpers used in their test cases when extracting
;; check-expects into test cases.
;;
;; NOTE: You will also need to `provide` these symbols in hwX-instructor-solution.rkt.
;; The struct names should be passed to `struct-out`. For example:
;; ```hwX-instructor-solution.rkt
;; ...
;; (provide
;;    plus
;;    minus
;;    (struct-out thing)
;; )
;; ```
;;
;; For convenience, you can generate the needed provide form by running this module:
;;     racket public-symbols.rkt
;; Add the printed code to the bottom of hwX-instructor-solution.rkt

;; Put function/constant names here
(define public-def-symbols
    (list
        'plus
        'minus
    )
)

;; Put struct names here
(define public-struct-symbols
    (list
        'thing
    )
)

;; DO NOT EDIT BELOW

(provide public-def-symbols public-struct-symbols)

(module+ main
    (displayln
        `(provide
            ,@public-def-symbols
            ,@(map (lambda (struct-symbol) `(struct-out ,struct-symbol)) public-struct-symbols)
        )
    )
)
