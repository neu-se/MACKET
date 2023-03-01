#lang racket

(define (extract-private-defs file_name public-def-symbols public-struct-symbols)
    (let ([file (open-input-file file_name)] )
        (extract-defs-helper file public-def-symbols public-struct-symbols)
    )
)

;; returns the list of objects of parsed file to be written out to file
(define (extract-defs-helper file public-def-symbols public-struct-symbols)
    (let
        ([current_line (read-syntax file file)])
        (unless (eof-object? current_line)
            (let [(datum (syntax->datum current_line))]
                (match datum
                    [
                        (list (quote define) (var const_name) _) #:when (and (symbol? const_name) (not (member const_name public-def-symbols)))
                        (writeln datum)
                    ]
                    [
                        (list-rest
                            (quote define)
                            (list-rest (var func_name) _)
                            _
                        ) #:when (not (member func_name public-def-symbols))
                        (writeln datum)
                    ]
                    [
                        (list (quote define-struct) (var const_name) _) #:when (and (symbol? const_name) (not (member const_name public-struct-symbols)))
                        (writeln datum)
                    ]
                    [_ '()]
                )
            )
            (extract-defs-helper file public-def-symbols public-struct-symbols)
        )
    )
)

(provide extract-private-defs)
