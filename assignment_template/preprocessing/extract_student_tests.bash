# Extract check-expects from a student implementation into rackunit test cases.
# Prints the resulting code to stdout.
# The extracted student tests can be evaluated using mutation testing.

# The name of the file that students should submit without a file extension.
# e.g. hw1, hw2, etc.
# This name will be interpolated into the file names of the instructor solution
# (e.g. hw1-instructor-solution.rkt), student implementation (e.g. hw1.rkt), and
# student test cases (e.g. hw1-tests.rkt).
hw_name=$1
# The reader or lang special form that should be used in this assignment.
# When check-expects are extracted from the student implementation and written
# to a file containing only test cases, this reader or lang special form will
# be placed at the top of the file.
reader_directive=$2


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cat <(echo $reader_directive) \
    <(echo '(require rackunit)') \
    <(echo '(require al2-test-runner)') \
    <(echo '(require "./test-runner.rkt")') \
    <(echo "(require \"./$hw_name-instructor-solution.rkt\")") \
    <(racket $SCRIPT_DIR/extract_requires.rkt <(sed -r 's/(#reader.*)|(#lang.*)//' $hw_name-instructor-solution.rkt)) \
    <(racket $SCRIPT_DIR/extract_private_defs_student.rkt <(sed -r 's/(#reader.*)|(#lang.*)//' $hw_name.rkt)) \
    <(racket $SCRIPT_DIR/extract_check_expects.rkt <(sed -r 's/(#reader.*)|(#lang.*)//' $hw_name.rkt)) \
    <(echo '(test-runner-cmd-line test-suite-wrapper)')
