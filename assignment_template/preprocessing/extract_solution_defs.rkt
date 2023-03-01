#lang racket
(require 2htdp/batch-io)

(define (extract-solution-defs-helper file)
    (let
        ([current_line (read-syntax file file)])
        (unless (eof-object? current_line)
            (let [(datum (syntax->datum current_line))]
                (match datum
                    [
                        (list (quote define) (var const_name) _) #:when (symbol? const_name)
                        (writeln datum)
                    ]
                    [
                        (list-rest
                            (quote define)
                            (list-rest (var func_name) _)
                            _
                        )
                        (writeln datum)
                    ]
                    [
                        (list (quote define-struct) (var struct_name) _)
                        (writeln datum)
                    ]
                    [_ '()]
                )
            )
            (extract-solution-defs-helper file)
        )
    )
)

(define (extract-solution-defs file_name output)
    (let ([file (open-input-file file_name)] )
        (extract-solution-defs-helper file)
    )
)

(command-line #:program "Racket solutions definitions extractor" #:args (input_file)
    (begin
        (read-accept-reader #t)
        (extract-solution-defs input_file '())
    )
)
