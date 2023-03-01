#!/bin/bash
set -e  # Script will exit nonzero if any subcommands fail.

subcmd=$1
if [ $subcmd = "setup" ]; then
    # Add any setup that needs to be run once before any other steps are taken.
    true
elif [ $subcmd = "discover_tests" ]; then
    # Prints a newline-separated list of test case names.
    grep "(test-case" hwX-tests.rkt | sed 's/(test-case//g' | sed 's/"//g'
elif [ $subcmd = "run_test" ]; then
    test_name=$2
    # Runs the test called $test_name.
    raco test ++arg -t ++arg "Test Suite" ++arg "$test_name" hwX-tests.rkt
elif [ $subcmd = "run_test_batch" ]; then
    args="raco test "
    for test in "${@:2}"; do
        args+="$arg ++arg -t ++arg 'Test Suite' ++arg '$test' "
    done
    args+="hwX-tests.rkt"
    eval $args
fi
