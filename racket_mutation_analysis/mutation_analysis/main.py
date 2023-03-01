import argparse
import json
import os
import shutil
import subprocess
import uuid
from collections import Counter
from collections.abc import Collection, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeAlias

import yaml

from racket_mutation_analysis.racket_mutation.schema import (
    FileResultDictionary, GeneratedMutants, Location, Mutant, MutantResult, MutantStatus,
    MutationTestResult, Position
)


class StopAfterFalsePositivesCheck(Exception):
    def __init__(self, false_positives: Sequence[str]):
        self.false_positives = false_positives


def main():
    args = parse_args()
    if args.init:
        with open('mutation_commands.sh', 'w') as f:
            f.write(MUTATION_CMD_SKELETON)
        exit(0)

    with open(args.mutants_file) as f:
        generated_mutants: GeneratedMutants = yaml.load(f, yaml.Loader)

    working_dir = f'mutation_working_dir_{uuid.uuid4().hex}'
    shutil.copytree(
        args.project_root,
        working_dir,
        ignore=shutil.ignore_patterns('mutation_working_dir_*', *args.ignore_pattern)
    )

    try:
        with ChangeDirectory(working_dir):
            runner = MutantRunner(
                generated_mutants,
                timeout=None if args.timeout < 0 else args.timeout,
                stop_after_false_positive_check=args.stop_after_false_positive_check,
                skip_false_positive_check=args.skip_false_positive_check,
                run_tests_in_one_batch=args.run_tests_in_one_batch,
                failfast=args.failfast,
                include_tests=[] if args.include_test is None else args.include_test,
                exclude_tests=[] if args.exclude_test is None else args.exclude_test,
                include_mutants=[] if args.include_mutant is None else args.include_mutant,
                exclude_mutants=[] if args.exclude_mutant is None else args.exclude_mutant,
            )
            file_results = runner.run()
    except StopAfterFalsePositivesCheck as e:
        if not args.keep_working_dir:
            shutil.rmtree(working_dir)

        if e.false_positives:
            print('False positives found in tests:')
            print('\n\t'.join(e.false_positives))
            exit(1)
        else:
            print('No false positives detected')
            exit(0)

    assert isinstance(args.threshold, int)
    mutation_analysis_result: MutationTestResult = {
        'schemaVersion': '1',
        'thresholds': {'high': args.threshold, 'low': args.threshold},
        'projectRoot': str(Path(args.project_root).absolute()),
        'files': file_results,
    }
    mutation_score = make_reports(mutation_analysis_result)

    if not args.keep_working_dir:
        shutil.rmtree(working_dir)

    if mutation_score < args.threshold:
        exit(1)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('mutants_file', help='A YAML file that contains mutant definitions.')

    parser.add_argument(
        '--init', action='store_true',
        help=f'When specified, creates a file called {MUTATION_CMD_SCRIPT_NAME} that will '
             'be run at different stages of mutation analysis and then exits. '
             'The user should add appropriate commands for each stage of mutation '
             'analysis to this file.')

    parser.add_argument('--project_root', '-p', default='.')
    parser.add_argument(
        '--ignore_pattern', '-i', action='append', default=[],
        help='Glob-style patterns of files within project root that should NOT '
             'be copied into the temporary working directory.')

    parser.add_argument(
        '--timeout', '-t', default=10, type=int,
        help='Time limit in seconds for commands (e.g., checking a test for false positives, '
             'running a test case against a mutant). Set to -1 for no time limit. '
             'Note that no time limit is placed on the setup step.'
    )

    false_positive_phase_args = parser.add_mutually_exclusive_group()
    false_positive_phase_args.add_argument(
        '--stop_after_false_positive_check', '--stop_afp', action='store_true', default=False,
        help='When specified, mutation analysis will stop after checking for false positives. '
             'If any false positives were detected, the program will exit nonzero.'
    )
    false_positive_phase_args.add_argument(
        '--skip_false_positive_check', '--sfp', action='store_true', default=False,
        help='When specified, test cases will not be checked for false positives '
             'before being run against mutants.'
    )

    test_running_args = parser.add_mutually_exclusive_group()
    test_running_args.add_argument(
        '--run_tests_in_one_batch', '-b', action='store_true', default=False,
        help='When specified, all valid tests will be run against a mutant in a '
             'single command instead of one at a time.'
    )
    test_running_args.add_argument(
        '--failfast', '-f', action='store_true', default=False,
        help='When specified, mutants will be marked as detected as soon as the first '
             'case fails against it, and no more tests will be run against that mutant.'
    )
    parser.add_argument(
        '--keep_working_dir', '-k', action='store_true', default=False,
        help='When specified, the temporary working directory will not be deleted '
             'after mutation analysis finishes.'
    )

    parser.add_argument(
        '--include_test', '--it', action='append',
        help='Run only the test case(s) listed here '
             '(this argument can be specified multiple times).'
    )
    parser.add_argument(
        '--exclude_test', '--et', action='append',
        help='Do not run the test case(s) listed here '
             '(this argument can be specified multiple times).'
    )

    parser.add_argument(
        '--include_mutant', '--im', action='append',
        help='Run only the mutant(s) listed here '
             '(this argument can be specified multiple times).'
    )
    parser.add_argument(
        '--exclude_mutant', '--em', action='append',
        help='Do not run the mutant(s) listed here '
             '(this argument can be specified multiple times).'
    )

    parser.add_argument(
        '--threshold', '--th', default=100, type=int,
        help='Exit nonzero if the mutation score is lower than this percentage.'
    )

    return parser.parse_args()


