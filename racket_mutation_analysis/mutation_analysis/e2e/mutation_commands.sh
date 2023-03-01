#!/bin/bash
set -e  # Script will exit nonzero if any subcommands fail.

subcmd=$1
if [ $subcmd = "setup" ]; then
    # Add any setup that needs to be run once before any other steps are taken.
    echo "Hello"
elif [ $subcmd = "discover_tests" ]; then
    # Add a command that prints a newline-separated list of test case names.
    echo "Regular test"
    echo "Regular test 2"
    echo "Regular test 3"
    echo "False positive test"
    echo "Timeout test"
elif [ $subcmd = "run_test" ]; then
    test_name=$2
    # Add a command that runs the test called $test_name.
    raco test ++arg "$test_name" hw-student-tests.rkt
fi
