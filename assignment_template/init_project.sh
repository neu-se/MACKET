#!/bin/bash

set -e

if [ -z $1 ]; then
    echo "Usage: bash $0 hw_name"
    exit 1
fi

# The name of the file that students should submit without a file extension.
# e.g. hw1, hw2, etc.
# A new directory with this name will be created, and an assignment template
# will be initialized in that directory using this name where necessary.
hw_name=$1

if [ -e $hw_name ]; then
    echo "A file or directory with the name \"$hw_name\" already exists."
    echo "Exiting."
    exit 1
fi

mkdir $hw_name
cp -r preprocessing $hw_name

for file in template/*; do
    sed "s/hwX/$hw_name/g" $file > $hw_name/$(echo $(basename $file) | sed "s/hwX/$hw_name/g")
done


echo "Project initialized. Next steps:"
echo "= Run 'cd $hw_name'"
echo "- Edit reader-directive.txt to contain the reader or lang directive needed for this assignment."
echo "- Add the assignment's public symbols to public-symbols.rkt"
echo "- Run 'racket public-symbols.rkt' and put the printed code at the bottom of $hw_name-instructor-solution.rkt"
echo "- Add your instructor solution and test cases (check-expects) to $hw_name-instructor-solution.rkt"
echo "- Run 'bash extract_instructor_tests.bash' to extract instructor test cases from $hw_name-instructor-solution.rkt into $hw_name-instructor-tests.rkt"
echo "- Run 'bash generate_mutants.bash"
echo "- Run 'make'"
