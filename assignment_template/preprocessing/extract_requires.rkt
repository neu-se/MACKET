#lang racket
(require 2htdp/batch-io)

(define (parse-args file)
    (let 
        ([current_line (read-syntax file file)])
        (unless (eof-object? current_line)
            (let [(datum (syntax->datum current_line))]
                (match datum
                    [
                        (list-rest (quote require) _)
                        (begin 
                            (writeln datum)
                            (parse-args file)
                        )                    
                    ]
                    [_ (parse-args file)]
                )
            )
        )
    )
)

(define (main-helper file_name output)
    (let ([file (open-input-file file_name)] )
        (parse-args file) 
    )
)

(command-line #:program "Racket requires extractor" #:args (input_file) 
    (begin
        (read-accept-reader #t)
        (main-helper input_file '())
    )
)