def make_reports(result: MutationTestResult) -> float:  # Return the mutation score %
    print('\n========================== SUMMARY ========================')
    status_counts = Counter()
    for filename, file_result in result['files'].items():
        for mutant_result in file_result['mutants']:
            status_counts.update([mutant_result['status']])
            print(f'Mutant {mutant_result["id"]}: {mutant_result["status"]}')
            if mutant_result['status'] == 'Killed':
                print('\tDetected by:', ', '.join(mutant_result['killedBy']))

    num_mutants = sum(status_counts.values())
    num_detected = status_counts["Killed"] + status_counts["Timeout"]
    print()
    print(f'Total mutants: {num_mutants}')
    print(f'# Detected: {num_detected}')
    print(f'# Undetected: {status_counts["Survived"]}')
    print(f'# Skipped: {status_counts["Ignored"]}')
    mutation_score = (num_detected / (num_mutants - status_counts['Ignored'])) * 100
    print(f'Mutation score: {mutation_score:.2f}%')

    json_str = json.dumps(result, indent=2)
    with open('mutants.json', 'w') as f:
        f.write(json_str)

    with open('mutants.html', 'w') as f:
        f.write(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
  <script
    src="https://www.unpkg.com/mutation-testing-elements@1.0.2/dist/mutation-test-elements.js">
  </script>
  <mutation-test-report-app>
    Your browser does not support custom elements. Please use a modern browser.
  </mutation-test-report-app>

    <script>
        document.querySelector('mutation-test-report-app').report = {json_str};
    </script>
</body>
</html>''')

    return mutation_score


class MutantRunner:
    def __init__(
        self,
        generated_mutants: GeneratedMutants,
        *,
        timeout: int | None,
        skip_false_positive_check: bool,
        stop_after_false_positive_check: bool,
        run_tests_in_one_batch: bool,
        failfast: bool,
        include_tests: Collection[str],
        exclude_tests: Collection[str],
        include_mutants: Collection[str],
        exclude_mutants: Collection[str],
    ):
        self.generated_mutants = generated_mutants
        self.timeout = timeout
        self.skip_false_positive_check = skip_false_positive_check
        self.stop_after_false_positive_check = stop_after_false_positive_check
        self.run_tests_in_one_batch = run_tests_in_one_batch
        self.failfast = failfast
        self.include_tests = set(include_tests)
        self.exclude_tests = set(exclude_tests)
        self.include_mutants = set(include_mutants)
        self.exclude_mutants = set(exclude_mutants)

    def run(self):
        self._setup()
        test_names = self._filter_test_names(self._discover_test_case_names())
        if self.skip_false_positive_check:
            false_positives: list[str] = []
        else:
            false_positives = self._false_positives_check(test_names)

        if self.stop_after_false_positive_check:
            raise StopAfterFalsePositivesCheck(false_positives)

        return self._run_tests_with_mutants(
            [name for name in test_names if name not in false_positives]
        )

    def _setup(self):
        print('=================== Running setup ===================', flush=True)
        result = subprocess.run(
            ['bash', MUTATION_CMD_SCRIPT_NAME, 'setup'],
            capture_output=True, errors='surrogateescape'
        )
        print_subprocess_output(result)

        if result.returncode != 0:
            print(f'The setup command exited with status {result.returncode}. Exiting.')
            exit(1)

    def _discover_test_case_names(self):
        print('=================== Running test case discovery ===================', flush=True)
        try:
            result = subprocess.run(
                ['bash', MUTATION_CMD_SCRIPT_NAME, 'discover_tests'],
                timeout=self.timeout,
                capture_output=True,
                errors='surrogateescape',
                check=True,
            )
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            print_subprocess_output(e)
            print('Error in test case discovery.', str(e), 'Exiting.')
            exit(1)

        print_subprocess_output(result)
        return [name.strip() for name in result.stdout.splitlines()]

    def _filter_test_names(self, test_names: Sequence[str]) -> Sequence[str]:
        if self.include_tests:
            test_names = [name for name in test_names if name in self.include_tests]
        if self.exclude_tests:
            test_names = [name for name in test_names if name not in self.exclude_tests]

        return test_names

    def _false_positives_check(self, test_names: Sequence[str]):
        print('=================== Checking for false positives ===================', flush=True)
        false_positives: list[str] = []
        for test_name in test_names:
            print(f'---- Checking test case "{test_name}" ----')
            try:
                result = subprocess.run(
                    ['bash', MUTATION_CMD_SCRIPT_NAME, 'run_test', test_name],
                    check=True,
                    timeout=self.timeout,
                    capture_output=True,
                    errors='surrogateescape'
                )
                print_subprocess_output(result)
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
                print_subprocess_output(e)
                print(f'*** FALSE POSITIVE found in test case "{test_name}" ***')
                print(str(e), flush=True)
                false_positives.append(test_name)

        return false_positives

    def _run_tests_with_mutants(self, test_names: Sequence[str]):
        print('=================== Running remaining tests against mutants ===================',
              flush=True)
        file_results: dict[str, FileResultDictionary] = {}
        for filename, mutations in self.generated_mutants.items():
            mutant_results: list[MutantResult] = []
            for mutant in mutations['mutants']:
                if (mutant['id'] in self.exclude_mutants
                        or self.include_mutants and mutant['id'] not in self.include_mutants):
                    mutant_results.append({
                        'id': mutant['id'],
                        'location': location_to_one_index(mutant['location']),
                        'mutatorName': mutant['mutator_name'],
                        'replacement': mutant['replacement'],
                        'status': 'Ignored',
                        'killedBy': [],
                    })
                    continue

                with InjectMutant(
                    filename, mutant=mutant['mutated_code'], original=mutations['original']
                ):
                    if self.run_tests_in_one_batch:
                        result_info = self._run_tests_in_batch(mutant, test_names)

                    else:
                        result_info = self._run_tests_one_by_one(mutant, test_names)

                    mutant_results.append({
                        'id': mutant['id'],
                        'location': location_to_one_index(mutant['location']),
                        'mutatorName': mutant['mutator_name'],
                        'replacement': mutant['replacement'],
                        'status': result_info.status,
                        'killedBy': result_info.detected_by_tests,
                    })

            file_results[filename] = {
                'language': 'racket',
                'source': mutations['original'],
                'mutants': mutant_results
            }

        return file_results

    def _run_tests_one_by_one(self, mutant: Mutant, test_names: Sequence[str]):
        detected_by_tests: list[str] = []
        timed_out: bool | None = None
        for test_name in test_names:
            print(f'---- Mutant: "{mutant["id"]}", Test case: "{test_name}" ----',
                  flush=True)
            try:
                result = subprocess.run(
                    ['bash', MUTATION_CMD_SCRIPT_NAME, 'run_test', test_name],
                    check=True,
                    timeout=self.timeout,
                    capture_output=True,
                    errors='surrogateescape'
                )
                print_subprocess_output(result)
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
                print(f'*** Test case "{test_name}" '
                      f'DETECTED mutant "{mutant["id"]}" ***')
                print(str(e))
                print_subprocess_output(e)
                detected_by_tests.append(test_name)

                if timed_out is None:
                    timed_out = isinstance(e, subprocess.TimeoutExpired)

                if self.failfast:
                    break

        if timed_out:
            status = 'Timeout'
        elif detected_by_tests:
            status = 'Killed'
        else:
            status = 'Survived'

        return self._MutantDetectionInfo(status, detected_by_tests)

    def _run_tests_in_batch(self, mutant: Mutant, test_names: Sequence[str]):
        status: MutantStatus
        print(f'---- Mutant: "{mutant["id"]}", All valid tests ----',
              flush=True)
        try:
            result = subprocess.run(
                ['bash', MUTATION_CMD_SCRIPT_NAME, 'run_test_batch', *test_names],
                check=True,
                timeout=self.timeout,
                capture_output=True,
                errors='surrogateescape'
            )
            print_subprocess_output(result)
            status = 'Survived'
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            print(f'*** Mutant "{mutant["id"]}" DETECTED ***')
            print(str(e))
            print_subprocess_output(e)

            status = 'Timeout' if isinstance(e, subprocess.TimeoutExpired) else 'Killed'

        return self._MutantDetectionInfo(status)

    @dataclass
    class _MutantDetectionInfo:
        status: MutantStatus
        detected_by_tests: list[str] = field(default_factory=list)


SubprocessResult: TypeAlias = (
    subprocess.CompletedProcess | subprocess.CalledProcessError | subprocess.TimeoutExpired
)


def print_subprocess_output(result: SubprocessResult):
    if result.stdout:
        print('---stdout---')
        print(result.stdout, flush=True)

    if result.stderr:
        print('---stderr---')
        print(result.stderr, flush=True)


MUTATION_CMD_SCRIPT_NAME = 'mutation_commands.sh'
MUTATION_CMD_SKELETON = '''#!/bin/bash
set -e  # Script will exit nonzero if any subcommands fail.

subcmd=$1
if [ $subcmd = "setup" ]; then
    # Add any setup that needs to be run once before any other steps are taken.
elif [ $subcmd = "discover_tests" ]; then
    # Add a command that prints a newline-separated list of test case names.
elif [ $subcmd = "run_test" ]; then
    test_name=$2
    # Add a command that runs the test called $test_name.
fi
'''


class ChangeDirectory:
    """
    Enables moving into and out of a given directory using "with" statements.
    """

    def __init__(self, new_dir: str):
        self._original_dir = os.getcwd()
        self._new_dir = new_dir

    def __enter__(self) -> None:
        os.chdir(self._new_dir)

    def __exit__(self, *args: object) -> None:
        os.chdir(self._original_dir)


class InjectMutant:
    """
    Context manager for replacing a file with a mutated version, then restoring the original file.
    """

    def __init__(self, filename: str, *, mutant: str, original: str):
        self.filename = filename
        self.original = original
        self.mutant = mutant

    def __enter__(self) -> None:
        with open(self.filename, 'w') as f:
            f.write(self.mutant)

    def __exit__(self, *args: object) -> None:
        with open(self.filename, 'w') as f:
            f.write(self.original)


def location_to_one_index(location: Location) -> Location:
    return {
        'start': position_to_one_index(location['start']),
        'end': position_to_one_index(location['end']),
    }


def position_to_one_index(position: Position) -> Position:
    return {
        'column': position['column'] + 1,
        'line': position['line'] + 1,
    }


if __name__ == '__main__':
    main()
