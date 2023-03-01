test_name=$1
expected_status=$2

echo "========== Running test $test_name ==========="

bash -c "run-mutants mutants.yml -p . --timeout 3 $(cat $test_name.args) &> $test_name.out"
status="$?"

diff <(sed -r 's/[0-9][0-9]?\.[0-9][0-9]? ms//g' $test_name.out.correct) <(sed -r 's/[0-9][0-9]?\.[0-9][0-9]? ms//g' $test_name.out) || exit 1
if [ $status != $expected_status ]; then
    echo "Expected exit status to be $expected_status, but it was $status"
    exit 1
fi
