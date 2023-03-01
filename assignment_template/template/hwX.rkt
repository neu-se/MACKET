;; Sample student implementation for template assignment. It's test cases
;; are inadequate and should not receive a high mutation score.

#reader(lib "htdp-intermediate-lambda-reader.ss" "lang")((modname hw2) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))

(check-expect (plus 0 0) 0)
(define (plus a b)
    (+ a b)
)

(define (minus a b)
    (- (helper a) b)
)
(check-expect (minus 0 0) 0)

(define (helper a)
    a
)

(define-struct thing [field1 field2])
(define THING1 (make-thing "field1" #false))
(check-expect (thing? THING1) #true)
(check-expect (thing-field1 THING1) "field1")
