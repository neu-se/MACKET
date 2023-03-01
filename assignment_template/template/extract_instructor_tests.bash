bash preprocessing/extract_instructor_tests.bash hwX \
    "$(grep -E "(#lang|#reader)" reader-directive.txt)" \
    > hwX-instructor-tests.rkt
