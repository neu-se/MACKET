#!/bin/bash

bash preprocessing/prepare_mutants.bash hwX reader_directive.txt
generate-mutants -p _mutant_gen _mutant_gen/hwX-instructor-solution.rkt hwX-mutants.yml
