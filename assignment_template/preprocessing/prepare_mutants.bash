# Creates the instructor solution file minus what should not be mutated.
# Creates a file with the resulting file to a new subdirectory called
# _mutant_gen.
# This file will be used with the mutant generator to create the mutants
# to analyze the student test cases with. 

# The name of the file that students should submit without a file extension.
# e.g. hw1, hw2, etc.
# This name will be interpolated into the file names of the instructor solution
# (e.g. hw1-instructor-solution.rkt), student implementation (e.g. hw1.rkt), and
# instructor test cases (e.g. hw1-instructor-tests.rkt).
hw_name=$1
# The reader or lang special form that should be used in this assignment.
# When check-expects are extracted from the student implementation and written
# to a file containing only test cases, this reader or lang special form will
# be placed at the top of the file.
reader_directive=$2
mkdir -p _mutant_gen
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cat <(echo "$(grep -E "(#lang|#reader)" reader-directive.txt)") \
    <(racket $SCRIPT_DIR/extract_requires.rkt <(sed -r 's,(#reader.*)|(#lang.*),,;s,require "./provide-hack.rkt",require "../provide-hack.rkt",' $hw_name-instructor-solution.rkt)) \
    <(racket $SCRIPT_DIR/extract_solution_defs.rkt <(sed -r 's/(#reader.*)|(#lang.*)//' $hw_name-instructor-solution.rkt) ) \
    <(racket public-symbols.rkt) > _mutant_gen/$hw_name-instructor-solution.rkt
